---
created: 2026-07-15
tags:
  - 개발/트러블슈팅
  - 개발/인프라
---

> [!bug] 문제
> Secret 값을 변경해 apply했고 성공했는데, 이미 떠 있는 Pod의 동작이 바뀌지 않는다. "apply 성공했는데 반영이 안 되는" 유령 버그처럼 보인다.

---

> [!question] 원인
> `envFrom.secretRef`(및 `env.valueFrom.secretKeyRef`)는 **컨테이너 생성 시점에 kubelet이 환경변수로 주입**한다. Secret을 갱신해도 실행 중인 Pod의 env는 그대로다. 볼륨 마운트 방식과 달리 env 주입은 런타임 갱신이 없다.

---

> [!tip] 해결 방법
> - pod template에 **rollout을 유발하는 annotation**을 심는다 — 예: 관련 리소스의 `modifiedAt` epoch 값. 값이 바뀌면 template 해시가 바뀌어 재기동이 강제된다
> - "정확히 값 변경일 때만"을 노리기보다 약간의 over-trigger를 감수하는 편이 단순하다 (별도 controller나 Reloader 없이 기존 GitOps 흐름 재사용)
> - 부속 함정: server-side apply(SSA)로 Secret을 관리하기로 했다면 `stringData`를 섞어 쓰지 말 것 — 필드 소유권 충돌이 난다 (K8s 공식 문서). apply 전략은 한 가지로 일원화

---

> [!info] 참고 자료
> - 출처: 로컬 DevLog 2026-05-14 (git 미추적 원본)
