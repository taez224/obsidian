# permanent-note 스킬 디자인 스펙

- 날짜: 2026-07-03
- 상태: 설계 승인됨 (대화에서 합의), 사용자 스펙 리뷰 대기
- 배경: 사용자 본인의 메모를 제텔카스텐 permanent note로 만드는 스킬.
  입력이 이미 사용자 자신의 언어이므로 "재진술" 요건이 입력 시점에 충족되고,
  AI 기여분은 별도 섹션에 격리되어 원문과 섞이지 않는다 — permanent 정체성 유지.

## 목표

사용자가 메모(생각, 단상)를 입력하면 `01_Slipbox/`에 스키마 준수 permanent 노트를
생성하고, 완료 시 Obsidian에서 열어준다. 외부 자료 정제(clipping 승격)는 비범위.

## 구성 요소

```
.agents/skills/permanent-note/
  SKILL.md                      # 스킬 본문 (스크립트 없음 — 전부 판단 작업)
.claude/skills/permanent-note   # → ../../.agents/skills/permanent-note 심링크
```

vault-lint/qmd 스킬과 동일 컨벤션. 번들 스크립트는 두지 않는다:
결정적·반복적 작업이 없고 (제목 요약, 교정, 연관 판단 모두 LLM 판단 영역),
필요해지면 그때 추가한다.

## 동작 플로우

1. **입력 수신**: 사용자 메모 (대화에 직접 입력 또는 스킬 인자)
2. **제목 생성**: 메모를 짧게 한 문장으로 요약 → 노트 제목 = 파일명.
   - 파일명 금지 문자 `/ \ : # ^ [ ] |` 는 제거 또는 자연스러운 대체
   - 기존 파일명과 충돌 시 사용자에게 확인 (덮어쓰기 금지)
3. **frontmatter**: `99_Templates/_property-schema.md` Slipbox 규격
   ```yaml
   created: <오늘 YYYY-MM-DD>
   tags:
     - <태그 체계(CLAUDE.md)에서 추론한 주제 태그>
     - slipbox
   type: permanent
   status: seedling
   ```
4. **본문 생성** (헤딩은 h2, CLAUDE.md 규약과 통일):
   - `## 원문` — 입력 메모를 오타·비문만 교정해 작성. **내용·논지·어휘 선택 변경 금지**
     (원문은 사용자의 언어여야 permanent 정체성이 유지된다)
   - `## AI 생성` — 보충 설명, 반례, 확장 아이디어, 추천 자료 등.
     AI 기여분임이 섹션 제목으로 명시되는 유일한 구역
   - `## 연관된 노트` — `mcp__qmd__query`(lex+vec 조합, intent 포함)로 후보 검색
     → 상위 후보를 실제로 Read → 관련성 판단 → 다음 형식으로 작성:
     `- [[노트명]] - 어떤 맥락에서 연관되는지 (한 줄)`
     **이유를 한 줄로 설명할 수 있는 것만** 포함 (LLM 링크 제안 ~30% 부적합 —
     vault-lint와 동일 원칙). 적합한 후보가 없으면 섹션은 만들되 빈 리스트 대신
     "아직 연관 노트 없음"을 남기고, 사용자에게 알린다 (Slipbox 최소 1링크
     규칙 위반 상태임을 명시 — 이후 vault-lint가 감시)
5. **완료 후**: `obsidian open` CLI로 생성 노트 열기
   (`obsidian:obsidian-cli` 스킬 명령 활용, CLI 부재 시 경로만 안내하는 degraded mode)

## 트리거

"permanent note 만들어줘", "메모 정리해서 슬립박스에", "제텔카스텐 노트로",
"슬립박스에 추가", "영구 노트 생성" 류. 외부 자료(URL, 클리핑) 정제 요청은
이 스킬 대상이 아님 — 그 경우 별도 승격 워크플로우(추후 스킬 후보).

## 비범위 (명시적 제외)

- Clipping/외부 원문 정제 및 승격 (별도 스킬 후보)
- 기존 노트 수정·연결 보강 (vault-lint 영역)
- qmd 인덱스 갱신 (qmd 스킬 영역)

## 검증 계획

1. 실제 메모 1건으로 엔드투엔드 실행 → 파일 위치·frontmatter·헤딩 구조 확인
2. 생성 노트가 `_property-schema.md` Slipbox 규격 통과하는지 확인
   (vault-lint 스캐너 frontmatter 검사로 교차 검증 가능)
3. 연관 노트 링크가 실존 노트를 가리키는지 확인 (죽은 링크 0)
4. `obsidian open`으로 노트가 실제로 열리는지 확인
