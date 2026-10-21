# 검색 범위 관리

현재 지식을 찾는 검색에서 검토 보고서·옛 원고·아웃라인이 본문과 경쟁하지 않도록 컬렉션을 나눈다. 파일 위치나 공개 범위는 바꾸지 않는다.

| 컬렉션 | 담는 자료 | 사용할 때 |
| --- | --- | --- |
| `PKM` | 아래 제외 경로를 뺀 vault의 Markdown | 일반 노트 검색. 기본 검색에 포함 |
| `PKM-workspace` | `_workspace/`, `20_Projects/blog/_outlines/` | 검토 이력·실험 기록·집필 방향을 찾을 때 명시적으로 선택 |
| `PKM-archive` | `40_Archive/` | 과거 기록이나 이전 입장과 비교할 때 명시적으로 선택 |

`30_Resources/References/Clippings/_local-snapshots/`는 개인 열람용 원문이라 세 컬렉션 모두에 넣지 않는다. 작성 중인 본문은 `PKM`에 남는다. 아웃라인을 작업 자료로 검색하는 것과 글 완료 후 Archive로 옮기는 것은 별도 판단이다.

## 설정

이 기기의 실제 설정은 `~/.config/qmd/index.yml`에 있다. QMD 2.8.3에서 확인한 구성은 다음과 같다. `<vault>`를 절대 경로로 바꾸고, 기존 모델·다른 컬렉션 설정은 보존한다. QMD는 숨김 파일·폴더를 기본적으로 색인하지 않는다.

```yaml
collections:
  PKM:
    path: <vault>
    pattern: "**/*.md"
    ignore:
      - "_workspace/**"
      - "20_Projects/blog/_outlines/**"
      - "40_Archive/**"
      - "30_Resources/References/Clippings/_local-snapshots/**"
  PKM-workspace:
    path: <vault>
    pattern: "{_workspace,20_Projects/blog/_outlines}/**/*.md"
    includeByDefault: false
  PKM-archive:
    path: <vault>
    pattern: "40_Archive/**/*.md"
    includeByDefault: false
```

세 컬렉션의 루트를 모두 vault로 유지하므로 결과에서 컬렉션 이름을 제외한 경로가 실제 vault 상대 경로다. `includeByDefault: false`는 기본 검색에서만 빠진다는 뜻이며, 명시한 컬렉션의 검색·원문 조회는 가능하다.

## 적용과 확인

1. 변경 전 설정과 현재 컬렉션 상태를 보존한다. 색인 갱신은 사용자에게 승인받은 범위에서 실행한다.
2. 설정 변경 뒤 `qmd update`로 검색 범위를 반영한다. 파일을 지우는 작업이 아니며, 내용 해시가 같은 문서는 기존 임베딩을 재사용한다. `qmd status` 또는 MCP `status`에서 임베딩 대기를 확인하고 필요한 경우에만 `qmd embed`를 실행한다. 강제 임베딩이나 `cleanup`을 함께 실행하지 않는다.
3. `qmd ls PKM`에 제외 경로가 없는지, 보조 컬렉션에서 작업·보관 자료를 찾을 수 있는지 확인한다. 일반 검색에는 `collections: ["PKM"]`을 명시한다.
4. [실제 질문 평가](../evals/cases.md)를 실행한다. 기존 노트의 이동·삭제는 필요 없다.

승인된 복구 작업에서는 보조 컬렉션 설정을 남긴 채 `PKM`의 원래 범위를 먼저 복원하고 `qmd update`한다. 원래 자료가 `PKM`에서 다시 검색되는지 확인한 뒤 `qmd collection remove PKM-workspace`, `qmd collection remove PKM-archive`로 보조 색인 등록을 제거하고 보존한 설정을 최종 복원한다. 이 명령은 원본 파일을 지우지 않는다. YAML에서 보조 컬렉션 이름만 먼저 지우면 QMD 2.8.3의 DB에 해당 문서가 활성 상태로 남을 수 있다.

MCP는 시작할 때 안내문과 기본 컬렉션 목록을 저장한다. 기본 목록이 계속 `PKM`이면 기존 연결도 갱신된 DB와 명시적인 컬렉션 선택을 사용할 수 있다. 표시 목록이 오래됐으면 `status`로 확인하고, 기본 컬렉션 자체를 바꿨다면 클라이언트에서 MCP를 재연결한다.

## 확인한 한계

QMD 2.8.3의 BM25는 전역 후보 일부를 만든 뒤 컬렉션을 걸러낸다. 이 구성은 작업 자료가 현재 노트의 결과 통합·재정렬 후보에 들어가는 것을 막지만 최초 BM25 후보 경쟁까지 완전히 분리하지는 않는다. 현재 사례로 효과를 확인하며, 필요한 노트가 계속 밀리면 원문과 정확 검색을 대조한다. 별도 색인은 실제 누락이 남을 때 검토한다.

같은 버전의 `qmd update` 마지막 임베딩 안내는 기본 모델 기준으로 대기 수를 계산할 수 있다. 사용자 지정 모델에서는 `qmd status` 또는 MCP `status`의 대기 수와 모델을 먼저 확인한다.
