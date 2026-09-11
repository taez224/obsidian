---
created: 2026-08-25
updated: 2026-09-11
slug: webflux-file-response-shapes
summary: 같은 외부 서비스를 호출한 세 API에서 파일 응답을 서로 다르게 받은 것은, 응답 다음 단계가 요구하는 것이 달랐기 때문이다.
tags:
  - 개발/Spring
---

# 외부 서비스의 파일 응답을 세 API에서 다르게 받은 이유

회사에서 문서 관리 시스템 구축 프로젝트 중, 한 Spring 기반 서비스에서(이하 Spring) PDF 텍스트 추출, 하이라이트, 분할 세 기능을 PDF 처리 전담 외부 서비스(이하 FastAPI)를 호출했는데, Spring 쪽에서 응답을 받는 형태는 셋 다 달랐다. 하나는 `toFuture()`로 끝나고, 하나는 응답 body를 다음 HTTP 요청에 그대로 잇고, 하나는 임시 파일로 내린 뒤 압축을 풀었다. 겉보기에는 일관성이 없어 보이지만, 각 기능에서 응답을 받은 다음 단계가 무엇을 요구했는지에 따라 형태가 정해졌다.

## 문자열 하나만 필요했던 텍스트 추출

이 기능의 결과는 PDF에서 추출된 문자열 하나였다. 애플리케이션에서 이 값을 하나의 결과로만 썼기 때문에 `Flux<DataBuffer>`로 받을 이유가 없었다. WebClient 응답을 `Mono<String>`으로 받고 `toFuture()`로 `CompletableFuture`에 연결해 나머지 동기 코드와 이었다. `Mono`는 0개 또는 1개의 결과를 발행하는 흐름이고, `toFuture()`는 그 결과를 Reactor 밖으로 넘기는 경계다.

## 내용을 볼 필요가 없었던 하이라이트 PDF

이 기능은 FastAPI에서 만든 PDF를 Spring에서 받아서 오브젝트 스토리지(S3)에 올리는 것으로 이어져야 했다. Spring이 파일 내용을 볼 이유는 없었다. 외부 서비스는 [`StreamingResponse`](https://fastapi.tiangolo.com/advanced/custom-response/)로 body를 조각내 보내고, Spring은 [`toEntityFlux(DataBuffer.class)`](https://docs.spring.io/spring-framework/docs/current/javadoc-api/org/springframework/web/reactive/function/client/WebClient.ResponseSpec.html)로 받아 `Mono<ResponseEntity<Flux<DataBuffer>>>`를 얻는다.

```text
Mono
└─ ResponseEntity 1개
   ├─ 상태·헤더
   └─ body: Flux<DataBuffer>
                 ├─ buffer 1
                 ├─ buffer 2
                 └─ ...
```

응답 객체는 하나지만 그 안의 파일 본문은 여러 `DataBuffer` 조각으로 흐른다. `DataBuffer` 하나가 PDF 한 페이지를 뜻하지는 않는다. 바이너리를 나눈 단위일 뿐이다.

이 body를 [`BodyInserters.fromDataBuffers`](https://docs.spring.io/spring-framework/docs/current/javadoc-api/org/springframework/web/reactive/function/BodyInserters.html)로 S3 PUT 요청의 body에 그대로 연결하면, Spring은 PDF 전체를 `byte[]`로 모으지 않고 받은 조각을 그대로 흘려보낸다. 이 경로에서 중간 코드는 각 `DataBuffer`를 읽지도 버리지도 않으므로 `release()`를 부르지 않는다. buffer를 소비하고 해제하는 쪽은 PUT 요청을 쓰는 HTTP writer다. 해제 책임에 대한 것은 [[코드마다 다른 DataBuffer release|별도의 노트]]로 정리해봤다.

## ZIP을 풀어야 했던 PDF 분할

이 기능에서는 사용자가 Spring에 PDF와 단어 목록을 보내면 FastAPI로 보낸 뒤 단어별 PDF를 만들어 ZIP 하나로 묶어 Spring으로 돌려준다. Spring 쪽에서는 이 ZIP을 풀어 PDF마다 따로 S3에 올리고 메타데이터를 DB에 남겨야 했다. ZIP을 풀어야 했으므로 위처럼 그대로 흘려보낼 수 없었다.

```text
Flux<DataBuffer>
→ 임시 ZIP 파일에 기록
→ ZipInputStream으로 엔트리 순회
→ PDF별 스토리지 업로드
→ 업로드 성공 후 메타데이터 DB 반영
```

임시 파일로 내린 이유는 둘이었다. WebClient의 reactive 수신과 ZIP 해제라는 blocking 작업을 분리할 수 있고, ZIP 전체를 메모리에 모으지 않아도 된다. ZIP 해제와 업로드는 blocking 작업을 별도 실행 경계로 격리하기 위해 `boundedElastic` 스케줄러에서 돌린다. 어디서 돌릴지는 `subscribeOn`과 `publishOn`이 정하는데, `subscribeOn`은 구독이 시작되는 위치를 바꾸고 `publishOn`은 그 지점 이후 downstream 신호를 처리하는 위치를 바꾼다.

업로드처럼 함수 안의 작업이 `Mono`를 반환하면 `map`이 아니라 `flatMap`이 필요하다. `map`은 `Mono<Mono<B>>`를 만들고, `flatMap`은 안쪽 `Mono`를 바깥 흐름에 이어 평탄화한다. 안쪽 작업이 끝나기 전에는 바깥 결과도 끝나지 않고, 안쪽 오류는 바깥 흐름으로 전파된다.

임시 파일 기록에는 [`DataBufferUtils.write`](https://docs.spring.io/spring-framework/docs/current/javadoc-api/org/springframework/core/io/buffer/DataBufferUtils.html)를 썼다. channel을 받는 오버로드는 buffer를 해제하지 않고 그대로 다시 발행하므로 `.doOnNext(DataBufferUtils::release)`를 뒤에 붙였다. 하이라이트 경로와 달리 여기서는 원본 buffer를 다음 writer로 넘기지 않기 때문에 이 코드가 마지막 소비자다. `Path`를 받는 오버로드는 channel 생성·기록·해제·닫기를 안에서 처리하고 `Mono<Void>`를 돌려주므로, 이쪽으로 바꾸면 `Mono.using`은 임시 파일의 생성과 삭제만 맡게 된다.

```java
Mono.using(
    () -> tempZipPath,
    path -> DataBufferUtils.write(body, path).then(unzipAndUpload(path)),
    path -> Files.deleteIfExists(path)
)
```

channel을 직접 여는 현재 구조가 틀린 것은 아니다. `Path` 오버로드는 자원 관리 코드를 줄이는 후보다.

ZIP은 `ZipInputStream`으로 엔트리를 앞에서부터 순서대로 읽는다. 순차 업로드에는 단순하지만 엔트리 크기를 미리 알 수 없다. 엔트리별 `Content-Length`가 필요하거나 병렬로 올리려면 central directory를 읽는 `ZipFile`이 필요한데, 그 차이에 관한 것은 [[스트림 ZIP이 돌려주는 엔트리 크기 -1]] 참조.

## 보류한 대안

- 외부 서비스가 스토리지에 직접 올리고 key 목록만 돌려주는 방식은 Spring의 ZIP 처리를 없애지만, 자격증명을 누가 갖는지, 메타데이터의 정본이 어디인지, 일부만 올라갔을 때 누가 정리하는지를 다시 설계해야 했다. (보안에 민감한 프로젝트라 내맘대로 할 수가 없었다..는 뜻)
- `multipart/mixed`는 ZIP 없이 여러 파일을 순차로 보낼 수 있다. 목록을 미리 몰라도 도착하는 대로 흘릴 수 있지만, Spring 쪽의 streaming multipart 파싱과 실패 처리가 ZIP보다 복잡해진다.
- ZIP 엔트리를 `STORED`로 둘지 `DEFLATED`로 둘지는 PDF의 재압축 이득과 CPU 비용을 검토 후에 정한다.

## 확인 범위

세 형태는 한 프로젝트의 세 기능에서 나온 것이고, 파일 응답을 처리하는 방법을 모두 나열한 것은 아니다. operator와 API의 동작은 Spring Framework와 Reactor의 현재 javadoc, [Data Buffers and Codecs](https://docs.spring.io/spring-framework/reference/core/databuffer-codec.html), Java 21 API 문서로 확인했다.
