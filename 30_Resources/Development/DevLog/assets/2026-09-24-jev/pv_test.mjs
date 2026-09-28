import { readFileSync } from 'node:fs'
const lets = new RegExp("(함께|한번|한 번|이제|지금부터)?\\s*(살펴|알아|들어가)\\s*(봅시다|보시죠|보겠습니다|보자|볼까요)", "g")
const pv = new RegExp("((살펴|알아|다뤄)\\s?(봅니다|보려\\s?한다|보려\\s?합니다)|다룹니다|다루겠습니다|다룰\\s?예정입니다|(만들어|그려|넘어가|구조화\\s?해|나누어|정리해)\\s?(보자|봅시다|가겠다|가겠습니다))(?=[.!…]*(\\s|$))", "g")
const S = JSON.parse(readFileSync('exp4_sample.json','utf8'))
const P = new Set(JSON.parse(readFileSync('exp4_labels.json','utf8')).preview)
const hit = (s) => (s.match(pv)||[]).length>0 || (s.match(lets)||[]).length>0
const pred = S.filter(r=>hit(r.sentence)).map(r=>r.id)
console.log('sample: pred', pred.length, 'tp', pred.filter(i=>P.has(i)).length, 'fp', pred.filter(i=>!P.has(i)), 'fn', [...P].filter(i=>!pred.includes(i)))
console.log('pv-only hits', S.filter(r=>(r.sentence.match(pv)||[]).length && !(r.sentence.match(lets)||[]).length).map(r=>r.id))
