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
    covered: {
      type: 'array',
      items: {
        type: 'object', additionalProperties: false,
        properties: {
          path: { type: 'string' },
          title: { type: 'string' },
          status: { type: 'string' },
          claim: { type: 'string', description: '본문이 실제로 착지한 국소 주장' },
          openingScene: { type: 'string', description: '도입 장면/질문, 없으면 "none"' },
          climaxEvidence: { type: 'string', description: '클라이맥스의 경험·사례·자료, 없으면 "none"' },
          landing: { type: 'string', description: '마지막에 남긴 결론/기준' },
        },
        required: ['path', 'title', 'status', 'claim', 'openingScene', 'climaxEvidence', 'landing'],
      },
      description: '인접한 기존 글의 본문 단위 커버리지',
    },
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
          overlapNote: { type: 'string', description: '가장 가까운 기존 글과 무엇이 같고 무엇이 다른지' },
        },
        required: ['title', 'angle', 'tension', 'evidenceNotes', 'coinedTerm', 'whyYours', 'overlapNote'],
      },
    },
  },
  required: ['angles'],
}

// ── stage: Mine (소스 병렬 채굴 → 커널 기반 인접 글 점검) ────────────────────
log('[Mine] ' + SOURCES.length + '개 소스 병렬 채굴' + (FOCUS ? (' / 포커스: ' + FOCUS) : ''))
const mineThunks = SOURCES.map((src) => () => agent(
  ['너는 ' + VAULT + '/' + src + ' 폴더를 채굴하는 자료조사가다. Glob/Grep/Read로 이 폴더의 노트를 훑어라.',
    FOCUS ? ('포커스 주제(있으면 우선): ' + FOCUS) : '',
    'frontmatter(status/type)·연결 수·최근 수정일을 단서로, 글의 씨앗이 될 커널을 최대 8개 뽑아라.',
    '성숙 노트(evergreen/growing, 3+연결)와 1인칭 경험(DevLog/Periodic)을 우선한다. 각 커널의 핵심 생각·경험 단서·통념과의 긴장·성숙도를 적어라. 기억·추측 금지, 실제로 읽은 노트만.'].join('\n'),
  { label: 'mine:' + src.split('/').pop(), phase: 'Mine', schema: MINE_SCHEMA, agentType: AGENT }
))
const mineRes = await parallel(mineThunks)
const kernels = mineRes.flatMap((r) => (r && r.kernels) || [])
if (!kernels.length) { log('[Mine] 커널 없음'); return { angles: [], kernels: [], coverage: [] } }
log('[Mine] 커널 ' + kernels.length + '개 수집')

// ── JS 압축(거대 synthesis 에이전트 없음) ──
const kernelBrief = kernels.map((k, i) =>
  (i + 1) + '. [' + k.maturity + '] ' + k.note + ' — ' + k.kernel +
  (k.tension !== 'none' ? (' / 긴장: ' + k.tension) : '') +
  (k.experienceHook !== 'none' ? (' / 경험: ' + k.experienceHook) : '')
).join('\n')

log('[Mine] 커널과 가까운 기존 글의 본문 점검')
const coverage = await agent(
  ['너는 인접 글 점검자다. ' + BLOG + ' 의 Markdown 중 frontmatter가 status: draft 또는 status: published인 실제 글을 Glob/Grep으로 찾는다.',
    '아래 커널들과 논지상 가까운 정본 글을 커널별 1~3개씩 shortlist하고 중복을 제거한 뒤 본문을 Read하라. type: series인 시리즈 허브와 project_id: blog인 프로젝트 허브, Archive의 반복본은 세지 않는다.',
    FOCUS ? ('사용자가 지정한 포커스: ' + FOCUS) : '',
    '## 커널', kernelBrief,
    '각 글의 경로·제목·상태뿐 아니라 본문이 실제로 주장한 것, 도입 장면/질문, 클라이맥스 증거, 마지막 착지를 기록하라.',
    '제목과 목차만 보고 추정하지 않는다. 같은 렌즈나 어휘는 반복 가능하므로 그것만으로 중복 판정하지 않는다.'].join('\n'),
  { label: 'coverage', phase: 'Mine', schema: COVERAGE_SCHEMA, agentType: AGENT }
)

const coveredBrief = ((coverage && coverage.covered) || []).map((c) =>
  '- ' + c.title + ' [' + c.status + '] (' + c.path + ')\n' +
  '  주장: ' + c.claim + '\n' +
  '  도입: ' + c.openingScene + '\n' +
  '  절정 증거: ' + c.climaxEvidence + '\n' +
  '  착지: ' + c.landing
).join('\n') || '(없음)'

// ── stage: Angles (압축 브리프 + 보이스로 종합) ────────────────────────────────
log('[Angles] ' + kernels.length + '개 커널 → 앵글 ' + COUNT + '개 종합')
const result = await agent(
  ['너는 이 저자의 편집장이다. 먼저 보이스 프로파일을 Read: ' + VOICE,
    '아래 채굴 커널에서, 이 저자만의 날카로운 블로그 앵글 ' + COUNT + '개를 제안하라.', '',
    '## 채굴 커널', kernelBrief, '',
    '## 인접한 기존 글', coveredBrief, '',
    '규칙: (1) 통념과 부딪히는 긴장이 있을 것 (2) 실제 1인칭 경험과 이어질 것 (3) 일반론·트렌드 요약·"N가지" listicle 금지 (4) 누구나 쓸 수 있으면 탈락 — 플랫폼/백엔드 현장 + 시스템 사고가 교차하는 지점.',
    '반복 렌즈·어휘·저자 캐릭터는 허용한다. 새 글이 기존 글과 같은 국소 주장에 같은 장면 또는 증거를 쓰고 같은 결론에 착지할 때만 중복으로 본다. 그 경우 새 질문·경계·반례·증거를 찾아 각도를 바꿔라. 다른 발행면을 위한 의도적 자립형 재구성은 가능하되 overlapNote에 밝힌다.',
    '각 앵글: 제목 초안 · 한 문장 POV(칼끝) · 통념 vs 주장 · 근거 노트(위키링크) · 조어 후보(필요할 때만, 없으면 "none") · 왜 내 각인가 · 가장 가까운 기존 글과의 차이.'].join('\n'),
  { label: 'synthesize-angles', phase: 'Angles', schema: ANGLE_LIST_SCHEMA, agentType: AGENT }
)
const angles = (result && result.angles) || []
log('[완료] 앵글 ' + angles.length + '개 반환')

return { angles, kernels, coverage: (coverage && coverage.covered) || [] }
