---
title: AI 개발 운영체계
created: 2026-07-11
tags:
  - 프로젝트/job-search-2026
  - 커리어/이직
  - AI/에이전트
aliases:
  - AI 엔지니어링 원장
  - AI 활용 경력 근거
---

# AI 개발 운영체계

> [!abstract] 목적
> AI 도구 사용 자체가 아니라, 실제 프로젝트에서 요구사항·맥락·검증·인수인계를 어떻게 구조화했는지 기록한다. 이력서에는 검증된 사실만 가져가고, 팀 생산성이나 품질 향상은 측정 근거가 생기기 전까지 성과로 주장하지 않는다.

## 경력 포지셔닝

> 분산 시스템의 복잡성을 신뢰할 수 있는 운영 흐름으로 정리하고, AI가 만든 결과를 팀이 검증하고 책임질 수 있는 변경으로 전환하는 백엔드·플랫폼 엔지니어

AI를 별도 전문 분야처럼 내세우기보다 다음 두 경험을 하나의 역량으로 연결한다.

1. QRA·Gallery에서 비동기 배포 lifecycle과 운영 안전장치를 설계·구현했다.
2. 같은 프로젝트를 수행하며 AI가 만든 결과를 요구사항, ADR, 코드, 테스트, 실행 결과와 연결하는 개발 운영체계를 반복적으로 다듬었다.

## 검증된 경험

- 약 60일 동안 AI 에이전트를 실제 개발에 지속적으로 사용하며 규칙과 workflow를 개선했다.
- `AGENTS.md`와 경로별 규칙으로 아키텍처·도메인·검증 기준을 필요한 시점에 제공했다.
- 요구사항 정제 → EPIC·이슈 분해 → 구현 → 리뷰 → 검증의 흐름을 반복 가능한 명령과 산출물로 연결했다.
- ADR, 테스트, 실행 로그, E2E 결과를 통해 AI 대화에 머무는 판단을 저장소의 근거로 옮겼다.
- 단일 모델의 결론을 그대로 채택하지 않고 다른 모델의 리뷰와 실제 코드·테스트 결과를 교차 확인했다.
- QRA·Gallery의 full-lifecycle E2E에서 SUBSCRIBE부터 배포, 관측, UNSUBSCRIBE cleanup까지 실제 환경의 상태 변화를 검증했다.
- Gallery MR의 Risk/Rollback, Test Plan, Reviewer Guide, AI Provenance를 통해 사람이 확인한 범위와 리뷰 지점을 명시했다.

> [!note] 사용량 수치의 위치
> [[60일간의 AI 에이전틱 워크플로]]에 기록된 4,737 prompts·521 sessions는 장기간 실험했다는 보조 근거다. 생산성이나 품질 향상을 직접 증명하는 KPI로 사용하지 않는다.

## 저장소 검증 결과

> [!important] 증거 우선순위
> 실제 역량의 근거는 `qra-backend`와 `gallery`의 커밋·규칙·이슈·테스트·E2E 산출물이다. [[60일간의 AI 에이전틱 워크플로]]는 왜 이런 구조를 만들었는지 설명하고, 저장소는 실제로 만들고 사용했는지를 증명한다.

### 0. Hive - 대화형 협업과 초기 가드레일

Hive는 QRA 수준의 AI 개발 운영체계를 갖춘 프로젝트가 아니다. 핵심 기능을 개발하던 시기에는 AI를 설계 대안 탐색, 리팩터링, 문서화에 부분적으로 활용했지만, 어떤 변경이 AI의 도움을 받았는지 커밋 단위로 추적할 수 있는 구조는 없었다. 저장소에 남은 직접 근거는 핵심 구현 이후부터 확인된다.

| 날짜 | 커밋 | 저장소에서 확인한 변화 | 의미와 주장 경계 |
| --- | --- | --- | --- |
| 2025-09-17~10-01 | `08d4c1e` 이후 핵심 구현 커밋 | 멀티테넌시 전략과 모듈의 주요 구현 진행 | 당시 AI를 일부 사용했다는 회고는 있으나, 저장소만으로 기여 범위를 분리할 수 없어 AI 성과로 주장하지 않음 |
| 2025-10-24 | `20c773a` | 루트·모듈별 `CLAUDE.md`에 구조, 빌드·테스트, 변경 금지 규칙 추가 | 반복 설명하던 저장소 맥락을 파일로 고정하기 시작 |
| 2025-12-19 | `a556490` | `AGENTS.md`, 이슈 백로그, 계획 승인 후 구현하는 `resolve-issue` 명령 추가 | 대화형 사용에서 계획·승인·검증 절차가 있는 초기 workflow로 전환 |
| 2025-12-19~22 | `0c69bde`, `e8daab1` | SQL injection 방어와 테스트 보강; 이슈 백로그에 Claude Code 작업 기록 | AI 보조가 실제 보안 수정·테스트 산출물과 연결됐다는 후반부 직접 근거 |

Hive가 보여주는 강점은 “AI로 4주 만에 만들었다”가 아니다. **AI와 대화하며 설계와 구현을 보조받는 것만으로는 맥락 재사용과 결과 검증이 부족하다는 한계를 경험했고, 이후 저장소 규칙과 계획 승인 절차를 만들기 시작했다**는 점이다. 이 경험이 QRA에서 요구사항·이슈·구현·DoD를 잇는 운영체계로 발전했다.

> [!warning] 사용하지 않을 주장
> 과거 발표·블로그 초안의 생산 속도, 실패 0건, 시간 단축 수치는 현재 저장소에서 독립적으로 검증되지 않는다. 외부 이력서와 포트폴리오에는 사용하지 않는다.

### 1. qra-backend - 개발 하네스를 처음 구축

| 날짜 | 커밋 | 저장소에서 확인한 변화 | 증명하는 역량 |
| --- | --- | --- | --- |
| 2026-02-02 | `18f92f2` | `AGENTS.md`, 문서 계층 규칙, ADR, 아키텍처·도메인·로컬 개발 문서, `/sync-domain-docs` 추가 | 암묵지를 AI가 실행할 수 있는 프로젝트 맥락으로 구조화 |
| 2026-02-26 | `c322d0a` | 구현 workflow, Test Architect·Backend Engineer·Code Reviewer 역할, 요구사항·시나리오·이슈 도구 정립 | 요구사항부터 구현·리뷰까지 단계와 역할 설계 |
| 2026-02-27 | `7f5ae78`, `afa0355` | progressive disclosure, observation masking, workspace 산출물과 `/review-implement` 중심으로 context engineering 리팩터링 | 컨텍스트 비용과 세션 drift를 줄이는 운영 설계 |
| 2026-04-15 | `e80158d` | 명령 모음을 재사용 가능한 skill과 reference 구조로 재편하고 DoD·workspace schema를 분리 | 실험을 지속적으로 운영할 수 있는 개발 도구 체계로 전환 |

현재 `qra-backend/.claude/WORKFLOW.md`에는 다음 흐름이 실제 규칙으로 남아 있다.

```text
refine-requirement → create-issue → implement-task → review-implement → submit-mr
```

- 요구사항과 시나리오 문서를 GitLab 이슈의 SSOT와 연결한다.
- `brief.md`, `pipeline-state.json`, `review-report.md`로 세션 간 handoff와 복구 지점을 남긴다.
- AC 매핑, 컨벤션, 진입점, 범위 외 변경, 성능·리소스, 빌드·테스트를 확인한 뒤 DoD를 판정한다.
- 에이전트 팀 실험이 환경에 맞지 않자 병렬 역할 수를 늘리기보다 단일 workflow와 명확한 검증 단계로 단순화했다.

### 2. gallery - 그대로 복사하지 않고 재설계

| 날짜 | 커밋 | 저장소에서 확인한 변화 | 증명하는 역량 |
| --- | --- | --- | --- |
| 2026-05-08 | `57d573137` | Gallery 전용 `WORKFLOW.md`, 규칙·스킬·hooks, GitLab 이슈·MR 템플릿을 54개 파일에 정립 | 기존 하네스를 새 저장소의 SSOT·브랜치·라벨 체계에 맞게 이식 |
| 2026-05-18 | `aafcda425` | 선택적 의사결정 게이트 `spec-drilling`과 코드 매핑·결정 묶음·정합 검증·세 곳 동기화 규칙 추가 | AI 구현 전에 결정 부채를 찾아 사람의 판단으로 닫는 능력 |
| 2026-05-21 | `be8d12de0` | SUBSCRIBE부터 UNSUBSCRIBE까지 연결하는 `full-lifecycle.sh`와 실행 가이드 추가 | 단위 테스트를 넘어 실제 운영 lifecycle을 재현하는 검증 하네스 설계 |
| 2026-05-22 | `542b15bb9` | runtime Secret·DB provisioner resource cleanup 구현 | 하네스를 실제 복합 기능 구현에 적용 |
| 2026-05-22 | `0e2f4ca3f` | db-secret cleanup, provisioner cleanup, 단위 테스트와 full-lifecycle assertion 보강 | 구현 결과를 테스트·스크립트·운영 invariant로 닫는 능력 |

Gallery의 2026-05-08 [[2026-05-08|DevLog]]에서도 QRA의 프로세스 자산을 복사하지 않고 Gallery의 Project ID, 라벨, 이슈 템플릿, AC 어휘와 테스트 전략에 맞게 다시 정립했다고 기록했다.

특히 `.claude/workspace/6/spec-drilling.md`와 `.claude/workspace/15/spec-drilling.md`에는 다음 과정이 실제 산출물로 남아 있다.

- ADR에서 이미 닫힌 결정과 아직 사람의 판단이 필요한 결정을 분리한다.
- 현재 코드의 진입점과 새 동작의 gate를 라인 단위로 매핑한다.
- AC별 구현 위치와 단위·통합·E2E 테스트 경계를 먼저 연결한다.
- 선택한 안뿐 아니라 기각한 대안과 trade-off를 기록한다.
- 이슈, ADR, spec 문서가 함께 바뀌어야 하는 연쇄 영향을 검증한다.
- 외부 DB 보존처럼 구현하지 않아야 할 범위도 negative invariant로 고정한다.

### 3. 실제 기능 전달과 연결된 대표 사례

가장 강한 사례는 **QRA에서 만든 하네스를 Gallery에 재설계하고, runtime Secret·DB provisioning·cleanup lifecycle에 적용한 경험**이다.

1. **요구사항과 책임 경계**: ADR-019에서 앱 Secret, DB credential Secret, 외부 DB 자산의 소유권과 삭제 정책을 구분했다.
2. **구현 전 결정**: Issue #6·#7·#14·#15를 spec-drilling하며 Secret apply gate, 부분 실패, label ownership, cleanup 범위를 코드에 매핑했다.
3. **구현**: runtime Secret 실체화, ArgoCD PreSync DB provisioning, label 기반 cleanup과 live hook resource 삭제를 구현했다.
4. **검증**: 단위 테스트와 manifest 검증에 더해 `full-lifecycle.sh`로 SUBSCRIBE → 자산 생성 → 배포 관측 → UNSUBSCRIBE → cleanup을 연결했다.
5. **운영 invariant**: 생성된 runtime 자산과 GitOps desired state는 제거하되 외부 DB/schema/role과 Tier A 관리 Secret은 보존하도록 검증했다.

이 연결은 AI가 코드를 얼마나 많이 생성했는지가 아니라, **모호한 요구사항을 결정과 코드로 좁히고 실제 환경에서 검증 가능한 결과로 닫는 능력**을 보여준다.

## AI 활용 방식의 발전

| 단계 | 프로젝트 | 당시 방식 | 다음 단계로 이어진 학습 |
| --- | --- | --- | --- |
| 탐색 | Hive | 설계 대안·리팩터링·문서화를 대화형으로 보조받고, 후반에 `CLAUDE.md`와 단일 이슈 명령 도입 | 대화만으로는 맥락과 검증 기준이 세션마다 달라질 수 있음 |
| 체계화 | QRA | 프로젝트 맥락, 요구사항, 이슈, 구현, 리뷰, DoD와 handoff 산출물을 workflow로 연결 | 절차가 많아지는 것보다 필요한 맥락과 검증 게이트를 정확히 두는 것이 중요 |
| 적용·검증 | Gallery | QRA 체계를 저장소 특성에 맞게 재설계하고 spec-drilling, MR 책임 장치, full-lifecycle E2E로 확장 | AI 활용의 가치는 생성량보다 실제 상태 변화와 복구 가능성으로 증명해야 함 |

## 나의 AI 활용 역량

> [!summary] 핵심 정의
> 내 강점은 프롬프트를 잘 쓰는 데 있지 않다. AI가 복잡한 코드베이스에서 반복적으로 일할 수 있도록 맥락과 작업 경계를 설계하고, 그 결과를 사람이 검증하고 책임질 수 있는 엔지니어링 산출물로 바꾸는 데 있다.

| 역량 | 실제로 한 일 | 저장소 증거 |
| --- | --- | --- |
| 맥락 설계 | 아키텍처·도메인·금지 패턴을 `AGENTS.md`, 경로별 규칙, ADR로 분리하고 필요한 시점에만 제공 | qra-backend `18f92f2`, `7f5ae78`, `afa0355` |
| 문제 정의 | 자연어 요구사항의 암묵적 가정·실패 경로를 인터뷰하고 비즈니스 AC와 구현 전 결정으로 좁힘 | `refine-requirement`, Gallery `spec-drilling`, workspace #6·#15 |
| 작업 흐름 설계 | 요구사항 → 이슈 → 구현 → 리뷰 → MR을 단계별 skill과 workspace artifact로 연결 | qra-backend `e80158d`, Gallery `57d573137` |
| 검증 설계 | AC 매핑, 컨벤션, 진입점, 리소스, 빌드·테스트를 DoD로 판정하고 실제 환경 E2E로 확장 | `review-implement`, `be8d12de0`, `0e2f4ca3f` |
| 판단과 단순화 | 에이전트 팀, 테스트 도구와 복잡한 프로토콜을 실험하되 환경에 맞지 않으면 제거·보류 | [[60일간의 AI 에이전틱 워크플로]], [[2026-05-08|DevLog]] |
| 책임 경계 | AI가 만든 설명과 사람이 확인한 범위를 구분하고 위험·롤백·리뷰 지점을 명시 | Gallery MR 템플릿, AI Provenance, Reviewer Guide |

이 역량은 `AI 모델을 개발하는 능력`이나 `AI 기능을 제품에 탑재하는 능력`과는 다르다. 현재 근거로 가장 정확한 표현은 **AI-assisted engineering workflow와 verification harness를 설계하고 실제 플랫폼 개발에 적용한 능력**이다.

## 책임과 인수인계 장치

Gallery의 MR 템플릿에는 `Risk / Rollback`, `Test Plan / Evidence`, `Reviewer Guide`, `AI Provenance`가 포함되어 있다. AI가 설명 초안을 만들 수는 있지만 다음 항목은 사람이 확정하도록 설계했다.

- 어떤 위험 신호를 확인해야 하는가
- 코드와 데이터는 어떻게 되돌릴 수 있는가
- 어떤 테스트와 수동 검증을 실제로 수행했는가
- 리뷰어가 어느 파일과 경로부터 봐야 하는가
- 어떤 AI 도구를 썼고 사람이 어디까지 검토했는가

> [!warning] 확인 상태
> MR #252 본문은 GitLab token 만료로 현재 live 재검증하지 못했다. 로컬 MR 템플릿과 [[AI로 빨라진 개인, 소화하지 못하는 팀]]의 캡처는 확인했으며, 외부 포트폴리오에 사용하기 전 MR 원문을 다시 대조한다.

## 개발 운영체계

| 단계 | 내가 설계한 장치 | 남기는 결과 |
| --- | --- | --- |
| 의도 정제 | 요구사항 인터뷰, 완료 조건, EPIC·이슈 분해 | 구현 가능한 요구사항과 작업 경계 |
| 맥락 제공 | `AGENTS.md`, 경로별 규칙, 도메인 문서, ADR | 아키텍처·용어·금지 패턴의 공통 기준 |
| 구현 운영 | 작업 단위 명령, 작은 diff, 상태 모델 중심 구현 | 리뷰 가능한 코드와 변경 단위 |
| 검증 | 단위·통합 테스트, 교차 리뷰, 실제 환경 E2E | 코드 주장과 대응되는 실행 근거 |
| 인수인계 | Risk/Rollback, Reviewer Guide, AI Provenance | 사람이 확인한 범위와 복구 시작점 |
| 학습 회수 | DevLog, 회고, 실패 원인의 규칙·하네스 반영 | 다음 작업에 재사용할 지식 |

## QRA·Gallery에서의 적용

| 프로젝트 문제 | AI와 함께 수행한 작업 | 사람이 책임진 판단·검증 |
| --- | --- | --- |
| 배포 기능의 서비스 분리 | 코드베이스 탐색, PoC·설계안 비교, 이슈 초안 | QRA 책임 경계, 멀티모듈 구조, 단계별 구현 범위 확정 |
| 비동기 상태 정합성 | 실패 시나리오·대안 탐색, 테스트 후보 생성 | disposition, lineage, lease, Outbox 선택과 상태 전이 검증 |
| ArgoCD·Kubernetes 관측 | API·라이브러리 탐색, 구현·리뷰 보조 | 실제 workload readiness 판정과 재시작 복구 검증 |
| QRA → Gallery 재통합 | 영향 범위 탐색, migration·호출 경계 점검 | 보존할 책임과 제거할 경계, ADR-019 확정 |
| Secret·DB provisioning | 구현 후보와 예외 경로 탐색 | Secret 비노출 경계, PreSync 책임, cleanup·retention 분리 |
| 전체 lifecycle | E2E 스크립트·진단 보조 | 실제 환경의 12개 phase 실행과 실패 원인 확인 |

## 이력서에 사용할 수 있는 주장

- QRA에서 요구사항 정제, 이슈 분해, 구현, DoD 리뷰와 MR 제출을 연결한 AI 개발 workflow를 설계하고 반복 운용했다.
- QRA의 workflow를 Gallery의 GitLab SSOT·브랜치·라벨·테스트 전략에 맞게 재설계했다.
- runtime Secret·DB provisioning·cleanup 구현에서 ADR, spec-drilling, 코드, 테스트와 full-lifecycle E2E를 연결했다.
- AI 산출물을 판단·추적·복구 가능한 변경으로 만들기 위해 workspace artifact와 Risk/Rollback·Reviewer Guide·AI Provenance 경계를 설계했다.
- 에이전트 팀 실패와 검증 누락을 규칙·스킬·DoD·E2E 하네스 개선으로 환류했다.

## 아직 주장하면 안 되는 것

- AI 도입으로 팀 전체 생산성이 향상됐다는 표현
- 리뷰 시간, 결함률, 배포 시간 등이 특정 비율로 감소했다는 표현
- 팀 전체가 같은 workflow를 채택했다는 표현
- AI가 설계나 구현을 자율적으로 완료했다는 표현
- 프롬프트·세션 수를 생산성 지표로 제시하는 표현

## 추가로 확보할 측정 근거

- [ ] 요구사항 정제부터 MR 생성까지 걸린 시간의 전후 비교
- [ ] 리뷰 재작업 횟수와 주요 피드백 유형
- [ ] E2E가 배포 전 발견한 결함과 재발 방지 사례
- [ ] 장애·실패 시 최초 확인 지점과 복구 시간
- [ ] 반복 작업이 명령·규칙·스크립트로 전환된 사례 수
- [ ] 팀원이 실제로 재사용하거나 이어받은 문서·workflow 사례
- [ ] QRA와 Gallery의 GitLab 이슈·MR에서 workflow 산출물이 재사용된 횟수
- [ ] MR #252 원문과 블로그 캡처의 Risk/Rollback·Reviewer Guide·AI Provenance 내용 재대조

## 공개 가능한 대표 글

- [[60일간의 AI 에이전틱 워크플로]] - 실제 프로젝트에 AI workflow를 붙이며 규칙과 검증 체계를 다듬은 과정
- [[AI로 빨라진 개인, 소화하지 못하는 팀]] - 개인의 생성 속도와 팀의 흡수 능력을 구분한 관점
- [[AI 코딩 도구는 이해 부채를 만든다]] - 생성 결과 뒤에 사람의 이해와 판단 역량을 남겨야 하는 이유
- [[AI 시대 플랫폼팀은 어떻게 진화하는가]] - 플랫폼 엔지니어가 조직의 개발·학습 구조를 설계해야 한다는 확장 관점

## 연결된 노트

- [[QRA 프로젝트 정리]] - 실제 시스템과 기술적 기여의 정본
- [[경력 원장]] - 이력서에서 사용할 경력 사실
- [[이력서]] - 외부 제출용 핵심 주장
- [[포트폴리오 구성]] - 주장을 설계 결정과 실행 근거로 검증하는 구조
- [[면접 준비]] - AI 시대의 개발 방식과 책임 경계에 관한 답변
