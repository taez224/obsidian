---
title: "W09: 배포 생명주기 & 품질 체계"
created: 2026-03-02
tags:
  - project
  - 프로젝트/vizend-qra
type: weekly-review
week: 2026-W09
status: active
---

# W09 (02-24 ~ 03-02) — 배포 생명주기 & 품질 체계

## 이번 주 요약

기능 구현 중심에서 **품질 체계 구축**으로 전환되는 시점. JaCoCo 커버리지, 시나리오 전면 정비, placeholder 문법 전환 등 "코드를 잘 만드는 시스템"을 만드는 작업이 두드러짐.

## 주요 작업

### Placeholder 문법 전환 (02-25)
- `${name}` → `((name))` — 쉘 변수/Helm과의 충돌 방지
- DeploymentFlow에 패키지 버전/설정 관리 추가

### Deployment 생명주기 (02-26)
- 구버전 자동 정리 + 관측 순서 역전 방어 (#77)
- preemption key를 `namespace:serviceName`으로 변경

### 품질 체계 구축 (02-27)
- JaCoCo 커버리지 `-Pcoverage` 선택적 실행 도입
- 파빌리온 내 이름 고유성 검증 (#93, #94)
- Context-engineering 기반 AI 워크플로 업그레이드

### Pre-save 검증 (02-24)
- GitOps/Registry 저장 전 connectivity test API (#74)

## 데일리 로그

- [[2026-02-24]] — Pre-save 연결 테스트 API
- [[2026-02-25]] — Placeholder 문법 전환, DeploymentFlow 확장
- [[2026-02-26]] — Deployment 생명주기 정리
- [[2026-02-27]] — JaCoCo, 이름 고유성, 워크플로 업그레이드

## 회고

> [!check] 잘한 점
> - JaCoCo를 `-Pcoverage` 플래그로 선택적 실행하여 일반 빌드 속도에 영향 없이 커버리지 확보
> - 관측 순서 역전 방어는 분산 시스템의 핵심 이슈를 선제 대응

> [!warning] 개선할 점
> - 시나리오 문서 정비에 시간 소요 — 자동화 여지 있음

## 핵심 인사이트

- **관측 순서 역전**: 분산 시스템에서 이벤트 순서 보장 불가 → preemption key로 판정 단위 특정
- **placeholder `((name))`**: 이중 괄호는 쉘, Helm, Mustache 등 기존 문법과 충돌 없음

## 다음 주 방향

→ Gallery 이벤트 통합 (Subscribe/Update/Unsubscribe), 배포 파이프라인 완성
