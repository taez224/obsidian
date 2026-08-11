#!/usr/bin/env node
// blog-structure-scan — developmental(구조) 층의 결정론적 스캐너.
//
// blog-slop-lint.mjs가 문장·표기(line/copy 층)를 보는 동안 이 스크립트는 글의 뼈대를 본다.
// 판단은 하지 않는다. 사람이 역방향 아웃라인을 채울 재료와, 눈으로는 잘 안 보이는
// 교차 절 반복만 기계적으로 뽑아준다.
//
//   node .claude/workflows/blog-structure-scan.mjs "<파일>" [--min-lcs 15] [--json]
//
// 판정 기준과 이 출력을 읽는 법은 references/structural-review.md 가 정본이다.

import { readFileSync } from "node:fs";
import { basename } from "node:path";

const DEFAULTS = {
  minLcs: 15, // 교차 절 반복으로 볼 최소 공통 문자열 길이
  longPara: 350, // 문단 밀도 경고 기준 (국내 기술 블로그 벤치마크)
  // 본문이 아닌 꼬리 절. 여기의 출처·도구 이름은 본문과 겹치는 게 정상이다.
  tailPattern: /^(?:참고\s*자료|참고자료|인용\s*출처|출처|부록|연관된?\s*노트|연결된?\s*노트|관련\s*링크)(?:\s*(?:[:—–-]|및|·|\/)\s*.*)?$/,
  // 산문 반복은 조사·어미를 달고 다니고 고유명사 반복은 그렇지 않다.
  // `claudecodeguide`(한글 0%)는 걸러내고 `프론트엔드와백엔드의sse컨벤션은`(한글 다수)은 남긴다.
  minHangulRatio: 0.6,
};

function parseArgs(argv) {
  const args = { file: null, minLcs: DEFAULTS.minLcs, json: false };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === "--json") args.json = true;
    else if (a === "--min-lcs") args.minLcs = Number(argv[++i]);
    else if (!args.file) args.file = a;
  }
  return args;
}

// ── 파싱 ──────────────────────────────────────────────────────────────────
// 본문을 절 → 문단으로 쪼갠다. frontmatter, 코드블록, 꼬리 절(참고 자료 등)은 제외.

function parse(raw) {
  const lines = raw.split("\n");
  let start = 0;
  if (lines[0]?.trim() === "---") {
    const end = lines.indexOf("---", 1);
    if (end > 0) start = end + 1;
  }

  const sections = [];
  let articleTitle = "";
  let cur = { title: "(도입)", line: start + 1, paras: [] };
  let inFence = false;
  let pending = null;

  const flush = () => {
    if (!pending?.text) return;
    cur.paras.push(pending);
    pending = null;
  };

  const append = (kind, text, lineNo, forceNew = false) => {
    if (!text) return;
    if (!forceNew && pending?.kind === kind) {
      pending.text += " " + text;
      return;
    }
    flush();
    pending = { line: lineNo, kind, text };
  };

  for (let i = start; i < lines.length; i++) {
    const line = lines[i];
    const lineNo = i + 1;

    if (/^\s*```/.test(line)) {
      flush();
      inFence = !inFence;
      continue;
    }
    if (inFence) continue;

    if (/^##\s+/.test(line)) {
      flush();
      sections.push(cur);
      cur = { title: line.replace(/^##\s+/, "").trim(), line: lineNo, paras: [] };
      continue;
    }
    if (/^#\s+/.test(line)) {
      flush();
      if (!articleTitle) articleTitle = line.replace(/^#\s+/, "").trim();
      continue;
    }
    if (/^#{3,6}\s+/.test(line)) {
      flush();
      continue;
    }

    const t = line.trim();
    if (!t) {
      flush();
      continue;
    }
    if (/^!\[/.test(t) || /^!\[\[/.test(t)) { flush(); continue; } // 이미지
    if (/^\*[^*]+\*$/.test(t)) { flush(); continue; } // 캡션
    if (/^\|/.test(t)) { flush(); continue; } // 표

    const kind = /^>/.test(t) ? "quote" : /^[-*+]\s/.test(t) ? "list" : "prose";
    const text = t.replace(/^>\s?/, "").replace(/^[-*+]\s/, "");
    if (!text) {
      if (/^>\s*$/.test(t)) flush();
      continue;
    }

    if (kind === "list") append(kind, text, lineNo, true);
    else if (kind === "prose" && pending?.kind === "list" && /^\s{2,}/.test(line)) {
      pending.text += " " + text;
    } else append(kind, text, lineNo);
  }
  flush();
  sections.push(cur);

  return {
    articleTitle,
    sections: sections.filter(
      (s) => s.paras.length && !DEFAULTS.tailPattern.test(s.title)
    ),
  };
}

const hangulRatio = (s) =>
  s.length ? (s.match(/[가-힣]/g) || []).length / s.length : 0;

// 링크·강조·코드 표기를 걷어낸 순수 글자수. slop-lint와 같은 세는 방식.
const strip = (s) =>
  s
    .replace(/\[([^\]]*)\]\([^)]*\)/g, "$1")
    .replace(/\[\[([^\]|]*\|)?([^\]]*)\]\]/g, "$2")
    .replace(/[`*_~]/g, "");

const chars = (s) => strip(s).replace(/\s/g, "").length;

// 첫 문장. 역방향 아웃라인을 채울 때 요지의 단서로만 쓴다.
function firstSentence(text, max = 46) {
  const s = strip(text).trim();
  const m = s.match(/^[^.!?]*[.!?]/);
  const out = (m ? m[0] : s).trim();
  return out.length > max ? out.slice(0, max) + "…" : out;
}

// ── 교차 절 반복 ──────────────────────────────────────────────────────────
// 서로 다른 절에 있는 문단 쌍의 최장 공통 부분문자열을 찾는다.
// 한국어는 공백 토큰화가 신통치 않아 문자 단위로 본다.

function normalize(s) {
  return strip(s)
    .replace(/[^\p{Letter}\p{Number}]/gu, "")
    .toLowerCase();
}

function longestCommon(a, b) {
  if (!a.length || !b.length) return "";
  let prev = new Uint16Array(b.length + 1);
  let best = 0;
  let end = 0;
  for (let i = 1; i <= a.length; i++) {
    const cur = new Uint16Array(b.length + 1);
    const ca = a[i - 1];
    for (let j = 1; j <= b.length; j++) {
      if (ca === b[j - 1]) {
        cur[j] = prev[j - 1] + 1;
        if (cur[j] > best) {
          best = cur[j];
          end = i;
        }
      }
    }
    prev = cur;
  }
  return a.slice(end - best, end);
}

function findRepeats(sections, minLcs) {
  const items = [];
  sections.forEach((s, si) =>
    s.paras.forEach((p) => items.push({ ...p, si, section: s.title, norm: normalize(p.text) }))
  );

  const hits = [];
  for (let i = 0; i < items.length; i++) {
    for (let j = i + 1; j < items.length; j++) {
      if (items[i].si === items[j].si) continue; // 같은 절 안은 보지 않는다
      const lcs = longestCommon(items[i].norm, items[j].norm);
      if (lcs.length >= minLcs && hangulRatio(lcs) >= DEFAULTS.minHangulRatio) {
        hits.push({ a: items[i], b: items[j], lcs, len: lcs.length });
      }
    }
  }
  return hits.sort((x, y) => y.len - x.len);
}

// 제목이 절 제목에 재사용되거나, 절 제목이 첫 문장에서 거의 그대로 반복되는 후보.
// 의미 중복 판정이 아니라 편집자가 확인할 위치만 제공한다.
function findHeadingEchoes(articleTitle, sections) {
  const hits = [];
  const articleNorm = normalize(articleTitle);

  for (const section of sections) {
    const sectionNorm = normalize(section.title);
    if (articleNorm && articleNorm === sectionNorm) {
      hits.push({ type: "article-section", line: section.line, title: section.title, ratio: 1 });
    }

    const first = section.paras.find((p) => p.kind === "prose");
    if (!first || !sectionNorm) continue;
    const firstNorm = normalize(first.text);
    const lcs = longestCommon(sectionNorm, firstNorm);
    const ratio = lcs.length / Math.min(sectionNorm.length, firstNorm.length);
    if (lcs.length >= 10 && ratio >= 0.65 && hangulRatio(lcs) >= DEFAULTS.minHangulRatio) {
      hits.push({
        type: "section-opening",
        line: first.line,
        title: section.title,
        lcs,
        ratio: Number(ratio.toFixed(2)),
      });
    }
  }

  return hits;
}

// ── 출력 ──────────────────────────────────────────────────────────────────

function main() {
  const args = parseArgs(process.argv.slice(2));
  if (!args.file) {
    console.error('사용법: node blog-structure-scan.mjs "<파일>" [--min-lcs 15] [--json]');
    process.exit(2);
  }

  if (!Number.isFinite(args.minLcs) || args.minLcs < 4) {
    console.error("--min-lcs는 4 이상의 숫자여야 합니다.");
    process.exit(2);
  }

  const { articleTitle, sections } = parse(readFileSync(args.file, "utf8"));
  const total = sections.reduce(
    (n, s) => n + s.paras.reduce((m, p) => m + chars(p.text), 0),
    0
  );
  const repeats = findRepeats(sections, args.minLcs);
  const headingEchoes = findHeadingEchoes(articleTitle, sections);
  const longParas = sections.flatMap((s) =>
    s.paras.filter((p) => p.kind === "prose" && chars(p.text) >= DEFAULTS.longPara)
      .map((p) => ({ ...p, section: s.title }))
  );

  if (args.json) {
    console.log(
      JSON.stringify(
        {
          file: basename(args.file),
          articleTitle,
          total,
          sections: sections.map((s) => ({
            title: s.title,
            line: s.line,
            chars: s.paras.reduce((m, p) => m + chars(p.text), 0),
            paras: s.paras.length,
          })),
          repeats: repeats.map((r) => ({
            lcs: r.lcs,
            len: r.len,
            a: { line: r.a.line, section: r.a.section },
            b: { line: r.b.line, section: r.b.section },
          })),
          headingEchoes,
          longParas: longParas.map((p) => ({ line: p.line, chars: chars(p.text) })),
        },
        null,
        2
      )
    );
    return;
  }

  console.log(`structure-scan  (${basename(args.file)})`);
  console.log(`  본문 ${total}자 · ${sections.length}개 절\n`);

  console.log("절 비중");
  for (const s of sections) {
    const c = s.paras.reduce((m, p) => m + chars(p.text), 0);
    const pct = total ? Math.round((c / total) * 100) : 0;
    const bar = "█".repeat(Math.max(1, Math.round(pct / 2)));
    console.log(
      `  ${String(c).padStart(5)}자 ${String(pct).padStart(3)}%  ${bar.padEnd(20)} ${s.title} (문단 ${s.paras.length})`
    );
  }

  console.log("\n역방향 아웃라인 뼈대  — 요지 한 줄은 사람이 채운다");
  for (const s of sections) {
    console.log(`  ## ${s.title}`);
    s.paras.forEach((p, i) => {
      const mark = p.kind === "quote" ? "❯" : p.kind === "list" ? "·" : "①②③④⑤⑥⑦⑧⑨⑩"[i] || "○";
      console.log(`     ${mark} ${String(p.line).padStart(3)}행  ${firstSentence(p.text)}`);
    });
  }

  console.log("\n교차 절 반복  — 서로 다른 절에서 겹치는 표현");
  if (!repeats.length) {
    console.log(`  없음 (${args.minLcs}자 이상 기준)`);
  } else {
    for (const r of repeats.slice(0, 12)) {
      console.log(`  ⚠ ${r.len}자  "${r.lcs}"`);
      console.log(`      ${String(r.a.line).padStart(3)}행 ${r.a.section}`);
      console.log(`      ${String(r.b.line).padStart(3)}행 ${r.b.section}`);
    }
    if (repeats.length > 12) console.log(`  … 외 ${repeats.length - 12}건`);
  }

  console.log("\n제목·도입 메아리  — 제목을 첫 문장이 그대로 되풀이하는 후보");
  if (!headingEchoes.length) {
    console.log("  없음");
  } else {
    for (const h of headingEchoes) {
      if (h.type === "article-section") {
        console.log(`  ⚠ ${h.line}행  글 제목과 같은 절 제목: "${h.title}"`);
      } else {
        console.log(`  ⚠ ${h.line}행  절 제목이 첫 산문 문단에 ${Math.round(h.ratio * 100)}% 겹침: "${h.title}"`);
      }
    }
  }

  console.log("\n문단 밀도");
  if (!longParas.length) {
    console.log(`  ${DEFAULTS.longPara}자 초과 산문 문단 없음`);
  } else {
    for (const p of longParas) console.log(`  ⚠ ${p.line}행  ${chars(p.text)}자  (${p.section})`);
  }

  console.log("\n  판정하지 않는다. 반복이 의도된 회수인지, 절 비중이 역할에 맞는지는");
  console.log("  references/structural-review.md 를 보고 사람이 정한다.");
}

main();
