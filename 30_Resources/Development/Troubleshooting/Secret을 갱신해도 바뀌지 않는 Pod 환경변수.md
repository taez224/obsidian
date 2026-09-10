---
summary: 환경변수로 주입한 Secret은 컨테이너 생성 시점에만 읽히므로, 값이 바뀌면 pod template을 바꿔 Pod를 새로 띄워야 한다.
created: 2026-07-15
slug: k8s-envfrom-secret-reload
tags:
  - 개발/Kubernetes
---

# Secret을 갱신해도 바뀌지 않는 Pod 환경변수

Secret 값을 바꿔서 apply했고 명령은 성공했는데, 이미 떠 있는 Pod의 동작이 바뀌지 않았다. 겉으로는 apply가 반영되지 않는 문제처럼 보인다.

원인은 [Secret을 환경변수로 주입하는 방식](https://kubernetes.io/docs/tasks/inject-data-application/distribute-credentials-secure/)에 있다. `envFrom.secretRef`와 `env.valueFrom.secretKeyRef`는 컨테이너를 만드는 시점에 kubelet이 값을 환경변수로 넣어 준다. 그 뒤에 Secret을 갱신해도 이미 실행 중인 Pod의 환경변수는 그대로 남는다. 환경변수 주입에는 런타임 갱신 경로가 없다. [Secret을 볼륨으로 마운트하는 방식](https://kubernetes.io/docs/concepts/configuration/secret/)은 파일이 갱신되지만 그쪽도 반영에 지연이 있고, `subPath`로 마운트한 파일은 자동으로 갱신되지 않는다.

그래서 값이 바뀌면 Pod를 새로 뜨게 만들어야 한다. Deployment의 pod template에 rollout을 유발하는 annotation을 심는 방법을 썼다. 관련 리소스의 `modifiedAt` epoch 값을 annotation에 넣으면, 값이 바뀔 때 pod template이 바뀐 것으로 취급되어 새 ReplicaSet의 rollout이 시작된다.

값이 실제로 달라졌을 때만 정확히 rollout하도록 만들기보다, 조금 과하게 도는 것을 감수하는 편이 단순했다. 별도 controller나 Reloader 같은 도구를 들이지 않고 기존 GitOps 흐름을 그대로 쓸 수 있다.

## server-side apply와 stringData

Secret을 server-side apply로 관리하기로 했다면 `stringData`와 함께 쓰는 조합은 피하는 편이 낫다. 공식 문서가 이 필드는 server-side apply와 잘 맞지 않는다고 설명한다. 다만 언제나 충돌한다고 단정하기보다, 실제로 사용한 필드와 field manager를 확인하는 편이 정확하다.

## 확인 범위

환경변수 주입에 갱신 경로가 없다는 것과 볼륨 마운트·`subPath`의 동작은 Kubernetes 공식 문서로 확인했다. annotation으로 rollout을 유발하는 방법은 실제 GitOps 흐름에 적용했다. server-side apply와 `stringData`의 충돌은 문서 설명이며 직접 재현하지 않았다.
