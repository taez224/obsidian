---
created: 2026-07-15
tags:
  - 개발/트러블슈팅
  - 개발/인프라
---

> [!bug] 문제
> GitOps 저장소에 ServiceAccount manifest를 추가했는데, 같은 패턴의 다른 서비스 SA는 ArgoCD에 보이면서 새 SA만 동기화·표시되지 않는다.

---

> [!question] 원인
> SA 단독 manifest만으로는 부족했다. 기존에 동작하던 SA들은 **ClusterRoleBinding까지 한 세트**로 정의돼 있었고, 새 SA는 CRB가 빠져 있었다. deployment가 참조하는 `serviceAccountName`과의 연결도 함께 확인해야 한다.

---

> [!tip] 해결 방법
> - SA + ClusterRoleBinding(또는 RoleBinding)을 세트로 추가하고, deployment의 `serviceAccountName` 지정까지 확인
> - 실제 권한 부여 여부는 추측하지 말고 직접 검증:
> ```bash
> kubectl get sa -n <ns>
> kubectl auth can-i <verb> <resource> --as=system:serviceaccount:<ns>:<sa>
> ```

---

> [!info] 참고 자료
> - 출처: 로컬 DevLog 2026-05-06 (git 미추적 원본)
