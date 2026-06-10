export const meta = {
  name: 'blog-recompose',
  description: '기술블로그 재작곡 파이프라인: 저자의 선행 글 + 현재 초안을 채굴해, 1인칭 경험을 척추로 한 *완전히 새로운* 구성을 짠다. Mine(목소리·개념·알맹이·브랜드) → Outline(판정 패널) → Compose(새 작곡) → Gate(브랜드·정확성·구조).',
  whenToUse: '있는 초안을 다듬는 게 아니라, 선행 글들과 퍼스널 브랜드를 엮어 처음부터 새로 구성하고 싶을 때. args로 소스 3개·출력·브랜드 리드를 넘긴다.',
  phases: [
    { title: 'Mine' },
    { title: 'Outline' },
    { title: 'Compose' },
    { title: 'Gate' },
  ],
}

// ───────────────────────────────────────────────────────────────────────────
// 사용법 (args):
//   {
//     experienceSource: "<1인칭 경험 글 절대경로>",   // 척추 재료 (예: 60일 글)
//     conceptSource:    "<재사용 개념 글 절대경로>",   // 프레임 (예: 플랫폼팀 글)
//     substanceSource:  "<현재 초안 절대경로>",        // 검증된 알맹이 (예: v4)
//     output:           "<새 글을 쓸 절대경로>",        // 예: v5.md
//     brandLead:        "<브랜드 리드 한 줄>",
//     outlineCandidates: 3                            // 선택
//   }
//
// 설계 원칙(blog-review-polish 계승):
//  - JS 합성, 거대 JSON synthesis 에이전트 없음(hang 차단), raw 결과 항상 반환.
//  - 검증된 사실/인용은 보존(작곡이 새 수치·출처를 지어내면 Gate가 잡는다).
//  - 1인칭 경험=척추 / 리서치=보조 / 실행(PR 표·PR 두 줄)=클라이맥스.
//  - 과교정·목소리 평탄화 금지. AI-제네릭 신호는 Gate에서 신고.
//  - ⚠️ 출간 선행글은 참조(위키링크)만, 사건·장면 재서술 금지 / 소스에 없는 장면 창작 금지(자기 중복·날조 방지). Compose가 지키고 Gate가 선행글과 대조해 검출.
// ───────────────────────────────────────────────────────────────────────────

let A = args || {}
if (typeof A === 'string') { try { A = JSON.parse(A) } catch (e) { A = {} } }
const EXP = A.experienceSource
const CONCEPT = A.conceptSource
const SUBSTANCE = A.substanceSource
const OUT = A.output
const BRAND = A.brandLead || '실전 브리지형 — 현장에서 직접 부딪힌 플랫폼/백엔드 엔지니어가 개인 실험을 팀·플랫폼 원칙으로 일반화. hands-on 경험↔시스템 사고를 잇는 다리. 존댓말 1인칭, 정직한 메타("내가 X하려다 사실 Y였다"), 독자 직접 질문. 트렌드는 양념, 경험이 본체.'
const NUM_OUTLINES = A.outlineCandidates || 3
const AGENT = 'general-purpose'

if (!EXP || !CONCEPT || !SUBSTANCE || !OUT) {
  log('❌ args 필요: {experienceSource, conceptSource, substanceSource, output, brandLead}')
  return { error: 'missing required args', got: A }
}

// ── schemas ────────────────────────────────────────────────────────────────
const VOICE_SCHEMA = {
  type: 'object', additionalProperties: false,
  properties: {
    arc: { type: 'string', description: '글을 관통하는 1인칭 서사 호(예: AI를 조련하려다 팀 방식이 훈련됨)' },
    signatures: { type: 'array', items: { type: 'string' }, description: '저자의 문체 시그니처' },
    authenticPhrases: { type: 'array', items: { type: 'string' }, description: '그대로 살릴 만한 저자의 실제 문장(인용)' },
    keyFacts: { type: 'array', items: { type: 'string' }, description: '구체 사실(프로젝트명·날짜·무엇을 했는지). 지어내지 말 것.' },
    voiceRules: { type: 'string', description: '재작곡 시 지킬 목소리 규칙' },
  },
  required: ['arc', 'signatures', 'authenticPhrases', 'keyFacts', 'voiceRules'],
}
const CONCEPT_SCHEMA = {
  type: 'object', additionalProperties: false,
  properties: {
    frames: {
      type: 'array',
      items: {
        type: 'object', additionalProperties: false,
        properties: {
          name: { type: 'string' }, def: { type: 'string', description: '한 줄 정의' },
          connect: { type: 'string', description: '이번 주제(개인→팀 회수)와 어떻게 연결되나' },
        },
        required: ['name', 'def', 'connect'],
      },
    },
    reusableLines: { type: 'array', items: { type: 'string' }, description: '그대로/살짝 변형해 쓸 문장' },
  },
  required: ['frames', 'reusableLines'],
}
const SUBSTANCE_SCHEMA = {
  type: 'object', additionalProperties: false,
  properties: {
    keep: {
      type: 'array',
      items: {
        type: 'object', additionalProperties: false,
        properties: {
          claim: { type: 'string' }, source: { type: 'string' }, why: { type: 'string', description: '왜 살려야 하나' },
        },
        required: ['claim', 'source', 'why'],
      },
      description: '검증된 사실/인용 — 정확성 보존 대상',
    },
    strongMaterial: { type: 'array', items: { type: 'string' }, description: '가장 기술블로그다운 강한 재료(예: PR 맥락 표)' },
    drop: { type: 'array', items: { type: 'string' }, description: '재작곡에서 버리거나 강등할 것(현학·상품화)' },
  },
  required: ['keep', 'strongMaterial', 'drop'],
}
const BRAND_SCHEMA = {
  type: 'object', additionalProperties: false,
  properties: {
    positioning: { type: 'string' }, voice: { type: 'string' },
    themes: { type: 'array', items: { type: 'string' } },
    signatureMoves: { type: 'array', items: { type: 'string' } },
    antiPatterns: { type: 'array', items: { type: 'string' }, description: 'AI-제네릭으로 빠지는 신호(피할 것)' },
  },
  required: ['positioning', 'voice', 'themes', 'signatureMoves', 'antiPatterns'],
}
const OUTLINE_SCHEMA = {
  type: 'object', additionalProperties: false,
  properties: {
    title: { type: 'string' },
    spine: { type: 'string', description: '한 줄 척추(1인칭 호)' },
    sections: {
      type: 'array',
      items: {
        type: 'object', additionalProperties: false,
        properties: {
          heading: { type: 'string' }, beat: { type: 'string', description: '이 섹션이 하는 일' },
          materials: { type: 'array', items: { type: 'string' }, description: '쓸 재료(1인칭/개념/리서치)' },
          show: { type: 'string', description: '이 섹션의 현장 장면(show 요소)' },
        },
        required: ['heading', 'beat', 'materials', 'show'],
      },
    },
    climax: { type: 'string', description: '실행 클라이맥스(예: PR 맥락 표/PR 두 줄)' },
  },
  required: ['title', 'spine', 'sections', 'climax'],
}
const JUDGE_SCHEMA = {
  type: 'object', additionalProperties: false,
  properties: {
    scores: {
      type: 'object', additionalProperties: false,
      properties: {
        brandFit: { type: 'number' }, showNotExplain: { type: 'number' },
        spineStrength: { type: 'number' }, freshness: { type: 'number' },
      },
      required: ['brandFit', 'showNotExplain', 'spineStrength', 'freshness'],
    },
    total: { type: 'number' }, verdict: { type: 'string' },
    bestIdeasToGraft: { type: 'array', items: { type: 'string' } },
  },
  required: ['scores', 'total', 'verdict', 'bestIdeasToGraft'],
}
const COMPOSE_SCHEMA = {
  type: 'object', additionalProperties: false,
  properties: {
    wordCountApprox: { type: 'number' },
    sectionsWritten: { type: 'array', items: { type: 'string' } },
    voiceNote: { type: 'string', description: '어떻게 1인칭 척추를 유지했는지' },
    factsPreserved: { type: 'array', items: { type: 'string' }, description: '보존한 검증 사실/인용' },
  },
  required: ['wordCountApprox', 'sectionsWritten', 'voiceNote', 'factsPreserved'],
}
const GATE_SCHEMA = {
  type: 'object', additionalProperties: false,
  properties: {
    brandMatch: { type: 'string', enum: ['strong', 'ok', 'weak'] },
    aiTellSignals: { type: 'array', items: { type: 'string' } },
    showVsExplain: { type: 'string', enum: ['show-led', 'mixed', 'explain-led'] },
    accuracyFlags: { type: 'array', items: { type: 'string' }, description: '작곡이 새로 만든 미검증/과장 주장' },
    structureOk: { type: 'boolean' },
    topFixes: { type: 'array', items: { type: 'string' } },
  },
  required: ['brandMatch', 'aiTellSignals', 'showVsExplain', 'accuracyFlags', 'structureOk', 'topFixes'],
}

// ── phase: mine ──────────────────────────────────────────────────────────────
async function mine() {
  log('[Mine] 3개 소스 병렬 채굴')
  const [voice, concept, substance] = await parallel([
    () => agent([
      '대상 파일: ' + EXP + ' (저자의 1인칭 경험담 — ⚠️ 이미 출간된 글)', 'Read 도구로 전문 읽기.', '',
      '이 글에서 *재작곡의 1인칭 척추*가 될 재료를 뽑아라. 단, 이 글은 이미 출간됐으므로 새 글은 이걸 *재서술*하면 안 되고 *참조(위키링크)*만 한다. 그래서 사건·연대기보다 *재사용 가능한 깨달음*을 뽑는다:',
      '- arc: 글을 관통하는 1인칭 서사 호(예: AI를 조련하려다 팀 방식이 훈련됨)',
      '- authenticPhrases: 그대로 살릴 만한 저자의 *깨달음·주장* 문장(원문 인용). 사건 묘사·연대기 문장은 제외 — 그건 재서술 대상이라 새 글에 옮기면 자기 중복이 된다.',
      '- keyFacts: 구체 사실(프로젝트명·날짜·무엇을 했는지). 원문에 있는 것만. 이건 *정확성 참조용*일 뿐, 본문에 그대로 옮겨 적을 소재가 아니다.',
      '- signatures/voiceRules: 문체 특징과 재작곡 시 지킬 규칙. voiceRules에 "출간 선행글은 링크로만 참조, 사건·장면 재서술 금지, 소스에 없는 장면 창작 금지"를 반드시 포함하라.',
    ].join('\n'), { label: 'voice-miner', phase: 'Mine', schema: VOICE_SCHEMA, agentType: AGENT }),
    () => agent([
      '대상 파일: ' + CONCEPT + ' (저자의 개념/프레임 글)', 'Read 도구로 전문 읽기.', '',
      '이번 글에 *얇게* 끌어올 재사용 프레임을 뽑아라(예: Golden Path, Force Multiplier/레버리지). 각 프레임의 한 줄 정의 + 이번 주제(개인 생산성→팀 회수)와 어떻게 연결되는지. 그대로/살짝 변형해 쓸 문장도. 과하게 많이 넣지 말 것 — 핵심 2~3개.',
    ].join('\n'), { label: 'concept-miner', phase: 'Mine', schema: CONCEPT_SCHEMA, agentType: AGENT }),
    () => agent([
      '대상 파일: ' + SUBSTANCE + ' (현재 초안)', 'Read 도구로 전문 읽기.', '',
      '재작곡에서 *살릴 검증된 알맹이*와 *버릴 것*을 분리하라:',
      '- keep: 검증된 사실/인용(예: Faros 154%/91%, comprehension debt, 인식/이해 부채 분해, 회수 개념)과 출처. 정확성 보존 대상.',
      '- strongMaterial: 가장 기술블로그다운 강한 재료(예: PR 맥락 표, PR 템플릿 두 줄).',
      '- drop: 현학적이거나 상품화된 부분(과한 학술 나열 등).',
    ].join('\n'), { label: 'substance-miner', phase: 'Mine', schema: SUBSTANCE_SCHEMA, agentType: AGENT }),
  ])

  log('[Mine] 브랜드 프로필 종합')
  const brand = await agent([
    '너는 퍼스널 브랜드 전략가다. 아래 세 채굴 결과와 브랜드 리드를 종합해 이 저자의 브랜드 프로필을 확정하라.',
    '브랜드 리드: ' + BRAND, '',
    '## 경험(voice)', JSON.stringify(voice), '',
    '## 개념(concept)', JSON.stringify(concept), '',
    '## 알맹이(substance)', JSON.stringify(substance), '',
    'positioning/voice/themes/signatureMoves/antiPatterns(AI-제네릭 신호) 반환.',
  ].join('\n'), { label: 'brand-profiler', phase: 'Mine', schema: BRAND_SCHEMA, agentType: AGENT })

  return { voice, concept, substance, brand }
}

// ── phase: outline (판정 패널) ───────────────────────────────────────────────
async function outline(mined) {
  log('[Outline] 후보 ' + NUM_OUTLINES + '개 생성')
  const ctx = [
    '브랜드: ' + JSON.stringify(mined.brand),
    '1인칭 척추 재료: ' + JSON.stringify(mined.voice),
    '재사용 프레임: ' + JSON.stringify(mined.concept),
    '살릴 알맹이: ' + JSON.stringify(mined.substance && mined.substance.keep),
    '강한 재료: ' + JSON.stringify(mined.substance && mined.substance.strongMaterial),
  ].join('\n')
  const angles = [
    '입장 변경(confession) 중심 — "조련하려다 깨달음"을 전면에 세운다',
    '문제→실험→일반화 — 개인 실험을 사례로 깔고 팀 원칙으로 끌어올린다',
    'Golden Path 브리지 — 개인 워크플로에서 팀/플랫폼 경계로 잇는다',
    '독자 동일시 — "당신 팀의 PR엔 뭐가 남나"를 처음부터 끝까지 추적한다',
  ]
  const candidates = (await parallel(angles.slice(0, NUM_OUTLINES).map((ang, i) => () =>
    agent([
      '너는 기술블로그 편집장이다. 아래 재료로 *완전히 새로운* 글 아웃라인을 설계하라.',
      '이 후보의 각도: ' + ang, '', ctx, '',
      '원칙: 1인칭 경험=척추, 리서치=보조, 실행(PR 표/PR 두 줄)=클라이맥스. 개념 설명이 아니라 현장 장면으로. 제목·척추 한 줄·섹션별(heading/beat/materials/show)·클라이맥스를 반환.',
    ].join('\n'), { label: 'outline:c' + (i + 1), phase: 'Outline', schema: OUTLINE_SCHEMA, agentType: AGENT })
  ))).filter(Boolean)
  if (!candidates.length) return null

  log('[Outline] 판정 → 합성')
  const judged = (await parallel(candidates.map((c, i) => () =>
    agent([
      '너는 까다로운 기술블로그 심사위원이다. 이 아웃라인을 brandFit/showNotExplain/spineStrength/freshness(각 0~10)로 채점하고 총점·평가·다른 후보에 이식할 좋은 아이디어를 반환.',
      '브랜드: ' + (mined.brand && mined.brand.positioning), '', '아웃라인: ' + JSON.stringify(c),
    ].join('\n'), { label: 'judge:c' + (i + 1), phase: 'Outline', schema: JUDGE_SCHEMA, agentType: AGENT }).then(j => (j ? { c, j } : null))
  ))).filter(Boolean)
  if (!judged.length) return candidates[0]

  const scored = judged.sort((a, b) => (b.j.total || 0) - (a.j.total || 0))
  const best = scored[0]
  const graft = scored.flatMap(x => x.j.bestIdeasToGraft || [])

  const finalOutline = await agent([
    '너는 편집장이다. 아래 *베스트 아웃라인*을 기준으로 다른 후보들의 좋은 아이디어를 이식해 최종 아웃라인을 확정하라.',
    '베스트: ' + JSON.stringify(best.c), '',
    '이식 후보 아이디어: ' + graft.join(' / '), '',
    '브랜드: ' + JSON.stringify(mined.brand), '',
    '최종 아웃라인을 같은 스키마로 반환. 1인칭 척추·show 우선·실행 클라이맥스 유지.',
  ].join('\n'), { label: 'outline-final', phase: 'Outline', schema: OUTLINE_SCHEMA, agentType: AGENT })
  return finalOutline || best.c
}

// ── phase: compose (새 작곡) ─────────────────────────────────────────────────
async function compose(mined, theOutline) {
  log('[Compose] v5 작곡 → ' + OUT)
  return agent([
    '너는 이 저자 본인의 목소리로 쓰는 한국어 기술블로그 작가다. 아래 아웃라인과 재료로 *완전히 새로운* 글을 써서 ' + OUT + ' 에 Write 도구로 저장하라.', '',
    '## 절대 규칙',
    '- 1인칭 경험이 척추다. 개념 설명으로 열지 말고, 저자가 겪은 일(예: 신규 프로젝트에서 AI 워크플로를 만들다가 "조련하려다 팀 방식이 훈련됨"을 깨달음)에서 출발하라.',
    '- ⚠️ 재서술 금지(가장 중요): experienceSource·conceptSource는 *이미 출간된 글*이다. 그 글의 사건·장면·연대기·커맨드명·고유 문장을 본문에 옮겨 적지 마라. 선행 글 참조는 위키링크 + 거기서 얻은 *깨달음 한 줄*로만 하고, 구체 사건은 "자세한 건 [[그 글]]에 적었습니다" 식으로 링크해 보낸다. 독자가 두 글을 다 읽었을 때 겹친다고 느끼면 실패다.',
    '- ⚠️ 창작 금지: 소스(keyFacts·원문)에 없는 장면·일화·인물·수치를 지어내지 마라(가상의 온보딩 장면, 안 일어난 대화 등). 실재가 확인된 것만 쓰고, 모르면 비운다.',
    '- 검증된 사실/인용은 그대로 보존(예: Faros 154%/91%, comprehension debt). 새 수치·새 출처를 절대 지어내지 마라.',
    '- 리서치/학술 개념은 척추를 떠받치는 보조로만. 개념 나열 금지. 한 글에 학술 개념 2개 이하만 본문 노출.',
    '- 실행(PR 맥락 표, PR 템플릿 두 줄)을 클라이맥스로 배치.',
    '- 존댓말 1인칭, 정직한 메타, 독자에게 직접 질문. AI-제네릭("X가 아니라 Y" 남발, 번역투, 과한 헤지, 현학적 영어 병기) 금지.',
    '- 프론트매터는 현재 초안과 같은 형식(title/created/tags/status: draft/author/summary/related)을 유지. 참고문헌 섹션은 현재 초안의 *검증된* 출처를 재사용.',
    '- 원본 세 글(' + EXP + ' / ' + CONCEPT + ' / ' + SUBSTANCE + ')을 Read로 다시 열어 정확한 1인칭 문장·수치·출처를 확인한 뒤 써라.', '',
    '## 최종 아웃라인', JSON.stringify(theOutline), '',
    '## 1인칭 재료(그대로 살릴 문장 포함)', JSON.stringify(mined.voice), '',
    '## 재사용 프레임(얇게)', JSON.stringify(mined.concept), '',
    '## 보존할 검증 알맹이', JSON.stringify(mined.substance && mined.substance.keep), '',
    '## 강한 재료(클라이맥스로)', JSON.stringify(mined.substance && mined.substance.strongMaterial), '',
    '다 쓰면 wordCountApprox/sectionsWritten/voiceNote/factsPreserved 반환.',
  ].join('\n'), { label: 'composer', phase: 'Compose', schema: COMPOSE_SCHEMA, agentType: AGENT })
}

// ── phase: gate ──────────────────────────────────────────────────────────────
async function gate() {
  log('[Gate] 브랜드 · 정확성 · 구조 점검')
  const [brand, structure] = await parallel([
    () => agent([
      '너는 이 저자의 글을 잘 아는 까다로운 독자다. ' + OUT + ' 를 Read로 끝까지 읽어라.',
      '브랜드 리드: ' + BRAND, '',
      '판정: 이게 "이 저자가 직접 쓴 글"처럼 읽히나(brandMatch: strong/ok/weak), AI-제네릭 신호(aiTellSignals)는 없나, 개념 설명이 아니라 현장을 보여주나(showVsExplain: show-led/mixed/explain-led). topFixes에 우선 수정 3개. accuracyFlags/structureOk는 임시값.',
    ].join('\n'), { label: 'brand-gate', phase: 'Gate', schema: GATE_SCHEMA, agentType: AGENT }),
    () => agent([
      '너는 적대적 팩트·중복·구조 점검자다. ' + OUT + ' 를 Read하고, 출간된 선행 글 ' + EXP + ' 와 ' + CONCEPT + ' 도 Read해 대조하라.',
      '아래를 점검해 전부 accuracyFlags에 신고하라:',
      '1. 자기 중복(가장 중요): 본문이 선행 글의 사건·장면·연대기·고유 문장을 재서술했는가? 겹치는 구절을 인용해 신고하라. 출간글은 참조+위키링크만 허용이고 재서술은 금지다.',
      '2. 창작: 소스에 없는 장면·일화·수치를 지어냈는가? 해당 구절을 신고하라.',
      '3. 새 미검증/과장 주장 — 특히 수치·연구 귀속.',
      '그리고 Bash로 프론트매터(--- 쌍)/위키링크 [[ ]] 짝/이미지 임베드/마크다운 표/참고문헌 링크 구조 무결성(structureOk)을 확인하라. accuracyFlags/structureOk 채우고 나머지는 임시값.',
    ].join('\n'), { label: 'accuracy-overlap-structure-gate', phase: 'Gate', schema: GATE_SCHEMA, agentType: AGENT }),
  ])
  return {
    brandMatch: brand ? brand.brandMatch : 'unknown',
    aiTellSignals: brand ? brand.aiTellSignals : [],
    showVsExplain: brand ? brand.showVsExplain : 'unknown',
    accuracyFlags: structure ? structure.accuracyFlags : [],
    structureOk: structure ? structure.structureOk : null,
    topFixes: brand ? brand.topFixes : [],
  }
}

// ── orchestrate ──────────────────────────────────────────────────────────────
const out = { output: OUT }
out.mined = await mine()
out.outline = await outline(out.mined)
if (!out.outline) { log('아웃라인 실패 — 정지'); return out }
log('[Outline] 확정: ' + (out.outline.title || '(제목 없음)') + ' / 척추: ' + (out.outline.spine || ''))
out.compose = await compose(out.mined, out.outline)
out.gate = await gate()
log('완료. v5 → ' + OUT + ' / 브랜드일치=' + (out.gate ? out.gate.brandMatch : '?') + ' / show=' + (out.gate ? out.gate.showVsExplain : '?'))
return out
