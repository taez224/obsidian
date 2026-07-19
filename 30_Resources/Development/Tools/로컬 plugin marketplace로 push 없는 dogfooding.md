---
created: 2026-07-15
tags:
  - 개발/도구
  - AI/에이전트
---

# 로컬 plugin marketplace로 push 없는 dogfooding

Claude Code 플러그인을 개발할 때, 원격 저장소에 push하지 않고도 **로컬 경로를 marketplace로 직접 등록**해 다른 레포에서 설치·사용할 수 있다.

```
/plugin marketplace add /absolute/path/to/plugin-repo
```

- 레포에 `marketplace.json`이 있으면 그 자체가 marketplace로 동작
- 다른 프로젝트 레포에서 위 명령으로 등록 → 스킬을 `/플러그인명:스킬명`으로 즉시 호출

가치는 **반복 사이클의 속도**에 있다. 외부 시스템(원격 CI·배포) 없이 수정 → 즉시 테스트가 가능해서, 도구를 만들고 다음 작업에서 바로 자기 소비하는 dogfooding 회로가 성립한다. 실제로 스킬 신설 → 다음 주 본격 활용 → 결함 발견·수정의 1주 사이클이 이 구조 위에서 돌았다.

## 출처

- 로컬 DevLog weekly 2026-W20 (git 미추적 원본)
