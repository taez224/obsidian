---
created: 2026-09-24
updated: 2026-09-30
slug: jev-system-one
summary: 글 대신 판단을 돌려주는 Jev의 세 가지 질문 타입과, 실제로 개인 지식 관리와 탐색에 실험해 본 기록
tags:
  - AI
---

# Jev와 System One 모델

TypeSafe AI가 공개한 Jev가 요즘 화제라 살펴봤다. LLM처럼 답을 문장으로 쓰지 않고 미리 정한 선택지 가운데 답을 확률과 함께 돌려주는 모델이다. 질문 타입 세 가지를 매주 쏟아지는 논문·글과 내 Obsidian 노트에 하나씩 적용해 봤다. 시험한 버전은 2026년 9월에 나온 `jev-1.13.0`이다.

## System One 모델

[공식 발표 글](https://typesafe.ai/blog/introducing-system-one-models-and-jev)은 Jev를 **System One 모델**의 첫 모델로 소개한다. 이름은 Kahneman이 빠르고 직관적인 판단을 시스템 1, 느리고 신중한 추론을 시스템 2로 나눈 데서 따왔다. 채팅과 글쓰기는 LLM에 맡기고 소프트웨어가 바로 쓸 수 있는 구조화된 판단을 빠르게 내리는 것이 목표라고 한다.

LLM과 가장 다른 점은 답에 붙는 확률이다. 형식만 보면 차이가 크지 않다. 요즘 LLM API에는 Structured Outputs처럼 JSON 스키마를 강제하는 기능이 있어서 LLM도 정해진 형식으로 답하게 할 수 있다. 하지만 LLM은 스키마 안에서도 답을 토큰 단위로 이어 써서 값 하나만 돌려준다. 확신도를 필드로 달라고 해도 그 숫자 역시 생성한 텍스트라, 발표 글은 LLM이 과신하고 일관되지 않다고 지적한다. 스키마에 딱 맞는데 내용은 지어낸 답이 나와도 코드는 알아챌 수 없다.[^schema]

Jev는 선택지를 미리 받아 모든 선택지의 확률을 한 번에 계산하고 이 확률이 실제 정답률과 맞도록 학습했다고 밝힌다. 그래서 코드가 확률을 보고 바로 처리할지, 사람에게 넘길지 정할 수 있다. 선택지 밖의 답은 나오지 않는 대신 문장, 코드, 설명은 만들지 못한다. 발표 글은 System One 형태의 질문에서 비슷한 수준의 LLM보다 40~200배 빠르고 가격은 입력 100만 토큰당 $0.042이며 출력은 무료라고 밝힌다.

## 질문 타입

| 타입 | 돌려주는 값 |
| --- | --- |
| **Noul** (예/아니오) | "예"일 확률 (0~1) |
| **Choice** (선택지 고르기) | 선택지마다 확률, 가장 높은 선택지와 그 확신도 |
| **Score** (단계 매기기) | 단계별 확률의 가중평균과 확신도 |

Noul은 답이 예와 아니오뿐이라 확률 하나로 충분하므로 확신도를 따로 주지 않는다. 값이 0이나 1에 가까울수록 모델이 한쪽 답에 확률을 몰아 준 것이다. 그 답이 맞는다는 보장은 아니다.

판단할 자료(`state`)는 한 번만 보내고 그 자료에 대한 질문 여러 개를 한 요청에 묶을 수 있다. 질문은 병렬로 평가되어 여러 개를 묶어도 응답 시간이 거의 늘지 않는다. 아래 예시는 Python SDK(`typesafe-sdk`)로 실제로 돌린 호출을 기반으로 간소화한 것이다.

### Noul: 관심 주제 판정

매주 arXiv와 Hacker News에 쌓이는 논문과 글에서 읽을 것을 고르는 데 썼다. 노트에 적어 둔 내 주장(예: 「AI 코딩 도구는 이해 부채를 만든다」)을 관심 질문 다섯 개로 바꿔 질문마다 Noul을 하나씩 두고 글의 제목과 초록을 보낸다. 한 글이 여러 질문에 해당할 수 있어서 Choice가 아닌 Noul 여러 개로 물었다. 하나라도 0.8을 넘은 글만 그 주에 읽을 후보 목록에 올린다.

```python
from typesafe_sdk import Noul, TypeSafeClient

client = TypeSafeClient()
state = {"title": title, "summary": abstract}  # 글의 제목과 초록
questions = {
    # AI 도구가 사람의 이해와 역량을 어떻게 바꾸는가
    "comprehension_debt": Noul(instructions="Does this item discuss how using AI assistants, especially coding assistants, affects people's own understanding of the work, their skill development, or their skill decline?"),
    # ... 나머지 네 질문
}
result = client.system_one(state, questions)
print(result.nouls["comprehension_debt"].noul)  # 0.97
```

ChatGPT를 쓴 프로그래밍 수업의 학생들이 과제 점수는 높았지만 기억한 내용은 적었다는 [실험 논문](https://arxiv.org/abs/2609.21194)을 판정한 결과다. 응답의 `answers`에는 질문 키마다 확률 하나가 온다.

```json
"answers": {
  "comprehension_debt": {"type": "noul", "noul": 0.97},
  "thinking_partner": {"type": "noul", "noul": 0.72},
  ...
}
```

| 관심 질문 | "예"일 확률 |
| --- | --- |
| AI 도구가 사람의 이해와 역량을 어떻게 바꾸는가 | 0.97 |
| AI를 쓰면서 사람의 사고가 유지되거나 길러지는가 | 0.72 |
| 사람이 AI 산출물을 수락하기 전에 어떻게 확인하는가 | 0.30 |
| 개인 지식 관리와 글쓰기 | 0.08 |
| 팀과 조직이 AI를 어떻게 받아들이는가 | 0.05 |

이 확률은 논문의 결론이 맞을 확률이 아니라, "제목과 초록이 이 주제를 다루는가"에 대한 답이 "예"일 확률이다. 0.97이라는 답은 "많이 다룬다"가 아니라 "다룬다고 거의 확신한다"는 뜻이다. 얼마나 많이 다루는지처럼 정도를 재려면 순서 있는 단계로 묻는 Score를 쓴다.

LLM과 마찬가지로 질문을 잘 설계해야 한다. 위 표의 두 번째 질문은 원래 "사람이 통제권을 유지하는 의사결정 지원을 다루는가"였는데, 계약서의 모순을 찾아 주는 분석 도구 논문이 0.96으로 올라왔다. 지금처럼 "사람의 사고가 유지되거나 길러지는가"로 좁히자 같은 논문이 0.40으로 내려갔다.

### Choice: 노트 태그 분류

내 노트와 블로그 글에는 `조직`, `커리어`, `AI`처럼 직접 정한 태그 몇 가지 가운데 하나를 대표 분류 기준으로 사용한다. 여기에선 Jev에 노트의 제목, 요약문, 본문의 일부를 보내고 **Choice**로 해당 글에 가장 적절한 태그가 무엇인지 선택하게 했다.

```python
from typesafe_sdk import Choice

state = {"title": title, "summary": summary, "body_excerpt": body}
question = Choice(
    instructions="Which topic is this note's main claim about? Judge by what the note argues, not by words it merely mentions.",
    criteria={  # 선택지 이름: 설명
        "조직": "Organizations: delegation, hiring, team performance, leadership.",
        "커리어": "Career and self-development: growth, skills, motivation, job changes.",
        # ... AI, 개발, 심리, 철학, 글쓰기, 지식관리
        "none_of_the_above": "The note fits none of the topics above.",
    },
)
result = client.system_one(state, {"topic": question})
answer = result.choices["topic"]
print(answer.choice, answer.confidence)  # 개발 0.44
```

응답에는 고른 선택지와 확신도, 모든 선택지의 확률이 포함된다. 아래는 보리스 체르니가 나눈 개발자 유형 다섯 가지에 내 작업 방식을 비춰 본 [[보리스 체르니의 다섯 아키타입으로 본 나의 작업 방식|노트]]의 Choice 응답이다.

```json
"topic": {
  "type": "choice",
  "choice": "개발",
  "confidence": 0.44,
  "probabilities": {
    "개발": 0.51,
    "커리어": 0.34,
    "철학": 0.08,
    // 나머지 선택지들...
    "none_of_the_above": 0.0
  }
}
```

[Confidence 문서](https://docs.typesafe.ai/confidence)에 따르면 Confidence(확신도)는 확률 분포에서 계산한 값으로, 확률이 한 선택지에 몰릴수록 높고 고르게 퍼질수록 낮다. 위 응답에서 Jev의 `choice` 결과는 `개발`이지만, `confidence`가 0.44로 그다지 높지 않다. 그 이유는 `probabilities`에서 보이듯이 `커리어`에도 0.34만큼의 가능성이 있다고 봤기 때문이다. 실제로 이 노트에 내가 붙인 태그는 `커리어`였다.

호출 비용이 싸서 모든 공개 노트를 대상으로 돌려 봤는데 대상 노트 74개 중 38개는 확신도가 1.0이었다. 확신도가 높은데 내 분류와 다른 노트는 직접 확인했다. 상황에 따른 리더십을 다룬 [[SLII 01 - 상황에 따른 맞춤형 리더십|블로그 글]]은 `조직`이 확신도 1.0으로 나왔는데, 나는 `커리어`를 붙여 두었다. 다시 읽어 보니 리더십을 다루는 글이라 태그를 `조직`으로 바꿨다. 다만 Jev도 [[AI 시대의 판단력은 맥락을 실행 기준으로 바꾸는 능력이다]]처럼 제목에 들어간 단어에 끌려 `AI`를 고른 경우가 있어서 무조건 Jev 응답에 따르지 않고 내가 직접 확인한 뒤에 변경했다. 이 노트는 `철학` 태그를 유지했다.

주제 8개가 모든 노트를 아우르지 못할 수 있어서 "해당 없음"(`none_of_the_above`)을 선택지에 넣었다. 딱 맞는 답이 없더라도 Jev는 주어진 선택지 중 하나를 고르기 때문이다. 공식 문서도 목록이 모든 입력을 커버하지 못할 수 있으면 이런 선택지를 넣으라고 권한다. 선택지 이름과 설명은 모델에 그대로 전달되므로, [Choice 문서](https://docs.typesafe.ai/primitives/choice)의 권장대로 선택지끼리 구분되게 쓴다.

### Score: 읽을거리의 난이도 평가

후보 목록에 오른 글마다 읽는 데 필요한 사전 지식을 세 단계로 나눠 봤다. 선택지에 순서가 있으면 Choice 대신 **Score**를 쓴다. 단계는 직접 정하되 낮은 것부터 순서대로 주고, 응답에서는 그 순서대로 0부터 번호가 붙는다.

| 단계 | 기준 |
| --- | --- |
| 0 누구나 | 프로그래밍 배경 없이 읽을 수 있다 |
| 1 현업 개발자 | 일상적인 개발 경험이 있으면 따라갈 수 있다 |
| 2 전문 지식 | 머신러닝, 통계, 특정 시스템의 내부 구조 같은 전문 지식이 필요하다 |

```python
from typesafe_sdk import Score

state = {"title": title, "text": text[:6000]}  # 글 앞부분 6,000자
question = Score(
    instructions="How much prior technical knowledge does a reader need to follow this article?",
    criteria=[
        # 0: 누구나
        "General audience: no programming background needed.",
        # 1: 현업 개발자
        "Working developer: assumes everyday software development experience.",
        # 2: 전문 지식
        "Specialist: assumes specialized knowledge such as machine learning, statistics, or a specific system's internals.",
    ],
)
result = client.system_one(state, {"level": question})
answer = result.scores["level"]
print(answer.score, answer.confidence)  # 1.31 0.0
```

최근 후보 목록에 오른 글 다섯 편의 결과다.

| 글 | 점수 (0~2), 확신도 |
| --- | --- |
| ["rogue" AI 에이전트는 없다](https://eoinhiggins.substack.com/p/there-are-no-rogue-ai-agents) (의견 글) | 0.09, 0.87 |
| [AI 없이 한 달](https://blog.bustikiller.com/2026/09/25/one-month-without-ai.html) (개발자의 체험기) | 1.00, 1.00 |
| [jevgrep](https://github.com/dzhng/jevgrep) (설치해 쓰는 도구) | 1.06, 0.91 |
| [ChatGPT를 쓴 학생의 인지 실험](https://arxiv.org/abs/2609.21194) (논문) | 1.31, 0.00 |
| [Unblocked의 Jev 운영 비교](https://getunblocked.com/blog/jev-in-production-vs-cross-encoder/) (cross-encoder와 비교한 운영 사례) | 2.00, 0.99 |

학생 인지 실험 논문의 응답이다. `legend`는 요청에 넣은 단계 설명을 번호와 함께 돌려준다.

```json
"level": {
  "type": "score",
  "score": 1.31,
  "confidence": 0.0,
  "legend": {"0": "General audience: ...", "1": "Working developer: ...", "2": "Specialist: ..."},
  "probabilities": {"0": 0.26, "1": 0.17, "2": 0.57}
}
```

점수는 단계별 확률의 가중평균이라 단계 사이의 값이 나온다. 이 논문의 1.31만 보면 현업 개발자보다 조금 어려운 글 같지만, 확률은 누구나(0.26)와 전문 지식(0.57)으로 갈렸고 가운데 단계는 0.17뿐이다. 확신도도 0.00이었다. 가장 높은 확률(0.57)이 Choice 예시(0.51)보다 높은데도 확신도는 더 낮다. 계산식은 공개되지 않았지만, 확률이 서로 떨어진 두 단계로 갈린 것이 반영된 것으로 보인다. 교육 연구라 코드 지식 없이도 읽히지만 통계 분석을 따라가려면 전문 지식이 필요해서, 두 판단이 모두 나올 만한 글로 보인다. 점수가 일정 값을 넘는지로 글을 거를 때는 확신도가 낮은 응답을 따로 봐야 한다.

## Jev에 맡길 일과 맡기지 않을 일

| 판단 | 맡길 곳 |
| --- | --- |
| 입력만 읽으면 확인할 수 있는 기준 (주제를 다루는가, 읽는 데 어떤 지식이 필요한가) | Jev |
| 입력 밖을 추론하거나 여러 단계를 거쳐야 하는 판단 | LLM |
| 왜 그렇게 판단했는지 설명이 필요한 경우 | LLM |
| 매주 수백, 수천 건씩 들어오는 판단 | Jev |

이 노트의 예시는 모두 판단 기준이 **입력 안에 적혀 있는** 경우다. 입력 밖을 추론해야 하는 판단은 LLM 쪽에 두었다. 공식 [jev-1.13 약점 문서](https://docs.typesafe.ai/model-jaggedness/jev-1.13)가 여러 단계를 거치는 추론을 약점으로 꼽기 때문이다. 쓸모는 정확도보다 양에서 갈렸다. 한 주 치 논문과 글 1,600여 건은 직접 읽거나 LLM에 모두 넘기기에는 많은데, Jev에는 제목과 초록만 보내 1분이 안 걸려 5센트쯤으로 후보를 좁혔다.

노트 74개의 태그 분류처럼 한 번 하고 끝나는 일은 LLM으로도 충분하다. 그래도 Jev의 확률은 쓸모가 있었다. 확신도가 1.0인데 내 태그와 다른 노트는 태그를 다시 볼 이유가 됐고, 보리스 체르니 노트처럼 확신도가 낮은 노트는 Jev의 답 대신 내가 정했다. Jev의 답을 그대로 따르기보다, 확률을 보고 어디까지 코드에 맡기고 어디부터 직접 볼지 정하는 데 쓰는 편이 맞았다.

[^schema]: TypeSafe, [SDE cascade](https://docs.typesafe.ai/cookbooks/sde_cascade), 공식 쿡북. 작은 LLM이 JSON 스키마를 통과한 추출 결과에 원문에 없는 날짜를 지어 넣은 사례를 보이고, 스키마 검사로는 이를 잡을 수 없다고 설명한다.
