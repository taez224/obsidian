---
summary: 반환된 Future를 기다리는 Async executor의 작업이 끝나지 않을 때 완료·취소 경로를 점검한다.
created: 2026-07-15
slug: spring-async-pool-starvation
tags:
  - 개발/Spring
---

# Spring Async 스레드풀 기아 - 반환한 Future의 완료 경로

외부 시스템의 상태를 관측하는 비동기 작업이 로컬에서는 정상인데 개발계와 운영계에서만 timeout으로 끝났다. 선행 단계인 동기화는 성공하고, 관측 단계는 시작 로그를 한 번 찍은 뒤 멈췄다. manifest와 권한 차이를 전수 비교했지만 거기서는 원인이 나오지 않았다.

## 반환한 Future를 기다리는 경로

당시 개발 기록은 `@Async` 메서드가 반환한 `CompletableFuture`가 완료되지 않아 executor 작업이 끝나지 않는 것을 원인으로 진단했다.

[Spring 6.1.6의 `AsyncExecutionInterceptor`](https://github.com/spring-projects/spring-framework/blob/v6.1.6/spring-aop/src/main/java/org/springframework/aop/interceptor/AsyncExecutionInterceptor.java)는 대상 메서드가 `Future`를 반환하면 executor 안에서 그 결과를 `get()`으로 기다린다. 이 경로에서는 내부 Future가 끝나지 않는 것이 곧 worker 점유로 이어진다. Future 객체가 미완료라는 사실만으로 모든 환경에서 스레드가 점유되는 것은 아니고, 이렇게 결과를 기다리는 경로일 때 문제가 된다.

수정 전 코드에서 관측을 중단하는 경로는 별도의 완료 플래그를 세우고 상태를 정리했지만, 반환한 Future 자체는 끝내지 않았다. 예약해 둔 timeout도 그 플래그가 이미 설정되어 있으면 Future를 완료 처리하지 않고 넘어갈 수 있었다.

이 경로로 worker가 모두 점유되면 이후 작업은 시작하지 못하고 큐에 쌓이는 기아(starvation) 상태가 될 수 있다. 당시 진단도 외부 응답 지연보다 이 대기 경로에 초점을 맞췄다. 로컬은 동시에 도는 작업이 적어 기아가 드러나지 않는다.

여기서 얻은 점검 순서가 하나 있다. 로컬은 되는데 원격만 실패하면 스레드풀과 동시성도 후보에 넣고, 해당 executor의 스레드 이름이 로그에 등장하는지부터 확인한다.

## 고친 방법

중단 경로에서도 결과 Future가 끝나도록 했다. [`CompletableFuture`](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/concurrent/CompletableFuture.html)는 정상 완료와 예외 완료와 취소를 구분하므로, 호출자가 중단을 성공으로 오해하지 않도록 세 경로를 나눠서 끝냈다. 내부에 중첩되어 있던 불필요한 `@Async`는 제거했고, 중단할 때 예약된 timeout 작업도 함께 취소하도록 바꿨다.

같은 스레드 점유는 메모리 증가로도 나타날 수 있다. OOM이 의심되는 상황이라면 스레드 덤프로 교차 확인하는 편이 낫다.

## 확인 범위

`AsyncExecutionInterceptor`의 동작은 Spring 6.1.6 기준으로 확인했다.
