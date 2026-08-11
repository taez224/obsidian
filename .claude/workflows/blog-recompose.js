export const meta = {
  name: 'blog-recompose',
  description: '여러 소스의 경험·개념·근거를 대조해 새 글의 논지와 저자 소유 아웃라인을 만든다. 기본은 Outline에서 멈추며, 전문은 writeFullDraft: true일 때만 작성한다.',
  whenToUse: '기존 자료를 한 글로 재구성하거나 초안의 구조를 크게 바꿀 때. 전문 작성 여부와 발행면·재사용 정책을 args로 명시한다.',
  phases: [
    { title: 'Mine' },
    { title: 'Outline' },
    { title: 'Compose' },
    { title: 'Gate' },
  ],
}

// 사용법 (args):
// {
//   experienceSource: "<경험 자료 절대경로>",
//   conceptSource: "<개념 자료 절대경로>",
//   substanceSource: "<현재 초안/리서치 절대경로>",
//   output: "<전문을 쓸 절대경로>",             // writeFullDraft=true일 때만 필수
//   writeFullDraft: false,                      // 기본 false
//   publicationSurface: "company-tech|personal-tech|brunch|other",
//   reusePolicy: "detect|intentional-adaptation",
//   brandLead: "<이번 글에서 특히 살릴 저자 관점>", // 선택
//   outlineCandidates: 3                       // 선택, 1~5
// }
//
// 원칙:
// - 소스는 역할이 다를 뿐 서열이 없다. 경험을 만들거나 리서치를 저자의 결론으로 승격하지 않는다.
// - 인접 글 중복은 같은 어휘가 아니라 국소 주장 + 장면/증거 + 착지의 결합으로 판정한다.
// - 반복 렌즈와 저자 캐릭터는 허용한다. 다른 발행면의 의도적 자립형 재구성도 계약에 따라 허용한다.
// - 기본 산출물은 저자가 직접 쓸 수 있는 아웃라인이다. 전문 작성과 파일 쓰기는 명시적으로만 실행한다.

let A = args || {}
if (typeof A === 'string') { try { A = JSON.parse(A) } catch (e) { A = {} } }
const EXP = A.experienceSource
const CONCEPT = A.conceptSource
const SUBSTANCE = A.substanceSource
const OUT = A.output || ''
const WRITE_FULL_DRAFT = A.writeFullDraft === true
const SURFACE = A.publicationSurface || 'unspecified'
const REUSE_POLICY = A.reusePolicy || 'detect'
const BRAND = A.brandLead || ''
const NUM_OUTLINES = Math.max(1, Math.min(5, A.outlineCandidates || 3))
const AGENT = 'general-purpose'
const VAULT = A.vaultRoot || '/Users/taez/Projects/obsidian'
const VOICE = VAULT + '/.agents/skills/taez-insight-blog-writer/references/voice-profile.md'
const KOREAN = VAULT + '/.agents/skills/taez-insight-blog-writer/references/korean-first-draft.md'

if (!EXP || !CONCEPT || !SUBSTANCE || (WRITE_FULL_DRAFT && !OUT)) {
  log('❌ args 필요: experienceSource, conceptSource, substanceSource. writeFullDraft=true이면 output도 필요합니다.')
  return { error: 'missing required args', got: A }
}

const MATERIAL_SCHEMA = {
  type: 'object', additionalProperties: false,
  properties: {
    sourcePath: { type: 'string' },
    role: { type: 'string', enum: ['experience', 'concept', 'substance'] },
    publicationStatus: { type: 'string', enum: ['published', 'draft', 'note', 'unknown'] },
    localClaim: { type: 'string', description: '이 소스가 실제로 착지한 국소 주장' },
    openingScene: { type: 'string', description: '도입 장면/질문, 없으면 "none"' },
    climaxEvidence: { type: 'string', description: '핵심 경험·사례·자료, 없으면 "none"' },
    landing: { type: 'string', description: '마지막에 남긴 결론/기준' },
    episodes: { type: 'array', items: { type: 'string' }, description: '실제로 적힌 경험·판단 변화·마찰' },
    artifacts: { type: 'array', items: { type: 'string' }, description: '커맨드·PR·도표·워크플로 등 확인 가능한 실행 증거' },
    reusableClaims: {
      type: 'array',
      items: {
        type: 'object', additionalProperties: false,
        properties: {
          claim: { type: 'string' },
          attribution: { type: 'string', description: '출처/저자/연도, 없으면 "author"' },
          verificationStatus: { type: 'string', enum: ['verified', 'unresolved', 'not_checked'] },
        },
        required: ['claim', 'attribution', 'verificationStatus'],
      },
    },
    authorLanguage: { type: 'array', items: { type: 'string' }, description: '그대로 보존할 가치가 있는 실제 표현' },
    boundaries: { type: 'array', items: { type: 'string' }, description: '이 소스만으로 말할 수 없는 것과 빠진 개인 근거' },
  },
  required: ['sourcePath', 'role', 'publicationStatus', 'localClaim', 'openingScene', 'climaxEvidence', 'landing', 'episodes', 'artifacts', 'reusableClaims', 'authorLanguage', 'boundaries'],
}

const SYNTHESIS_SCHEMA = {
  type: 'object', additionalProperties: false,
  properties: {
    candidateTheses: { type: 'array', items: { type: 'string' }, description: '소스가 실제로 지지하는 논지 후보' },
    evidenceMap: { type: 'array', items: { type: 'string' }, description: '논지와 경험·아티팩트·외부 근거의 연결' },
    overlapRisks: { type: 'array', items: { type: 'string' }, description: '같은 주장+장면/증거+착지 조합의 반복 위험' },
    safeReuse: { type: 'array', items: { type: 'string' }, description: '반복 가능한 렌즈·어휘·맥락과 그 이유' },
    unresolved: { type: 'array', items: { type: 'string' }, description: '저자가 채우거나 검증해야 할 빈칸' },
  },
  required: ['candidateTheses', 'evidenceMap', 'overlapRisks', 'safeReuse', 'unresolved'],
}

const OUTLINE_SCHEMA = {
  type: 'object', additionalProperties: false,
  properties: {
    thesis: { type: 'string', description: '독자에게 남길 판단 한 문장' },
    movement: { type: 'string', enum: ['changed-judgment', 'follow-the-cost', 'failure-led', 'two-cases', 'changed-question'] },
    titleOptions: {
      type: 'array',
      items: {
        type: 'object', additionalProperties: false,
        properties: {
          title: { type: 'string' },
          strategy: { type: 'string' },
          foregrounds: { type: 'string', description: '글의 어느 장면·판단·착지를 전면에 세우는지' },
        },
        required: ['title', 'strategy', 'foregrounds'],
      },
      description: '필요할 때만 2~3개의 실질적으로 다른 제목 전략',
    },
    opening: { type: 'string', description: '출발 장면·마찰·질문. 완성 산문이 아니라 집필 메모' },
    sections: {
      type: 'array',
      items: {
        type: 'object', additionalProperties: false,
        properties: {
          heading: { type: 'string' },
          role: { type: 'string' },
          sceneOrExperience: { type: 'string', description: '직접 쓸 장면/경험, 없으면 저자 질문' },
          claim: { type: 'string' },
          evidence: { type: 'array', items: { type: 'string' } },
          boundaryOrCounter: { type: 'string', description: '이 절에 실제로 필요한 경계·반론이 있을 때만 사용' },
          handoffQuestion: { type: 'string', description: '다음 절의 독립적인 질문을 열어야 할 때만 사용' },
        },
        required: ['heading', 'role', 'sceneOrExperience', 'claim', 'evidence'],
      },
    },
    climax: { type: 'string', description: '글의 무게중심이 되는 실행 증거·발견' },
    landing: { type: 'string', description: '마지막에 남길 기준' },
    overlapDecision: { type: 'string', description: '가장 인접한 글과 무엇을 공유하고 어디서 갈라지는지' },
    authorPrompts: { type: 'array', items: { type: 'string' }, description: '발명하지 않고 저자가 채워야 할 경험·판단·검증' },
  },
  required: ['thesis', 'movement', 'opening', 'sections', 'climax', 'landing', 'overlapDecision', 'authorPrompts'],
}

const SELECTION_SCHEMA = {
  type: 'object', additionalProperties: false,
  properties: {
    selectedIndex: { type: 'number' },
    rationale: { type: 'string' },
    preserveFromOthers: { type: 'array', items: { type: 'string' } },
    risks: { type: 'array', items: { type: 'string' } },
  },
  required: ['selectedIndex', 'rationale', 'preserveFromOthers', 'risks'],
}

const MOVEMENT_PLAN_SCHEMA = {
  type: 'object', additionalProperties: false,
  properties: {
    movements: {
      type: 'array',
      items: { type: 'string', enum: ['changed-judgment', 'follow-the-cost', 'failure-led', 'two-cases', 'changed-question'] },
    },
    reason: { type: 'string' },
  },
  required: ['movements', 'reason'],
}

const COMPOSE_SCHEMA = {
  type: 'object', additionalProperties: false,
  properties: {
    wordCountApprox: { type: 'number' },
    sectionsWritten: { type: 'array', items: { type: 'string' } },
    voiceNote: { type: 'string' },
    factsPreserved: { type: 'array', items: { type: 'string' } },
    unresolvedLeftVisible: { type: 'array', items: { type: 'string' } },
  },
  required: ['wordCountApprox', 'sectionsWritten', 'voiceNote', 'factsPreserved', 'unresolvedLeftVisible'],
}

const GATE_SCHEMA = {
  type: 'object', additionalProperties: false,
  properties: {
    voiceMatch: { type: 'string', enum: ['strong', 'ok', 'weak'] },
    titleAndHeadingIssues: { type: 'array', items: { type: 'string' } },
    unsupportedClaims: { type: 'array', items: { type: 'string' } },
    accidentalOverlap: { type: 'array', items: { type: 'string' } },
    structureOk: { type: 'boolean' },
    topFixes: { type: 'array', items: { type: 'string' } },
  },
  required: ['voiceMatch', 'titleAndHeadingIssues', 'unsupportedClaims', 'accidentalOverlap', 'structureOk', 'topFixes'],
}

function minePrompt(path, role) {
  return [
    'Read 도구로 대상 파일을 전문 읽어라: ' + path,
    '이 자료의 역할은 ' + role + '이지만, 실제 내용이 역할 설명과 다르면 내용이 우선이다.',
    'frontmatter와 본문을 근거로 publicationStatus를 판정하고, 제목/목차가 아니라 본문이 실제로 한 국소 주장·도입 장면·클라이맥스 증거·착지를 기록한다.',
    '실제로 적힌 경험, 커맨드·PR·도표·워크플로 같은 아티팩트, 재사용 가능한 주장과 귀속, 보존할 저자 표현, 이 자료만으로 말할 수 없는 경계를 분리한다.',
    '수치·인용·외부 연구가 본문 안에서 1차 출처까지 검증되었는지 알 수 없으면 verificationStatus="not_checked" 또는 "unresolved"로 둔다. 추정으로 verified를 주지 않는다.',
    '사건·판단 변화·성과를 만들지 않는다. sourcePath="' + path + '", role="' + role + '".',
  ].join('\n')
}

async function mine() {
  log('[Mine] 세 소스의 본문·증거·착지 병렬 채굴')
  const materials = (await parallel([
    () => agent(minePrompt(EXP, 'experience'), { label: 'mine:experience', phase: 'Mine', schema: MATERIAL_SCHEMA, agentType: AGENT }),
    () => agent(minePrompt(CONCEPT, 'concept'), { label: 'mine:concept', phase: 'Mine', schema: MATERIAL_SCHEMA, agentType: AGENT }),
    () => agent(minePrompt(SUBSTANCE, 'substance'), { label: 'mine:substance', phase: 'Mine', schema: MATERIAL_SCHEMA, agentType: AGENT }),
  ])).filter(Boolean)

  const synthesis = await agent([
    '너는 자료 편집자다. 저자 목소리 기준을 먼저 Read하라: ' + VOICE,
    '아래 소스들을 대조해 소스가 실제로 지지하는 논지 후보, 논지-증거 연결, 인접 글 중복 위험, 안전하게 반복할 수 있는 렌즈, 미검증/미작성 빈칸을 정리하라.',
    '발행면: ' + SURFACE + ' / 재사용 정책: ' + REUSE_POLICY + (BRAND ? ' / 이번 글의 강조점: ' + BRAND : ''),
    '중복은 같은 어휘가 아니라 같은 국소 주장에 같은 장면 또는 증거를 쓰고 같은 결론에 착지하는 경우다. 반복 렌즈와 저자 캐릭터는 허용한다.',
    'reusePolicy="intentional-adaptation"이면 다른 지면을 위한 자립형 재구성을 허용하되 무엇을 재사용하는지 밝힌다. 그 밖에는 새 질문·경계·반례·증거가 필요하다.',
    '외부 자료의 발견을 저자의 제목이나 결론으로 자동 승격하지 않는다.',
    JSON.stringify(materials),
  ].join('\n'), { label: 'mine:synthesis', phase: 'Mine', schema: SYNTHESIS_SCHEMA, agentType: AGENT })

  return { materials, synthesis }
}

const MOVEMENTS = [
  ['changed-judgment', '실제 판단이 바뀌었을 때만: 이전 판단 → 부분적으로 맞았던 점 → 경계 발견 → 새 기준'],
  ['follow-the-cost', '판단은 유지되지만 비용이 보였을 때: 결정 → 청구된 대가 → 누가 치렀는가 → 다시 고를 기준'],
  ['failure-led', '실제 실패가 있을 때: 무너진 장면 → 원인 → 바꾼 것 → 아직 남은 한계'],
  ['two-cases', '서로 다른 실제 사례가 있을 때: 통한 경우와 깨진 경우 → 경계선 → 적용 기준'],
  ['changed-question', '답보다 질문 재구성이 핵심일 때: 처음 질문 → 어긋남 → 새 질문 → 판단 기준'],
]

async function outline(mined) {
  log('[Outline] 재료에 맞는 움직임 후보 ' + NUM_OUTLINES + '개 선택')
  const movementPlan = await agent([
    '아래 자료가 실제로 지지하는 글의 움직임을 최대 ' + NUM_OUTLINES + '개 고른다. 다양성보다 근거 적합성이 우선이다.',
    '선택지: ' + MOVEMENTS.map((m) => m[0] + '=' + m[1]).join(' / '),
    '판단이 바뀌지 않았는데 changed-judgment를, 실패가 없는데 failure-led를 고르지 않는다. 하나만 강하면 하나만 반환해도 된다.',
    '자료: ' + JSON.stringify(mined),
  ].join('\n'), { label: 'outline:movements', phase: 'Outline', schema: MOVEMENT_PLAN_SCHEMA, agentType: AGENT })
  const planned = ((movementPlan && movementPlan.movements) || []).slice(0, NUM_OUTLINES)
  const chosenMovements = (planned.length ? planned : ['changed-question']).map((id) => MOVEMENTS.find((m) => m[0] === id)).filter(Boolean)
  log('[Outline] 움직임: ' + chosenMovements.map((m) => m[0]).join(', '))

  const candidates = (await parallel(chosenMovements.map((movement, index) => () => agent([
    '너는 한국어 블로그 구조 편집자다. 저자 목소리 기준을 Read하라: ' + VOICE,
    '발행면: ' + SURFACE + ' / 재사용 정책: ' + REUSE_POLICY + (BRAND ? ' / 강조점: ' + BRAND : ''),
    '이 후보가 시험할 움직임: ' + movement[0] + ' — ' + movement[1],
    '자료: ' + JSON.stringify(mined),
    '자료가 이 움직임을 지지하지 않으면 반전이나 실패를 만들지 말고, 가장 가까운 정직한 움직임으로 바꿔 movement에 기록한다.',
    '완성 산문 대신 저자가 직접 쓸 아웃라인을 만든다. 각 절에 역할·직접 쓸 장면/경험·주장·근거를 두고, 경계/반론과 다음 질문은 그 절에서 실제 역할이 있을 때만 필드를 사용한다.',
    '자료의 경계나 금지사항을 독자에게 알릴 문장으로 자동 변환하지 않는다. 쓰지 않으면 충족되는 가드레일은 아웃라인 산문 항목이 아니다.',
    '리서치는 근거로 붙이고 문헌 검토를 글의 척추로 만들지 않는다. 개인 장면·판단·수치가 없으면 authorPrompts에 빈칸으로 남긴다.',
    '제목은 도입 장면 하나가 아니라 실제 클라이맥스나 착지를 약속해야 한다. 제목과 절 제목을 같은 문장으로 쓰지 않는다. 필요할 때만 2~3개의 실질적으로 다른 제목 전략을 만든다.',
  ].join('\n'), { label: 'outline:c' + (index + 1), phase: 'Outline', schema: OUTLINE_SCHEMA, agentType: AGENT })))).filter(Boolean)
  if (!candidates.length) return { candidates: [], selected: null, selection: null }

  const selection = await agent([
    '너는 최종 구조를 고르는 편집자다. 숫자 점수 없이 다음 기준으로 가장 강한 후보 하나를 고른다: 소스가 실제로 지지하는 논지, 개인 증거가 클라이맥스를 받치는가, 제목이 착지를 가리키는가, 인접 글과 국소 결론이 갈리는가, 발행면에 맞는가.',
    'selectedIndex는 0부터 시작한다. 다른 후보에서 살릴 요소와 선택 후보의 위험을 적는다.',
    '발행면: ' + SURFACE + ' / 재사용 정책: ' + REUSE_POLICY,
    '후보: ' + JSON.stringify(candidates),
  ].join('\n'), { label: 'outline:select', phase: 'Outline', schema: SELECTION_SCHEMA, agentType: AGENT })

  const selectedIndex = selection && Number.isInteger(selection.selectedIndex) && selection.selectedIndex >= 0 && selection.selectedIndex < candidates.length
    ? selection.selectedIndex : 0
  const base = candidates[selectedIndex]
  const selected = await agent([
    '너는 저자에게 넘길 최종 아웃라인을 정리한다. 선택된 후보의 논지와 움직임을 보존하고, 다른 후보에서 살릴 요소는 겹치지 않을 때만 이식한다.',
    '선택 후보: ' + JSON.stringify(base),
    '선택 이유와 위험: ' + JSON.stringify(selection),
    '자료 경계: ' + JSON.stringify(mined.synthesis && mined.synthesis.unresolved),
    '완성 산문을 쓰지 말고 같은 OUTLINE_SCHEMA로 반환한다. 선택 필드를 형식적으로 채우지 말고, 제목과 첫 절 제목 중복, 결론 선취, 외부 자료가 주인공이 되는 문제를 마지막으로 제거한다.',
  ].join('\n'), { label: 'outline:final', phase: 'Outline', schema: OUTLINE_SCHEMA, agentType: AGENT })

  return { movementPlan, candidates, selection, selected: selected || base }
}

async function compose(mined, selectedOutline) {
  log('[Compose] 명시적으로 요청된 전문 작성 → ' + OUT)
  return agent([
    '너는 TaeZ의 한국어 블로그 공동 집필자다. 먼저 목소리와 한국어 초안 기준을 Read하라: ' + VOICE + ' / ' + KOREAN,
    '세 원자료를 다시 Read해 사실·장면·표현을 확인한 뒤, 최종 아웃라인에 따라 새 글을 ' + OUT + ' 에 Write 도구로 저장한다.',
    '발행면: ' + SURFACE + ' / 재사용 정책: ' + REUSE_POLICY,
    '소스에 없는 사건·대화·판단 변화·성과·수치를 만들지 않는다. verificationStatus가 verified가 아닌 외부 주장은 확정 사실처럼 쓰지 않는다.',
    '같은 렌즈와 경험을 다시 다룰 수 있다. 다만 의도 없이 같은 국소 주장+장면/증거+착지를 복제하지 않는다. intentional-adaptation이면 해당 지면에서 이해되도록 필요한 맥락을 자립적으로 쓴다.',
    '외부 연구는 저자의 판단을 받치는 만큼만 쓴다. 제목이나 절 제목이 출처의 관찰을 저자의 논지로 가장하지 않게 한다.',
    'frontmatter와 링크 형식은 발행면과 대상 경로의 기존 형식을 따른다. Obsidian 정본이면 wikilink를 보존하고, 외부 발행용 원고면 공개 링크나 자립적인 맥락을 쓴다.',
    '최종 아웃라인: ' + JSON.stringify(selectedOutline),
    '채굴 자료: ' + JSON.stringify(mined),
    '다 쓴 뒤 작성 결과와 남겨둔 미검증 빈칸을 반환한다.',
  ].join('\n'), { label: 'compose', phase: 'Compose', schema: COMPOSE_SCHEMA, agentType: AGENT })
}

async function gate(mined) {
  log('[Gate] 전문의 목소리 · 근거 · 제목 · 인접 글 중복 점검')
  return agent([
    'Read 도구로 완성 원고를 전문 읽어라: ' + OUT,
    '저자 목소리 기준도 Read하라: ' + VOICE,
    '아래 채굴 자료와 대조한다: ' + JSON.stringify(mined),
    '제목이 글의 실제 클라이맥스/착지를 가리키는지, 제목과 절 제목이 겹치는지, 소제목이 각 절의 역할과 맞는지 확인한다.',
    '소스에 없는 장면·대화·판단 변화·성과·수치, unresolved/not_checked를 확정 사실처럼 쓴 부분을 unsupportedClaims에 기록한다.',
    'accidentalOverlap에는 같은 국소 주장+같은 장면/증거+같은 착지를 의도 없이 반복한 경우만 기록한다. 반복 어휘·렌즈만으로 신고하지 않는다. reusePolicy=' + REUSE_POLICY + '를 반영한다.',
    'Bash로 프론트매터, 마크다운 링크/이미지/표의 기본 구조 무결성도 확인한다.',
  ].join('\n'), { label: 'gate', phase: 'Gate', schema: GATE_SCHEMA, agentType: AGENT })
}

const out = { output: WRITE_FULL_DRAFT ? OUT : null, writeFullDraft: WRITE_FULL_DRAFT, publicationSurface: SURFACE, reusePolicy: REUSE_POLICY }
out.mined = await mine()
out.outline = await outline(out.mined)
if (!out.outline.selected) { log('[Outline] 후보 생성 실패 — 정지'); return out }
log('[Outline] 기본 산출물 완성: ' + out.outline.selected.thesis)

out.compose = null
out.gate = null
if (WRITE_FULL_DRAFT) {
  out.compose = await compose(out.mined, out.outline.selected)
  out.gate = await gate(out.mined)
  log('[완료] 전문 작성 및 게이트 완료 → ' + OUT)
} else {
  log('[완료] 아웃라인에서 종료. 전문 작성은 writeFullDraft: true일 때만 실행합니다.')
}

return out
