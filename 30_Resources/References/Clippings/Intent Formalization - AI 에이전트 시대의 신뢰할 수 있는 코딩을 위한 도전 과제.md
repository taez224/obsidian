---
title: "Intent Formalization: A Grand Challenge for Reliable Coding in the Age of AI Agents"
source: https://arxiv.org/abs/2603.17150
author:
  - Shuvendu K. Lahiri
published: 2026-03-17
created: 2026-09-22
description: 자연어 요구와 실제 프로그램 동작 사이의 간극을 intent gap이라 부르고, 비형식적 의도를 검사 가능한 형식 명세로 옮기는 intent formalization을 AI 시대 코딩 신뢰성의 핵심 과제로 제시한 논문.
status: unread
my_take: ""
---

> [!note] 저장 맥락
> [[verification이 빨라져도 validation을 대신하지 않는다]]의 출처 후보. 요구사항 정의와 다른 층위의 문제에 붙은 용어(intent gap)를 확인하려고 저장.

## 내용 요약

- AI가 코드를 유창하게 만들어도 "생성된 코드가 사용자가 의도한 일을 하는가"는 남는다. 비형식 자연어 요구와 정밀한 프로그램 동작 사이의 간극을 intent gap이라 부르며, AI 생성 코드는 이 간극을 전례 없는 규모로 키운다.
- intent formalization은 비형식 의도를 검사 가능한 형식 명세의 집합으로 옮기는 일이다. 흔한 오해를 걸러내는 가벼운 테스트부터 완전한 기능 명세, 정확한 코드를 자동 합성하는 도메인 특화 언어까지 신뢰성 요구에 따른 스펙트럼으로 본다.
- 중심 병목은 명세 자체의 검증이다. 명세가 맞는지 판정할 오라클은 사용자뿐이므로, 가벼운 사용자 상호작용과 테스트 같은 대리 산출물로 명세 품질을 평가하는 반자동 지표가 필요하다.
- 상호작용형 테스트 주도 형식화, AI가 생성한 사후조건으로 실제 버그를 잡은 사례, 비형식 명세에서 검증된 코드를 만드는 파이프라인 등 초기 연구를 조사했다.
- 벤치마크 너머로의 확장, 변경에 대한 합성 가능성, 명세 검증 지표, 풍부한 논리 처리, 사람과 AI의 명세 상호작용 설계를 열린 과제로 든다.

(요약은 초록에 근거한다. 본문 절은 확인하지 않았다.)
