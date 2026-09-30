---
created: 2026-09-24
updated: 2026-09-30
slug: jev-system-one
summary: 문장 대신 선택지별 확률을 돌려주는 Jev는 LLM과 무엇이 다르고, 어떤 판단을 맡길 만한가.
tags:
  - AI
---

# Jev와 System One 모델

[TypeSafe AI](https://typesafe.ai/)가 공개한 ==Jev==가 요즘 화제라 살펴봤다. LLM과 달리 답을 문장으로 쓰지 않고, 미리 정한 선택지마다 확률을 매겨 돌려준다. 질문 타입 세 가지로 내 관심사와 맞는 논문과 글을 필터링하고 Obsidian 노트들의 태그를 분류해 봤다. 시험한 버전은 `jev-1.13.0`이다.

## System One 모델

[공식 발표 글](https://typesafe.ai/blog/introducing-system-one-models-and-jev)은 Jev를 **System One 모델**^[이름은 Kahneman이 빠르고 직관적인 판단을 *시스템 1*, 느리고 신중한 추론을 *시스템 2*로 나눈 데서 따왔다.] 가운데 첫 번째로 소개한다. 채팅과 글쓰기는 LLM에 맡기고, Jev는 프로그램이 바로 받아 쓸 수 있는 판단을 빠르게 내리는 데 집중한다고 한다.

LLM과 가장 다른 점은 선택지마다 계산해 돌려주는 확률이다. LLM에도 Structured Outputs로 선택지별 확률 필드를 채우게 할 수는 있다. 하지만 그 숫자는 모델이 계산한 값이 아니라 답과 함께 생성한 텍스트다. 발표 글은 이렇게 받은 숫자가 실제보다 높게 나오고 요청마다 달라진다고 지적한다.

Jev는 선택지를 미리 받아 모든 선택지의 확률을 한 번에 계산한다. TypeSafe는 이 확률이 실제 정답률과 맞도록 학습시켰다고 한다. 그래서 코드가 확률을 보고 바로 처리할지, 사람에게 넘길지 정할 수 있다. 답은 주어진 선택지 안에서만 나오고, 문장이나 코드, 설명은 만들지 못한다.

## 질문 타입

질문 타입은 필요한 답의 형태에 맞춰 고른다.

| 타입 | 돌려주는 값 |
| --- | --- |
| **Noul** (예/아니오) | "예"일 확률 (0~1) |
| **Choice** (선택지 고르기) | 선택지마다 확률, 고른 선택지, 확신도 |
| **Score** (단계 매기기) | 단계마다 확률, 그 가중평균인 점수, 확신도 |

[Confidence 문서](https://docs.typesafe.ai/confidence)에 따르면 **Confidence(확신도)** 는 확률 분포에서 계산한 값으로, 확률이 한 선택지에 몰릴수록 높고 고르게 퍼질수록 낮다. 값이 0이나 1에 가까울수록 모델이 한쪽 답에 확률을 몰아 준 것이다. Noul은 "예"일 확률 하나로 충분해서 확신도를 따로 주지 않는다.

### Noul: 관심 주제 판정

매주 arXiv와 각종 커뮤니티에 쌓이는 논문과 글에서 내 관심사에 맞는 읽을거리를 고르는 데 썼다. 관심 주제를 질문 다섯 개로 정리해 질문마다 Noul을 하나씩 두고, 글의 제목과 초록을 함께 보냈다. 한 글이 여러 질문에 해당할 수 있어서 Choice가 아닌 Noul 여러 개로 물었다. 하나라도 0.8을 넘은 글만 그 주의 읽을거리 후보에 올렸다.

```python
from typesafe_sdk import Noul, TypeSafeClient

client = TypeSafeClient()
state = {"title": title, "summary": abstract}  # 글의 제목과 초록
questions = {
    # 이 글은 AI 도구가 사람의 이해와 역량에 미치는 영향을 다루는가
    "comprehension_debt": Noul(instructions="Does this item discuss how using AI assistants, especially coding assistants, affects people's own understanding of the work, their skill development, or their skill decline?"),
    # ... 나머지 네 질문
}
result = client.system_one(state, questions)
print(result.nouls["comprehension_debt"].noul)  # 0.97
```

예시로 든 글은 ChatGPT를 쓴 프로그래밍 수업에서 학생들의 과제 점수는 높았지만 기억한 내용은 적었다는 [실험 논문](https://arxiv.org/abs/2609.21194)이다. 이 논문을 실제로 판정한 결과는 다음과 같다.

| 관심 질문 | "예"일 확률 |
| --- | --- |
| 이 글은 AI 도구가 사람의 이해와 역량에 미치는 영향을 다루는가 | 0.97 |
| 이 글은 AI를 쓰면서 사람의 사고가 유지되거나 길러지는지를 다루는가 | 0.72 |
| 이 글은 사람이 AI 산출물을 수락하기 전에 확인하는 방법을 다루는가 | 0.30 |
| 이 글은 개인 지식 관리와 글쓰기를 다루는가 | 0.08 |
| 이 글은 팀과 조직이 AI를 받아들이는 방식을 다루는가 | 0.05 |

이 확률은 "제목과 초록이 이 주제를 다루는가"에 대한 답이 "예"일 확률이다. 0.97이라는 답은 "많이 다룬다"가 아니라 "다룬다고 거의 확신한다"는 뜻이다. 얼마나 많이 다루는지처럼 정도를 판단하려면 단계를 다루는 Score를 쓴다.

LLM과 마찬가지로 질문을 잘 설계해야 한다. 위 표의 두 번째 질문은 원래 "사람이 통제권을 유지하는 의사결정 지원을 다루는가"였는데, 이 질문에는 계약서의 모순을 찾아 주는 분석 도구 논문까지 0.96이 나왔다. 지금처럼 "사람의 사고가 유지되거나 길러지는가"로 좁히자 같은 논문이 0.40으로 내려갔다.

### Choice: 노트 태그 분류

내 노트와 블로그 글에는 `개발`, `커리어`, `AI`처럼 직접 정한 주제 태그 가운데 하나를 메인 태그로 붙인다. Jev에는 노트의 제목, 요약, 본문 일부를 보내고 **Choice**로 가장 맞는 태그를 고르게 했다.

공개 노트 74개에 돌려 본 뒤, 확신도가 0.8 이상인데 내 태그와 다른 노트 8개를 다시 확인했다. [[SLII 01 - 상황에 따른 맞춤형 리더십|리더십을 다룬 블로그 글]]은 `커리어` 태그였는데 Jev는 1.0의 확신도로 `조직`을 선택했다. 깔끔하게 인정하고 태그를 `커리어`에서 `조직`으로 바꿨다. 반대로 [[AI 시대의 판단력은 맥락을 실행 기준으로 바꾸는 능력이다]]는 `AI`가 확신도 0.97로 나왔지만 `철학`을 유지했다. 제목에 "AI"가 들어 있을 뿐, 무엇에 무게를 두고 선택하는가를 다루는 글이기 때문이다.

다음은 [[보리스 체르니의 다섯 아키타입으로 본 나의 작업 방식|내 작업 방식을 다룬 노트]]를 Choice로 분류해 본 예제다.

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

Jev는 딱 맞는 답이 없어도 주어진 선택지 중 하나를 고르므로 "해당 없음"(`none_of_the_above`)을 선택지에 넣었다. 선택지 이름과 설명은 그대로 모델에 들어가므로, [Choice 문서](https://docs.typesafe.ai/primitives/choice)가 권하는 대로 서로 겹치지 않게 쓴다.

이 노트의 실제 판정 결과다.

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

Jev의 *choice*는 `개발`이었지만 *probabilities*를 보면 `커리어`일 가능성도 0.34라고 봤고 최종 *confidence*는 0.44에 그쳤다. 해당 노트에 내가 실제로 붙인 태그는 `커리어`였다. 확신도가 이렇게 낮으면 Jev의 답을 그대로 믿지 않고 직접 확인한다.

### Score: 적용 절차의 구체성

**Score**는 어디에 써볼 수 있을지 고민하다 읽을거리 후보 들 중 직접 따라해볼 수 있는 자료인지 여부를 알려주는 데에 실험해봤다. 적용 방법이 없는 글은 0, 원리와 예시를 설명하지만 실행 절차가 부족한 글은 1, 필요한 준비와 실행 절차를 제시한 글은 2로 정했다.

```python
from typesafe_sdk import Score

state = {"title": title, "text": body}  # 이미지와 링크 주소 같은 잡음을 뺀 본문. 논문은 초록
question = Score(
    instructions="How specific are the practical implementation instructions in the supplied text? Judge only this text, not linked pages or prior knowledge. Rate procedural specificity, not article value, scientific quality, or the presence of code alone.",
    criteria=[
        "The text presents news, opinions, claims or results, but gives no practical explanation or instructions for implementing or trying the described technique.",
        "The text explains the technique with concepts, workflow or illustrative examples, but lacks the concrete setup and execution instructions needed to try it from this text alone.",
        "The text supplies concrete setup and execution steps, commands, code or interface actions sufficient to try the described technique, with necessary prerequisites stated. This does not guarantee that the procedure works.",
    ],
)
result = client.system_one(state, {"specificity": question})
answer = result.scores["specificity"]
print(answer.score, answer.confidence)  # 2.0 1.0
```

최근 읽을거리 후보 다섯 편의 실제 판정 결과다.

| 글 | 점수 (0~2), 확신도 | 확률 (0 / 1 / 2) |
| --- | --- | --- |
| ["rogue" AI 에이전트는 없다](https://eoinhiggins.substack.com/p/there-are-no-rogue-ai-agents) | 0.00, 1.00 | 1.00 / 0.00 / 0.00 |
| [AI 없이 한 달](https://blog.bustikiller.com/2026/09/25/one-month-without-ai.html) | 0.24, 0.64 | 0.76 / 0.24 / 0.00 |
| [The Work Behind Delegation](https://arxiv.org/abs/2609.24234) | 0.49, 0.26 | 0.51 / 0.49 / 0.00 |
| [일이 너무 많을 때](https://hbr.org/2026/09/what-to-do-when-theres-too-much-work) (HBR) | 1.08, 0.88 | 0.00 / 0.92 / 0.08 |
| [jevgrep](https://github.com/dzhng/jevgrep) | 2.00, 1.00 | 0.00 / 0.00 / 1.00 |

점수는 단계별 확률의 가중평균이라 확률이 갈리면 단계 사이의 값이 나온다. 「The Work Behind Delegation」의 0.49는 0과 1 사이의 글이라는 뜻이 아니라, 적용 방법이 없다(0.51)와 원리를 설명한다(0.49)로 반씩 갈렸다는 뜻이다. 확신도도 0.26으로 낮다. 개발자가 AI 에이전트를 감독하는 과정을 틀로 정리한 논문이라 원리 설명으로도, 연구 결과 보고로도 읽힐 수 있다.

Jev는 다섯 편 가운데 jevgrep 하나만 직접 따라 해볼 수 있는 글로 골랐다. 점수나 확신도가 높다고 더 적합한 글이라는 뜻은 아니다. 개념을 이해하려는지, 직접 시험하려는지에 따라 필요한 자료가 다르다.

## Jev에 맡길 일과 맡기지 않을 일

| 판단                                               | 맡길 곳 |
| ------------------------------------------------ | ---- |
| 입력만 읽으면 확인할 수 있는 기준 (주제를 다루는가, 적용 절차가 얼마나 구체적인가) | Jev  |
| 입력 밖을 추론하거나 여러 단계를 거쳐야 하는 판단                     | LLM  |
| 왜 그렇게 판단했는지 설명이 필요한 경우                           | LLM  |

여러 단계를 거치는 추론을 LLM에 둔 것은 공식 [jev-1.13 약점 문서](https://docs.typesafe.ai/model-jaggedness/jev-1.13)가 이를 약점으로 꼽기 때문이다. 반면 Jev는 많은 글을 빠르고 싸게 거르는 데 강했다. 한 주 치 논문과 글 1,600여 건은 직접 읽거나 LLM에 모두 넘기기에는 많은데, Jev에는 제목과 초록만 보내 관심 질문 다섯 개로 판정했다. 1분도 걸리지 않았고 비용은 $0.05쯤이었다.

노트의 태그를 한 번 검토하는 일은 LLM으로도 충분하다. 그래도 Jev의 확률은 쓸모가 있었다. 확신도가 낮은 답과, 확신도가 높은데 내 판단과 어긋난 답을 직접 봤다. Jev의 답을 그대로 따르기보다, 확률을 보고 어디까지 코드에 맡기고 어디부터 직접 볼지 정하는 데 쓰는 편이 맞았다.
