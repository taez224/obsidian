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
| `tags` | List | ✅ | [[CLAUDE]] 태그 체계 준수. `#` 없이 작성 |
| `aliases` | List | ⬜ | 다른 이름으로도 wikilink 받기 위함 |

---

## 🧠 Slipbox (`01_Slipbox/`)

영구 보관 노트. Zettelkasten 정원 비유로 **성숙도(status)** 를 표현한다.

```yaml
---
created: 2026-01-15
tags:
  - <주제 태그>
  - slipbox
type: permanent       # permanent | literature | fleeting | hub(MOC)
status: seedling      # seedling | growing | evergreen
aliases:
  - <대체 이름>
---
```

| 필드 | 값 | 의미 |
|------|----|----|
| `type: permanent` | 영구 노트 (자기 언어로 정제됨) | 기본값 |
| `type: literature` | 외부 자료 요약 (책/아티클의 정리본) | |
| `type: fleeting` | 단상/스케치 (곧 승격되거나 폐기) | |
| `type: hub` | MOC (Map of Content) | |
| `status: seedling` | 막 심은 씨앗 (< 200자, 연결 0~1개) | |
| `status: growing` | 자라는 중 (내용·연결 추가되는 중) | |
| `status: evergreen` | 성숙 (3+ 연결, 자기 글로 정제됨, 안정적) | |

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
| `project_id` | kebab-case, 폴더명과 일치 |
| `status: active` | 진행 중 — 14일 미수정 시 `_dashboard.base`의 "방치된 프로젝트"에 표시 |
| `status: planning` | 기획 단계 (아직 코드 안 씀) |
| `status: on-hold` | 일시 중단 |
| `status: completed` | 완료 → `40_Archive/`로 이동 검토 |

### 프로젝트 하위 노트 (`20_Projects/<project>/weekly/` 등)

프로젝트 진행 중 생기는 회고·기록 노트. 프로젝트 노트와 달리 `project_id`·`status`를 갖지 않는다.

```yaml
---
created: 2026-02-02
type: weekly-review    # 주간 회고. 다른 하위 노트 타입이 생기면 여기 등재
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
tags:
  - blog
  - <주제 태그>
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

---

## 📚 Books (`30_Resources/References/Books/`)

이미 잘 표준화되어 있음. 유지 + 마이너 정리.

```yaml
---
created: 2025-08-12 18:40
tags:
  - 📚독서
  - <주제 태그>               # 예: AI, 개발/인프라, 글쓰기
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

날짜 기반 일자 노트. 현 스키마 유지.

```yaml
---
date: 2026-03-16
tags:
  - 개발/DevLog
projects:
  - <project-id>      # 20_Projects/ 의 project_id와 매칭
---
```

---

## 📰 Articles & Clippings (`30_Resources/References/Articles/`, `30_Resources/References/Clippings/`)

**Obsidian Web Clipper 호환 포맷** 사용. Clipper가 자동 생성하는 필드를 그대로 활용한다.

```yaml
---
title: <원본 제목>
source: https://...           # 원본 URL (Clipper 자동)
author:
  - "[[원작자]]"               # Clipper는 wikilink로 감쌈
published: 2024-09-14         # 원본 발행일 (Clipper 자동)
created: 2025-02-10           # vault 수집일 (Clipper 자동)
description: <원본 요약>
thumbnail: <이미지 URL>       # 선택
tags:
  - clippings                 # 기본 (Clipper 자동)
  - <주제 태그>                # 수동 추가 (예: 개발/Java, AI)
status: unread                # unread | read | archived
my_take: ""                   # 내 한 줄 평 (정리 시 작성)
---
```

> Clippings는 **literature note**의 일종. 정리 시 다음 둘 중 하나:
> - **승격**: 핵심 인사이트 추출 → `01_Slipbox/` 에 새 permanent 노트 작성, clipping을 링크
> - **참조용 보관**: `my_take` 한 줄만 채우고 `status: read`로 유지

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
  - type/timeline/daily   # ⚠️ frontmatter tags에 # 금지 (CLAUDE.md 규약)
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
- [[CLAUDE]] - 태그 체계 원천
- [[_dashboard]] - Projects base 쿼리
- [[_index]] - Slipbox / Resources base 쿼리
