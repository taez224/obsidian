# vault-lint Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** vault 헬스를 결정적으로 스캔(Python)하고 판단 작업(연결 제안 등)은 승인 루프로 처리하는 vault-lint 스킬 구축.

**Architecture:** 기계 검사는 stdlib 전용 `lint_scan.py`가 JSON으로 출력, 판단·승인·적용은 SKILL.md 절차가 Claude+qmd로 수행. 스펙: `_workspace/2026-06-12-001/vault-lint-design.md` (단, SKILL.md는 스펙 삭제 후에도 자립해야 하므로 스펙을 참조하지 않는다).

**Tech Stack:** Python 3 stdlib (json/os/re/sys/unicodedata/subprocess/tempfile), Claude Code skill (SKILL.md), qmd MCP.

**File Structure:**

```
.agents/skills/vault-lint/
  SKILL.md                       # 스킬 본문 (자립적 — 스펙 참조 금지)
  scripts/lint_scan.py           # 스캐너 (읽기 전용)
  scripts/test_lint_scan.py      # 픽스처 기반 테스트 (pytest 불필요, python3 직접 실행)
.claude/skills/vault-lint        # → ../../.agents/skills/vault-lint 심링크
```

---

### Task 1: 테스트 픽스처 작성 (실패 확인까지)

**Files:**
- Create: `.agents/skills/vault-lint/scripts/test_lint_scan.py`

- [ ] **Step 1: 테스트 파일 작성**

핵심 검증: NFC/NFD 교차 해석, alias 해석, Archive로 향하는 링크 생존, 첨부 임베드 비오탐, 고립 탐지(slipbox 플래그), 죽은 링크, frontmatter 위반(공통/폴더별/DevLog 예외).

```python
#!/usr/bin/env python3
"""lint_scan.py 픽스처 테스트. 실행: python3 test_lint_scan.py"""
import json
import os
import subprocess
import sys
import tempfile
import unicodedata

SCRIPT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "lint_scan.py")


def write(root, rel, text):
    path = os.path.join(root, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)


def build_fixture(root):
    fm = "---\ncreated: 2026-06-12\ntags:\n  - AI\n"
    slip_fm = fm + "type: permanent\nstatus: seedling\n---\n"
    # 정상 Slipbox 노트: NFC 링크 3종 — 일반 / NFD 파일 / Archive 파일 + 죽은 링크 + 첨부 임베드
    write(root, "01_Slipbox/연결된 노트.md",
          slip_fm + "[[대상 노트]] [[단상]] [[옛노트]] [[없는노트]] ![[그림.png]]\n"
          + "```\n[[코드블록 링크는 무시]]\n```\n")
    # alias로만 링크되는 노트
    write(root, "01_Slipbox/별명 노트.md",
          fm + "type: permanent\nstatus: seedling\naliases:\n  - 별명\n---\n[[연결된 노트]]\n")
    write(root, "30_Resources/대상 노트.md", fm + "---\n[[별명]]\n")
    # NFD 파일명 (디스크) — NFC 링크 [[단상]]이 해석되어야 함
    write(root, "00_Inbox/" + unicodedata.normalize("NFD", "단상") + ".md", fm + "---\n본문\n")
    # Archive: 해석 집합에는 포함, 검사 대상에선 제외
    write(root, "40_Archive/옛노트.md", fm + "---\n[[고립 아님]]\n")
    # Archive에서만 백링크를 받는 노트 → 고립 아님
    write(root, "30_Resources/고립 아님.md", fm + "---\n본문\n")
    # 진짜 고립 (Slipbox) → slipbox 플래그
    write(root, "01_Slipbox/고립 노트.md", slip_fm + "본문뿐\n")
    # frontmatter 위반: created 누락 + 태그에 # + Slipbox 필수(type/status) 누락
    write(root, "01_Slipbox/나쁜 노트.md", "---\ntags:\n  - '#ai'\n---\n[[대상 노트]]\n")
    # DevLog: created 없이 date만 → 위반 아님
    write(root, "30_Resources/Development/DevLog/2026-06-12.md",
          "---\ndate: 2026-06-12\ntags:\n  - 개발/DevLog\n---\n[[대상 노트]]\n")
    # 첨부파일 실물
    write(root, "_attachments/그림.png", "png-bytes")
    # 제외 대상: _ 파일, _workspace
    write(root, "01_Slipbox/_index.md", "no frontmatter but excluded\n")
    write(root, "_workspace/tmp.md", "excluded\n")


def main():
    with tempfile.TemporaryDirectory() as root:
        build_fixture(root)
        out = subprocess.run([sys.executable, SCRIPT, root], capture_output=True, text=True)
        assert out.returncode == 0, out.stderr
        r = json.loads(out.stdout)

        orphan_paths = {o["path"] for o in r["orphans"]}
        assert "01_Slipbox/고립 노트.md" in orphan_paths, orphan_paths
        assert all(o["slipbox"] for o in r["orphans"] if o["path"].startswith("01_Slipbox/"))
        # NFD 파일·alias·Archive 대상·백링크만 있는 노트는 고립 아님
        for p in ("00_Inbox/단상.md", "01_Slipbox/별명 노트.md", "30_Resources/고립 아님.md"):
            assert unicodedata.normalize("NFC", p) not in {unicodedata.normalize("NFC", q) for q in orphan_paths}, p

        dead_targets = {d["target"] for d in r["dead_links"]}
        assert dead_targets == {"없는노트"}, dead_targets  # NFD·alias·Archive·png는 오탐 금지, 코드블록 무시

        issues = {i["path"]: i["issues"] for i in r["frontmatter_issues"]}
        bad = issues.get("01_Slipbox/나쁜 노트.md", [])
        assert any("created" in s for s in bad), bad
        assert any("#" in s for s in bad), bad
        assert any("type" in s for s in bad), bad
        assert "30_Resources/Development/DevLog/2026-06-12.md" not in issues, issues
        assert not any("_index" in p or "_workspace" in p for p in
                       [*orphan_paths, *issues]), "제외 규칙 위반"

        assert r["stats"]["notes_scanned"] >= 7
        print("OK — all assertions passed")


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: 실패 확인**

Run: `python3 .agents/skills/vault-lint/scripts/test_lint_scan.py`
Expected: FAIL — `lint_scan.py` 부재로 subprocess 실패 (AssertionError 또는 FileNotFoundError)

---

### Task 2: lint_scan.py 구현

**Files:**
- Create: `.agents/skills/vault-lint/scripts/lint_scan.py`

- [ ] **Step 1: 스캐너 전체 구현**

```python
#!/usr/bin/env python3
"""vault-lint 기계 검사 스캐너 — 읽기 전용, vault 파일을 절대 수정하지 않는다.

사용: python3 lint_scan.py [vault_root]   (기본: 현재 디렉토리)
출력: JSON {stats, orphans, dead_links, frontmatter_issues}

스키마 출처: 99_Templates/_property-schema.md — 스키마 변경 시 아래 설정 블록만 갱신.
"""
import json
import os
import re
import sys
import unicodedata

# ── 설정 블록 ──────────────────────────────────────────────
SCAN_EXCLUDE_TOP = {"40_Archive", "99_Templates", "_workspace", "_attachments"}
FOLDER_REQUIRED = {            # 폴더 prefix → 필수 frontmatter 키
    "01_Slipbox/": ("type", "status"),
    "30_Resources/References/Clippings/": ("status",),
}
DATE_INSTEAD_OF_CREATED = ("30_Resources/Development/DevLog/",)  # date 필드가 created 대체
# ───────────────────────────────────────────────────────────

WIKILINK_RE = re.compile(r"!?\[\[([^\[\]]+?)\]\]")
FENCED_RE = re.compile(r"```.*?```", re.DOTALL)
INLINE_CODE_RE = re.compile(r"`[^`\n]*`")
KEY_RE = re.compile(r"^([A-Za-z_][\w-]*):\s*(.*)$")
LIST_ITEM_RE = re.compile(r"^\s*-\s+(.+)$")


def nfc(s):
    return unicodedata.normalize("NFC", s)


def split_frontmatter(text):
    if not text.startswith("---\n"):
        return None, text
    end = text.find("\n---", 4)
    if end == -1:
        return None, text
    return text[4:end].splitlines(), text[end + 4:]


def parse_frontmatter(lines):
    """최상위 스칼라 키 + 리스트 키 항목을 뽑는 미니 파서 (stdlib에 YAML 없음)."""
    scalars, lists = {}, {}
    current = None
    for line in lines:
        m = KEY_RE.match(line)
        if m:
            current = m.group(1)
            val = m.group(2).strip()
            scalars[current] = val
            if val.startswith("[") and val.endswith("]"):
                lists[current] = [t.strip().strip("'\"") for t in val[1:-1].split(",") if t.strip()]
        elif current is not None:
            lm = LIST_ITEM_RE.match(line)
            if lm:
                lists.setdefault(current, []).append(lm.group(1).strip().strip("'\""))
    return scalars, lists


def extract_links(body):
    body = FENCED_RE.sub("", body)
    body = INLINE_CODE_RE.sub("", body)
    out = []
    for m in WIKILINK_RE.finditer(body):
        t = m.group(1).split("|")[0].split("#")[0].strip()
        if t:
            out.append(nfc(t))
    return out


def is_scanned(rel):
    parts = rel.split("/")
    if parts[0] in SCAN_EXCLUDE_TOP:
        return False
    return not os.path.basename(rel).startswith("_")


def main():
    root = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else ".")

    all_md, resolve, target_index = [], set(), {}
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if not d.startswith(".")]
        for fn in filenames:
            rel = nfc(os.path.relpath(os.path.join(dirpath, fn), root))
            if fn.endswith(".md"):
                all_md.append(rel)
                keys = {nfc(fn[:-3]), rel, rel[:-3]}
            else:
                keys = {nfc(fn), rel}
            resolve.update(keys)
            if fn.endswith(".md"):
                for k in keys:
                    target_index.setdefault(k, set()).add(rel)

    # 1차: frontmatter 캐시 + aliases를 해석 집합에 등록
    fm_cache, body_cache = {}, {}
    for rel in all_md:
        try:
            with open(os.path.join(root, rel), encoding="utf-8") as f:
                text = f.read()
        except (OSError, UnicodeDecodeError):
            continue
        fm_lines, body = split_frontmatter(text)
        body_cache[rel] = body
        if fm_lines is None:
            fm_cache[rel] = (None, {})
            continue
        scalars, lists = parse_frontmatter(fm_lines)
        fm_cache[rel] = (scalars, lists)
        for alias in lists.get("aliases", []):
            a = nfc(alias)
            resolve.add(a)
            target_index.setdefault(a, set()).add(rel)

    # 2차: 링크 그래프 (in-link는 Archive 포함 전체에서 수집)
    in_degree = {rel: 0 for rel in all_md}
    out_count, dead_links = {}, []
    for rel in all_md:
        links = extract_links(body_cache.get(rel, ""))
        out_count[rel] = len(links)
        for t in links:
            hit = target_index.get(t)
            if hit:
                for tgt in hit:
                    if tgt != rel:
                        in_degree[tgt] += 1
            elif t not in resolve and is_scanned(rel):
                dead_links.append({"source": rel, "target": t})

    scanned = [rel for rel in all_md if is_scanned(rel)]

    orphans = [
        {"path": rel, "slipbox": rel.startswith("01_Slipbox/")}
        for rel in scanned
        if out_count.get(rel, 0) == 0 and in_degree.get(rel, 0) == 0
    ]

    frontmatter_issues = []
    for rel in scanned:
        scalars, lists = fm_cache.get(rel, (None, {}))
        issues = []
        if scalars is None:
            issues.append("frontmatter 블록 없음")
        else:
            created_key = "date" if rel.startswith(DATE_INSTEAD_OF_CREATED) else "created"
            if not scalars.get(created_key):
                issues.append(f"필수 필드 누락: {created_key}")
            tags = lists.get("tags", [])
            if not tags:
                issues.append("필수 필드 누락: tags")
            for t in tags:
                if t.startswith("#"):
                    issues.append(f"태그에 # 포함: {t}")
            for prefix, required in FOLDER_REQUIRED.items():
                if rel.startswith(prefix):
                    for k in required:
                        if not scalars.get(k):
                            issues.append(f"필수 필드 누락 ({prefix}): {k}")
            if rel.startswith("20_Projects/") and scalars.get("project_id") and not scalars.get("status"):
                issues.append("필수 필드 누락 (project): status")
        if issues:
            frontmatter_issues.append({"path": rel, "issues": issues})

    print(json.dumps({
        "stats": {
            "vault_root": root,
            "md_total": len(all_md),
            "notes_scanned": len(scanned),
            "orphans": len(orphans),
            "dead_links": len(dead_links),
            "frontmatter_issues": len(frontmatter_issues),
        },
        "orphans": orphans,
        "dead_links": dead_links,
        "frontmatter_issues": frontmatter_issues,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: 테스트 통과 확인**

Run: `python3 .agents/skills/vault-lint/scripts/test_lint_scan.py`
Expected: `OK — all assertions passed`

- [ ] **Step 3: 커밋**

```bash
git add .agents/skills/vault-lint/scripts/
git commit -m "vault-lint: 기계 검사 스캐너 + 픽스처 테스트"
```

---

### Task 3: 실제 vault 검증 (스펙 검증 계획 1~3)

- [ ] **Step 1: 실 vault 실행**

Run: `cd /Users/taez/Projects/obsidian && python3 .agents/skills/vault-lint/scripts/lint_scan.py | head -80`
Expected: 유효한 JSON, `notes_scanned` ≈ 230±30 (md 295개 중 Archive/Templates/_ 제외)

- [ ] **Step 2: 고립 노트 교차 대조**

스캐너 `orphans` 중 slipbox 항목을 `01_Slipbox/` 실물과 대조한다. 기준: base 수식(`file.links.length + file.backlinks.length == 0`)과 동일 정의. 각 고립 후보 노트를 Grep으로 역검증 (`[[<노트명>` 패턴이 vault 어디에도 없고, 본문에 `[[`가 없는지).

- [ ] **Step 3: 죽은 링크 표본 3건 수동 확인**

`dead_links`에서 3건을 골라 대상 파일이 실제로 없는지 Glob으로 확인. 오탐 발견 시 원인(정규화/경로/alias) 수정 후 Task 1 테스트에 회귀 케이스 추가.

- [ ] **Step 4: 조정사항 있으면 커밋**

```bash
git add .agents/skills/vault-lint/scripts/
git commit -m "vault-lint: 실 vault 검증 반영"
```

---

### Task 4: SKILL.md 작성 + 심링크

**Files:**
- Create: `.agents/skills/vault-lint/SKILL.md`
- Create: `.claude/skills/vault-lint` (symlink)

- [ ] **Step 1: SKILL.md 작성**

작성 전 plugin-dev:skill-development 스킬을 호출해 description 트리거 최적화·구조 가이드를 적용한다. 본문 골자 (자립적 — `_workspace` 스펙 참조 금지):

```markdown
---
name: vault-lint
description: Obsidian vault 헬스 체크 및 개선 적용. 고립 노트의 연결 후보를 qmd로 찾아 제안하고, 죽은 링크·frontmatter 스키마 위반을 스캔해 승인된 항목만 적용한다. "vault lint", "vault 점검", "슬립박스 점검", "고립 노트 정리", "연결 제안", "죽은 링크 확인", "주간 정리" 요청 시 사용.
---

# vault-lint: Vault 헬스 체크 + 승인 기반 개선

핵심 원칙: **자동 적용 0건.** 모든 변경은 후보 제시 → 사용자 승인 → 승인분만 적용.
(근거: LLM 링크 제안의 ~30%는 부적합하다는 실사용 보고)

## 절차

1. **기계 검사**: `python3 <skill-dir>/scripts/lint_scan.py <vault-root>` 실행, JSON 파싱.
   스캐너는 읽기 전용이며 고립 노트·죽은 링크·frontmatter 위반을 반환한다.
2. **판단 검사** (qmd MCP 필요 — 불능 시 이 단계를 건너뛰고 리포트에 "degraded mode" 명시):
   - 연결 후보: Slipbox 고립 노트마다 본문을 Read → `mcp__qmd__query`(lex+vec, intent 필수)
     → 상위 후보 노트를 실제로 읽고 → **이유를 한 줄로 설명 가능한 것만** 노트당 1~3개 제안.
   - MOC 공백: Slipbox 전체 frontmatter를 직접 읽어 같은 태그/링크 클러스터 3+ 노트에
     `type: hub` 노트가 없으면 MOC 생성 제안. (Slipbox 50+ 노트가 되면 스캐너 집계 검토)
   - 죽은 링크 처치: 항목별 "오타 수정 / 스텁 생성 / 링크 제거 / 의도적 placeholder 유지" 제안.
     Zettelkasten에서 미해결 링크는 "나중에 쓸 노트" 표시일 수 있다 — 제거를 기본값으로 하지 말 것.
   - frontmatter: 유도 가능한 값만 제안 — created 누락은
     `git log --diff-filter=A --follow --format=%as -1 -- <file>`로, 태그 `#`는 제거로.
     유도 불가(type/status/태그 내용)는 리포트 전용.
3. **리포트 생성**: `_workspace/lint-YYYY-MM-DD/report.md` — 요약 통계, 카테고리별 발견+제안,
   degraded 여부. (7일 수명 규약 대상)
4. **승인**: AskUserQuestion(multiSelect)으로 카테고리별 채택 항목 선택.
5. **체크포인트 커밋**: `git status` 요약(함께 커밋될 무관 변경 N건)을 고지한 뒤
   vault 관례대로 `checkpoint: lint 적용 전 스냅샷` 전체 커밋.
6. **적용**: 승인 항목만. 연결 추가는 노트 하단 `## 연결된 노트` 섹션에 `- [[노트]] - 이유` 형식
   (CLAUDE.md 연결 규약). 거부 항목은 리포트에 `보류` 표기.
7. **마무리**: 적용 내역 요약. 자동 커밋 없음 — 커밋 여부는 사용자 판단.

## 경계

- 스키마 기준은 `99_Templates/_property-schema.md`. 스키마 변경 시 `lint_scan.py` 상단
  설정 블록만 갱신하면 된다.
- inbox 승격·대화 캡처는 이 스킬 비범위.
```

(실제 작성 시 skill-development 가이드에 따라 description·구조를 다듬는다. 위 골자에서 벗어나는 변경은 스펙 위반 여부를 확인할 것.)

- [ ] **Step 2: 심링크 생성 (qmd 컨벤션과 동일)**

```bash
ln -s ../../.agents/skills/vault-lint /Users/taez/Projects/obsidian/.claude/skills/vault-lint
ls -la /Users/taez/Projects/obsidian/.claude/skills/
```

Expected: `vault-lint ⇒ ../../.agents/skills/vault-lint`

- [ ] **Step 3: 커밋**

```bash
git add .agents/skills/vault-lint/SKILL.md .claude/skills/vault-lint
git commit -m "vault-lint: SKILL.md + .claude 심링크"
```

---

### Task 5: E2E 드라이런 + 마무리

- [ ] **Step 1: E2E 드라이런** — 새 스킬 절차 1~3단계만 수행(적용 없이): 스캐너 실행 → Slipbox 고립 노트 1개에 대해 qmd 연결 후보 탐색 → `_workspace/lint-2026-06-12/report.md` 생성. 리포트에 통계/제안/이유가 형식대로 들어갔는지 확인.

- [ ] **Step 2: 승인 루프는 실 사용에서 검증** — 사용자에게 리포트를 보여주고 첫 실전 lint를 지금 돌릴지 확인 (돌리면 절차 4~7 진행).

- [ ] **Step 3: 메모리 갱신** — `qmd-vault-search.md` 메모리에 vault-lint 스킬 존재를 한 줄 연결하거나 신규 project 메모리 작성.

- [ ] **Step 4: 커밋**

```bash
git add _workspace/lint-2026-06-12/
git commit -m "vault-lint: E2E 드라이런 리포트"
```
