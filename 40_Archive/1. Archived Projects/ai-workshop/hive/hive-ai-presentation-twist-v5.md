# Hive Framework: AI 협업으로 만든 멀티테넌시 프레임워크

## Hive Framework

**Hive: 엔터프라이즈급 멀티테넌시 프레임워크**

Spring Boot Auto-Configuration 기반 멀티테넌시 솔루션

**"설정보다 구현에, 인프라보다 비즈니스에"**

> 하단 정보: 발표자 · 날짜 · 로고
> 발표 시간: 10-15분 | 대상: 현업 개발자

## Agenda

### 오늘의 여정

1. **왜 멀티테넌시인가?**
   - 업계 현황과 필요성

2. **기존 솔루션의 한계**
   - 70% 커스텀 구축 현실

3. **Hive의 혁신**
   - 4대 핵심 가치

4. **핵심 아키텍처**
   - 설계 철학과 구현

5. **실전 적용 사례**
   - Devlime 프로젝트

6. **향후 계획**
   - 로드맵과 비전

> 초반에는 Hive의 필요성과 기능 전달 → 성과 공유 → "어떻게 가능했나?" 질문으로 전환 → 후반부에 AI 협업 스토리의 반전 강조

## Hive가 해결하는 문제

### 현재의 고통

- ❌ 복잡한 설정 (50+ LOC)
- ❌ 데이터 유출 위험
- ❌ 전략 변경 시 전면 재작성
- ❌ 환경별 다른 코드

### Hive의 답

- ✅ 한 줄 설정
- ✅ 구조적 안전
- ✅ 무중단 전략 전환
- ✅ 환경별 자동 최적화

**💡 멀티테넌시를 Spring Boot처럼 쉽게**

> 레이아웃: 문제 → Hive → 해결 (3컬럼)

## 멀티테넌시의 필요성

### 전통적 방식 (단일 DataSource)

- 모든 고객 데이터/Connection Pool 공유
- 부하 전파, WHERE 조건 의존
- 전략 변경 = 전면 재작성

### DataSource Separation

- 테넌트별 독립 DataSource
- 장애/성능 격리, 규제 대응 용이
- 전략 변경 = 설정 1줄

**💡 Hive = DataSource Separation 프레임워크**

**📊 효과: Noisy Neighbor 해결, 규제 준수 자동화**

> 레이아웃: Split Screen (전통 방식 vs DataSource 분리)

## 업계 리더들의 선택

### Salesforce
**Shared Database 전략**

### ServiceNow
**Database-per-Tenant 전략**

### Atlassian
**하이브리드 전략**

### 인사이트

- 절대적 정답 없음, 하이브리드 전환이 핵심
- 업계 현실: 70% 이상이 커스텀 구축
- 스키마 마이그레이션의 고통

> 3분할 카드 (Salesforce / ServiceNow / Atlassian)

## 개발자와 운영팀의 3대 고충

### ⚙️ 복잡한 설정 (80+ LOC)
수동 설정, Bean 정의, 예외 처리

### ⚠️ 데이터 유출 위험 (필터 누락)
tenantId 조건 빠진 실수 → 모든 데이터 노출

### 🔄 스키마 마이그레이션 혼란 (수천 테넌트)
전략 전환 시 전면 재작성 필요

**💀 휴먼 에러는 언제든 발생 → 구조적 해결이 필요**

> 코드 예시: tenantId 조건 빠진 실수 → 모든 데이터 노출 스크린샷

## Hive의 근본적 해결책

### Before: 수동 관리
```java
// 수동 tenantId 검사, 예외 처리
if (tenantId == null) throw new Exception();
list = repository.findByTenantId(tenantId);
```

### After: 자동 격리
```java
// findAll()만 호출하면 격리 자동 적용
list = repository.findAll();
```

### 설정
```yaml
vizend.hive.data-policy.strategy: DATABASE
```

**✨ 복잡함을 숨기고 단순함을 제공 — "Just Works"**

> Before/After 코드 비교 + 설정 비교

## Hive의 4대 핵심 가치

### 🛡️ 구조적 안전
인프라 레벨 데이터 격리

### 🔄 점진적 성장
전략 전환을 설정으로

### 🌍 환경별 최적화
DYNAMIC vs STRICT

### ⚡ 운영 자동화
Phase 기반 부트스트랩 (Validation → Update → Migration)

> 4개 카드 레이아웃, 각 가치별 아이콘 표시

## Minimal Configuration의 마법

### 기존 방식
- @Configuration 클래스 작성
- 50+ LOC Bean 설정
- 수동 예외 처리

### Hive 방식
- starter 의존성 추가
- YAML 5줄 설정
- Auto-Configuration 자동 적용

**→ 설정 시간 90% 절감, Auto-Configuration 철학**

> 코드 비교 화면

## 비즈니스와 함께 성장하는 전략

### Stage 1: SHARED
- 빠른 MVP, 비용 최저
- 단일 DB, 스키마 공유

### Stage 2: SCHEMA
- 균형 잡힌 격리
- DB 공유, 스키마 분리

### Stage 3: DATABASE
- 완전 격리, 규제 대응
- 테넌트별 독립 DB

**전환 예: 설정 한 줄 교체, 무중단 전략 전환**

> 타임라인 (Shared → Schema → Database)

## STRICT vs DYNAMIC 모드

### 🚀 DYNAMIC (개발 환경)
- 테넌트 DB 자동 생성
- failure-policy: WARN
- 빠른 실험 가능

### 🔒 STRICT (운영 환경)
- 사전 등록 된 테넌트만 허용
- failure-policy: FAIL_FAST
- 안전성 최우선

**동일 코드 + 다른 정책 → 환경별 최적화 자동 적용**

> Split Screen (개발 vs 운영)

## 숫자로 본 구축 성과

### 생산성
예측 4-6주 → **기본 기능 2주 + 고도화 1주**

### 운영 가치
테넌트 온보딩 시간 **70% 단축 예상**

### 문서화
README/가이드/워크로그 **자동화**

> 숫자 강조 레이아웃, 그래프 또는 메트릭 카드

## 어떻게 이렇게 빨랐을까?

**멀티 전략 지원 + 안정성 + 문서화까지 3주**

### 🤔 비밀은 무엇일까요?

> 질문 형태로 청중의 호기심 유발
> 다음 슬라이드로 자연스럽게 전환

## 반전 공개 — AI 페어 프로그래밍

**Claude Code와 4주간 짝 프로그래밍**

- 36개 커밋
- 테스트 실패 0회

### 역할 분담

**👤 사람**
- 문제 정의
- 아키텍처 결정
- 최종 검증

**🤖 AI**
- 구현 설계
- 코드 작성
- 리팩토링/문서 초안

> Claude Code 로고 또는 협업 일러스트
> 커밋 히스토리 스크린샷

## 협업 루프 사례 ① — 테넌트별 DB 생성 자동화

### 문제
DB-per-tenant 전략에서 모든 테넌트가 동일 DatabaseCreator를 공유
→ DBMS별 옵션 적용 불가

### 요청
"테넌트 JDBC URL을 읽어 DBMS를 감지하고, 안전하게 Creator를 골라줘. 로그는 마스킹해줘."

### AI Plan Mode
1. 팩토리 패턴 설계
2. 캐시 전략 제안
3. 단위/통합 테스트 목록 작성

### 결과
- TenantAwareDatabaseCreatorFactory 도입
- URL 마스킹/캐싱 구현
- 테스트 3종 추가 (Factory/Consistency/Multi-DBMS)

**💡 인사이트:** 복잡한 분기 로직도 AI가 구조화해주니 우리는 정책 결정에 집중

> Plan Mode 스크린샷 또는 다이어그램

## 협업 루프 사례 ② — Provisioner 템플릿 메서드 도입

### 문제
- 전략별 Provisioner에 재시도·에러 처리가 중복
- 새 전략 추가 시 수정 범위 과도

### 요청
"공통 로직은 템플릿으로 묶고, 전략별 훅만 남겨줘."

### AI Plan Mode
1. 추상 클래스 설계
2. 훅 메서드 정의
3. 적용 대상 클래스 목록화
4. 회귀 테스트 제안

### 결과
- AbstractTenantProvisioner 도입
- 공통 재시도/에러 처리 단일화
- TenantDataSourceFactory로 생성 로직 집중
- **수정 파일 수 5→1**

**💡 인사이트:** 패턴 선언만으로도 일관된 구조와 테스트 포인트가 자동으로 잡힌다

> Before/After 클래스 다이어그램

## 협업 루프 사례 ③ — Bootstrap Phase 통합 오케스트레이션

### Pain
전략별 초기화 순서 불일치

### 요청
"Discovery/Prepare/Activate 3-Phase로 묶고 FAIL_FAST 정책도 반영해줘."

### AI 제안
1. PhaseExecutionOrchestrator 설계
2. PhaseResult 리포트 구조 재정의
3. 중단 로직/리포팅 테스트 플랜 제시

### 결과
- PhaseExecutionOrchestrator 도입
- TenantInitializationReport 연동
- 부트스트랩 프로세스 문서 자동 생성 (`docs/tenant-bootstrap-process.md`)

**💡 인사이트:** 프로세스형 리팩토링은 AI가 시나리오·테스트까지 패키지로 제공하면 사람이 검증과 승인에 집중

> Phase 다이어그램 또는 프로세스 플로우

## 협업 원칙과 학습

### 협업 루프
문제 포착 → 방향 제시 → AI 계획 → 사람 검증 → 실행/테스트

### 4가지 원칙

1. **CLAUDE.md로 가드레일 공유**
   - 프로젝트 컨텍스트와 규칙 명시

2. **한 번에 하나의 목표**
   - 작은 단위로 반복

3. **실패 시 로그/디프 근거로 재요청**
   - 구체적 피드백 제공

4. **신뢰하되 항상 검증**
   - 테스트와 코드 리뷰 필수

**📢 Call to Action: 내일 한 번 AI 페어 프로그래밍을 시도해보세요**

> 순환 다이어그램 또는 프로세스 플로우

## Closing Takeaways — AI 협업 후기

### AI 협업에서 느낀 점

1. **짧은 적응기를 넘기면 개발 속도와 품질이 동시에 급상승**

2. **개인의 한계가 크게 확장**
   - 혼자선 하기 힘들었던 설계/리팩토링도 가능

3. **팀에서는 고점보다 저점을 올리는 게 핵심**
   - 병목 프로세스 먼저 정리

4. **가드레일과 검증 루틴이 필수**
   - CLAUDE.md, 자동 테스트, 코드 리뷰

**메시지: 속도와 품질을 함께 잡으려면 '역할 분담 + 구조적 검증'이 답**

> 4개 포인트를 카드 형태로 배치
> 감사 메시지

---

## 백업 슬라이드: 검증 체크리스트

### 코드 변경 후 필수 확인 사항

- ☑ **테스트 결과 확인**
  - 모든 테스트 통과 여부

- ☑ **주요 Diff 코드 리뷰**
  - 변경 사항의 적절성 검토

- ☑ **롤백 플랜 준비**
  - 문제 발생 시 복구 방안

- ☑ **문서/워크로그 업데이트**
  - 변경 내용 기록 및 공유

> 체크리스트 형태로 정리
> 슬라이드 14-17에서는 실제 코드/다이어그램 캡처, Plan Mode 스크린샷 등을 덧붙이면 현장감 상승
