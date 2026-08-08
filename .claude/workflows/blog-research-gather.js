export const meta = {
  name: 'blog-research-gather',
  description: '블로그 리서치 fan-out: 다학제 렌즈로 병렬 웹 리서치 + 반례 의무 수집 후, 재사용 리서치 노트를 Resources에 생성한다.',
  whenToUse: '주제/seed에 대한 다학제 근거+반례를 모아 재사용 리서치 노트를 만들 때(파이프라인 ② research). args로 seed 경로 또는 주제, 렌즈 수를 넘긴다.',
  phases: [
    { title: 'Profile' },
    { title: 'Gather' },
    { title: 'Counter' },
    { title: 'Write' },
  ],
}

// ───────────────────────────────────────────────────────────────────────────
// 사용법 (args):
//   {
//     seed:      "<seed 노트 절대경로>",   // seed 또는 topic 중 하나 필수
//     topic:     "<주제/주장 한 줄>",       // seed 없을 때
//     lenses:    4,                         // 선택: 다학제 렌즈 수
//     vaultRoot: "/Users/taez/Projects/obsidian" // 선택
//   }
//
// 설계 원칙:
//  - 반례 의무: 뒷받침 근거만 모으면 slop의 씨앗. "이 주장이 틀린다면?"을 별도 적대 에이전트로 강제 수집.
//  - 웹 grounding: 기억·추측 금지, 실제로 연 URL만. (정확성은 발행 전 blog-review-polish factcheck가 한 번 더)
//  - JS 합성: 거대 synthesis 에이전트 없음. 렌즈 결과를 JS로 brief 압축, raw도 항상 반환.
//  - 노트 생성: Write 단계에서 에이전트가 결과를 자기 언어로(Feynman, 인용 덤프 금지) Resources 리서치 노트로 저장한다. 영구 노트 승격은 별도 승인 절차다.
// ───────────────────────────────────────────────────────────────────────────

let A = args || {}
if (typeof A === 'string') { try { A = JSON.parse(A) } catch (e) { A = {} } }
const VAULT = A.vaultRoot || '/Users/taez/Projects/obsidian'
const SEED = A.seed || ''
const TOPIC = A.topic || ''
const LENSES = A.lenses || 4
const AGENT = 'general-purpose'

if (!SEED && !TOPIC) { log('❌ args.seed(경로) 또는 args.topic(주제) 중 하나가 필요합니다.'); return { error: 'need seed or topic', got: A } }

// ── schemas ──────────────────────────────────────────────────────────────────
const RESEARCH_PROFILE_SCHEMA = {
  type: 'object', additionalProperties: false,
  properties: {
    claim: { type: 'string', description: '핵심 주장 한 줄' },
    subQuestions: { type: 'array', items: { type: 'string' }, description: '하위 질문 3~6개' },
    searchQueries: { type: 'array', items: { type: 'string' }, description: '검색 키워드(국문+영문 섞어) 4~8개' },
    lenses: { type: 'array', items: { type: 'string' }, description: '다학제 렌즈(예: 소프트웨어공학, 사회기술, 경제/조직, 인지심리, 철학)' },
  },
  required: ['claim', 'subQuestions', 'searchQueries', 'lenses'],
}
const LENS_FINDINGS_SCHEMA = {
  type: 'object', additionalProperties: false,
  properties: {
    lens: { type: 'string' },
    evidence: {
      type: 'array',
      items: {
        type: 'object', additionalProperties: false,
        properties: {
          claim: { type: 'string' },
          direction: { type: 'string', enum: ['supports', 'challenges'] },
          sourceUrl: { type: 'string', description: '실제로 연 출처 URL' },
          verificationStatus: { type: 'string', enum: ['verified', 'unresolved'] },
          scope: { type: 'string', description: '적용 범위와 한계' },
        },
        required: ['claim', 'direction', 'sourceUrl', 'verificationStatus', 'scope'],
      },
      description: '주장을 뒷받침하거나 제한하는 근거와 검증 상태',
    },
    data: {
      type: 'array',
      items: {
        type: 'object', additionalProperties: false,
        properties: {
          claim: { type: 'string', description: '검증한 수치·직접 인용·특정 연구 결과' },
          sourceUrl: { type: 'string', description: '실제로 연 1차 출처 URL' },
          publishedDate: { type: 'string', description: '출처 발행일, 확인 불가면 "unknown"' },
          dataWindow: { type: 'string', description: '조사·관측 기간, 해당 없으면 "not_applicable"' },
          scope: { type: 'string', description: '표본·제품·도메인·지역과 주요 한계' },
          verificationStatus: { type: 'string', enum: ['verified', 'unresolved'] },
        },
        required: ['claim', 'sourceUrl', 'publishedDate', 'dataWindow', 'scope', 'verificationStatus'],
      },
      description: '재사용 가능한 수치·직접 인용·연구 결과와 검증 범위',
    },
    sources: { type: 'array', items: { type: 'string' }, description: '실제로 연 URL' },
    insight: { type: 'string', description: '이 렌즈에서의 한 줄 통찰' },
  },
  required: ['lens', 'evidence', 'data', 'sources', 'insight'],
}
const COUNTER_SCHEMA = {
  type: 'object', additionalProperties: false,
  properties: {
    counterExamples: {
      type: 'array',
      items: {
        type: 'object', additionalProperties: false,
        properties: {
          text: { type: 'string', description: '반례/반증 한 줄' },
          source: { type: 'string', description: '출처 URL/귀속, 없으면 "none"' },
          impact: { type: 'string', enum: ['weakens', 'invalidates'], description: '주장을 약화시키는지 무효화하는지' },
          verificationStatus: { type: 'string', enum: ['verified', 'unresolved', 'reasoned_boundary'] },
        },
        required: ['text', 'source', 'impact', 'verificationStatus'],
      },
    },
    sources: { type: 'array', items: { type: 'string' } },
  },
  required: ['counterExamples', 'sources'],
}

// ── stage: Profile ────────────────────────────────────────────────────────────
log('[Profile] 리서치 프로필 추출' + (SEED ? ' (seed: ' + SEED + ')' : ' (topic)'))
const seedCtx = SEED ? ('seed 노트를 Read 도구로 읽어라: ' + SEED) : ('주제: ' + TOPIC)
const profile = await agent(
  [seedCtx, '',
    '이 글감의 리서치 프로필을 뽑아라: 핵심 주장(claim) · 하위 질문 3~6개 · 검색 키워드(국문+영문 섞어 4~8개) · 이 주제를 입체적으로 볼 다학제 렌즈 ' + LENSES + '개(서로 겹치지 않게).'].join('\n'),
  { label: 'research-profile', phase: 'Profile', schema: RESEARCH_PROFILE_SCHEMA, agentType: AGENT }
)
if (!profile) { log('[Profile] 실패'); return { profile: null, lensFindings: [], counters: null, brief: '', sources: [] } }
const q = (profile.searchQueries || []).join(' / ')

// ── stage: Gather (렌즈별 병렬 웹 리서치) ─────────────────────────────────────
log('[Gather] ' + (profile.lenses || []).length + '개 렌즈 병렬 리서치 (웹)')
const lensFindings = (await parallel((profile.lenses || []).map((lens) => () => agent(
  ['너는 "' + lens + '" 관점의 리서치어다. WebSearch/WebFetch로 1차 출처를 실제로 찾아라. 기억·추측 금지, 직접 연 URL만.', '',
    '핵심 주장: ' + profile.claim, '검색 키워드: ' + q, '',
    '이 렌즈에서 주장을 뒷받침/반박하는 근거와 한 줄 통찰을 반환하라.',
    'evidence의 각 항목은 실제로 연 출처 URL, 지지/반박 방향, 적용 범위와 검증 상태를 함께 기록한다. 접근하지 못한 근거를 verified로 표시하지 않는다.',
    '수치·직접 인용·특정 연구 결과는 반드시 원 논문, 공식 보고서, 공식 보도자료 등 1차 출처에서 확인하고 data에 발행일·데이터 수집/관측 기간·표본/제품/도메인 범위와 한계를 함께 기록한다.',
    '403, JavaScript 셸, 페이월, 검색 실패는 주장이 없거나 틀렸다는 증거가 아니다. 공식 PDF·DOI·저장소·보도자료·RSS 같은 대체 1차 경로를 시도하고도 확인하지 못하면 verificationStatus="unresolved"로 남긴다.',
    '법·정책 일정은 제안, 잠정 합의, 입법 채택, 최종 승인, 관보 게재, 발효, 적용일을 구분해 공식 출처에서 현재 단계를 확인한다.'].join('\n'),
  { label: 'lens:' + lens, phase: 'Gather', schema: LENS_FINDINGS_SCHEMA, agentType: AGENT }
)))).filter(Boolean)

// ── stage: Counter (반례 의무) ────────────────────────────────────────────────
log('[Counter] 반례 의무 수집')
const counters = await agent(
  ['너는 적대적 반례 사냥꾼이다. "이 주장이 틀린다면 어떤 경우인가"를 웹으로 적극 탐색하라. 뒷받침 근거가 아니라 *약점·반증·경계조건*만 모은다. 기억·추측 금지.', '',
    '핵심 주장: ' + profile.claim, '검색 키워드: ' + q, '',
    '구체적인 수치·연구 귀속을 쓰는 반례는 1차 출처를 직접 열어 확인한다. 접근하지 못한 출처를 확인한 것처럼 쓰지 않는다.',
    '반례/반증을 최대 5개, 출처와 함께. 각 반례가 주장을 약화(weakens)시키는지 무효화(invalidates)하는지 평가한다. 논리적으로만 도출한 경계조건은 source="none", verificationStatus="reasoned_boundary"로 사실 주장과 구분한다.'].join('\n'),
  { label: 'counter', phase: 'Counter', schema: COUNTER_SCHEMA, agentType: AGENT }
)

// ── JS 합성(거대 synthesis 에이전트 없음, raw 항상 반환) ──
const briefLines = ['## 핵심 주장: ' + profile.claim]
lensFindings.forEach((f) => {
  briefLines.push('### 렌즈: ' + f.lens + (f.insight ? ' — ' + f.insight : ''))
  ;(f.evidence || []).slice(0, 3).forEach((e) => {
    briefLines.push('- [근거:' + e.verificationStatus + '/' + e.direction + '] ' + e.claim)
    briefLines.push('  출처: ' + e.sourceUrl + ' / 범위: ' + e.scope)
  })
  ;(f.data || []).forEach((d) => {
    briefLines.push('- [데이터:' + d.verificationStatus + '] ' + d.claim)
    briefLines.push('  출처: ' + d.sourceUrl + ' / 발행: ' + d.publishedDate + ' / 관측기간: ' + d.dataWindow + ' / 범위: ' + d.scope)
  })
})
if (counters && (counters.counterExamples || []).length) {
  briefLines.push('### 반례(의무)')
  counters.counterExamples.forEach((c) => briefLines.push('- [' + c.impact + '/' + c.verificationStatus + '] ' + c.text + (c.source && c.source !== 'none' ? ' (' + c.source + ')' : '')))
}
const brief = briefLines.join('\n')

const sources = []
lensFindings.forEach((f) => (f.sources || []).forEach((s) => sources.push(s)))
if (counters) (counters.sources || []).forEach((s) => sources.push(s))
const uniqSources = Array.from(new Set(sources))

// ── stage: Write (에이전트가 다중 출처 리서치 노트를 Resources에 저장) ──
const slug = (profile.claim || 'research').replace(/[\\/:*?"<>|\n]/g, ' ').replace(/\s+/g, ' ').slice(0, 40).trim()
const notePath = VAULT + '/30_Resources/References/etc/' + slug + ' — 리서치.md'
const relatedSeed = SEED ? '[[' + SEED.split('/').pop().replace(/\.md$/, '') + ']]' : ''
log('[Write] 리서치 노트 생성 → ' + notePath)
await agent(
  ['너는 파일 작성자다. 아래 리서치 결과를 *자기 언어로*(Feynman, 인용 덤프 금지) 정리해 ' + notePath + ' 에 다중 출처 참고노트로 생성하라. 이 노트는 사용자의 영구 주장이 아니다.', '',
    'frontmatter 필드: title("' + slug + ' — 리서치") / source: ""(다중 출처는 본문 ## 출처에 기록) / author: [] / published: "" / created(오늘 YYYY-MM-DD) / description(<핵심 주장 한 줄>) / tags: [📰article, <주제 태그>] / status: unread / my_take: ""' + (relatedSeed ? (' / related: ["' + relatedSeed + '"]') : ''), '',
    '본문 섹션(필수): ## AI 종합  /  ## 핵심 주장과 근거  /  ## 반례·긴장(의무)  /  ## 재사용 데이터·인용  /  ## 미검증·접근 불가  /  ## 출처', '',
    'evidence·data·counterExamples에서 verificationStatus="unresolved"인 항목은 확정 사실처럼 본문 근거에 섞지 말고 ## 미검증·접근 불가에 둔다. reasoned_boundary는 외부 사실이 아니라 논리적 경계조건이라고 표시한다. 발행일·데이터 기간·범위와 한계를 지우지 않는다.', '',
    '핵심 주장: ' + profile.claim, '', '### 브리프', brief, '', '### 출처', uniqSources.join('\n')].join('\n'),
  { label: 'write-research-note', phase: 'Write', agentType: AGENT }
)

log('[완료] 렌즈 ' + lensFindings.length + ' / 반례 ' + ((counters && counters.counterExamples) || []).length + ' → ' + notePath)
return { profile, lensFindings, counters, brief, sources: uniqSources, notePath }
