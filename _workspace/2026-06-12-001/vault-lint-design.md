# vault-lint 스킬 디자인 스펙

- 날짜: 2026-06-12
- 상태: 승인됨 (대화에서 섹션별 합의)
- 배경: AI-Zettelkasten 사례 분석(claude-obsidian wiki-lint, Karpathy LLM Wiki lint 패턴)에서 추출.
  이 vault는 base 대시보드로 "탐지"는 갖췄으나 "실행"(연결 제안·수정 적용)이 없다는 갭을 메운다.

## 목표

vault 헬스 문제를 결정적으로 스캔하고, 판단이 필요한 개선(연결 제안·MOC 생성·죽은 링크 처리)을
**후보로 제시 → 사용자 승인 → 승인분만 적용**하는 스킬. 자동 적용 0건이 설계 원칙
(사례 경고: "LLM 링크 제안의 ~30%는 부적합").

## 구성 요소

```
.agents/skills/vault-lint/
  SKILL.md                  # 스킬 본문
  scripts/lint_scan.py      # 기계 검사 스캐너 (Python 3 stdlib만)
.claude/skills/vault-lint   # → ../../.agents/skills/vault-lint 심링크 (qmd 스킬과 동일 컨벤션)
```

리포트: `_workspace/lint-YYYY-MM-DD/report.md` (vault의 7일 수명 규약 적용 대상).

## 1) lint_scan.py — 기계 검사 (결정적, 읽기 전용)

- 대상: vault 전체 `.md`. 제외: `40_Archive/`, `99_Templates/`, `_workspace/`, `_attachments/`, dotfolder, `_`로 시작하는 파일
- 출력: JSON to stdout `{stats, orphans[], dead_links[], frontmatter_issues[]}`
- 파일 수정 절대 금지

검사 항목:

| 검사 | 규칙 |
|------|------|
| 고립 노트 | 위키링크 그래프에서 in+out 링크 0. `01_Slipbox/` 소속이면 `slipbox: true` 플래그 (CLAUDE.md "최소 1개 링크" 규칙 위반으로 격상) |
| 죽은 링크 | `[[대상]]`이 어떤 파일과도 매칭 안 됨. `[[노트\|표시명]]`·`[[노트#헤딩]]`·`![[임베드]]` 파싱, 코드블록 내 링크 제외. **링크 해석 집합은 vault 전체** — 파일명(경로 포함/미포함 모두) + 모든 노트의 frontmatter `aliases` 값. 검사 "대상" 노트만 제한하고 해석 집합은 Archive/Templates 포함 전체로 구축 (Archive로 향하는 링크는 살아있는 링크). 해석 집합은 **모든 확장자 포함** — `![[img.png]]` 같은 첨부 임베드가 .md 전용 집합에서 오탐되는 것 방지. 비교 전 양쪽 모두 `unicodedata.normalize('NFC', s)` 적용 (실측: 디스크에 NFD 파일명 1건 존재, 에이전트 셸 작성 경로로 유입 가능) |
| frontmatter 위반 | (a) frontmatter 블록 부재 (b) 공통 필수 `created`/`tags` 누락 (c) tags 항목에 `#` 포함 (d) 폴더별 필수 필드 누락 — Slipbox: `type`/`status`, Clippings: `status`. Projects는 **`project_id`가 있는 노트만** `status` 검증 (blog 초안 등 비프로젝트 파일 오탐 방지). 기준: `99_Templates/_property-schema.md` |

스키마가 바뀌면 스크립트의 폴더별 규칙 테이블만 갱신하면 된다 (스크립트 상단 상수로 분리).

## 2) SKILL.md — 판단 검사 + 승인 루프 (Claude)

판단 검사 (Slipbox 집중):

- **연결 후보**: 스캐너의 Slipbox 고립 노트마다 — 노트 본문 Read → `mcp__qmd__query`(lex+vec, intent 포함) → 상위 후보를 실제로 읽고 관련성 판단 → **이유를 한 줄로 설명할 수 있는 것만** 노트당 1~3개 제안. 형식은 CLAUDE.md 연결 섹션 규약: `- [[노트]] - 이유`
- **MOC 공백**: 같은 태그/링크 클러스터에 3+ 노트가 있는데 `type: hub` 노트가 없으면 MOC 생성 제안
- **죽은 링크 처치 제안**: 항목별로 "오타 수정 / 스텁 생성 / 링크 제거 / 의도적 placeholder로 유지" 중 하나를 근거와 함께 제안 (Zettelkasten에서 미해결 링크는 "나중에 쓸 노트" 표시일 수 있음)
- **frontmatter 수정 제안**: 제안값이 결정적으로 유도 가능한 항목만 승인 루프에 포함 — `created` 누락은 git 최초 커밋일(`git log --diff-filter=A --format=%as -1 -- <file>`)로 제안, tags의 `#` 포함은 제거 제안. 유도 불가능한 항목(태그 내용, type/status 값 등)은 리포트 전용
- **MOC 클러스터 판단의 데이터 소스**: 현 규모(Slipbox 8개)에서는 Claude가 Slipbox frontmatter를 직접 읽어 판단. 스캐너 태그 집계는 추가하지 않음 (YAGNI) — Slipbox 50+ 노트가 되면 재검토

실행 플로우:

1. `lint_scan.py` 실행 → JSON 파싱
2. 판단 검사 수행 (qmd MCP 불능 시: 연결 제안 스킵, 기계 검사만 — degraded mode를 리포트에 명시)
3. `_workspace/lint-YYYY-MM-DD/report.md` 생성 (요약 통계 + 카테고리별 발견 + 제안)
4. 카테고리별로 묶어 승인 질문 (AskUserQuestion, multiSelect — 항목 나열이 아닌 채택 선택)
5. 적용 전 체크포인트 커밋 — vault 관례(`checkpoint: ...` 스냅샷 커밋)대로 전체 트리 스냅샷. 커밋 전 `git status` 요약(함께 커밋될 무관 변경 N건)을 고지하고 진행
6. 승인 항목만 적용. 거부 항목은 리포트에 `보류`로 기록
7. 적용 후 자동 커밋 없음 (사용자 판단)

트리거: "vault lint", "vault 점검", "슬립박스 점검", "고립 노트 정리", "연결 제안", "주간 정리" 류.

## 비범위 (명시적 제외)

- index.md/log.md 장부 (git + devlog 스킬이 대체)
- hot cache 세션 메모리 (Claude Code 메모리가 대체)
- 임베딩 중복 탐지 (qmd가 이미 수행)
- inbox 승격·대화 캡처 (별도 스킬 후보로 보류)

## 검증 계획

1. 스캐너 단독 실행 → JSON 구조 확인
2. 고립 노트 결과를 `_global-health.base`/`01_Slipbox/_index.base` 대시보드와 교차 대조
3. 죽은 링크 표본 3건 수동 확인 (실제 부재 여부)
4. 스킬 전체 1회 실행 → 리포트 생성·승인 루프·적용까지 엔드투엔드 확인
