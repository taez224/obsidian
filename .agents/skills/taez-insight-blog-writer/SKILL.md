---
name: taez-insight-blog-writer
description: Use when TaeZ explicitly asks to turn vault notes, work experience, engineering decisions, research, or a substantial draft into a Korean blog outline or article, substantially restructure or review an article for publication, or review and select the title and section headings of an existing article. Default to an outline-first collaboration that leaves prose authorship to TaeZ; write a full draft only when explicitly requested. Choose the writing contract by publication surface, including Brunch or personal essays and company technical blogs. Do not trigger for isolated sentence-level polish, ordinary Obsidian note editing, or exploratory conversation that has not become an article task.
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

| 단계 | 워크플로 | 핵심 산출 |
| --- | --- | --- |
| ① 앵글 | `blog-angle-mine` | 앵글 후보. 사람이 seed 노트를 직접 만든다. |
| ② 리서치 | `blog-research-gather` | Resources 리서치 노트와 반례 수집. |
| ③ 구조 | `blog-recompose`의 outline-only 기본값 또는 직접 구조화 | 한 줄 논지, 절별 역할, 근거와 경계를 담은 사용자 집필용 아웃라인. |
| ④ 사용자 집필 | 사람 게이트 | TaeZ가 아웃라인을 바탕으로 본문을 직접 쓴다. AI는 여기서 자동으로 전문을 이어 쓰지 않는다. |
| ④' 공동 초안 | `blog-recompose`의 `writeFullDraft: true` 또는 직접 작성 | 사용자가 전문 초안을 명시적으로 요청했을 때만 실행한다. |
| ⑤ 기본 검수 | `blog-review-polish`의 `light` | 사용자가 본문을 쓴 뒤 결정론적 lint + 편집 관점 1회. |
| ⑥ 발행 게이트 | `references/slop-gate.md` + `blog-review-polish` 선택 단계 | 사용자가 발행 전 최종 검수를 요청할 때만 실행. 브런치는 `light`에 필요한 fact-check만 더하고, 회사 기술 블로그의 전체 검수에만 `mode: "publish"`를 사용. |
| 상시 | `blog-slop-lint.mjs` | 결정론적 슬롭 린트. |

### 런타임별 실행 경로

- **Claude Code**: 위 `.claude/workflows/`는 Claude 런타임에서 파이프라인을 가속하는 실행 자산이다.
- **Codex**: 같은 근거와 글의 역할을 따르되, vault 검색 → 논지·구조 설계 → 사용자 집필에서 기본적으로 멈춘다. 사용자가 전문이나 패치를 요청했을 때만 한국어 초안 점검과 `node .claude/workflows/blog-slop-lint.mjs "<file>"`로 이어간다. 사람 게이트와 전체 검수는 발행 직전에만 사용하며 Claude 전용 워크플로를 직접 실행할 필요는 없다.

두 런타임 모두 이 스킬의 `references/`와 본문의 판단 기준을 공유한다.

### 단일 출처 파일 (`references/`)

- `voice-profile.md` — 지킬 목소리 DNA.
- `anti-slop-lexicon.md` — 금지표현·문장부호의 단일 출처. lint와 AI-티 감별사가 함께 사용한다.
- `korean-first-draft.md` — 새 글을 쓸 때 읽는 번역투·정형 문장 예방 규칙. 윤문용 전체 분류표가 아니다.
- `slop-gate.md` — 발행 전 사람 사인오프.
- `amplifier-lenses.md` — 쓰기 전 앵글과 다듬기 단계의 가치 증폭 렌즈.
- `domestic-tech-blog-benchmark.md` — 회사 기술 블로그의 최신 제목·구조·문장 리듬 표본.

## Workflow

### 1. Clarify the article contract

If missing, ask for only the information needed:

- target reader
- author position
- publication surface
- source material
- desired artifact: outline, draft, revision, review, or reusable workflow

If the user already provides direction, proceed without asking.

If the user says they will write the article themselves, or does not explicitly ask for full prose, choose `outline` as the default artifact. Stop after delivering or saving the outline. Do not continue into a full draft in the same turn merely because enough material exists.

새 글 작성, 본문의 대규모 재작성, 발행 전 종합 검토, 기존 글의 제목·헤딩 종합 검토에서는 `references/voice-profile.md`를 읽는다. 단순 문장 단위 수정에는 불러오지 않는다.

Choose the contract by publication surface before selecting a structure.

- **Brunch·personal essay**: preserve the writer's question, lived texture, and reading rhythm. A named framework, research section, counterargument, or operating model is optional.
- **Personal technical blog**: connect an actual technical decision or failure to a reusable criterion. Add artifact evidence where it carries the argument.
- **Company technical blog**: prioritize reproducibility, factual accuracy, system context, and reader utility. Load the domestic benchmark only here or when explicitly requested.

Before building the evidence base for a series article:

- Inspect the target article frontmatter and the user request for a `series` name.
- If a series is identified, read `20_Projects/blog/<series>.md` first. If that exact file does not exist, search project-note titles and aliases for the series name rather than inventing a new hub.
- Treat the series hub as the editorial source of truth for the central question, article role, order, and unresolved follow-ups. Do not silently change the series plan; report a proposed hub update when the article reveals a meaningful change.
- When a series article is marked `published` with a confirmed `published` date, sync the hub's `last_published` to the latest known publication date. Change the hub's `status` or `ended` only when the user explicitly decides to pause or complete the series.

### 2. Build the personal evidence base

Search the vault before writing: the topic's project notes, previous posts in `20_Projects/blog/`, related Slipbox claims, and counterexamples when the claim needs them. Do not rely on a fixed anchor list; find the evidence that fits this article. The invariant is source-grounded authorial judgment, whether it changed or became clearer.

Before deep research or outlining, run an adjacency check regardless of whether the article belongs to a series:

- Use exact title/term search and semantic claim search to shortlist the 1–3 nearest canonical blog posts. Exclude archives and duplicate drafts.
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

Verify claims before promoting them into the outline:

- Confirm numbers, direct quotations, and named research findings in the primary source. A secondary source attaching an institution's name to a number is not enough.
- Record the source publication date and, when relevant, the data-collection window, product or domain, sample, and stated limitations. Recent publication does not make a fast-changing product observation durable.
- Treat 403 responses, JavaScript shells, paywalls, and missing search results as access failures, not evidence that a source or passage does not exist. Try an official PDF, DOI, repository, press release, RSS feed, or another first-party route; if still unresolved, label it `unresolved` rather than `false`.
- For laws and policy schedules, distinguish proposal, provisional agreement, legislative adoption, final approval, official publication, entry into force, and application date. Verify the current stage in an official source.
- A finding can be accurate and still be the wrong protagonist. Do not turn a source's observation into the article title or a section heading unless it expresses TaeZ's claim; otherwise keep it as nearby evidence with scope limits.

Load `references/anti-slop-research.md` only when the topic touches AI slop, workslop, writing quality, developer content saturation, or "AI-generated but valuable" distinctions.

Research should sharpen the user's claim, not turn the post into a literature review.

For company-facing Korean tech blog polish, or when the user mentions domestic tech blogs such as Toss, Woowahan, Banksalad, Kakao, Naver D2, LINE/LY, Daangn, or Hyperconnect, load `references/domestic-tech-blog-benchmark.md`. Use it as a rhythm and density benchmark, not as a template to imitate.

### 4. State the article's claim in plain language

Before drafting, state what this article leaves with the reader in one sentence. Several framings are available; pick the one the material actually supports rather than reaching for the first:

```text
판단 전환:  People commonly see X. This experience showed Y. That changes Z.
비용 노출:  X was the right call. It billed Y, paid by Z.
경계 발견:  X holds here and breaks there. The line is Y.
질문 교체:  I asked X. Answering it showed X was the wrong question. The better question was Y.
```

The first framing fits only when a genuine change of judgment or disagreement defines the article. An article whose judgment never changed is not weaker — it is a different article, and forcing a reversal into it manufactures a fake turn.

Do not force a conventional view, personal turn, or practical move into a reflective essay. Reject claims that remain generic, such as:

- "AI is useful but risky"
- "Use AI responsibly"
- "Humans still matter"
- "Tools are not enough"
- "Communication is important"
- "Culture matters"
- "We need better process"

Make the claim specific with the subset that matters here: what changed, what cost moved, who pays it, what the user learned, or what structure prevents the failure.

이 단계에서 `references/amplifier-lenses.md`의 생성형 렌즈(이해관계·통찰 독창성·브랜드)를 브레인스토밍으로 함께 돌린다. 이 요소들은 윤문으로 나중에 붙이지 않는다.

### 5. Build only the structure this article needs

Choose the movement the material supports. This is a menu, not a ranking — the list exists because a writer who reaches for the same movement every time produces articles that feel identical even when the evidence is different.

- **판단이 바뀐 이야기** — 착각 → 부분 성공 인정 → 반전 → 원칙. 필자가 실제로 생각을 바꿨고 전후가 근거로 남아 있을 때.
- **비용을 따라가는 이야기** — 결정 → 그 결정이 청구한 대가 → 대가를 감수할지 다시 고르기. 판단은 그대로인데 가격표가 보이기 시작했을 때.
- **실패에서 시작하는 이야기** — 무너진 장면 → 무너진 이유 → 바꾼 것 → 아직 못 고친 것. 실제로 무언가 부러졌을 때.
- **두 사례를 부딪히는 이야기** — 원칙이 통한 사례와 통하지 않은 사례 → 경계선 → 경계선의 근거. 진짜 반례가 재료에 있을 때.
- **질문이 바뀌는 이야기** — 처음 던진 질문 → 답하다 질문이 틀렸음을 발견 → 새 질문. 글의 가치가 답이 아니라 재구성에 있을 때.

Add a framework, technical evidence, counterargument, or operating model only when it carries the claim. Do not report omitted sections or fill them with boilerplate.

### 5.1 Stop at a writer-owned outline by default

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
- Keep research as evidence notes attached to the claim it supports. Do not turn all gathered papers into body sections.
- Mark missing personal evidence as a prompt for TaeZ to fill. Never invent a workplace scene, judgment change, result, or number.
- Do not write polished opening paragraphs, transitions, or closing prose unless explicitly requested.
- After TaeZ writes prose, review structure, evidence, repetition, and unsupported leaps first. Rewrite only the named section or sentence range they authorize; preserve manually written thought flow elsewhere.

Run a title and heading pass before handing off the outline:

- Make the article title promise the actual climax or landing, not only the opening scene or one supporting study.
- Do not reuse the article title verbatim as a section title.
- Let each section heading perform its local role: a scene heading can name the artifact or friction; a conceptual section can use a restrained thesis; a landing can be short and declarative.
- Do not require a proper noun, question, contrast, or experience suffix. For a company technical blog, compare with a current sample from `references/domestic-tech-blog-benchmark.md` and explain fit by article type.
- When options are useful, produce 2–3 meaningfully different strategies and state what part of the article each foregrounds. Do not generate a quota of cosmetic variants.

#### 연재 글의 구조

연재의 한 편을 쓸 때는 직전 1~2편을 목차가 아니라 **본문으로** 읽는다. 아래는 초안 전 선택이자 검수 시 확인 항목이며, 연재 관련 판단은 여기 모아 둔다.

- **각 편은 서로 다른 국소 결론에 착지한다.** 시즌의 중심 주제를 함께 밀 수는 있지만, 앞 편의 국소 결론을 새 소재로 다시 증명하는 데 그치면 별도 회차보다 각주에 가깝다.
- **이어짐은 재진술이 아니라 다음 문제로 표시한다.** "앞 편에서 말한 X가 여기서 이어집니다" 같은 문장으로 연결을 설명하기보다, 앞 편이 남긴 미해결 질문·비용·예외·모순 중 하나를 이번 편의 출발점으로 삼는다.
- **같은 움직임이 연속되면 재료 때문인지 습관 때문인지 확인한다.** 재료가 실제로 그렇다면 연속해도 된다. 다만 도입 장면과 마지막 문단의 역할까지 같아지면 독자에게는 같은 글이므로 둘 중 하나를 바꾼다. 다양성을 만들려고 재료에 없는 움직임을 씌우지는 않는다.
- **원자료의 마찰을 지우지 않는다.** 실패·비용·한계·미해결 지점이 실제로 있는데 원칙이 매번 통하는 장면만 남기지 않았는지 확인한다. 없으면 만들지 않는다.
- 허브의 회차 역할과 실제 초안의 착지점이 어긋나면 허브 갱신 후보로 보고한다.
- 파일 단위 lint는 편 사이의 반복을 보지 못한다. 이 확인은 사람이나 검수 단계에서만 걸린다.

### 5.2 Draft natural Korean before polishing

사용자가 전문 초안이나 본문의 대규모 재작성을 명시적으로 요청했을 때만 먼저 `references/korean-first-draft.md`를 읽고 다음을 적용한다. 이는 사후 윤문이 아니라 초안의 기본 품질 기준이다.

- 정의·프레임보다 실제 장면, 구체 주어, 행동 동사로 문단을 시작한다.
- `~에 대해`, `~를 통해`, `~에 있어서`, `~와 관련하여`, 불필요한 피동과 긴 관형어를 그대로 옮기지 않는다. 자연스러운 조사·능동형·짧은 문장으로 다시 쓴다.
- `중요한 것은`, `주목할 점은`, `따라서`, `결론적으로`, `X가 아니라 Y` 같은 문장 공식으로 논지를 운반하지 않는다. 비용·장면·인과를 직접 쓴다.
- 문단마다 같은 길이·종결어미·접속사 리듬을 반복하지 않는다. 다만 일부러 문학적인 표현, 비유, 구어체를 덧붙여 해결하지도 않는다.
- 고유명사·수치·날짜·직접 인용·기술 약어는 바꾸지 않는다. 목록은 실제 단계·비교·선택지를 보여줄 때만 사용한다.

초안을 쓴 뒤 30초 동안 문단 첫 문장, 문두 접속사, 추상 명사 연쇄, 독립해도 의미가 남는 안내 문장을 훑는다. 발견한 문제만 고친다. 처음부터 모든 문장을 휴머나이즈하거나, 이 기준을 문장 길이·종결어미의 기계적 균일화 규칙으로 사용하지 않는다.

### 6. Apply the anti-slop tests

먼저 `node .claude/workflows/blog-slop-lint.mjs "<file>"`로 기계적 슬롭을 확인한다. high는 대체로 제거한다. `references/slop-gate.md`는 사용자가 발행 전 최종 검수를 요청했을 때만 읽고, 글의 장르와 근거에 맞는 항목만 사람이 판단한다.

`humanize-korean` 전체 워크플로는 기본 단계가 아니다. 사용자가 명시적으로 윤문을 요청했거나, 발행 직전 사람이 번역투·정형 문장을 확인했을 때만 실행한다. 이때도 의미·사실·인용은 보존하고, 초안의 논지나 장르를 바꾸지 않는다.

For a substantial draft or review, check only the applicable questions:

- Could a reader get this by asking ChatGPT a broad question? If yes, add personal evidence or a sharper claim.
- Does every research citation do work? Remove decorative citations.
- If the article claims a changed judgment, is the before/after visible?
- Is the practical takeaway about behavior or structure, not just attitude?
- Are output metrics separated from actual capability, learning, reliability, or user value?
- Are AI-generated phrases flattened out without making the prose bland?

For a series article, 5단계의 `연재 글의 구조`를 검수 항목으로 다시 훑는다. 여기서 실제로 확인할 것은 하나다 — 직전 편과 이번 편을 이어 읽었을 때 같은 악장이 반복되는가. 소재만 바뀐 채 "오해 → 사실은 아니었다 → 원칙"이 다시 돌면 구조로 돌아간다.

For company-tech-blog publication checks only, run a domestic-tech-blog rhythm pass:

- Does the title point to the article's real climax or landing, and do the section headings answer the reader's next question without repeating the title?
- Does the opening start from a concrete friction before naming a framework?
- Does each paragraph do one job: scene, problem, cause, criterion, example, or landing?
- Are 350+ character paragraphs split unless they are code, tables, or intentional bullets?
- Is the main concept singular, with adjacent concepts demoted to symptoms, evidence, or operating criteria?
- Does the article leave one usable criterion, question, or workflow instead of many abstract lessons?

### 7. Editing stance

When reviewing an existing draft:

- Lead with structural problems, repeated claims, weak transitions, and unsupported leaps.
- Treat an external review as a hypothesis. Verify its factual claims and reject changes that displace TaeZ's thesis, scene, or publication contract even when the suggested sentence is locally polished.
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

- publication-readiness verdict
- top 3 structural issues
- concrete rewrite suggestions
- optional direct patch

For a new article or substantial revision, finish with a concise `지식 환류` report:

- `사용한 Slipbox`: list only notes actually used in the article and state the usage context.
- `새 영구 노트 후보`: report reusable claims that emerged while writing as candidates only.
- If neither exists, state `환류 후보 없음` instead of forcing a link or claim.

Do not create a permanent note or change `seedling / growing / evergreen` status from this report. Apply those changes only when the user explicitly requests them through `permanent-note` or `review-zettelkasten`.

For reusable workflow work, update or create:

- a workflow note in the vault
- this skill or its references
