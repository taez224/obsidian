---
created: 2026-09-22
slug: verification-not-validation
tags:
  - AI
  - 개발
type: permanent
status: seedling
aliases:
  - verification과 validation
---

# verification이 빨라져도 validation을 대신하지 않는다

AI 코딩 도구를 쓰면서 테스트를 작성하고 통과시키는 데 드는 수고가 크게 줄었다. 수정을 요청하면 관련 테스트를 알아서 만들고, TDD를 요청하면 테스트부터 구현과 리팩터링까지 이어간다. 테스트까지 모두 통과하면 내가 요청한 기능도 완성됐다고 여기기 쉽다.

하지만 테스트 통과는 테스트에 담긴 조건을 만족했다는 뜻일 뿐이다. 구현과 테스트가 잘못된 전제 위에 만들어졌다면, 사용자의 요구와 어긋난 기능도 테스트를 통과할 수 있다.

## verification과 validation

Boehm은 1984년 논문[^boehm]에서 *verification*과 *validation*을 다음과 같이 구분했다.

| 구분           | 확인하는 것                                                                                     |
| ------------ | ------------------------------------------------------------------------------------------ |
| verification | 제품을 명세에 맞게 만들었는가? - *Are we building the product right?*                                   |
| validation   | 제품이 실제 사용 맥락에서 사용자의 필요와 목적에 맞는가. 곧 제품의 적합성(fitness) - *Are we building the right product?* |

Boehm은 요구사항과 설계 명세를 개발 초기에 확인해 뒤늦은 수정 비용을 줄이는 문제를 다뤘다. validation은 다 만든 제품을 마지막에 점검하는 일에 그치지 않고 요구사항 자체가 사용자의 필요에 맞는지를 확인하는 일이기도 하다.

Lahiri는 AI 에이전트 시대에 자연어로 적은 요구와 프로그램의 실제 동작 사이의 간극을  **intent gap**이라 부른다[^lahiri]. 이 간극을 줄이려면 의도를 테스트나 명세로 구체화해야 하지만, 그 명세가 실제 의도를 담았는지에 대한 최종 판단은 결국 요구를 낸 사람에게 남는다고 본다.

verification과 validation을 단순히 기계적 테스트와 사람의 리뷰로 나눌 수는 없다. validation에도 실제 사용 환경을 반영한 테스트를 쓸 수 있고, 리뷰에서 명세와 구현의 일치를 확인할 수도 있다. 구분하는 기준은 방법이 아니라 확인하려는 대상이다.

어떤 확인이 빠졌는지는 무엇이 어긋났는지로 가린다. 구현이 명세와 달랐다면 verification을, 명세대로 만들었는데 필요와 어긋났다면 validation을 놓친 것이다.

## 테스트 통과와 작업 완료

내 경험에서는 validation을 건너뛰기 쉬워진 것이 문제였다. 구현과 테스트에 시간이 걸릴 때는 중간에 직접 써보며 [[AI로 빨라진 개인, 소화하지 못하는 팀|내 선택을 다시 생각할 틈]]도 있었다. 이제는 직접 써보기 전에 테스트가 먼저 통과한다. 직접 써볼 수 있는 시점도 함께 앞당겨졌지만, 먼저 나온 테스트 통과를 완료로 받아들이면 그 기회를 놓치게 된다.

## 개별 기능 테스트가 놓치는 것

요즘 AI가 쓴 테스트를 볼 때는 테스트 코드 자체보다 각 테스트가 무엇을 확인하는지, 빠진 조건이나 중복된 검사가 없는지를 더 살핀다. 그렇다고 처음부터 모든 사용 상황을 예상할 수는 없다. 놓친 상황은 직접 써보거나 리뷰하면서 발견되곤 했다.

요구사항이 명시돼 있어도 테스트가 실제 사용 방식을 놓칠 수 있다. SpecBench[^specbench]에서는 개별 기능을 확인하는 공개 테스트의 통과율은 높았지만 여러 기능을 조합한 숨겨진 테스트에서 그 성공이 이어지지 않았다. 이 사례는 validation 이전의 verification 공백을 보여준다.

## 요구사항을 다시 살피기까지

한 기능을 몇 주 다듬는 동안 "이게 정말 필요한가"라는 의문이 있었는데, 리뷰를 준비하며 이 기능의 목적과 구현을 나란히 놓고 본 뒤에야 어긋난 부분이 보였다. 다시 살핀 것은 [[Human Agency는 판단을 실제 선택으로 옮기는 힘이다|이 기능이 필요하다고 판단한 근거]]였다. 테스트는 매번 통과했으니 verification은 항상 한 셈이다. 요구사항의 validation은 몇 주 뒤에야 했고, 그사이 어긋난 기능을 다듬은 시간이 그 비용이었다. 요구사항을 다시 살펴볼 시점은 테스트처럼 저절로 오지 않았다.

> [!question]- 발전시킬 질문
> - 혼자 일할 때는 언제, 무엇을 기준으로 구현과 요구사항을 다시 살펴볼까?

## 연관된 글

> [!article] 리뷰가 판단을 다시 열었던 경험
> [[AI Agent 시대의 Human Agency]]

## 연관된 노트

- [[AI 시대의 판단력은 맥락을 실행 기준으로 바꾸는 능력이다]] - 테스트가 확인할 기준을 제품과 사용자의 맥락에서 정하는 일
- [[생성은 AI에게, 검증은 나에게]] - 사람이 맡은 검증에 요구사항의 적합성까지 포함해야 하는 이유
- [[AI 코딩 도구는 이해 부채를 만든다]] - 속도가 건너뛰게 하는 단계가 이해인 경우

[^boehm]: Barry W. Boehm, [Verifying and Validating Software Requirements and Design Specifications](https://doi.org/10.1109/MS.1984.233702), IEEE Software 1(1), 1984.
[^lahiri]: Shuvendu K. Lahiri, [Intent Formalization: A Grand Challenge for Reliable Coding in the Age of AI Agents](https://arxiv.org/abs/2603.17150), arXiv, 2026.
[^specbench]: Bingchen Zhao 외, [SpecBench: Measuring Reward Hacking in Long-Horizon Coding Agents](https://arxiv.org/abs/2605.21384), arXiv, 2026.
