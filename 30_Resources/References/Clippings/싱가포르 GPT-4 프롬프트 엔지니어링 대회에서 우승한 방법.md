---
title: "How I Won Singapore’s GPT-4 Prompt Engineering Competition"
source: "https://towardsdatascience.com/how-i-won-singapores-gpt-4-prompt-engineering-competition-34c195a93d41"
author:
  - "[[Sheila Teo]]"
published: 2023-12-29
created: 2025-01-19
description: 싱가포르 GPT-4 프롬프트 엔지니어링 대회에서 우승하며 익힌 대규모 언어 모델 활용 전략을 설명한다.
tags:
  - "clippings"
status: unread
my_take: ""
---

## 내용 요약

- Context·Objective·Style·Tone·Audience·Response를 명시하는 CO-STAR 프레임워크로 프롬프트의 배경과 출력 조건을 구조화한다.
- 긴 지시와 입력 데이터를 특수 구분자나 XML 태그로 나눠 모델이 각 영역의 역할을 구별하게 하는 방법을 설명한다.
- 역할·행동 규칙·금지사항을 시스템 프롬프트에 두고, 필요하면 사용자와의 상호작용에 따라 가드레일을 동적으로 바꾸는 방식을 다룬다.
- LLM은 정확한 수치 계산보다 이상치·군집·텍스트 분류 같은 패턴 탐색에 적합하다는 전제에서 고객 데이터 분석 사례를 보여준다.
- 복잡한 작업을 단계로 분해하고 중간 산출물을 참조하며 응답 형식을 지정하고, 결과를 원본 데이터와 대조해 검증하는 절차를 제시한다.
