# Domestic Korean Tech Blog Benchmark

Use this reference when editing Korean company-facing technical blog posts, especially when the user asks for publication polish, domestic tech blog comparison, or sentence rhythm review.

This is a benchmark, not a house style to copy. Preserve TaeZ's authorial judgment and concrete work evidence.

## Source Set

Representative domestic references:

- Toss Tech: `https://toss.tech/article/skill-quality-rubric`
- Toss Tech: `https://toss.tech/article/41789`
- Woowahan Tech: `https://techblog.woowahan.com/26177/`
- Woowahan Tech: `https://techblog.woowahan.com/25189/`
- Banksalad Tech: `https://blog.banksalad.com/tech/techspec-is-not-doc/`
- Kakao Tech: `https://tech.kakao.com/`
- Hyperconnect Tech Blog: `https://hyperconnect.github.io/`

Refresh sources with web search when the user asks for the latest comparison or source-backed recommendations.

## Structural Patterns

- Start from friction, not from a concept. Good openings show a message, review scene, repeated annoyance, outage moment, or failed assumption before naming a tool or theory.
- Name the framework after the reader recognizes the problem. Concepts should feel discovered, not imported.
- Use section titles that answer the reader's next question: why it failed, where the cost moved, what criterion separated cases, when to apply it.
- Move from lived episode to reusable criterion. A strong post leaves a practical decision rule, checklist, metric boundary, or operating model.
- Keep one main concept. Adjacent concepts should be symptoms, evidence, or implementation details, not co-equal theses.

## Sentence And Rhythm Patterns

- Prefer short paragraphs with one job. A paragraph should usually handle one of: scene, problem, cause, contrast, definition, example, implication.
- Split 350+ character paragraphs unless the density is intentional, such as a table explanation, code-adjacent bullet, or tightly scoped example.
- Put the topic sentence first when the paragraph is technical. Then support it with one concrete detail.
- Use specific workplace nouns over abstract nouns: PR, review, diff, rollback, migration, incident, log, test result, dashboard, template, meeting note.
- Avoid stacking explanation layers in one sentence. If a sentence contains definition, reason, exception, and consequence, split it.
- Let examples do work. A screenshot, code block, PR template, metric, or incident timeline can replace a paragraph of explanation.

## Company Blog Tone

- Be restrained. Avoid heroic language, trend slogans, and consulting-style frameworks.
- Use research sparingly. Cite only when it strengthens a claim already earned by the article's own scene.
- Keep personal voice, but attach it to changed judgment: "I expected X; what blocked us was Y."
- Avoid generic AI commentary. The point is not that "humans still matter"; the point is which responsibility, boundary, or system must change.
- Do not over-explain familiar engineering concepts to engineers. Explain only the local decision, boundary, or tradeoff.

## Publication Review Checklist

Before finalizing a Korean company tech blog post, check:

- Opening: does the first section show a concrete friction before using the main framework?
- Thesis: can the article be reduced to one sentence with `what changed -> where cost moved -> what structure prevents it`?
- Concept load: is there one main frame and at most two supporting terms?
- Evidence: does each citation, screenshot, code block, or metric directly support a nearby paragraph?
- Paragraph density: are 350+ character prose paragraphs split or intentionally dense?
- Rhythm: do long paragraphs alternate with short landing sentences?
- Takeaway: does the reader leave with one usable question, standard, or workflow?
- Ending: does the conclusion return to the opening problem instead of opening a new concept?
