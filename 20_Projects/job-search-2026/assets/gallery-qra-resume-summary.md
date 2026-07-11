---
title: Gallery QRA 이력서 raw summary
created: 2026-07-11
tags:
  - 프로젝트/job-search-2026
  - 커리어/이직
  - 개발/플랫폼
type: evidence
status: raw
aliases:
  - gallery-qra-resume-summary
---

# Gallery + qra-backend 이력서/경력기술서 raw summary

> [!warning] 정본이 아닌 조사 자료
> 이 문서는 초기 조사 결과와 문장 후보를 보존한다. `qra-backend는 ADR/POC 중심`이라는 아래 초기 판단은 실제 Git 이력과 소스 확인 결과 부정확했다. 외부 제출용 내용은 [[QRA 프로젝트 정리]]를 사용한다.

작성 기준: `/Users/taez/Projects/nextree/vizend/gallery`, `/Users/taez/Projects/nextree/vizend/qra-backend` 현재 repo 증거.

초기 주의 문구(폐기): qra-backend를 ADR/POC/계약 설계 성과로만 제한하려 했으나, 실제로는 QRA 프로젝트에서 배포 오케스트레이션·관측·런타임 모니터링·동시성 제어·결과 집계를 구현했고 이후 Gallery로 이관·확장했다.

작성 전략:

- 국내 빅테크/대기업 수시 채용용으로는 단순 구현 나열보다 Challenge-Action-Result(CAR) 구조를 우선한다.
- 정량 수치가 확인되지 않은 성과는 과장하지 않고 "자동화", "회귀 위험 감소", "운영 경계 명확화", "수동 절차 제거 기반 마련"처럼 증거 가능한 표현으로 제한한다.
- ATS/LLM 파서 대응을 위해 표준 기술명(Kubernetes, ArgoCD, GitOps, Secret management, DB provisioning, E2E validation, AI-driven programming)을 본문에 자연스럽게 포함한다.
- "AI 사용" 자체가 아니라 issue lifecycle, workspace artifact, DoD review, E2E harness를 설계한 engineering productivity 성과로 표현한다.

## Professional Summary 초안

Kubernetes, ArgoCD, GitOps 기반 구독형 서비스 배포 자동화와 runtime Secret/DB provisioning 영역을 설계·구현한 백엔드 엔지니어. Gallery 백엔드에서 구독 시점 Secret 입력, AES 기반 저장, K8s Secret 실체화, ArgoCD PreSync DB provisioning, unsubscribe cleanup boundary, full-lifecycle E2E validation을 연결해 운영 자동화 경로를 구축했다. qra-backend에서는 ADR-019, PreSync DB provisioning POC, subscription secret contract를 정리해 Gallery-Qra 재통합 이후 구현 기준을 마련했다. 또한 AI-driven programming을 일회성 코드 생성이 아니라 issue lifecycle, DoD review, workspace artifact, E2E harness로 구조화해 반복 가능한 개발 검증 체계로 운용했다.

## Core Technical Skills 초안

- Backend: Java 21, Spring Boot, Gradle, JPA, Flyway
- Platform: Kubernetes, ArgoCD, GitOps, K8s Secret, Kubernetes Job, PreSync Hook
- Reliability: deployment observation, lifecycle cleanup, label selector, idempotent workflow, E2E validation
- Security: Secret management, AES encryption, redaction, sensitive payload isolation, runtime secret materialization
- Database: PostgreSQL, DB provisioning, schema/role automation, database-per-Kollex, schema-per-Drama
- Engineering Workflow: AI-driven programming, agent workflow design, spec drilling, DoD review, E2E harness, build output masking

## 1. Subscription Runtime Secret 자동화

### 해결한 문제

구독자가 입력한 민감값을 GitOps repo나 Kafka payload에 싣지 않고, 구독 흐름 안에서 안전하게 K8s Secret으로 실체화해야 했다.

### 설계/구현/검증

- `runtimePrerequisites.secrets`로 publisher가 필요한 Secret metadata를 선언.
- `subscriptionSecrets`로 구독자가 value를 입력.
- Secret value는 subscription store에 AES 암호화 저장.
- 배포 직전에만 K8s Secret으로 실체화하고 GitOps에는 Secret 이름만 남김.
- required/unknown/duplicate key 검증, `toString` redaction, JPA round-trip 테스트, runtime secret plan resolver 테스트로 검증.

### 기술/키워드

Secret management, Kubernetes Secret, AES, ValueEncryptor, GitOps 비경유 Secret, contract validation, redaction.

### 이력서 bullet 초안

- 구독 시점 Secret 입력부터 AES 저장, 서버 검증, K8s Secret 실체화까지 이어지는 runtime secret 자동화 경로를 설계·구현하여 GitOps/Kafka payload의 민감값 노출을 제거.

### 면접 1분 버전

기존 배포 흐름은 manifest 중심이라 Secret value를 어디에 둘지가 문제였습니다. 저는 Secret metadata와 value를 분리하고, value는 subscription store에 AES로 저장한 뒤 배포 직전에 K8s Secret으로 apply하는 구조를 잡았습니다. GitOps에는 Secret 이름만 남기고 값은 남기지 않게 했고, required/unknown key 검증과 마스킹 테스트로 운영 중 누출 가능성을 줄였습니다.

## 2. DB Provisioning + ArgoCD PreSync

### 해결한 문제

구독 후 사람이 DB, schema, role, DB credential Secret을 수동 준비해야 하는 병목이 있었다.

### 설계/구현/검증

- ArgoCD PreSync Hook + Kubernetes Job 기반 provisioning 경로를 설계.
- Bootstrap/Reconcile wave로 DB 생성, schema/role 준비, workload 기동 순서를 분리.
- `ProvisionerManifestAction`으로 workload manifest와 provisioner manifest를 같은 GitOps 흐름에 묶음.
- PostgreSQL engine gate, unsupported engine reject, manifest determinism, RBAC/ConfigMap/Secret reference를 테스트로 검증.

### 기술/키워드

ArgoCD PreSync Hook, Kubernetes Job, GitOps, PostgreSQL, DB provisioning, database-per-Kollex, schema-per-Drama.

### 이력서 bullet 초안

- ArgoCD PreSync Hook 기반 DB provisioning 파이프라인을 도입해 구독 시 DB/schema/role 및 DB credential Secret 생성을 GitOps 배포 흐름에 통합.

### 면접 1분 버전

구독 즉시 배포가 되려면 앱뿐 아니라 DB도 준비돼야 했습니다. 저는 GitOps commit에 workload manifest와 provisioner Job manifest를 함께 묶고, ArgoCD PreSync wave로 DB 생성, schema/role reconcile, workload 기동 순서를 보장했습니다. PostgreSQL v1 경로는 테스트로 manifest, wave, Secret 주입, unsupported engine reject까지 검증했습니다.

## 3. GitOps/ArgoCD 배포 관측과 Cleanup 경계

### 해결한 문제

ArgoCD sync 성공만으로 실제 배포 성공을 판단하기 어렵고, unsubscribe 시 어떤 자산을 지우고 어떤 자산을 보존할지 경계가 불명확했다.

### 설계/구현/검증

- ArgoCD health와 K8s pod stabilization을 함께 보는 관측 흐름 보강.
- PreSync Bootstrap/Reconcile Job 실패를 Kollex/Drama 단위로 분리 판정.
- runtime Secret, DB credential Secret, provisioner hook resource를 label selector 기반으로 정리.
- 외부 DB/schema/role은 보존하는 cleanup boundary를 ADR과 E2E로 고정.

### 기술/키워드

ArgoCD observation, Kubernetes labels/selectors, lifecycle cleanup, GitOps prune, runtime boundary.

### 이력서 bullet 초안

- ArgoCD sync 이후 Deployment health와 K8s 안정화까지 확인하는 관측 흐름과 label selector 기반 cleanup을 정비해 구독 해지 시 runtime 자산은 제거하고 외부 DB 자산은 보존하는 운영 경계를 구현.

### 면접 1분 버전

ArgoCD sync가 끝났다고 서비스가 준비됐다고 볼 수 없어서, ArgoCD health와 K8s pod 안정화 조건을 분리해 관측했습니다. 반대로 unsubscribe에서는 Secret, Deployment, provisioner hook resource는 지우되 DB/schema/role은 보존하는 정책을 label selector와 E2E invariant로 고정했습니다.

## 4. Full Lifecycle E2E 검증 자동화

### 해결한 문제

runtime secret, DB provisioner, cleanup이 각각은 맞아도 실제 subscribe-to-unsubscribe 흐름에서 함께 깨질 수 있었다.

### 설계/구현/검증

- `full-lifecycle.sh`로 SUBSCRIBE -> runtime secret/DB provisioning -> outbox 완료 신호 -> UNSUBSCRIBE -> cleanup/preservation invariant를 검증.
- K8s Secret labels, DB/schema/role 존재, Pod env 주입, ArgoCD prune, cleanup 결과를 한 흐름에서 확인.
- false positive를 줄이기 위해 fresh state cleanup과 production UI gate에 가까운 outbox 완료 조건을 사용.

### 기술/키워드

E2E automation, lifecycle validation, Kubernetes, PostgreSQL, ArgoCD, GitOps, shell automation.

### 이력서 bullet 초안

- 구독부터 해지까지 runtime secret, DB provisioning, ArgoCD prune, cleanup invariant를 한 번에 검증하는 full-lifecycle E2E 스크립트를 구축해 회귀 위험을 낮춤.

### 면접 1분 버전

단위 테스트만으로는 GitOps, ArgoCD, K8s, DB가 만나는 지점의 문제를 잡기 어렵습니다. 그래서 실제 SUBSCRIBE API를 호출하고, Secret/DB/schema/role/Pod env/outbox/cleanup까지 검증하는 E2E를 만들었습니다. cleanup에서는 지워야 할 자산과 보존해야 할 외부 DB 자산을 동시에 assert합니다.

## 5. qra-backend ADR-019 / PreSync / Secret Contract 정리

### 해결한 문제

Qra 분리 구조에서 Gallery 재통합 이후 DB/Secret 책임 경계를 다시 정의해야 했다.

### 설계/구현/검증

- ADR-019에서 Gallery/Qra 재통합 전제의 책임 경계를 재정의.
- DB는 ArgoCD PreSync Hook + Kubernetes Job, 앱 Secret은 subscription store 기반 실체화로 분리.
- local PreSync DB provisioner POC guide 작성.
- `SubscribeTargetsResponse`, `SecretKeyMeta`, `subscriptionSecrets`, `@FieldEncrypted` 저장 계약을 설계.

### 기술/키워드

ADR, platform architecture, ArgoCD PreSync POC, API contract, Secret contract, DB provisioning.

### 이력서 bullet 초안

- Gallery-Qra 재통합 전제에서 DB provisioning과 subscription secret 계약을 ADR/POC/구현 로드맵으로 재정의해 이후 Gallery 구현의 기준선을 마련.

### 면접 1분 버전

qra-backend에서는 코드 구현보다 결정 정리가 핵심이었습니다. Qra가 별도 서비스일 때의 Secret 전달 모델을 재통합 전제에 맞게 재해석했고, DB는 PreSync Job, 앱 Secret은 subscription store 기반으로 분리했습니다. 이 결정이 Gallery 구현의 ADR-019 경로로 이어졌습니다.

## 부가. AI-driven Engineering Workflow / Harness 설계

### 해결한 문제

AI agent를 단순 코드 작성 보조로 쓰면 맥락 누락, 검증 생략, 세션 간 drift가 생기기 쉽다. Gallery 작업에서는 이슈 정제, spec drilling, 구현, 리뷰, MR 준비, E2E 실행을 일관된 절차와 산출물로 연결할 필요가 있었다.

### 설계/구현/검증

- `refine-requirement -> create-issue -> spec-drilling -> implement-issue -> review-implement -> submit-mr -> promote-release` 형태의 issue lifecycle skill chain을 정리.
- `.claude/workspace/{iid}/brief.md`, `spec-drilling.md`, `review-report.md`, `pipeline-state.json` 산출물 convention을 정의해 세션 간 handoff를 가능하게 함.
- `review-implement`에서 AC 매핑, 코드 변경 분석, 빌드 검증, 컨벤션 수집을 병렬 phase로 나누고 DoD 판정으로 수렴.
- `implement-issue` pipeline lead에서 Test Architect, Backend Engineer, Code Reviewer 역할을 분리하고, context isolation/build output masking/pipeline-state 갱신 규칙을 둠.
- `full-lifecycle-e2e` Codex skill을 만들어 preflight, streaming execution, phase label, failure triage, validated invariant를 고정해 E2E harness를 재현 가능하게 함.

### 기술/키워드

AI-driven programming, agent workflow design, development harness, skill chain, context isolation, DoD automation, E2E harness, build output masking, knowledge capture.

### 이력서 bullet 초안

- AI agent 기반 개발 워크플로를 issue lifecycle, workspace artifact, DoD review, E2E harness로 구조화해 세션 간 handoff와 반복 검증이 가능한 개발 운영 체계를 설계.

### 면접 1분 버전

AI를 단순히 코드 생성에 쓰면 결과가 세션마다 흔들리기 쉽습니다. 저는 Gallery 작업에서 요구사항 정제, spec drilling, 구현, 리뷰, MR 준비를 skill chain으로 나누고, 각 단계가 남기는 산출물을 `.claude/workspace`에 고정했습니다. 또 full-lifecycle E2E는 Codex skill로 만들어 preflight, streaming 실행, phase별 의미, 실패 진단까지 표준화했습니다. 그래서 AI-assisted 개발을 일회성 프롬프트가 아니라 재현 가능한 engineering harness로 다루었습니다.

## 최종 이력서 Bullet

- Kubernetes/ArgoCD/GitOps 기반 구독 배포 흐름에서 runtime Secret value를 Git/Kafka payload에서 분리하고, AES 저장 후 배포 직전 K8s Secret으로 실체화하는 Secret management 경로 설계·구현.
- `runtimePrerequisites`와 `subscriptionSecrets` 계약을 정의하고 required/unknown/duplicate key 검증, redaction, JPA round-trip 테스트를 추가해 구독 시점 Secret 입력의 서버 측 안전성을 확보.
- ArgoCD PreSync Hook + Kubernetes Job 기반 DB provisioning을 도입해 구독 시 DB/schema/role 및 DB credential Secret 생성을 GitOps 배포 파이프라인에 통합.
- workload manifest, DB provisioner manifest, runtime Secret apply, Git push, ArgoCD sync를 하나의 배포 흐름으로 묶고 실패 단계별 timeline/관측 경로를 정비.
- ArgoCD health와 K8s stabilization을 함께 보는 배포 관측 로직을 보강하고, PreSync Bootstrap/Reconcile Job 실패를 구독/Drama 단위로 분리 판정하도록 테스트화.
- 구독 해지 시 runtime Secret, DB credential Secret, provisioner hook resource, GitOps desired-state manifest를 label selector 기반으로 정리하면서 외부 DB/schema/role은 보존하는 cleanup boundary 구현.
- SUBSCRIBE -> runtime secret/DB provisioning -> deployment observation -> UNSUBSCRIBE -> cleanup invariant를 검증하는 full-lifecycle E2E 스크립트를 구축해 운영 회귀를 자동 검증.
- AI agent 기반 개발 워크플로를 issue lifecycle, workspace artifact, DoD review, E2E harness로 구조화해 세션 간 handoff와 반복 검증이 가능한 개발 운영 체계를 설계.

## ATS/CAR 친화 이력서 Bullet

- 구독형 서비스 배포에서 Secret value가 GitOps repo와 Kafka payload에 노출될 수 있는 구조적 위험을 해결하기 위해, metadata/value를 분리한 `runtimePrerequisites`/`subscriptionSecrets` 계약과 AES 저장, K8s Secret 실체화 흐름을 설계·구현.
- 구독 시점 runtime Secret 입력의 신뢰성을 높이기 위해 required key 누락, unknown key, duplicate key, value redaction, JPA round-trip을 검증하는 서버 측 contract test를 구축.
- 수동 DB 준비가 필요한 배포 병목을 줄이기 위해 ArgoCD PreSync Hook과 Kubernetes Job 기반 DB provisioning 경로를 설계하고, DB/schema/role 및 DB credential Secret 생성을 GitOps 배포 흐름에 통합.
- workload manifest와 DB provisioner manifest, runtime Secret apply, Git push, ArgoCD sync를 하나의 lifecycle로 연결해 배포 흐름의 책임 경계와 실패 진단 지점을 명확화.
- ArgoCD sync 성공만으로는 부족한 배포 판정을 보강하기 위해 Deployment health, K8s pod stabilization, PreSync Job failure fan-out을 함께 보는 observation 흐름을 정비.
- 구독 해지 시 제거 대상과 보존 대상을 분리하기 위해 label selector 기반 runtime Secret/DB credential Secret/provisioner hook cleanup을 구현하고, 외부 DB/schema/role 보존 boundary를 E2E invariant로 고정.
- SUBSCRIBE부터 UNSUBSCRIBE까지 Secret materialization, DB provisioning, ArgoCD prune, cleanup boundary를 한 번에 검증하는 full-lifecycle E2E harness를 구축해 분산된 운영 회귀를 자동 검증.
- AI-driven programming을 단발성 코드 생성이 아니라 issue lifecycle, spec drilling, workspace artifact, DoD review, build output masking, E2E harness로 구조화해 반복 가능한 개발 검증 체계를 설계.

## CAR 상세 예시

### Runtime Secret 자동화

- Challenge: 구독자가 입력한 API token/password류 Secret value를 GitOps manifest나 Kafka event payload에 싣지 않으면서도 배포 시점에는 K8s runtime Secret으로 사용할 수 있어야 했다.
- Action: `runtimePrerequisites.secrets` metadata와 `subscriptionSecrets` value를 분리하고, subscription store AES 저장 -> 배포 직전 K8s Secret apply -> Deployment envFrom reference 흐름을 설계·구현했다.
- Result: GitOps repo와 event payload에서 민감값을 제거하고, catalog 기반 검증과 redaction test로 Secret handling의 운영 안전성을 확보했다.

### DB Provisioning 자동화

- Challenge: 구독 후 DB/schema/role/DB credential Secret 준비가 수동 절차로 남아 있으면 "구독 즉시 배포" UX와 운영 재현성이 깨진다.
- Action: ArgoCD PreSync Hook + Kubernetes Job 기반 provisioning manifest를 workload manifest와 같은 GitOps 흐름에 묶고, Bootstrap/Reconcile wave로 DB 생성과 Drama별 schema/role/Secret 생성을 분리했다.
- Result: 구독 배포 과정에서 DB provisioning을 선언형 배포 lifecycle에 편입했고, PostgreSQL engine gate와 manifest unit test, local E2E로 동작 경계를 검증했다.

### Lifecycle Cleanup

- Challenge: 구독 해지 시 runtime 자산은 제거해야 하지만 외부 DB/schema/role은 복구와 재구독 가능성을 위해 보존해야 했다.
- Action: runtime Secret과 DB credential Secret은 ownership label selector로 삭제하고, provisioner hook live resource와 GitOps desired-state manifest cleanup을 분리했다.
- Result: 제거 대상과 보존 대상의 운영 boundary가 명확해졌고, full-lifecycle E2E에서 cleanup과 external asset preservation을 동시에 검증할 수 있게 됐다.

### AI-driven Development Harness

- Challenge: AI agent 기반 개발은 세션 간 맥락 drift, 검증 누락, 산출물 불일치가 발생하기 쉽다.
- Action: issue lifecycle skill chain, `.claude/workspace` 산출물 convention, `review-implement` DoD 판정, `full-lifecycle-e2e` Codex skill을 정리해 개발-검증-handoff 흐름을 표준화했다.
- Result: AI-assisted 개발을 일회성 프롬프트가 아니라 재현 가능한 engineering workflow로 운용할 수 있는 기반을 만들었다.

## 경력기술서 상세 서술

Gallery 백엔드의 subscription/deployment 경로에서 Kubernetes, ArgoCD, GitOps, Secret management, DB provisioning이 결합되는 운영 자동화 영역을 설계·구현했다. 구독자가 입력한 앱 Secret value가 GitOps repo나 Kafka payload에 남지 않도록 `runtimePrerequisites` metadata와 `subscriptionSecrets` value를 분리하고, value는 subscription store에 AES 암호화 저장한 뒤 배포 직전에 K8s Secret으로 실체화하는 구조를 만들었다. 동시에 구독 시 DB 준비가 수동 절차로 남지 않도록 ArgoCD PreSync Hook과 Kubernetes Job 기반 provisioner manifest를 GitOps 배포 흐름에 통합해 DB/schema/role 및 DB credential Secret 생성을 자동화했다. 배포 성공 판정은 ArgoCD sync 여부만 보지 않고 Deployment health와 K8s pod stabilization까지 관측하도록 보강했으며, 구독 해지 시에는 runtime 자산을 label selector 기반으로 정리하되 외부 DB/schema/role은 보존하는 cleanup boundary를 명확히 했다. 이 흐름은 단위 테스트와 함께 `full-lifecycle.sh` E2E로 SUBSCRIBE부터 UNSUBSCRIBE까지 검증되도록 구성했다. qra-backend에서는 ADR-019, PreSync DB provisioning POC, subscription secret input contract를 정리해 Gallery 재통합 이후 구현 기준을 마련했다. 또한 AI-assisted 개발을 일회성 코드 생성이 아니라 issue lifecycle, workspace artifact, DoD review, E2E harness로 구조화해 세션 간 handoff와 반복 검증이 가능한 개발 운영 방식으로 정리했다.

## 추가 확인 질문

1. 이력서에 넣을 수 있는 정량 수치가 있는가? 예: 수동 작업 단계 수 감소, E2E 소요 시간, 관련 테스트 수, 장애/회귀 방지 사례.
2. 역할 표현 수위는 어느 정도가 맞는가? 단독 설계/구현, 리뷰/정리/검증 중심, 팀 협업 중 담당 영역 중 어디에 가까운가.
3. qra-backend는 문서/ADR/POC 설계 성과로만 둘지, Gallery 구현으로 이관된 재통합 설계 주도까지 표현해도 되는가.
4. 지원 포지션이 백엔드 플랫폼, DevOps/SRE, 제품 백엔드 중 어디에 가까운가. 같은 증거라도 강조점이 달라진다.
5. AI-driven programming 항목은 이력서 본문 bullet로 강하게 넣을지, 포트폴리오/면접 보조 소재로 분리할지 결정이 필요하다.

## 면접 방어 포인트

- Secret value를 왜 GitOps에 넣지 않았는가: GitOps는 desired state 선언에는 적합하지만 plain Secret value를 저장하면 repo, diff, audit, clone 경로로 민감값이 확산된다. 그래서 Secret name/reference는 GitOps에 두고 value는 platform-managed runtime Secret으로 분리했다.
- 왜 PreSync Hook을 선택했는가: workload가 뜨기 전에 DB/schema/role/DB credential Secret이 준비되어야 하므로 ArgoCD lifecycle에서 workload 이전 단계에 실행되는 PreSync가 자연스럽다. 외부 operator 없이 Kubernetes Job으로 시작할 수 있어 1차 MVP에 적합했다.
- 왜 cleanup에서 DB를 지우지 않았는가: unsubscribe는 접근 경로와 runtime 자산을 닫는 작업이고, 외부 DB/schema/role 삭제는 복구, 환불, 재구독, 데이터 삭제권 정책과 엮인 별도 결정이다. 그래서 runtime cleanup과 data retention boundary를 분리했다.
- AI-driven workflow를 어떻게 설명할 것인가: AI가 코드를 대신 썼다는 식으로 말하지 않는다. 요구사항 정제, spec drilling, 코드 매핑, DoD review, E2E harness를 산출물 중심으로 표준화해 반복 가능한 개발 검증 체계를 만들었다고 설명한다.

## 주요 증거 파일

- `docs/adr/019-service-db-secret-provisioning-responsibility.md`
- `gallery-feature/src/main/java/io/vizend/gallery/feature/deployment/action/task/DeploymentGitOpsTask.java`
- `gallery-feature/src/main/java/io/vizend/gallery/feature/deployment/action/task/ArgoCdObservationTask.java`
- `gallery-feature/src/test/java/io/vizend/gallery/feature/deployment/runtime/RuntimeSecretPlanResolveTaskTest.java`
- `gallery-feature/src/test/java/io/vizend/gallery/feature/deployment/action/ProvisionerManifestActionTest.java`
- `gallery-feature/src/test/java/io/vizend/gallery/feature/deployment/action/task/DeploymentGitOpsTaskSecretApplyTest.java`
- `gallery-feature/src/test/java/io/vizend/gallery/feature/deployment/action/DeploymentResourceCleanupActionTest.java`
- `docs/guide/scripts/run/full-lifecycle.sh`
- `../qra-backend/docs/adr/019-service-db-secret-provisioning-responsibility.md`
- `../qra-backend/docs/review/adr-019-implementation-roadmap.md`
- `../qra-backend/docs/guide/local-dev-guide-db-provisioner.md`
- `../qra-backend/docs/guide/subscription-secret-input-design.md`
- `AGENTS.md`
- `.codex/skills/full-lifecycle-e2e/SKILL.md`
- `.claude/skills/review-implement/SKILL.md`
- `.claude/skills/implement-issue/references/pipeline-lead.md`
- `.agent/workflows/implementation-lead.md`
