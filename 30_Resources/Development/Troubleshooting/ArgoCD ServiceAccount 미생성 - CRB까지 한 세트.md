---
created: 2026-07-15
summary: ServiceAccount가 보이지 않거나 권한 오류가 날 때 객체 생성, RBAC 권한 부여, Pod의 참조를 나눠 확인한다.
tags:
  - 개발/Kubernetes
  - 개발/ArgoCD
---

# ArgoCD에서 ServiceAccount가 보이지 않을 때

> [!bug] 문제
> GitOps 저장소에 ServiceAccount manifest를 추가했는데, 같은 패턴의 다른 서비스 ServiceAccount는 ArgoCD에 보이면서 새 계정만 동기화·표시되지 않았다.

## 생성과 권한 부여를 구분한다

당시 기록에서는 기존 구성과 비교해 ClusterRoleBinding 누락과 Deployment의 `serviceAccountName`을 함께 점검했다. 다만 **ClusterRoleBinding이 없어서 ServiceAccount 객체가 생성되지 않았다고 단정할 근거는 충분하지 않다.** ServiceAccount 생성에 ClusterRoleBinding이 필수인 것은 아니다.

ServiceAccount는 워크로드가 사용할 신원이다. RoleBinding이나 ClusterRoleBinding은 그 신원에 권한을 연결하고, Pod의 `serviceAccountName`은 어떤 신원으로 실행할지 지정한다. 객체가 없는 문제와 객체는 있지만 권한이 없는 문제를 따로 확인해야 한다.

## 확인 순서

1. ArgoCD가 바라보는 repository 경로와 revision에 ServiceAccount manifest가 포함되는지, 생성될 namespace가 맞는지 확인한다.
2. 클러스터에 객체가 실제로 없는지 확인한다. 객체가 있다면 ArgoCD 표시·추적 문제와 Pod의 참조를 나눠 조사한다.
3. 객체가 없다면 ArgoCD의 동기화 결과와 오류 메시지에서 manifest 생성·적용이 어디서 실패했는지 확인한다.
4. 필요한 API 권한이 없는 문제라면 RoleBinding 또는 ClusterRoleBinding을 확인한다. namespace 범위 권한에는 RoleBinding을 사용할 수 있으며, cluster-wide 권한이 필요할 때만 그 범위에 맞게 부여한다.

```bash
kubectl get sa <service-account> -n <namespace>
kubectl auth can-i <verb> <resource> -n <namespace> \
  --as=system:serviceaccount:<namespace>:<service-account>
```

두 명령은 각각 객체 존재와 특정 작업의 권한을 확인한다. `--as`를 사용하는 조사 계정에는 해당 신원을 impersonate할 권한이 필요하다.

## 참고 자료

- 비공개 개발 기록 2026-05-06 — 초기 관찰과 구성 비교. 생성 실패의 직접 원인은 추가 근거가 필요하다.
- [Kubernetes Service Accounts](https://kubernetes.io/docs/concepts/security/service-accounts/) - 계정 생성·권한·Pod 지정
- [Kubernetes RBAC](https://kubernetes.io/docs/reference/access-authn-authz/rbac/) - RoleBinding과 ClusterRoleBinding의 범위
