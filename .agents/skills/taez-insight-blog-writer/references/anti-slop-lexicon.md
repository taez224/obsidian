---
created: 2026-06-09
tags:
  - 개발/DevLog
  - meta
  - 글쓰기
aliases:
  - Anti-Slop Lexicon
  - 슬롭 사전
  - 금지표현 사전
---

# 🧹 Anti-Slop Lexicon — 금지표현·문장부호 단일 출처

> AI 슬롭의 기계적 시그니처를 한국어 실현형으로 옮긴 **단일 편집 출처**.
> 두 곳이 이 파일 *하나*를 본다 → 드리프트 차단:
> 1. `blog-slop-lint.mjs` (결정론적 CLI) — 아래 ` ```json ` 블록의 패턴을 regex/밀도로 검사.
> 2. `blog-review-polish.js`의 "한국어 AI-티 감별사" 페르소나 — 같은 카테고리를 편집 기준으로 사용.
>
> 원칙: **금지표현을 지우는 게 목적이 아니라, 건조한 고유 정보로 대체하는 것**이 목적이다.
> 비어 있는 매끄러움(slop)을 측정된 비용·인과·장면으로 바꾼다.

## 설계 메모 — 왜 zero-tolerance가 아닌가

이 저자의 *발행된* 글도 em-dash를 5~6회, "할 수 있습니다"를 4회 쓴다. 무관용 lint는 저자의 실제
목소리와 싸운다. 그래서 등급을 나눈다.

- `high` — 명백한 슬롭. 거의 항상 삭제/재작성. (이모지, 비즈니스 허영 도입, 안내형 상투)
- `medium` — 사람이 본다. 문맥상 정당할 수 있음. (수사 잡음, 양분법 템플릿, 한자어 동사, 밀도 초과)
- `low` — 정보용 카운트. 막지 않음.

lint 판정: `high`가 하나라도 있으면 **fail**, `medium`만 있으면 **warn**, 없으면 **pass**.
warn/fail은 발행을 *막지* 않는다. 막는 것은 `_slop-gate`의 사람 사인오프다. lint는 그 사인오프에
들이댈 **증거**를 만든다.

## 카테고리 — manifesto 원형(EN) → 한국어 실현형 → 건조한 대체

| # | 카테고리 | manifesto 원형(EN) | 한국어 슬롭 실현형 | 건조한 대체 |
| --- | --- | --- | --- | --- |
| 1 | 양분법 수사 | It's not about X, it's about Y | "단순히 X가 아니라 Y의 문제입니다", "X가 아니라 Y" 남발 | 측정된 비용·인과를 직접 명시 ("이 방식은 메모리를 14% 더 쓴다") |
| 2 | 안내형 상투 | Let's dive in / Let's unpack | "가볍게 파헤쳐 봅시다", "함께 살펴봅시다", "알아봅시다", "본격적으로 들어가기 전에" | 안내 문장 삭제, 바로 장면/사실로 진입 |
| 3 | 수사 보조 잡음 | Important to note that | "주목할 점은", "~라는 점이 중요합니다", "사실상", "본질적으로", "흥미롭게도" | 잡음 구문 제거, 주장만 남김 |
| 4 | 비즈니스 허영 | In today's fast-paced digital landscape | "빠르게 변화하는 ~ 속에서", "급변하는", "AI 시대를 맞아", "바야흐로" | 벤치마크 수치·아티팩트 근거를 곧바로 제시 |
| 5 | 문장부호 | 🚀 emoji, dramatic em-dash (—) | 본문 이모지, 극적 em-dash 남발, 과잉 느낌표 | 콤마(,)·마침표(.)·괄호(())로 환원 |
| 6 | 한국어 AI-티 | (토스 라이팅 원칙 위반) | 한자어 동사("수행/진행"), "~할 수 있습니다" 남발, "~라고 할 수 있다" 헤지, "~에 있어서" 번역체 | 능동·단정·사람을 행동 주체로 ([[korean-tech-writing-guide]]) |

## 적용

- lint 단독: `node .claude/workflows/blog-slop-lint.mjs "<초안 절대경로>"`
- 파이프라인: `blog-review-polish`의 Final-gate가 위 CLI를 `--json`으로 호출해 게이트 리포트에 병합.
- 사람: `slop-gate.md` 6번(표면 매끄러움 제거) 검사 시 lint 리포트를 근거로 사용.

## 패턴 (기계 파싱 — lint가 읽는 단일 출처)

> ⚠️ regex는 JSON 문자열이라 백슬래시가 이중(`\\s`)으로 들어간다. 패턴을 고치면 lint를 다시 돌려
> 오탐을 확인할 것. 새 카테고리를 추가하면 위 표에도 같은 카테고리명을 적어 동기화한다.

```json
{
  "version": 1,
  "thresholds": {
    "emDashPerK": 2.0,
    "canDoPerK": 6.0,
    "exclaimPerK": 1.5,
    "aboutNotPerK": 4.0
  },
  "patterns": [
    {
      "id": "dive-in",
      "category": "안내형 상투",
      "severity": "high",
      "pattern": "(가볍게\\s*)?(파헤쳐|들여다|뜯어)\\s*(봅시다|보겠습니다|보자|보죠)",
      "fix": "안내 문장 삭제, 바로 장면/사실로 진입"
    },
    {
      "id": "lets-explore",
      "category": "안내형 상투",
      "severity": "high",
      "pattern": "(함께|한번|한 번|이제|지금부터)?\\s*(살펴|알아|들어가)\\s*(봅시다|보시죠|보겠습니다|보자|볼까요)",
      "fix": "독자 안내 제거, 본론부터"
    },
    {
      "id": "before-we-begin",
      "category": "안내형 상투",
      "severity": "medium",
      "pattern": "본격적으로\\s*(들어가|시작하)(기|니)\\s*(전에|앞서)",
      "fix": "도입 의식 생략, 첫 문장을 장면으로"
    },
    {
      "id": "vanity-fastpaced",
      "category": "비즈니스 허영",
      "severity": "high",
      "pattern": "(빠르게\\s*변화하는|급변하는|날로\\s*(발전|진화)하는|숨가쁘게\\s*돌아가는)",
      "fix": "허영 도입 삭제, 측정된 사실로 시작"
    },
    {
      "id": "vanity-era",
      "category": "비즈니스 허영",
      "severity": "high",
      "pattern": "(바야흐로|시대를\\s*맞아|시대의\\s*흐름\\s*속|시대가\\s*도래|첨단을\\s*달리)",
      "fix": "'~의 시대' 수사 제거, 구체 근거 제시"
    },
    {
      "id": "filler-note",
      "category": "수사 보조 잡음",
      "severity": "medium",
      "pattern": "주목(할\\s*(점은|만한|필요가)|해야\\s*할)",
      "fix": "'주목' 안내 제거, 주장만 남김"
    },
    {
      "id": "filler-important-point",
      "category": "수사 보조 잡음",
      "severity": "medium",
      "pattern": "(라는|다는)\\s*점(이|을)\\s*(중요|강조|기억|유의|명심)",
      "fix": "'~라는 점이 중요합니다' 군더더기 제거"
    },
    {
      "id": "filler-adverbs",
      "category": "수사 보조 잡음",
      "severity": "medium",
      "pattern": "(사실상|본질적으로|흥미롭게도|놀랍게도|결과적으로\\s*보면|어떻게\\s*보면)",
      "fix": "의미 없는 부사 잡음 삭제"
    },
    {
      "id": "dichotomy-template",
      "category": "양분법 수사",
      "severity": "medium",
      "pattern": "(단순한|단순히|그저|단지)\\s*[^\\n.]{0,40}?(의\\s*문제|문제|것|기능|일)(가|이|는)?\\s*아니(라|ㅂ니다|다)",
      "fix": "양분법 대신 측정된 비용·인과를 직접 명시"
    },
    {
      "id": "hedge-can-say",
      "category": "한국어 AI-티",
      "severity": "medium",
      "pattern": "(라고|다고|이라고)\\s*할\\s*수\\s*있(습니다|다|죠)",
      "fix": "'~라고 할 수 있다' 헤지 제거, 단정으로"
    },
    {
      "id": "hanja-verb",
      "category": "한국어 AI-티",
      "severity": "medium",
      "pattern": "(을|를)\\s*(수행|진행)(합니다|한다|하는|하고|했|하며|하여)",
      "fix": "한자어 동사 제거: '수행/진행' → 구체 동사 (토스 원칙)"
    },
    {
      "id": "translationese-eseo",
      "category": "한국어 AI-티",
      "severity": "medium",
      "pattern": "에\\s*있어서",
      "fix": "'~에 있어서' 번역체 제거"
    },
    {
      "id": "emoji-body",
      "category": "문장부호",
      "severity": "high",
      "pattern": "[\\u{1F300}-\\u{1FAFF}]",
      "flags": "gu",
      "fix": "본문 장식 이모지 제거 (🚀 등). 의미는 문장으로. (→ ★ ✅ 등 기능 표기는 제외)"
    }
  ],
  "densities": [
    {
      "id": "em-dash",
      "category": "문장부호",
      "severity": "medium",
      "pattern": "[—–]",
      "perKey": "emDashPerK",
      "fix": "극적 em-dash를 콤마/마침표/괄호로 환원"
    },
    {
      "id": "can-do",
      "category": "한국어 AI-티",
      "severity": "medium",
      "pattern": "할\\s*수\\s*있(습니다|다)",
      "perKey": "canDoPerK",
      "fix": "'~할 수 있습니다' 남발 축소: 능동 단정으로"
    },
    {
      "id": "exclaim",
      "category": "문장부호",
      "severity": "low",
      "pattern": "!",
      "perKey": "exclaimPerK",
      "fix": "과잉 느낌표 축소"
    },
    {
      "id": "about-not",
      "category": "양분법 수사",
      "severity": "low",
      "pattern": "아니라|아니었|아닙니다",
      "perKey": "aboutNotPerK",
      "fix": "'X가 아니라 Y' 양분법 축소. 문장을 쪼갠 'X가 아니었습니다. Y였습니다'도 같은 구문이다"
    }
  ]
}
```

## 연관된 노트

- [[slop-gate]] - 이 사전을 근거로 사람이 사인오프하는 게이트
- [[voice-profile]] - 지켜야 할 목소리 DNA (이 사전은 *반대로* 피할 것)
- [[korean-tech-writing-guide]] - 한국어 AI-티 카테고리의 1차 출처(토스 라이팅 원칙)
