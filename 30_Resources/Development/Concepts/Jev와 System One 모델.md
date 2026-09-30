---
created: 2026-09-24
updated: 2026-09-30
slug: jev-system-one
summary: 문장 대신 선택지별 확률을 돌려주는 Jev는 LLM과 무엇이 다르고, 그 확률은 어디에 쓸모가 있는가.
tags:
  - AI
---

# Jev와 System One 모델

TypeSafe AI가 공개한 Jev가 요즘 화제라 살펴봤다. LLM처럼 답을 문장으로 쓰지 않고 미리 정한 선택지 가운데 답을 확률과 함께 돌려주는 모델이다. 질문 타입 세 가지를 매주 쏟아지는 논문·글과 내 Obsidian 노트에 하나씩 적용해 봤다. 시험한 버전은 `jev-1.13.0`이다.

## System One 모델

[공식 발표 글](https://typesafe.ai/blog/introducing-system-one-models-and-jev)은 Jev를 **System One 모델**의 첫 모델로 소개한다. 이름은 Kahneman이 빠르고 직관적인 판단을 시스템 1, 느리고 신중한 추론을 시스템 2로 나눈 데서 따왔다. 채팅과 글쓰기는 LLM에 맡기고, Jev는 소프트웨어가 바로 쓸 수 있는 구조화된 판단을 빠르게 내리는 것이 목표라고 한다.

LLM과 가장 다른 점은 답에 붙는 확률이다. LLM도 Structured Outputs로 JSON 스키마를 강제할 수 있지만, 답은 여전히 토큰을 이어 쓴 값 하나다. 확신도를 필드로 달라고 해도 그 숫자 역시 생성한 텍스트라, 발표 글은 LLM이 과신하고 일관되지 않다고 지적한다.

Jev는 선택지를 미리 받아 모든 선택지의 확률을 한 번에 계산하고 이 확률이 실제 정답률과 맞도록 학습했다고 밝힌다. 그래서 코드가 확률을 보고 바로 처리할지, 사람에게 넘길지 정할 수 있다. 선택지 밖의 답은 나오지 않는 대신 문장, 코드, 설명은 만들지 못한다. 발표 글은 System One 형태의 질문에서 비슷한 수준의 LLM보다 40~200배 빠르고 가격은 입력 100만 토큰당 $0.042이며 출력은 무료라고 밝힌다.

## 질문 타입

| 타입 | 돌려주는 값 |
| --- | --- |
| **Noul** (예/아니오) | "예"일 확률 (0~1) |
| **Choice** (선택지 고르기) | 선택지마다 확률, 가장 높은 선택지와 그 확신도 |
| **Score** (단계 매기기) | 단계별 확률의 가중평균과 확신도 |

[Confidence 문서](https://docs.typesafe.ai/confidence)에 따르면 ==Confidence(확신도)==는 확률 분포에서 계산한 값으로, 확률이 한 선택지에 몰릴수록 높고 고르게 퍼질수록 낮다. Noul은 답이 예와 아니오뿐이라 확률 하나로 충분하므로 확신도를 따로 주지 않는다. 값이 0이나 1에 가까울수록 모델이 한쪽 답에 확률을 몰아 준 것이다.

판단할 자료(`state`)는 한 번만 보내고 그 자료에 대한 질문 여러 개를 한 요청에 묶을 수 있다. 질문은 병렬로 평가되어 여러 개를 묶어도 응답 시간이 거의 늘지 않는다. 아래 예시는 Python SDK(`typesafe-sdk`)로 실제로 돌린 호출을 기반으로 간소화한 것이다.

### Noul: 관심 주제 판정

매주 arXiv와 각종 커뮤니티에 쌓이는 논문과 글에서 내 관심사에 맞는 읽을 거리를 고르는 데 썼다. 내 관심 주제를 몇 가지 질문으로 정리하고 질문마다 Noul을 하나씩 두어 글의 제목과 초록을 보낸다. 한 글이 여러 질문에 해당할 수 있어서 Choice가 아닌 Noul 여러 개로 물었다. 하나라도 0.8을 넘은 글만 그 주에 읽어볼 만한 글 목록에 올린다.

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

아래는 'ChatGPT를 쓴 프로그래밍 수업의 학생들이 과제 점수는 높았지만 기억한 내용은 적었다는 [실험 논문](https://arxiv.org/abs/2609.21194)'을 판정한 결과다.

| 관심 질문 | "예"일 확률 |
| --- | --- |
| AI 도구가 사람의 이해와 역량을 어떻게 바꾸는가 | 0.97 |
| AI를 쓰면서 사람의 사고가 유지되거나 길러지는가 | 0.72 |
| 사람이 AI 산출물을 수락하기 전에 어떻게 확인하는가 | 0.30 |
| 개인 지식 관리와 글쓰기 | 0.08 |
| 팀과 조직이 AI를 어떻게 받아들이는가 | 0.05 |

이 확률은 "제목과 초록이 이 주제를 다루는가"에 대한 답이 "예"일 확률이다. 0.97이라는 답은 "많이 다룬다"가 아니라 "다룬다고 거의 확신한다"는 뜻이다. 얼마나 많이 다루는지처럼 정도를 재려면 순서 있는 단계로 묻는 Score를 쓴다.

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

Jev는 딱 맞는 답이 없어도 주어진 선택지 중 하나를 고르므로 "해당 없음"(`none_of_the_above`)을 선택지에 넣었다. 선택지 이름과 설명은 모델에 그대로 전달되므로 [Choice 문서](https://docs.typesafe.ai/primitives/choice)의 권장대로 서로 구분되게 쓴다.

아래는 [[보리스 체르니의 다섯 아키타입으로 본 나의 작업 방식|나의 개발 스타일을 다룬 노트]]의 Choice 응답이다.

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

Jev의 `choice`는 `개발`이지만 `커리어`에도 0.34가 가서 확신도는 0.44에 그쳤다. 실제로 내가 붙인 태그는 `커리어`였고, 이렇게 확신도가 낮은 노트는 Jev의 답을 그대로 반영하기보다 사람이 직접 확인하는 것이 좋다.

[[SLII 01 - 상황에 따른 맞춤형 리더십|리더십을 다룬 블로그 글]]은 `조직`이 확신도 1.0으로 나와 `커리어` 태그에서 `조직`으로 바꾸기도 했다. 반대로 [[AI 시대의 판단력은 맥락을 실행 기준으로 바꾸는 능력이다]]는 제목의 단어에 이끌렸는지 `AI`가 나와서 기존 `철학` 태그를 유지했다.

### Score: 읽을거리의 근거 수준

읽을거리 후보 목록에 오른 글은 노트를 쓸 때 근거로 인용할 수도 있어서, 글마다 주장을 무엇으로 뒷받침하는지 세 단계로 나눠 봤다. 의견, 경험, 측정은 근거의 강도에 순서가 있으므로 Choice 대신 **Score**를 쓴다.

| 단계 | 기준 |
| --- | --- |
| 0 의견 | 작성자의 견해와 추론이 중심이다 |
| 1 경험 | 작성자나 한 팀이 직접 해 본 경험을 근거로 든다 |
| 2 측정 | 실험, 벤치마크, 수집한 데이터를 근거로 든다 |

```python
from typesafe_sdk import Score

state = {"title": title, "text": body}  # 이미지와 링크 주소 같은 잡음을 뺀 본문. 논문은 초록
question = Score(
    instructions="What kind of evidence does this article mainly rely on to support its claims?",
    criteria=[
        # 0: 의견
        "Opinion: the article argues from the author's views and reasoning, without its own measurements or a first-hand account of trying something.",
        # 1: 경험
        "Experience: the main evidence is the author's or one team's first-hand account of trying something, without systematic measurement.",
        # 2: 측정
        "Measurement: the article presents experiments, benchmarks, or collected data such as counts, rates, or comparisons across conditions.",
    ],
)
result = client.system_one(state, {"evidence": question})
answer = result.scores["evidence"]
print(answer.score, answer.confidence)  # 2.0 1.0
```

최근 후보로 들어온 글 여섯 편의 결과다.

| 글                                                                                      | 점수 (0~2), 확신도 | 확률 (의견 / 경험 / 측정)  |
| -------------------------------------------------------------------------------------- | ------------- | ------------------ |
| ["rogue" AI 에이전트는 없다](https://eoinhiggins.substack.com/p/there-are-no-rogue-ai-agents) | 0.01, 0.99    | 1.00 / 0.00 / 0.00 |
| [AI 없이 한 달](https://blog.bustikiller.com/2026/09/25/one-month-without-ai.html)         | 1.00, 1.00    | 0.00 / 1.00 / 0.00 |
| [일이 너무 많을 때](https://hbr.org/2026/09/what-to-do-when-theres-too-much-work) (HBR)       | 1.45, 0.18    | 0.27 / 0.00 / 0.73 |
| [The Work Behind Delegation](https://arxiv.org/abs/2609.24234)                         | 1.36, 0.43    | 0.01 / 0.62 / 0.37 |
| [ChatGPT를 쓴 학생의 인지 실험](https://arxiv.org/abs/2609.21194)                               | 2.00, 1.00    | 0.00 / 0.00 / 1.00 |

점수는 단계별 확률의 가중평균이라, 확률이 떨어진 두 단계로 갈리면 그 사이 값이 나온다. HBR 뉴스레터의 1.45는 경험 단계처럼 보이지만 경험의 확률은 0이고 의견과 측정으로 갈렸다. 조언이 중심인데 설문과 데이터를 언급한 글이었기 때문인 것으로 보인다. 단순 점수 뿐만 아니라 확신도와 확률 분포도 함께 봐야 한다.

## Jev에 맡길 일과 맡기지 않을 일

| 판단                                               | 맡길 곳 |
| ------------------------------------------------ | ---- |
| 입력만 읽으면 확인할 수 있는 기준 (주제를 다루는가, 어떤 근거를 내세우는가) | Jev  |
| 입력 밖을 추론하거나 여러 단계를 거쳐야 하는 판단                     | LLM  |
| 왜 그렇게 판단했는지 설명이 필요한 경우                           | LLM  |

여러 단계를 거치는 추론을 LLM에 둔 것은 공식 [jev-1.13 약점 문서](https://docs.typesafe.ai/model-jaggedness/jev-1.13)가 이를 약점으로 꼽기 때문이다. 강점은 양에서 드러났다. 한 주 치 논문과 글 1,600여 건은 직접 읽거나 LLM에 모두 넘기기에는 많은데, Jev에는 제목과 초록만 보내 1분이 안 걸려 $0.05쯤으로 후보를 좁혔다.

노트 74개의 태그 분류처럼 한 번 하고 끝나는 일은 LLM으로도 충분하다. 그래도 Jev의 확률은 쓸모가 있었다. 확신도가 낮은 답과, 확신도가 높은데 내 판단과 어긋난 답을 직접 봤다. Jev의 답을 그대로 따르기보다, 확률을 보고 어디까지 코드에 맡기고 어디부터 직접 볼지 정하는 데 쓰는 편이 맞았다.
