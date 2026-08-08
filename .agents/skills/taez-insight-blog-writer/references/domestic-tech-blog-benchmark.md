# Domestic Korean Tech Blog Benchmark

Use this reference for Korean company-facing technical blog outlines, title or heading review, and publication polish. It is a current comparison surface, not a house style to copy. Preserve TaeZ's thesis and work evidence.

## Sampling current titles

Prefer official RSS feeds because they expose recent titles without search-ranking bias:

- Toss Tech: `https://toss.tech/rss.xml`
- Woowahan Tech: `https://techblog.woowahan.com/feed/`
- Kakao Tech: `https://tech.kakao.com/feed/`
- Daangn: `https://medium.com/feed/daangn`
- LY Corporation: `https://techblog.lycorp.co.jp/ko/feed/index.xml`

When the user asks for current comparison or source-backed title recommendations:

1. Sample 10–20 recent titles across at least three publications relevant to the article type.
2. Record the sampling date and treat observed patterns as a snapshot, not a permanent rule.
3. If a feed is blocked, redirected, stale, or unavailable, use the publication's official archive, category, or tag page. An inaccessible feed does not imply that no recent posts exist.
4. Open representative article bodies before borrowing structural lessons. Titles alone do not reveal whether a post is an engineering case study, perspective essay, series installment, or event article.

## Title patterns

Common patterns include:

- a concrete technology, artifact, or problem joined to a reason, process, or outcome;
- a question that names the reader's actual uncertainty;
- a colon or dash joining the topic to a concrete case;
- experience suffixes such as `개발기`, `도입기`, `적용기`, or `해결기` when the article is genuinely a build or incident story;
- a scale or measured outcome when the number is verified and central;
- a restrained thesis followed by the system or project that earned it.

These are observations, not required templates:

- Proper nouns and technology names are common but not mandatory.
- Perspective articles can use thesis-led, conversational, or aphoristic titles.
- Do not infer a prohibition from a pattern missing in a small sample.
- Do not force a case-study suffix onto a reflective article or a question onto a conclusion-led article.

Judge a title by article alignment:

- Does it point to the actual climax or landing rather than only the opening scene?
- Does the body deliver the promised problem, artifact, decision, or insight?
- Is it distinct from every section heading?
- If it foregrounds a source or trend, is that source truly the article's protagonist rather than supporting evidence?
- Does it sound natural on the chosen publication surface without erasing TaeZ's recurring voice?

When alternatives help, produce 2–3 strategies rather than many cosmetic variants. For each, state whether it foregrounds the scene, the reader's question, or the article's conclusion.

## Structural patterns

- Start from friction, not from a concept. Good openings show a message, review scene, repeated annoyance, outage moment, or failed assumption before naming a tool or theory.
- Name the framework after the reader recognizes the problem. Concepts should feel discovered, not imported.
- Use section titles that answer the reader's next question. A scene section can name the artifact or failure; a conceptual section can use a restrained thesis; the climax should expose the actual technical decision or evidence.
- Move from lived episode to reusable criterion. A strong post leaves a practical decision rule, checklist, metric boundary, or operating model.
- Keep one main concept. Adjacent concepts should be symptoms, evidence, or implementation details, not co-equal theses.

## Sentence and rhythm patterns

- Prefer short paragraphs with one job. A paragraph should usually handle one of: scene, problem, cause, contrast, definition, example, implication.
- Split 350+ character paragraphs unless the density is intentional, such as a table explanation, code-adjacent bullet, or tightly scoped example.
- Put the topic sentence first when the paragraph is technical. Then support it with one concrete detail.
- Use specific workplace nouns over abstract nouns: PR, review, diff, rollback, migration, incident, log, test result, dashboard, template, meeting note.
- Avoid stacking explanation layers in one sentence. If a sentence contains definition, reason, exception, and consequence, split it.
- Let examples do work. A screenshot, code block, PR template, metric, or incident timeline can replace a paragraph of explanation.

## Company blog tone

- Be restrained. Avoid heroic language, trend slogans, and consulting-style frameworks.
- Use research sparingly. Cite only when it strengthens a claim already earned by the article's own scene.
- Keep personal voice, but attach it to an observed decision, friction, or changed judgment.
- Avoid generic AI commentary. Name which responsibility, boundary, or system changed.
- Do not over-explain familiar engineering concepts to engineers. Explain only the local decision, boundary, or tradeoff.

## Publication review checklist

- Title: does it match the article type, climax, and landing without duplicating a section title?
- Headings: does each answer the reader's next question or expose the local artifact, rather than promote a supporting source into the thesis?
- Opening: does the first section show a concrete friction before using the main framework?
- Thesis: can the article be reduced to one sentence naming what changed and why it matters?
- Concept load: is there one main frame and at most two supporting terms?
- Evidence: does each citation, screenshot, code block, or metric directly support a nearby paragraph?
- Paragraph density: are 350+ character prose paragraphs split or intentionally dense?
- Takeaway: does the reader leave with one usable question, standard, or workflow?
- Ending: does the conclusion resolve the article's real problem instead of opening a new concept?
