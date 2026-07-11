---
name: taez-insight-blog-writer
description: Use when TaeZ wants to turn rough Korean notes, work experiences, engineering decisions, research findings, or half-written drafts into a distinctive Korean technical blog post with personal branding, original insight, company-tech-blog polish, and anti-slop editorial standards. Trigger for requests about "내 글", "퍼스널 브랜딩", "인사이트 있는 글", "기술블로그", "회사 기술블로그", "국내 기술블로그", "초안", "윤문", "구조 리팩토링", "deep research 기반 글쓰기", "나만의 관점", or "발행 가능한 글".
---

# TaeZ Insight Blog Writer

## Purpose

Help TaeZ write Korean technical blog posts that feel earned, specific, and publishable: lived experience first, changed judgment second, reusable framework third, prose last.

Default reader: practical software engineers. Default author position: 실전형 사상가 - someone who turns hands-on engineering, platform, workflow, team, career, or product experiences into reusable insight.

## Operating Principles

- Do not produce generic AI thought-leadership. A post needs a lived scene, a concrete tradeoff, and a claim that survives objections.
- Preserve TaeZ's recurring lenses when relevant, but do not force them: platform-as-enablement, workflow as operating system, team capability over individual output, evidence-backed reflection, dogfooding, responsibility boundaries, learning loops.
- Treat AI assistance as acceptable. Slop is not "AI was used"; slop is "no authorial judgment, no context, no accountable takeaway."
- Structure before sentence polish. If the argument is weak, do not run a humanizing pass yet.
- Keep Korean natural and technically literate. Avoid over-explaining familiar engineering ideas.

## 파이프라인 오케스트레이션

이 스킬은 블로그 파이프라인의 단일 진입점이다. 과거 문서의 `blog-polish`와 `blog-pipeline`은 사용하지 말고, 아래 자산만 사용한다.

### 라우팅

- **vault 노트 기반**(Slipbox·DevLog·Periodic·초안) → 아래 vault 파이프라인을 사용한다.
- **git 저장소·커밋·설계문서 기반** → `git log`·`git diff`·설계문서에서 사건·전환·일반화를 추출한 뒤 직접 초안 경로로 합류한다.

### vault 파이프라인 (`.claude/workflows/`)

| 단계 | 워크플로 | 핵심 산출 |
| --- | --- | --- |
| ① 앵글 | `blog-angle-mine` | 앵글 후보. 사람이 seed 노트를 직접 만든다. |
| ② 리서치 | `blog-research-gather` | Slipbox 리서치와 반례 수집. |
| ③ 작곡 | `blog-recompose` | 선행글·초안 재작곡. |
| ③' 직접 초안 | 이 스킬의 article spine | 새 글을 직접 쓴다. |
| ④ 사람 게이트 | `references/slop-gate.md` | 7항목 사인오프. |
| ⑤ 검수·윤문 | `blog-review-polish` | 사실 검증·6인 패널·윤문·최종 게이트. |
| 상시 | `blog-slop-lint.mjs` | 결정론적 슬롭 린트. |

### 단일 출처 파일 (`references/`)

- `voice-profile.md` — 지킬 목소리 DNA.
- `anti-slop-lexicon.md` — 금지표현·문장부호의 단일 출처. lint와 AI-티 감별사가 함께 사용한다.
- `slop-gate.md` — 발행 전 사람 사인오프.
- `amplifier-lenses.md` — 쓰기 전 앵글과 다듬기 단계의 가치 증폭 렌즈.

## Workflow

### 1. Clarify the article contract

If missing, ask for only the information needed:

- target reader
- author position
- publication surface
- source material
- desired artifact: outline, draft, revision, review, or reusable workflow

If the user already provides direction, proceed without asking.

### 2. Build the personal evidence base

Search the vault before writing. Prefer these anchors when relevant:

- `20_Projects/blog/60일간의 AI 에이전틱 워크플로.md`
- `01_Slipbox/AI 시대 플랫폼팀은 어떻게 진화하는가.md`
- latest `20_Projects/blog/AI로 빨라진 개인, 소화하지 못하는 팀.md`

Extract:

- actual episode: what happened
- prior belief: what TaeZ thought then
- changed belief: what TaeZ thinks now
- artifact evidence: commands, PRs, diagrams, workflow names, failed experiments
- transferable implication: what other engineers can reuse

If the topic is not AI/platform related, search for the topic-specific project notes, daily notes, resources, or slipbox entries instead. The invariant is not the topic; the invariant is TaeZ's observed change in judgment.

### 3. Deep research, but only after the thesis shape exists

Use current external research when claims are time-sensitive or trend-dependent. Prefer primary or high-signal sources: papers, official engineering posts, original case studies, standards, and respected practitioner essays.

Load `references/anti-slop-research.md` only when the topic touches AI slop, workslop, writing quality, developer content saturation, or "AI-generated but valuable" distinctions.

Research should sharpen the user's claim, not turn the post into a literature review.

For company-facing Korean tech blog polish, or when the user mentions domestic tech blogs such as Toss, Woowahan, Banksalad, Kakao, Naver D2, LINE/LY, Daangn, or Hyperconnect, load `references/domestic-tech-blog-benchmark.md`. Use it as a rhythm and density benchmark, not as a template to imitate.

### 4. Force an original thesis

Before drafting, state the article's one-line thesis in this form:

```text
Most people say X. My experience suggests Y. The practical move is Z.
```

Reject theses that are only:

- "AI is useful but risky"
- "Use AI responsibly"
- "Humans still matter"
- "Tools are not enough"
- "Communication is important"
- "Culture matters"
- "We need better process"

Make the thesis more specific by adding: what changed, what cost moved, who pays it, what the user learned, and what structure prevents the failure.

이 단계에서 `references/amplifier-lenses.md`의 생성형 렌즈(이해관계·통찰 독창성·브랜드)를 브레인스토밍으로 함께 돌린다. 이 요소들은 윤문으로 나중에 붙이지 않는다.

### 5. Use the TaeZ article spine

Default structure:

1. **Scene** - a real engineering moment, not a generic trend opening.
2. **Tension** - why the obvious interpretation is incomplete.
3. **Personal turn** - what TaeZ tried, believed, or changed.
4. **Framework** - name the reusable concept.
5. **Evidence** - research, data, or artifact evidence that support or constrain the claim.
6. **Counterargument** - the strongest objection and the honest boundary.
7. **Operating model** - what a team should do differently.
8. **Landing** - a concise conclusion that returns to the opening question.

### 6. Apply the anti-slop tests

먼저 `node .claude/workflows/blog-slop-lint.mjs "<file>"`로 기계적 슬롭을 확인한다. high는 대체로 제거하고, lint가 판단할 수 없는 깊이·1인칭·반례는 `references/slop-gate.md`에서 사람이 판단한다.

Before finalizing, check:

- Could a reader get this by asking ChatGPT a broad question? If yes, add personal evidence or a sharper claim.
- Does every research citation do work? Remove decorative citations.
- Is there a before/after in TaeZ's thinking? If not, it may read like a report.
- Is the practical takeaway about behavior or structure, not just attitude?
- Are output metrics separated from actual capability, learning, reliability, or user value?
- Are AI-generated phrases flattened out without making the prose bland?

For company-tech-blog publication checks, run a domestic-tech-blog rhythm pass:

- Does the opening start from a concrete friction before naming a framework?
- Does each paragraph do one job: scene, problem, cause, criterion, example, or landing?
- Are 350+ character paragraphs split unless they are code, tables, or intentional bullets?
- Is the main concept singular, with adjacent concepts demoted to symptoms, evidence, or operating criteria?
- Does the article leave one usable criterion, question, or workflow instead of many abstract lessons?

### 7. Editing stance

When reviewing an existing draft:

- Lead with structural problems, repeated claims, weak transitions, and unsupported leaps.
- Preserve strong local phrasing unless it damages clarity.
- Make small patches when the draft is close; suggest restructuring only when the argument is genuinely confused.
- For Obsidian posts, preserve frontmatter, wikilinks, markdown tables, image links, and `## 연관된 노트`.

## Output Formats

For a new article, produce:

- one-line thesis
- title options if needed
- outline
- draft or patch
- source notes

For a review, produce:

- publication-readiness verdict
- top 3 structural issues
- concrete rewrite suggestions
- optional direct patch

For reusable workflow work, update or create:

- a workflow note in the vault
- this skill or its references
