import { readFileSync, writeFileSync } from 'node:fs'
const lex = JSON.parse(readFileSync('/Users/taez/Projects/obsidian/.agents/skills/taez-insight-blog-writer/references/anti-slop-lexicon.md','utf8').match(/```json\s*\n([\s\S]*?)\n```/)[1])
const pats = lex.patterns.filter(p=>['lets-explore','preview-sentence'].includes(p.id)).map(p=>new RegExp(p.pattern))
const U = JSON.parse(readFileSync('exp5_unseen_jev.json','utf8'))
writeFileSync('exp5_unseen_regex.json', JSON.stringify(U.map(r=>pats.some(re=>re.test(r.sentence)))))
