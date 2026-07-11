---
name: vault-lint
description: 이 스킬은 사용자가 "vault lint", "vault 점검", "죽은 링크 확인", "frontmatter 점검"을 요청하거나 vault 헬스 체크를 언급할 때 사용한다. 기계 검사(고립 노트·죽은 링크·스키마 위반)는 스캐너 스크립트로 수행하고, 승인된 항목만 적용한다. 고립 노트 연결·승격·구조 노트 생성 같은 의미 판단 작업은 review-zettelkasten을 사용한다.
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

이 단계는 스캐너 결과만 사용하며 QMD를 요구하지 않는다. 노트의 의미를 읽어야 하는 연결·승격·구조화 판단은 `review-zettelkasten`으로 넘긴다.

- **연결 공백·MOC 공백 — 탐지·보고만** (적용은 `review-zettelkasten` 위임):
  `slipbox: true`인 고립 노트와, 같은 태그/링크 클러스터에 3+ 노트가 있는데 `type: hub`
  노트가 없는 군집을 리포트에 기록한다. 어떤 노트를 어떻게 연결·구조화할지의 의미 판단과
  적용은 이 스킬에서 하지 않고, 리포트에 "review-zettelkasten으로 처리"를 안내한다.
  (Slipbox 50+ 노트 도달 시 스캐너에 태그 집계 추가를 검토)
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

- 죽은 링크 처치로 링크를 추가·수정할 때는 대상 노트 하단 `## 연관된 노트` 섹션에
  `- [[노트]] - 이유` 형식 (CLAUDE.md 연결 규약). 섹션이 없으면 생성, 있으면 항목 추가.
- 거부 항목: 리포트에 `보류`로 표기해 다음 lint에서 중복 제안을 피한다.

### 7. 마무리

적용 내역을 요약한다. **적용 후 자동 커밋은 하지 않는다** — 커밋 여부는 사용자 판단.

## 경계

- 스키마 기준은 `99_Templates/_property-schema.md`. 스키마가 바뀌면 `scripts/lint_scan.py`
  상단 설정 블록(SCAN_EXCLUDE_TOP / FOLDER_REQUIRED / DATE_INSTEAD_OF_CREATED)만 갱신한다.
- 스캐너 수정 시 `scripts/test_lint_scan.py`를 실행해 회귀를 확인한다.
- Inbox 승격, 대화 캡처는 이 스킬의 비범위다.
- 이 스킬은 **기계적 상태 점검**을 담당한다. 노트의 의미를 읽고 판단하는 연결 제안·승격·
  병합·구조 노트(MOC) 생성은 `review-zettelkasten`이 담당한다. 함께 요청받으면 이 스킬로
  상태를 확인한 뒤 review-zettelkasten으로 넘긴다.
