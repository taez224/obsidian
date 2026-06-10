---
title: "W12: K8s 인프라 최적화"
created: 2026-03-22
tags:
  - project
  - 프로젝트/vizend-qra
type: weekly-review
week: 2026-W12
status: active
---

# W12 (03-17 ~ 03-22) — K8s 인프라 최적화

## 이번 주 요약

K8s 인프라 레이어 대폭 최적화. Shared informer 재편으로 API 호출 최소화, Event enrichment로 실패 메시지 설명력 향상, Deployment 상태 기반 서비스 모니터링 완성.

## 주요 작업

### GitOps 안정성 (03-17)
- GitOps 큐 중복 실행 방지 — Batch Dispatch Lease (#171)
- Kollex 배포 제외(EXCLUDED) 상태 도입 (#168)
- K8s Pod namespace batch 최적화 (#167)
- 스레드 풀 튜닝

### Harbor 연동 (03-18)
- 이미지 좌표 기반 image ref 해석 (#56)
- Harbor URL 인코딩 버그 수정 3건
- Harbor 설정/이미지 등록 가이드

### K8s 인프라 재편 (03-19) — **가장 밀도 높은 날 (6이슈)**
- Shared informer/cache 재편 (#178) — **아키텍처 레벨 변경**
- K8S Event on-demand enrichment 1단계 (#184, #185)
- Pod 모니터링 확장 (#54, US-9.1)
- 배포 준비 실패 즉시 기록 (#182)
- K8s client 설정 속성 추가 (#181)

### 마무리 (03-20)
- Event enrichment 2단계 — RuntimeWatchTask 확장 (#187)
- Deployment 상태 기반 서비스 요약 조회 (#173, US-9.2)

## 데일리 로그

- [[2026-03-17]] — GitOps lease, EXCLUDED 상태, namespace batch
- [[2026-03-18]] — Image ref 해석, Harbor 인코딩 수정
- [[2026-03-19]] — Shared informer 재편, Event enrichment, Pod 모니터링
- [[2026-03-20]] — Enrichment 2단계, Deployment 상태 조회

## 회고

> [!check] 잘한 점
> - Shared informer 재편(#178)이 다른 이슈들의 선행 조건 역할 → 적절한 순서 배치
> - Event enrichment를 2단계로 분할 (ArgoCd → RuntimeWatch)하여 점진적 적용
> - ADR-015/016으로 leader-only, 멱등 수렴 원칙을 명문화

> [!warning] 개선할 점
> - 03-19의 6이슈는 여전히 과부하 — 하지만 shared informer가 선행이므로 불가피한 면도 있음

## 핵심 인사이트

- **Shared informer**: watch마다 개별 informer → namespace 단위 공유로 API 호출 대폭 감소
- **On-demand enrichment**: 실패 시에만 K8S Event를 조회하여 부하 최소화하면서 설명력 향상
- **Pod 집계 → Deployment 상태**: 개별 Pod 카운팅보다 K8S Deployment 상태가 서비스 건강도의 더 정확한 지표

## 프로젝트 누적 성과

> [!success] 8주간 달성
> - EPIC 7개 완료, 이슈 80+건 처리
> - 핵심 아키텍처 결정 ADR 7건 문서화
> - Gallery → QRA 마이그레이션 완료
> - 배포 파이프라인 전체 사이클 (요청 → 실행 → 관측 → 결과 집계) 구현
> - 런타임 모니터링 아키텍처 2차 재설계 (상태 머신 → cooldown + leader election)
> - Container Registry 3종 (Harbor/ECR/NCR) 통합
