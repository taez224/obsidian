import { readFileSync } from 'node:fs'
const lex = JSON.parse(readFileSync('/Users/taez/Projects/obsidian/.agents/skills/taez-insight-blog-writer/references/anti-slop-lexicon.md','utf8').match(/```json\s*\n([\s\S]*?)\n```/)[1])
const pats = lex.patterns.filter(p=>['lets-explore','preview-sentence'].includes(p.id)).map(p=>new RegExp(p.pattern))
const H = JSON.parse(readFileSync('exp5_holdout.json','utf8'))
console.log(JSON.stringify(H.filter(r=>pats.some(re=>re.test(r.sentence))).map(r=>r.id)))
