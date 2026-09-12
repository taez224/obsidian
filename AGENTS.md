# Agent Instructions

## 저장소와 정본

이 저장소는 PARA와 Zettelkasten을 사용하는 Obsidian vault다. 사이트 코드는 별도 `taez224.github.io` 저장소에서 관리한다.

| 위치 | 역할 |
| --- | --- |
| `00_Inbox/` | 개인 단상의 빠른 포착 |
| `01_Slipbox/` | 독립적으로 재사용할 자기 주장 |
| `10_Periodic Notes/` | 날짜별 기록과 일정 |
| `20_Projects/` | 프로젝트 목표·현재 상태·산출물 |
| `30_Resources/` | 외부 자료와 개발 지식 |
| `40_Archive/` | 완료·보관 자료 |
| `99_Templates/` | 속성 규칙과 작성 안내 |

- 위치·운영 주기는 [Obsidian 운영 워크플로](<30_Resources/Obsidian 운영 워크플로.md>)가 정본이다.
- 속성·summary·slug·태그·연결 기준은 [속성 스키마](99_Templates/_property-schema.md)가 정본이다. 작성할 때 공통 필드와 해당 노트 유형의 절을 읽는다.
- 현재 목표와 판단 근거는 `20_Projects/<project-id>/<project-id>.md`에서 확인한다. 소스와 DevLog를 프로젝트 폴더에 복제하지 않는다.
- 모든 문서를 미리 읽지 않는다. 현재 작업의 스킬을 읽고, 거기서 참조한 정본의 필요한 절로 이동한다.

## 작업별 진입점

Obsidian Markdown을 만들거나 수정할 때는 아래 작업 스킬과 [obsidian-markdown](.agents/skills/obsidian-markdown/SKILL.md)을 함께 읽는다.

| 요청 | 먼저 읽을 스킬 |
| --- | --- |
| 개인 생각을 빠르게 저장 | [capture-fleeting-note](.agents/skills/capture-fleeting-note/SKILL.md) |
| 아직 읽지 않은 URL·자료 보관 | [capture-reference-card](.agents/skills/capture-reference-card/SKILL.md) |
| 읽은 자료와 내 반응 정리 | [literature-note](.agents/skills/literature-note/SKILL.md) |
| 영구 노트 작성·승격 명시 | [permanent-note](.agents/skills/permanent-note/SKILL.md) |
| 노트 연결·병합·분리·MOC 검토 | [review-zettelkasten](.agents/skills/review-zettelkasten/SKILL.md) |
| 질문으로 생각 검토 | [socratic-dialogue](.agents/skills/socratic-dialogue/SKILL.md) |
| 개발 개념·설계·문제 해결 기록 | [development-note](.agents/skills/development-note/SKILL.md) |
| 프로젝트 상태·근거·허브 갱신 | [sweep-project-context](.agents/skills/sweep-project-context/SKILL.md) |
| 사이트 작업을 노트 이력에 반영 | [sweep-site-worklog](.agents/skills/sweep-site-worklog/SKILL.md) |
| 블로그 구성·작성·발행 검토 | [taez-insight-blog-writer](.agents/skills/taez-insight-blog-writer/SKILL.md) |
| 속성·죽은 링크·vault 점검 | [vault-lint](.agents/skills/vault-lint/SKILL.md) |
| 정확 검색·의미 검색 | [qmd](.agents/skills/qmd/SKILL.md) |

캡처 요청이 겹치면 **영구 노트·승격 명시 → 외부 자료의 읽음 여부 → 개인 단상** 순서로 판단한다. 외부 자료를 아직 읽지 않았다면 자료카드, 읽고 반응을 남기려 한다면 참고노트로 처리한다. URL이 생각의 출처일 뿐 저장 대상은 개인 단상이라면 Quick Capture로 남긴다.

## 핵심 경계

- 단순 메모를 영구 노트로 승격하지 않는다. 외부 자료의 요약과 자기 주장을 구분한다. Quick Capture의 `AI 생성`은 사용자의 주장이나 검증된 자료가 아니며 명시적 채택 없이 영구 노트로 옮기지 않는다.
- 개발 지식은 Concepts, 재현 가능한 해결법은 Troubleshooting, 특정 도구 사용법은 Tools다. 설계 판단은 도구 이름이 있어도 Concepts에 둔다. `Development/` 바로 아래에는 노트를 만들지 않는다.
- 시간순 업무 기록은 중앙 DevLog에 두고 `projects`에는 canonical project_id를 쓴다. 기술은 폴더 대신 기술 태그로 표현한다. 세부 기준은 운영 워크플로의 개발 노트 절을 따른다.
- 블로그 전문은 `20_Projects/blog/`에 한 번만 둔다. Slipbox에는 독립 주장만 남긴다. 연재 작업은 해당 연재 허브와 [블로그 운영 기준](20_Projects/blog/blog.md)을 먼저 읽는다.
- 공개 여부를 자동으로 확대하지 않는다. 공개하기로 한 경험·해석은 유지하되 비공개 정보는 제외한다. 새 공개 노트에는 slug를 정하고, 이미 공개한 주소는 임의로 바꾸지 않는다.
- 관계를 설명할 수 없는 링크는 억지로 만들지 않는다. 링크 수만으로 성숙도를 올리지 않는다. 연결 형식은 속성 스키마를 따른다.

## 승인과 편집

- 삭제·이동·승격·병합·MOC 생성·공개 범위 변경·커밋·push는 사용자 승인 후 적용한다. 이미 승인된 범위는 다시 묻지 않는다. 승인 전 의미 변경 작업은 후보 보고까지 완료로 본다.
- 편집 직전에 현재 내용을 다시 읽고 해당 부분만 고친다. 다른 세션과 Obsidian의 변경을 덮어쓰지 않는다. 요청 밖에서 발견한 개선은 이번 변경에 섞지 않고 제안으로만 알린다.
- 커밋 제목은 `type(scope): 명사형 제목` 형식으로 쓰고 한국어 명사형으로 짧게 끝낸다. "~한다"가 아니라 "~ 추가", "~ 갱신", "~로 변경" 등. `type`은 `feat`, `fix`, `refactor`, `docs`, `chore`, `test`, `style`, `ci`이고, `scope`는 바뀐 영역 이름(`vault`, `dev`, `blog`, `slipbox`, `vault-lint` 등)이며 닫힌 목록이 아니다. 예: `docs(dev): 트러블슈팅 제목을 상황형으로 변경`, `chore(vault-lint): 개발 노트 속성 검사 추가`.
- 큰 정리 전에는 승인된 체크포인트 커밋이 필요하다. 무관한 변경을 임의로 포함하지 않는다. 파일명 버전 대신 Git을 사용하고 블로그 반복 초안은 승인 후 `40_Archive/blog-drafts/`로 보관한다.
- 일반 첨부는 `_attachments/`, 프로젝트 전용 에셋은 폴더 로컬 `assets/`에 둔다. 루트에는 `CLAUDE.md`, `AGENTS.md`, `README.md`, `_global-health.base` 외의 작업 파일을 만들지 않는다.

## 글쓰기

한국어 노트·글·보고는 [공통 글쓰기 기준](.agents/guides/writing.md)을 따른다. 짧게 쓰되 조사·어미와 의미를 생략하지 않는다. 장르와 종결체는 사용자 요청과 작업 스킬을 따른다.

## 검색과 확인

- 정확한 제목·파일명·문자열은 `rg`, 간접적인 개념·주장은 QMD MCP `query`로 찾는다. 중요한 판단은 후보 원문을 읽고 내린다. Codex의 샌드박스 CLI에서 Metal 오류가 난 의미 검색을 반복하지 않는다.
- `_workspace/`, `40_Archive/`, `30_Resources/References/Clippings/_local-snapshots/`는 연결 후보에서 제외한다. 검색 작성법과 재색인은 qmd 스킬을 따른다. 수동 재색인은 명시적으로 요청받았을 때만 수행한다.

## 위임과 생각거리

- 노트 작성·수정과 의미 판단은 주 에이전트가 직접 한다. 하위 에이전트는 읽기 전용 조사·검증만 맡는다. Codex는 `luna_worker`, Claude Code는 Agent 도구를 사용한다.
- 서로 범위가 겹치지 않는 독립 조사·검증이 둘 이상일 때만 병렬로 나누고, 각 위임에 읽을 폴더·기대 결과·검증 방법을 명시한다. 결과는 근거와 후보이지 사용자 승인이 아니다.
- 현재 자료에서 직접 드러난 판단 변화·모순·재사용할 주장만 요청 완료 후 생각거리 하나로 짧게 알릴 수 있다. 이를 위한 추가 검색은 하지 않는다. 넘긴 생각거리는 저장하거나 독촉하지 않는다. 문답은 socratic-dialogue, 노트 발전 후보는 review-zettelkasten을 따른다.

## 지침 관리

- 공통 진입점은 이 파일이다. [CLAUDE.md](CLAUDE.md)는 `@AGENTS.md`로 가져온 뒤 Claude 전용 지침만 덧붙인다. 상세 운영·속성·절차는 각 정본에서 수정한다.
- 스킬 정본은 `.agents/skills/<skill-name>/`다. Codex는 직접 읽으므로 `.codex/skills/`에 링크하지 않는다. Claude는 `.claude/skills/`에 상대 심볼릭 링크를 둔다.
- `defuddle`, `json-canvas`, `obsidian-bases`, `obsidian-cli`, `obsidian-markdown`은 Claude의 obsidian-skills 플러그인과 이름이 겹치므로 Claude 링크를 만들지 않는다. `.agents/skills/`의 해당 사본은 Codex용이다.
- 공통 SKILL.md와 도구별 실행 설정을 분리한다. Claude 전용 실행 설정은 `.claude/workflows/`, Codex 전용 설정은 `.codex/`에 둔다.

## 검증 명령

노트의 의미와 공개 여부는 기계 검사의 통과만으로 승인하지 않는다. 문체 경고도 자동 수정하지 않는다.

```bash
python3 .agents/scripts/check_guides.py
python3 .agents/skills/vault-lint/scripts/test_lint_scan.py
# vault 전체 점검 요청 시 읽기 전용 JSON 보고서 생성
python3 .agents/skills/vault-lint/scripts/lint_scan.py .
```

Git 훅 `.agents/hooks/post-commit`은 Markdown 변경 커밋 후 QMD를 갱신한다. lint나 배포의 성공을 뜻하지 않는다. 사이트 코드·배포 검증은 별도 사이트 저장소의 AGENTS.md를 따른다.
