#!/usr/bin/env node
// blog-slop-lint — 결정론적 AI-슬롭 린트 (LLM 호출 0)
//
// 사용법:
//   node blog-slop-lint.mjs "<초안.md 절대경로>" [--lexicon <경로>] [--json]
//
// 단일 출처: 20_Projects/blog/_anti-slop-lexicon.md 의 ```json 블록(패턴/밀도/임계값).
// 이 파일은 패턴을 하드코딩하지 않는다 — lexicon 하나만 고치면 lint와 LLM 페르소나가 같이 따라온다.
//
// 검사 전 제외(오탐 방지): frontmatter, 코드펜스(``` ~ ```), 인라인 코드(`..`),
//   wikilink 타깃([[..]]), 마크다운 링크/이미지의 URL, 단독 URL.
//   제외는 같은 길이의 공백으로 마스킹해 line:col 좌표를 보존한다.
//
// 판정: high 1개↑ → fail(exit 2) / medium만 → warn(exit 1) / 없음 → pass(exit 0).
//   warn·fail은 발행을 막지 않는다(막는 건 _slop-gate의 사람 사인오프). lint는 그 근거를 만든다.

import { readFileSync } from 'node:fs'
import { fileURLToPath } from 'node:url'
import { dirname, resolve } from 'node:path'

const __dirname = dirname(fileURLToPath(import.meta.url))

// ── args ─────────────────────────────────────────────────────────────────────
const argv = process.argv.slice(2)
const flags = new Set(argv.filter((a) => a.startsWith('--')))
const positional = argv.filter((a) => !a.startsWith('--'))
const FILE = positional[0]
const lexIdx = argv.indexOf('--lexicon')
const LEXICON = lexIdx !== -1 ? argv[lexIdx + 1] : resolve(__dirname, '../../20_Projects/blog/_anti-slop-lexicon.md')
const AS_JSON = flags.has('--json')

if (!FILE) {
  process.stderr.write('usage: node blog-slop-lint.mjs "<file.md>" [--lexicon <path>] [--json]\n')
  process.exit(64)
}

// ── load lexicon (single source of truth) ────────────────────────────────────
function loadLexicon(path) {
  const raw = readFileSync(path, 'utf8')
  const m = raw.match(/```json\s*\n([\s\S]*?)\n```/)
  if (!m) throw new Error('lexicon에 ```json 패턴 블록이 없습니다: ' + path)
  return JSON.parse(m[1])
}

// ── mask non-prose so we never flag code/links/wikilinks (preserve columns) ───
function spaces(s) { return ' '.repeat(s.length) }

function maskLineInline(line) {
  return line
    // 이미지/링크의 URL 부분만 마스킹 (표시 텍스트는 남김)
    .replace(/(!?\[[^\]]*\]\()([^)]*)(\))/g, (_, a, url, c) => a + spaces(url) + c)
    // wikilink 전체 마스킹 (노트 제목이 슬롭으로 오탐되지 않게)
    .replace(/\[\[[^\]]*\]\]/g, spaces)
    // 인라인 코드
    .replace(/`[^`]*`/g, spaces)
    // 단독 URL
    .replace(/https?:\/\/\S+/g, spaces)
}

// frontmatter + 코드펜스를 제외하고, 본문 줄을 마스킹해서 반환
function extractProse(text) {
  const lines = text.split('\n')
  const out = [] // { n: 1-based line, text: masked prose }
  let i = 0
  // frontmatter
  if (lines[0] !== undefined && lines[0].trim() === '---') {
    let end = -1
    for (let k = 1; k < lines.length; k++) { if (lines[k].trim() === '---') { end = k; break } }
    if (end !== -1) i = end + 1
  }
  let inFence = false
  for (; i < lines.length; i++) {
    const line = lines[i]
    if (/^\s*(```|~~~)/.test(line)) { inFence = !inFence; continue } // 펜스 라인 자체 제외
    if (inFence) continue
    out.push({ n: i + 1, text: maskLineInline(line) })
  }
  return out
}

// ── run ───────────────────────────────────────────────────────────────────────
const lex = loadLexicon(LEXICON)
const text = readFileSync(FILE, 'utf8')
const prose = extractProse(text)
const proseJoined = prose.map((p) => p.text).join('\n')
const proseChars = proseJoined.replace(/\s/g, '').length // 공백 제외 글자 수
const perKBase = Math.max(proseChars / 1000, 0.001)

const hits = [] // { line, col, severity, category, id, matched, fix }

// 패턴(라인 단위, line:col)
for (const p of lex.patterns || []) {
  const re = new RegExp(p.pattern, p.flags && p.flags.includes('g') ? p.flags : (p.flags || '') + 'g')
  for (const { n, text: lt } of prose) {
    for (const mm of lt.matchAll(re)) {
      hits.push({
        line: n, col: mm.index + 1, severity: p.severity, category: p.category,
        id: p.id, matched: mm[0].replace(/\s+/g, ' ').trim(), fix: p.fix,
      })
    }
  }
}

// 밀도(전체 본문 기준)
const densities = []
for (const d of lex.densities || []) {
  const re = new RegExp(d.pattern, (d.flags || '') + (/(g)/.test(d.flags || '') ? '' : 'g'))
  const count = [...proseJoined.matchAll(re)].length
  const rate = count / perKBase
  const threshold = (lex.thresholds && lex.thresholds[d.perKey]) ?? Infinity
  const exceeded = rate > threshold
  densities.push({ id: d.id, category: d.category, severity: d.severity, count, rate: +rate.toFixed(2), threshold, exceeded, fix: d.fix })
}

// 판정
const activeDensityHits = densities.filter((d) => d.exceeded)
const allSev = [...hits.map((h) => h.severity), ...activeDensityHits.map((d) => d.severity)]
const has = (s) => allSev.includes(s)
const verdict = has('high') ? 'fail' : has('medium') ? 'warn' : 'pass'
const exitCode = verdict === 'fail' ? 2 : verdict === 'warn' ? 1 : 0

// 카테고리/심각도 집계
const byCat = {}
for (const h of hits) byCat[h.category] = (byCat[h.category] || 0) + 1
for (const d of activeDensityHits) byCat[d.category] = (byCat[d.category] || 0) + 1
const sevCount = { high: 0, medium: 0, low: 0 }
for (const s of allSev) if (sevCount[s] !== undefined) sevCount[s]++

const report = {
  file: FILE, verdict, proseChars,
  severityCount: sevCount, byCategory: byCat,
  hits: hits.sort((a, b) => ({ high: 0, medium: 1, low: 2 }[a.severity] - { high: 0, medium: 1, low: 2 }[b.severity]) || a.line - b.line),
  densities,
}

// ── output ─────────────────────────────────────────────────────────────────────
if (AS_JSON) {
  process.stdout.write(JSON.stringify(report, null, 2) + '\n')
  process.exit(exitCode)
}

const C = { high: '🔴', medium: '🟡', low: '⚪' }
const L = []
L.push(`slop-lint: ${verdict.toUpperCase()}  (${FILE.split('/').pop()})`)
L.push(`  본문 ${proseChars}자 / high ${sevCount.high} · medium ${sevCount.medium} · low ${sevCount.low}`)
if (report.hits.length) {
  L.push('')
  L.push('패턴 검출:')
  for (const h of report.hits) {
    L.push(`  ${C[h.severity]} ${h.line}:${h.col} [${h.category}] "${h.matched}"  → ${h.fix}`)
  }
}
if (densities.length) {
  L.push('')
  L.push('밀도:')
  for (const d of densities) {
    const mark = d.exceeded ? C[d.severity] + ' 초과' : '✅'
    L.push(`  ${mark} ${d.id} (${d.category}): ${d.count}회 = ${d.rate}/1K (임계 ${d.threshold})${d.exceeded ? '  → ' + d.fix : ''}`)
  }
}
if (!report.hits.length && !activeDensityHits.length) { L.push(''); L.push('  깨끗합니다. (단, 깊이·1인칭·반례는 lint가 아니라 _slop-gate에서 사람이 본다)') }
process.stdout.write(L.join('\n') + '\n')
process.exit(exitCode)
