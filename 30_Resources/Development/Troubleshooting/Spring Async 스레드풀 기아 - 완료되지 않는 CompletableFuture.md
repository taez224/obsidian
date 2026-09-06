---
summary: 반환된 Future를 기다리는 Async executor의 작업이 끝나지 않을 때 완료·취소 경로를 점검한다.
created: 2026-07-15
tags:
  - 개발/Spring
---

> [!bug] 문제
> 외부 시스템 상태를 관측하는 비동기 작업이 로컬에서는 정상인데 개발계·운영계에서만 timeout. 선행 단계(동기화)는 성공하고, 관측 단계는 시작 로그 한 번 찍고 멈춘다. manifest·권한 차이를 전수 비교했지만 무혐의.

---

> [!question] 원인
> 당시 개발 기록은 `@Async` 메서드가 반환한 `CompletableFuture`의 완료 누락으로 executor 작업이 끝나지 않는 것을 원인으로 진단했다. Spring 6.1.6의 `AsyncExecutionInterceptor`는 대상 메서드가 `Future`를 반환하면 executor 안에서 그 결과를 `get()`으로 기다린다. 이 경로에서는 내부 Future의 미완료가 worker 점유로 이어진다. Future 객체가 미완료라는 사실만으로 모든 환경에서 스레드가 점유되는 것은 아니다.
>
> 수정 전 코드에서 관측 중단은 별도의 완료 플래그를 세우고 상태를 정리했지만, 반환한 Future는 끝내지 않았다. 예약된 timeout도 그 플래그가 이미 설정되어 있으면 Future 완료 처리를 건너뛸 수 있었다. 수정에서는 내부 `@Async`를 제거하고 중단 시에도 결과 Future가 끝나도록 했다. 이 경로로 worker가 모두 점유되면 이후 작업은 **시작하지 못하고 큐에 쌓이는 기아(starvation)** 상태가 될 수 있다. 당시 진단도 외부 응답 지연보다 이 대기 경로에 초점을 맞췄다.
>
> 로컬은 동시 작업이 적어 기아가 드러나지 않는다 — **"로컬 OK / 원격만 실패"라면 스레드풀·동시성도 점검**하고, 해당 executor 스레드명이 로그에 등장하는지부터 확인할 것.

---

> [!tip] 해결 방법
> - 중단(stop) 경로에서도 Future를 끝낸다. 정상 완료, 예외 완료, 취소를 구분해 호출자가 중단을 성공으로 오해하지 않게 한다
> - 내부의 불필요한 `@Async` 중첩 제거
> - stop 시 예약된 timeout task도 함께 취소
> - 같은 스레드 점유가 메모리 증가(OOM 의심)와도 연결될 수 있으므로 스레드 덤프로 교차 확인

---

> [!info] 참고 자료
> - 출처: 비공개 개발 기록 2026-05-21. 2026-09-06 수정 전 코드·Spring 6.1.6 소스·수정 커밋을 대조했다. 당시 실행 환경의 스레드 덤프를 다시 확보하거나 장애를 재현한 것은 아니다.
> - [Spring 6.1.6 AsyncExecutionInterceptor](https://github.com/spring-projects/spring-framework/blob/v6.1.6/spring-aop/src/main/java/org/springframework/aop/interceptor/AsyncExecutionInterceptor.java) - 반환된 Future를 기다리는 executor 작업
> - [Java CompletableFuture](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/concurrent/CompletableFuture.html) - 완료·예외·취소의 차이
