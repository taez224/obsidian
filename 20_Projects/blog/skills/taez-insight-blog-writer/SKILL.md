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

## 파이프라인 오케스트레이션 (단일 진입점)

이 스킬이 블로그 파이프라인의 **단일 두뇌**다. 아래 워크플로·게이트·단일출처 파일을 알고, 소재
종류에 따라 라우팅한다. (드리프트 주의: 과거 문서가 가리키던 `blog-polish`/`blog-pipeline`은
없는 이름이다. 실제 자산은 아래가 전부다.)

### 라우팅 — 소재가 무엇인가

- **vault 노트 기반**(Slipbox·DevLog·Periodic·초안) → 아래 vault 파이프라인.
- **git 저장소/커밋/설계문서·README 기반**(Spec-driven) → 이 스킬이 직접 처리한다.
  `git log`/`git diff`/설계문서에서 사건·전환·일반화를 추출한 뒤 ③' 직접 초안 경로로 합류한다.
  (구 전역 `taez-tech-blog` 스킬은 2026-06-10 일원화로 폐기 — 더 이상 라우팅하지 않는다.)

### vault 파이프라인 (`.claude/workflows/`)

런타임 워크플로 러너로 이름+args를 넘겨 실행한다.

| 단계 | 워크플로 | 핵심 args | 산출 |
| --- | --- | --- | --- |
| ① 앵글 | `blog-angle-mine` | `{sources?, count?, focus?}` | 앵글 후보 리포트(파일 안 씀). **사람이** seed 노트를 직접 만든다(human gate) |
| ② 리서치 | `blog-research-gather` | `{seed\|topic, lenses?}` | Slipbox 리서치 노트. **반례 의무 수집** 포함 |
| ③ 작곡 | `blog-recompose` | `{experienceSource, conceptSource, substanceSource, output, brandLead?}` | 선행글+초안 재작곡(Mine→Outline→판정→Compose→Gate) |
| ③' 직접 초안 | (이 스킬의 article spine) | — | 새 글을 직접 쓸 때 |
| ④ 사람 게이트 | `_slop-gate.md` | (수동) | 7항목 사인오프 → `slop_check: passed` 전엔 ⑤로 못 간다 |
| ⑤ 검수·윤문 | `blog-review-polish` | `{file, workCopy?, stages?, maxRounds?}` | Fact-check→Research→6인 패널→윤문 루프→Final-gate. **Final-gate에 결정론 슬롭 린트 자동 포함** |
| 상시 | `blog-slop-lint.mjs` | `node ...blog-slop-lint.mjs "<file>" [--json]` | LLM 0의 결정론 린트. 언제든 단독 실행 |

### 단일 출처 파일 (`20_Projects/blog/`)

- `_voice-profile.md` — 지킬 목소리 DNA.
- `_anti-slop-lexicon.md` — **피할** 금지표현·문장부호 단일 출처. lint와 ⑤의 "한국어 AI-티
  감별사" 페르소나가 *이 파일 하나*를 공유한다. 패턴을 고치려면 여기만 고친다.
- `_slop-gate.md` — 발행을 막는 사람 사인오프(깊이·1인칭·반례 — lint가 못 보는 것).

### manifesto 4규칙 → 이 파이프라인 매핑

1. **Spec-driven Post Draft** → git/설계문서 소재도 이 스킬이 직접 담당(구 `taez-tech-blog` 폐기).
2. **Authentic Learning History**(진짜 삽질) → `_slop-gate` 1·2번(구체 장면·1인칭 실패담) 필수.
3. **Opinionated Assertions**(논쟁적 관점) → `_slop-gate` 4·5번(통념 반례·강한 POV), ② 반례 의무.
4. **Robotic Detector Verification** → 외부 SaaS(GPTZero 등) 대신 **로컬 결정론 린트
   `blog-slop-lint.mjs`**(재현 가능·0원)로 대체 + `_slop-gate` 6번 **음독 테스트**(사람).

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
- latest `20_Projects/blog/AI로 개인은 빨라졌는데, 왜 팀의 속도는 그대로일까.md`

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

먼저 결정론 린트를 돌려 기계적 슬롭을 걷어낸 뒤, 사람이 봐야 할 깊이 질문으로 넘어간다.

- 기계: `node .claude/workflows/blog-slop-lint.mjs "<file>"` — `_anti-slop-lexicon.md` 기준 금지표현·
  문장부호·밀도 검출. high는 거의 항상 제거. (단 lint는 *표면*만 본다 — 깊이·1인칭·반례는 사람 몫)

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
