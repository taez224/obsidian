---
title: Introducing System One Models & Jev
source: https://typesafe.ai/blog/introducing-system-one-models-and-jev
author:
  - Diogo Almeida
published: 2026-09-15
created: 2026-09-23
description: TypeSafe AI가 텍스트 대신 타입이 정해진 판단과 확률을 돌려주는 첫 System One 모델 Jev를 공개하며, LLM과의 차이와 속도·비용·타입 안전성 근거를 제시한 발표 글.
thumbnail: https://framerusercontent.com/images/RtIGTDwO43jR4ZDilesXiR5znc.jpg
status: unread
my_take: ""
---

## 내용 요약

- 채팅 모델은 이미 사람보다 뛰어난데 자동화가 늘지 않는 이유를 문제로 삼는다. 답으로 소프트웨어가 바로 쓸 수 있는 빠르고 구조화된 판단을 내리는 모델 계열을 제안하고, Kahneman의 시스템 1 사고에서 이름을 따 System One 모델이라 부른다.
- 첫 모델 Jev는 문자열을 생성하지 않는다. 비정형 상태와 미리 정의한 질문을 받아 타입이 정해진 값과 보정된(calibrated) 확률·확신도를 돌려주며, 출력을 순차가 아닌 병렬로 한 번에 샘플링한다.
- 학습 방법으로 RLHF·RLVR 대신 확률이 실제 정답률과 맞도록 최적화하는 RLCD(Reinforcement Learning for Calibrated Decisions)를 쓴다고 밝힌다.
- 가격은 입력 100만 토큰당 $0.042, 출력은 무료이고 응답 시간은 70~500ms다. 사내 워크플로 평가에서 LLM 대비 193.6배 빠르고 444.6배 저렴했다는 수치는 실제 이득의 상한에 가깝다고 스스로 단서를 붙인다.
- 워크플로 평가는 같은 코드 워크플로에서 GPT-6 Astra와 Fable 5.1 예측의 평균을 기준 답으로 삼아 비교한다. 평가를 사내 팀이 만들었고 기준 모델 선택에 편향이 있을 수 있다고 밝힌다.
- 타입 오류는 스키마 보장으로 수학적으로 불가능하다고 주장하며, 환각률 0%는 실측이 아니라 스키마 보장에서 나온 값이라고 설명한다.
- 적합한 용도로 워크플로 안의 분류·라우팅·채점 같은 "스마트 if 문", 대규모 데이터 map-reduce, 실시간 애플리케이션, LLM 출력 검증과 가드레일을 든다. Choice 선택지는 최대 255개이며, 데모로 Doom 플레이와 위키 레이싱을 보여 준다.
