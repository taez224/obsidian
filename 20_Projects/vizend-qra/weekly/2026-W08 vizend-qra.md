---
title: "W08: 런타임 모니터링 & 장애 감지"
created: 2026-02-23
tags:
  - project
  - 프로젝트/vizend-qra
type: weekly-review
week: 2026-W08
status: active
---

# W08 (02-17 ~ 02-23) — 런타임 모니터링 & 장애 감지

## 이번 주 요약

프로젝트에서 가장 밀도 높은 주. 런타임 모니터링 인프라 대규모 리팩토링(02-18), 장애 감지 시스템 완성(02-19), Topology API 구현(02-23)까지 핵심 기능 3개를 완성.

## 주요 작업

### SSE 및 모듈 이관 (02-16)
- SSE 모니터링 connection limit 추가
- GitHelper를 qra-feature → qra-proxy로 이관

### 런타임 모니터링 리팩토링 (02-18)
- Pod 모니터링 상세화
- 라이프사이클 하드닝 (M-2, M-3, M-4)
- Pod 실패 분류 통합 (M-10, H-4)
- `@Transactional` → `TransactionTemplate` 전환
- RuntimeWatchTask helper 분리

### 장애 감지 시스템 (02-19) — **가장 밀도 높은 날 (커밋 20+)**
- Sliding-window incident threshold rule engine (#51)
- Notification service adapter with retry (#52)
- K8s manifest schema validation (#71)
- 배포 성공을 consecutive readiness 기반으로 판정
- `qra.*` → `vizend.qra.*` 설정 네임스페이스 마이그레이션

### Topology API (02-23)
- Namespace topology graph + resource detail API (#54)
- ArgoCD 인증 체인 전체 수정 (세션 로그인 → 토큰 캐싱 → RSA 복호화, #73)

## 데일리 로그

- [[2026-02-16]] — SSE 강화, GitHelper 이관
- [[2026-02-18]] — 런타임 모니터링 대규모 리팩토링
- [[2026-02-19]] — 장애 감지 시스템, manifest 검증, SSE 개선
- [[2026-02-20]] — Environment scope guard
- [[2026-02-23]] — Topology API, ArgoCD 인증 수정

## 회고

> [!check] 잘한 점
> - 02-19 하루에 4개 큰 주제를 병행 처리 — ultrawork 병렬 실행의 진가 발휘
> - ArgoCD 인증 체인 3단계 누락을 발견하고 한번에 해결

> [!warning] 개선할 점
> - 02-19의 작업 밀도가 과도 — 커밋 메시지 품질이 다소 하락
> - ArgoCD 인증 이슈는 통합 테스트가 있었다면 더 일찍 발견 가능

## 핵심 인사이트

- **consecutive readiness**: 일시적 ready 상태에 속지 않는 배포 성공 판정
- **sliding-window threshold**: 연속 장애를 시간 윈도우로 판정하는 패턴

## 다음 주 방향

→ 배포 생명주기 관리, 품질 체계 구축
