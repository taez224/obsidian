import assert from 'node:assert/strict'
import { readFile } from 'node:fs/promises'
import { fileURLToPath } from 'node:url'
import test from 'node:test'

// Workflow 런타임의 LLM 호출을 대체해 분기·입력·산출물 계약만 검사한다.
// 원고 품질과 실제 Claude 도구 실행의 성공 여부는 이 검사로 판단하지 않는다.
const sourcePath = process.argv[2] || fileURLToPath(new URL('../../.claude/workflows/blog-recompose.js', import.meta.url))
const source = (await readFile(sourcePath, 'utf8')).replace('export const meta =', 'const meta =')
const AsyncFunction = Object.getPrototypeOf(async function () {}).constructor
const workflow = new AsyncFunction('args', 'agent', 'parallel', 'log', source)
const technicalTypes = ['explanation', 'tutorial', 'howto']

function valueFor(schema) {
  if (schema.enum) return schema.enum[0]
  if (schema.type === 'object') return Object.fromEntries((schema.required || []).map((key) => [key, valueFor(schema.properties[key])]))
  if (schema.type === 'array') return []
  if (schema.type === 'boolean') return true
  if (schema.type === 'number') return 0
  return 'fixture'
}

async function run(args, overrides = {}) {
  const calls = []
  const agent = async (prompt, options) => {
    calls.push({ prompt, ...options })
    if (Object.hasOwn(overrides, options.label)) return overrides[options.label]
    return valueFor(options.schema)
  }
  const result = await workflow(args, agent, (tasks) => Promise.all(tasks.map((task) => task())), () => {})
  return { result, calls }
}

for (const docType of technicalTypes) {
  test(`${docType}: 개인 경험 없이 기술 아웃라인에서 종료`, async () => {
    const { result, calls } = await run({ substanceSource: '/fixtures/source.md', docType })
    assert.equal(result.error, undefined)
    assert.equal(result.docType, docType)
    assert.equal(result.outline.selected.documentContract.docType, docType)
    assert.deepEqual(calls.map((call) => call.label), ['mine:substance', 'mine:synthesis', 'outline:technical'])
    assert.equal(result.output, null)
    assert.equal(result.compose, null)
    assert.equal(result.gate, null)
    const schema = calls.at(-1).schema
    assert.ok(schema.required.includes('documentContract'))
    for (const key of ['thesis', 'movement', 'climax', 'landing']) assert.equal(schema.properties[key], undefined)
    const section = schema.properties.sections.items
    assert.ok(section.required.includes('readerQuestion'))
    assert.equal(section.properties.sceneOrExperience, undefined)
    assert.equal(calls.some((call) => call.prompt.includes('/voice-profile.md')), false)
  })

  test(`${docType}: 명시한 전문 작성과 검수까지 문서 계약 전달`, async () => {
    const contract = { docType, goal: '자료에 있는 작업을 수행하고 결과 확인', reader: '기존 사용자' }
    const { result, calls } = await run({ conceptSource: '/fixtures/source.md', docType, writeFullDraft: true, output: '/fixtures/output.md' }, {
      'outline:technical': { title: '작업 안내', documentContract: contract, sections: [], authorPrompts: [] },
    })
    assert.equal(result.error, undefined)
    assert.equal(result.output, '/fixtures/output.md')
    for (const label of ['compose', 'gate']) {
      const call = calls.find((entry) => entry.label === label)
      assert.ok(call.prompt.includes(JSON.stringify(contract)))
      assert.ok(call.prompt.includes('/tech-doc-types.md'))
      assert.equal(call.prompt.includes('/voice-profile.md'), false)
    }
    const compose = calls.find((call) => call.label === 'compose').schema
    assert.ok(calls.find((call) => call.label === 'compose').prompt.includes('/korean-first-draft.md'))
    const gate = calls.find((call) => call.label === 'gate').schema
    assert.ok(compose.required.includes('contractNote'))
    assert.equal(compose.properties.voiceNote, undefined)
    assert.ok(gate.required.includes('contractMatch'))
    assert.equal(gate.properties.voiceMatch, undefined)
  })
}

test('통찰형은 기존 움직임·목소리 기준을 유지', async () => {
  const { result, calls } = await run({ experienceSource: '/fixtures/experience.md', docType: 'insight', writeFullDraft: true, output: '/fixtures/output.md' })
  assert.equal(result.error, undefined)
  assert.ok(calls.some((call) => call.label === 'outline:movements'))
  assert.equal(calls.some((call) => call.label === 'outline:technical'), false)
  assert.ok(calls.find((call) => call.label === 'outline:c1').schema.required.includes('thesis'))
  for (const label of ['compose', 'gate']) assert.ok(calls.find((call) => call.label === label).prompt.includes('/voice-profile.md'))
  assert.ok(result.compose.voiceNote)
  assert.ok(result.gate.voiceMatch)
})

test('미지정 유형은 종합 단계에서 정한 값을 이후 단계에 전달', async () => {
  const { result, calls } = await run(JSON.stringify({ substanceSource: '/fixtures/source.md' }), {
    'mine:synthesis': { docType: 'howto', evidenceMap: [], unresolved: [] },
  })
  assert.equal(result.docType, 'howto')
  assert.equal(calls.at(-1).label, 'outline:technical')
})

test('필수 입력·유형 오류에서는 작성 전에 종료', async () => {
  for (const args of [{}, { substanceSource: '/fixtures/source.md', writeFullDraft: true }, { substanceSource: '/fixtures/source.md', docType: 'other' }]) {
    const { result, calls } = await run(args)
    assert.ok(result.error)
    assert.equal(calls.length, 0)
  }
  const { result, calls } = await run({ substanceSource: '/fixtures/source.md', docType: 'explanation' }, {
    'mine:synthesis': { docType: 'insight' },
  })
  assert.ok(result.error)
  assert.equal(calls.some((call) => call.phase === 'Outline'), false)
})

test('아웃라인 실패 시 전문 작성 생략', async () => {
  for (const docType of ['insight', ...technicalTypes]) {
    const { result, calls } = await run({ substanceSource: '/fixtures/source.md', docType, writeFullDraft: true, output: '/fixtures/output.md' }, {
      'outline:c1': null, 'outline:technical': null,
    })
    assert.equal(result.outline.selected, null)
    assert.equal(calls.some((call) => call.phase === 'Compose' || call.phase === 'Gate'), false)
  }
})

test('통찰형 선택 인덱스와 최종 정리 실패 시 기존 후보 보존', async () => {
  const { result } = await run({ substanceSource: '/fixtures/source.md', docType: 'insight' }, {
    'outline:select': { selectedIndex: 99 }, 'outline:final': null,
  })
  assert.deepEqual(result.outline.selected, result.outline.candidates[0])
})
