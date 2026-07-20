---
created: 2026-07-20
tags:
  - 커리어/성장
  - 개발/플랫폼
  - slipbox
type: permanent
status: seedling
aliases:
  - Builder-Sweeper
  - 문제 주도형 Prototyper
---

# 나의 일하는 방식은 Builder-Sweeper에 가깝다

나는 아이디어를 많이 쏟아내는 전형적인 Prototyper라기보다, 문제를 만나면 작은 PoC로 가능성을 확인하고 빠르게 구조화하는 문제 주도형 Prototyper에 가깝다. 중심 역할은 Builder-Sweeper다. 확인한 경로를 실제 제품·인프라로 구현하고, 책임이 겹치거나 복잡해진 부분을 걷어낸다.

일을 끝낼 때는 Maintainer 관점이 함께 작동한다. 기능이 한 번 동작하는 데서 멈추지 않고 lifecycle, 검증, 복구 가능성, 운영 시의 실패 경로까지 챙겨야 비로소 완결됐다고 본다. 이 관점은 구현을 늦추기 위한 절차가 아니라, 내가 만든 결과를 사람이 계속 책임질 수 있게 만드는 기준이다.

Grower에 가깝지 않다고 단정하지는 않는다. 제품이 PMF를 찾은 뒤 사용자·시장 반응을 바탕으로 반복 개선한 경험이 아직 충분하지 않아서, 지금은 내 역할로 채택하지 않는다. 이후 실제 경험이 쌓이면 이 노트의 판단을 보강하거나 수정한다.

## 출처

- [[AI 시대의 다섯 역할 아키타입 - Boris Cherny#^roles-span-two-or-three|AI 시대의 다섯 역할 아키타입 - Boris Cherny]] - 한 사람이 둘 또는 셋의 역할을 함께 할 수 있다는 분류의 전제
- [[AI 시대의 다섯 역할 아키타입 - Boris Cherny#^builder-sweeper-take|AI 시대의 다섯 역할 아키타입 - Boris Cherny]] - Builder-Sweeper·Maintainer·문제 주도형 Prototyper에 대한 나의 현재 해석
- [[HEXACO 성격검사 결과 - 2026-07-09 (claude)#^generator-verifier-combo|HEXACO 성격검사 결과]] - 창의성과 완벽주의가 함께 나타나는 성향의 참고 근거

## 연관된 노트

- [[생성은 AI에게, 검증은 나에게]] - 생성과 검증을 분리해 검증 책임을 유지하는 개인 작업 방식
