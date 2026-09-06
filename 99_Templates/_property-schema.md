---
tags:
  - meta
  - schema
created: 2026-05-27
aliases:
  - Property Schema
  - Master Property Schema
---

# 📐 Master Property Schema

> **Single source of truth** — 이 vault의 모든 노트가 따라야 하는 frontmatter 표준.
> Bases 쿼리와 Dataview는 이 스키마를 전제로 작성된다. 스키마 변경 시 **이 파일을 먼저 갱신**하고 기존 노트를 마이그레이션할 것.

---

## 🌐 공통 필드 (모든 노트)

| 필드 | 타입 | 필수 | 설명 |
|------|------|------|------|
| `created` | Date `YYYY-MM-DD` | ✅ | 노트 생성일 (file.ctime 폴백 금지 — 항상 명시) |
| `tags` | List | ⬜ | 실제 횡단 탐색·필터에 사용할 때만 아래 기준으로 작성 |
| `aliases` | List | ⬜ | 다른 이름으로도 wikilink 받기 위함 |

> [!note] Bases 구현 규칙
> `created` 누락은 스키마 위반이며 `vault-lint`가 탐지한다. Base의 `file.ctime` 폴백은 누락 노트를 숨기지 않기 위한 **표시용 방어**일 뿐, `created`를 대신하지 않는다. Inbox 7일·30일 기준은 `_inbox.base`와 `_global-health.base`, 프로젝트 14일 기준은 `_dashboard.base`와 `_global-health.base`에 중복 정의되므로 기준 변경 시 두 파일을 함께 수정한다.

### 태그 사용 기준

태그는 선택 필드다. 폴더·`type`·`status`로 이미 드러나는 노트의 역할을 다시 표기하지 않고, 서로 다른 폴더를 가로질러 실제로 검색하거나 필터링할 주제·프로젝트에만 사용한다. 계층형 태그는 `/`로 구분한다. Frontmatter에서는 `#`를 붙이지 않고, `#task`·`#next` 같은 인라인 태그만 본문에서 사용한다.

```yaml
tags:
  - AI
  - 개발/Java
  - 커리어/성장
```

| 카테고리 | 태그 예시 | 용도 |
|----------|-----------|------|
| `AI/` | `AI`, `AI/에이전트`, `AI/프롬프트` | AI 관련 콘텐츠 |
| `개발/` | `개발/Java`, `개발/프론트엔드`, `개발/도구`, `개발/플랫폼`, `개발/인프라` | 개발 관련 |
| `커리어/` | `커리어/성장`, `커리어/동기부여`, `커리어/이직`, `커리어/시니어` | 커리어·자기계발 |
| `프로젝트/` | `프로젝트/onlyoffice-demo` | canonical project_id별 구분 |
| `심리/` | `심리/성격검사` | 심리·자기이해 |
| `철학` | `철학` | 철학·사상 |
| `글쓰기` | `글쓰기` | 글쓰기·커뮤니케이션 |
| `소프트웨어공학` | `소프트웨어공학` | 설계·품질·개발 방법론 |
| `지식관리` | `지식관리` | Obsidian·PARA·Zettelkasten 운영 |

`inbox`, `slipbox`, `blog`, `📚독서`, `📰article`, `clippings`처럼 위치나 다른 속성과 역할이 겹치는 태그는 새 노트의 기본값으로 넣지 않는다. 기존 노트에서는 일괄 삭제하지 않고 실제로 다시 사용할 때만 점진적으로 정리한다. `type/timeline/*`처럼 현재 템플릿의 Dataview 쿼리가 실제로 사용하는 태그는 유지한다.

---

## 📥 Inbox (`00_Inbox/`)

빠른 포착 노트. 정리·연결·승격 판단은 나중으로 미루고 원문과 다음 처리 상태만 기록한다.

```yaml
---
created: 2026-07-13
next_action: ""
---
```

| 필드 | 타입 | 필수 | 설명 |
|------|------|------|------|
| `next_action` | Text | ⬜ | 기본값은 빈 문자열. `promote-slipbox`, `archive-resources`, `link-project/<id>` 중 하나를 사용하며 삭제 결정은 본문 체크박스로 남김 |

본문 정본은 `99_Templates/quick-capture.md`를 따른다. `AI 생성`은 사용자의 주장이 아니며, 사용자가 명시적으로 채택하기 전에는 permanent note의 본문 근거로 사용하지 않는다.

---

## 🧠 Slipbox (`01_Slipbox/`)

영구 보관 노트. Zettelkasten 정원 비유로 **성숙도(status)** 를 표현한다.

```yaml
---
created: 2026-01-15
type: permanent       # permanent | fleeting | hub(MOC)
status: seedling      # seedling | growing | evergreen
aliases:
  - <대체 이름>
used_in:              # 선택 — 승인된 재사용 근거만 기록
  - "[[이 노트를 다시 쓴 글이나 문서]]"
---
```

| 필드 | 값 | 의미 |
|------|----|----|
| `type: permanent` | 영구 노트 (자기 언어로 정제됨) | 기본값 |
| `type: fleeting` | 단상/스케치 (곧 승격되거나 폐기) | |
| `type: hub` | MOC (Map of Content) | |
| `status: seedling` | 중심 주장은 명료하지만 아직 충분히 검토·적용되지 않은 생각 | 길이와 링크 수로 판정하지 않음 |
| `status: growing` | 근거·반례·적용이 붙거나 실제 글과 판단에서 재사용되기 시작한 생각 | |
| `status: evergreen` | 반복해서 검토·재사용했고 현재 판단 기준으로 안정된 생각 | 자동 판정하지 않음 |
| `used_in` | 이 노트를 **다른 맥락에서 다시 쓴** 글·문서 | 자동 기록하지 않음. `_index.base`의 재사용 뷰가 개수를 센다 |

### 연결 규칙

- 같은 키워드보다 근거·적용·반례·상하위 관계를 한 줄로 설명할 수 있는 링크를 우선한다.
- 특정 주장·인용은 블록 링크, 절 전체는 헤딩 링크, 문서 전체가 관련될 때만 문서 링크를 사용한다.
- 관계를 설명할 수 있는 본문 문장 안의 링크를 우선한다. 본문에 자연스럽게 넣기 어려운 관계만 `## 연관된 노트`에 이유와 함께 둔다.
- 적합한 연결이 없으면 억지로 만들지 않는다. Backlinks가 보여주는 역연결을 본문에 중복하지 않는다.
- 연결 수만으로 `growing`·`evergreen`을 판정하지 않는다.
- 실제 `## 연관된 노트` 형식은 `99_Templates/slipbox-template.md`를 따른다.

### 재사용(`used_in`)에 무엇을 넣는가

`status`가 재사용을 기준으로 판정되는데 재사용을 관측할 방법이 없어서 두는 필드다. **출처는 재사용이 아니다** — 이 노트를 낳은 자료를 넣으면 노트가 태어난 사실을 재사용으로 세게 되고, 다산성 자료 하나가 자기 자식 노트들의 점수를 통째로 올린다. X에서 파생된 것은 X를 입증하지 못한다.

| 넣는다 | 넣지 않는다 |
|--------|-------------|
| 이 노트를 인용한 블로그 글 | 이 노트를 승격시킨 원본 참고노트 |
| 이 원칙을 적용한 운영 문서·프로젝트 노트 | 이 노트에서 파생된 분석 문서 |
| 다른 자료를 읽다가 이 주장을 불러 쓴 참고노트 | `00_Inbox`의 초안 (승격·흡수될 때 다시 판정) |

후보 탐지는 `vault-lint`가 기계적으로 하고(`reuse_by_note`), **기록은 사람이 승인한 항목만** 한다. 자동으로 채우지 않는다.

---

## 🚀 Projects (`20_Projects/`)

진행 중인 프로젝트. Bases `_dashboard.base`가 `status`를 기준으로 동작.

```yaml
---
created: 2026-01-29
tags:
  - 프로젝트/<project-id>
  - <도메인 태그>
title: Vizend QRA
project_id: vizend-qra
status: active        # active | on-hold | completed | planning
started: 2026-01-29
ended: null           # completed일 때만
---
```

| 필드 | 비고 |
|------|------|
| `project_id` | kebab-case, 폴더명과 일치. 여러 저장소를 건드려도 하나의 결과물을 향하면 같은 ID를 사용 |
| `status: active` | 진행 중 — 프로젝트 허브가 14일 이상 미수정되면 `_dashboard.base`의 "프로젝트 허브 미갱신 (14일+)"에 표시 |
| `status: planning` | 기획 단계 (아직 코드 안 씀) |
| `status: on-hold` | 일시 중단 |
| `status: completed` | 완료 → `40_Archive/`로 이동 검토 |

### 프로젝트 하위 노트 (`20_Projects/<project>/`)

프로젝트에서 계속 참조할 결정·설계·산출물만 둔다. 시간순 업무 기록과 정기 회고의 정본은 중앙 `30_Resources/Development/DevLog/`이며 `projects` 속성으로 연결한다. 기존 프로젝트별 weekly 노트는 역사 자료로 유지하되 새 정기 기록은 중앙 DevLog에 작성한다. 하위 노트는 프로젝트 허브와 달리 `project_id`·`status`를 갖지 않는다.

```yaml
---
created: 2026-02-02
type: project-note
tags:
  - 프로젝트/<project-id>
---
```

---

## 📝 Blog Posts (`20_Projects/blog/`)

개인 글·기술 글의 **전문 정본**. 초안과 외부 발행본을 이 폴더에 한 번만 보관하고, `01_Slipbox/`에는 이 글에서 분리한 독립 개념만 둔다.

```yaml
---
title: <글 제목>
created: 2026-07-11             # vault 수집·작성일
status: draft                   # draft | published
author: TaeZ
summary: <한두 문장 요약>
publication: Velog              # 외부 발행본일 때
source: https://...             # 외부 원문 URL
published: 2025-08-29           # 원문 발행일을 확인한 경우에만
series: <연재명>                # 연재일 때
series_order: 1
related:
  - "[[관련 글 또는 프로젝트]]"
---
```

| 규칙 | 설명 |
|------|------|
| 정본 위치 | 전문은 `20_Projects/blog/`에만 둔다. 프로젝트별 하위 `blog/` 폴더를 만들지 않는다. |
| 발행본 | `status: published`에는 `publication`, `source`를 필수로 둔다. `published`는 발행일이 확인될 때만 기록한다. |
| 초안 | `status: draft`를 사용한다. 과거 반복본은 `40_Archive/blog-drafts/`로 보낸다. |
| 연재 | `series`, `series_order`와 앞·뒤 글 링크를 사용한다. |
| 프로젝트 글 | `프로젝트/<project-id>` 태그와 프로젝트 노트 링크로 맥락을 남긴다. |
| Slipbox | 블로그 전문을 복제하지 않는다. 재사용할 개념은 별도의 `type: permanent` 노트로 압축하고 블로그 글을 링크한다. |

### 연재 허브 (`20_Projects/blog/<series>.md`)

연재명과 같은 파일명의 허브를 두고, 글의 `series` 값으로 연결한다. 허브 자체에는 `series`를 넣지 않아 실제 연재 글 목록과 섞이지 않게 한다.

```yaml
---
title: Think with AI
created: 2026-07-15
type: series
status: active                # active | on-hold | completed
started: 2026-07-15
ended: null                   # completed일 때만
last_published: null          # 실제 최근 발행일, 발행 전이면 null
next_action: 1화 발행
---
```

| 필드 | 규칙 |
|------|------|
| `status` | `active`는 진행 의사가 있음, `on-hold`는 잠정 중단, `completed`는 기획한 흐름이 완결됨을 뜻한다. 공백 기간만으로 자동 전환하지 않는다. |
| `started` | 연재를 시작했거나 연재로 관리하기로 결정한 날짜 |
| `ended` | `completed`일 때만 완결일 기록 |
| `last_published` | 최근 글을 실제 발행한 날짜. 새 글 발행 시 갱신하며 초안 작성일로 대신하지 않는다. |
| `next_action` | 진행 중·잠정 중단 연재를 다시 열 때 판단할 한 가지 행동 |

Blog Base는 `last_published` 또는 발행 전 `started`를 기준으로 30일·90일 공백을 표시한다. 이는 점검 신호일 뿐 `on-hold`나 `completed`를 자동 판정하지 않는다.

---

## 📚 Books (`30_Resources/References/Books/`)

이미 잘 표준화되어 있음. 유지 + 마이너 정리.

```yaml
---
created: 2025-08-12 18:40
title: <책 제목>
author:
  - <저자>
publisher: <출판사>
category: 국내도서    # 국내도서 | eBook | 외서
total_page: 400
publish_date: 2020-02-20
cover_url: <yes24 등 이미지 URL>
status: 읽는 중       # 예정 | 읽는 중 | 완독 | 중단
start_read_date: 2025-08-13
finish_read_date: null
my_rate: 0            # 0 ~ 5 (0.1 단위 허용)
book_note: <한줄평>
---
```

> `category`는 `국내도서`·`eBook`·`외서`처럼 도서 형식을 기록한다. 판매처의 세부 분류를 태그로 복사하지 말고 vault의 주제 태그 0~2개만 사용한다.

---

## 🔧 DevLog (`30_Resources/Development/DevLog/`)

회사 업무 맥락을 포함할 수 있는 로컬 개발 기록이다. Git에서는 제외하지만 본인이 작성한 경력·글쓰기 근거이므로 QMD 검색에는 포함한다.

| 폴더 | 역할 | 작성 기준 |
|------|------|-----------|
| `daily/` | 사실과 작업 흐름 | 한 일·오류·명령·임시 판단을 편하게 기록 |
| `weekly/` | 선택적 압축 | 프로젝트별 변화·결정·성과·다음 행동만 요약 |
| `monthly/` | 장기 패턴 | 여러 주를 관통하는 패턴이나 블로그·이직 소재가 있을 때만 작성 |

```yaml
---
date: 2026-03-16
projects:
  - <project-id>      # 20_Projects/ 의 project_id와 매칭
---
```

`projects`는 `20_Projects/`의 canonical `project_id`와 맞춘다. 저장소·모듈·도구 이름을 별도 프로젝트 값으로 만들지 않고, 어떤 결과물을 위한 작업이었는지에 따라 귀속한다. Java·Spring·Kubernetes 같은 기술은 하위 폴더를 만들지 않고 `개발/*` 태그로 표현한다. 날짜에서 벗어나 재사용할 수 있는 문제 해결법은 `30_Resources/Development/Troubleshooting/`으로 분리한다.

---

## 🧠 Development Concepts (`30_Resources/Development/Concepts/`)

공개 가능한 개발 지식 노트다. 개념 설명, 설계 선택을 이해하기 위한 학습 기록, 독립 실험의 결과를 담는다. 프로젝트·조직·운영 맥락을 그대로 보존하는 기록은 여기에 두지 않는다.

```yaml
---
created: 2026-09-06
summary: <노트가 설명하는 개념 또는 학습 질문을 한두 문장으로 요약>
tags:
  - 개발/<기술>
---
```

`created`는 모든 노트의 필수 필드이고 `summary`는 Concepts 노트의 식별 요약이다. `tags`는 여러 폴더를 가로질러 실제로 검색할 기술 주제가 있을 때만 선택적으로 쓴다. 발행 상태를 나타내는 별도 속성은 두지 않으며, 공개 여부는 내용 검토와 공개 대상 목록에서 판단한다.

---

## 📰 Articles & Clippings (`30_Resources/References/Articles/`, `30_Resources/References/Clippings/`)

Clippings는 아래의 공통 속성을 사용한다. Git 추적 카드에는 출처 메타데이터와 확인 가능한 요약만 남기며, 개인 열람용 원문 스냅샷은 Git에서 제외된 `_local-snapshots/`로 분리한다.

```yaml
---
title: <원본 제목>
source: https://...           # 원본 URL (Clipper 자동)
author:
  - <원작자>                   # 기존 Clipper의 wikilink 값도 허용
published: 2024-09-14         # 원본 발행일 (Clipper 자동)
created: 2025-02-10           # vault 수집일 (Clipper 자동)
description: <원문에 근거한 한국어 식별 문장 1~2개> # 평가·시사점 추가 금지
thumbnail: <이미지 URL>       # 선택
status: unread                # unread | read | archived
my_take: ""                   # 내 한 줄 평 (정리 시 작성)
---
```

> Clippings는 **읽기 전 수집함**이며 literature note 자체가 아니다. 원문 제목을 한국어 파일명으로 옮기고, 출처 메타데이터와 원문에 근거한 한국어 식별 문장 1~2개, 저장 맥락을 남긴다. 원문을 충분히 확인했을 때만 핵심 주장·방법·사례를 보존하는 `## 내용 요약` 4~7개를 추가하고, 유료벽·로그인·불완전 추출로 사실 확인이 부족하면 이 섹션을 생략한다. `source`가 원문 URL의 정본이므로 본문의 `## 원문` 링크는 만들지 않는다. 전문·장문 번역은 Git 추적 카드에 넣지 않으며, 개인 열람용 원문은 명시적으로 요청한 경우에만 Git에서 제외된 `Clippings/_local-snapshots/`에 둔다.
>
> 읽은 뒤에는 다음 중 필요한 만큼만 진행한다:
> - 반응이 한 줄이면 `my_take`를 채우고 `status: read`로 유지
> - 인용과 생각을 남길 가치가 있으면 `Articles/`에 별도 literature note를 만들고 clipping을 링크
> - 여러 맥락에 재사용할 내 주장이 생기면 이후 검토에서 `01_Slipbox/` 영구 노트로 승격

> 기존 전문 번역형 Articles는 역사 기록으로 유지한다. `source`와 `status`처럼 확인 가능한 속성만 우선 보강하고, 본문은 실제로 다시 사용할 때만 `literature-note` 기준으로 재정리한다. 새 literature note에는 전문을 복제하지 않는다.

---

## 📅 Periodic Notes (`10_Periodic Notes/`)

```yaml
---
created: 2026-05-27   # 파일명(YYYY-MM-DD)에서 파생, 모든 노트 공통 필드
type: daily           # daily | weekly | monthly (단일 문자열, list 아님)
date: 2026-05-27      # daily: YYYY-MM-DD / weekly: 첫날 / monthly: 1일
week: 2026-W22        # daily/weekly만 (gggg-[W]WW, ISO week)
month: 2026-05        # weekly/monthly만 (YYYY-MM)
tags:
  - type/timeline/daily   # ⚠️ frontmatter tags에 # 금지
---
```

> Templater 템플릿은 `tp.file.title` 기준으로 날짜를 파생시킨다 (백필 시 정확성 확보). `tp.date.now()` 사용 금지.

---

## 🚦 마이그레이션 규칙

1. **신규 노트**: 반드시 위 스키마 따른다. 템플릿(`99_Templates/`)이 자동 적용.
2. **기존 노트**: 발견 시점에 점진적 보강. 빈 필드는 `null` 또는 생략 가능 — 단 **필수 필드는 채워야** Bases 쿼리에서 누락되지 않음.
3. **`40_Archive/`는 스키마 비적용**: 아카이브 노트의 frontmatter(비표준 `status` 등)는 역사 기록으로 그대로 두고 마이그레이션하지 않는다.
4. **스키마 변경**:
   1. 이 문서 먼저 수정
   2. `99_Templates/` 영향 받는 템플릿 동기화
   3. `_*.base` 쿼리 영향 검토
   4. 기존 노트 마이그레이션 또는 폴백 로직 추가

## 연관된 노트
- [[Obsidian 운영 워크플로]] - 사람이 주기적으로 실행하는 vault 운영 흐름
- [[_dashboard]] - Projects base 쿼리
- [[_index]] - Slipbox / Resources base 쿼리
