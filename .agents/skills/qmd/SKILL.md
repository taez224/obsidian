---
name: qmd
description: Bootstrap QMD search instructions from the installed qmd CLI, plus this vault's canonical note-search procedure (rg vs QMD MCP routing, structured query guidance, reindexing). Use when users ask to find notes, retrieve documents, inspect a wiki, or answer from indexed local markdown.
license: MIT
allowed-tools: Bash(qmd:*), mcp__qmd__*
---

# QMD - Query Markdown Documents

이 스킬이 vault 노트 검색 절차의 **정본**이다. `AGENTS.md`의 "노트 검색"에는 라우팅 경계만 남기고, 실행 상세는 여기에 둔다. 아래 `qmd skill show`가 로드하는 generic CLI 지침보다 이 문서의 라우팅이 우선한다.

## 검색 라우팅

- 정확한 제목·파일명은 `rg --files | rg "<제목>"`, 본문의 정확한 문자열·부분 문자열은 `rg -n -F "<표현>"`을 우선한다. `rg`는 항상 현재 파일을 그대로 읽어 재인덱싱 지연이 없고 문자 그대로 매칭돼 랭킹 노이즈가 없다. 한국어 부분 문자열·제목은 BM25 토큰화 영향을 피하도록 특히 `rg`를 우선한다.
- 개념·주장·간접 표현은 `intent / lex / vec / hyde`를 직접 작성한 QMD structured query를 사용한다. `lex`는 정확한 앵커로만 쓰고 의미 탐색은 `vec / hyde`를 중심으로 한다.
- CLI `qmd search`는 모델을 실행하지 않는 lexical 검색이라 Codex 샌드박스에서도 사용할 수 있다.
- **Codex 의미 검색은 QMD MCP `query`로 실행한다.** 기본 셸 샌드박스의 CLI `qmd query`·`vsearch`·`embed`는 macOS Metal 컨텍스트 생성에 실패할 수 있다. 같은 명령을 반복하지 말고 MCP를 사용하며, MCP를 쓸 수 없을 때만 사용자 승인 후 샌드박스 밖 CLI 실행을 요청한다.

## 탐색 목적에 따른 결과 제시

요청과 현재 대화에서 무엇을 찾으려는지 판단한다. 이미 드러난 목적을 다시 묻거나 매번 목적 선택지를 제시하지 않는다. 목적이 불분명하면 관련성이 높은 노트와 맞는 이유를 짧게 보여주며 시작한다. 다음 구분은 출력 양식이나 순서가 아니며, 요청이 바뀌면 필요한 부분만 조정한다.

| 목적 | 우선 보여줄 결과 |
| --- | --- |
| 다시 찾기 | 가장 유력한 노트와 해당 대목, 기억한 표현과 맞는 이유. 대상이 분명하면 그 결과에서 끝내고 관련 자료를 늘리지 않는다. |
| 배우고 이해하기 | 소수의 핵심 원문과 읽을 대목, 각 자료가 설명하는 부분과 설명·적용 조건이 갈리는 지점. 요청한 설명도 함께 제공하며, 원문을 읽거나 자기 설명을 먼저 해야 답을 주는 절차로 바꾸지 않는다. |
| 주장 검토 | 주장을 직접 받치는 근거, 적용 범위를 좁히거나 반박하는 근거, 아직 확인하지 못한 점. 단순한 주제 일치를 지지나 반박으로 취급하지 않고, 찾지 못한 반례를 만들어 균형을 맞추지 않는다. |
| 글감 탐색 | 서로 다른 질문 후보와 각 질문을 받치는 실제 노트·경험·자료. 키워드만 바꾼 같은 질문을 늘리지 않고, AI가 제안한 질문을 사용자의 확정된 주장이나 아웃라인으로 바꾸지 않는다. |

각 결과에는 실제로 읽은 노트로 가는 링크와 필요한 대목을 붙인다. 원문이 말한 내용과 AI의 비교·해석을 구분하고, 검색 점수나 순위를 근거의 강도나 진실성으로 해석하지 않는다. 반대 근거를 찾지 못했으면 이번 확인 범위에서 찾지 못했다고만 말한다.

검색 후보 수는 사용자에게 보여줄 개수가 아니다. 같은 역할의 결과는 추리고, 필요한 대목을 확인했거나 추가 결과가 현재 답·질문·판단을 바꾸지 않으면 탐색을 멈춘다. 확인할 수 없는 부분은 남기며, 더 많은 검색으로 해결할 수 없는 문제에는 필요한 관찰·실험을 제안할 수 있다.

다른 작성·검토 스킬 안에서 검색했다면 그 작업의 산출물과 보고 형식을 우선한다. 목적별 검색 보고서를 별도로 붙이거나 새 메타데이터·스킬·절차를 만들지 않는다. 검색만 요청받았을 때는 노트 작성·수정·연결·승격까지 진행하지 않는다.

## Structured query 작성

- 모호한 요청을 bare `qmd query`에 그대로 넘기지 않는다. `intent`에는 무엇을 찾는지와 피하려는 **개념적 오탐**을 적는다. `intent`는 검색 필터가 아니라 query expansion·청크 선택·rerank에 쓰이는 의미 문맥이다.
- 연결·승격처럼 누락 비용이 큰 검색은 후보를 15개(`-n 15` 또는 `limit: 15`) 가져온다.
- 범위 제한은 QMD collection이 분리돼 있으면 `collections`로 적용한다. 현재처럼 단일 `PKM` collection 안의 폴더를 좁힐 때는 반환된 `file` 필드를 직접 검사한다 (예: Slipbox 대조는 `01_Slipbox/`만 남긴다).
- 기본 검색에서는 rerank를 유지한다. 경로 필터 후 적절한 후보가 없을 때만 MCP `rerank: false`(CLI 모델 실행이 허용된 환경은 `--no-rerank`)로 재확인한다.

## 판단과 검증

- 중요한 판단은 `rg`의 정확 후보와 QMD의 의미 후보를 병합한다. 실제 사용한 방식을 정확 검색·의미 검색으로 짧게 밝히며, 실행하지 못한 검색까지 수행했다고 보고하지 않는다.
- 검색 snippet은 후보 탐색에만 사용하고, 판단하기 전에 상위 후보 원문을 MCP `get`·`multi_get`으로 가져와 읽는다.
- `_workspace/`, `40_Archive/`, `30_Resources/References/Clippings/_local-snapshots/`는 현재 지식 연결 후보에서 제외한다. 로컬 스냅샷은 검색 근거가 아니라 개인 열람용 원문 보관본이다.
- `qmd update && qmd embed` 수동 실행은 사용자가 QMD 갱신·재인덱싱을 직접 요청했을 때만 한다. 대량 이동·삭제·병합 뒤 검색 결과가 오래되었으면 갱신 필요성을 알리되, 요청 전에는 현재 파일과 `rg`로 확인하고 평소 갱신은 post-commit hook에 맡긴다.

### 재색인 트리거: git post-commit

정기 재색인은 `.agents/hooks/post-commit`이 담당한다. 마크다운이 바뀐 커밋마다 `qmd update && qmd embed`를 백그라운드로 실행한다.

- 새 기기에서는 한 번 등록해야 한다: `git config core.hooksPath .agents/hooks`
- `qmd update`는 git diff가 아니라 컬렉션 전체를 재스캔하므로, gitignore된 노트(DevLog daily, job-search)도 이때 함께 갱신된다.
- 대신 인덱스 신선도는 **커밋 주기에 묶인다.** 며칠 커밋 없이 Obsidian에서만 작업해 검색 결과가 오래되었다면 현재 파일로 재확인하고, 필요하면 사용자에게 수동 갱신 요청 여부를 확인한다.
- 실행 기록은 `.git/qmd-index.log`에 남는다. 검색 결과가 최신 노트를 놓치면 여기부터 확인한다.
- 훅은 `.git/qmd-index.lock`으로 중복 실행을 막는다. 이전 색인 프로세스가 trap 없이 죽어 잠금이 남아도, 다음 커밋에서 PID가 죽은 것을 확인하고 잠금을 지운 뒤 진행한다. 로그의 `stale lock removed` 줄이 그 흔적이다.

`sandbox_workspace_write.writable_roots`의 QMD 캐시 허용은 SQLite 읽기·쓰기를 위한 설정이며 Metal GPU 실행 권한과는 별개다. `qmd doctor`의 GPU 탐지 성공만으로 샌드박스 안 모델 실행 성공을 판단하지 않는다.

## Bootstrap: generic CLI instructions (위 라우팅이 우선)

This installed skill is intentionally a small bootstrap so it does not go stale
when the qmd package updates.

Load the full, version-matched QMD instructions from the CLI:

!`qmd skill show`

If your agent does not support bang-command expansion, run:

```bash
qmd skill show
```

Then follow those instructions within the vault routing above. Search first, fetch full sources with MCP `get` or `multi_get`, and answer from retrieved text rather than snippets.
