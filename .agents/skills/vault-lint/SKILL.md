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
`dead_links`(미해석 위키링크), `frontmatter_issues`(스키마 위반),
`base_issues`(`.base` 파일의 미인식 키 — 현재는 `sortBy`, 실제 Bases 스키마엔 없고 `sort` 리스트가 맞음), `stats`,
`periodic_placeholders`(Periodic Notes의 의도된 날짜·주차·월 링크),
`series_placeholders`(진행 중·잠정 중단 시리즈 허브의 예정 글 링크),
`priorities`(기계 수정 후보 / 의미 검토 후보 / 정보성 항목 수).
`stats.reuse`는 블로그→Slipbox 고유 링크, 해당 블로그 수, 재사용된 Slipbox 수를 관찰용으로 제공한다. 목표 비율이나 품질 점수로 해석하지 않는다.
NFC 정규화·alias 해석·`\|` 이스케이프·첨부 임베드를 처리하므로 스캐너 결과를 기계 검사 후보의 기준으로 사용한다. 다만 실제 수정 전에는 영향받는 파일과 예상 밖 결과를 표본 확인해 스키마 드리프트나 파서 한계를 점검한다.

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
- **Periodic placeholder**: `10_Periodic Notes/`의 날짜·주차·월 패턴 미해결 링크는 전체
  `dead_links`에는 보존하되 `meaning_review`에서 제외하고 `informational`로만 보고한다.
- **Series placeholder**: `type: series`이고 `status`가 `completed`가 아닌 허브의 미해결 링크는
  예정 글로 보고 전체 `dead_links`에는 보존하되 `meaning_review`에서 제외한다. 완결 시리즈의
  미해결 링크는 오타·누락 가능성이 있으므로 기존처럼 의미 검토 대상으로 남긴다.
- **frontmatter 수정**: 제안값이 결정적으로 유도 가능한 항목만 승인 루프에 올린다 —
  `created` 누락은 `git log --diff-filter=A --follow --format=%as -1 -- <file>` 결과로,
  태그의 `#` 포함은 제거로 제안. 유도 불가 항목(type/status/태그 내용)은 리포트 전용.
- **base 파일 미인식 키**: 결정적으로 치환 가능하다 — `sortBy: {property: X, direction: Y}`를
  `sort:` 리스트(`- property: X` / `  direction: Y`)로 바꾸는 수정을 제안한다. 자동 적용은 아니고
  승인 후 적용.

### 3. 리포트 생성

`_workspace/lint-YYYY-MM-DD/report.md` 에 작성한다 (7일 수명 규약 대상):
우선순위 요약(`mechanical` → `meaning_review` → `informational`) → 카테고리별 발견 + 제안(이유 포함) → degraded 여부.
고립 노트는 폴더별로 묶고, 연결 제안은 Slipbox 항목에만 첨부한다.
`stats.reuse`는 현재 상태를 관찰하는 참고값으로만 표시하고 목표치·합격 조건·수정 후보를 만들지 않는다.

### 4. 승인

현재 런타임의 사용자 입력 도구로 **카테고리별 채택 항목을 선택**받는다. 다중 선택을 지원하지 않으면 대화에서 승인 범위를 요청한다. 항목을 일일이 나열해 묻지 말고 "frontmatter 수정 N건", "죽은 링크 처치 N건"처럼 묶되, 실제 적용 대상은 사용자가 식별할 수 있게 리포트에 남긴다.

### 5. 체크포인트 커밋 판단

- 적용 전 `git status`를 확인하고 기존 변경과 이번 lint 대상 변경을 구분해 고지한다.
- 소수의 결정적 수정은 체크포인트 커밋 없이 적용한다.
- 큰 정리 작업은 `AGENTS.md` 규약에 따라 체크포인트가 필요하다. 커밋 대상과 메시지를 보여주고 **별도 승인을 받은 뒤에만** 생성한다.
- 무관 변경은 기본적으로 체크포인트에 포함하지 않는다. 분리할 수 없으면 사용자가 전체 스냅샷을 명시적으로 승인하기 전까지 큰 정리 적용을 중단한다.

### 6. 적용

승인 항목만 적용한다.

- 죽은 링크 처치로 링크를 추가·수정할 때는 대상 노트 하단 `## 연관된 노트` 섹션에
  `- [[노트]] - 이유` 형식 (`AGENTS.md` 연결 규약). 섹션이 없으면 생성, 있으면 항목 추가.
- 거부 항목: 리포트에 `보류`로 표기해 다음 lint에서 중복 제안을 피한다.

### 7. 마무리

적용 내역을 요약한다. **적용 후 자동 커밋은 하지 않는다** — 커밋 여부는 사용자 판단.

## 경계

- 스키마 기준은 `99_Templates/_property-schema.md`. 스키마가 바뀌면 `scripts/lint_scan.py`
  상단 설정 블록(SCAN_EXCLUDE_TOP / FOLDER_REQUIRED / DATE_INSTEAD_OF_CREATED / BASE_INVALID_KEYS)만
  갱신한다. `.base` 파일에서 새로운 미인식 키를 발견하면 `BASE_INVALID_KEYS`에 추가한다.
- 스캐너 수정 시 `scripts/test_lint_scan.py`를 실행해 회귀를 확인한다.
- Inbox 승격, 대화 캡처는 이 스킬의 비범위다.
- 이 스킬은 **기계적 상태 점검**을 담당한다. 노트의 의미를 읽고 판단하는 연결 제안·승격·
  병합·구조 노트(MOC) 생성은 `review-zettelkasten`이 담당한다. 함께 요청받으면 이 스킬로
  상태를 확인한 뒤 review-zettelkasten으로 넘긴다.
