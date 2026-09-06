---
summary: 도메인 식별자는 보존하고 Kubernetes label과 selector에 사용할 변환 규칙을 한곳에서 관리한다.
created: 2026-07-15
tags:
  - 개발/Kubernetes
---

> [!bug] 문제
> 도메인 식별자에 `:` 같은 문자가 포함되어 K8s label 값 규칙을 위반, label/selector 기반 리소스 관리가 불가능.

---

> [!question] 원인
> 도메인 ID 체계와 K8s label 문법의 충돌. label 값은 최대 63자이며, 비어 있지 않다면 영숫자로 시작·종료해야 한다. 중간에는 영숫자·`-`·`_`·`.`을 사용할 수 있다. 원본 ID 자체를 바꾸면 도메인 전체가 흔들리고, apply와 delete가 각자 다른 방식으로 sanitize하면 selector가 어긋난다.

---

> [!tip] 해결 방법
> - 원본 ID는 보존하고, **label/selector 전용 투영값을 만드는 단일 함수(SSOT, 변환 규칙의 정본)** 를 둔다 (예: `toLabelValue()`)
> - 단순 치환으로 서로 다른 ID가 같은 값이 되지 않는지도 확인한다. 변환의 결정성·충돌 가능성·최대 길이를 함께 검증한다
> - **apply와 delete가 같은 함수를 공유**해야 붙인 라벨과 찾는 라벨이 항상 일치
> - 부속 원칙: bulk delete의 selector에는 소유 범위를 충분히 포함한다 — `managed-by` 같은 넓은 라벨만으로 일괄 삭제하면 남의 리소스까지 지운다. apply 시점에 소유 단위까지 좁은 ownership label을 붙여둘 것

---

> [!info] 참고 자료
> - 출처: 비공개 개발 기록 2026-05-18
> - [Kubernetes Labels and Selectors](https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/) - label 값 문법과 selector
