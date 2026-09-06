---
title: Reactive PDF 파일 처리 파이프라인 스터디
created: 2026-08-25
tags:
  - 개발/Spring
---

# Reactive PDF 파일 처리 파이프라인 스터디

실제로 구현했던 PDF 추출·하이라이트·분할 흐름을 Spring WebFlux와 Reactor 개념으로 다시 설명하기 위한 스터디 노트다.

관련 기록: [[2026-08-25|2026-08-25 DevLog]]

> [!warning] 근거 경계
> 회사 내부 코드는 이 노트로 가져오지 않는다. 구현 흐름은 당시 경험과 내부 코드에서 확인한 operator를 바탕으로 정리하고, 정확한 인자·예외 처리·DB 상태 전이는 확인 전까지 단정하지 않는다.

## 실제 구현 흐름

### 텍스트 추출

```text
Spring WebClient
→ 텍스트 응답
→ toFuture()
→ 하나의 텍스트 결과로 비동기 완료
```

텍스트는 애플리케이션에서 하나의 결과로 사용했기 때문에 `Flux<DataBuffer>`가 아니라 `toFuture()` 경로로 처리했다.

### PDF 하이라이트

```text
FastAPI PDF 처리
→ StreamingResponse
→ Spring WebClient의 Flux<DataBuffer>
→ 별도 서비스에서 S3 URL 발급
→ 발급받은 S3 URL로 PUT
   body: BodyInserters.fromDataBuffers(body)
→ 파일 결과와 메타데이터 처리
```

이 경로에서는 FastAPI의 응답 body를 S3 요청 body로 그대로 전달한다. 따라서 Spring이 각 `DataBuffer`를 직접 해석하거나 버리지 않으며, 중간 코드에서 임의로 `release()`하지 않는다.

### PDF 분할

사용자는 PDF와 단어 목록을 함께 보낸다.

```text
Spring WebClient
→ FastAPI에 PDF + 단어 목록 전달

FastAPI
→ 단어별 매칭 페이지 선택
→ {단어}.pdf 생성
→ 한 페이지가 여러 단어에 매칭되면 각 PDF에 중복 포함
→ 모든 PDF를 ZIP으로 묶음
→ StreamingResponse로 반환

Spring
→ toEntityFlux(DataBuffer.class)
→ Mono<ResponseEntity<Flux<DataBuffer>>>
→ subscribeOn(...)
→ flatMap(...)
→ fileId·파일 메타데이터 생성
→ 임시 ZIP 파일 기록
→ ZipInputStream으로 압축 해제
→ PDF별 S3 업로드
→ 업로드 성공 후 메타데이터 DB 반영
→ SplitPdfResult 반환
```

임시 ZIP 기록 단계에서는 `AsynchronousFileChannel`과 `DataBufferUtils.write`를 사용했고, `DataBufferUtils.write(...).doOnNext(DataBufferUtils::release)`로 write 이후 buffer를 직접 release했다. ZIP 해제와 PDF별 S3 업로드는 ZIP 전체를 FastAPI에서 S3로 곧바로 넘기는 end-to-end streaming 경로가 아니다.

## 개념 지도

| 개념 | 이 흐름에서의 역할 |
| --- | --- |
| `Mono<T>` | 0개 또는 1개의 결과를 발행하는 비동기 흐름 |
| `Flux<T>` | 여러 결과를 순서대로 발행하는 비동기 흐름 |
| `toFuture()` | `Mono` 결과를 `CompletableFuture`로 연결 |
| `StreamingResponse` | FastAPI가 파일 응답 body를 스트림 형태로 내보내는 방식 |
| `toEntityFlux` | 하나의 `ResponseEntity` 안에 `Flux` body를 보존 |
| `DataBuffer` | 파일 전체가 아닌 바이너리 조각 |
| `BodyInserters.fromDataBuffers` | 기존 `Publisher<DataBuffer>`를 새 HTTP 요청 body에 연결 |
| `flatMap` | 내부 비동기 `Mono`를 바깥 흐름에 연결하고 중첩을 평탄화 |
| `subscribeOn` | 구독과 upstream 요청이 시작되는 실행 위치 변경 |
| `publishOn` | 그 이후 downstream 연산의 실행 위치 변경 |
| `boundedElastic` | blocking 작업을 별도 실행 경계로 격리 |
| `AsynchronousFileChannel` | 임시 ZIP 파일에 비동기적으로 기록하기 위한 파일 channel |
| `Mono.fromCallable` | channel open 같은 Callable 실행을 lazy `Mono`로 감쌈 |
| `Mono.using` | resource 생성·사용·cleanup을 하나의 흐름으로 묶음 |
| `DataBufferUtils.write` | `DataBuffer` stream을 파일·channel로 기록 |
| `ZipInputStream` | ZIP entry를 순서대로 읽는 blocking 입력 스트림 |
| `toBodilessEntity` | 업로드 응답 body 없이 상태·헤더만 받음 |
| `then` | 앞 단계의 값은 버리고 완료·오류 신호만 다음 단계로 전달 |

## 이번에 이해한 핵심

### `Mono<ResponseEntity<Flux<DataBuffer>>>` 읽기

```text
Mono
└─ ResponseEntity 1개
   ├─ 상태·헤더
   └─ body: Flux<DataBuffer>
                 ├─ buffer 1
                 ├─ buffer 2
                 └─ ...
```

응답 객체는 하나지만, 그 안의 파일 본문은 여러 `DataBuffer` 조각으로 흐른다. `DataBuffer` 하나가 PDF 한 페이지나 하나의 결과 파일을 뜻하는 것은 아니다.

### `map`과 `flatMap`

```text
map:     Mono<A> → Mono<B>
flatMap: Mono<A> → Mono<Mono<B>>를 Mono<B>로 평탄화
```

S3 업로드나 파일 처리처럼 함수 내부 작업이 `Mono`를 반환하면 `flatMap`이 필요하다. 내부 작업이 완료되기 전에는 바깥 결과도 완료되지 않고, 내부 오류는 바깥 흐름으로 전파된다.

### `subscribeOn`과 `publishOn`

```text
데이터 흐름:    upstream ─────────→ downstream
구독 요청:      upstream ←───────── downstream
```

- `subscribeOn`: 구독과 upstream 요청이 시작되는 위치를 바꾼다.
- `publishOn`: 그 지점 이후 downstream 신호를 처리하는 위치를 바꾼다.

현재 코드에서 확인한 위치는 `toEntityFlux` 이후의 `subscribeOn`, S3 업로드 chain 안의 `publishOn`이다. 두 operator를 사용한 정확한 의도는 위치만으로 단정하지 않는다.

### `DataBuffer` 소유권과 release

| 처리 방식 | release 판단 |
| --- | --- |
| `fromDataBuffers(body)`로 downstream HTTP writer에 그대로 전달 | 현재 중간 코드에서 직접 release하지 않음 |
| `DataBufferUtils.write`로 파일에 기록하고 더 이상 전달하지 않음 | write 이후 release 필요 |
| buffer를 비동기 작업을 위해 보관 | `retain()`과 작업 완료 후 `release()` 검토 |
| filter·skip·cache 등으로 버려질 수 있음 | `doOnDiscard(DataBuffer.class, DataBufferUtils::release)` 검토 |

split API에서 `DataBufferUtils.write(...).doOnNext(DataBufferUtils::release)`를 사용한 이유는, write 이후 원본 buffer를 더 이상 다음 writer로 넘기지 않기 때문으로 이해한다.

### `Path` 오버로드와 `Mono.using`

```java
DataBufferUtils.write(body, tempZipPath)
```

`DataBufferUtils.write(Publisher<DataBuffer>, Path, OpenOption...)`는 파일 기록에 필요한 channel 생성·write·buffer release·channel close를 감싼 편의 API다. 이 오버로드를 사용하면 `Mono.using`은 임시 ZIP 파일의 생성·삭제를 관리하는 역할로 좁힐 수 있다.

```java
Mono.using(
    () -> tempZipPath,
    path -> DataBufferUtils.write(body, path)
        .then(unzipAndUpload(path)),
    path -> Files.deleteIfExists(path)
)
```

현재 수동 `AsynchronousFileChannel` 구조가 틀렸다는 뜻은 아니며, Path 오버로드는 자원 관리 코드를 줄이는 리팩터링 후보이다.

### `ZipInputStream`과 `ZipFile`

- `ZipInputStream`: entry를 앞에서부터 순서대로 읽는다. blocking 스트림이지만 현재 구조처럼 순차 처리에는 단순하다.
- `ZipFile`: central directory를 먼저 읽고 entry 목록·크기·개별 접근을 활용할 수 있다. 병렬 업로드나 entry의 `Content-Length`가 필요할 때 검토할 수 있다.

`ZipInputStream`이 현재 구조에서 잘못된 것은 아니다. `ZipFile` 전환은 성능·병렬성·entry 크기 요구가 실제로 있을 때 판단한다.

## 설계 판단과 보류한 대안

- ZIP을 임시 파일에 기록하면 WebClient의 reactive 수신과 blocking ZIP 해제를 분리할 수 있다.
- ZIP을 메모리의 `byte[]`로 모으지 않아 대용량 ZIP 전체 버퍼링을 피한다.
- FastAPI가 S3에 직접 업로드하고 key 목록만 반환하는 방식은 자격증명·메타데이터 정본·부분 실패 처리의 경계를 다시 설계해야 한다.
- `multipart/mixed`는 ZIP 없이 여러 파일을 전달하는 대안이지만, Spring의 streaming multipart 파싱과 실패 처리가 더 복잡해질 수 있다.
- `ZIP_STORED`와 `ZIP_DEFLATED` 중 무엇이 나은지는 실제 압축 설정과 크기·CPU 측정 전에는 결정하지 않는다.

## 아직 확인할 것

- `Mono.using` cleanup이 성공·오류·취소에서 임시 파일을 모두 삭제하는지
- ZIP 해제와 PDF별 S3 업로드의 정확한 blocking 경계와 `boundedElastic` 적용 범위
- PDF별 업로드가 순차인지 병렬인지, 부분 실패 시 이미 올라간 객체와 DB 상태를 어떻게 처리하는지
- `fileId`와 메타데이터 DB 반영이 S3 업로드 성공 이후 정확히 어떤 상태 전이를 거치는지
- Python ZIP 생성 시 실제 compression 설정과 ZIP entry 이름 인코딩
- `ZipFile` 전환이 필요한 실제 요구사항이 있는지

## 내 말로 설명하기

텍스트 추출은 하나의 문자열 결과가 필요해서 WebClient 호출을 `toFuture()`로 처리했다. PDF 분할은 FastAPI가 단어별 PDF를 만들고 ZIP으로 묶어 `StreamingResponse`로 반환한다. Spring은 이를 `Flux<DataBuffer>`로 받아 임시 ZIP 파일에 기록하고, 압축을 푼 뒤 각 PDF를 S3에 업로드한다. 이 과정에서 파일 처리와 resource cleanup을 Reactor 흐름에 연결하기 위해 `Mono.using`, `Mono.fromCallable`, `AsynchronousFileChannel`, `DataBufferUtils.write`, `ZipInputStream`, `boundedElastic`, `flatMap`을 함께 사용한다.

## 참고 자료

- [FastAPI custom response](https://fastapi.tiangolo.com/advanced/custom-response/)
- [Spring WebClient `toEntityFlux`](https://docs.spring.io/spring-framework/docs/current/javadoc-api/org/springframework/web/reactive/function/client/WebClient.ResponseSpec.html)
- [Spring `BodyInserters.fromDataBuffers`](https://docs.spring.io/spring-framework/docs/current/javadoc-api/org/springframework/web/reactive/function/BodyInserters.html)
- [Spring `DataBufferUtils`](https://docs.spring.io/spring-framework/docs/current/javadoc-api/org/springframework/core/io/buffer/DataBufferUtils.html)
- [Spring Data Buffers and Codecs](https://docs.spring.io/spring-framework/reference/core/databuffer-codec.html)
- [Java `AsynchronousFileChannel`](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/nio/channels/AsynchronousFileChannel.html)
- [Java `ZipInputStream`](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/zip/ZipInputStream.html)
- [Java `ZipFile`](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/zip/ZipFile.html)
- [Reactor `Mono`](https://projectreactor.io/docs/core/release/api/reactor/core/publisher/Mono.html)
