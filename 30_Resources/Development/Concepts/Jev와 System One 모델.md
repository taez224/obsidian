---
created: 2026-09-24
updated: 2026-09-26
slug: jev-system-one
summary: 문장 대신 정해진 선택지와 확률을 돌려주는 System One 모델 Jev는 무엇이고, 읽을거리 선별과 노트 정리에 적용하면 어떤 판단을 맡길 수 있는가.
tags:
  - AI
---

# Jev와 System One 모델

TypeSafe AI가 공개한 Jev가 요즘 화제라 살펴봤다. LLM처럼 답을 문장으로 쓰지 않고, 질문에 대해 선택된 값이나 점수와 함께 확률을 돌려주는 모델이다. 한국어 자료에 어디까지 쓸 수 있을지 궁금해서 두 곳에 적용해 봤다. 매주 쏟아지는 논문과 글에서 읽을 것을 고르는 일과, 내 노트를 주제별로 나누고 다시 읽을 노트를 고르는 일이다. 시험한 버전은 2026년 9월에 나온 `jev-1.13.0`이다.

## System One 모델

[공식 발표 글](https://typesafe.ai/blog/introducing-system-one-models-and-jev)은 Jev를 **System One 모델**의 첫 모델로 소개한다. 이름은 Kahneman이 빠르고 직관적인 판단을 시스템 1, 느리고 신중한 추론을 시스템 2로 나눈 데서 따왔다. 채팅과 글쓰기는 LLM에 맡기고, 소프트웨어 안에서 반복되는 작은 판단을 빠르고 싸게 내리는 것이 목표다.

LLM과 가장 다른 점은 출력이다. LLM은 답을 토큰 단위로 이어 쓰기 때문에 결과를 코드에서 쓰려면 문장을 다시 해석해야 하고, 가끔 형식이 깨진다. Jev는 선택지를 미리 받고 모든 선택지의 확률을 한 번에 계산해 돌려준다. 선택지 밖의 답은 나올 수 없다. 대신 문장, 코드, 설명은 만들지 못한다. 발표 글은 비교 가능한 LLM보다 40~200배 빠르고, 가격은 입력 100만 토큰당 $0.042라고 밝힌다.

## 질문 타입

질문은 세 가지 타입 중에서 고른다.

| 타입 | 돌려주는 값 |
| --- | --- |
| 예/아니오 질문 (Noul) | "예"일 확률 (0~1) |
| 선택지 고르기 (Choice) | 선택지마다 확률, 가장 높은 선택지, 그 선택의 확신도 |
| 단계 매기기 (Score) | 낮음·보통·높음처럼 순서가 있는 단계 위의 위치와 단계별 확률 |

SDK와 API에서는 괄호 안의 이름을 쓴다. 판단할 자료(`state`)는 한 번만 보내고, 그 자료에 대한 질문 여러 개를 한 요청에 묶을 수 있다. 아래 예시는 Python SDK(`typesafe-sdk`)로 실제로 돌린 호출이다. 흐름을 보여주기 위해 입력과 선택지 일부를 줄였으며, `title`·`body` 같은 변수는 앞에서 준비한 값이다. 지시문은 영어로 썼다. 공식 문서가 영어를 주 학습 언어로 밝히고 있어서다.

## 읽을거리 선별에 적용

arXiv의 HCI·소프트웨어공학·AI 분야에는 일주일에 논문이 1,000편 넘게 올라오고, Hacker News와 GeekNews에도 수백 건이 쌓인다. 다 읽을 수는 없어서, 내 노트에 적어 둔 주장을 관심 질문으로 바꿔 Jev에게 거르게 했다.

| 관심 질문 | 바탕이 된 노트 |
| --- | --- |
| AI 도구가 사람의 이해와 역량을 어떻게 바꾸는가 | [[AI 코딩 도구는 이해 부채를 만든다]] |
| 사람이 AI 산출물을 수락하기 전에 어떻게 확인하는가 | [[생성은 AI에게, 검증은 나에게]] |
| 팀과 조직이 AI를 어떻게 받아들이는가 | [[팀의 AI 역량은 사용량이 아니라 회수율로 드러난다]] |
| AI를 쓰면서 사람의 사고가 유지되거나 길러지는가 | [[AI와의 스파링으로 내 생각을 끌어내고 다듬는다]] |
| 개인 지식 관리와 글쓰기 | [[세컨드 브레인은 퍼스트 브레인의 사고를 보조해야 한다]] |

질문마다 예/아니오 질문(Noul)을 하나씩 두고, 논문이나 글의 제목과 초록을 한 요청에 보낸다. 질문은 병렬로 평가되므로 다섯 개를 묶어도 응답 시간은 거의 늘지 않는다.

```python
from typesafe_sdk import Noul, TypeSafeClient

client = TypeSafeClient()  # TYPESAFE_API_KEY 환경 변수를 읽는다
QUESTIONS = {
    "comprehension": Noul(instructions=(
        "Does this item discuss how using AI assistants, especially coding assistants, affects people's own "
        "understanding of the work, their skill development, or their skill decline?")),
    # ... 나머지 네 질문
}

result = client.system_one({"title": title, "summary": abstract}, QUESTIONS)
scores = {k: result.nouls[k].noul for k in QUESTIONS}
```

실제 입력 한 건과 결과다. ChatGPT를 쓴 프로그래밍 수업의 학생들이 과제 점수는 높았지만 직후와 48시간 뒤에 기억한 내용은 적었다는 [실험 논문](https://arxiv.org/abs/2609.21194)이다. 실제 호출에서는 제목과 초록 전체를 보냈고, 아래에는 초록 앞부분만 남겼다.

```python
state = {
    "title": "Your Programming Students' Cognition with ChatGPT: "
             "Higher Performance, Lower Retention, and Reduced Ownership",
    "summary": "Generative AI can improve students' programming performance, but successful task "
               "completion may not reflect what they retain. We examined performance, retention, ...",
}
```

점수는 논문의 결론이 맞을 확률이 아니라, 제목과 초록이 각 관심 주제를 다룬다고 Jev가 판단한 정도다.

| 관심 주제 | "예"일 확률 |
| --- | --- |
| AI 도구와 이해·역량 | 0.97 |
| AI 사용과 사고의 유지·발달 | 0.74 |
| AI 산출물의 확인 | 0.33 |
| 개인 지식 관리와 글쓰기 | 0.08 |
| 팀과 조직의 AI 수용 | 0.05 |

질문이 넓으면 넓은 대로 충실하게 고른다는 점은 조심해야 했다. 처음에는 "사람이 통제권을 유지하는 의사결정 지원"을 물었더니 계약서의 모순을 찾아 주는 분석 도구 논문이 0.96으로 올라왔다. 질문을 "사람의 사고가 유지되거나 길러지는가"로 좁히자 같은 논문은 0.40으로 내려갔다.

질문 하나라도 0.8을 넘은 것만 모아, 출처별로 상위 3~5건씩 주간 목록을 만든다. 논문과 글 1,600여 건을 판정하는 데 1분이 안 걸렸고 5센트쯤 들었다.

시험하는 동안 걸러진 목록에서 논문 5편과 글 3편을 읽을 자료로 저장했다. 목록에서 빠진 좋은 글이 얼마나 되는지는 재지 않았다.

### 점수순 목록에서 읽기 묶음으로

관련성이 높은 글만 고르면 비슷한 자료가 반복될 수 있다. 그래서 ‘AI 도구와 이해·역량’ 주제에는 자료의 특징을 함께 고려하는 읽기 묶음을 추가했다.

Jev에는 제목과 초록을 보고 현업 개발자를 대상으로 했는지, 시간이 지난 뒤에도 측정했는지, AI 없이 수행하는 평가가 있는지, 사람의 이해나 역량을 측정했는지를 물었다. Choice로 ‘명시됨·명시적 제외·미확인’을 고르게 하고, 실증 연구·적용 경험·해설 같은 자료 유형도 구분했다.

이 판단은 저장해 두고 다시 쓴다. 코드는 저장 자료에서 드물게 확인된 조건과 자료 유형을 고려하고, 중복을 줄여 함께 읽을 목록을 만든다. ‘이미 앎’과 ‘관심 밖’ 같은 반응도 구분해 기록하고, 실제로 도움이 됐다는 반응이 쌓이면 선택 가중치를 조정하도록 했다. 자료를 열거나 저장한 것만으로 도움이 됐다고 간주하지는 않는다.

첫 실행에서는 논문 한 편과 적용 경험 글 한 편을 골랐다. 다만 초록만으로는 확인되지 않거나 모델의 확신이 낮은 연구 조건이 많았다. 저장 자료에서 드물게 확인된 조건이 학계에서도 드문 것은 아니므로, 우선 다시 읽을 이유를 찾는 단서로만 쓴다. 목록은 만들었지만 추천이 실제로 좋아졌는지는 읽은 뒤의 반응으로 확인해야 한다.

## 노트 정리에 적용

### 주제 분류

내 노트와 글에는 조직, 커리어, AI처럼 직접 정해 둔 주제 8개 가운데 하나가 붙어 있다. 노트의 제목, 요약문, 본문 앞부분을 보내고 선택지 고르기(Choice)로 하나를 고르게 했다. 예시는 상황적 리더십 모델을 다룬 [[SLII 01 - 상황에 따른 맞춤형 리더십|블로그 글]]이다.

```python
from typesafe_sdk import Choice

result = client.system_one(
    {
        "title": "SLII®: 상황에 따른 맞춤형 리더십",
        "summary": "팀원의 역량과 몰입을 기준으로 개발 수준을 진단하고, ... SLII 모델의 구조를 정리한다.",
        "body_excerpt": body[:2000],
    },
    {
        "topic": Choice(
            instructions="Which topic is this note's main claim about? "
                         "Judge by what the note argues, not by words it merely mentions.",
            criteria={
                "조직": "Organizations: delegation, hiring, team performance, leadership; "
                        "principles that still hold without AI.",
                "커리어": "Career and self-development: growth, skills and learning, "
                          "self-management, motivation, job changes, seniority.",
                # ... AI, 개발, 심리, 철학, 글쓰기, 지식관리
                "none_of_the_above": "The note fits none of the topics above.",
            },
        ),
    },
)
answer = result.choices["topic"]
print(answer.choice, answer.confidence)  # 조직 1.0
```

이 글에는 원래 `커리어`가 붙어 있었는데, 다시 읽어 보니 리더십을 다루는 글이라 Jev의 답이 맞았다. 노트 74개에 돌려 보니 80%가 기존 분류와 같았고, 확신도가 0.8 이상인데 기존과 다른 8개를 다시 읽어 보니 5개는 기존 분류가 틀렸다. Jev가 틀린 답은 "AI 시대의 판단력"처럼 제목에 들어간 단어에 끌려 `AI`를 고른 경우가 많았다.

그래서 분류를 자동으로 바꾸지 않고, 확신도가 높은데 어긋난 노트만 골라 다시 읽는 데 썼다.

선택지에는 "해당 없음"(`none_of_the_above`)을 꼭 넣었다. 맞는 답이 없을 때 고를 곳이 없으면, Jev는 그럴듯한 오답을 자신 있게 고른다.[^ko-audit] 선택지 이름과 설명은 모델에게 그대로 전달되므로, [Choice 문서](https://docs.typesafe.ai/primitives/choice)의 권장대로 선택지끼리 구분되게 설명을 쓴다.

### 본문의 뒷받침 정도

노트 본문이 중심 주장을 얼마나 뒷받침하는지 단계 매기기(Score)로 세 단계를 매기게 했다. 단계의 이름과 설명은 직접 정한다. 이번에는 주장과 설명만 있는지, 근거·반례·적용 사례 가운데 하나가 있는지, 둘 이상이 있는지다. 링크 수에 끌리지 않도록 출처와 연관된 노트 목록은 빼고 보냈다.

```python
from typesafe_sdk import Score

SUPPORT = Score(
    instructions="How much support does this Korean note give its central claim, beyond stating and explaining the claim? ...",
    criteria=[  # 낮은 단계부터 순서대로
        "Only the claim: ... no concrete evidence, no counterexample or limit, and no real case where it was applied.",
        "One kind of support: ... exactly one of concrete evidence, a counterexample or limit, or a real case.",
        "Several kinds of support: ... two or more of them.",
    ],
)
answer = client.system_one({"title": title, "body": body}, {"support": SUPPORT}).scores["support"]
```

| 노트 | 점수 (0~2) | 단계별 확률 | 확신도 |
| --- | --- | --- | --- |
| [[세컨드 브레인은 퍼스트 브레인의 사고를 보조해야 한다]] | 1.97 | 0: 0.01, 1: 0.02, 2: 0.97 | 0.96 |
| [[AI 코딩 도구는 이해 부채를 만든다]] | 0.80 | 0: 0.35, 1: 0.50, 2: 0.15 | 0.25 |

점수는 단계별 확률로 평균을 낸 값이라 단계 사이의 값이 될 수 있다. 확신도(`confidence`)는 API가 함께 돌려주는 값으로, Choice의 확신도처럼 확률이 한 단계에 몰릴수록 높고 여러 단계에 퍼질수록 낮다. 앞 노트는 본문에 한계와 적용 사례를 갖췄고, 뒤 노트는 본문 대부분이 설명이다. 비유만으로 된 노트를 높게 매기거나 주장 하나가 아니라 규칙 목록인 노트를 잘못 매긴 경우도 있어서, 점수는 다시 읽을 노트를 고르는 데만 썼다. 점수가 낮은 노트는 근거를 보강할 후보로, 높은데 아직 다듬지 않은 노트는 다듬을 후보로 다시 읽는다.

## 잘 맞지 않았던 곳

두 곳 말고도 판단을 몇 가지 더 시켜 봤다. 판단 기준이 **입력 안에 그대로 적혀 있는 것**은 잘했다. 초록이 어떤 주제를 다루는지, 노트의 본문에 근거나 적용 사례가 있는지는 입력만 읽으면 확인할 수 있다. 반대로 입력 밖을 추론해야 하는 판단으로 시험한 두 가지, 허수아비 찾기와 노트 관계 판단은 결과가 좋지 않았다.

허수아비는 상대 주장을 일부러 약하게 세워 두고 반박하는 글쓰기다. "플랫폼 팀은 지원 조직이 아니라 핵심 전략 엔진이다"처럼 "X가 아니라 Y"로 쓴 문장을 발행한 블로그 글에서 뽑아, X가 Y를 돋보이게 하려고 세워 둔 허수아비인지 물었다. 그걸 알려면 독자가 실제로 플랫폼 팀을 지원 조직으로 생각하는지부터 따져야 한다. Jev는 그런 문장 18개 중 1개만 찾았다.[^labels] 두 노트가 서로의 근거인지 반례인지를 물었을 때도 대부분 한두 가지 관계로 몰아 답했다. 공식 [jev-1.13 약점 문서](https://docs.typesafe.ai/model-jaggedness/jev-1.13)도 여러 단계를 거치는 추론을 약점으로 꼽는다.

판단이 정확해도 쓸모가 없는 곳도 있었다. 글에 근거로 붙일 내 경험 문단을 고르게 해 봤는데, 판단은 쓸 만했다. 하지만 나는 글을 LLM과 함께 쓰고, 노트를 검색해 쓸 문단을 고르는 일도 그 LLM이 이미 하고 있었다. 한 번에 문단 수십 개를 보는 일이라 Jev가 더 빠르고 싸도 달라지는 것이 없었다.

## 적용 범위와 한계

쓸모가 가장 분명했던 곳은 읽을거리 선별이다. 한 주 치 논문과 글은 양이 많아 사람이 직접 읽거나 글쓰기 LLM에 모두 넘기기에는 부담스럽고, Jev의 답은 사람이 다시 볼 후보에 그치며, 잘못 올라온 후보는 읽지 않고 넘길 수 있다. 노트 정리에서도 분류와 점수를 노트에 자동으로 반영하지 않고, 다시 읽을 노트를 고르는 데만 썼다.

노트 정리에는 영어 지시문과 한국어 노트를 함께 사용했다. 주제 분류에는 쓸 만했지만, 노트 관계를 해석하는 판단은 결과가 좋지 않았다. 지시문 언어에 따른 차이는 따로 비교하지 않았다. 독립 측정에서는 한국어 정확도가 영어보다 6.5%p 낮았다.[^ko-audit]

공개된 지 얼마 안 된 모델이라 제3자 검증은 아직 적다. 한 사회과학 분류 연구에서는 과제 15개 중 14개에서 가장 좋은 LLM보다 정확도가 낮았고, 비용은 44분의 1이었다.[^css-study] 정확도가 중요한 판단을 통째로 맡길 근거는 아직 없다.

[^labels]: 이 판단의 정답은 Jev를 돌리기 전에 Claude가 붙였다. 그래서 수치는 사람의 판단이 아니라 이 정답과의 일치다. 판단마다 한 번씩만 돌렸다.
[^ko-audit]: [jev-calibration-audit FINDINGS](https://github.com/jujumilk3/jev-calibration-audit/blob/main/FINDINGS.md), jujumilk3, GitHub, 2026-09-18. 영어 원문을 번역한 한국어 편향 벤치마크(KoBBQ)로 `jev-1.13.0`을 시험했다. 정답이 "알 수 없음"인 문항에서 이 선택지를 빼자 고정관념에 맞는 답을 다섯 번 중 네 번, 확신도 0.79로 골랐다. 한국어 정확도는 MMLU-ProX 기준으로 쟀다.
[^css-study]: Hazem Ibrahim, Yasir Zaki, [Evaluating Decision Models for Text Annotation in Computational Social Science](https://arxiv.org/abs/2609.24574), arXiv, 2026.
