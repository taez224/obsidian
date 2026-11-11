---
created: 2026-09-22
slug: verification-not-validation
tags:
  - 개발
  - AI
type: permanent
status: growing
aliases:
  - verification과 validation
---

# verification이 빨라져도 validation을 대신하지 않는다

AI 코딩 도구를 쓰면서 테스트를 작성하고 통과시키는 데 드는 수고가 크게 줄었다. 수정을 요청하면 AI가 관련 테스트를 알아서 만든다. TDD를 요청하면 테스트를 먼저 작성한 뒤 구현하고 리팩터링한다. 테스트까지 모두 통과하면 내가 요청한 기능도 완성됐다고 여기기 쉽다.

하지만 테스트 통과는 테스트에 담긴 조건을 만족했다는 뜻일 뿐이다. 구현과 테스트 자체가 잘못된 전제에서 출발했다면 사용자의 필요와 어긋난 기능도 테스트를 통과할 수 있다.

![모니터의 네모 부품은 검사를 통과했지만, 실제 둥근 구멍을 막자 틈이 남아 마법사가 손을 멈춘다.|480](../_attachments/illustrations/verification-not-validation.webp)

## verification과 validation

Boehm은 1984년 논문[^boehm]에서 *verification*과 *validation*을 다음과 같이 구분했다.

| 구분           | 확인하는 것                                                                                     |
| ------------ | ------------------------------------------------------------------------------------------ |
| verification | 제품을 명세에 맞게 만들었는가? - *Are we building the product right?*                                   |
| validation   | 제품이 실제 사용 맥락에서 사용자의 필요와 목적에 맞는가? (적합성, fitness) - *Are we building the right product?* |

Boehm은 요구사항과 설계 명세를 개발 초기에 확인해 뒤늦은 수정 비용을 줄이는 문제를 다뤘다. validation은 다 만든 제품을 마지막에 점검하는 일에 그치지 않고 요구사항 자체가 사용자의 필요에 맞는지를 확인하는 일이기도 하다.

Lahiri는 AI 에이전트 시대에 자연어로 적은 요구와 프로그램의 실제 동작 사이의 간극을 **intent gap**이라 부른다[^lahiri]. 이 간극을 줄이려면 의도를 테스트나 명세로 구체화해야 하지만 그 명세가 실제 의도를 담았는지는 결국 요구를 낸 사람이 판단할 수밖에 없다고 본다.

verification과 validation을 단순히 자동 테스트와 사람의 리뷰로 나눌 수는 없다. validation에도 실제 사용 환경을 반영한 테스트를 쓸 수 있고 리뷰로 명세와 구현이 맞는지 확인할 수도 있다. 구분하는 기준은 방법이 아니라 확인하려는 대상이다.

구현과 명세의 불일치를 잡아내지 못했다면 verification을 놓친 것이다. 명세대로 만들었어도 실제 필요와 어긋난다는 점을 알아채지 못했다면 validation을 놓친 것이다.

## 테스트 통과와 작업 완료

AI를 쓰면서 validation을 건너뛰기 쉬워졌다. 구현과 테스트에 시간이 걸리던 때는 중간에 직접 써보며 [[AI로 빨라진 개인, 소화하지 못하는 팀|내 선택을 다시 생각할 틈]]도 있었다. 이제는 직접 써보기 전에 테스트가 먼저 통과한다. 구현이 빨라진 만큼 직접 써볼 수 있는 시점도 앞당겨졌다. 하지만 테스트 통과만으로 다 됐다고 생각하면 직접 써보지 않고 넘어가기 쉽다.

## 개별 기능 테스트가 놓치는 것

요즘 AI가 쓴 테스트를 볼 때는 테스트 코드 자체보다 각 테스트가 무엇을 확인하는지, 빠진 조건이나 중복된 검사가 없는지를 더 살핀다. 그렇다고 처음부터 모든 사용 상황을 예상할 수는 없다. 놓친 상황은 대개 직접 써보거나 리뷰하면서 드러났다.

요구사항이 명시돼 있어도 테스트가 실제 사용 방식을 놓칠 수 있다. SpecBench[^specbench]에서는 개별 기능을 확인하는 공개 테스트의 통과율은 높았지만 여러 기능을 조합한 숨겨진 테스트의 통과율은 그보다 낮았다. 숨겨진 테스트도 같은 명세에서 나왔으니 이 사례는 validation에 앞서 verification부터 놓친 경우다.

## 몇 주 뒤에야 확인한 요구사항

한 기능을 몇 주 다듬는 동안 "이 방향으로 가면 되나?" 싶은 순간이 있었다. 그런데 AI가 자신 있게 개선을 이어 가고 테스트를 만들어 통과시키니 나도 그런가 보다 하고 끌려갔다. 리뷰를 준비하면서 구현한 기능이 원래 목적에 맞는지 확인하다가 어긋난 부분을 발견했다. 그제야 [[Human Agency는 판단을 실제 선택으로 옮기는 힘이다|왜 이 방향이 맞다고 생각했는지]] 따져 봤다. 그동안에는 테스트에 담긴 조건을 만족하는지만 확인했다. 요구사항의 validation은 몇 주 뒤에야 했다. 그동안 목적에 맞지 않는 기능을 계속 다듬고 있었다. 테스트는 계속 돌렸지만 요구사항이 맞는지는 따로 확인하지 않았다.

> [!question]- 발전시킬 질문
> - 혼자 개발할 때는 요구사항이 실제 필요에 맞는지 언제, 어떻게 확인할까?

## 연관된 글

> [!article] 테스트를 통과한 SSE를 결국 쓰지 않은 이유
> [[AI Agent 시대의 Human Agency]]

## 연관된 노트

- [[AI 시대의 판단력은 맥락을 실행 기준으로 바꾸는 능력이다]]
- [[생성은 AI에게, 검증은 나에게]]
- [[AI 코딩 도구는 이해 부채를 만든다]]

[^boehm]: Barry W. Boehm, [Verifying and Validating Software Requirements and Design Specifications](https://doi.org/10.1109/MS.1984.233702), IEEE Software 1(1), 1984.
[^lahiri]: Shuvendu K. Lahiri, [Intent Formalization: A Grand Challenge for Reliable Coding in the Age of AI Agents](https://arxiv.org/abs/2603.17150), arXiv, 2026.
[^specbench]: Bingchen Zhao 외, [SpecBench: Measuring Reward Hacking in Long-Horizon Coding Agents](https://arxiv.org/abs/2605.21384), arXiv, 2026.
