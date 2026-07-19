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
30_Resources/         Development (DevLog, Troubleshooting, Tools) + References
40_Archive/           완료·보관
99_Templates/         노트 템플릿 + property schema
```

작업 경계·태그·연결 규칙은 **[AGENTS.md](AGENTS.md)** 를, 사람이 반복할 운영 흐름은 [Obsidian 운영 워크플로](<30_Resources/Obsidian 운영 워크플로.md>)를 따른다. `CLAUDE.md`는 호환을 위한 심볼릭 링크다.

## 🔄 워크플로우

```
오늘의 기록 ───────────────→ 10_Periodic Notes
개인 단상 ────────────────→ 00_Inbox ─────┐
외부 자료 ────────────────→ 30_Resources ─┴─ 주간 검토 → 삭제 / 보관 / Project 흡수 / Slipbox 승격
완료할 결과물 ────────────→ 20_Projects
```

- **매일**: 필요한 기록만 Daily Note 또는 Inbox에 포착. 같은 내용은 이중 기록하지 않음
- **주간**: Inbox와 실제로 읽은 Resources를 삭제·보관·Project 흡수·Slipbox 승격으로 라우팅하고, `_global-health.base`의 큰 부채만 점검
- **월간**: MOC 필요성, 프로젝트 상태, Slipbox의 실제 재사용과 성숙도 검토

> 실제 사용 방법과 AI 스킬의 역할은 [Obsidian 운영 워크플로](<30_Resources/Obsidian 운영 워크플로.md>)를 참조하세요.

## 📊 Bases 대시보드

| Base | 위치 | 용도 |
|------|------|------|
| `_global-health.base` | vault root | Inbox 부채, 고립 Slipbox, 프로젝트 허브 미갱신, 오래된 Clippings |
| `_inbox.base` | `00_Inbox/` | 정리 부채 (7일+/30일+ 체류), 분류 도우미 |
| `_index.base` | `01_Slipbox/` | 고립 노트, 허브 노트, 연결 분석 |
| `_dashboard.base` | `20_Projects/` | 프로젝트 상태, 진행 중, 프로젝트 허브 미갱신 |
| `_index.base` | `20_Projects/blog/` | 초안·발행 글, 연재 상태, 장기 발행 공백 점검 |
| `_index.base` | `30_Resources/` | 도서 평점·메타데이터, 읽기 대기 Clippings, DevLog, 자주 참조됨 |

## 📐 노트 작성 표준

**모든 frontmatter는 [99_Templates/_property-schema.md](99_Templates/_property-schema.md) 를 따른다.**

타입별 필수 필드:

- **Slipbox**: `created`, `tags`, `type` (`permanent`/`fleeting`/`hub`), `status` (`seedling`/`growing`/`evergreen`)
- **Project**: `created`, `title`, `project_id`, `status` (`active`/`on-hold`/`completed`/`planning`), `started`
- **Blog Series**: `created`, `title`, `type: series`, `status` (`active`/`on-hold`/`completed`), `started`, `last_published`, `next_action`
- **Book**: `created`, `title`, `author`, `category`, `status`, `my_rate`, `start_read_date`, `finish_read_date`
- **DevLog**: `date`, `tags`, `projects[]` — `daily/weekly/monthly`에 로컬 보관

## 🛠️ 권장 플러그인

- **Templater** — 동적 템플릿
- **Periodic Notes** — 일/주/월간 자동 생성
- **QuickAdd** — 빠른 캡처
- **Obsidian Git** — GitHub 백업
- **Tasks** — 체크박스 태스크 집계
- **Smart Connections** — Obsidian 안에서 연관 노트 탐색 (에이전트의 정밀 검색은 QMD)

## 🔗 참고

- [PARA 방법론](https://fortelabs.co/blog/para/)
- [Zettelkasten 방법론](https://zettelkasten.de/)
- [Obsidian Bases 공식 문서](https://help.obsidian.md/bases)
