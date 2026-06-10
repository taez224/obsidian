---
title: "W10: 배포 파이프라인 완성"
created: 2026-03-09
tags:
  - project
  - 프로젝트/vizend-qra
type: weekly-review
week: 2026-W10
status: active
---

# W10 (03-03 ~ 03-09) — 배포 파이프라인 완성

## 이번 주 요약

배포 파이프라인의 양 끝단(입구/출구)을 완성하고, 멱등성 + 안정성을 강화한 주. Gallery 이벤트 통합의 핵심 구현.

## 주요 작업

### 사전 검증 (03-03)
- Gallery 배포 가능성 검증 Peer API (#97)
- PackageType workloadType 필터링 (#99, ADR-012)

### EPIC-14 집중 (03-04) — 하루 4이슈
- ArgoCD project 필수/default 금지 검증 (#100, #102)
- namespace 기반 appName 자동 계산 (#101)
- directoryInitStatus 상태 + 실패 재시도 API (#104)

### 파이프라인 양단 완성 (03-05)
- **입구**: DeploymentRequestEvent 핸들러 (#107, US-2.1)
- **출구**: 배포 결과 집계 도메인/유스케이스 (#110, #111, #112)
- manifest 디렉토리 자동 초기화 (#103)

### Gallery 이벤트 통합 (03-06)
- UpdateSubscribeEvent full-spec 변경 감지 (#117-118)
- deploymentGroupKey + attempt 재배포 모델 (#120)
- batch/result dedupe 정합성 (#121)
- DB 스키마 유니크 제약/인덱스 (#96)

### 멱등성 + Undeploy (03-09) — 7이슈
- 3-state disposition 모델 (NEW/DUPLICATE/CONFLICT)
- Route collision 감지
- US-2.6 undeploy git-first 재작성 (#135)
- Sync tracking 확장 (#126)

## 데일리 로그

- [[2026-03-03]] — 배포 가능성 검증, workloadType 필터링
- [[2026-03-04]] — EPIC-14 집중 (4이슈)
- [[2026-03-05]] — 파이프라인 양단 완성
- [[2026-03-06]] — Gallery 이벤트 통합
- [[2026-03-09]] — 멱등성, collision, undeploy

## 회고

> [!check] 잘한 점
> - 03-05에 입구(Event 핸들러)와 출구(결과 집계)를 같은 날 구현하여 전체 사이클 완성
> - 3-state disposition 모델로 단순 idempotency key보다 정교한 중복/충돌 구분 달성

> [!warning] 개선할 점
> - 03-09의 7이슈는 과부하 — 일부는 다음 날로 분산 가능했음

## 핵심 인사이트

- **3-state disposition**: NEW/DUPLICATE/CONFLICT — "같은 요청 재처리"와 "다른 요청 충돌"을 구분
- **git-first undeploy**: Git을 source of truth로 두면 장애 시 Git에서 복구 가능

## 다음 주 방향

→ 레거시 정리, Container Registry 연동, 모니터링 아키텍처 재설계
