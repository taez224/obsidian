---
title: GPT-6 Astra for UI Design
source: https://www.youtube.com/watch?v=flKdHHybUl4
author:
  - Nick Babich
published: 2026-09-07
created: 2026-09-12
description: Nick Babich가 음식 배달 앱을 예로 들어 GPT-6 Astra로 UI 목업 이미지를 생성하고 design.md를 거쳐 Claude Code로 프로토타입까지 만드는 세 단계 작업 흐름을 보여 주는 영상이다.
thumbnail: https://i.ytimg.com/vi/flKdHHybUl4/maxresdefault.jpg
status: unread
my_take: ""
---

## 내용 요약

- UI 디자인 작업 흐름을 GPT-6 Astra로 UI 목업 생성, 그 목업에서 `design.md` 생성, 목업과 `design.md`를 Claude Code에 넘겨 프로토타입 제작이라는 세 단계로 나눈다.
- 목업을 생성하는 프롬프트는 GPT 모델이 마크다운 처리에 최적화되어 있으므로 마크다운 형식으로 쓰고, 코딩된 프로토타입이 아니라 이미지를 만들라고 명시적으로 요구한다. 프롬프트에는 화면에 들어갈 섹션과 컴포넌트 같은 기능 정보, 색상·간격·타이포그래피 같은 시각 스타일, iOS라는 플랫폼 관례를 모두 담는다.
- 같은 프롬프트를 medium과 max effort로 각각 실행해 비교하는데, max 쪽이 배달 아이콘이나 프로모션 카드 이미지, 여백 활용에서 조금 낫지만 이미지가 가로로 늘어나는 문제를 보였다고 말한다. 제품 아이디어를 탐색하는 단계에서는 품질을 크게 잃지 않으면서 더 빠른 medium으로 충분하다고 판단한다.
- `design.md`를 제품이 어떻게 보이고 느껴져야 하는지 정의하는 마크다운 파일이자 AI를 위한 디자인 시스템으로 설명한다. 색상·타이포그래피·간격·컴포넌트와 해야 할 것·하지 말 것을 담아 UI 목업과 코드 프로토타입 사이의 간극을 줄인다고 본다.
- 명세를 주지 않고 `design.md` 생성을 요청하면 Google의 공식 명세와 어긋난 파일이 나오므로, 최신 명세가 올라온 GitHub 페이지 링크를 후속 프롬프트에서 참조하게 해야 한다고 말한다. 이 작업에도 max effort는 필요하지 않다고 덧붙인다.
- 마지막 단계에서 도구를 바꾸는 이유로 역할 분담을 든다. GPT-6 Astra로는 위계·간격·구도·이미지·타이포그래피가 원하는 대로 나올 때까지 반복하며 시각적 목표를 정의하고, Claude Code는 작업 디렉터리 안에서 기존 아키텍처·컴포넌트·관례를 확인하고 여러 파일을 수정하며 구현을 검증할 수 있으므로 그 목표를 실제 제품으로 옮기는 데 쓴다고 설명한다.
- 목업 PNG와 `design.md`를 작업 디렉터리에 넣고 Claude Code의 공식 design 플러그인으로 디자인을 만들면, 실제 기능 제품으로 전환하기 전에 시각 속성을 조정해 볼 수 있다고 말한다.
