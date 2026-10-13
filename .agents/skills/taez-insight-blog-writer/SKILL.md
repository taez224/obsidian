---
name: taez-insight-blog-writer
description: 사용자가 "이걸 블로그 글로 써보자", "아웃라인 짜줘", "튜토리얼·트러블슈팅·개념 설명 글로 정리해줘", "발행 전에 검토해줘", "제목이랑 소제목 골라줘", "최종 어셈블 돌려줘"처럼 vault 노트·업무 경험·설계 판단·리서치·초안을 한국어 블로그 글의 아웃라인이나 원고로 만들거나, 발행을 위해 크게 재구성·검토하려 할 때 사용한다. 경험에서 판단을 끌어내는 통찰형 글과 개념 설명·학습·문제 해결을 위한 기술 글을 모두 다루고, 브런치·개인 기술 블로그·회사 기술 블로그 같은 발행면에 맞춰 집필 계약을 고른다. 기본은 아웃라인까지 만들고 본문은 TaeZ가 쓰며, 전문 초안은 명시적으로 요청할 때만 쓴다. 문장 단위 다듬기는 sentence-audit, 이해·흐름만 보는 점검은 reader-perspective-review가 맡고, 일반 노트 편집이나 아직 글 작업이 되지 않은 탐색 대화에는 쓰지 않는다.
---

# TaeZ Insight Blog Writer

## Purpose

Help TaeZ turn grounded experience and judgment into Korean articles that fit their actual publication surface. Structure and evidence serve the article; they are not fixed sections every article must contain.

## Operating Principles

- Do not produce generic AI thought-leadership. Use lived scenes, tradeoffs, and objections when the source material and genre call for them; never invent them to satisfy a format.
- Preserve TaeZ's recurring lenses when relevant, but do not force them: platform-as-enablement, workflow as operating system, team capability over individual output, evidence-backed reflection, dogfooding, responsibility boundaries, learning loops.
- Treat AI assistance as acceptable. Slop is not "AI was used"; slop is "no authorial judgment, no context, no accountable takeaway."
- Structure before sentence polish. If the argument is weak, do not run a humanizing pass yet.
- Default to outline-first collaboration. Leave the sentences, transitions, and final emphasis to TaeZ unless they explicitly request a full draft or a named-section rewrite.
- Treat external research and editorial reviews as evidence and proposals, not authority. Check them against the article contract and TaeZ's actual thesis before applying them.
- Draft natural Korean from the first pass. Do not rely on a later humanizing pass to repair translationese, templated pivots, or inflated abstraction.
- Keep Korean technically literate. Avoid over-explaining familiar engineering ideas.

## 파이프라인 오케스트레이션

이 스킬은 블로그 파이프라인의 단일 진입점이다. 과거 문서의 `blog-polish`와 `blog-pipeline`은 사용하지 말고, 아래 자산만 사용한다.

### 라우팅

- **vault 노트 기반**(Slipbox·DevLog·Periodic·초안) → 아래 vault 파이프라인을 사용한다.
- **git 저장소·커밋·설계문서 기반** → `git log`·`git diff`·설계문서에서 사건·전환·일반화를 추출한 뒤 직접 초안 경로로 합류한다.

### vault 파이프라인 (`.claude/workflows/`)

표의 `blog-*` 워크플로(`.js`)는 여러 에이전트를 띄우는 Workflow 스크립트라서, 사용자가 워크플로 실행을 명시했을 때만 돌린다. 명시가 없으면 같은 단계를 이 스킬의 절차와 `references/`로 직접 수행한다. `blog-slop-lint.mjs`와 `blog-structure-scan.mjs`는 LLM을 호출하지 않는 결정론 스크립트이므로 필요할 때 `node`로 바로 실행한다.

| 단계 | 워크플로 | 핵심 산출 |
| --- | --- | --- |
| ① 앵글 | `blog-angle-mine` | 앵글 후보. 사람이 seed 노트를 직접 만든다. |
| ② 리서치 | `blog-research-gather` | Resources 리서치 노트와 반례 수집. |
| ③ 구조 | `blog-recompose`의 outline-only 기본값 또는 직접 구조화 | 한 줄 논지, 절별 역할, 근거와 경계를 담은 사용자 집필용 아웃라인. |
| ④ 사용자 집필 | 사람 게이트 | TaeZ가 아웃라인을 바탕으로 본문을 직접 쓴다. AI는 여기서 자동으로 전문을 이어 쓰지 않는다. |
| ④' 공동 초안 | `blog-recompose`의 `writeFullDraft: true` 또는 직접 작성 | 사용자가 전문 초안을 명시적으로 요청했을 때만 실행한다. |
| ⑤ 구조 검토 | `references/structural-review.md` + `blog-structure-scan.mjs` | 초안이 처음 완성됐거나 절을 재배치한 뒤. 문장을 다듬기 **전에** 뼈대를 본다. |
| ⑤' 기본 검수 | `blog-review-polish`의 `light` | 처음 읽는 독자 재독 + 구조 스캔 관측 + 결정론적 lint + 편집 판단 1회. 기술 글이면 `docType`을 넘긴다. |
| ⑥ 발행 게이트 | `references/slop-gate.md` + `blog-review-polish` 선택 단계 | 사용자가 발행 전 최종 검수를 요청할 때만 실행. 브런치는 `light`에 필요한 fact-check만 더하고, 회사 기술 블로그의 전체 검수에만 `mode: "publish"`를 사용. |
| ⑥' 최종 어셈블 | `references/final-assembly.md` | 사용자가 `final-assembly`, `완전 최종 어셈블`, `페르소나 패널 최종점검`처럼 다중 관점의 발행 사인오프를 명시했을 때만 실행. 파일은 승인 전 수정하지 않는다. |
| 상시 | `blog-slop-lint.mjs` | 결정론적 슬롭 린트(문장·표기). |
| 상시 | `blog-structure-scan.mjs` | 결정론적 구조 스캐너(절 비중·역방향 아웃라인 뼈대·교차 절 반복). 판정은 하지 않는다. |

### 런타임별 실행 경로

- **Claude Code**: 위 `.claude/workflows/`는 Claude 런타임에서 파이프라인을 가속하는 실행 자산이다. 최종 어셈블은 `blog-review-polish`의 발행 단계와 `references/final-assembly.md`의 조정 규칙을 함께 따른다.
- **Codex**: 새 글은 자료 확인 → 유형에 맞는 구조 설계 → 사용자 집필에서 기본적으로 멈춘다. substantial review에서는 `references/structural-review.md`와 필요한 읽기 전용 구조·문체 검사를 수행한다. 실제 편집은 사용자가 요청한 범위에서만 한다. 사용자가 최종 어셈블을 명시하면 `references/final-assembly.md`에 따라 격리된 좌석을 구성하고 교차 판정한다. 사람 게이트와 전체 검수는 발행 직전에만 사용한다.

두 런타임 모두 이 스킬의 `references/`와 본문의 판단 기준을 공유한다.

### 단일 출처 파일 (`references/`)

- `voice-profile.md` - 지킬 목소리 DNA.
- `anti-slop-lexicon.md` - 금지표현·문장부호의 단일 출처. lint와 AI-티 감별사가 함께 사용한다.
- `korean-first-draft.md` - 새 글을 쓸 때 읽는 번역투·정형 문장 예방 규칙. 윤문용 전체 분류표가 아니다.
- `slop-gate.md` - 발행 전 사람 사인오프.
- `final-assembly.md` - 명시적으로 요청한 발행 직전 다중 페르소나 검토와 교차 판정.
- `structural-review.md` - 문장이 아니라 뼈대를 보는 developmental 층. 역방향 아웃라인 절차와 판정 목록.
- `visual-argument-review.md` - 논지를 운반하는 도식의 사실·위계·강조·실제 렌더 검토.
- `amplifier-lenses.md` - 쓰기 전 앵글과 다듬기 단계의 가치 증폭 렌즈.
- `domestic-tech-blog-benchmark.md` - 회사 기술 블로그의 최신 제목·구조·문장 리듬 표본.
- `tech-doc-types.md` - 기술 글의 문서 유형(설명·학습·문제 해결), 문서 계약, 유형별 기준.
- `research-verification.md` - 외부 수치·인용·연구·정책 일정을 개요에 올리기 전 확인 기준.
- `series.md` - 연재 허브 확인, 연재 글의 구조와 검수 항목.

## Workflow

### 1. Clarify the article contract

If missing, ask for only the information needed:

- target reader
- author position
- publication surface
- source material
- desired artifact: outline, draft, revision, review, or reusable workflow
- document type, for a technical article (see below)

If the user already provides direction, proceed without asking.

집필·리뷰의 기준과 범위 판단은 [공통 글쓰기 기준의 작성 전후 대조](../../guides/writing.md#작성-전후-대조)를 따른다.

If the user says they will write the article themselves, or does not explicitly ask for full prose, choose `outline` as the default artifact. Stop after delivering or saving the outline. Do not continue into a full draft in the same turn merely because enough material exists.

통찰형 글의 새 집필·대규모 재작성·발행 전 종합 검토·제목 종합 검토에서는 `references/voice-profile.md`를 읽는다. 기술 설명·학습·문제 해결 글은 사용자와 발행면의 톤을 따르며, 개인 관점이 글의 중심일 때만 이 reference를 사용한다. 단순 문장 단위 수정에는 불러오지 않는다.

Choose the contract by publication surface before selecting a structure.

- **Brunch·personal essay**: preserve the writer's question, lived texture, and reading rhythm. A named framework, research section, counterargument, or operating model is optional.
- **Personal technical blog**: connect an actual technical decision or failure to a reusable criterion. Add artifact evidence where it carries the argument.
- **Company technical blog**: prioritize reproducibility, factual accuracy, system context, and reader utility. Load the domestic benchmark only here or when explicitly requested.

발행면과 별개로 글의 주된 목적을 구분한다. 경험에서 판단을 끌어내는 통찰형은 `references/tech-doc-types.md`를 읽지 않고 4~5단계로 간다. 개념·원리 설명, 학습, 특정 작업·문제 해결을 위한 기술 글은 이 reference로 문서 유형과 계약을 정한 뒤 5.1단계에서 유형에 맞는 아웃라인을 만든다. 절 구성이 달라질 만큼 불명확한 부분만 묻는다.

블로그의 `summary`는 [속성 스키마](../../../99_Templates/_property-schema.md)의 블로그 summary 작성 기준을 따른다.

연재 글이면 근거를 모으기 전에 `references/series.md`의 연재 허브 확인을 따른다.

### 2. Build the personal evidence base

Search the vault before writing: the topic's project notes, previous posts in `20_Projects/blog/`, related Slipbox claims, and counterexamples when the claim needs them. Do not rely on a fixed anchor list; find the evidence that fits this article. The invariant is source-grounded authorial judgment, whether it changed or became clearer.

Before deep research or outlining, run an adjacency check regardless of whether the article belongs to a series:

- Use exact title/term search and semantic claim search to shortlist the 1-3 nearest canonical blog posts. Exclude archives and duplicate drafts.
- Read the shortlisted posts as bodies, not only headings or frontmatter. Record each post's local claim, opening scene, climax evidence, and landing conclusion.
- Allow recurring lenses, vocabulary, and authorial character. Treat the new article as duplicative only when it repeats substantially the same local claim with the same scene or evidence and lands at the same conclusion.
- If the publication contract calls for a self-contained adaptation on another surface, allow deliberate reuse and identify what is being adapted. Otherwise find a new question, boundary, counterexample, or piece of evidence before outlining.

Extract only what the source material actually supports:

- actual episode: what happened
- prior or changed belief, if there was one
- artifact evidence: commands, PRs, diagrams, workflow names, failed experiments
- transferable implication: what other engineers can reuse

### 3. Deep research, but only after the thesis shape exists

Use current external research when claims are time-sensitive or trend-dependent. Prefer primary or high-signal sources: papers, official engineering posts, original case studies, standards, and respected practitioner essays.

개요에 올리기 전에 수치·인용·연구 결과·정책 일정은 `references/research-verification.md`의 기준으로 확인한다.

Load `references/anti-slop-research.md` only when the topic touches AI slop, workslop, writing quality, developer content saturation, or "AI-generated but valuable" distinctions.

Research should sharpen the user's claim, not turn the post into a literature review.

For company-facing Korean tech blog polish, or when the user mentions domestic tech blogs such as Toss, Woowahan, Banksalad, Kakao, Naver D2, LINE/LY, Daangn, or Hyperconnect, load `references/domestic-tech-blog-benchmark.md`. Use it as a rhythm and density benchmark, not as a template to imitate.

### 4. 통찰형의 한 줄 논지

Before drafting, state what this article leaves with the reader in one sentence. Several framings are available; pick the one the material actually supports rather than reaching for the first:

```text
판단 전환:  People commonly see X. This experience showed Y. That changes Z.
비용 노출:  X was the right call. It billed Y, paid by Z.
경계 발견:  X holds here and breaks there. The line is Y.
질문 교체:  I asked X. Answering it showed X was the wrong question. The better question was Y.
```

The first framing fits only when a genuine change of judgment or disagreement defines the article. An article whose judgment never changed is not weaker - it is a different article, and forcing a reversal into it manufactures a fake turn.

Do not force a conventional view, personal turn, or practical move into a reflective essay. Reject claims that remain generic, such as:

- "AI is useful but risky"
- "Use AI responsibly"
- "Humans still matter"
- "Tools are not enough"
- "Communication is important"
- "Culture matters"
- "We need better process"

Make the claim specific with the subset that matters here: what changed, what cost moved, who pays it, what the user learned, or what structure prevents the failure.

통찰형에서 앵글을 더 탐색할 필요가 있을 때만 `references/amplifier-lenses.md`의 생성형 렌즈를 참고한다. 설명·학습·문제 해결 글에 이해관계·통찰 독창성·브랜드 탐색을 요구하지 않는다.

### 5. 통찰형의 전개

Choose the movement the material supports. This is a menu, not a ranking - the list exists because a writer who reaches for the same movement every time produces articles that feel identical even when the evidence is different.

- **판단이 바뀐 이야기** - 착각 → 부분 성공 인정 → 반전 → 원칙. 필자가 실제로 생각을 바꿨고 전후가 근거로 남아 있을 때.
- **비용을 따라가는 이야기** - 결정 → 그 결정이 청구한 대가 → 대가를 감수할지 다시 고르기. 판단은 그대로인데 가격표가 보이기 시작했을 때.
- **실패에서 시작하는 이야기** - 무너진 장면 → 무너진 이유 → 바꾼 것 → 아직 못 고친 것. 실제로 무언가 부러졌을 때.
- **두 사례를 부딪히는 이야기** - 원칙이 통한 사례와 통하지 않은 사례 → 경계선 → 경계선의 근거. 진짜 반례가 재료에 있을 때.
- **질문이 바뀌는 이야기** - 처음 던진 질문 → 답하다 질문이 틀렸음을 발견 → 새 질문. 글의 가치가 답이 아니라 재구성에 있을 때.

Add a framework, technical evidence, counterargument, or operating model only when it carries the claim. Do not report omitted sections or fill them with boilerplate.

### 5.1 Stop at a writer-owned outline by default

아웃라인의 위치·갱신·보관은 [블로그 운영 기준의 아웃라인 관리](../../../20_Projects/blog/blog.md#아웃라인-관리)를 따른다.

Build an outline that gives TaeZ enough structure to write without pre-writing the article for them. Use only the fields each section needs:

```markdown
## 한 줄 논지

- 이 글이 독자에게 남길 판단 한 문장

## 글의 움직임

- 출발 질문 또는 장면
- 글을 지나며 바뀌는 질문이나 드러나는 비용
- 마지막에 남길 기준

### 절 제목

- 역할:
- 직접 쓸 장면·경험:
- 이 절의 주장:
- 사용할 근거:
- 경계·반론:
- 다음 절로 넘길 질문:
```

- Do not require every field or impose a fixed number of sections.
- 설명·학습·문제 해결형이면 `## 한 줄 논지` 대신 `references/tech-doc-types.md`의 `## 문서 계약`으로 시작하고, 절 필드의 `이 절의 주장`은 `독자의 다음 질문`으로 바꿔 쓸 수 있다.
- Keep research as evidence notes attached to the claim it supports. Do not turn all gathered papers into body sections.
- Mark missing evidence as a prompt for TaeZ only when a section's claim cannot stand without it; otherwise narrow the claim to what the material supports. List details that would merely strengthen the article separately as optional, not as required fills. When TaeZ has said the given material is all that can be used, do not turn new facts into decisions to make either: narrow each claim to that material and keep any additions in the optional list. Never invent a workplace scene, judgment change, result, or number.
- Do not write polished opening paragraphs, transitions, or closing prose unless explicitly requested.
- After TaeZ writes prose, review structure, evidence, repetition, and unsupported leaps first. Rewrite only the named section or sentence range they authorize; preserve manually written thought flow elsewhere.

Run a title and heading pass before handing off the outline:

- Make the article title promise the actual climax or landing, not only the opening scene or one supporting study.
- Do not reuse the article title verbatim as a section title.
- Let each section heading perform its local role: a scene heading can name the artifact or friction; a conceptual section can use a restrained thesis; a landing can be short and declarative.
- Do not require a proper noun, question, contrast, or experience suffix. For a company technical blog, compare with a current sample from `references/domestic-tech-blog-benchmark.md` and explain fit by article type.
- When options are useful, produce 2-3 meaningfully different strategies and state what part of the article each foregrounds. Do not generate a quota of cosmetic variants.

연재의 한 편이면 `references/series.md`의 「연재 글의 구조」를 초안 전에 적용한다.

### 5.2 Draft natural Korean before polishing

사용자가 전문 초안이나 본문의 대규모 재작성을 명시적으로 요청했을 때만, 쓰기 전에 `references/korean-first-draft.md`를 읽고 적용한다. 이는 사후 윤문이 아니라 초안의 기본 품질 기준이며, 초안을 쓴 뒤의 30초 자체 점검도 그 파일을 따른다.

### 6. Apply the anti-slop tests

구조부터 본다. 초안이 처음 완성됐거나 절을 추가·삭제·재배치한 뒤에는 `node .claude/workflows/blog-structure-scan.mjs "<file>"`를 돌리고 `references/structural-review.md`의 절차와 판정 목록을 따른다. **구조가 안 잡힌 글에 문장을 다듬으면 절을 옮길 때 그 문장이 통째로 버려진다.** 문장만 고치는 요청에는 이 단계를 넣지 않는다.

초안이 완성되거나 구조를 크게 바꾼 뒤에는 문장 윤문 전에 `.agents/skills/reader-perspective-review/SKILL.md`의 독자 시점 점검도 적용한다. 이 공통 점검은 이 스킬의 구조·근거·발행 검토를 대체하지 않으며, 문장만 고치는 요청에는 반복하지 않는다. 같은 초안에 `blog-review-polish`의 light 검수를 돌린다면 그 처음 읽는 독자 재독이 이 점검을 겸한다.

글 전체의 최종 검토에서는 독자 시점 점검에 이어 [sentence-audit](../sentence-audit/SKILL.md)로 문장을 점검하되, 이미 점검한 원고는 이후 바뀐 부분과 앞뒤 연결만 확인한다.

글의 논지를 도식·인포그래픽이 운반한다면 `references/visual-argument-review.md`도 읽고 실제 발행 크기의 렌더를 확인한다. 장식 이미지는 이 검토를 강제하지 않는다.

그다음 필요한 문체 검토에 `node .claude/workflows/blog-slop-lint.mjs "<file>"`를 사용한다. 경고는 문맥에 따라 유지·수정 후보로 판단하며 검토 요청만으로 자동 수정하지 않는다. `references/slop-gate.md`는 사용자가 발행 전 최종 검수를 요청했을 때만 읽고, 글의 장르와 근거에 맞는 항목만 사람이 판단한다.

`humanize-korean` 전체 워크플로는 기본 단계가 아니다. 사용자가 명시적으로 윤문을 요청했거나, 발행 직전 사람이 번역투·정형 문장을 확인했을 때만 실행한다. 이때도 의미·사실·인용은 보존하고, 초안의 논지나 장르를 바꾸지 않는다.

For a substantial draft or review, check only the applicable questions:

- For an insight article, could a reader get this by asking ChatGPT a broad question? If yes, check whether personal evidence or a sharper claim is needed. Explanation, tutorial, and how-to articles are assessed by their declared learning or task goal.
- Does every research citation do work? Remove decorative citations.
- If the article claims a changed judgment, is the before/after visible?
- Is the practical takeaway about behavior or structure, not just attitude?
- Are output metrics separated from actual capability, learning, reliability, or user value?
- Are AI-generated phrases flattened out without making the prose bland?

연재 글이면 `references/series.md`의 「검수」 항목으로 다시 훑는다.

For company-tech-blog publication checks only, run the `Publication review checklist` in `references/domestic-tech-blog-benchmark.md`.

### 7. Editing stance

When reviewing an existing draft:

- When the request is limited to reader comprehension and flow, use `.agents/skills/reader-perspective-review/SKILL.md`. For a full blog review, this skill's article-specific review and publication requirements remain in force.
- Lead with structural problems, repeated claims, weak transitions, and unsupported leaps. 어디를 볼지가 아니라 어떻게 볼지는 `references/structural-review.md`가 정본이다. 인상으로 구조를 진단하지 말고 역방향 아웃라인을 먼저 채운다.
- 외부 리뷰는 가설로 보고, 먼저 해당 지적이 사용자가 정한 목적을 달성하는 데 필요한지 판단한다. 사실 오류는 바로잡되, 그 오류를 확인하는 데 필요했던 조사·검증 과정을 모두 본문에 추가하지 않는다. 목적에 필요한 내용이면 보강하고, 보조 내용이면 요약·각주·제외 중 알맞은 방법을 고른다.
- 구현 소개 글의 본문 코드는 독자가 사용할 경로를 우선한다. 계측·우회·재현 같은 검증용 코드는 검증 자체가 글의 주제이거나 결론을 이해하는 데 필요할 때만 보여 준다. 코드 축약으로 실행 의미가 달라지는 조건이나 동작은 보존한다.
- 기술 글은 문서 계약에서 선언한 유형의 기준으로 결함을 판정한다. 다른 유형의 기준은 선택 사항으로만 보고한다.
- 같은 부분에서 이해 질문이 반복되면 설명을 덧붙이기 전에 그 부분의 역할과 필요한 깊이를 다시 판단한다. 각 수정이 개별적으로 타당해도 합쳐진 글의 중심이 바뀌지 않았는지 본다.
- Preserve strong local phrasing unless it damages clarity.
- Make small patches when the draft is close; suggest restructuring only when the argument is genuinely confused.
- For Obsidian posts, preserve frontmatter, wikilinks, markdown tables, image links, and `## 연관된 노트`.

## Output Formats

For a new article, produce by default:

- one-line thesis
- title options only if needed
- writer-owned outline
- source notes attached to relevant claims

Produce a full draft or prose patch only when explicitly requested. An outline request is complete when the structure, evidence placement, open decisions, and author prompts are clear.

For a review, produce:

- first-read thesis and review mode (`fresh-reader` or `context-aware`)
- publication-readiness verdict
- actual structural issues, ordered by impact; report none when no necessary correction is found
- objective defects, editorial risks, and preferences kept distinct
- strong passages worth preserving only when this helps assess a proposed revision; no fixed quota
- concrete rewrite suggestions
- optional direct patch

For an explicitly requested final assembly, use `references/final-assembly.md` and report the panel composition, failed or omitted seats, cross-confirmed findings, rejected suggestions, deterministic gate results, and final readiness. Do not patch the article until TaeZ approves the selected findings.

스킬을 보완할 때는 [평가 사례](evals/cases.md)와 [검토 결함 장부](evals/defect-log.md)를 참고한다. 일반 글 검토에서는 기존 검사가 놓친 재사용 가능한 결함을 실제로 발견했을 때만 장부 추가 후보를 짧게 보고한다. 후보를 채우려고 지적을 만들거나 장부를 자동 수정하지 않는다.

For a new article or substantial revision, finish with a concise `지식 환류` report:

- `사용한 Slipbox`: list only notes actually used in the article and state the usage context.
- `새 영구 노트 후보`: report reusable claims that emerged while writing as candidates only.
- If neither exists, state `환류 후보 없음` instead of forcing a link or claim.

Do not create a permanent note or change `seedling / growing / evergreen` status from this report. Apply those changes only when the user explicitly requests them through `permanent-note` or `review-zettelkasten`.

For reusable workflow work, update or create:

- a workflow note in the vault
- this skill or its references
