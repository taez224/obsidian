---
summary: 도메인 식별자는 보존하고 Kubernetes label과 selector에 사용할 변환 규칙을 한곳에서 관리한다.
created: 2026-07-15
slug: k8s-label-safe-identifier
tags:
  - 개발/Kubernetes
---

# K8s label 규칙을 어기는 식별자

도메인 식별자에 `:`가 들어 있어서 그 값을 Kubernetes label에 그대로 쓸 수 없었다. label을 붙이지 못하니 selector로 리소스를 묶어 조회하거나 삭제하는 일도 되지 않았다.

두 이름 체계가 서로 다른 문법을 쓰는 것이 원인이다. [Kubernetes의 label 문법](https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/)은 값을 최대 63자로 제한하고, 값이 비어 있지 않다면 영숫자로 시작하고 끝나야 한다. 중간에는 영숫자와 `-`와 `_`와 `.`을 쓸 수 있다. 도메인 ID 체계는 이 제약과 무관하게 만들어졌다.

원본 ID를 label 문법에 맞게 바꾸는 방법은 쓰지 않았다. ID는 도메인 전체가 참조하는 값이라 형식을 바꾸면 영향 범위를 가늠하기 어렵다. 그래서 원본은 그대로 두고, label과 selector에 쓸 값을 따로 만들어 내는 함수 하나를 두었다. `toLabelValue()`처럼 변환 규칙을 한곳에만 두면 그 함수가 규칙의 정본이 된다.

함수를 하나로 모은 이유는 apply와 delete가 같은 값을 만들어야 하기 때문이다. 두 경로가 각자 변환하면 붙인 라벨과 찾는 라벨이 어긋나서 selector가 아무것도 찾지 못한다.

변환 함수를 만들 때는 서로 다른 ID가 같은 값으로 변환되지 않는지 확인해야 한다. 문자를 단순히 치환하면 서로 다른 ID가 같은 값이 될 수 있다. 변환이 언제나 같은 결과를 내는지, 충돌이 가능한지, 최대 길이를 넘지 않는지를 함께 검증한다.

## 일괄 삭제의 selector 범위

> [!warning] 넓은 라벨로 하는 일괄 삭제
> `managed-by`처럼 넓은 라벨만으로 일괄 삭제하면 같은 라벨을 쓰는 다른 리소스까지 지워버릴 수 있다.

여기서 딸려 나온 원칙이 하나 있다. 여러 리소스를 한 번에 지울 때는 selector에 소유 범위를 충분히 넣어야 한다. apply 시점에 소유 단위까지 좁은 ownership label을 함께 붙여 두면, 삭제할 때 그 라벨로 범위를 제한할 수 있다.
