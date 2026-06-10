---
title: "W07: 안정화 & API 확장"
created: 2026-02-16
tags:
  - project
  - 프로젝트/vizend-qra
type: weekly-review
week: 2026-W07
status: active
---

# W07 (02-10 ~ 02-16) — 안정화 & API 확장

## 이번 주 요약

마이그레이션 직후 안정화 주간. Race condition 수정 → API 확장 → 동시성/멱등성 보강 → CRUD 완성 + 코드 품질 전반 개선.

## 주요 작업

### Race Condition 수정 (02-10)
- `pendingEventRef` race condition으로 인한 이벤트 유실 버그 수정 (#60)
- 서버 재시작 시 Requested 상태 배포 observation 자동 복구

### API 확장 (02-11)
- Dynamic query 지원 (#69)
- GitOps Repository / Container Registry 조회 API (#67)
- Feature 모듈 Vizend 아키텍처 룰 위반 수정

### 동시성 보호 (02-12)
- GitOps 저장소 동시성 보호 + 배포 멱등성 보강 (#46, #47)
- Manifest 검증 강화 (#42)
- JGit 리소스 누수 수정

### CRUD 완성 (02-13)
- GitOps Repository / Container Registry CRUD + 연결 테스트 API (#67, #68)
- qra-proxy 코드 품질 개선, RuntimeWatch RS 추적 버그 수정

## 데일리 로그

- [[2026-02-10]] — Race condition 수정, observation 복구
- [[2026-02-11]] — Dynamic query, 조회 API, 패키지 구조 개선
- [[2026-02-12]] — 동시성 보호, manifest 검증, JGit 누수
- [[2026-02-13]] — CRUD 완성, 연결 테스트, 코드 품질

## 회고

> [!check] 잘한 점
> - 실환경 투입 전에 race condition, 리소스 누수 등 기반 이슈를 선제 해결
> - 멱등성/동시성 테스트를 함께 작성하여 회귀 방지

> [!warning] 개선할 점
> - JGit 리소스 누수는 마이그레이션 시 발견했어야 할 이슈 → 코드 리뷰 강화 필요

## 다음 주 방향

→ 런타임 모니터링 리팩토링, 장애 감지 시스템 구축
