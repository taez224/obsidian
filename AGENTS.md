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

- **매일**: 필요한 기록만 Daily Note 또는 Inbox에 포착. 같은 내용을 이중 기록하지 않음
- **주간**: Inbox와 실제로 읽은 Resources를 삭제·보관·Project 흡수·Slipbox 승격으로 라우팅
- **월간**: 프로젝트 상태, Slipbox 성숙도, MOC(Map of Content) 필요성 검토
- **분기/필요 시**: Archive 정리와 `vault-lint` 기계 점검

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

## Tag System (태그 체계)

계층형 태그 구조를 사용합니다. Frontmatter에서 `#` 기호 없이 작성합니다.

```yaml
tags:
  - AI
  - 개발/Java
  - 커리어/성장
```

### 주제별 태그

| 카테고리 | 태그 예시 | 용도 |
|----------|-----------|------|
| `AI/` | `AI`, `AI/에이전트`, `AI/프롬프트` | AI 관련 콘텐츠 |
| `개발/` | `개발/Java`, `개발/프론트엔드`, `개발/도구`, `개발/DevLog`, `개발/플랫폼`, `개발/트러블슈팅`, `개발/인프라` | 개발 관련 |
| `커리어/` | `커리어/성장`, `커리어/동기부여`, `커리어/이직`, `커리어/시니어` | 커리어/자기계발 |
| `프로젝트/` | `프로젝트/onlyoffice-demo` | 프로젝트별 구분 |
| `심리/` | `심리/성격검사` | 심리·자기이해 (성격검사, 자기 분석) |
| `철학` | `철학` | 철학/사상 |
| `글쓰기` | `글쓰기` | 글쓰기·커뮤니케이션 |
| `소프트웨어공학` | `소프트웨어공학` | 설계·품질·개발 방법론 |
| `지식관리` | `지식관리` | Obsidian·PARA·Zettelkasten 등 개인 지식관리 운영 |

### 노트 타입 태그

| 태그 | 용도 |
|------|------|
| `slipbox` | 01_Slipbox 영구 노트 |
| `blog` | 블로그 발행용 |
| `📚독서` | 책 노트 (메타데이터용) |
| `📰article` | 아티클/기사 스크랩 |
| `clippings` | Web Clipper 스크랩 (Clipper 자동 부여) |
| `TIL` | Periodic Notes의 Today-I-Learned 기록 |
| `type/timeline/*` | Periodic Notes 계층 (daily/weekly/monthly) |

### 태그 규칙

- Frontmatter에서 `#` 기호 사용하지 않음 (❌ `"#ai"` → ✅ `AI`)
- 계층 구분은 `/` 사용 (`개발/Java`)
- 인라인 태그(`#task`, `#next`)는 본문에서만 사용

## Linking Best Practices (노트 연결)

Zettelkasten 원칙에 따라 노트 간 연결을 적극 활용합니다.

### 핵심 규칙

| 규칙 | 설명 |
|------|------|
| **관계 우선** | 근거·적용·반례·상하위 관계를 한 줄로 설명할 수 있는 링크만 추가 |
| **출처 정밀도** | 특정 주장·인용은 블록 링크, 절 전체는 헤딩 링크, 문서 전체가 관련될 때만 문서 링크 사용 |
| **1개 이상 목표** | 새 영구 노트는 의미 있는 연결을 찾되, 적합한 연결이 없으면 억지로 만들지 않고 seedling 상태로 보고 |
| **연결 수는 성숙도가 아님** | 근거·반례·적용과 실제 재사용을 중심으로 상태를 판단하며 링크 개수만으로 `growing`·`evergreen`을 정하지 않음 |
| **Backlinks 활용** | 역링크는 Backlinks 패널로 확인 (수동 역연결 불필요) |

### 연관 섹션 형식

노트 하단에 `## 연관된 노트` 섹션을 추가합니다:

```markdown
## 연관된 노트

- [[관련 노트 1]] - 연관 이유 (간단한 설명)
- [[관련 노트 2]] - 어떤 맥락에서 연관되는지
```

### 연결 유형

| 유형 | 설명 | 예시 |
|------|------|------|
| **같은 주제** | 동일 개념의 다른 관점 | AI의 능력 ↔ AI의 책임 |
| **상위/하위** | 추상화 수준 연결 | 성장 철학 → 구체적 실천법 |
| **근거/적용** | 이론과 사례 | 철학 개념 → 실제 적용 사례 |

## Shared Agent Skills

- Claude와 Codex가 함께 쓰는 스킬의 정본은 `.agents/skills/<skill-name>/`에 둔다.
- `.claude/skills/<skill-name>`와 `.codex/skills/<skill-name>`에는 정본을 가리키는 **상대 심볼릭 링크**만 둔다.
- `SKILL.md`는 두 도구가 읽을 수 있는 공통 지침으로 유지하고, 도구 전용 런타임은 `.claude/workflows/` 또는 `.codex/`에 분리한다.

### 지식관리 스킬 라우팅

다음 순서로 캡처 경계를 판단한다.

1. 영구 노트·Slipbox 승격을 명시했으면 `permanent-note`를 사용한다.
2. 외부 자료라면 아직 읽지 않은 보관은 `capture-reference-card`, 읽고 남긴 반응은 `literature-note`를 사용한다.
3. 그 외의 개인 단상은 `capture-fleeting-note`를 사용한다.

| 요청 | 사용할 스킬 | 경계 |
|------|-------------|------|
| 단순 메모·아이디어 저장 | `capture-fleeting-note` | 원문 해석·검색 없이 `00_Inbox`에 포착하고, 원문에서 발전시킨 AI 초기 해석·질문을 필요할 때 접어서 추가. 원문만 요청하면 생략 |
| 읽지 않은 URL·외부 자료를 일단 보관 | `capture-reference-card` | 원문 제목·출처 메타데이터·한국어 식별 문장과, 사실 확인이 충분하면 내용 요약 4~7개를 `30_Resources/References/Clippings`에 포착. `source`가 URL의 정본이며 본문 원문 링크·전문·장문 번역은 넣지 않음. 개인용 전문 보관은 명시적 요청이 있을 때 Git에서 제외된 `_local-snapshots/`에만 저장 |
| 읽은 외부 자료(영상·아티클)의 참고노트 작성 | `literature-note` | 사용자가 반응한 대목 중심으로 인용/생각을 분리해 `30_Resources/References/Articles`에 저장. 전체 요약·단순 대화 요약 파일 생성·전문 복제·자동 승격 금지 |
| 생각·노트의 소크라테스식 문답 | `socratic-dialogue` | 사용자의 현재 입장을 확인한 뒤 답변에 따라 질문을 한 번에 하나씩 이어감. 대화 전문과 AI 결론은 저장하지 않고 채택한 변화만 후속 스킬의 입력 후보로 정리 |
| 명시적인 영구 노트 승격·보강 | `permanent-note` | 기존 Slipbox와 대조하고 사용자 언어의 주장으로 정제 |
| Inbox·Resources 승격, 병합, 연결, MOC 판단 | `review-zettelkasten` | 의미 판단 후보를 먼저 제안하고 승인된 항목만 적용 |
| frontmatter·죽은 링크·고립 노트 검사 | `vault-lint` | 기계적 탐지 담당. 연결·승격·MOC 의미 판단은 하지 않음 |

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
