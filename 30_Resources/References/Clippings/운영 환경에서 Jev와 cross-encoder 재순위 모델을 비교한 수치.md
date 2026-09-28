---
title: "Jev vs. a Cross-Encoder Reranker in Production: The Numbers"
source: https://getunblocked.com/blog/jev-in-production-vs-cross-encoder/
author:
  - Morteza Milani
published: 2026-09-22
created: 2026-09-28
description: Unblocked가 에이전트의 메모 선택 단계에서 운영 중이던 cross-encoder 재순위 모델과 Jev를 질문·메모 쌍 12,927개로 비교한 글. 같은 비용에서 정밀도와 재현율이 모두 올랐다고 보고한다.
thumbnail: https://cdn.sanity.io/images/31mw1ch6/production/72ba7132fa81ccd5a6a537d8bf6302436fb0e293-1600x836.png
status: unread
my_take: ""
---

> [!note] 저장 맥락
> Jev 레이더(2026-09-28)의 「요즘 관심사: Jev」 활용 사례에서 골라 저장했다.

## 내용 요약

- Unblocked의 에이전트는 질문마다 저장된 메모 중 무엇을 프롬프트에 넣을지 정한다. 기존 방식은 임베딩 코사인 유사도로 100개를 고른 뒤 cross-encoder로 재순위해 기준값 이상만 남기는 2단계였다.
- 운영 로그의 "열어 본 메모"는 기존 방식이 이미 보여 준 메모라서 평가 라벨로 쓰지 않았다. 대신 운영 질문 292개마다 당시 모든 메모를 후보로 복원하고, 결과를 모르는 LLM 심판이 12,927쌍을 채점하게 했다. 관련 쌍은 1.8%뿐이라 정확도는 보지 않았다.
- Jev를 두 방식으로 시험했다. 질문과 메모 한 쌍씩 묻는 방식은 기존 방식보다 낮았고, 질문을 state로 두고 메모 20개를 Noul 20개로 한 번에 묻는 fan-out 방식은 기존 방식을 넘었다. 메모 하나만 보면 비교 대상이 없어 후하게 채점한다고 해석한다.
- 지연은 p50 기준 0.20초에서 0.35초로 늘었고, 질문 1,000개당 비용은 $1.87에서 $1.76으로 비슷했다.
- 지시문 변형 9가지를 하루 동안 시험했지만 차이는 잡음 수준이었다. 기준값을 옮기는 것만으로 원하던 조정이 되었다며, 문구가 아니라 기준값을 조정하라고 권한다.
- 평가 비용은 약 12달러와 이틀이었고, 결과는 한 작업의 수치일 뿐 벤치마크가 아니라고 밝힌다. Jev는 이 결정을 운영에서 맡고 있다.
