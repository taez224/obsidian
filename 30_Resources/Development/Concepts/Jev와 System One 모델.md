---
created: 2026-09-24
updated: 2026-09-28
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

판단할 자료(`state`)는 한 번만 보내고 그 자료에 대한 질문 여러 개를 한 요청에 묶을 수 있다. 질문은 병렬로 평가되어 여러 개를 묶어도 응답 시간이 거의 늘지 않는다. 아래 예시는 Python SDK(`typesafe-sdk`)로 실제로 돌린 호출을 줄인 것이다. 코드의 `title`, `abstract`, `summary`, `body`, `text`는 미리 준비한 자료이며 생략한 질문과 선택지를 포함한 원래 호출의 결과를 함께 적었다. 지시문은 영어로 썼다. 공식 문서가 영어를 주 학습 언어로 밝히고 있어서다.

### Noul: 관심 주제 판정

매주 arXiv와 Hacker News에 쌓이는 논문과 글에서 읽을 것을 고르는 데 썼다. 노트에 적어 둔 내 주장(예: 「AI 코딩 도구는 이해 부채를 만든다」)을 관심 질문 다섯 개로 바꿔 질문마다 Noul을 하나씩 두고 글의 제목과 초록을 보낸다. 한 글이 여러 질문에 해당할 수 있어서 Choice 하나 대신 Noul 다섯 개로 물었다. 하나라도 0.8을 넘은 글만 주간 목록에 올린다.

```python
from typesafe_sdk import Noul, TypeSafeClient

client = TypeSafeClient()  # TYPESAFE_API_KEY 환경 변수를 읽는다
questions = {
    "comprehension_debt": Noul(instructions=(
        "Does this item discuss how using AI assistants, especially coding assistants, affects people's own "
        "understanding of the work, their skill development, or their skill decline?")),
    # ... 나머지 네 질문
}
result = client.system_one({"title": title, "summary": abstract}, questions)
scores = {k: result.nouls[k].noul for k in questions}
```

ChatGPT를 쓴 프로그래밍 수업의 학생들이 과제 점수는 높았지만 기억한 내용은 적었다는 [실험 논문](https://arxiv.org/abs/2609.21194)을 판정한 결과다. 점수는 논문의 결론이 맞을 확률이 아니라, "제목과 초록이 이 주제를 다루는가"에 대한 답이 "예"일 확률이다. 0.97은 "많이 다룬다"가 아니라 "다룬다고 거의 확신한다"는 뜻이다. 정도를 재고 싶으면 아래의 Score를 쓴다.

응답의 `answers`에는 질문 키마다 확률 하나가 온다. SDK에서는 이 값을 `result.nouls[키]`로 꺼낸다. 다섯 질문의 결과를 풀어 쓰면 아래 표와 같다.

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

같은 입력을 몇 번 다시 보내 보니 값이 0.02~0.04쯤 달라졌다. 기준값 바로 근처의 글은 호출마다 목록에 들어가거나 빠질 수 있다.

질문을 넓게 쓰면 관심 밖의 글도 그 질문에는 맞으므로 높은 점수를 받는다. 표의 두 번째 질문은 처음에 "사람이 통제권을 유지하는 의사결정 지원을 다루는가"였는데, 계약서의 모순을 찾아 주는 분석 도구 논문이 0.96으로 올라왔다. 지금처럼 "사람의 사고가 유지되거나 길러지는가"로 좁히자 같은 논문이 0.40으로 내려갔다.

### Choice: 노트 주제 분류

내 노트와 블로그 글에는 조직, 커리어, AI처럼 직접 정한 주제 8개 가운데 하나를 붙여 둔다. 노트의 제목, 요약문, 본문 앞부분을 보내고 Choice로 하나를 고르게 했다.

```python
from typesafe_sdk import Choice

result = client.system_one(
    {"title": title, "summary": summary, "body_excerpt": body[:2000]},
    {"topic": Choice(
        instructions="Which topic is this note's main claim about? "
                     "Judge by what the note argues, not by words it merely mentions.",
        criteria={
            "조직": "Organizations: delegation, hiring, team performance, leadership.",
            "커리어": "Career and self-development: growth, skills, motivation, job changes.",
            # ... AI, 개발, 심리, 철학, 글쓰기, 지식관리
            "none_of_the_above": "The note fits none of the topics above.",
        },
    )},
)
answer = result.choices["topic"]
print(answer.choice, answer.confidence)
```

응답에는 고른 선택지와 확신도, 모든 선택지의 확률이 함께 온다. 아래는 [[보리스 체르니의 다섯 아키타입으로 본 나의 작업 방식]] 노트의 응답이다.

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

[Confidence 문서](https://docs.typesafe.ai/confidence)에 따르면 확신도는 확률 분포에서 계산한 값으로, 확률이 한 선택지에 몰릴수록 높고 고르게 퍼질수록 낮다. 계산식은 공개하지 않았고 이 응답처럼 가장 높은 확률(0.51)과 확신도(0.44)가 다를 수 있다. 이 노트에 내가 붙인 분류는 `커리어`였고 Jev는 개발과 커리어 사이에서 갈렸다.

노트 74개 중 38개는 확신도가 1.0이었고 나머지는 이 노트처럼 확률이 여러 선택지로 나뉘었다. 결과는 확신도에 따라 다르게 썼다. 확신도가 높은데 내 분류와 다른 노트는 다시 읽었다. 상황적 리더십을 다룬 [[SLII 01 - 상황에 따른 맞춤형 리더십|블로그 글]]은 `조직`이 확신도 1.0으로 나왔는데, 나는 `커리어`를 붙여 두었다. 다시 읽어 보니 리더십을 다루는 글이라 태그를 `조직`으로 바꿨다. 다만 Jev도 [[AI 시대의 판단력은 맥락을 실행 기준으로 바꾸는 능력이다]]처럼 제목에 들어간 단어에 끌려 `AI`를 고르곤 해서 태그는 다시 읽은 뒤에만 바꿨다. 확신도가 낮은 노트는 두 주제에 걸친 경우가 많아서 Jev의 답을 쓰지 않고 내가 판단했다.

주제 8개가 모든 노트를 덮지 못할 수 있어서 "해당 없음"(`none_of_the_above`)을 선택지에 넣었다. 맞는 답이 없어도 Jev는 주어진 선택지 중 하나를 고르기 때문이다. 공식 문서도 목록이 모든 입력을 덮지 못할 수 있으면 이런 선택지를 넣으라고 권한다. 정답이 "알 수 없음"인 문항에서 그 선택지를 빼자, 고정관념에 맞는 답을 다섯 번 중 네 번 확신도 0.79로 고른 측정도 있다.[^ko-audit] 선택지 이름과 설명은 모델에 그대로 전달되므로, [Choice 문서](https://docs.typesafe.ai/primitives/choice)의 권장대로 선택지끼리 구분되게 쓴다.

### Score: 실행 방법의 구체성

읽을거리마다 개발자가 적용할 만한 내용을 얼마나 구체적으로 제시하는지를 의견·발견·실행 방법의 세 단계로 나눠 봤다. 선택지에 순서가 있으면 Choice 대신 Score를 쓴다. 단계는 직접 정해 낮은 것부터 순서대로 주고 응답에서는 0부터 번호가 붙는다.

```python
from typesafe_sdk import Score

apply = Score(
    instructions="How directly can a working software developer apply what this article offers to their own work?",
    criteria=[  # 낮은 단계부터 순서대로
        "Opinion or news: views, reports, or commentary with no method or finding to act on.",
        "Findings or principles: evidence or ideas a developer would still need to adapt before applying.",
        "Ready-to-use method: concrete steps, code, settings, or a tool a developer can apply right away.",
    ],
)
answer = client.system_one({"title": title, "text": text[:6000]}, {"apply": apply}).scores["apply"]
print(answer.score, answer.confidence)
```

최근 읽을거리 다섯 편의 결과다. 세 단계의 차이가 잘 드러나 이 기준을 예시로 골랐다. 점수는 위에 정의한 기준에 따른 결과일 뿐, 글의 가치나 읽을 우선순위를 뜻하지 않는다.

| 글 | 점수 (0~2), 확신도 |
| --- | --- |
| ["rogue" AI 에이전트는 없다](https://eoinhiggins.substack.com/p/there-are-no-rogue-ai-agents) (의견 글) | 0.14, 0.79 |
| [AI 없이 한 달](https://blog.bustikiller.com/2026/09/25/one-month-without-ai.html) (개발자의 체험기) | 0.57, 0.34 |
| [ChatGPT를 쓴 학생의 인지 실험](https://arxiv.org/abs/2609.21194) (논문) | 0.93, 0.90 |
| [Unblocked의 Jev 운영 비교](https://getunblocked.com/blog/jev-in-production-vs-cross-encoder/) (운영 사례) | 1.02, 0.97 |
| [jevgrep](https://github.com/dzhng/jevgrep) (설치해 쓰는 도구) | 2.00, 1.00 |

「AI 없이 한 달」의 응답이다. `legend`는 요청에 넣은 단계 설명을 번호와 함께 돌려준다.

```json
"apply": {
  "type": "score",
  "score": 0.57,
  "confidence": 0.34,
  "legend": {"0": "Opinion or news: ...", "1": "Findings or principles: ...", "2": "Ready-to-use method: ..."},
  "probabilities": {"0": 0.44, "1": 0.56, "2": 0.0}
}
```

점수는 단계별 확률의 가중평균이라 단계 사이의 값이 나온다. 표시된 확률로 다시 계산하면 0.56인데 점수는 0.57이다. 응답 값이 모두 소수 둘째 자리까지라 반올림 차이로 보인다. 확신도는 확률이 한 단계에 몰릴수록 높고 여러 단계에 퍼질수록 낮다. 이 글은 확률이 0단계와 1단계로 나뉘어 확신도가 0.34에 그쳤다. 모델이 두 단계를 명확히 구분하지 못한 글은 점수만 보고 거르지 말고 직접 열어 보는 편이 낫다.

## 적용 범위와 한계

판단 기준이 **입력 안에 적혀 있을 때**는 잘했다. 초록이 어떤 주제를 다루는지, 글이 바로 따라 할 방법을 주는지는 입력만 읽으면 확인할 수 있다. 입력 밖을 추론해야 하는 판단은 약했다. 블로그에서 "X가 아니라 Y"로 쓴 문장을 뽑아 X가 Y를 돋보이게 하려고 일부러 약하게 세운 주장인지 세 선택지의 Choice로 고르게 했을 때, 40문장 중 정답을 "그렇다"로 붙인 18개에서 1개만 맞혔다.[^labels] 글의 문장이 내 주장과 어떤 관계인지 네 선택지(반대 결과, 조건·경계, 구체 사례, 같은 말)로 물었을 때는 대부분 "구체 사례"를 골랐다. 공식 [jev-1.13 약점 문서](https://docs.typesafe.ai/model-jaggedness/jev-1.13)도 여러 단계를 거치는 추론을 약점으로 꼽는다.

쓸모는 정확도보다 양에서 갈렸다. 한 주 치 논문과 글 1,600여 건은 직접 읽거나 LLM에 모두 넘기기에는 많은데, Jev에는 제목과 초록만 보내 1분이 안 걸려 5센트쯤으로 후보를 좁혔다. 반대로 블로그 글의 주장에 근거로 붙일 내 경험 문단을 노트에서 고르게 했을 때는 판단이 정확했지만 글을 함께 쓰는 LLM이 이미 하던 일이라 달라지는 것이 없었다. 어느 쪽이든 Jev의 답은 사람이 다시 볼 후보로만 쓰고 노트에 자동으로 반영하지 않았다.

한국어 입력에 따른 차이는 따로 재지 않았다. 독립 측정에서는 일반 지식 문항(MMLU-ProX)의 한국어 정확도가 영어보다 6.5%p 낮았다.[^ko-audit] 공개된 지 얼마 안 된 모델이라 제3자 검증도 아직 적다. 한 사회과학 분류 연구에서는 과제 15개 중 14개에서 가장 좋은 LLM보다 정확도가 낮았고 비용은 44분의 1이었다.[^css-study]

[^schema]: TypeSafe, [SDE cascade](https://docs.typesafe.ai/cookbooks/sde_cascade), 공식 쿡북. 작은 LLM이 JSON 스키마를 통과한 추출 결과에 원문에 없는 날짜를 지어 넣은 사례를 보이고, 스키마 검사로는 이를 잡을 수 없다고 설명한다.
[^labels]: 이 판단의 정답은 Jev를 돌리기 전에 글쓰기에 함께 쓰는 LLM(Claude)이 붙였다. 그래서 수치는 사람의 판단이 아니라 이 정답과의 일치다. 판단마다 한 번씩만 돌렸다.
[^ko-audit]: [jev-calibration-audit FINDINGS](https://github.com/jujumilk3/jev-calibration-audit/blob/main/FINDINGS.md), jujumilk3, GitHub, 2026-09-18. 한국어 편향 벤치마크(KoBBQ)로 측정했다.
[^css-study]: Hazem Ibrahim, Yasir Zaki, [Evaluating Decision Models for Text Annotation in Computational Social Science](https://arxiv.org/abs/2609.24574), arXiv, 2026.
