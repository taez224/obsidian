---
created: 2026-07-15
slug: local-plugin-marketplace
summary: Claude Code 플러그인 저장소를 로컬 경로로 marketplace에 등록하면 push 없이 다른 저장소에서 바로 설치해 써 보며 고칠 수 있다.
tags:
  - 개발/도구
  - AI/에이전트
---

# 로컬 plugin marketplace로 push 없는 dogfooding

플러그인을 한 줄 고칠 때마다 원격 저장소에 push하고 설치를 다시 하면, 확인에 걸리는 시간이 고치는 시간보다 길어진다. 등록할 때 원격 주소 대신 **로컬 절대 경로**를 주면 이 왕복이 없어진다.

```
/plugin marketplace add /absolute/path/to/plugin-repo
```

- 레포에 `marketplace.json`이 있으면 그 자체가 marketplace로 동작
- 다른 프로젝트 레포에서 위 명령으로 등록 → 스킬을 `/플러그인명:스킬명`으로 즉시 호출

가치는 **반복 사이클의 속도**에 있다. 외부 시스템(원격 CI·배포) 없이 수정하고 바로 테스트할 수 있어서, 도구를 만든 사람이 다음 작업에서 직접 사용해 검증하는 dogfooding 흐름이 이어진다. 실제로 스킬 신설 → 다음 주 본격 활용 → 결함 발견·수정의 1주 사이클이 이 구조 위에서 돌았다.
