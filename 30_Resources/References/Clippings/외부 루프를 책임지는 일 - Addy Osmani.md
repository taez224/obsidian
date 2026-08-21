---
title: "Own the Outer Loop"
source: https://addyosmani.com/blog/own-the-outer-loop/
author:
  - Addy Osmani
published: 2026-07-15
created: 2026-08-13
description: 에이전트가 실행의 내부 루프를 맡을 때, 엔지니어는 증거를 바탕으로 경계에서 판정하고 책임지는 외부 루프를 맡아야 한다고 제안하는 AI Engineer World's Fair 2026 기조연설 원고.
thumbnail: https://addyosmani.com/assets/images/outer-loop.jpg
tags:
  - clippings
status: unread
my_take: ""
---

> [!note] 저장 맥락
> 'AI Agent 시대의 Human Agency' 글에서 outer loop를 인접 담론으로 확인한 자료.

## 내용 요약

- 저자는 에이전트를 모델 자체가 아니라 파일·도구·메모리·스킬·샌드박스·권한·관측성·복구 수단으로 이뤄진 harness와 결합된 시스템으로 정의한다.
- 그 시스템의 내부 루프는 조사, 구현, 검증, 반복으로 이뤄지며, 완료 여부는 모델의 자기 판단이 아니라 독립적인 검증이 정해야 한다고 주장한다.
- 내부 루프에서 나온 증거가 경계를 건너면, 의존 시스템을 책임지는 사람이 배포·차단·방향 전환·가드레일 추가 같은 최종 판정(verdict)을 내린다고 설명한다.
- 사람은 에이전트의 매 단계에 들어가기보다 입력·아키텍처·불변식을 정하는 제약 루프, 표본 검토 루프, 감사 루프, 소유권 루프를 맡아야 한다고 제안한다.
- 에이전트에게 가능한 최대 자율성을 주기보다, 타입 검사·테스트·훅·샌드박스 제한·감사 로그·모니터링처럼 작업을 멈추고 점검할 수 있는 back pressure를 설계해야 한다고 본다.
- 에이전트 위임의 위험으로 산출물을 무비판적으로 받아들이는 인지적 양도, 이해와 기억의 격차가 누적되는 인지 부채, 여러 에이전트를 조율하는 인지 대역폭의 한계를 든다.
