# Agent Instructions

This file provides guidance to AI coding agents when working with this repository.

## Repository Overview

This is an **Obsidian Vault** - a personal knowledge management system based on PARA methodology and Zettelkasten. It contains Markdown notes, not source code.

## Vault Structure (PARA + Zettelkasten)

```
00_Inbox/          빠른 캡처, 미분류 아이디어 (정기적으로 정리 필요)
01_Slipbox/        영구 보관용 노트 (Zettelkasten, 상호 연결)
  └─ _index.base   Slipbox 헬스 / 고립 노트 / 허브 노트 대시보드
10_Periodic Notes/ 시간 기반 노트 (일간/주간/월간)
  └─ YYYY/W##/     주차별 폴더 (2025-W01.md, 2025-01-01.md)
20_Projects/       진행 중인 프로젝트별 폴더
  └─ _dashboard.base  프로젝트 상태 / 방치된 프로젝트 / 최근 활동
30_Resources/      참고 자료
  ├─ Obsidian 운영 워크플로.md  사람용 vault 운영 정본
  ├─ Development/  개발 자료 (DevLog, Tools)
  ├─ References/   외부 자료 (Books, Articles, Clippings, etc)
  └─ _index.base   리소스 전반 / 도서 평점 / DevLog
40_Archive/        완료/보관 자료
99_Templates/      노트 템플릿 (Templater 문법 사용)
  └─ _property-schema.md  frontmatter 표준 (필수 참조)
00_Inbox/_inbox.base 정리 부채 가시화 (7일+/30일+ 체류 노트)
_global-health.base  vault 전체 헬스 대시보드 (Inbox 부채, 고립 노트, stale 프로젝트)
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

## Blog와 Slipbox의 경계

- `20_Projects/blog/`는 개인 글·기술 글의 **전문 정본**이다. 초안, 발행본, 연재 모두 이 폴더에 한 번만 둔다.
- 외부 발행본을 가져올 때도 전문을 Slipbox에 복제하지 않는다. `source`, `publication`, 확인된 경우 `published`를 기록한다.
- `01_Slipbox/`에는 재사용 가능한 독립 개념만 둔다. 블로그 글에서 영구 노트가 필요해지면 전문을 옮기거나 복제하지 말고, 별도 노트로 압축해 블로그 글을 링크한다.
- 프로젝트에서 나온 글도 `20_Projects/<project>/blog/`에 따로 두지 않는다. 중앙 blog에 두고 `프로젝트/<project-id>` 태그와 프로젝트 노트 링크로 맥락을 연결한다.
- 발행을 마친 뒤 반복본이 남아 있으면 정본 하나만 남기고 나머지는 `40_Archive/blog-drafts/`로 보낸다.
- 블로그의 속성·Base 운영 기준은 `20_Projects/blog/blog.md`와 `99_Templates/_property-schema.md`의 Blog 섹션을 따른다.

### 노트 검색 (QMD 우선)

특정 노트나 관련 내용을 찾을 때는 CLI 또는 MCP로 QMD를 우선 사용한다.

- 정확한 제목·파일명·고유어를 알면 lex 검색을 사용한다.
- 개념·주장·간접 표현을 찾으면 `intent / lex / vec / hyde`를 직접 작성한 structured query를 사용한다.
- 검색 snippet은 후보 탐색에만 사용하고, 판단하기 전에 상위 후보 원문을 가져와 읽는다.
- `_workspace/`와 `40_Archive/`는 현재 지식 연결 후보에서 제외한다.
- 대량 이동·삭제·병합 후 같은 세션에서 검색할 때만 `qmd update && qmd embed`를 수동 실행한다. 평소에는 SessionStart hook에 맡긴다.

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
| `프로젝트/` | `프로젝트/onlyoffice` | 프로젝트별 구분 |
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
| **1개 이상 목표** | 새 영구 노트는 의미 있는 연결을 찾되, 적합한 연결이 없으면 억지로 만들지 않고 seedling 상태로 보고 |
| **3개 이상은 성숙 신호** | 연결 수는 growing·evergreen 판단의 참고값이지 작성 할당량이 아님 |
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

## Working with This Vault

- 노트 생성/편집 시 해당 타입의 템플릿 구조를 따를 것
- Wikilinks `[[]]`로 노트 간 연결 유지
- Frontmatter (YAML) 형식 준수
- 한글 파일명 사용 가능 (URL 인코딩 불필요)

## Shared Agent Skills

- Claude와 Codex가 함께 쓰는 스킬의 정본은 `.agents/skills/<skill-name>/`에 둔다.
- `.claude/skills/<skill-name>`와 `.codex/skills/<skill-name>`에는 정본을 가리키는 **상대 심볼릭 링크**만 둔다.
- `SKILL.md`는 두 도구가 읽을 수 있는 공통 지침으로 유지하고, 도구 전용 런타임은 `.claude/workflows/` 또는 `.codex/`에 분리한다.

### 지식관리 스킬 라우팅

| 요청 | 사용할 스킬 | 경계 |
|------|-------------|------|
| 단순 메모·아이디어 저장 | `capture-fleeting-note` | 해석·확장·검색 없이 `00_Inbox`에 포착 |
| 명시적인 영구 노트 승격·보강 | `permanent-note` | 기존 Slipbox와 대조하고 사용자 언어의 주장으로 정제 |
| Inbox·Resources 승격, 병합, 연결, MOC 판단 | `review-zettelkasten` | 의미 판단 후보를 먼저 제안하고 승인된 항목만 적용 |
| frontmatter·죽은 링크·고립 노트 검사 | `vault-lint` | 기계적 탐지 담당. 연결·승격·MOC 의미 판단은 하지 않음 |

단순 메모를 자동으로 permanent note로 만들지 않는다. 삭제·이동·승격·병합·MOC 생성처럼 의미가 달라지는 변경은 사용자 승인 후 적용한다.

## Maintenance Rules (유지보수 규약, 2026-06-10 제정)

### 첨부파일

- 붙여넣기 이미지 등 일반 첨부는 `_attachments/` (Obsidian 설정 `attachmentFolderPath`로 강제)
- 프로젝트 전용 에셋은 폴더 로컬 `assets/` 허용 (예: `20_Projects/blog/assets/`)
- 루트에 떠도는 파일 금지 — 루트는 `CLAUDE.md`, `AGENTS.md`, `README.md`, `_global-health.base`만

### _workspace 수명

- 파이프라인 실행 산출물 폴더는 **7일 후 삭제** (상세: `_workspace/README.md`)
- 삭제 전 git 커밋으로 복구 가능성 확보

### 버전 관리

- **파일명 버전 금지** (`v2`, `bkup`, `최종` 등) — 버전은 git이 관리한다
- 글 시리즈는 **정본 1개**만 작업 폴더에 유지, 과거 반복본은 `40_Archive/blog-drafts/`
- 큰 정리 작업 전에는 체크포인트 커밋을 먼저 만들 것
