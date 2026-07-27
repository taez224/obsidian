export const meta = {
  name: 'blog-review-polish',
  description: '한국어 블로그 기본 검수와 선택적 발행 게이트. 기본은 결정론 lint와 편집 관점 1회이며, 사실검증·리서치·다중 관점·윤문 루프는 명시한 단계에서만 실행한다.',
  whenToUse: '블로그 초안을 가볍게 점검하거나, 사용자가 발행 전 전체 검수를 명시적으로 요청했을 때. args로 대상 파일과 옵션을 넘긴다.',
  phases: [
    { title: 'Light-review' },
    { title: 'Fact-check' },
    { title: 'Research' },
    { title: 'Editorial' },
    { title: 'Polish' },
    { title: 'Final-gate' },
  ],
}

// ───────────────────────────────────────────────────────────────────────────
// 사용법 (args 로 넘긴다):
//   {
//     file:        "<초안 절대경로>",                 // 필수
//     workCopy:    "<윤문본을 쓸 절대경로>",            // polish 단계에 필수(자동 사본 생성 안 함)
//     toneRef:     "<톤 레퍼런스 URL 또는 본문 일부>",   // 선택
//     targetReader:"<목표 독자 한 줄>",               // 선택
//     publicationSurface:"brunch|personal-tech|company-tech", // 선택
//     stages:      ["light"],                         // 선택(기본 light)
//     mode:        "publish",                         // 선택: 전체 발행 게이트
//     maxRounds:   2                                  // 선택(윤문 루프 상한)
//   }
//
// 전체 발행 게이트:
//   회사 기술 블로그 전체 검수: { file, mode: "publish", publicationSurface: "company-tech", workCopy: "<작업 사본 경로>" }
//   또는 stages를 ["factcheck","research","editorial","polish","gate"]로 명시한다.
//
// 설계에 반영한 이전 결함 보정:
//  - 정확성 센티넬: 윤문 루프가 과장/근거없는 주장을 새로 만들면 루프 안에서 잡는다.
//  - 통독 패스: 조각편집 후 '처음 읽는 독자'로 전체 일관성 1회 점검(gate).
//  - 거대 JSON synthesis 제거: 종합은 JS에서 압축(에이전트 hang 원인 차단), raw 결과도 항상 반환.
//  - 구조 회귀검사: 마크다운/프론트매터/위키링크/keep자산 무결성 점검(gate).
//  - 델타 재사실검증: 윤문본의 수치·귀속 주장만 다시 확인(gate).
//  - 웹 리서치 grounding: 패널이 진공 추측 대신 실측(경쟁 글 구조·트렌드 현재성)으로 트렌드/구조를 판정. 구조 차별화는 자동수정 않고 리포트 플래그로만 노출(저자 재설계 영역).
// ───────────────────────────────────────────────────────────────────────────

let A = args || {}
if (typeof A === 'string') { try { A = JSON.parse(A) } catch (e) { A = {} } } // 방어: 호출자가 args를 JSON 문자열로 넘겨도 견딘다
const FILE = A.file
if (!FILE) { log('❌ args.file 이 필요합니다. {file:"<절대경로>"} 객체로 넘기세요.'); return { error: 'args.file required', gotArgsType: typeof args } }
const FULL_STAGES = ['factcheck', 'research', 'editorial', 'polish', 'gate']
const STAGES = A.stages || (A.mode === 'publish' ? FULL_STAGES : ['light'])
const MAX_ROUNDS = A.maxRounds || 2
const WORK = A.workCopy || ''
const SURFACE = A.publicationSurface || 'unspecified'
const READER = A.targetReader || (SURFACE === 'company-tech'
  ? '과장보다 재현 가능한 근거와 실무 효용을 보는 기술 독자'
  : '이 글이 실제로 상정하는 독자')
const TONE = A.toneRef
  ? '톤 레퍼런스(이 톤에 맞춰라): ' + A.toneRef
  : '톤 기준: 현재 초안과 발행 매체의 목소리를 보존한다. 존댓말·질문·비유·1인칭을 형식적으로 추가하지 않는다. 영어 병기 과다와 번역투는 피한다.'
const GOAL = '목표: 글의 장르와 발행 매체 안에서 저자의 판단과 근거가 선명하게 읽힌다. 반목표: 보고서체 강요, listicle 강요, 트렌드 name-drop, 한국어 AI-티, 기술블로그 구조의 일괄 적용.'
const AGENT = 'general-purpose'

// ── schemas ────────────────────────────────────────────────────────────────
const CLAIM_LIST_SCHEMA = {
  type: 'object', additionalProperties: false,
  properties: {
    claims: {
      type: 'array',
      items: {
        type: 'object', additionalProperties: false,
        properties: {
          id: { type: 'string' },
          text: { type: 'string', description: '검증 대상 주장(본문 표현)' },
          source: { type: 'string', description: '귀속된 출처/저자/연도, 없으면 "none"' },
          critical: { type: 'boolean', description: '수치나 특정 연구 귀속이면 true' },
        },
        required: ['id', 'text', 'source', 'critical'],
      },
    },
  },
  required: ['claims'],
}
const VERDICT_SCHEMA = {
  type: 'object', additionalProperties: false,
  properties: {
    id: { type: 'string' },
    verdict: { type: 'string', enum: ['verified', 'partially_correct', 'misattributed', 'wrong', 'unverifiable'] },
    confidence: { type: 'string', enum: ['high', 'medium', 'low'] },
    whatSourceSays: { type: 'string' },
    discrepancy: { type: 'string' },
    recommendation: { type: 'string' },
    sourceUrl: { type: 'string' },
  },
  required: ['id', 'verdict', 'confidence', 'whatSourceSays', 'discrepancy', 'recommendation'],
}
const PERSONA_SCHEMA = {
  type: 'object', additionalProperties: false,
  properties: {
    persona: { type: 'string' },
    achievesGoal: { type: 'string', enum: ['yes', 'partly', 'no'] },
    findings: {
      type: 'array',
      items: {
        type: 'object', additionalProperties: false,
        properties: {
          line: { type: 'string' }, quote: { type: 'string' },
          issue: { type: 'string' }, severity: { type: 'string', enum: ['high', 'medium', 'low'] },
          suggestion: { type: 'string' },
        },
        required: ['line', 'quote', 'issue', 'severity', 'suggestion'],
      },
    },
    whatWorks: { type: 'string', description: '보존할 강점(keep-list 재료)' },
  },
  required: ['persona', 'achievesGoal', 'findings', 'whatWorks'],
}
const REVIEW_SCHEMA = {
  type: 'object', additionalProperties: false,
  properties: {
    persona: { type: 'string' },
    satisfied: { type: 'boolean' },
    remaining: {
      type: 'array',
      items: {
        type: 'object', additionalProperties: false,
        properties: {
          line: { type: 'string' }, issue: { type: 'string' },
          severity: { type: 'string', enum: ['high', 'medium', 'low'] }, fix: { type: 'string' },
        },
        required: ['line', 'issue', 'severity', 'fix'],
      },
    },
    note: { type: 'string' },
  },
  required: ['persona', 'satisfied', 'remaining', 'note'],
}
const EDIT_SCHEMA = {
  type: 'object', additionalProperties: false,
  properties: {
    changeCount: { type: 'number' }, changesSummary: { type: 'string' }, preservedVoiceNote: { type: 'string' },
  },
  required: ['changeCount', 'changesSummary', 'preservedVoiceNote'],
}
const GATE_SCHEMA = {
  type: 'object', additionalProperties: false,
  properties: {
    coherenceVerdict: { type: 'string', enum: ['ready', 'minor', 'needs-work'] },
    coherenceIssues: { type: 'array', items: { type: 'string' } },
    factDeltas: { type: 'array', items: { type: 'string' }, description: '윤문이 새로 만든 과장/오류, 없으면 빈 배열' },
    structureOk: { type: 'boolean' },
    structureNote: { type: 'string' },
  },
  required: ['coherenceVerdict', 'coherenceIssues', 'factDeltas', 'structureOk', 'structureNote'],
}
const SLOP_LINT_SCHEMA = {
  type: 'object', additionalProperties: false,
  properties: {
    verdict: { type: 'string', enum: ['pass', 'warn', 'fail', 'error'], description: 'lint 판정(명령 출력 그대로)' },
    high: { type: 'number' }, medium: { type: 'number' }, low: { type: 'number' },
    topHits: { type: 'array', items: { type: 'string' }, description: 'high·medium만 "line:col [category] matched → fix" 형식' },
  },
  required: ['verdict', 'high', 'medium', 'low', 'topHits'],
}
const LIGHT_REVIEW_SCHEMA = {
  type: 'object', additionalProperties: false,
  properties: {
    readiness: { type: 'string', enum: ['ready', 'minor', 'needs-work'] },
    strengths: { type: 'array', items: { type: 'string' } },
    issues: {
      type: 'array',
      items: {
        type: 'object', additionalProperties: false,
        properties: {
          line: { type: 'string' },
          issue: { type: 'string' },
          suggestion: { type: 'string' },
        },
        required: ['line', 'issue', 'suggestion'],
      },
    },
    slopVerdict: { type: 'string', enum: ['pass', 'warn', 'fail', 'error'] },
    slopHigh: { type: 'number' },
    slopMedium: { type: 'number' },
    slopHits: { type: 'array', items: { type: 'string' } },
  },
  required: ['readiness', 'strengths', 'issues', 'slopVerdict', 'slopHigh', 'slopMedium', 'slopHits'],
}
const DRAFT_PROFILE_SCHEMA = {
  type: 'object', additionalProperties: false,
  properties: {
    topic: { type: 'string', description: '한 줄 주제' },
    thesis: { type: 'string', description: '핵심 논지 한 줄' },
    skeleton: { type: 'array', items: { type: 'string' }, description: '섹션 골격(H2/H3 순서)' },
    hook: { type: 'string', description: '글을 여는 방식(훅 유형)' },
    claimedAngle: { type: 'string', description: '글이 내세우는 차별점/각도' },
    searchQueries: { type: 'array', items: { type: 'string' }, description: '경쟁 글·트렌드 검색용 키워드 3~6개(국문+영문)' },
  },
  required: ['topic', 'thesis', 'skeleton', 'hook', 'claimedAngle', 'searchQueries'],
}
const LANDSCAPE_SCHEMA = {
  type: 'object', additionalProperties: false,
  properties: {
    articles: {
      type: 'array',
      items: {
        type: 'object', additionalProperties: false,
        properties: {
          title: { type: 'string' }, url: { type: 'string' },
          angle: { type: 'string', description: '그 글의 각도 한 줄' },
          structure: { type: 'string', description: '섹션 골격 요약' },
          hook: { type: 'string' },
          overlap: { type: 'string', enum: ['high', 'medium', 'low'], description: '초안과 구조/각도 겹침' },
        },
        required: ['title', 'url', 'angle', 'structure', 'hook', 'overlap'],
      },
    },
    mostSimilar: { type: 'string', description: '가장 닮은 글 제목/URL + 왜' },
    clicheSignals: { type: 'array', items: { type: 'string' }, description: '이 주제에서 닳은 진부 패턴' },
    verdict: { type: 'string', enum: ['fresh', 'familiar', 'derivative'], description: '초안 구조 신선도 종합' },
  },
  required: ['articles', 'mostSimilar', 'clicheSignals', 'verdict'],
}
const TREND_SCHEMA = {
  type: 'object', additionalProperties: false,
  properties: {
    framingStatus: { type: 'string', enum: ['ahead', 'current', 'stale'], description: '초안 프레이밍의 현재성' },
    evidence: { type: 'string', description: '그렇게 본 근거(검색으로 확인한 것)' },
    missedDevelopments: { type: 'array', items: { type: 'string' }, description: '초안이 놓친 최근 3~6개월 전개' },
    stalePhrasings: { type: 'array', items: { type: 'string' }, description: '이미 식었거나 흔해진 프레이밍/표현' },
  },
  required: ['framingStatus', 'evidence', 'missedDevelopments', 'stalePhrasings'],
}
const DIFF_SCHEMA = {
  type: 'object', additionalProperties: false,
  properties: {
    differentiationVerdict: { type: 'string', enum: ['distinct', 'weak', 'derivative'] },
    uniqueAngle: { type: 'string', description: '이 글만의 각도(있다면, 없으면 "none")' },
    twists: {
      type: 'array',
      items: {
        type: 'object', additionalProperties: false,
        properties: {
          where: { type: 'string', description: '어느 부분을' },
          how: { type: 'string', description: '어떻게 비틀지(반례·재구성·범위축소 등)' },
          why: { type: 'string', description: '그러면 어떤 글과 차별화되는지' },
        },
        required: ['where', 'how', 'why'],
      },
      description: '각도가 weak/derivative일 때 비틀 지점 제안(최대 3개)',
    },
  },
  required: ['differentiationVerdict', 'uniqueAngle', 'twists'],
}

// ── personas (generic) ───────────────────────────────────────────────────────
const PERSONAS = [
  { id: '냉소적 시니어 동료', short: '시니어', seat: '동료가 눈 굴릴지 끄덕일지 직감으로. 현학·인용 밀도 과다·구체 사례 부족을 잡는다.' },
  { id: '30초 스키머', short: '스키머', seat: '헤더+각 문단 첫 문장만 훑는다. 골격으로 논지가 서나, 소제목이 정직한가, 표가 흐름을 끊나.' },
  { id: '글쓰기 편집자', short: '편집자', seat: '문장 리듬·종결 단조·영어 병기 밀도·잡초·음독 테스트. before→after를 최소 3개 제시.' },
  { id: '회의적 반대자', short: '반대자', seat: '가장 강한 반론(비용/실효성/새 개념어 피로)에 글이 답하는지 steelman.' },
  { id: '트렌드 감수자', short: '트렌드', seat: '트렌드가 논거인가 name-drop인가. 영어 개념어 밀도와 트렌드 균형. 리서치 브리프가 있으면 그 실측(트렌드 현재성·놓친 전개·경쟁 구조)과 대조해서 판정 — 추측 말고 브리프 근거로.' },
  { id: '한국어 AI-티 감별사', short: 'AI티', seat: '번역투·"A가 아니라 B" 공식·요약강박·헤지·영어병기·훈계조. 단 작가의 의도된 핵심 개념어는 보존 대상(결함 아님). 과교정으로 목소리 평탄화됐는지도 본다.' },
]

// 정확성 센티넬: 윤문 루프 전용 7번째 좌석
const ACCURACY_SENTINEL = {
  id: '정확성 센티넬', short: '정확성',
  seat: '이번 윤문이 *새로* 만든 과장/근거없는 단정만 본다. 절대·전부·항상·0에 가깝게·100%·고스란히 류의 강한 양화, 상관을 인과로 둔갑시킨 표현, 교육/타도메인 연구를 엔지니어링에 무리하게 끌어온 비약을 high로 신고. 원래 정확하던 문장은 건드리지 마라. remaining[].fix 에 안전한 헤지 표현을 제시.',
}

function fileCtx(path) {
  return ['대상 파일을 Read 도구로 먼저 전문 읽기(line 번호 확인): ' + path, '', GOAL, '목표 독자: ' + READER, TONE].join('\n')
}

// ── stage: light review (기본: 편집 관점 1회 + 결정론 lint) ──────────────────
async function runLightReview(path) {
  log('[Light-review] 통독 1회 + 결정론 슬롭 린트')
  const vaultRoot = path.includes('/20_Projects/') ? path.slice(0, path.indexOf('/20_Projects/')) : '/Users/taez/Projects/obsidian'
  const lintScript = vaultRoot + '/.claude/workflows/blog-slop-lint.mjs'
  return agent(
    [fileCtx(path), '',
      '한 명의 편집자로서 글을 처음부터 끝까지 한 번 읽어라. 웹 리서치, 별도 페르소나, 파일 수정은 하지 않는다.',
      '글의 장르와 발행 매체를 추정하되 기술블로그 구조를 에세이에 강제하지 않는다. 발행을 막는 구조·중복·비약만 최대 3개 issues에 적고, 보존할 강점은 strengths에 적는다.',
      '',
      '그 다음 Bash로 아래 결정론 lint를 정확히 한 번 실행하고 JSON 값을 그대로 옮겨라.',
      'node "' + lintScript + '" "' + path + '" --json',
      'verdict→slopVerdict, severityCount.high→slopHigh, severityCount.medium→slopMedium. high·medium hit만 slopHits에 "line:col [category] matched → fix" 형식으로 담는다. 명령 실패 시 slopVerdict="error".'
    ].join('\n'),
    { label: 'light-review', phase: 'Light-review', schema: LIGHT_REVIEW_SCHEMA, agentType: AGENT }
  )
}

// ── stage: fact-check ────────────────────────────────────────────────────────
async function runFactcheck(path) {
  log('[Fact-check] 검증 가능한 주장 추출 중...')
  const extracted = await agent(
    [fileCtx(path), '', '이 글에서 사실검증이 필요한 주장(수치·연구 귀속·정의·인용)을 모두 추출하라. 각 주장의 본문 표현과 귀속 출처를 적고, 수치나 특정 연구 귀속이면 critical=true.'].join('\n'),
    { label: 'extract-claims', phase: 'Fact-check', schema: CLAIM_LIST_SCHEMA, agentType: AGENT }
  )
  const claims = (extracted && extracted.claims) || []
  if (!claims.length) { log('[Fact-check] 추출된 주장 없음'); return { claims: [], verdicts: [] } }
  log('[Fact-check] ' + claims.length + '개 주장 → 주장별 웹 검증')

  const verdicts = await parallel(claims.map(c => () => agent(
    ['너는 팩트체커다. 오늘 기준 웹(WebSearch/WebFetch)으로 1차 출처를 찾아 검증하라. 기억·추측 금지, 블로그가 맞다고 가정 금지.', '',
      '주장: ' + c.text, '귀속 출처: ' + c.source, '핵심 주장 여부: ' + c.critical, '',
      '출처가 실재하고 주장을 실제로 뒷받침하는지, 수치는 정확한지, 귀속(저자/연도/매체)이 맞는지 확인한다.',
      '핵심 수치·연구 귀속이면 같은 패스에서 독립적인 권위 출처를 하나 더 대조하고, 없으면 confidence를 낮춘다. 별도 검증 에이전트를 다시 호출하지 않는다.',
      'verdict/근거/불일치/수정안 반환. id="' + c.id + '".'].join('\n'),
    { label: 'verify:' + c.id, phase: 'Fact-check', schema: VERDICT_SCHEMA, agentType: AGENT }
  )))
  return { claims, verdicts: verdicts.filter(Boolean) }
}

// ── stage: research (웹 grounding: 경쟁 구조 스캔 · 트렌드 현재성 · 차별화·각도) ──
async function runResearch(path) {
  log('[Research] 초안 프로필 추출...')
  const profile = await agent(
    [fileCtx(path), '', '이 글의 리서치 프로필을 뽑아라: 주제·한 줄 논지·섹션 골격(H2/H3 순서)·훅 유형·글이 내세우는 각도, 그리고 같은 주제의 경쟁 글과 최신 트렌드를 웹에서 찾기 위한 검색 키워드 3~6개(국문+영문 섞어).'].join('\n'),
    { label: 'draft-profile', phase: 'Research', schema: DRAFT_PROFILE_SCHEMA, agentType: AGENT }
  )
  if (!profile) { log('[Research] 프로필 추출 실패 — 스킵'); return { profile: null, landscape: null, trend: null, differentiation: null, brief: '', findings: [] } }

  const q = (profile.searchQueries || []).join(' / ')
  log('[Research] 경쟁 구조 스캔 + 트렌드 현재성 (병렬, 웹)')
  const [landscape, trend] = await parallel([
    () => agent(
      ['너는 콘텐츠 경쟁 분석가다. WebSearch/WebFetch로 같은 주제의 기존 글 5~8개를 실제로 찾아라(국문+영문). 검색 키워드: ' + q, '',
        '주제: ' + profile.topic, '초안 논지: ' + profile.thesis, '초안 골격: ' + (profile.skeleton || []).join(' > '), '',
        '각 글의 각도/구조/훅을 추출하고 초안과의 겹침도(high/med/low)를 매겨라. 가장 닮은 글, 이 주제에서 닳은 진부 패턴(clicheSignals: 예 "N가지 이유" listicle, "AI가 다 바꾼다" 식 도입), 초안 구조 신선도 종합(verdict)을 반환. 기억·추측 금지, 실제로 연 URL만.'].join('\n'),
      { label: 'landscape-scan', phase: 'Research', schema: LANDSCAPE_SCHEMA, agentType: AGENT }
    ),
    () => agent(
      ['너는 트렌드 감수자다. WebSearch/WebFetch로 최근 3~6개월 이 주제 담론을 확인하라. 검색 키워드: ' + q, '',
        '주제: ' + profile.topic, '초안 논지: ' + profile.thesis, '초안 각도: ' + profile.claimedAngle, '',
        '초안 프레이밍이 ahead/current/stale 중 무엇인지(근거 포함), 초안이 놓친 최근 전개(missedDevelopments), 이미 식은 프레이밍 신호(stalePhrasings)를 반환. 기억·추측 금지, 검색으로 확인한 것만.'].join('\n'),
      { label: 'trend-currency', phase: 'Research', schema: TREND_SCHEMA, agentType: AGENT }
    ),
  ])

  log('[Research] 차별화·각도 종합')
  const differentiation = await agent(
    ['너는 편집장이다. 아래 초안 프로필·경쟁 지형·트렌드 판정을 종합해 이 글의 차별화를 진단하라.', '',
      '## 초안', '주제: ' + profile.topic, '논지: ' + profile.thesis, '내세운 각도: ' + profile.claimedAngle, '골격: ' + (profile.skeleton || []).join(' > '), '',
      '## 경쟁 지형', landscape ? ('신선도: ' + landscape.verdict + ' / 가장 닮은 글: ' + landscape.mostSimilar + ' / 진부패턴: ' + (landscape.clicheSignals || []).join(', ')) : '(스캔 실패)', '',
      '## 트렌드', trend ? (trend.framingStatus + ' — ' + trend.evidence) : '(판정 실패)', '',
      '이 글만의 각도가 distinct/weak/derivative 중 무엇인지 판정(uniqueAngle). 약하거나 없으면 어디(where)를 어떻게(how: 반례·재구성·범위축소) 비틀면 어떤 글과 차별화되는지(why) 구체 제안 최대 3개(twists).'].join('\n'),
    { label: 'differentiation', phase: 'Research', schema: DIFF_SCHEMA, agentType: AGENT }
  )

  // ── JS 합성 (거대 JSON 에이전트 없음, raw 결과는 그대로 반환) ──
  const briefLines = []
  if (trend) {
    briefLines.push('### 트렌드 현재성: ' + trend.framingStatus)
    if (trend.evidence) briefLines.push('- 근거: ' + trend.evidence)
    if ((trend.missedDevelopments || []).length) briefLines.push('- 놓친 최근 전개: ' + trend.missedDevelopments.join(' / '))
    if ((trend.stalePhrasings || []).length) briefLines.push('- 식은 프레이밍: ' + trend.stalePhrasings.join(' / '))
  }
  if (landscape) {
    briefLines.push('### 경쟁 구조: ' + landscape.verdict + ' (가장 닮은 글 — ' + landscape.mostSimilar + ')')
    if ((landscape.clicheSignals || []).length) briefLines.push('- 피해야 할 진부 패턴: ' + landscape.clicheSignals.join(' / '))
  }
  if (differentiation) {
    briefLines.push('### 차별화 판정: ' + differentiation.differentiationVerdict + (differentiation.uniqueAngle && differentiation.uniqueAngle !== 'none' ? ' (이 글만의 각도: ' + differentiation.uniqueAngle + ')' : ''))
  }
  const brief = briefLines.join('\n')

  // 줄 단위로 고칠 수 있는 트렌드/프레이밍만 polish findings 로 머지(구조 차별화는 제외 — 리포트 플래그만)
  const findings = []
  if (trend) {
    (trend.stalePhrasings || []).slice(0, 4).forEach((s) => findings.push({
      severity: 'medium', line: '?', quote: s, persona: '트렌드 실측',
      issue: '이미 식었거나 흔해진 프레이밍', suggestion: '최신 담론에 맞게 표현 갱신 또는 제거',
    }))
    ;(trend.missedDevelopments || []).slice(0, 2).forEach((m) => findings.push({
      severity: 'medium', line: '?', quote: '(해당 주제 전반)', persona: '트렌드 실측',
      issue: '초안이 놓친 최근 전개: ' + m, suggestion: '한 줄로 현재성 보강(과장 없이)',
    }))
  }

  return { profile, landscape, trend, differentiation, brief, findings }
}

// ── stage: editorial diagnose (JS aggregation, no synthesis agent) ───────────
async function runEditorial(path, researchBrief) {
  log('[Editorial] 6인 패널 통독 진단...')
  const ground = researchBrief ? ('\n## 리서치 브리프(실측 근거 — 트렌드/구조 판정에 활용)\n' + researchBrief + '\n') : ''
  const reports = (await parallel(PERSONAS.map(p => () =>
    agent([fileCtx(path), ground, '## 너의 좌석: ' + p.id, p.seat, '',
      'persona="' + p.id + '". 이 좌석에서 본 것만, line 인용으로. whatWorks에 보존할 강점.'].join('\n'),
      { label: 'lens:' + p.short, phase: 'Editorial', schema: PERSONA_SCHEMA, agentType: AGENT })
  ))).filter(Boolean)

  // JS 집계 (거대 JSON synthesis 에이전트 대신 — hang 원인 차단)
  const rank = { high: 0, medium: 1, low: 2 }
  const findings = reports.flatMap(r => (r.findings || []).map(f => ({ ...f, persona: r.persona })))
    .sort((a, b) => (rank[a.severity] ?? 3) - (rank[b.severity] ?? 3))
  const keepList = reports.map(r => '- (' + r.persona + ') ' + r.whatWorks).join('\n')
  const goalScore = reports.map(r => r.achievesGoal)
  return { reports, findings, keepList, goalScore }
}

// ── stage: polish loop (editor → 6인 + 정확성 센티넬 재검수 → 수렴까지) ────────
async function runPolish(workPath, initialBrief, keepList) {
  log('[Polish] 작업 사본 준비: ' + workPath)
  await agent(
    ['Bash 도구로 원본을 작업 사본으로 복사하라(원본 보존). 정확히 이 명령을 실행: cp "' + FILE + '" "' + workPath + '"  그리고 결과만 요약 반환.'].join('\n'),
    { label: 'setup-copy', phase: 'Polish', agentType: AGENT }
  )

  const KEEP = ['## 절대 보존(건드리지 말 것)', keepList || '- 작가의 강점 문장/구체 사례/데이터/의도된 핵심 개념어/1인칭 메타',
    '', '## 목소리 규칙', '- 존댓말+1인칭 유지. 외과적 최소 수정. 전체 리라이트·과교정(목소리 평탄화) 금지.',
    '- 프론트매터/위키링크/이미지/표 구조 보존.'].join('\n')

  const reviewers = PERSONAS.concat([ACCURACY_SENTINEL])
  let brief = initialBrief
  let prevRemaining = Infinity
  let converged = false
  const roundLog = []
  let finalReviews = []

  for (let round = 1; round <= MAX_ROUNDS; round++) {
    log('[Polish] 라운드 ' + round + ': 윤문 적용')
    const edit = await agent(
      ['너는 한국어 기술블로그 에디터다. ' + workPath + ' 를 Read 후 Edit 도구로 정확히 부분 수정하라. 전체 리라이트 금지.', '',
        brief, '', KEEP, '',
        '끝나면 changeCount/changesSummary/preservedVoiceNote 반환.'].join('\n'),
      { label: 'edit:r' + round, phase: 'Polish', schema: EDIT_SCHEMA, agentType: AGENT }
    )
    const changeCount = (edit && typeof edit.changeCount === 'number') ? edit.changeCount : 0
    log('[Polish] 라운드 ' + round + ': ' + changeCount + '곳 → 패널 재검수')

    const reviews = (await parallel(reviewers.map(p => () =>
      agent(['이미 윤문이 적용된 파일을 Read로 다시 읽고 판정: ' + workPath, '', GOAL, '목표 독자: ' + READER, TONE, '',
        '## 좌석: ' + p.id, p.seat, '',
        'remaining에는 목표를 막는 high/medium만(없으면 빈 배열 + satisfied=true). 새 트집 금지. 보존 대상은 결함 아님. persona="' + p.id + '".'].join('\n'),
        { label: 'review:' + p.short + ':r' + round, phase: 'Polish', schema: REVIEW_SCHEMA, agentType: AGENT })
    ))).filter(Boolean)
    finalReviews = reviews

    const remaining = reviews.flatMap(r => (r.remaining || []).filter(f => f.severity === 'high' || f.severity === 'medium'))
    const okCount = reviews.filter(r => r.satisfied || !(r.remaining || []).some(f => f.severity === 'high' || f.severity === 'medium')).length
    roundLog.push({ round, changeCount, okCount, totalReviewers: reviews.length, remainingHighMed: remaining.length, summary: edit ? edit.changesSummary : '(edit 실패)' })

    if (okCount === reviews.length && reviews.length > 0) { converged = true; break }
    if (changeCount === 0) { log('[Polish] 변경 0건 — 정지'); break }
    if (remaining.length >= prevRemaining) { log('[Polish] 진전 없음 — 수렴 정지'); break }
    prevRemaining = remaining.length
    brief = ['## 이전 라운드 후에도 남은 high/medium만 외과적으로 더 고쳐라. 좋은 부분은 손대지 마라.',
      remaining.map(f => '- [' + f.severity + '] line ' + f.line + ': ' + f.issue + ' → ' + f.fix).join('\n'),
      '', KEEP].join('\n')
  }
  return { workPath, converged, rounds: roundLog, finalReviews }
}

// ── stage: final gate (통독 + 델타 재사실검증 + 구조검사) ──────────────────────
async function runGate(targetPath) {
  log('[Final-gate] 통독 일관성 + 델타 재사실검증 + 구조 회귀검사 + 결정론 슬롭 린트')
  // 린트 절대경로: 초안 경로에서 vault 루트를 역산(20_Projects 앞부분)
  const vaultRoot = targetPath.includes('/20_Projects/') ? targetPath.slice(0, targetPath.indexOf('/20_Projects/')) : '/Users/taez/Projects/obsidian'
  const lintScript = vaultRoot + '/.claude/workflows/blog-slop-lint.mjs'
  const [coherence, structure, slop] = await parallel([
    () => agent(['너는 이 글을 *처음 읽는* 목표 독자다: ' + READER + '. ' + targetPath + ' 를 Read로 끝까지 한 번에 읽어라.', '', GOAL, '',
      '조각편집 누적으로 생긴 전체 차원의 문제만 본다: 전환/흐름 끊김, 편집 후 중복, 소제목-본문 불일치, 한 줄 TL;DR이 서는가. 그리고 윤문이 새로 만든 과장/근거없는 단정(factDeltas)도 함께 신고. coherenceVerdict/coherenceIssues/factDeltas 채우고 structure 항목은 임시로 true/빈값.'].join('\n'),
      { label: 'fresh-read', phase: 'Final-gate', schema: GATE_SCHEMA, agentType: AGENT }),
    () => agent(['Bash 도구로 ' + targetPath + ' 의 구조 무결성을 점검하라. 확인: 프론트매터(--- 쌍), 위키링크 [[ ]] 짝, 이미지 ![](...) 임베드, 마크다운 표 헤더, 깨진 링크. grep/wc로 세고, structureOk(bool)와 structureNote(무엇을 확인했고 이상 있는지)만 채워라. 나머지 필드는 임시값.'].join('\n'),
      { label: 'structure-check', phase: 'Final-gate', schema: GATE_SCHEMA, agentType: AGENT }),
    // 결정론 슬롭 린트: LLM 판단이 아니라 명령 출력을 그대로 정리한다(_anti-slop-lexicon.md 단일 출처).
    () => agent(['너는 명령 실행기다. 판단하지 말고 아래 결정론 린트를 Bash로 실행해 출력 JSON만 정리하라.',
      'node "' + lintScript + '" "' + targetPath + '" --json', '',
      '출력 JSON에서: verdict, severityCount.high/medium/low 를 그대로 옮기고, hits 중 severity가 high·medium인 것만 골라 "line:col [category] matched → fix" 형식으로 topHits에 담아라. 밀도(densities)에서 exceeded=true인 항목도 topHits에 "[밀도] id rate/임계 → fix"로 추가. 명령이 비정상 종료/미설치면 verdict="error", 숫자는 0, topHits에 에러 메시지.'].join('\n'),
      { label: 'slop-lint', phase: 'Final-gate', schema: SLOP_LINT_SCHEMA, agentType: AGENT }),
  ])
  return {
    coherenceVerdict: coherence ? coherence.coherenceVerdict : 'unknown',
    coherenceIssues: coherence ? coherence.coherenceIssues : [],
    factDeltas: coherence ? coherence.factDeltas : [],
    structureOk: structure ? structure.structureOk : null,
    structureNote: structure ? structure.structureNote : '(검사 실패)',
    slopLint: slop || { verdict: 'error', high: 0, medium: 0, low: 0, topHits: ['린트 실행 실패'] },
  }
}

// ── orchestrate ──────────────────────────────────────────────────────────────
const out = { file: FILE, stages: STAGES }

if (STAGES.includes('light')) out.light = await runLightReview(FILE)

if (STAGES.includes('factcheck')) out.factcheck = await runFactcheck(FILE)

if (STAGES.includes('research')) {
  out.research = await runResearch(FILE)
  if (out.research && out.research.differentiation) {
    log('[Research] 판정 → 구조:' + (out.research.landscape ? out.research.landscape.verdict : '?') +
        ' / 트렌드:' + (out.research.trend ? out.research.trend.framingStatus : '?') +
        ' / 차별화:' + out.research.differentiation.differentiationVerdict)
  }
}

if (STAGES.includes('editorial')) {
  out.editorial = await runEditorial(FILE, out.research ? out.research.brief : '')
  // 리서치의 줄 단위 발견을 에디토리얼 findings 앞에 머지(구조 차별화는 제외 — 리포트 플래그만)
  if (out.research && out.research.findings && out.research.findings.length) {
    out.editorial.findings = out.research.findings.concat(out.editorial.findings || [])
  }
}

if (STAGES.includes('polish')) {
  if (!WORK) {
    log('[Polish] args.workCopy가 없어 수정 단계를 건너뜁니다. 파일명 버전 사본을 자동 생성하지 않습니다.')
    out.polish = { error: 'workCopy required for polish' }
  } else {
    const keepList = (out.editorial && out.editorial.keepList) ||
      (await agent([fileCtx(FILE), '', '이 글에서 절대 보존해야 할 강점(구체 사례/데이터/의도된 핵심 개념어/1인칭 메타)을 줄 단위로 나열하라.'].join('\n'),
        { label: 'derive-keep', phase: 'Polish', agentType: AGENT }))
    const brief = (out.editorial && out.editorial.findings && out.editorial.findings.length)
      ? ['## 이번 라운드 윤문 지시 — 아래 진단을 외과적으로 반영(우선순위: high→medium)',
          out.editorial.findings.filter(f => f.severity !== 'low')
            .map(f => '- [' + f.severity + '] line ' + f.line + ' "' + f.quote + '": ' + f.issue + ' → ' + f.suggestion).join('\n')].join('\n')
      : '에디토리얼 진단이 없으니, 먼저 ' + WORK + ' 를 통독하며 목표/반목표 기준으로 톤·구조·AI-티 문제를 직접 찾아 외과적으로 고쳐라.'
    out.polish = await runPolish(WORK, brief, typeof keepList === 'string' ? keepList : (keepList || ''))
  }
}

if (STAGES.includes('gate')) {
  const target = (out.polish && out.polish.workPath) ? out.polish.workPath : FILE
  out.gate = await runGate(target)
  if (out.gate && out.gate.slopLint) {
    const s = out.gate.slopLint
    log('[Final-gate] 슬롭 린트: ' + s.verdict + ' (high ' + s.high + ' · medium ' + s.medium + ')')
    if (s.verdict === 'fail' || s.verdict === 'warn') (s.topHits || []).slice(0, 8).forEach((h) => log('  · ' + h))
  }
}

log('완료. stages=' + STAGES.join(','))
return out
