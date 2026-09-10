---
summary: 낮은 버전의 미적용 마이그레이션을 발견하면 환경별 적용 이력부터 확인한다.
created: 2026-07-15
slug: flyway-history-divergence
tags:
  - 개발/Flyway
---

# Flyway 히스토리 분기 - 환경마다 갈린 적용 이력

로컬에서는 잘 적용되던 Flyway 마이그레이션이 개발계에 배포할 때 `Detected resolved migration not applied to database: <version>` 오류를 내며 부팅을 거부했다.

두 환경의 마이그레이션 이력이 갈린 것이 원인이다. 개발계 DB에는 이미 더 높은 버전이 적용되어 있는데, 새로 추가한 스크립트의 버전 번호가 그보다 낮았다. [Flyway는 적용된 버전보다 낮은 스크립트](https://documentation.red-gate.com/flyway/flyway-concepts/migrations/versioned-migrations)를 이미 지나간 버전으로 판정한다. 브랜치를 병합하거나 코드를 이관하는 과정에서 흔히 생기는 상황이다.

## 환경별 적용 이력 확인

> [!warning] 이미 공유 환경에 적용된 스크립트
> 버전 번호부터 고치기 전에 그 스크립트가 어느 환경에 이미 적용되었는지 확인한다. 공유 환경에 이미 적용된 스크립트는 버전과 내용을 바꾸지 않고, 상태를 맞추는 새 보정 마이그레이션을 검토한다.

아직 공유 환경에 적용하지 않았고 폐기해도 되는 로컬 DB만 사용했다면, 로컬 DB를 다시 만드는 것을 조건으로 뒤쪽 버전으로 조정할 수 있다. [`outOfOrder=true`](https://documentation.red-gate.com/fd/flyway-out-of-order-setting-277579015.html)는 누락된 낮은 버전을 뒤늦게 적용하는 선택지다. 다만 기존 변경과 실행 순서가 바뀌어도 결과가 안전한지 검증한 뒤에 써야 한다. 버전 리네임과 outOfOrder 중 어느 하나가 언제나 안전한 것은 아니다.
