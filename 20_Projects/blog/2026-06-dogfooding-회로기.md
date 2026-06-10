---
title: "AI 도구를 만들고 1주 뒤 자기가 써본다 — vizend-agent-hub 5월 dogfooding 회로기"
created: 2026-05-28
tags:
  - blog
  - AI/에이전트
  - 개발/도구
  - 개발/플랫폼
status: ready-for-publish
author: TaeZ
summary: "사내 공용 Claude Code 플러그인 vizend-agent-hub에 5월 한 달간 5개 스킬을 추가하며 발견한 1주 dogfooding 회로 패턴. 도구를 만든 다음 주에 자기가 써봐야 빠르게 성숙한다는 주장을 sync-domain-docs(1일 회로)와 spec-drilling(5일 회로) 두 사례로 검증한다."
---

# AI 도구를 만들고 1주 뒤 자기가 써본다

*vizend-agent-hub 5월 dogfooding 회로기*

---

## §1. 들어가며 — 같은 작업이 세 번째 반복될 때

일을 하다 보면 어느 순간 같은 작업이 세 번째 반복되는 시점이 온다. 5월 어느 평일 아침, vizend-gallery 레포의 `docs/guide/scripts/run/full-lifecycle.sh`를 세 번째 돌리고 있었다. 두 번까지는 "검증 중이니까" 하고 넘겼는데, 세 번째쯤 되면 이게 검증이 아니라 그냥 *반복* 이라는 게 분명해진다.

"같은 작업이 세 번 반복되면 자동화하라"는 익숙한 격언이다. AI 도구를 본격적으로 쓰기 전까지, 나에게 "자동화"의 단위는 보통 셸 스크립트나 Makefile 타깃이었다. 그런데 Claude Code를 일상적으로 쓰기 시작한 뒤로 자동화의 단위가 한 단계 올라갔다 — 슬래시 커맨드에서 스킬로, 그리고 플러그인으로.

이 글은 5월 한 달 동안 사내 공용 Claude Code 플러그인 `vizend-agent-hub`와 vizend-gallery 레포에 신규 스킬을 추가하면서 발견한 패턴에 관한 이야기다. 하나의 주장이 있다 — **도구를 만든 다음 주에 자기가 써봐야, 도구가 빠르게 성숙한다.** 너무 짧으면 결함이 안 보이고, 너무 길면 만든 이유를 잊는다. 그 사이 어딘가에 "1주"가 있다.

이어지는 본문에서 sync-domain-docs(공용 플러그인에서 시작, 만들고 다음 날 호출)와 spec-drilling(프로젝트 스킬로 시작, 만들고 5일 뒤 다섯 개 이슈에 같은 파이프라인 일관 적용) 두 사례로 이 패턴을 검증하고, 그 뒤에 *이 글 자체가 또 하나의 사례*가 되는 메타 회로 한 편을 짧게 덧붙인다. 1주 회로가 작동하기 위한 **인프라 조건**과 **회사 차원의 시사점**을 정리하는 게 글의 두 번째 축이다.

---

## §2. vizend-agent-hub 한 컷 — 사내 공용 플러그인의 구조

본격적인 사례에 들어가기 전에, `vizend-agent-hub`가 어떤 것인지 한 컷으로 정리한다.

Claude Code 플러그인은 결국 **두 파일**로 정의된다 — `plugin.json` (플러그인 자체)과 `.claude-plugin/marketplace.json` (마켓플레이스 등록 메타). 다른 모든 것 — 스킬, 에이전트, 훅, 슬래시 커맨드 — 은 그 위에 얹히는 컴포넌트다.

```json
// .claude-plugin/plugin.json
{
  "name": "vizend-agent-hub",
  "version": "0.4.0",
  "description": "Vizend 플랫폼 공용 에이전트·스킬·컨벤션 허브.
    어떤 레포에서든 Vizend 도메인 지식(서비스 메시, 레이어링,
    네이밍, 보안 패턴)을 자동 로드.",
  "author": { "name": "Vizend Team" }
}
```

5월 말 기준 vizend-agent-hub의 구성은 이렇다 (주요 스킬 발췌).

```
vizend-agent-hub/
├── .claude-plugin/        # plugin.json + marketplace.json
├── skills/                # 17개 공용 스킬
│   ├── architecture/      coding-standards/    conventions/
│   ├── flyway-script/  ★  sync-domain-docs/  ★ bootstrap/
│   ├── glossary/          hub-index/           security-review/
│   ├── verification-loop/ vsr-check/           git-workflow/
│   └── cross-service-context, dev-loop, onboarding,
│       service-catalog, create-integration-test
├── agents/                # 8개 서브에이전트
├── hooks/                 # SessionStart / Stop 등 2개
├── commands/              # 2개 슬래시 커맨드
└── docs/                  # 아키텍처·컨벤션·서비스 카탈로그
```

★는 5월 신규로 추가된 스킬 — sync-domain-docs는 §4에서 다룬다.

스킬은 폴더 하나 + `SKILL.md` 한 파일이라는 단순한 구조다. YAML frontmatter에 트리거 어휘를, 본문에 실행 절차를 적는다. 어떤 vizend 레포에서든 한 줄로 모든 스킬이 동시에 활성화된다 — 도메인 지식과 컨벤션, 자동화가 단일 진입점으로 통합된다.

플러그인이 회사 도구의 *공급측* 단일 출처라면, 그 도구를 *수요측*에서 즉시 호출할 수 있어야 dogfooding이 시작된다. 다음 절에서 그 수요측 인프라를 본다.

## §3. 1주 회로의 인프라 — 로컬 marketplace 등록

플러그인을 만들었어도, **다른 컨텍스트에서 호출할 수 없으면 dogfooding 자체가 불가능**하다. 처음엔 그래서 막혔다.

일반적인 플러그인 배포 사이클은 이렇다 — 변경하고, push하고, CI가 빌드하고, 다른 사용자가 pull 받아 다시 설치. 짧아도 며칠, 길면 한두 주가 걸린다. 이 사이클로는 만든 사람이 1주 안에 자기가 써볼 수가 없다. *만들기*와 *써보기* 사이에 너무 많은 단계가 끼어 있다.

해결책은 단순했다. `/plugin marketplace add` 가 **로컬 경로도 받는다**. GitLab을 거치지 않는다.

```bash
# GitLab을 거치는 일반 등록
/plugin marketplace add https://gitlab.vizend.io/experiment/vizend-agent-hub.git

# 로컬 경로 직접 등록 — dogfooding용
/plugin marketplace add /Users/taez/Projects/nextree/vizend/vizend-agent-hub
```

두 번째 줄이 1주 회로의 인프라 조건이다. 스킬을 추가하면 그 자리에서 다른 레포의 Claude Code 세션이 즉시 인식한다. `git push`도 CI도 거치지 않는다.

물론 한계도 있다. 로컬 경로 등록은 **자기 머신에서만 작동**하므로 팀 전체 배포는 결국 GitLab 경로가 필요하다. 하지만 *팀 배포 전*에 만든 사람이 1주 안에 자기 검증을 끝내는 단계가 보장된다는 게 핵심 — 팀에 배포되는 시점에는 이미 1주 회로를 한 번 돈 도구가 들어간다.

5월 12일, 첫 사례가 이 인프라 위에서 시작됐다.

---

## §4. 사례 1 — sync-domain-docs (1일 회로의 가장 짧은 극단)

5월 12일, `sync-domain-docs` 스킬을 vizend-agent-hub로 옮겨 다시 정리했다. 원래는 vizend-qra 레포 안의 로컬 스킬이었는데, 다른 vizend 서비스들도 같은 작업이 필요하다는 걸 확인하고 플러그인 단위로 끌어올렸다.

스킬의 description은 이렇게 정리됐다:

```yaml
name: vizend-agent-hub:sync-domain-docs
description: "Vizend 서비스의 도메인 모델 코드 ↔ 문서 동기화 — *-domain
  모듈 자동 발견, Entity/VO/Enum 차집합 계산, 표·mermaid·변경이력 자동 갱신.
  TRIGGER: '/sync-domain-docs', '도메인 모델 문서 동기화'..."
```

핵심은 **repo-agnostic** — 어느 vizend 서비스에서 호출되든 동일하게 작동한다. 모듈명을 하드코딩하지 않고 컨벤션 기반 discovery를 쓴다.

다음 날인 5월 13일, vizend-gallery 레포에서 `/vizend-agent-hub:sync-domain-docs` 를 처음 호출했다. **만든 다음 날, 만든 곳과 다른 레포에서 호출 — 그게 첫 외부 시각이었다.**

호출하자마자 결함이 보였다. 두 가지 — (1) `.codex-plugin/plugin.json`이 아직 `0.3.2`로 남아 있어 codex 컨텍스트에서는 새 스킬을 인식하지 못했고, (2) `marketplace.json`은 이미 `0.4.0`인데 `plugin.json` 본체가 일치하지 않는 정합성 깨짐. 둘 다 **버전 정합성** 결함이었고, 만들 때 *플러그인 입장*에서만 봐서 안 보였던 것이 사용하는 입장에서 30분 만에 노출됐다.

같은 날 v0.4.0으로 promote하고 CHANGELOG를 정리했다. Unreleased 섹션에 누적돼 있던 3개 항목 — Skill name 정책, `check-task-completion` 훅, planner Pre-flight — 도 같이 묶어서 한 번에 닫았다.

**1일 회로**. 다만 여기서 잡힌 건 *형식적 정합성* 결함이었지, 도구의 의미적 빈틈은 아니다. 1일은 *정합성 검증층*으로 자기 자리를 가진다 — 의미적 검증은 다음 사례, 5일 회로에서 일어난다.

---

## §5. 사례 2 — spec-drilling (5일 회로의 표준 케이스)

두 번째 사례는 공용 플러그인이 아닌 **프로젝트 스킬**(project-scope)이다. 같은 1주 회로 원리가 *팀 공용*과 *프로젝트 한정* 양쪽에서 동일하게 작동한다는 걸 보여주는 사례.

5월 14일 목요일, gallery 레포에서 작업하다가 `status::spec` 상태로 멈춰 있는 이슈들이 눈에 거슬렸다. *구현 직전*인데 *결정이 안 닫힌* 이슈들이었다. ADR과 코드 사이의 미정 결정을 묶어 사용자에게 옵션으로 제시하고, 닫힌 결정을 ADR 변경이력·이슈 description·spec 문서 세 곳에 동시 기록하는 절차가 필요했다.

그 자리에서 `spec-drilling`이라는 신규 스킬을 만들기 시작했다 — vizend-agent-hub로 끌어올리지 않고 `gallery/.claude/skills/spec-drilling/`에 두었다. 충분히 일반화되기 전까지는 *프로젝트 한정*으로 검증하는 게 맞다고 봤다. 만들고 나서 바로 한 일은 `plugin-dev:skill-reviewer` 에이전트에 품질 검토를 맡긴 것 — 스킬을 쓰지 않고 *읽어줄* 사람의 시각을 확보하기 위해.

5월 18일 월요일, 5일 뒤. epic-1의 이슈 #8을 보다가 `/spec-drilling 8`을 입력했다. 그게 첫 본격 사용이었다. 같은 날 #14는 기존 브랜치에서 `/implement-issue`로 이어 갔고, #13은 `/review-implement`로 최근 커밋만 한정해 리뷰했다. 5월 19일에는 #7을 같은 흐름으로, 22일에는 #15를 다시 `/spec-drilling`으로 처리했다.

정리하면 W21 한 주 안에 다섯 개의 이슈(#7, #8, #13, #14, #15)가 **하나의 파이프라인** — spec-drilling으로 결정 게이트 통과, implement-issue로 구현, review-implement로 코드 리뷰 — 으로 흘러갔다. spec-drilling이 *직접 호출*된 건 두 번(#8, #15), 같은 파이프라인의 *다른 단계 스킬*이 처리한 게 세 번(#7, #13, #14). 도구 한 묶음이 5개 이슈에 일관 적용된 셈이다.

5일 만에 한 스킬이 *의식적 워크플로우*에서 *자동화 단계*로 넘어간 셈이다. 이슈 번호만 바뀌고 도구가 동일하게 작동하는 순간, 그 도구가 자기 자리를 잡았다는 신호다.

만들 때 의식했던 절차와 5일 뒤 실 사용에서 발견한 빈틈은 달랐다. Phase 0 진입 가드는 만들 때 *형식적 안전장치* 정도였는데, 실 사용에서는 *작업을 멈춰 세우는 압력*으로 동작했다. ADR 변경이력 기록 형식도 만들 때 *예시 한 줄* 이었던 게, 5번 반복되는 동안 *템플릿*으로 굳었다.

> *만든 시점의 직관과 1주 후 실 사용의 압력은 서로 다른 정보를 만든다. 그 사이가 도구의 빈틈을 메운다.*

spec-drilling은 지금은 gallery 안에 있지만, 5월 회로를 한 번 돈 결과로 *일반화 가능성*이 보였다. 6월에는 vizend-agent-hub로 끌어올리는 것이 다음 사이클의 과제다 — **개인 회로 → 팀 회로**로의 확장.

---

## §6. (메타) 사례 3 — 이 글 자체가 회로 안에 있다

이 글에 인용된 모든 수치 — "5월 신규 스킬", "spec-drilling W21 적용", "1일/5일 회로" — 의 1차 사료는 vault 안의 weekly DevLog 4편과 monthly DevLog 1편이다. 그 DevLog들은 `devlog`라는 별도 스킬 명세를 따라 Claude Code가 작성했다. 그 스킬도 5월 한 달 동안 같은 1주 회로로 진화했고, 회로가 돌면서 누적된 DevLog가 결국 이 글의 ground truth가 됐다.

즉 **만든 도구가 이 글의 글감을 만들었고, 그 글감이 이 글의 결론이 된 셈이다.**

> *도구가 도구를 만든다.*

---

## §7. 1주 회로 모델 — 왜 하필 "1주"인가

세 사례에서 공통으로 보인 흐름을 모델로 정리하면 이렇다.

```
Day 0   스킬 생성 + skill-reviewer 품질 검토
        ↓
Day 1   다른 레포(컨텍스트)에서 첫 호출 — 형식적 정합성 검증
        ↓
Day 5   같은 패턴의 작업 2~5회에 본격 적용 — 의미적 빈틈 노출
        ↓
Day 7   결함·누락 가시화 → 보강 또는 다음 스킬로 분기
```

실제 사례에 매핑하면 — sync-domain-docs는 Day 0~1에서 정합성 결함을 잡고 같은 날 v0.4.0으로 한 사이클이 닫혔다. spec-drilling은 Day 0~5에서 의미적 빈틈(Phase 0 가드의 작동 방식, ADR 변경이력 템플릿 등)이 노출됐고 5일에 걸쳐 다섯 개 이슈에 적용되며 보강됐다.

여기서 결정적인 변수는 회로의 **길이**다. 너무 짧아도 너무 길어도 안 된다.

**너무 짧으면 (당일 ~ 1일)**: 만든 사람이 자기 작성 패턴에 너무 익숙해서, 결함이 안 보인다. sync-domain-docs(1일 회로)에서도 발견된 결함은 `.codex-plugin/plugin.json` 정합성 같은 *형식적* 결함이었지, *의미적* 빈틈은 아니었다. 의미적 검증엔 며칠이 더 필요하다.

**너무 길면 (한 달+)**: 만든 이유를 잊는다. 다시 본 도구가 *자기 코드도 outsider* 가 되어서, 보강이 아니라 *다시 만드는* 비용이 든다. 한 달 뒤의 나는 너무 멀어져 있다.

**1주가 그 사이다** — 어제의 내가 오늘의 내게 막 외부인이 되는 시간. 도구의 구조는 기억하고 있어서 보강할 수 있을 만큼 가깝고, 만들 때의 패턴에서 충분히 벗어나 있어서 비판할 수 있을 만큼 멀다.

회사 차원에서 보면 더 강력해진다. 팀 공용 플러그인은 회로의 양옆이 *서로 다른 사람*이 될 수 있다 — A가 만들고 B가 다음 날 호출하고 C가 1주 뒤 다른 사례에 적용. **개인의 시간차 회로가 팀의 협업 회로로 확장된다.** vizend-agent-hub의 스킬 17개는 그 누적이고, sync-domain-docs와 spec-drilling은 그중 5월에 닫힌 두 사이클이다.

그래서 어떤 수치가 나왔는지, 이제 정리해 보자.

---

## §8. Scoreboard — 1주 회로 적용의 정량 결과

5월 한 달 동안 누적된 변화는 다음과 같다.

| 지표 | 5월 실측 |
|---|---|
| 스킬 생성 → **첫 다른-컨텍스트 호출 소요 일수** | **1~5일** (sync-domain-docs 1일 / spec-drilling 5일) |
| 결함 발견 주체 | **본인이 1주 안에** (외부 사용자 보고 0건) |
| 5월 신규 공용 스킬 (vizend-agent-hub) | **4개** + 프로젝트 스킬 1개<br/>— sync-domain-docs / flyway-script / planner / release-bump(`.claude/skills/`) + spec-drilling(gallery project-scope) |
| 5월 release | **v0.4.0 (5/13) 1회** — 4개 신규 스킬 + 부가 항목(check-task-completion 훅, Skill name 정책, planner Pre-flight) 묶음 |
| W21 spec-drilling 파이프라인 적용 | **5개 이슈** (#7, #8, #13, #14, #15)<br/>— `/spec-drilling` 직접 호출 2회 (#8, #15) + 후속 `/implement-issue` · `/review-implement` 3회 (#7, #13, #14) |
| 누적 공용 스킬 (월말) | **17개** |

> *5월 release 빈도(1회)는 4월의 9차례 빠른 promote 직후의 안정 사이클로, 4월·5월 평균은 월 ~5회.*

핵심 변수는 단순하다 — **만든 사람이 1주 안에 다른 컨텍스트(다른 레포)에서 한 번이라도 호출했는가**. 이 한 가지가 도구의 진화 속도를 자릿수 단위로 변화시킨다.

## §9. 우리가 한 선택과 그 이유

위 표의 결과를 만든 건 우연이 아니라 두 가지 의식적 선택이었다.

**1. 로컬 marketplace 등록 가능 환경 — 회로의 인프라 조건**

플러그인 변경을 사용해보기 위해 `git push → CI → 다른 사용자 pull` 사이클을 거치면 회로 자체가 길어진다. Claude Code의 `/plugin marketplace add` 가 로컬 경로를 받는다는 점이 결정적이었다 — 만든 스킬을 같은 날 다른 레포에서 호출할 수 있어야 회로가 1주 안에 닫힌다. 공용 플러그인(vizend-agent-hub)이든 프로젝트 스킬(gallery)이든 *수요측 즉시 호출*이 1주 회로의 전제다.

**2. 만든 사람이 *다른 컨텍스트*에서 호출하는 동선 — 회로의 인지 조건**

가장 결정적인 선택. 다른 사람이 써주기 전에 *내가* 다른 레포(또는 다른 사례)에서 한 번이라도 호출해봐야 결함이 빠르게 노출된다. sync-domain-docs를 만든 다음 날 gallery 레포에서 호출했고, 거기서 정합성 결함을 발견해 같은 날 v0.4.0으로 promote했다(§4 참조). **만들 때의 나**와 **다른 컨텍스트에서 쓸 때의 나**는 충분히 다른 사람이다 — 그 거리가 결함 노출의 속도를 만든다.

## §10. 우리 팀에 도입하려면

회사·팀에 1주 dogfooding 회로를 도입하려 한다면, 다음 체크리스트로 시작하면 된다.

**전제 조건**
- [ ] Claude Code v2.x 이상 (로컬 marketplace 등록 지원 확인)
- [ ] 팀이 공용으로 쓸 단일 레포 하나 (이름은 `<팀명>-agent-hub` 권장)
- [ ] 만든 사람이 다른 레포에서 호출할 수 있는 동선 (멀티 레포 작업 환경)

**첫 스킬 추천 영역** (효과 검증이 빠른 순)
1. **반복되는 코드 리뷰 절차** — 만들고 다음 코드 리뷰에서 즉시 사용 (1일 회로)
2. **도메인 컨벤션 점검** — 컨벤션 위반 자동 탐지. 같은 주 다른 PR에서 검증
3. **다단계 디버깅 가이드** — pub/sub self-loopback 점검 같은 정형 디버깅 절차

**vizend-agent-hub 시작점**: `gitlab.vizend.io/experiment/vizend-agent-hub` — 모든 vizend 레포에서 한 줄로 즉시 사용 가능.

```bash
/plugin marketplace add https://gitlab.vizend.io/experiment/vizend-agent-hub.git
```

또는 로컬 dogfooding 시작:

```bash
/plugin marketplace add /Users/<you>/Projects/.../<your-team>-agent-hub
```

투자 시간 — 첫 스킬 30분~1시간, 1주 후 효과 검증. **그 1주가 차이를 만든다.**

---

> 5월의 내가 만든 도구로 6월의 내가 이 글을 쓴다. 도구는 만들어진 순간이 끝이 아니다 — 만든 사람이 1주 뒤 외부인으로 돌아와 그 도구를 다시 쓸 때, 비로소 회로가 닫힌다.

