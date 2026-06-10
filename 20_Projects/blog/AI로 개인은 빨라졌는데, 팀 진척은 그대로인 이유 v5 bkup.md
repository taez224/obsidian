---
title: AI로 개인은 빨라졌는데, 팀 진척은 그대로인 이유
created: 2026-06-01
tags:
  - blog
  - AI
  - 개발/도구
  - 소프트웨어공학
status: draft
author: TaeZ
summary: 개인의 AI 활용은 자동으로 팀의 역량이 되지 않습니다. 개인이 빨라진 만큼 팀에 설명, 검증, 판단, 기록이 남아야 합니다. 이 글은 그 변환을 '회수'라고 부르고, 워크플로는 개인화하되 하네스의 경계는 표준화해야 한다는 관점으로 AI 활용 격차를 다룹니다.
related:
  - "[[개인의 AI 활용을 팀의 역량으로 바꾸려면]]"
  - "[[AI 활용 격차 — 2026 Q2 다학제 리서치]]"
  - "[[60일간의 AI 에이전틱 워크플로]]"
  - "[[AI 시대 플랫폼팀은 어떻게 진화하는가]]"
---

## 개인은 빨라졌는데, 왜 팀은 그대로일까

PR 리뷰에서 이런 장면을 자주 보게 됩니다. 변경량은 많고 설명도 붙어 있습니다. 테스트 결과도 있고, 요약도 제법 정리돼 있습니다. 그런데 리뷰어가 "왜 이 방식으로 나눴어요?"라고 묻는 순간 대화가 멈춥니다. 작성자는 코드가 무엇을 하는지는 설명하지만, 그 판단을 자기 말로 방어하지 못합니다.

이때 리뷰어가 검토하는 것은 더 이상 코드만이 아닙니다. 작성자가 AI와 나눈 대화의 빈칸, 선택되지 않은 대안, 확인했는지 알 수 없는 예외까지 함께 떠안게 됩니다. PR 본문에는 설명이 있지만, 팀이 믿고 이어받을 수 있는 판단의 흔적은 부족합니다. 그래서 리뷰는 결함을 찾는 과정이 아니라, 소화되지 않은 맥락을 다시 캐내는 과정이 됩니다.

저도 한동안은 개인의 작업 흐름을 잘 만들면 팀도 자연스럽게 빨라질 거라고 생각했습니다. [[60일간의 AI 에이전틱 워크플로]]를 만들 때도 요구사항 정의부터 구현, 리뷰, PR까지의 흐름을 촘촘히 잡는 데 집중했습니다. 실제로 개인의 속도는 빨라졌습니다. 문제는 그 속도가 팀의 진척으로 곧장 옮겨가지 않는다는 데 있었습니다.

병목은 코드 생성이 아니라, 생성된 결과가 팀 안으로 들어오는 지점에 있었습니다. 작성 비용이 낮아졌다고 해서 변경을 이해하고, 검증하고, 운영 중 책임지는 비용까지 같이 낮아지는 것은 아닙니다. 누군가 빠르게 만든 산출물이 팀의 자산이 되려면 설명, 검증, 기록의 형태로 바뀌어야 합니다. 이 변환이 일어나지 않으면 아낀 시간은 리뷰어의 해석 비용으로 되돌아옵니다.

이 글에서 저는 이 변환을 **흡수**라고 부르려 합니다. AI 산출물을 팀이 이어받을 수 있는 판단의 형태로 바꾸는 일입니다. 흡수가 끊기면 작성자는 빠르게 제출하지만, 팀은 매번 "무엇을 믿어도 되는가"를 다시 확인해야 합니다.

## 이득이 새는 과정

개인이 얻은 이득은 보통 한 번에 사라지지 않습니다. 팀의 자산으로 흡수되기 전에 몇 단계를 거치며 조금씩 샙니다.

### 1. 전이 실패: 산출과 검증의 속도 불일치

코드의 양(LOC)이 늘었다고 그게 곧 팀의 진척은 아닙니다. 초안을 팀이 이어받을 수 있는 형태로 바꾸려면 별도의 비용이 듭니다. AI가 생성의 장벽을 낮춰 아낀 시간의 상당 부분은 그 출력을 검토하고 검증하는 비용으로 다시 빠져나갑니다. 

Faros의 텔레메트리 리포트를 보면 PR 생성량은 늘었지만 PR 하나의 크기와 리뷰 시간이 함께 부풀었고, 정작 조직 수준의 DORA 지표 개선은 뚜렷하지 않았습니다. 작성 속도가 '리뷰하고 배포할 수 있는 변경'으로 전이되지 않으면 산출물은 자산이 아니라 병목이 됩니다.

### 2. 맥락의 고립: 개인의 머릿속에만 머무는 지식

같은 도구를 써도 이득의 크기는 사람마다 다릅니다. 숙련된 엔지니어는 이미 축적된 도메인 지식과 경험이 있기에 AI를 날카롭게 통제하며 고품질의 산출물을 솎아냅니다. 

문제는 이 과정에서 발생한 **'엔지니어의 진짜 판단 과정과 노하우(Context)'가 개인의 머릿속 블랙박스에만 갇혀 있다는 점**입니다. 팀 차원에서 이 Context를 공유 자산으로 흡수하는 시스템이 없다면, 시니어 개발자 혼자만 빨라질 뿐 팀 전체의 역량으로는 이어지지 못합니다.

### 3. 흡수 실패: 조직적 소화 불량

정보가 단순히 내부 저장소에 누적된다고 해서 조직의 자산이 되지는 않습니다. 경영학에는 외부 지식의 가치를 식별하고, 이를 내부 지식 체계로 소화하여 실제 업무에 활용하는 능력을 '흡수 역량'이라 부릅니다. 

AI가 내놓은 코드는 팀의 관점에서 볼 때 '외부에서 유입된 지식'에 가깝습니다. 작성자는 내부 구성원이지만, 판단 근거가 개인의 AI 대화창 안에서 만들어지고 팀의 공유 기억으로 넘어오지 않으면 코드가 저장소에 머지되고 빌드가 통과했다고 해서 팀이 그것을 완전히 흡수한 것은 아닙니다. 팀 내부에 그 결과를 해석할 수 있는 사전 지식과 검증할 명확한 기준이 부재하다면 그것은 자산이 아니라 부채입니다.

**이 과정들의 공통점은 하나입니다. '흡수'가 끊긴다는 것입니다.** 그리고 흡수되지 못한 채 비용은 사라지지 않고, 이자가 붙어 결국 팀 전체에 청구됩니다.

물론 설명이 부족한 PR이나 맥락 없는 문서는 AI 이전에도 있었습니다. 하지만 AI 산출물은 코드와 설명, 테스트까지 그럴듯한 한 묶음으로 들어오기 때문에 문제를 더 늦게 드러냅니다. 예전의 단순 복붙은 어딘가 삐걱거리며 한 번 더 생각할 마찰을 남겼지만, 지금은 그 마찰이 줄어든 만큼 검증 비용이 조용히 다음 사람에게 전가됩니다.

## 이해 부채와 워크슬롭

흡수되지 못한 상태가 팀에 누적되면 먼저 **이해 부채(Comprehension Debt)**가 쌓입니다. 코드베이스가 요구하는 도메인 복잡도와, 팀이 집단으로 공유하고 있는 실제 이해도 사이의 격차를 뜻합니다. 

코드는 저장소에 가득 차는데 "이 시스템이 어디로 가야 하는가"에 대한 팀의 멘탈 모델은 오히려 비어갑니다. 각자 자기 대화창에서 AI와만 이야기하다 보니, 동료가 짠 코드의 진짜 맥락을 아무도 모르는 상태에 가까워집니다. 이런 팀은 장애가 터지면 원인 경계를 좁히지 못해 우왕좌왕하고, 코드 리뷰에서도 맥락을 몰라 겉도는 형식적인 질문만 반복합니다.

여기서 이해 부채와 워크슬롭은 같은 말이 아닙니다. 이해 부채는 팀 안에 쌓이는 지식 격차이고, 워크슬롭은 그 격차가 협업의 표면에서 다음 사람에게 전가되는 형태입니다. 누군가 충분히 소화하지 않은 AI 산출물은 다음 사람에게 해석, 검증, 재작업을 요구합니다. HBR이 말한 **워크슬롭(Workslop)**은 이 비용 전가가 드러나는 대표적인 형태입니다. 겉보기엔 그럴듯하지만 실제 과업을 진전시키지 못하고, 받는 사람에게 해석과 재작업의 몫을 넘기는 산출물입니다.

AI가 만든 산출물은 팀 안으로 들어오는 순간 자동으로 자산이 되지 않습니다. 말하자면 통관 비용이 붙습니다. 설명하고, 검증하고, 기록하는 과정을 거치면 팀의 지식이 되지만, 그 과정을 건너뛰면 그럴듯한 산출물은 곧바로 다음 사람의 세금이 됩니다.

하지만 이걸 개개인의 게으름으로 치부해서는 안 됩니다. 시스템과 프로토콜의 빈자리에 가깝고, 그래서 설계로 해결할 수 있습니다. 결국 부채와 워크슬롭은 AI나 사람 자체의 문제가 아닙니다. 흡수를 보장할 명확한 경계가 설계되지 않은, 팀 시스템의 빈자리가 만든 결과입니다. 그렇다면 다음 질문은 명확해집니다. 그 경계를 어떻게 세울 것인가.

## 나는 한때 워크플로 전체를 규격화하려 했다

경계를 어떻게 세울지 추상적인 처방을 던지기 전에, 제 실패담부터 꺼내겠습니다.

[[60일간의 AI 에이전틱 워크플로]]에서 저는 요구사항 정의부터 구현, 리뷰, 머지까지 전 과정을 촘촘한 커맨드로 규격화했습니다. `/refine-requirement`로 요구사항을 인터뷰하고, `/implement-task`로 구현하고, `/review-implement`로 리뷰하는 식의 파이프라인이었죠. 작은 팀에서는 제법 잘 굴러갔고, 그래서 더 위험했습니다. 저는 한동안 "좋은 흐름을 만들었으니 이 흐름을 넓히면 되겠다"고 착각했습니다.

그런데 거기서 부작용이 보였습니다. 어떤 개발자는 탐색적으로 코드를 만지며 문제를 푸는 게 더 빠른데, 정해진 커맨드 순서를 강제하니 자기 방식이 막혀 답답해했습니다. 어떤 팀은 자기 도메인에 안 맞는 리뷰 단계를 의무로 끼워 넣자 그냥 형식적으로 통과시켜 버렸습니다. 규격이 흡수를 보장한 게 아니라, 오히려 새로운 누수를 만든 겁니다. 그때 저는 AI를 조련하겠다며 규칙을 쌓아 올릴수록, 정작 더 엄격하게 훈련되고 있던 건 우리 팀의 일하는 방식이라는 걸 깨달았습니다. 그 순간부터 프로세스는 안전장치가 아니라 규제가 됩니다.

여기서 제가 끌어낸 원칙은 이렇습니다. **표준화할 것은 워크플로가 아니라 하네스다.** 개발자가 어떤 도구를 쓰고 어떤 경로로 문제를 풀지는 개인의 자유로 두되, 팀의 메인 저장소에 코드가 들어오기 직전의 경계만 똑같이 통과시키는 방식입니다. 작업 경로는 강제하지 않습니다. 대신 머지 직전에 남겨야 할 증거는 강제합니다. 워크플로는 개인화하고, 하네스의 경계는 표준화한다. 60일을 되짚어 도달한 결론입니다.

이 경계는 두 가지로 이루어집니다.

- **기본 경로:** 좋은 입력과 올바른 판단을 자연스럽게 유도하는 템플릿과 환경. 가장 안전한 길을 가장 쉬운 길로 만들어 줍니다. 과거 [[AI 시대 플랫폼팀은 어떻게 진화하는가]]에서 다룬 플랫폼 원칙의 AI 버전입니다. 강제로 한 길만 걷게 하는 게 아니라, 안전한 길을 선택하기 쉽게 만드는 일입니다.
- **책임 경계:** AI 산출물이 팀의 결과물이 되기 직전, 사람이 반드시 개입해 설명·검증·기록을 붙잡는 차단벽.

이 경계를 통과하려면 세 가지가 남아야 합니다. 설명은 "AI가 어떤 판단을 했는가"를 드러내야 하고, 검증은 "사람이 무엇을 확인했는가"를 보여줘야 하며, 기록은 "다음 사람이 어디서 이어받으면 되는가"를 남겨야 합니다. 필요한 것은 더 그럴듯한 설명이 아니라, 판단이 실제로 일어난 증거입니다. 셋 중 하나라도 비어 있으면 리뷰어가 멈출 수 있어야 합니다.

![워크플로는 개인화하고(각자의 경로), 팀 레포 직전의 승인 경계만 설명·검증·기록으로 표준화한다](assets/ai-team-recovery-approval-boundary.png)

하네스의 경계는 규제보다 안전벨트에 가깝습니다. 무엇을 타고 어디로 갈지는 자유지만, 출발 전 벨트 한 번은 모두가 똑같이 맵니다. 개발자가 어떤 AI 도구를 쓰고 프롬프트를 어떻게 조합하든 상관없습니다. 다만 코드가 팀에 반영되기 전에는 '설명·검증·기록'이라는 같은 관문을 통과해야 합니다.

물론 이 경계를 유지하는 데도 인지적 비용이 듭니다. 앞서 짚었듯 아낀 시간의 일부는 검증 비용으로 되돌아옵니다. 그럼에도 감수할 만한 이유는, 흡수하지 못했을 때 팀이 치를 대가가 그보다 훨씬 크기 때문입니다.

## 하네스는 얇게, 스킬은 두껍게

이 비대칭을 설명하는 데 빌려올 만한 표현이 하나 있습니다. 2026년 4월 Garry Tan의 글을 계기로 널리 회자된 "Thin Harness, Fat Skills" — 하네스는 얇게, 스킬은 두껍게입니다. 원래 맥락에서는 모델을 돌리는 실행 루프는 가볍게 두고, 판단 절차와 도메인 지식은 마크다운 스킬에 두껍게 쌓자는 뜻에 가깝습니다.

다만 이 표현을 정설처럼 가져오고 싶지는 않습니다. 하네스를 얼마나 얇게 둘지, 센서와 검증을 얼마나 촘촘히 둘지는 아직 사람마다 다르게 말합니다. 여기서 말하는 '얇게/두껍게'는 제가 60일을 통과하며 고른 관점에 가깝습니다. 참고로 원어는 'Thick'이 아니라 'Fat Skills'인데, 한국어로 옮길 때 어감 때문에 저는 '두꺼운'으로 부르고 있습니다.

이걸 팀에 대입하면 두 축이 됩니다.

- **절차적 규제는 얇게.** 구성원의 일하는 방식을 사사건건 묶는 절차는 줄이고, 머지 직전의 공통 관문(설명·검증·기록)만 선명하게 남깁니다.
- **개인과 팀의 역량은 두껍게.** 대신 각자가 AI를 다루는 역량, 도메인 맥락을 나누는 노하우, 팀 내부의 모범 사례는 조직 차원에서 적극적으로 공유되고 두텁게 쌓이도록 지원합니다.

앞서 말한 기본 경로와 책임 경계가 바로 이 글에서 말하는 '얇은 하네스'의 구체적인 구현입니다. 얇지만 선명한 두 개의 고정점, 그게 골든 패스와 승인 경계인 셈입니다.

그렇다면 이 얇은 하네스는 현장에서 어떻게 작동할까요? 제 경험상 흡수는 두 곳에서 갈립니다. 먼저 **문화**입니다. LOC나 PR 수 같은 숫자로만 압박하는 단기 지표를 걷어내야, 실무자가 "이 작업은 AI 초안 기반이니 이 부분의 논리적 맹점을 함께 봐달라"고 솔직하게 말할 안전감이 생깁니다. 다음은 **관행**입니다. 기능이 작동하는지, 산출물이 얼마나 나왔는지만 보던 데서 멈추지 말고, 코드 이면에 해석과 예외 검증이 실려 있는지를 머지 직전에 서로 확인하는 일입니다. 앞서 말한 설명·검증·기록을 PR 관문에 녹이는 게 그 출발점입니다.

그리고 이 둘을 떠받치는 책임이 필요합니다. 누수가 어디서 일어나는지 관찰하고, 골든 패스와 승인 경계를 계속 고치는 일입니다. 새 플러그인을 깔고 토큰 사용량을 들여다보는 관리가 아니라, 기술의 언어와 협업의 역동을 함께 읽는 일에 가깝습니다. 테크 리더나 시니어가 리뷰 병목과 컨텍스트 파편화가 생기는 길목을 짚어, 팀원이 AI를 보여주기식이 아니라 실질적인 무기로 쓰도록 길을 깔아 줘야 합니다.

## 평준화의 함정

좋은 AI 도구가 보급되면서, 얼핏 조직 전반의 생산성이 상향 평준화되는 것처럼 보이는 착시가 생깁니다. 주니어도 매끄러운 보고서를 쓰고 복잡한 코드를 순식간에 만들어 냅니다.

하지만 낮아진 것은 역량이 아니라 초안의 진입장벽입니다. 문제는 그다음입니다. 매끄러운 초안이 많아질수록, 팀 안에서는 검증할 줄 아는 사람에게 더 많은 부담이 몰립니다. 흡수 시스템이 없는 팀에서는 초안이 늘수록 병목도 같이 늘고, 그걸 팀의 자산으로 바꿀 수 있는 팀과 그러지 못하는 팀 사이의 거리는 더 벌어집니다.

## 흡수하는 팀, 흘려보내는 팀

결국 이 글의 한 문장은 이겁니다. AI는 강점만 키우지 않습니다. 약점과 허점도 함께 키웁니다. 그 둘을 가르는 건, 개인이 AI로 만든 산출물을 팀이 흡수할 수 있는 경계가 있느냐입니다. 작성 비용이 낮아질수록 오히려 희소해지는 것은 책임질 수 있는 판단입니다.

그러니 질문을 바꿔야 합니다. "우리 팀은 AI를 얼마나 많이 쓰는가"는 이제 좋은 질문이 아닙니다. 진짜 질문은 여기에 가깝습니다. **"우리 팀은 AI의 산출물을 인간의 판단을 거쳐 팀 지식으로 흡수할 단단한 경계를 갖고 있는가?"**

저는 이 질문을 거창한 제도로 시작하지 않으려 합니다. 지금은 PR에 한 줄을 더 추가하는 것보다, 리뷰에서 한 번 멈출 기준을 합의하는 쪽이 더 중요하다고 봅니다. **"AI가 만든 판단은 무엇이고, 사람은 무엇을 확인했으며, 다음 사람은 어디서 이어받으면 되는가?"** 이 세 가지가 남지 않는 변경은 아직 팀에 흡수된 변경이 아닙니다.


---

## 참고 문헌

본문에서 직접 인용한 자료와, 논지를 보강하는 추가 참고 자료를 함께 모았습니다.

**개인 이득과 그 한계**
- Daniotti, Wachs, Feng, Neffke, ["Who is using AI to code? Global diffusion and impact of generative AI"](https://www.science.org/doi/10.1126/science.adz9311) (Science, 2026‑01) — 이득이 숙련자에 집중, 격차 확대
- ["DORA Report 2025"](https://dora.dev/research/2025/dora-report/) (Google Cloud, 2025‑09) — "AI는 증폭기"
- DORA, ["Balancing AI tensions: Moving from AI adoption to effective SDLC use"](https://dora.dev/insights/balancing-ai-tensions/) (2026‑03) — 검증 비용, 리뷰 부담, production readiness gap
- Faros AI Research, ["The AI Productivity Paradox Report 2025"](https://www.faros.ai/blog/ai-software-engineering) (2025‑07, 벤더 텔레메트리 리포트) — 개인 산출 증가와 리뷰 병목

**변환·흡수·자산화**
- Cohen & Levinthal, ["Absorptive Capacity: A New Perspective on Learning and Innovation"](https://doi.org/10.2307/2393553) (Administrative Science Quarterly, 1990) — 흡수역량
- Pletsch, Tonial, Matos, Koch, ["Digital transformation: The role of generative AI in the evolution of knowledge management systems"](https://doi.org/10.1108/JKM-09-2025-1398) (Journal of Knowledge Management, 2026‑03) — 흡수역량, 동화 단계의 공백
- Figge, Anderson, Lewis, ["AI-human learning systems: Investigating the strategic role of AI for organizational learning"](https://doi.org/10.1177/14761270251385860) (Strategic Organization, 2026) — 개인·팀·AI 학습 시스템
- Kost, Hærem, Pentland, ["Transactive memory systems and team performance: the mediating role of routines"](https://doi.org/10.1093/icc/dtaf062) (Industrial and Corporate Change, 2026) — 공유 기억과 루틴
- Dellarocas, ["Gen AI Could Fix Performance Reviews—or Make Them Even Worse"](https://hbr.org/2026/05/gen-ai-could-fix-performance-reviews-or-make-them-even-worse) (Harvard Business Review, 2026‑05) — 매끄러운 서술보다 판단의 증거가 중요하다는 관점
- Shen & Tamkin (Anthropic), ["How AI Impacts Skill Formation"](https://arxiv.org/abs/2601.20245) (arXiv, 2026‑01) — 이해 구축형이 위임형보다 숙달
- ["Knowledge Activation: AI Skills as the Institutional Knowledge Primitive"](https://arxiv.org/abs/2603.14805) (arXiv, 2026‑06) — 개인 AI 역량을 공유 가능한 팀 자산으로 코드화·표준화·재사용

**부채와 그 경계**
- Sankaranarayanan, ["Mitigating \"Epistemic Debt\" in Generative AI-Scaffolded Novice Programming using Metacognitive Scripts"](https://arxiv.org/abs/2602.20206) (arXiv, 2026‑02, 프리프린트) — 기능적 결과와 인지적 소유의 괴리
- Ahmad, ["Comprehension Debt in GenAI-Assisted Software Engineering Projects"](https://arxiv.org/abs/2604.13277) (arXiv, 2026‑04) — 팀의 집단 이해도와 코드베이스 요구 수준 사이의 격차
- Riedl, Savage, Zvelebilova, ["Cognitive Spillover in Human-AI Teams"](https://dl.acm.org/doi/10.1145/3805039) (ACM TOCHI, 2026‑04) — 공유 언어와 공유 정신모델의 동질화
- Becker, Rush, Barnes, Rein (METR), ["Measuring the Impact of Early-2025 AI on Experienced Open-Source Developer Productivity"](https://arxiv.org/abs/2507.09089) (arXiv, 2025‑07) — 숙련 개발자 RCT에서 AI 사용 시 20% 빨라졌다고 체감했지만 실제 완료 시간은 19% 증가(단기 과제 속도 측정)
- Jian Wang, ["Cognitive offloading through digital tools and critical thinking"](https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2026.1781101/full) (Frontiers in Psychology, 2026‑03) — 오프로딩과 비판적 사고의 양의 상관
- Matta, ["From Extended to Amplified: The Generative Mind in the Age of LLMs"](https://philarchive.org/rec/MATFET-3) (PhilArchive, 2026‑01, 프리프린트) — '증폭된 마음'(축소 아닌 변형)
- Niederhoffer, Kellerman et al. (BetterUp Labs & Stanford Social Media Lab), ["AI-Generated 'Workslop' Is Destroying Productivity"](https://hbr.org/2025/09/ai-generated-workslop-is-destroying-productivity) (Harvard Business Review, 2025‑09) — 형식만 채운 AI 산출물이 수신자의 재작업 비용과 신뢰 비용을 만든다는 조사
- Niederhoffer, Robichaux, Hancock, ["Why People Create AI 'Workslop'—and How to Stop It"](https://hbr.org/2026/01/why-people-create-ai-workslop-and-how-to-stop-it) (Harvard Business Review, 2026‑01) — 불명확한 AI 지침과 과부하가 보여주기식 AI 사용을 만든다는 후속 분석
- Liu & Kovács, ["Big Tech's Looming Capability Crisis"](https://hbr.org/2026/06/big-techs-looming-capability-crisis) (Harvard Business Review, 2026‑06) — 코드 생산 비용 하락 이후 더 희소해지는 판단·책임·서명

**흡수 메커니즘과 격차**
- Hardman, ["The 'Cognitive Offloading' Paradox"](https://drphilippahardman.substack.com/p/the-cognitive-offloading-paradox) (2026‑04; 원 연구 Wang & Zhang 2026, 912명) — 전략적 오프로딩 해석
- LearnLM Team & Eedi, ["AI tutoring can safely and effectively support students: An RCT in UK classrooms"](https://arxiv.org/abs/2512.23633) (arXiv, 2025‑12, 프리프린트) — 인간‑인‑루프 검토의 우위
- Chowdhury, Banik, Ferdous, Shamim, ["From Industry Claims to Empirical Reality: Code Review Agents in Pull Requests"](https://arxiv.org/abs/2604.03196) (arXiv, 2026‑04) — 머지 전 사람 승인 강제
- Kraishan, ["The AI Attribution Paradox: Transparency as Social Strategy in OSS"](https://arxiv.org/abs/2512.00867) (arXiv, 2025‑11, 프리프린트) — 출처표기는 사회적 신호
- Ni, Wang, Feng et al., ["Generative AI in Action: Field Experiment from Alibaba's Customer Service"](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5012601) (SSRN, 2024‑11) — 균일 배포가 톱 성과자 품질을 떨어뜨림

**하네스와 플랫폼 운영**
- Garry Tan, ["Thin Harness, Fat Skills"](https://x.com/garrytan/status/2042925773300908103) (2026‑04) — 지능은 스킬로 올리고 하네스는 얇게라는 비대칭을 널리 퍼뜨린 글
- Anthropic, ["A harness for every task: dynamic workflows in Claude Code"](https://claude.com/blog/a-harness-for-every-task-dynamic-workflows-in-claude-code) (2026‑06) — 과제별 동적 하네스와 복잡 작업의 검증 구조
- Böckeler, ["Harness engineering for coding agent users"](https://martinfowler.com/articles/harness-engineering.html) (Martin Fowler, 2026‑04) — 가이드와 센서, 인간의 steering loop
- Böckeler & Ford, ["Harness engineering and agent feedback: Exploring AI coding sensors"](https://www.thoughtworks.com/en-us/insights/blog/generative-ai/harness-engineering-agent-feedback-exploring-ai-coding-sensors) (Thoughtworks, 2026‑05) — deterministic sensor와 self-correction loop
- Lopopolo, ["Harness engineering: leveraging Codex in an agent-first world"](https://openai.com/index/harness-engineering/) (OpenAI, 2026‑02) — 짧은 지도, 저장소 지식, 기계적 검증, 중앙 경계와 지역 자율성
- Frontiers in Computer Science, ["Platform engineering and internal developer portals: a multivocal literature review"](https://www.frontiersin.org/journals/computer-science/articles/10.3389/fcomp.2026.1814498/full) (2026‑05) — 표준화와 자율성의 긴장, mandated tooling 저항

## 연결된 노트

- [[60일간의 AI 에이전틱 워크플로]] - AI를 팀 개발 흐름에 넣으며 하네스를 만든 실전 경험입니다.
- [[AI 시대 플랫폼팀은 어떻게 진화하는가]] - AI 시대에 플랫폼팀이 조직의 학습과 전환을 설계해야 한다는 배경 관점입니다.
- [[개인의 AI 활용을 팀의 역량으로 바꾸려면]] - 이 글의 출발점이 된 원문입니다.
- [[AI 활용 격차 — 2026 Q2 다학제 리서치]] - 지지·반례 양쪽 증거를 모은 리서치 문서
- [[AI 활용 격차를 다시 본다 — 반례를 통과한 회수율]] - 같은 재료로 쓴 변증법적 버전
