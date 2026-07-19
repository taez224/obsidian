---
title: "My Thoughts on AI, Part 2: Agent Setup, Workflow, and Tools"
source: https://blog.isquaredsoftware.com/2026/05/ai-thoughts-part-2-agent-workflow-tools/
author:
  - Mark Erikson
published: 2026-05-07
created: 2026-07-13
description: Mark Erikson이 실제로 사용하는 AI 개발 환경과 에이전트 워크플로, 도구 구성을 소개한 글.
thumbnail: https://blog.isquaredsoftware.com/images/logo.png
tags:
  - clippings
status: unread
my_take: ""
---

## 내용 요약

- 저자가 실제 개발에 사용하는 OpenCode·CodeNomad, Anthropic Opus, VS Code와 Fork 중심의 에이전트 개발 환경을 설명하고 공개 예제 설정 저장소를 함께 제시한다.
- 새 작업을 시작할 때 부모 오케스트레이터가 현재 초점과 최근 진행 기록을 읽고 계획을 세우며, 실제 코드 탐색과 구현은 별도 하위 작업 세션이 수행하는 구조를 사용한다.
- 모든 명령을 무제한 허용하지 않고 읽기·검색·Git·셸 명령별 권한 규칙을 세워, 반복 작업의 마찰을 줄이면서 위험한 동작은 사람이 통제하도록 구성한다.
- 공유 코드 저장소와 별도로 개인 `dev-plans` 저장소를 두고 아키텍처 조사, 기능 계획, 일일 진행 기록, 하위 작업 인계 문서를 Markdown 산출물로 보존한다.
- `AGENTS.md`에는 에이전트가 따라야 할 공통 작업 원칙을 두고, 프로젝트 초기화·진행 기록·인계·작업 추적 같은 반복 절차는 명령과 스킬로 분리해 자동화한다.
- 긴 하위 작업의 컨텍스트 압축에서 세부사항이 사라지는 문제를 진행 기록과 인계 파일로 완화하고, 부모 세션은 결과만 받아 컨텍스트를 오래 유지하도록 설계한다.
- 현재 방식은 저장소 구조와 당면 과업에는 효과적이지만, 과거 결정과 연구 자료를 다시 찾는 장기 기억 및 반복된 교정에서 운영 개선점을 추출하는 자동화는 남은 과제라고 평가한다.
