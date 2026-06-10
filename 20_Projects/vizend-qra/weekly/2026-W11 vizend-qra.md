---
title: "W11: 레거시 정리 & 모니터링 재설계"
created: 2026-03-16
tags:
  - project
  - 프로젝트/vizend-qra
type: weekly-review
week: 2026-W11
status: active
---

# W11 (03-10 ~ 03-16) — 레거시 정리 & 모니터링 재설계

## 이번 주 요약

기술 부채 대청소 + 모니터링 아키텍처 전면 재설계. 레거시 이벤트/모듈 제거(03-11), Container Registry 연동(03-12~13), 상태 머신→cooldown 전환 + Outbox 패턴(03-15).

## 주요 작업

### 안정화 (03-10)
- NPE 방어 3건, requestId 추적성 추가
- K8S stabilization 토글, Deployer 이메일 암복호화 테스트

### 레거시 대청소 (03-11) — **8개 머지**
- 레거시 이벤트 4종 제거/전환 (#109, #137)
- `qra-client` 모듈 삭제, Vizend convention 적용
- 디렉토리 초기화 로직 이관 (#139)
- Requirements v2 초안 작성

### Container Registry (03-12 ~ 03-13)
- Browse API — Harbor/ECR/NCR 통합 (#142)
- Peer API — Gallery 연동 (#144)
- 스키마 정리 — brochureApiPath 제거 (#145)
- Queued GitOps processing 도입

### 배포 관측 정교화 (03-14)
- Superseded 상태 도입 (#156)
- Deployment lineage 쿼리
- Preemption 로직 단순화

### 모니터링 아키텍처 재설계 (03-15)
- 상태 머신 → cooldown 기반 전환 (#163)
- Leader election 구현
- In-memory backup 제거 → DB 기반 복원 준비
- DeploymentResultOutbox (Outbox 패턴, #113)

### 정리 (03-16)
- 테스트 속도 개선, 구현 현황 추적 문서

## 데일리 로그

- [[2026-03-10]] — NPE 방어, requestId, 이메일 암복호화
- [[2026-03-11]] — 레거시 대청소 (8 머지)
- [[2026-03-12]] — Registry Browse API, Requirements v2 마이그레이션
- [[2026-03-13]] — Registry Peer API, 스키마 정리, Queued GitOps
- [[2026-03-14]] — Superseded 상태, lineage 쿼리
- [[2026-03-15]] — 모니터링 재설계 (상태머신→cooldown, Outbox)
- [[2026-03-16]] — 테스트 속도 개선

## 회고

> [!check] 잘한 점
> - 03-11의 대청소는 이전 주에 새 이벤트 체계를 먼저 구축해뒀기에 가능 — 순서가 중요
> - Outbox 패턴으로 트랜잭션과 이벤트 발행의 원자성 확보
> - 상태 머신→cooldown 전환으로 분산 환경 복잡도 대폭 감소

> [!warning] 개선할 점
> - 주 7일 작업은 지속 불가능 — 03-14(토), 03-15(일) 작업은 주중에 분산할 것

## 핵심 인사이트

- **Outbox 패턴**: DB 테이블에 먼저 기록 → 별도 프로세스가 발행, 트랜잭션 원자성 보장
- **상태 머신 vs cooldown**: 상태 머신은 state explosion 위험, cooldown은 시간 기반 판정으로 분산 환경에 적합
- **Lock → Queue 진화**: lock은 경합 시 실패, queue는 순서 보장

## 다음 주 방향

→ K8s 인프라 최적화, Event enrichment
