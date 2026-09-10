---
summary: 해제 책임은 흐름의 대칭이 아니라 그 buffer의 최종 소비자가 정하므로, 다음 writer에게 넘기면 손대지 않고 되돌려받는 흐름이면 직접 해제한다.
created: 2026-08-25
slug: databuffer-release-ownership
tags:
  - 개발/Spring
---

# 코드마다 다른 DataBuffer release

외부 서비스가 파일을 스트리밍으로 반환하고, 그것을 `Flux<DataBuffer>`로 받아 스토리지로 옮기는 API가 둘 있었다. 한쪽 코드에는 `DataBufferUtils.release()`가 있고 다른 쪽에는 없었다.

리뷰에서 걸린다. 여기 해제가 빠진 것 아니냐는 지적이 나온다. 대칭을 맞추려는 직관이 틀리는 경우다.

> [!warning] 양쪽을 같게 맞추는 수정
> 지적에 맞춰 양쪽에 다 넣으면 조기 해제나 이중 해제가 난다. 반대로 둘 다 빼면 풀에서 재사용하는 buffer가 해제되지 않고, 부하가 걸린 뒤에야 leak detector 경고로 드러난다.

## 해제 책임을 정하는 것은 최종 소비자다

해제 책임은 흐름의 모양이 아니라 그 buffer의 최종 소비자가 누구인지가 정한다. 같은 `Flux<DataBuffer>`라도 다음 단계가 무엇이냐에 따라 답이 반대가 된다.

**다음 단계로 넘기는 경우에는 해제하지 않는다.** [`BodyInserters.fromDataBuffers(body)`](https://docs.spring.io/spring-framework/docs/current/javadoc-api/org/springframework/web/reactive/function/BodyInserters.html)로 다음 HTTP 요청의 body에 그대로 연결하면, 이 흐름에서는 HTTP writer에 buffer의 소비와 해제를 맡긴다. 해제 주체는 사용하는 writer 구현과 Spring 버전에서 확인해야 한다. 중간 코드가 release하면 writer가 읽기도 전에 buffer가 해제된다.

**소비하지 않고 되돌려주는 경우에는 해제해야 한다.** [`DataBufferUtils.write(publisher, channel)`](https://docs.spring.io/spring-framework/docs/current/javadoc-api/org/springframework/core/io/buffer/DataBufferUtils.html#write(org.reactivestreams.Publisher,java.nio.channels.AsynchronousFileChannel))은 이름과 달리 buffer를 소비하지 않는다. javadoc은 이 오버로드가 채널을 닫지도 원본 버퍼를 해제하지도 않는다고 설명한다. 같은 buffer를 그대로 다시 발행하는 통과 연산자이므로, 뒤에 `.then()`만 붙이면 아무도 해제하지 않는다.

**원소가 버려질 수 있는 경우에는 버려지는 경로까지 막아야 한다.** `filter`나 `skip`처럼 원소를 걸러내는 연산자, prefetch나 cache처럼 원소를 폐기할 수 있는 연산자를 거치면, 폐기된 buffer는 어느 소비자에도 도달하지 않는다.

문제의 뿌리는 `DataBuffer`가 풀에서 재사용되는 메모리일 수 있는데도 소유권 이전이 타입에 드러나지 않는다는 점이다. `Flux<DataBuffer>`라는 시그니처만 보고는 이것이 넘기는 흐름인지 되돌려받는 흐름인지 알 수 없다. 그래서 리뷰에서 대칭성으로 판단하게 되고, 그 판단이 틀린다.

## 경계마다 묻는 질문

경계마다 이 buffer의 최종 소비자가 누구인지를 묻는다. 다음 writer에게 넘긴다면 손대지 않고, 내가 마지막이라면 해제한다. 두 API의 release 유무가 다른 것은 모순이 아니라 정상이다. 그 이유를 주석 한 줄로 남기면 다음 리뷰가 같은 자리에서 다시 걸리지 않는다.

`write(publisher, channel)`을 쓴다면 반환된 `Flux`에서 해제한다. 체인 안에서는 `.doOnNext(DataBufferUtils::release).then()`을 붙이고, 직접 구독한다면 `DataBufferUtils.releaseConsumer()`를 쓴다.

파일로 내리는 것이 목적이라면 채널을 직접 열지 않는 편이 낫다. `DataBufferUtils.write(source, Path, OpenOption...)` 오버로드는 `Mono<Void>`를 반환한다. 채널을 직접 열고 닫으며 release를 조합하는 코드보다 책임을 한곳에서 다루기 쉽지만, buffer 해제 계약은 사용하는 Spring 버전의 문서와 구현으로 확인한다.

폐기 경로가 있는 체인에는 `doOnDiscard(DataBuffer.class, DataBufferUtils::release)`를 건다. buffer를 비동기 작업이 끝날 때까지 보관해야 한다면 `retain()`으로 소유권을 명시하고, 완료와 오류와 취소 모든 경로에서 해제되도록 한다.

## 확인 범위

`write(publisher, channel)`이 buffer를 해제하지 않는다는 것과 `fromDataBuffers`의 동작은 Spring Framework javadoc과 참조 문서로 확인했다. 두 API의 release 유무가 각각 맞다는 것은 실제 코드에서 buffer의 다음 단계를 따라가며 확인했다. writer가 해제하는 정확한 시점은 사용하는 Spring 버전에서 다시 확인해야 한다.

## 참고 자료

- [Spring Data Buffers and Codecs](https://docs.spring.io/spring-framework/reference/core/databuffer-codec.html) - pooled buffer의 전달·소비·폐기 책임을 한곳에서 설명한다.
