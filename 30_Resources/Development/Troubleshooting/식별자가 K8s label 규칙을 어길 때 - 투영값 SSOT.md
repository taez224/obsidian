---
created: 2026-07-15
tags:
  - 개발/트러블슈팅
  - 개발/인프라
---

> [!bug] 문제
> 도메인 식별자에 `:` 같은 문자가 포함되어 K8s label 값 규칙(영숫자·`-`·`_`·`.`)을 위반, label/selector 기반 리소스 관리가 불가능.

---

> [!question] 원인
> 도메인 ID 체계와 K8s label 문법의 충돌. 원본 ID 자체를 바꾸면 도메인 전체가 흔들리고, apply와 delete가 각자 다른 방식으로 sanitize하면 selector가 어긋난다.

---

> [!tip] 해결 방법
> - 원본 ID는 보존하고, **label/selector 전용 투영값을 만드는 단일 함수(SSOT)** 를 둔다 (예: `toLabelValue()`)
> - **apply와 delete가 같은 함수를 공유**해야 붙인 라벨과 찾는 라벨이 항상 일치
> - 부속 원칙: bulk delete의 안전성은 라벨의 좁기에 비례 — `managed-by` 같은 넓은 라벨만으로 일괄 삭제하면 남의 리소스까지 지운다. apply 시점에 소유 단위까지 좁은 ownership label을 붙여둘 것

---

> [!info] 참고 자료
> - 출처: 로컬 DevLog 2026-05-18 (git 미추적 원본)
