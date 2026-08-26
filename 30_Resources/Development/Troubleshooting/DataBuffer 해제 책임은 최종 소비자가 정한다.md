---
created: 2026-08-25
tags:
  - 개발/트러블슈팅
  - 개발/Java
  - 개발/Spring
---

> [!bug] 문제
> 외부 서비스가 파일을 스트리밍으로 반환하고, 그걸 `Flux<DataBuffer>`로 받아 스토리지로 옮기는 API가 둘 있다. 한쪽 코드에는 `DataBufferUtils.release()`가 있고 다른 쪽에는 없다.
>
> 리뷰에서 걸린다. "여기 해제가 빠진 것 아니냐." 맞춰서 양쪽에 다 넣으면 이번엔 조기 해제나 이중 해제가 난다. 반대로 둘 다 빼면 pooled buffer가 새고, 부하가 걸린 뒤에야 leak detector 경고로 드러난다.
>
> 대칭을 맞추려는 직관이 틀린 경우다.

---

> [!question] 원인
> 해제 책임은 **흐름의 모양이 아니라 그 buffer의 최종 소비자가 누구인지**가 정한다. 같은 `Flux<DataBuffer>`라도 다음 단계가 무엇이냐에 따라 답이 반대가 된다.
>
> **넘기는 경우 — 해제하지 않는다.**
> `BodyInserters.fromDataBuffers(body)`로 다음 HTTP 요청의 body에 그대로 연결하면, 그 요청을 쓰는 downstream writer가 buffer를 소비하고 해제한다. 중간 코드가 release하면 writer가 읽기 전에 풀려버린다.
>
> **소비하지 않고 되돌려주는 경우 — 해제해야 한다.**
> `DataBufferUtils.write(publisher, channel)`은 이름과 달리 buffer를 소비하지 않는다. javadoc이 명시한다 — *does not close the channel ... and does **not** release the data buffers in the source. If releasing is required, then subscribe to the returned `Flux` with a `releaseConsumer()`.* 즉 **같은 buffer를 그대로 재발행하는 통과 연산자**다. 뒤에 `.then()`만 붙이면 아무도 해제하지 않는다.
>
> **버릴 수 있는 경우 — 버려지는 경로까지 막아야 한다.**
> `filter`·`skip`이나 prefetch·cache처럼 원소를 폐기할 수 있는 operator를 거치면, 폐기된 buffer는 어느 소비자에도 도달하지 않는다.
>
> 뿌리는 `DataBuffer`가 pooled 자원인데 **소유권 이전이 타입에 드러나지 않는다**는 점이다. `Flux<DataBuffer>` 시그니처만 보고는 이게 넘기는 흐름인지 되돌려받는 흐름인지 알 수 없다. 그래서 리뷰에서 대칭성으로 판단하게 되고, 그 판단이 틀린다.

---

> [!tip] 해결 방법
> - 경계마다 **"이 buffer의 최종 소비자가 누구인가"** 를 묻는다. 다음 writer에게 넘기면 손대지 않고, 내가 마지막이면 해제한다. 두 API의 release 유무가 다른 것은 모순이 아니라 정상이다. 그 이유를 주석 한 줄로 남기면 다음 리뷰가 다시 걸리지 않는다
> - `write(publisher, channel)`을 쓴다면 반환된 `Flux`에서 해제한다. 체인 안에서는 `.doOnNext(DataBufferUtils::release).then()`, 직접 구독한다면 `DataBufferUtils.releaseConsumer()`
> - **파일로 내리는 게 목적이라면 채널을 직접 열지 않는다.** `DataBufferUtils.write(source, Path, OpenOption...)` 오버로드는 `Mono<Void>`를 반환하고 채널 개폐와 해제를 함께 처리한다. `AsynchronousFileChannel.open` + `Mono.using` + 수동 release가 한 줄로 줄고, 실수할 지점 자체가 사라진다
> - 폐기 경로가 있는 체인에는 `doOnDiscard(DataBuffer.class, DataBufferUtils::release)`를 건다
> - buffer를 비동기 작업 동안 보관해야 하면 `retain()`으로 소유권을 명시하고, 완료·오류·취소 모든 경로에서 해제되게 한다
