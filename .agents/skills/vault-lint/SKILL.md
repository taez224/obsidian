---
name: vault-lint
description: 이 스킬은 사용자가 "vault lint", "vault 점검", "슬립박스 점검", "고립 노트 정리", "연결 제안", "죽은 링크 확인", "frontmatter 점검", "주간 정리"를 요청하거나 vault 헬스 체크·노트 연결 개선을 언급할 때 사용한다. 기계 검사(고립 노트·죽은 링크·스키마 위반)는 스캐너 스크립트로, 연결 후보 제안은 qmd 검색으로 수행하고, 승인된 항목만 적용한다.
---

# vault-lint: Vault 헬스 체크 + 승인 기반 개선

핵심 원칙: **자동 적용 0건.** 모든 변경은 후보 제시 → 사용자 승인 → 승인분만 적용.
(근거: LLM 링크 제안의 ~30%는 부적합하다는 실사용 보고 — 제안의 채택 여부는 항상 사람이 결정한다)

## 절차

### 1. 기계 검사 (결정적)

```bash
python3 <skill-base-dir>/scripts/lint_scan.py /Users/taez/Projects/obsidian
```

스캐너는 읽기 전용이며 JSON을 반환한다: `orphans`(고립 노트, `slipbox` 플래그 포함),
`dead_links`(미해석 위키링크), `frontmatter_issues`(스키마 위반), `stats`.
NFC 정규화·alias 해석·`\|` 이스케이프·첨부 임베드를 처리하므로 결과를 재검증할 필요 없음.
의심스러운 항목만 표본 확인한다.

### 2. 판단 검사

qmd MCP가 필요하다. 사용 불가하면 이 단계를 건너뛰고 리포트에 **"degraded mode (기계 검사만)"**를 명시한다.

- **연결 후보** (`slipbox: true`인 고립 노트 대상, 고립이 없으면 out-link 0인 Slipbox 노트로 확대):
  노트 본문을 Read → `mcp__qmd__query`(lex+vec 조합, `intent` 필수) → 상위 후보 노트를
  실제로 읽고 관련성 판단 → **이유를 한 줄로 설명할 수 있는 것만** 노트당 1~3개 제안.
  설명할 수 없으면 제안하지 않는다.
  qmd 후보 중 `_workspace/`·`40_Archive/` 경로는 링크 대상에서 제외한다 (수명 제한·버전
  아카이브 파일). 이미 역링크가 있는 노트로의 수동 역연결도 제안하지 않는다 (Backlinks 패널 규약).
- **MOC 공백**: Slipbox 전체 frontmatter를 직접 읽어, 같은 태그/링크 클러스터에 3+ 노트가
  있는데 `type: hub` 노트가 없으면 MOC 생성을 제안한다. (Slipbox 50+ 노트 도달 시
  스캐너에 태그 집계 추가를 검토)
- **죽은 링크 처치**: 항목별로 "오타 수정 / 스텁 생성 / 링크 제거 / 의도적 placeholder 유지"
  중 하나를 근거와 함께 제안한다. Zettelkasten에서 미해결 링크는 "나중에 쓸 노트" 표시일 수
  있으므로 제거를 기본값으로 하지 않는다.
- **frontmatter 수정**: 제안값이 결정적으로 유도 가능한 항목만 승인 루프에 올린다 —
  `created` 누락은 `git log --diff-filter=A --follow --format=%as -1 -- <file>` 결과로,
  태그의 `#` 포함은 제거로 제안. 유도 불가 항목(type/status/태그 내용)은 리포트 전용.

### 3. 리포트 생성

`_workspace/lint-YYYY-MM-DD/report.md` 에 작성한다 (7일 수명 규약 대상):
요약 통계 → 카테고리별 발견 + 제안(이유 포함) → degraded 여부.
고립 노트는 폴더별로 묶고, 연결 제안은 Slipbox 항목에만 첨부한다.

### 4. 승인

AskUserQuestion(multiSelect)으로 **카테고리별 채택 항목을 선택**받는다.
항목을 일일이 나열해 묻지 말고 "연결 제안 N건 중 채택할 것"처럼 묶는다.

### 5. 체크포인트 커밋

적용 전 `git status` 요약을 고지한다 — 함께 커밋될 무관 변경이 N건 있다면 명시.
vault 관례대로 전체 스냅샷 커밋: `checkpoint: lint 적용 전 스냅샷`.

### 6. 적용

승인 항목만 적용한다.

- 연결 추가: 대상 노트 하단 `## 연결된 노트` 섹션에 `- [[노트]] - 이유` 형식 (CLAUDE.md 연결 규약).
  섹션이 없으면 생성, 있으면 항목 추가.
- 거부 항목: 리포트에 `보류`로 표기해 다음 lint에서 중복 제안을 피한다.

### 7. 마무리

적용 내역을 요약한다. **적용 후 자동 커밋은 하지 않는다** — 커밋 여부는 사용자 판단.

## 경계

- 스키마 기준은 `99_Templates/_property-schema.md`. 스키마가 바뀌면 `scripts/lint_scan.py`
  상단 설정 블록(SCAN_EXCLUDE_TOP / FOLDER_REQUIRED / DATE_INSTEAD_OF_CREATED)만 갱신한다.
- 스캐너 수정 시 `scripts/test_lint_scan.py`를 실행해 회귀를 확인한다.
- Inbox 승격, 대화 캡처는 이 스킬의 비범위다.
