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

## 개인의 이득은 왜 팀에 쌓이지 않는가

최근 개발 조직의 최대 화두는 단연 생성형 AI를 활용한 생산성 혁신입니다. 누구나 AI 어시스턴트를 켜고 순식간에 수백 줄의 코드를 뽑아내는 시대를 살고 있습니다. 하지만 여기서 기묘한 현상이 발생합니다. 개인이 코드를 짜는 속도는 분명 몇 배나 빨라졌는데, 왜 팀의 최종 배포 속도나 제품의 퀄리티는 그만큼 극적인 스파이크를 보여주지 못할까요?

AI는 개인과 조직의 강점만 키우지 않습니다. 그동안 묻혀 있던 약점과 허점도 함께 키웁니다. 성과는 도구가 아니라, 그 도구가 작동하는 *팀의 시스템*이 정합니다.

우리는 지금 기술이 아니라 '일하는 방식의 시스템적 누수'를 점검해야 하는 시점에 와 있습니다.


AI가 개인의 작업 속도를 끌어올린 건 분명합니다. 생성되는 코드와 PR, 문서 생산량도 늘었습니다.  팀의 진척 속도는 별반 달라진게 없어보입니다.

이제 많은 개발 조직에서 AI는 일상 도구가 되었고, 코드와 PR, 문서 생산량도 늘었습니다. 그런데도 왜 팀 전체의 진척은 개인이 빨라진 만큼 따라오지 않을까요?

이 간극은 AI가 효과 없다는 뜻이 아닙니다. 다만 개인이 작업을 빨리 끝내는 것과 팀이 더 빨리 전진하는 일은 다른 문제입니다. 팀의 진척은 작성 속도만으로 움직이지 않습니다. 요구사항을 이해하고, 리뷰하고, 테스트를 믿고, 배포를 판단하고, 운영을 책임지는 일이 함께 맞물려야 빨라집니다.

물론 맥락 없는 PR이나 부실한 코드 리뷰는 AI 이전에도 있었습니다. 달라진 것은 **문제가 확산되는 속도**입니다. 코드 작성 속도가 빨라진 만큼, 제대로 이해하지 못한 변경과 검증되지 않은 판단 역시 더 빠르게 팀의 코드베이스로 들어옵니다.

---

## 개인의 이득은 왜 팀에 고이지 않는가

개인이 도구로부터 얻은 이득이 팀의 자산으로 연결되지 못하고 중간에 새어버리는 길목은 크게 세 곳입니다.

#### 1. 전이 실패: 산출과 검증의 속도 불일치

코드의 양(LOC)이 늘어났다고 그게 곧 팀의 진척을 의미하진 않습니다. 초안을 팀이 이어받을 수 있는 형태로 만드는 데는 별도의 비용이 듭니다.

AI가 초기 작업 시작의 진입장벽을 낮춰준 만큼, 절약한 시간의 상당 부분은 AI 출력의 검토와 검증 비용으로 다시 지출됩니다. 개발 생산성 분석 업체 Faros의 리포트에 따르면, PR과 task 생성량은 늘었지만, PR 하나의 크기는 154%, 리뷰 시간은 91% 커졌고 정작 조직 수준의 DORA 지표 개선은 뚜렷하지 않았습니다. 개인의 작성 속도가 곧바로 '리뷰하고 배포할 수 있는 변경'으로 전이되지 않으면, 산출물이 아무리 늘어도 팀의 역량으로 쌓이지 않고 병목만 만들 뿐입니다.

#### 2. 맥락의 고립 : 개인의 머릿속에만 머무는 지식

같은 도구를 쓰더라도 이득을 가져가는 정도는 사람마다 다릅니다. 숙련된 엔지니어는 이미 축적된 도메인 지식과 경험(Context)이 있기에 AI를 날카롭게 통제하며 고품질의 산출물을 솎아냅니다. 

문제는 이 과정에서 발생한 **'엔지니어의 진짜 판단 과정과 노하우'가 개인의 머릿속 블랙박스에만 갇혀 있다는 점**입니다. 팀 차원에서 이 지식을 공유 자산으로 회수(Transfer)하는 시스템이 없다면, 시니어 개발자 혼자만 빨라질 뿐 팀 전체의 역량 상향 평준화로는 이어지지 못하고 지식이 파편화되어 고립됩니다.

#### 3. 흡수 실패: 조직적 소화 불량

외부에서 들어온 정보가 단순히 저장소에 누적된다고 해서 조직의 자산이 되지는 않습니다. 경영학에는 외부 지식의 가치를 식별하고, 이를 내부 지식 체계로 소화하여 실제 업무에 활용하는 능력을 '흡수 역량'이라 부릅니다. 

AI가 뱉어낸 코드는 팀의 관점에서 볼 때 '외부에서 유입된 지식'에 가깝습니다. 코드가 저장소에 머지되고 빌드가 통과했다고 해서 팀이 그것을 완전히 흡수한 것은 아닙니다. 팀 내부에 그 결과를 해석할 수 있는 사전 지식과 검증할 명확한 기준이 부재하다면 그것은 자산이 아니라 부채입니다.

---

## 이해 부채와 워크슬롭

이렇게 경계에서 지식을 제대로 '회수'하지 않는다면, 그 비용은 사라지지 않고 훨씬 더 무서운 이자가 되어 팀 전체에 청구됩니다.

### 1단계: 팀의 집단 인지를 갉아먹는 '이해 부채'

개인의 미회수 상태가 팀 안에 누적될 때, 이를 **'이해 부채(Comprehension Debt)'**라고 부릅니다. 이는 코드베이스가 요구하는 도메인의 복잡도와, 팀이 집단적으로 보유한 실제 이해도 사이의 격차를 뜻합니다. 

AI 덕분에 코드는 저장소에 가득 쌓이지만, 정작 **"이 시스템이 궁극적으로 어떤 구조와 방향으로 가야 하는가"에 대한 팀의 '공유 정신모델(Shared Mental Model)'은 텅 비어가는 기이한 현상**이 발생합니다. 각자가 자기 대화창 안에서 AI와만 소통하다 보니, 동료가 짠 코드의 진짜 맥락을 아무도 모르는 지경에 이릅니다.

공유 정신모델이 무너진 팀은 장애가 터졌을 때 원인의 경계를 좁히지 못해 우왕좌왕하고, 코드 리뷰는 맥락을 몰라 겉핥기식 질문만 맴돕니다. 부채가 임계점을 넘으면 팀은 AI가 제안하는 패턴에 무조건 의존하게 되고, 결국 조직 전체의 기술적 시야 자체가 AI의 틀 안으로 좁아지게 됩니다.

### 2단계: 신뢰를 파괴하는 진흙탕, '워크슬롭(Workslop)'

이해 부채로 인해 팀원들이 인지적 고갈 상태에 빠지면, 조직은 마침내 **'워크슬롭(Workslop)'**의 범람을 마주하게 됩니다.

> **워크슬롭(Workslop):** 겉보기에는 그럴싸하고 세련되어 보이지만, 실제로는 알맹이가 없어 받는 사람에게 인지적 노동과 검증의 책임을 떠넘기는 '낮은 노력의 AI 생성물'.

하버드 비즈니스 리뷰(HBR)의 조사에 따르면 직장인의 **41%가 동료가 보낸 워크슬롭 때문에 업무에 직접적인 피해**를 입었고, 놀랍게도 **절반이 넘는 53%는 자신도 은밀히 워크슬롭을 보낸 적이 있다**고 고백했습니다.

워크슬롭이 정말 치명적인 이유는 단순한 품질 저하 때문이 아닙니다. **팀원 간의 신뢰 기반을 흔들기 때문입니다**.

### 이것은 개인이 아닌 '시스템'의 실패다

워크슬롭을 받아보고 보낸 사람의 무능함이나 게으름을 탓하는 것은 가장 전형적인 '근본적 귀인 오류'입니다. HBR 연구의 핵심은 **워크슬롭의 범람이 개인이 아닌 '시스템의 실패'라는 점을 명확히 짚어냅니다**. 

리더들은 강력한 도구를 무작정 쓰라는 모호한 지시만 내리는 반면, 과중한 업무에 시달리는 팀원들은 불확실함을 인정하거나 도움을 요청할 심리적 안전감을 갖지 못했습니다. 결국 "나도 AI를 쓰고 있다"는 것을 증명하기 위해 **'보여주기식(Performative) AI 사용'**으로 도피한 결과물이 바로 워크슬롭인 것입니다.

반대로 말하면, 해결책 역시 시스템에 있습니다. 연구에 따르면 **팀 내에 "내가 AI를 썼고, 이 부분은 검증이 필요하다"고 솔직하게 털어놓을 수 있는 문화적 신뢰가 구축되었을 때, 워크슬롭은 무려 61%나 감소했습니다**.

결국 부채와 슬롭은 개인이나 AI라는 기술 자체의 문제가 아니라, **'지식을 회수할 경계(Harness)'가 설계되어 있지 않은 팀 시스템의 부재**가 낳은 결과물입니다. 그렇기에 질문은 자연스럽게 '하네스를 어떻게 설계할 것인가'로 넘어갈 수밖에 없습니다.

> 이해 부채와 워크슬롭은 개인의 게으름 때문에 발생하는 것이 아닙니다. AI를 쓰라는 무조건적인 압박은 존재하지만, 어디까지를 사람이 책임져야 하는지 경계가 모호할 때, 업무 과부하에 시달리는 직원들이 '보여주기식(Performative) AI 활용'으로 도피하면서 발생하는 **명백한 시스템과 경영의 실패**입니다.

## 워크플로는 개인화하고, 하네스의 경계는 표준화한다

이해 부채와 워크슬롭을 막기 위해 팀이 도입해야 할 핵심 장치가 바로 **하네스**입니다. 우리가 질문해야 할 것은 "AI에게 일을 얼마나 많이 맡길 것인가"가 아닙니다. "AI가 만든 결과물이 '팀의 자산'으로 편입되기 전, 어디서 최종 책임의 경계를 잡을 것인가"의 문제입니다.

여기서 저의 생각도 과거에 비해 조금 변화했습니다. [[60일간의 AI 에이전틱 워크플로]]에서는 요구사항 정의부터 구현, 리뷰, 머지까지의 모든 흐름을 촘촘한 커맨드와 규칙으로 규격화하려 했습니다. 작은 팀에서는 유효했을 지 몰라도, 이를 전사 조직으로 확장하려 하니 개별 개발자의 자유로운 문제 풀이 방식과 창의성까지 획일화하려는 악효과가 났습니다. 그 순간 프로세스는 안전장치가 아니라 불필요한 '규제'가 되어버립니다.

지금 도달한 결론은 다릅니다. 우리가 표준화해야 할 것은 개발자의 워크플로 전체가 아니라, 팀이 공유할 '기본 경로(Golden Path)'와 최종 '책임 경계(Approval Boundary)'입니다. 
- **기본 경로 (Golden Path):** 좋은 입력과 올바른 판단을 미리 유도하여 안전하게 이동할 수 있는 최적의 템플릿과 환경을 제공하는 것 (과거 [[AI 시대 플랫폼팀은 어떻게 진화하는가]]에서 다룬 플랫폼의 역할과 맞닿아 있습니다).
    
- **책임 경계 (Approval Boundary):** AI 산출물이 팀의 최종 결과물이 되기 직전, 사람이 반드시 개입해 설명·검증·기록 상태를 붙잡는 최종 차단벽.

![워크플로는 개인화하고, 하네스의 경계는 표준화한다](assets/ai-team-recovery-approval-boundary.png)

하네스의 경계는 안전벨트에 가깝습니다. 개발자가 어떤 AI 도구를 쓰고, 프롬프트를 어떻게 조합하며, 어떤 경로로 문제를 해결할지는 온전히 개인의 자유입니다. 하지만 팀의 메인 레포지토리에 코드가 반영되기 전에는 '설명(Why)·검증(Validation)·기록(Context)'이라는 동일한 승인 경계를 반드시 통과해야 합니다.

물론 이러한 회수 경계를 유지하는 것 역시 인지적 비용이 듭니다. 앞서 짚었듯 절약한 시간의 상당 부분이 검증 비용으로 되돌아오니까요. 그럼에도 이 비용을 기꺼이 감수해야 하는 이유는 **회수하지 않았을 때 팀이 치러야 할 대가가 압도적으로 크기 때문**입니다.

최근 실리콘밸리의 AI 아키텍처 방법론을 관통하는 핵심 격언 중 하나가 "하네스는 얇게, 스킬은 두껍게 (Thin Harness, Thick Skills)"입니다. 복잡한 하드코딩이나 과도한 규칙으로 AI 모델을 억압하기보다, 가벼운 실행 엔진(Thin Harness) 위에 개발자의 풍부한 도메인 맥락(Thick Skills)을 유연하게 넘겨주라는 설계 철학입니다.

이를 우리 팀의 일하는 방식에 대입해 보면 아주 명확한 통찰이 됩니다.
 
- **조직의 규제(Thin Harness)는 얇고 가볍게:** 구성원들을 통제하는 절차나 사사건건 감시하는 규칙은 최소한의 안전핀(설명·검증·기록)만 남기고 아주 얇고 명확하게 걷어내야 합니다. 규제가 얇아야 팀의 속도가 죽지 않습니다.
    
- **개인의 역량(Thick Skills)은 두껍고 풍부하게:** 대신 구성원 개개인이 AI를 다루는 역량, 도메인 맥락을 공유하는 노하우, 팀 내부의 모범 사례(Skill)는 조직 차원에서 적극적으로 공유되고 두텁게 축적되도록 지원해야 합니다.


## 평준화의 함정: 누구나 그럴싸한 초안을 만드는 시대의 격차

시장에 좋은 AI 도구가 보급되면서, 얼핏 조직 전반의 생산성이 '상향 평준화'되는 것처럼 보이는 착시가 일어납니다. 주니어도 매끄러운 보고서를 쓰고, 복잡한 코드 생성을 순식간에 해내니까요.

하지만 이것은 역량이 평준화된 것이 아니라 **'초안의 진입 장벽'이 평준화된 것뿐**입니다. 모두가 상향 평준화된 도구의 출력물에만 의존하기 시작할 때, 역설적으로 그 결과물을 검증하고 소화하는 조직의 '회수 시스템'이 부재한 팀은 급격한 **조직적 하향 평준화(워크슬롭화)**를 겪게 됩니다. 

결국 도구가 평준화된 시대에 조직의 진짜 격차는 '누가 더 AI를 많이 쓰느냐'가 아니라, **'누가 AI의 휘발성 산출물에서 인간의 맥락과 엔지니어링 판단을 더 많이 회수해 조직의 고유 자산으로 남기느냐'**에서 결정됩니다.

## 워크슬롭을 멈추는 3가지 시스템적 기둥

그렇다면 '얇은 하네스(Thin Harness)'와 '두꺼운 스킬(Thick Skills)'을 갖춘 조직은 구체적으로 어떻게 작동해야 할까요? 하버드 비즈니스 리뷰(HBR) 연구진은 워크슬롭의 범람을 막고 AI를 진정한 협업 파트너로 안착시키기 위해 시스템이 작동해야 할 **세 가지 핵심 레이어**를 제안합니다.

| **레이어**                    | **리더의 역할 (Top-Down)**                                                   | **실무자의 역할 (Bottom-Up)**                                         |
| -------------------------- | ----------------------------------------------------------------------- | --------------------------------------------------------------- |
| **1. 문화 (Culture)**        | LOC, PR 수 같은 숫자로만 압박하는 단기 지표를 걷어내고, 도구 활용을 투명하게 밝힐 수 있는 **심리적 안전감** 제공. | "이 작업은 AI 초안을 기반으로 작성했으니, 이 부분의 논리적 맹점을 봐달라"고 동료에게 **솔직하게 공유**. |
| **2. 관행 (Practice)**       | 무조건적인 사용 지시 대신, 코드의 설명·검증을 요구하는 **얇은 하네스 프로토콜** 설계.                     | 기계적인 자동화의 유혹에서 벗어나, 머지 직전 **인간의 판단력(Human Judgment)을 기록**으로 남김. |
| **3. 책임 (Accountability)** | 기술과 협업의 역동을 모두 이해하는 시니어/조직을 통해 현장 밀착형 **기본 경로(Golden Path)** 구축 지원.     | 주니어와 시니어 간의 AI 활용 격차를 줄이기 위해, 자신만의 프롬프트 노하우와 도메인 지식을 **팀에 전파**. |

> **protective factor (보호 지표):** 팀원들이 도구 활용을 투명하게 밝히고 피드백을 주고받는 '문화적 신뢰'가 형성되었을 때, 워크슬롭은 무려 **61%나 감소**했습니다. 신뢰는 사사건건 코드를 감시하는 비용을 줄여주는 가장 가성비 좋은 안전망입니다.

### 1. 문화(Culture): 심리적 안전감과 솔직한 공유

과부하에 걸린 팀원들이 AI 사용 사실을 숨기거나, AI가 대충 뱉어낸 코드를 완벽하게 검증한 척 포장해서 넘길 때 워크슬롭이 태어납니다.

리더는 LOC, PR 수 같은  숫자로만 압박하는 단기 지표를 걷어내고, 도구 활용을 투명하게 밝힐 수 있는 **심리적 안전감**을 주어야 하고, 실무자는 "이 작업은 AI 초안을 기반으로 작성했으니, 이 부분의 논리적 맹점을 함께 봐달라"고 솔직하게 동료 리뷰어에게 요청할 수 있어야 합니다. 

> 연구에 따르면, 팀원들이 도구 활용을 투명하게 밝히고 피드백을 주고받는 '문화적 신뢰'가 형성되었을 때, 워크슬롭은 무려 **61%나 감소**했습니다. 신뢰는 통제 비용을 줄여주는 가장 강력한 안전망입니다.

### 2. 관행(Practice): 인간의 판단을 요구하는 승인 프로토콜

아무리 문화가 좋아도 일상적인 코드 리뷰나 공유 방식이 형식적이면 소용이 없습니다. 요구사항 정의나 초안 작성을 AI에게 위임하더라도, 머지(Merge) 직전에는 **인간의 판단력(Human Judgment)을 반드시 개입시키는 명확한 프로세스**가 필요합니다.

- **리더는:** 무조건적인 사용 지시 대신, 코드의 설명과 검증을 요구하는 **얇은 하네스 프로토콜**을 설계해야 합니다.
    
- **실무자는:** 기계적인 자동화의 유혹에서 벗어나, 머지 직전 **인간의 판단력을 기록**으로 남겨야 합니다. 앞서 소개한 '설명(Why)·검증(Validation)·기록(Context)'의 3대 회수 질문을 우리 팀의 PR 하네스 관문에 녹여내는 것이 좋은 출발점입니다.

앞서 소개한 '설명(Why)·검증(Validation)·기록(Context)'의 3대 회수 질문을 개발 라이프사이클에 녹여내야 합니다. 단순한 기능 작동 여부나 양적 산출문만 확인하는 관행을 넘어, AI가 만든 코드 이면에 '인간 작업자의 해석과 예외 조건 검증'이 포함되어 있는지를 서로 확인하는 **'얇은 하네스' 관문**을 팀의 표준 관행으로 삼아야 합니다.  

### 3. 책임(Accountability): 기술과 관계를 잇는 '협업 아키텍처'

우리에게 필요한 것은 단순히 새로운 AI 플러그인을 설치해 주고 토큰 사용량을 모니터링하는 IT 관리자가 아닙니다. 기술의 언어와 인간 협업의 역동을 동시에 이해하는 **'AI 협업 아키텍트(AI Collaboration Architect)'** 관점의 책임이 필요합니다.

테크 리더나 시니어 개발자들은 팀의 업무 흐름을 관찰하며 어디서 지식 누수(리뷰 병목, 컨텍스트 파편화)가 일어나는지 포착하고, 주니어들이 AI를 '보여주기식'이 아닌 실질적인 무기로 쓸 수 있도록 현장 밀착형 기본 경로(Golden Path)를 함께 설계해 줄 책임이 있습니다.

## 결론: 더 나은 기술을 위해, 더 인간적인 협업으로

생성형 AI가 가져온 가장 거대한 역설은, **기술이 고도로 발전할수록 시스템의 성패를 가르는 최종 열쇠는 언제나 '가장 인간적인 역량'으로 되돌아온다**는 점입니다.

인공지능이 1초 만에 그럴싸하지만 알맹이 없는 '슬롭'을 쏟아내는 시대입니다. 이 속도전에서 조직이 길을 잃지 않으려면 리더들은 숫자로만 증명되는 단기적 압박에서 벗어나야 하고, 실무자들은 기계적인 자동화 유혹에서 스스로 선을 그어야 합니다. 대신, 구성원들이 맥락을 짚고 질문을 던지며 서로의 결과물을 날카롭게 교차 검증하는 **'다소 느리지만 단단한 인간적 협업의 공간'**을 팀 내에 의도적으로 유지해야 합니다.

질문은 "우리 팀은 AI를 얼마나 많이 쓰는가"가 되어서는 안 됩니다. **"우리 팀은 AI의 파도 속에서 인간의 판단력을 온전히 회수할 '단단한 경계'를 갖고 있는가?"**가 되어야 합니다. 기술의 슬러지에 침몰하지 않고 공유 자산의 단단한 성을 함께 쌓아 올리는 것, 그것이 지금 이 시대 모든 개발자와 리더들이 함께 설계해야 할 진짜 협업의 아키텍처입니다.


---

## 참고 문헌

본문에서 직접 인용한 자료와, 논지를 보강하는 추가 참고 자료를 함께 모았습니다.

**개인 이득과 그 한계**
- Daniotti, Wachs, Feng, Neffke, ["Who is using AI to code? Global diffusion and impact of generative AI"](https://www.science.org/doi/10.1126/science.adz9311) (Science, 2026‑01) — 이득이 숙련자에 집중, 격차 확대
- ["DORA Report 2025"](https://dora.dev/research/2025/dora-report/) (Google Cloud, 2025‑09) — "AI는 증폭기"
- DORA, ["Balancing AI tensions: Moving from AI adoption to effective SDLC use"](https://dora.dev/insights/balancing-ai-tensions/) (2026‑03) — 검증 비용, 리뷰 부담, production readiness gap
- Faros AI Research, ["The AI Productivity Paradox Report 2025"](https://www.faros.ai/blog/ai-software-engineering) (2025‑07, 벤더 텔레메트리 리포트) — 개인 산출 증가와 리뷰 병목

**변환·흡수·회수**
- Cohen & Levinthal, ["Absorptive Capacity: A New Perspective on Learning and Innovation"](https://doi.org/10.2307/2393553) (Administrative Science Quarterly, 1990) — 흡수역량
- Pletsch, Tonial, Matos, Koch, ["Digital transformation: The role of generative AI in the evolution of knowledge management systems"](https://doi.org/10.1108/JKM-09-2025-1398) (Journal of Knowledge Management, 2026‑03) — 흡수역량, 동화 단계의 공백
- Figge, Anderson, Lewis, ["AI-human learning systems: Investigating the strategic role of AI for organizational learning"](https://doi.org/10.1177/14761270251385860) (Strategic Organization, 2026) — 개인·팀·AI 학습 시스템
- Kost, Hærem, Pentland, ["Transactive memory systems and team performance: the mediating role of routines"](https://doi.org/10.1093/icc/dtaf062) (Industrial and Corporate Change, 2026) — 공유 기억과 루틴
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

**회수 메커니즘과 격차**
- Hardman, ["The 'Cognitive Offloading' Paradox"](https://drphilippahardman.substack.com/p/the-cognitive-offloading-paradox) (2026‑04; 원 연구 Wang & Zhang 2026, 912명) — 전략적 오프로딩 해석
- LearnLM Team & Eedi, ["AI tutoring can safely and effectively support students: An RCT in UK classrooms"](https://arxiv.org/abs/2512.23633) (arXiv, 2025‑12, 프리프린트) — 인간‑인‑루프 검토의 우위
- Chowdhury, Banik, Ferdous, Shamim, ["From Industry Claims to Empirical Reality: Code Review Agents in Pull Requests"](https://arxiv.org/abs/2604.03196) (arXiv, 2026‑04) — 머지 전 사람 승인 강제
- Kraishan, ["The AI Attribution Paradox: Transparency as Social Strategy in OSS"](https://arxiv.org/abs/2512.00867) (arXiv, 2025‑11, 프리프린트) — 출처표기는 사회적 신호
- Ni, Wang, Feng et al., ["Generative AI in Action: Field Experiment from Alibaba's Customer Service"](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5012601) (SSRN, 2024‑11) — 균일 배포가 톱 성과자 품질을 떨어뜨림

**하네스와 플랫폼 운영**
- Garry Tan, ["Thin Harness, Fat Skills"](https://x.com/garrytan/status/2042925773300908103) (2026‑04) — 지능은 스킬로 올리고 하네스는 얇게라는 비대칭의 원 정식화
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
