---
created: 2026-09-06
summary: kubectl로 Deployment의 rollout, Pod 상태, Event와 로그를 차례로 확인해 배포가 어디서 멈췄는지 좁힌다.
tags:
  - 개발/Kubernetes
---

# kubectl로 배포 상태를 확인하는 순서

배포가 끝났는지 확인하거나 진행이 멈춘 지점을 찾을 때 쓰는 조회 순서다. 먼저 Deployment 전체를 보고, 필요한 Pod로 좁힌 뒤 Event와 로그를 읽는다.

아래는 이미 존재하는 Deployment를 조회하는 예제다. `example-context`, `demo`, `document-api`는 예시 이름이므로 자신의 환경에 맞게 바꾼다. 조회할 클러스터의 접근 설정과 필요한 조회 권한이 준비되어 있어야 한다.

## 1. 조회할 대상을 정한다

```bash
kubectl config current-context

kube_context='example-context'
kube_namespace='demo'
kube_deployment='document-api'
```

현재 context를 확인한 뒤 조회 대상을 명시한다. 이후 명령의 `--context`와 `-n`은 각각 사용할 context와 namespace를 지정한다. 기본 context 설정을 바꿀 필요는 없다.

## 2. Deployment와 rollout을 확인한다

```bash
kubectl --context "$kube_context" -n "$kube_namespace" \
  get deployment "$kube_deployment"

kubectl --context "$kube_context" -n "$kube_namespace" \
  rollout status "deployment/$kube_deployment" --timeout=60s
```

`get deployment`에서 원하는 복제본 수에 비해 준비된 복제본이 얼마나 있는지 본다. `rollout status`는 rollout이 끝나는지 기다린다. **60초 timeout은 이 명령의 대기 한도이며, 배포를 취소하는 명령이 아니다.** 시간이 지났다면 다음 단계에서 상태를 더 확인한다.

기본적으로 최신 rollout을 따라가므로, 기다리는 중에 새 rollout이 시작되면 관측 대상이 바뀔 수 있다. 특정 revision만 확인하려는 경우에는 `--revision`으로 고정한다. [kubectl rollout status](https://kubernetes.io/docs/reference/kubectl/generated/kubectl_rollout/kubectl_rollout_status/)

## 3. 해당 Deployment의 Pod로 좁힌다

```bash
kubectl --context "$kube_context" -n "$kube_namespace" \
  describe deployment "$kube_deployment"
```

출력의 `Selector`, replica 상태, `Conditions`, `Events`를 확인한다. 아래는 Selector가 `app=document-api`인 경우의 예다. 이름이 비슷한 Pod를 찾기보다 실제 Selector에 맞춰 조회한다.

```bash
kubectl --context "$kube_context" -n "$kube_namespace" \
  get pods -l 'app=document-api' -o wide
```

`READY`, `STATUS`, `RESTARTS`를 보고 확인할 Pod를 고른다. 상태 이름은 원인을 좁히는 단서다.

| 표시된 상태 | 다음에 확인할 것 |
| --- | --- |
| `Pending` | 스케줄링, 자원·볼륨 등 Pod Event에 나타난 대기 이유 |
| `ImagePullBackOff` | 이미지 이름, 레지스트리 접근, 인증 관련 Event |
| `CrashLoopBackOff` | 컨테이너 종료 정보와 직전 실행의 로그 |
| 실행 중이지만 준비되지 않음 | 준비 상태 조건, probe 실패, 초기화 진행 상황 |

## 4. Event와 컨테이너 로그를 읽는다

앞에서 고른 실제 Pod 이름을 넣는다.

```bash
kube_pod='document-api-example-pod'

kubectl --context "$kube_context" -n "$kube_namespace" \
  describe pod "$kube_pod"
```

컨테이너의 `State`, `Last State`, 준비 상태와 하단 `Events`를 함께 본다. 컨테이너가 시작되기 전에 막혔다면 애플리케이션 로그보다 Event가 먼저 단서를 줄 수 있다. [kubectl describe](https://kubernetes.io/docs/reference/kubectl/generated/kubectl_describe/)

`describe`에서 확인한 컨테이너 이름으로 로그를 조회한다. 아래의 `app`도 실제 이름으로 바꾼다.

```bash
kube_container='app'

kubectl --context "$kube_context" -n "$kube_namespace" \
  logs "$kube_pod" -c "$kube_container" --tail=100 --timestamps
```

컨테이너가 재시작됐고 직전 인스턴스의 로그가 남아 있다면 다음을 사용한다.

```bash
kubectl --context "$kube_context" -n "$kube_namespace" \
  logs "$kube_pod" -c "$kube_container" --previous --tail=100 --timestamps
```

`--previous`는 같은 Pod 안에서 직전에 종료된 컨테이너 인스턴스의 로그를 뜻한다. 이전 Deployment 버전의 로그를 찾아주는 옵션은 아니다. [kubectl logs](https://kubernetes.io/docs/reference/kubectl/generated/kubectl_logs/)

## 확인 결과를 해석하는 범위

이 순서로 확인하는 것은 Kubernetes가 보고하는 배포 진행과 컨테이너 상태다. rollout이 완료되고 Pod가 준비됐더라도 실제 사용자 요청의 성공 여부는 Service·Ingress·애플리케이션 기능까지 이어서 확인해야 할 수 있다.

관련 원리는 [[Kubernetes의 원하는 상태와 실제 상태]]에 정리했다. 이 개념을 알고 명령을 읽으면 “변경을 요청했다”, “Pod가 생겼다”, “요청을 받을 준비가 됐다”를 구분할 수 있다.
