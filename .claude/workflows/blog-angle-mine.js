export const meta = {
  name: 'blog-angle-mine',
  description: '블로그 앵글 채굴 fan-out: vault의 Slipbox·Inbox·DevLog·Periodic을 병렬 채굴하고 기존 글과 중복 제거한 뒤, 저자만의 날카로운 앵글 후보를 리포트로 반환한다. 앵글 선택은 사람 몫이라 파일은 쓰지 않는다.',
  whenToUse: '쌓인 노트에서 글감 앵글 후보를 받고 싶을 때(파이프라인 ① seed). args로 소스 폴더·개수·포커스를 넘긴다. 마음에 드는 앵글의 seed 노트는 리포트를 보고 직접 만든다.',
  phases: [
    { title: 'Mine' },
    { title: 'Angles' },
  ],
}

// ───────────────────────────────────────────────────────────────────────────
// 사용법 (args):
//   {
//     sources:   ["01_Slipbox","00_Inbox","30_Resources/Development/DevLog","10_Periodic Notes"], // 선택
//     count:     5,                          // 선택: 반환할 앵글 수
//     focus:     "<포커스 주제 한 줄>",        // 선택: 채굴 편향
//     vaultRoot: "/Users/taez/Projects/obsidian" // 선택
//   }
//
// 설계 원칙(blog-review-polish/​recompose 계승):
//  - JS 합성: 거대 JSON synthesis 에이전트 없음. 채굴 raw는 JS로 압축해 종합 에이전트에 넘긴다(hang 차단). raw도 항상 반환.
//  - 파일 미작성: 후보를 리포트로 반환한다(앵글 선택은 사람 몫). 고른 앵글의 seed 노트는 리포트를 보고 직접 만든다.
//  - slop 방어를 발굴부터: 일반론·트렌드 요약·listicle 후보는 종합 단계에서 탈락. 통념과의 긴장 + 1인칭 경험 연결을 요구.
// ───────────────────────────────────────────────────────────────────────────

let A = args || {}
if (typeof A === 'string') { try { A = JSON.parse(A) } catch (e) { A = {} } }
const VAULT = A.vaultRoot || '/Users/taez/Projects/obsidian'
const SOURCES = A.sources || ['01_Slipbox', '00_Inbox', '30_Resources/Development/DevLog', '10_Periodic Notes']
const COUNT = A.count || 5
const FOCUS = A.focus || ''
const AGENT = 'general-purpose'
const VOICE = VAULT + '/.agents/skills/taez-insight-blog-writer/references/voice-profile.md'
const BLOG = VAULT + '/20_Projects/blog'

// ── schemas ──────────────────────────────────────────────────────────────────
const MINE_SCHEMA = {
  type: 'object', additionalProperties: false,
  properties: {
    kernels: {
      type: 'array',
      items: {
        type: 'object', additionalProperties: false,
        properties: {
          note: { type: 'string', description: '노트 경로 또는 제목' },
          kernel: { type: 'string', description: '이 노트가 품은 핵심 생각 한 줄' },
          experienceHook: { type: 'string', description: '1인칭 경험/실패 장면 단서, 없으면 "none"' },
          tension: { type: 'string', description: '통념과 부딪히는 지점, 없으면 "none"' },
          maturity: { type: 'string', enum: ['evergreen', 'growing', 'seedling', 'inbox', 'devlog', 'unknown'] },
        },
        required: ['note', 'kernel', 'experienceHook', 'tension', 'maturity'],
      },
    },
  },
  required: ['kernels'],
}
const COVERAGE_SCHEMA = {
  type: 'object', additionalProperties: false,
  properties: {
    covered: { type: 'array', items: { type: 'string' }, description: '이미 발행/초안에서 다룬 각도(제목+논지 한 줄씩)' },
  },
  required: ['covered'],
}
const ANGLE_LIST_SCHEMA = {
  type: 'object', additionalProperties: false,
  properties: {
    angles: {
      type: 'array',
      items: {
        type: 'object', additionalProperties: false,
        properties: {
          title: { type: 'string', description: '제목 초안' },
          angle: { type: 'string', description: '한 문장 POV(칼끝)' },
          tension: { type: 'string', description: '통념 vs 내 주장' },
          evidenceNotes: { type: 'array', items: { type: 'string' }, description: '근거가 되는 노트(위키링크 형태)' },
          coinedTerm: { type: 'string', description: '조어 후보, 없으면 "none"' },
          whyYours: { type: 'string', description: '왜 이 저자만의 각인가 한 줄' },
        },
        required: ['title', 'angle', 'tension', 'evidenceNotes', 'coinedTerm', 'whyYours'],
      },
    },
  },
  required: ['angles'],
}

// ── stage: Mine (병렬 채굴 + 중복 점검) ────────────────────────────────────────
log('[Mine] ' + SOURCES.length + '개 소스 병렬 채굴' + (FOCUS ? (' / 포커스: ' + FOCUS) : ''))
const mineThunks = SOURCES.map((src) => () => agent(
  ['너는 ' + VAULT + '/' + src + ' 폴더를 채굴하는 자료조사가다. Glob/Grep/Read로 이 폴더의 노트를 훑어라.',
    FOCUS ? ('포커스 주제(있으면 우선): ' + FOCUS) : '',
    'frontmatter(status/type)·연결 수·최근 수정일을 단서로, 글의 씨앗이 될 커널을 최대 8개 뽑아라.',
    '성숙 노트(evergreen/growing, 3+연결)와 1인칭 경험(DevLog/Periodic)을 우선한다. 각 커널의 핵심 생각·경험 단서·통념과의 긴장·성숙도를 적어라. 기억·추측 금지, 실제로 읽은 노트만.'].join('\n'),
  { label: 'mine:' + src.split('/').pop(), phase: 'Mine', schema: MINE_SCHEMA, agentType: AGENT }
))
const coverageThunk = () => agent(
  ['너는 중복 점검자다. ' + BLOG + ' 의 Markdown 중 frontmatter가 status: draft 또는 status: published인 실제 글만 Glob/Read로 훑어, 이미 다룬 각도를 한 줄씩(제목+논지) 나열하라. type: series인 시리즈 허브와 project_id: blog인 프로젝트 허브는 기존 글로 세지 않는다. 새 앵글이 실제 글을 반복하지 않게 쓸 dedup 목록이다.'].join('\n'),
  { label: 'coverage', phase: 'Mine', schema: COVERAGE_SCHEMA, agentType: AGENT }
)

const mineRes = await parallel([...mineThunks, coverageThunk])
const coverage = mineRes[mineRes.length - 1]
const kernels = mineRes.slice(0, -1).flatMap((r) => (r && r.kernels) || [])
if (!kernels.length) { log('[Mine] 커널 없음'); return { angles: [], kernels: [], coverage: (coverage && coverage.covered) || [] } }
log('[Mine] 커널 ' + kernels.length + '개 수집')

// ── JS 압축(거대 synthesis 에이전트 없음) ──
const kernelBrief = kernels.map((k, i) =>
  (i + 1) + '. [' + k.maturity + '] ' + k.note + ' — ' + k.kernel +
  (k.tension !== 'none' ? (' / 긴장: ' + k.tension) : '') +
  (k.experienceHook !== 'none' ? (' / 경험: ' + k.experienceHook) : '')
).join('\n')
const coveredBrief = ((coverage && coverage.covered) || []).map((c) => '- ' + c).join('\n') || '(없음)'

// ── stage: Angles (압축 브리프 + 보이스로 종합) ────────────────────────────────
log('[Angles] ' + kernels.length + '개 커널 → 앵글 ' + COUNT + '개 종합')
const result = await agent(
  ['너는 이 저자의 편집장이다. 먼저 보이스 프로파일을 Read: ' + VOICE,
    '아래 채굴 커널에서, 이 저자만의 날카로운 블로그 앵글 ' + COUNT + '개를 제안하라.', '',
    '## 채굴 커널', kernelBrief, '',
    '## 이미 다룬 각도(반복 금지)', coveredBrief, '',
    '규칙: (1) 통념과 부딪히는 긴장이 있을 것 (2) 1인칭 경험과 이어질 것 (3) 일반론·트렌드 요약·"N가지" listicle 금지 (4) 누구나 쓸 수 있으면 탈락 — 플랫폼/백엔드 현장 + 시스템 사고가 교차하는 지점.',
    '각 앵글: 제목 초안 · 한 문장 POV(칼끝) · 통념 vs 주장 · 근거 노트(위키링크) · 조어 후보(있으면, 없으면 "none") · 왜 내 각인가 한 줄.'].join('\n'),
  { label: 'synthesize-angles', phase: 'Angles', schema: ANGLE_LIST_SCHEMA, agentType: AGENT }
)
const angles = (result && result.angles) || []
log('[완료] 앵글 ' + angles.length + '개 반환')

return { angles, kernels, coverage: (coverage && coverage.covered) || [] }
