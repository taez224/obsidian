---
summary: 낮은 버전의 미적용 마이그레이션을 발견하면 환경별 적용 이력부터 확인한다.
created: 2026-07-15
tags:
  - 개발/Flyway
---

> [!bug] 문제
> 로컬에서는 잘 적용되던 Flyway 마이그레이션이 개발계 배포에서 `Detected resolved migration not applied to database: <version>`으로 부팅 거부.

---

> [!question] 원인
> 두 환경의 마이그레이션 히스토리가 갈렸다. 개발계 DB에는 이미 더 높은 버전이 적용돼 있는데, 새로 추가한 스크립트의 버전 번호가 그보다 낮아 "이미 지나간 버전"으로 판정됨. 브랜치 병합·코드 이관 과정에서 흔히 생기는 상황.

---

> [!tip] 해결 방법
> - 버전을 바꾸기 전에 **어느 환경에 이미 적용됐는지** 확인한다. 아직 공유 환경에 적용하지 않았고 폐기 가능한 로컬 DB만 사용했다면, 로컬 DB를 재생성하는 조건으로 뒤쪽 버전으로 조정할 수 있다. 이미 공유 환경에 적용된 스크립트는 버전·내용을 바꾸지 않고 새 보정 마이그레이션을 검토한다
> - `outOfOrder=true`는 누락된 낮은 버전을 뒤늦게 적용하는 선택이다. 기존 변경과 실행 순서를 바꿔도 안전한지 검증한 뒤 사용한다. 버전 리네임과 outOfOrder 중 하나가 항상 안전한 것은 아니다

---

> [!info] 참고 자료
> - 출처: 비공개 개발 기록 2026-05-06, 2026-04-28
> - [Flyway Versioned migrations](https://documentation.red-gate.com/flyway/flyway-concepts/migrations/versioned-migrations) - 적용된 버전과 변경 이력
> - [Flyway Out Of Order](https://documentation.red-gate.com/fd/flyway-out-of-order-setting-277579015.html) - 낮은 버전의 뒤늦은 적용
