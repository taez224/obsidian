# 🧠 Second Brain — Obsidian Vault

> 개발자를 위한 개인 지식 관리 시스템 (PARA + Zettelkasten + Obsidian Bases)

이 vault는 학습·프로젝트·독서·개발 일지를 한 곳에서 축적하고 자동 집계하는 개인 지식 베이스입니다.

---

## 📂 폴더 구조

```
00_Inbox/             빠른 캡처 (주간 정리)
01_Slipbox/           영구 노트 (Zettelkasten)
10_Periodic Notes/    Daily / Weekly / Monthly
20_Projects/          진행 중인 프로젝트
30_Resources/         Development (DevLog, Tools) + References (Books, Articles, Clippings)
40_Archive/           완료·보관
99_Templates/         노트 템플릿 + property schema
```

자세한 구조·태그 체계·연결 규칙은 **[CLAUDE.md](CLAUDE.md)** 가 single source of truth입니다.

## 🔄 워크플로우

```
Daily / 캡처 → 00_Inbox → (주간 정리) → 01_Slipbox 또는 30_Resources
                              ↓
                    20_Projects (진행 중 학습은 병기)
```

- **매일**: Daily Note + Inbox 캡처
- **주간**: Inbox → Slipbox/Resources 승격, `_global-health.base` 점검
- **월간**: MOC 필요성, 프로젝트 상태, Slipbox 성숙도(`seedling → growing → evergreen`) 검토

> 실제 사용 방법과 AI 스킬의 역할은 [[Obsidian 운영 워크플로]]를 참조하세요.

## 📊 Bases 대시보드

| Base | 위치 | 용도 |
|------|------|------|
| `_global-health.base` | vault root | Inbox 부채, 고립 Slipbox, stale 프로젝트 등 vault 헬스 |
| `_inbox.base` | `00_Inbox/` | 정리 부채 (7일+/30일+ 체류), 분류 도우미 |
| `_index.base` | `01_Slipbox/` | 고립 노트, 허브 노트, 연결 분석 |
| `_dashboard.base` | `20_Projects/` | 프로젝트 상태, 방치된 프로젝트, 최근 활동 |
| `_index.base` | `30_Resources/` | 도서 평점, DevLog, 자주 참조됨 |

## 📐 노트 작성 표준

**모든 frontmatter는 [99_Templates/_property-schema.md](99_Templates/_property-schema.md) 를 따른다.**

타입별 필수 필드:

- **Slipbox**: `created`, `tags`, `type` (`permanent`/`literature`/`fleeting`/`hub`), `status` (`seedling`/`growing`/`evergreen`)
- **Project**: `created`, `title`, `project_id`, `status` (`active`/`on-hold`/`completed`/`planning`), `started`
- **Book**: `created`, `title`, `author`, `category`, `status`, `my_rate`, `start_read_date`, `finish_read_date`
- **DevLog**: `date`, `tags`, `projects[]`

## 🛠️ 권장 플러그인

- **Templater** — 동적 템플릿
- **Periodic Notes** — 일/주/월간 자동 생성
- **QuickAdd** — 빠른 캡처
- **Obsidian Git** — GitHub 백업
- **Tasks** — 체크박스 태스크 집계
- **Smart Connections** — AI 임베딩 기반 의미 검색

## 🔗 참고

- [PARA 방법론](https://fortelabs.co/blog/para/)
- [Zettelkasten 방법론](https://zettelkasten.de/)
- [Obsidian Bases 공식 문서](https://help.obsidian.md/bases)
