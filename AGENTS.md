# Agent Instructions

This file provides guidance to AI coding agents when working with this repository.

## Repository Overview

This is an **Obsidian Vault** - a personal knowledge management system based on PARA methodology and Zettelkasten. It contains Markdown notes, not source code.

## Vault Structure (PARA + Zettelkasten)

```
00_Inbox/          빠른 캡처, 미분류 아이디어 (정기적으로 정리 필요)
  └─ _inbox.base   정리 부채 가시화 (7일+/30일+ 체류 노트)
01_Slipbox/        영구 보관용 노트 (Zettelkasten, 상호 연결)
  └─ _index.base   Slipbox 헬스 / 고립 노트 / 허브 노트 대시보드
10_Periodic Notes/ 시간 기반 노트 (일간/주간/월간)
  └─ YYYY/W##/     주차별 폴더 (2025-W01.md, 2025-01-01.md)
20_Projects/       진행 중인 프로젝트별 폴더
  └─ _dashboard.base  프로젝트 상태 / 진행 중 / 허브 미갱신 점검
30_Resources/      참고 자료
  ├─ Obsidian 운영 워크플로.md  사람용 vault 운영 정본
  ├─ Development/  개발 자료
  │  ├─ DevLog/    로컬 개발 기록 (daily, weekly, monthly)
  │  ├─ Troubleshooting/ 재사용 가능한 문제 해결 기록
  │  └─ Tools/     개발 도구 자료
  ├─ References/   외부 자료 (Books, Articles, Clippings, etc)
  └─ _index.base   리소스 전반 / 도서 평점 / DevLog
40_Archive/        완료/보관 자료
99_Templates/      노트 템플릿 (Templater 문법 사용)
  └─ _property-schema.md  frontmatter 표준 (필수 참조)
_global-health.base  vault 전체 헬스 대시보드 (Inbox 부채, 고립 노트, 허브 미갱신, 오래된 Clippings)
```

> **Frontmatter 작성 시 [[_property-schema]] 를 반드시 참조**할 것. Bases 쿼리가 이 스키마를 전제로 동작.

## 운영 정본

- 사람용 운영 흐름과 주기: [[Obsidian 운영 워크플로]]
- frontmatter 스키마: [[_property-schema]]
- 에이전트 작업 규칙: `AGENTS.md`
- 개별 작업의 실행 절차: 해당 `.agents/skills/<skill-name>/SKILL.md`

운영 문서의 상세 내용을 AGENTS나 스킬에 복제하지 않는다. 이 문서에는 에이전트가 잘못된 위치에 쓰거나 의미 판단을 자동 적용하지 않도록 하는 경계만 둔다.

## Workflow (Knowledge Flow)

```
오늘의 기록·일정 ─────────────→ 10_Periodic Notes
개인 단상·아이디어 ───────────→ 00_Inbox
책·아티클·영상·외부 자료 ─────→ 30_Resources
완료할 작업·프로젝트 산출물 ───→ 20_Projects
재사용 가능한 자기 주장 ───────→ 01_Slipbox
```

### Development와 Project의 경계

- 시간순 업무 기록은 중앙 `30_Resources/Development/DevLog/{daily,weekly,monthly}/`에 두고 `projects` 속성으로 프로젝트를 구분한다. `projects`에는 저장소명이 아니라 결과물 기준의 canonical `project_id`만 사용한다.
- Java·Spring·Kubernetes 같은 기술은 폴더가 아니라 `개발/*` 태그로 표현한다. 재사용 가능한 해결법은 `Development/Troubleshooting/`에 둔다.
- `20_Projects/<project-id>/<project-id>.md`는 목표·현재 상태·다음 행동·주요 근거의 정본이다. 소스 저장소나 DevLog를 프로젝트 폴더에 복제하지 않는다.
- 프로젝트의 현재 상태·남은 일·근거를 다시 모으거나 허브를 갱신할 때는 `sweep-project-context`를 사용한다. 원자료를 먼저 대조하고 의미 변경 후보를 제안한 뒤 승인된 내용만 허브에 반영한다.

## Blog와 Slipbox의 경계

- `20_Projects/blog/`는 개인 글·기술 글의 **전문 정본**이다. 초안, 발행본, 연재 모두 이 폴더에 한 번만 둔다.
- 외부 발행본을 가져올 때도 전문을 Slipbox에 복제하지 않는다. `source`, `publication`, 확인된 경우 `published`를 기록한다.
- `01_Slipbox/`에는 재사용 가능한 독립 개념만 둔다. 블로그 글에서 영구 노트가 필요해지면 전문을 옮기거나 복제하지 말고, 별도 노트로 압축해 블로그 글을 링크한다.
- 프로젝트에서 나온 글도 `20_Projects/<project>/blog/`에 따로 두지 않는다. 중앙 blog에 두고 `프로젝트/<project-id>` 태그와 프로젝트 노트 링크로 맥락을 연결한다.
- 발행을 마친 뒤 반복본이 남아 있으면 정본 하나만 남기고 나머지는 `40_Archive/blog-drafts/`로 보낸다.
- 블로그의 속성·Base 운영 기준은 `20_Projects/blog/blog.md`와 `99_Templates/_property-schema.md`의 Blog 섹션을 따른다.
- 연재 글을 작성·수정할 때는 글의 `series` 또는 사용자가 언급한 연재명을 확인하고, 같은 이름의 `20_Projects/blog/<series>.md`가 있으면 먼저 읽는다. 실행 절차는 `taez-insight-blog-writer`를 따른다.

### 노트 검색 (정확 검색 + QMD 의미 검색)

- 정확한 제목·파일명·문자열은 `rg`, 개념·주장·간접 표현은 QMD 의미 검색을 사용한다.
- **Codex 의미 검색은 QMD MCP `query`로 실행한다.** 기본 셸 샌드박스의 CLI `qmd query`는 macOS Metal 컨텍스트 오류를 낼 수 있다 — 같은 명령을 반복하지 않는다.
- 중요한 판단은 정확 검색과 의미 검색 후보를 병합하고, snippet이 아니라 상위 후보 원문을 읽고 내린다.
- `_workspace/`, `40_Archive/`, `30_Resources/References/Clippings/_local-snapshots/`는 현재 지식 연결 후보에서 제외한다.
- structured query 작성법, rerank·후보 수 정책, 재색인 절차 등 실행 상세는 `qmd` 스킬(`.agents/skills/qmd/SKILL.md`)이 정본이다.

## Frontmatter와 연결

- frontmatter·태그·노트 유형·성숙도는 `99_Templates/_property-schema.md`를 따른다.
- 영구 노트 링크는 키워드보다 근거·적용·반례·상하위 관계를 우선한다.
- 특정 주장·인용은 블록 링크, 절 전체는 헤딩 링크, 문서 전체가 관련될 때만 문서 링크를 사용한다.
- 적합한 연결이 없으면 억지로 만들지 않는다. 연결 수만으로 성숙도를 올리지 않는다.
- 영구 노트의 실제 형식은 `99_Templates/slipbox-template.md`, 허브는 `99_Templates/hub-note.md`를 따른다.

## Shared Agent Skills

- Claude와 Codex가 함께 쓰는 스킬의 정본은 `.agents/skills/<skill-name>/`에 둔다.
- `.claude/skills/<skill-name>`와 `.codex/skills/<skill-name>`에는 정본을 가리키는 **상대 심볼릭 링크**만 둔다.
- `SKILL.md`는 두 도구가 읽을 수 있는 공통 지침으로 유지하고, 도구 전용 런타임은 `.claude/workflows/` 또는 `.codex/`에 분리한다.

### 지식관리 스킬 라우팅

세부 절차는 각 스킬이 정본이다. 캡처 경계만 다음 순서로 판단한다.

1. 영구 노트·Slipbox 승격을 명시했으면 `permanent-note`를 사용한다.
2. 외부 자료라면 아직 읽지 않은 보관은 `capture-reference-card`, 읽고 남긴 반응은 `literature-note`를 사용한다.
3. 그 외의 개인 단상은 `capture-fleeting-note`를 사용한다.

생각이나 판단을 질문으로 검토하려는 요청은 `socratic-dialogue`를 사용하고, 확인된 변화만 후속 노트 스킬의 입력 후보로 넘긴다.

단순 메모를 자동으로 permanent note로 만들지 않는다. 삭제·이동·승격·병합·MOC 생성처럼 의미가 달라지는 변경은 사용자 승인 후 적용한다. 이 작업들은 후보 보고까지를 현재 작업의 완료로 보며, 승인 없이 적용을 계속 진행하지 않는다.

Quick Capture의 `AI 생성`은 사용자의 주장이나 검증된 참고자료가 아니다. 분석·가설·대응표·잠정 주장과 발전 질문을 접힌 callout에 둘 수 있지만, 사용자가 명시적으로 채택하지 않은 내용은 영구 노트 본문으로 승격하지 않는다. 외부 사실·인용은 출처 검증 전까지 발전시킬 단서로만 다룬다.

## Maintenance Rules

### 첨부파일

- 붙여넣기 이미지 등 일반 첨부는 `_attachments/` (Obsidian 설정 `attachmentFolderPath`로 강제)
- 프로젝트 전용 에셋은 폴더 로컬 `assets/` 허용 (예: `20_Projects/blog/assets/`)
- 루트에 떠도는 파일 금지 — 루트는 `CLAUDE.md`, `AGENTS.md`, `README.md`, `_global-health.base`만

### 버전 관리

- **파일명 버전 금지** (`v2`, `bkup`, `최종` 등) — 버전은 git이 관리한다
- 글 시리즈는 **정본 1개**만 작업 폴더에 유지, 과거 반복본은 `40_Archive/blog-drafts/`
- 큰 정리 작업 전에는 체크포인트 커밋을 먼저 만들 것
