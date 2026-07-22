---
title: Martin Fowler의 'LLMs bring new nature of abstraction'을 읽고..
created: 2025-06-27
published: 2025-06-27
tags:
  - blog
  - AI
status: published
author: TaeZ
publication: Velog
source: https://velog.io/@taez224/AI-%EC%8B%9C%EB%8C%80-%EA%B0%9C%EB%B0%9C%EC%9E%90%EB%8A%94-%EB%A7%A4%EC%9D%BC-%EC%A3%BC%EC%82%AC%EC%9C%84%EB%A5%BC-%EA%B5%B4%EB%A6%B0%EB%8B%A4
summary: LLM의 비결정성이 개발의 추상화·테스트·품질 판단을 어떻게 바꾸는지 Martin Fowler 글을 바탕으로 성찰한 후기.
related:
  - "[[AI 시대 개발자는 매일 주사위를 굴린다]]"
---

# Martin Fowler의 'LLMs bring new nature of abstraction'을 읽고..

Martin Fowler의 글을 읽고 받은 인사이트를 AI와 함께 정리하면서 관련 내용을 브런치에 정리했고, velog에는 조금 더 가볍게 후기의 후기 느낌으로 정리

---

## 결정론적 개발은 끝났다

입력과 출력이 정확히 대응하던 시절, 개발은 예측 가능한 세계의 논리 게임이었다.  
조건을 정확히 정의하고, 코드를 작성하고, 테스트를 통과하면 그것이 ‘정답’이었다.

이 결정론적 기반 위에서 우리는 수많은 개발 문화를 쌓아올렸다.

모두는 “이 코드는 항상 이렇게 동작해야 한다”는 전제 위에 세워졌다.

하지만 그 기본값이 이제 흔들리고 있다.

---

## 프롬프트는 관측이다

LLM 시대의 개발은 하나의 명제를 전제로 한다:

> “같은 프롬프트를 입력해도 결과는 매번 달라질 수 있다.”

이는 단순한 노이즈나 랜덤 시드의 문제가 아니다.  
LLM은 본질적으로 확률적이며, 프롬프트는 출력 결과에 영향을 미치는 관측 행위다.

양자역학에서 입자의 상태가 관측되기 전까지는 ‘확률적 파동’으로 존재하듯,  
프롬프트 역시 LLM 내부의 잠재적 결과 공간을 특정 방향으로 붕괴시키는 작용을 한다.

```python
# 프롬프트 A: 간단한 요청
prompt_a = "Write a function to sort a list"

# 프롬프트 B: 상세한 요청  
prompt_b = """
Write a Python function to sort a list of integers.
Requirements:
- Use efficient algorithm (prefer O(n log n))
- Handle edge cases (empty list, single element)
- Include proper error handling
- Add comprehensive docstrings
- Follow PEP 8 style guidelines
"""
```

위 두 프롬프트는 ‘정렬 함수 작성’이라는 같은 목표를 요청하지만 프롬프트 구성이라는 `관측 방법` 에 따라 전혀 다른 결과물이 나온다.  
프롬프트는 설계서이고, 관측 방식이며, 결과를 유도하는 장치다.

---

## 4\. Martin Fowler가 말한 “비결정적 추상화”

최근 Martin Fowler는 이런 흐름을 non-deterministic abstraction 이라고 명명했다.  
이는 단순히 추상화 수준을 올리는 것이 아니라, 추상화의 방식이 확률적으로 바뀌는 것을 의미한다.

Fortran에서 Ruby로의 진화는 ‘편리함의 도약’이었지만,  
Ruby에서 프롬프트로의 도약은 ‘성격이 완전히 다른’ 도약이다.

과거에는 코드를 컴파일하면 항상 같은 버그가 발생했지만,  
지금은 프롬프트를 실행할 때마다 미묘하게 다른 품질의 결과가 나타난다.

이전 추상화는 선형적 발전이었다면,  
LLM은 추상화의 방향을 수평으로, 그것도 불확실성의 공간으로 밀어넣고 있다.

---

## 우리는 무엇을 설계해야 하는가?

개발자의 역할은 구현자에서 설계자, 조정자, 관측자로 전환되고 있다.

- 문제 정의는 더 복잡해지고
- 프롬프트는 ‘명령’이 아니라 ‘출력 경향’을 유도하는 도구이며
- 버그는 코드보다도 설명의 부족, 맥락의 누락에서 발생한다

결국 필요한 것은 두 가지다:

**1\. 설계 능력**: 복잡한 의도를 명확하게 구조화하고, 프롬프트로 전환하는 능력  
**2\. 수용 전략**: ‘정답’이 아니라 ‘수용 가능한 출력 범위’를 정의하고, 이를 실험·조정하는 능력

---

## 전략 없는 확률은 도박이다

지금까지 우리는 확정성 위에 전략을 세웠다.  
이제는 확률성 위에서 전략을 다시 짜야 한다.

- 테스트는 여전히 필요한가?
- 품질 기준은 정량인가, 정성인가?
- 출력을 안정화하는 가장 현실적인 방법은 무엇인가?

이 질문은 모두 비결정성의 시대에 개발자가 풀어야 할 전략적 과제가 된다.

---

## 우리는 더 이상 기계의 언어로 말하지 않는다

개발은 더 이상 컴파일러와 인터프리터를 위한 활동이 아니다.  
LLM 시대의 개발은 인간의 언어, 맥락, 관측, 설계, 조율, 판단의 영역으로 이동하고 있다.

⸻

> “프롬프트는 코드가 아니라 계약서다. 결과는 출력이 아니라 해석이다.”

개발자는 더 이상 정확한 입력으로 정확한 출력을 얻는 엔지니어가 아니다.  
우리는 이제 확률의 파동 위에서 전략을 구성하는 아키텍트다.

⸻

📚 관련 링크

- 📘 [Martin Fowler - LLMs bring new nature of abstraction](https://martinfowler.com/articles/2025-nature-abstraction.html)
- ✍️ [brunch - AI 시대 개발자는 매일 주사위를 굴린다](https://brunch.co.kr/@taez/7)
