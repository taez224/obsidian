---
created: 2026-07-11
tags:
  - 지식관리
aliases:
  - Obsidian Workflow
  - 옵시디언 워크플로
---

# Obsidian 운영 워크플로

> [!summary] 운영 원칙
> **포착은 가볍게, 정리는 몰아서, 연결은 필요할 때, 판단은 사람이 한다.**

PARA는 노트의 위치를 정하고, Zettelkasten은 생각을 발전시킨다. AI는 검색과 정리 비용을 줄이지만 삭제·승격·병합·공개 여부는 사람이 결정한다.

## 전체 흐름

```text
오늘의 일정·한 일 ─────────────→ Daily Note
순간적으로 떠오른 생각 ────────→ Inbox
책·아티클·영상 같은 외부 자료 ─→ Resources
진행 중인 업무·이직·블로그 ────→ Projects

Inbox·Resources
       ↓ 주간 검토
삭제 / Resources 유지 / Project 흡수 / Slipbox 승격
                                      ↓
                              영구 노트 연결
                                      ↓
                         필요할 때만 MOC 생성
                                      ↓
                           블로그·이력서·판단에 활용
```

## 어디에 기록할지 결정하기

| 입력 | 위치 | 판단 기준 |
| --- | --- | --- |
| 오늘 한 일, 일정, 감정, 할 일 | `10_Periodic Notes` | 오늘이라는 시간 맥락이 중요함 |
| 문득 떠오른 개인 생각 | `00_Inbox` | 나중에 다시 생각하고 싶음 |
| 책·아티클·영상·외부 자료 | `30_Resources` | 출처와 자료 맥락이 중심임 |
| 이직·블로그·개발 작업 | `20_Projects` | 완료해야 할 결과물이 있음 |
| 여러 맥락에서 재사용할 자기 주장 | `01_Slipbox` | 원자료 없이도 독립적으로 이해할 수 있음 |
| 완료된 프로젝트·반복 초안 | `40_Archive` | 현재 작업 공간에서 더 이상 쓰지 않음 |

Daily Note와 Inbox에 같은 내용을 이중으로 적지 않는다. 오늘의 기록이면 Daily Note, 미래에 다시 생각할 아이디어면 Inbox에 둔다.

## 매일 — 포착

매일 노트를 완성하거나 정리하지 않는다. 기록할 것이 있을 때만 다음처럼 포착한다.

- 순간적인 생각은 `capture-fleeting-note`로 Inbox에 저장한다.
- 오타와 명백한 음성 인식 오류만 고치고 내용을 확장하지 않는다.
- 캡처 단계에서는 태그, 기존 노트 검색, 연결, 영구 노트 여부를 고민하지 않는다.
- 출처가 분명한 자료는 Inbox를 거치지 않고 Resources에 둔다.
- 프로젝트 수행 중인 자료와 결정은 해당 Project에 둔다.

```text
메모해줘: 템플릿은 내용을 채우는 양식보다 생각을 확장하는 질문이어야 한다
```

## 참고노트 — Resources

Books·Articles·Clippings는 외부 자료의 맥락을 보존하는 참고노트다. 모든 내용을 요약하지 않고 다음만 남긴다.

- 원자료에서 중요하다고 느낀 내용
- 동의하거나 의심한 부분
- 내 경험·기존 생각과 연결되는 부분

책 전체 기록은 `30_Resources/References/Books`에 유지한다. 다른 글과 판단에 재사용할 **내 주장**이 생겼을 때만 별도 permanent note로 압축하고 원본 참고노트를 출처로 연결한다. 전문을 Slipbox에 복제하지 않는다.

## 주간 — 검토와 라우팅

주 1회 20~30분 동안 [[00_Inbox/_inbox.base|Inbox Base]]에서 오래된 노트부터 처리한다. 각 노트에는 다음 중 하나만 결정한다.

1. 삭제
2. Resources에 보관
3. Project에 흡수
4. 새 permanent note로 승격
5. 기존 permanent note에 합치기

의미 판단이 필요하면 `review-zettelkasten`을 사용한다.

```text
이번 주 Inbox와 읽은 자료를 검토해서 삭제·보관·승격·기존 노트 보강 후보를 먼저 제안해줘
```

AI는 후보, 제목, 중심 주장, 연결 이유를 먼저 제안한다. 승인 전에는 생성·이동·삭제하지 않는다.

새 permanent note를 만들기 전에는 QMD의 structured query(`intent / lex / vec / hyde`)로 현재 Slipbox를 검색한다.

- 같은 주장 → 기존 노트 보강
- 이어지는 주장 → 새 노트 생성 후 관계를 설명해 연결
- 반대되는 주장 → 충돌 지점을 설명할 수 있을 때 연결
- 키워드만 일치 → 연결하지 않음

이번 주에 실제로 읽거나 사용한 Resources만 검토한다. 모든 참고노트에서 영구 노트를 억지로 뽑지 않는다.

## Slipbox — 생각 발전

Permanent note는 완성품이 아니라 계속 수정되는 생각의 단위다.

| 상태 | 의미 |
| --- | --- |
| `seedling` | 핵심 생각이 생긴 초기 노트 |
| `growing` | 설명·사례·연결이 늘어나는 중 |
| `evergreen` | 반복해서 검토했고 안정적으로 재사용 가능 |

새 노트 수를 늘리는 것보다 기존 생각을 발전시키는 것을 우선한다. 영구 노트는 다음 조건을 목표로 한다.

- 한 문장 중심 주장이 있음
- 이 노트만 읽어도 이해할 수 있음
- 사용자의 언어와 판단이 들어 있음
- 연결에는 근거·적용·반례·상하위 관계를 한 줄로 설명함

명시적으로 승격하려면 `permanent-note`를 사용한다. AI가 입력에 없던 내용을 덧붙일 때는 본문에 섞지 않고 발전시킬 질문으로 분리한다.

## MOC — 필요할 때만 구조화

MOC는 정기 산출물이 아니라 반복해서 함께 찾는 생각의 지도다. 다음 조건이 모두 맞을 때만 `type: hub` 노트를 만든다.

- 서로 다른 permanent note가 3개 이상 있음
- 하나의 질문이나 글감으로 반복해서 함께 찾음
- 링크 목록이 아니라 탐색 순서가 필요함

형식은 [[99_Templates/hub-note|hub-note 템플릿]]을 따른다. 월간에는 MOC를 반드시 업데이트하지 않고 **새 MOC가 필요한지 검토**한다.

## Projects와 Blog

Projects에는 종료하거나 전달해야 할 결과물을 둔다.

- 프로젝트 안에서만 필요한 기록 → Project 유지
- 다른 프로젝트에서도 재사용할 판단 → Slipbox
- 블로그 전문 정본 → `20_Projects/blog`
- 블로그에서 분리한 독립 개념 → Slipbox
- 발행 후 남은 반복 초안 → `40_Archive/blog-drafts`

프로젝트의 현재 상태는 [[20_Projects/_dashboard.base|Project Dashboard]]에서 확인한다.

## 글쓰기

빈 문서에서 바로 시작하기보다 축적된 노트에서 출발한다.

1. 쓰려는 질문을 정한다.
2. QMD로 Slipbox·Resources·DevLog를 검색한다.
3. 기존 MOC가 있으면 탐색 순서를 확인한다.
4. 필요하면 임시 개요 또는 MOC를 만든다.
5. `20_Projects/blog`에서 전문 정본을 작성한다.
6. 글쓰기 중 생긴 재사용 가능한 판단을 Slipbox에 돌려보낸다.

## 월간·분기 점검

### 월간

- Project의 `active / on-hold / completed` 상태 확인
- 최근 사용한 `seedling / growing` 노트만 검토
- 반복 탐색하는 노트 군집에 MOC가 필요한지 확인
- `_global-health.base`에서 큰 정리 부채만 확인

### 분기 또는 필요할 때

- 완료 프로젝트와 반복 블로그 초안을 Archive로 이동
- 사용하지 않는 태그와 폴더 구조 정리
- 대규모 정리 전 체크포인트 커밋
- `vault-lint`로 frontmatter·죽은 링크·고립 Slipbox 점검

모든 orphan을 없애려고 하지 않는다. 고립 여부는 Slipbox에는 중요하지만 Books·Clippings·독립 블로그는 연결되지 않아도 문제가 아니다.

## AI 스킬의 역할

| 스킬·도구 | 역할 |
| --- | --- |
| `capture-fleeting-note` | 생각을 해석하지 않고 Inbox에 빠르게 저장 |
| `permanent-note` | 명시적으로 요청한 생각을 영구 노트로 정제·보강 |
| `review-zettelkasten` | 승격·병합·연결·MOC를 의미 단위로 판단하고 승인 후 적용 |
| `vault-lint` | frontmatter·죽은 링크·고립 노트를 기계적으로 검사 |
| QMD | 정확 검색과 의미 검색으로 기존 노트 탐색 |
| Bases | Inbox·Project·Slipbox 상태를 화면에서 확인 |

스킬의 세부 실행 절차는 각 `SKILL.md`가 정본이다. 이 문서에는 사람이 기억할 운영 경계만 둔다.

## QMD 갱신

Codex 세션 시작 시 hook이 `qmd update && qmd embed`를 자동 실행한다. 평소에는 별도로 관리하지 않는다.

다음 경우에만 수동 갱신한다.

- 여러 노트를 이동·삭제·병합한 뒤
- 블로그나 Resources를 대량 이관한 뒤
- 새 노트를 같은 세션에서 바로 의미 검색해야 할 때
- 긴 세션에서 검색 결과가 현재 파일과 다를 때

노트 하나를 고칠 때마다 embed하지 않는다.

## 과도하게 관리하지 않기

다음 항목은 목표가 아니다.

- 매일 반드시 Daily Note 만들기
- 모든 Inbox를 즉시 비우기
- 모든 책에서 영구 노트 만들기
- 모든 노트를 3개 이상 연결하기
- 매달 MOC 만들기
- orphan 수치를 0으로 만들기
- 모든 `seedling`을 `evergreen`으로 올리기

> [!important]
> 시스템을 잘 관리하는 것이 목적이 아니다. 생각을 다시 찾고, 발전시키고, 글과 판단에 사용하는 것이 목적이다.

## 정본과 대시보드

- 구조·태그·에이전트 규칙: [[AGENTS]]
- frontmatter 스키마: [[99_Templates/_property-schema|Property Schema]]
- 빠른 포착 형식: [[99_Templates/quick-capture|Quick Capture Template]]
- 영구 노트 형식: [[99_Templates/slipbox-template|Slipbox Template]]
- MOC 형식: [[99_Templates/hub-note|Hub Note Template]]
- Inbox 상태: [[00_Inbox/_inbox.base|Inbox Base]]
- Slipbox 상태: [[01_Slipbox/_index.base|Slipbox Index]]
- Project 상태: [[20_Projects/_dashboard.base|Project Dashboard]]

## 연관된 노트

- [[제텔카스텐이란?]] - 포착·참고노트·영구 노트·구조 노트의 구분을 정리한 출발 메모
- [[세컨드 브레인은 옵시디언 with 클로드 코드]] - 현재 워크플로를 정비하게 된 참고 자료
