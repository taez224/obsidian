import { readFileSync } from 'node:fs'
const END = "(?=[.!…]*(\\s|$))"
const PV2 = [
  // 1. 청유형 종결: 튜토리얼 단계 전환
  "(보|하|들|가|오)자" + END,
  // 2. 예정·의도 종결. '~려 한다'는 글을 다루는 동사로 한정한다
  "(예정(입니다|이다)?|고자\\s?(합니다|한다)|(다루|설명하|정리하|소개하|알아보|살펴보|이야기하|풀어보)려\\s?(합니다|한다)|보겠(습니다|다)|차례(입니다|다))" + END,
  // 3. 다음 글·편, 이번 글이 주어
  "(다음\\s?(글|편(?!집)|포스트)|(이번|이)\\s?(글|편|포스트|시리즈)에서는)",
  // 4. 글이 자기를 서술
  "(소개합니다|다룹니다|다루겠습니다|(살펴|알아|다뤄)\\s?봅니다)" + END,
].join("|")
const re = new RegExp(PV2)
const lets = new RegExp("(함께|한번|한 번|이제|지금부터)?\\s*(살펴|알아|들어가)\\s*(봅시다|보시죠|보겠습니다|보자|볼까요)")
const hit = s => re.test(s) || lets.test(s)
const S = JSON.parse(readFileSync('exp4_sample.json','utf8')), P = new Set(JSON.parse(readFileSync('exp4_labels.json','utf8')).preview)
const H = JSON.parse(readFileSync('exp5_holdout.json','utf8')), HP = new Set(JSON.parse(readFileSync('exp5_labels.json','utf8')).preview)
const sc = (X, G) => { const p = X.filter(r=>hit(r.sentence)).map(r=>r.id); return `pred=${p.length} tp=${p.filter(i=>G.has(i)).length} fp=[${p.filter(i=>!G.has(i))}] fn=[${[...G].filter(i=>!p.includes(i))}]` }
console.log('design60 :', sc(S,P)); console.log('holdout40:', sc(H,HP))
const U = JSON.parse(readFileSync('exp5_unseen_jev.json','utf8'))
const hits = U.filter(r=>hit(r.sentence))
console.log(`sweep: regex=${hits.length} jev>=0.8 among regex=${hits.filter(r=>r.preview>=0.8).length} jev<0.5 among regex=${hits.filter(r=>r.preview<0.5).length} | jev>=0.88 total=${U.filter(r=>r.preview>=0.88).length} caught=${U.filter(r=>r.preview>=0.88&&hit(r.sentence)).length}`)
console.log('regex hits with jev<0.5:'); hits.filter(r=>r.preview<0.5).forEach(r=>console.log(`  ${r.preview.toFixed(2)} ${r.sentence.slice(0,80)}`))
console.log('PATTERN_JSON=' + JSON.stringify(PV2))
