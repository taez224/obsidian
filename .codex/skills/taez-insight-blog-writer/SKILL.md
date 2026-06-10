---
name: taez-insight-blog-writer
description: Use when TaeZ wants to turn rough Korean notes, work experiences, engineering decisions, research findings, or half-written drafts into a distinctive Korean technical blog post with personal branding, original insight, and anti-slop editorial standards. Trigger for requests about "내 글", "퍼스널 브랜딩", "인사이트 있는 글", "기술블로그", "초안", "윤문", "구조 리팩토링", "deep research 기반 글쓰기", "나만의 관점", or "발행 가능한 글".
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
- latest `20_Projects/blog/AI로 개인은 빨라졌는데, 팀 진척은 그대로인 이유*.md`

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

Before finalizing, check:

- Could a reader get this by asking ChatGPT a broad question? If yes, add personal evidence or a sharper claim.
- Does every research citation do work? Remove decorative citations.
- Is there a before/after in TaeZ's thinking? If not, it may read like a report.
- Is the practical takeaway about behavior or structure, not just attitude?
- Are output metrics separated from actual capability, learning, reliability, or user value?
- Are AI-generated phrases flattened out without making the prose bland?

### 7. Editing stance

When reviewing an existing draft:

- Lead with structural problems, repeated claims, weak transitions, and unsupported leaps.
- Preserve strong local phrasing unless it damages clarity.
- Make small patches when the draft is close; suggest restructuring only when the argument is genuinely confused.
- For Obsidian posts, preserve frontmatter, wikilinks, markdown tables, image links, and `## 연결된 노트`.

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
