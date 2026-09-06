---
summary: Secret 적용 성공과 실행 중인 컨테이너의 환경변수 갱신은 별개의 일이다.
created: 2026-07-15
tags:
  - 개발/Kubernetes
---

> [!bug] 문제
> Secret 값을 변경해 apply했고 성공했는데, 이미 떠 있는 Pod의 동작이 바뀌지 않는다. "apply 성공했는데 반영이 안 되는" 유령 버그처럼 보인다.

---

> [!question] 원인
> `envFrom.secretRef`(및 `env.valueFrom.secretKeyRef`)는 **컨테이너 생성 시점에 kubelet이 환경변수로 주입**한다. Secret을 갱신해도 실행 중인 Pod의 env는 그대로다. 일반 Secret 볼륨의 파일 갱신과 달리 env 주입은 런타임 갱신이 없다. 볼륨도 반영 지연이 있으며, `subPath`로 마운트한 파일은 자동 갱신되지 않는다.

---

> [!tip] 해결 방법
> - Deployment의 pod template에 **rollout을 유발하는 annotation**을 심는다 — 예: 관련 리소스의 `modifiedAt` epoch 값. 값이 바뀌면 Pod template 변경으로 새 ReplicaSet의 rollout이 시작된다
> - "정확히 값 변경일 때만"을 노리기보다 약간의 over-trigger를 감수하는 편이 단순하다 (별도 controller나 Reloader 없이 기존 GitOps 흐름 재사용)
> - 부속 함정: server-side apply(SSA)로 Secret을 관리하기로 했다면 `stringData`와의 조합은 피하는 편이 좋다. 공식 문서는 이 필드가 SSA와 잘 맞지 않는다고 설명한다. 무조건 충돌한다고 단정하기보다 사용한 필드와 field manager를 확인한다

---

> [!info] 참고 자료
> - 출처: 비공개 개발 기록 2026-05-14
> - [Kubernetes: Secret을 환경변수로 사용하기](https://kubernetes.io/docs/tasks/inject-data-application/distribute-credentials-secure/)
> - [Kubernetes Secrets](https://kubernetes.io/docs/concepts/configuration/secret/) - 볼륨 갱신과 stringData 제약
