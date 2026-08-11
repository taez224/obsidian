#!/usr/bin/env python3
"""vault-lint 기계 검사 스캐너 — 읽기 전용, vault 파일을 절대 수정하지 않는다.

사용: python3 lint_scan.py [vault_root]   (기본: 현재 디렉토리)
출력: JSON {stats, priorities, orphans, dead_links, periodic_placeholders, series_placeholders,
           frontmatter_issues, base_issues}

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
    "30_Resources/References/Articles/": ("source", "published", "status"),
    "30_Resources/References/Clippings/": ("status",),
}
DATE_INSTEAD_OF_CREATED = ("30_Resources/Development/DevLog/",)  # date 필드가 created 대체
ORPHAN_EXCLUDE = (             # 날짜 기반 노트 — 위키링크 연결이 목적이 아니라 orphan 판정 제외
    "10_Periodic Notes/",
    "30_Resources/Development/DevLog/",
)
BASE_INVALID_KEYS = {"sortBy"}  # .base 파일에 없는 키인데 흔히 착각해서 쓰는 것들. 발견되는 대로 추가.

# 재사용 판정 — "이 영구 노트가 다른 맥락에서 다시 쓰였는가"를 센다.
# 출처(이 자료에서 노트가 나왔다)는 재사용이 아니다. X에서 파생된 것은 X를 입증하지 못한다.
REUSE_PROVENANCE_MARKERS = (   # 링크 옆 설명에 이 표현이 있으면 출처로 보고 재사용에서 뺀다
    "로 승격", "으로 승격",
    "압축한 영구 노트", "정제한 영구 노트", "정제한 결과",
    "에서 출발한",
)
# 맨 "승격"·"출발점"은 마커에 넣지 않는다. 본문 개념어로도 쓰이고,
# "출발점"은 화자가 누구냐에 따라 출처와 재사용이 뒤집힌다.
# ───────────────────────────────────────────────────────────

WIKILINK_RE = re.compile(r"!?\[\[([^\[\]]+?)\]\]")
FENCED_RE = re.compile(r"```.*?```", re.DOTALL)
INLINE_CODE_RE = re.compile(r"`[^`\n]*`")
KEY_RE = re.compile(r"^([A-Za-z_][\w-]*):\s*(.*)$")
LIST_ITEM_RE = re.compile(r"^\s*-\s+(.+)$")
BASE_KEY_RE = re.compile(r"^\s*([A-Za-z_][\w-]*)\s*:")
PERIODIC_PLACEHOLDER_RE = re.compile(
    r"^(?:\d{4}-\d{2}(?:-\d{2})?|\d{4}-W\d{2})$"
)
# 블록 ID는 줄 끝에서만 인식된다 — 단독 줄(`^id`)과 텍스트 뒤(`본문 ^id`) 둘 다 유효하다.
# 줄 앞에 두면(`^id 본문`) Obsidian이 블록 ID로 보지 않는다.
BLOCK_ANCHOR_RE = re.compile(r"(?:^|\s)\^([A-Za-z0-9-]+)[ \t]*$")
ANCHOR_LINK_RE = re.compile(r"!?\[\[([^\[\]]+?)\]\]")


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


def extract_links_with_context(body):
    """(target, 링크가 있던 줄) 목록.

    재사용 판정은 링크 자체가 아니라 링크 옆에 적은 관계 설명을 봐야 해서
    줄 텍스트가 필요하다. 관계 설명은 본문 문장이나 ``## 연관된 노트``
    항목 어느 쪽에도 있을 수 있다.
    """
    body = FENCED_RE.sub("", body)
    body = INLINE_CODE_RE.sub("", body)
    out = []
    for line in body.splitlines():
        for m in WIKILINK_RE.finditer(line):
            # 표 안의 위키링크는 파이프를 \| 로 이스케이프함 — 풀어준 뒤 분리
            t = m.group(1).replace("\\|", "|").split("|")[0].split("#")[0].strip()
            if t:
                out.append((nfc(t), line.strip()))
    return out


def extract_links(body):
    return [t for t, _ in extract_links_with_context(body)]


def extract_block_anchors(body):
    """이 문서가 실제로 정의한 블록 ID 집합."""
    body = FENCED_RE.sub("", body)
    return {m.group(1) for line in body.splitlines()
            for m in [BLOCK_ANCHOR_RE.search(line)] if m}


def extract_anchor_links(body):
    """(대상 문서, 블록 ID) 목록 — `[[문서#^id]]` 형태만.

    블록 링크는 앵커가 없어도 문서로는 해석되므로 링크가 살아 있는 것처럼 보인다.
    그래서 죽은 링크 검사만으로는 잡히지 않고 출처 정밀도가 조용히 문서 단위로 퇴화한다.
    """
    body = FENCED_RE.sub("", body)
    body = INLINE_CODE_RE.sub("", body)
    out = []
    for m in ANCHOR_LINK_RE.finditer(body):
        raw = m.group(1).replace("\\|", "|").split("|")[0].strip()
        if "#^" not in raw:
            continue
        target, _, anchor = raw.partition("#^")
        target, anchor = target.strip(), anchor.strip()
        if target and anchor:
            out.append((nfc(target), anchor))
    return out


def reuse_source_kind(rel):
    if rel.startswith("00_Inbox/"):
        return "inbox"
    if rel.startswith("30_Resources/References/"):
        return "reference"
    if rel.startswith("20_Projects/blog/"):
        return "blog"
    if rel.startswith("20_Projects/"):
        return "project"
    return "operational"          # 운영 문서·MOC 등 — 자료가 아니라 적용처다


def classify_reuse_edge(kind, marked, mutual):
    """(판정, 사유). 판정은 reuse | excluded | pending."""
    if kind == "inbox":
        # README 원칙: Inbox는 탐색 단서일 뿐 현재 입장의 근거가 아니다.
        # Inbox를 벗어나 승격·흡수될 때 다시 판정한다.
        return "pending", "Inbox 초안 — 근거로 세지 않음"
    if marked:
        return "excluded", "출처 표지 문구"
    if kind == "blog":
        # 블로그는 노트를 낳기도 하고 인용하기도 해서 상호 여부로 갈리지 않는다.
        # 표지 문구가 없으면 인용으로 본다.
        return "reuse", "블로그 인용"
    if mutual and kind == "reference":
        return "excluded", "상호 + 읽은 자료"
    if mutual:
        return "reuse", "상호지만 상대가 적용처"
    return "reuse", "단방향"


def is_scanned(rel):
    parts = rel.split("/")
    if len(parts) == 1:  # 루트 인프라 문서 (README/CLAUDE/AGENTS) — 노트 아님
        return False
    if parts[0] in SCAN_EXCLUDE_TOP:
        return False
    # _ 접두 규칙은 파일명뿐 아니라 중간 폴더에도 적용 (예: blog/_candidates/)
    return not any(p.startswith("_") for p in parts)


def is_base_scanned(rel):
    # .base 대시보드는 관례상 파일명이 _로 시작하므로(_index.base 등) is_scanned의
    # _ 제외 규칙을 그대로 쓰면 전부 걸러진다 — 최상위 제외 폴더만 적용한다.
    parts = rel.split("/")
    top = parts[0] if len(parts) > 1 else None
    return top not in SCAN_EXCLUDE_TOP


def is_periodic_placeholder(source, target):
    return (
        source.startswith("10_Periodic Notes/")
        and PERIODIC_PLACEHOLDER_RE.fullmatch(target) is not None
    )


def is_series_placeholder(source, fm_cache):
    """진행 중·잠정 중단 시리즈 허브의 미해결 링크는 예정 글로 취급한다."""
    scalars, _ = fm_cache.get(source, (None, {}))
    if scalars is None:
        return False
    note_type = scalars.get("type", "").strip("'\"")
    status = scalars.get("status", "").strip("'\"")
    return note_type == "series" and status != "completed"


def scan_base_issues(root, all_base):
    issues = []
    for rel in all_base:
        try:
            with open(os.path.join(root, rel), encoding="utf-8") as f:
                lines = f.read().splitlines()
        except (OSError, UnicodeDecodeError):
            continue
        for i, line in enumerate(lines, start=1):
            m = BASE_KEY_RE.match(line)
            if m and m.group(1) in BASE_INVALID_KEYS:
                issues.append({"path": rel, "line": i, "key": m.group(1)})
    return issues


def main():
    root = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else ".")

    all_md, all_base, resolve, target_index = [], [], set(), {}
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if not d.startswith(".")]
        for fn in filenames:
            rel = nfc(os.path.relpath(os.path.join(dirpath, fn), root))
            if fn.endswith(".base"):
                all_base.append(rel)
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
    out_count, dead_links, blog_to_slipbox_edges = {}, [], set()
    out_targets = {rel: set() for rel in all_md}
    slipbox_inbound = {}          # tgt → {src: [링크가 있던 줄]}
    for rel in all_md:
        links = extract_links_with_context(body_cache.get(rel, ""))
        out_count[rel] = len(links)
        for t, line in links:
            hit = target_index.get(t)
            if hit:
                for tgt in hit:
                    if tgt != rel:
                        in_degree[tgt] += 1
                        out_targets[rel].add(tgt)
                    if (
                        rel.startswith("20_Projects/blog/")
                        and tgt.startswith("01_Slipbox/")
                    ):
                        blog_to_slipbox_edges.add((rel, tgt))
                    if (
                        tgt.startswith("01_Slipbox/")
                        and not rel.startswith("01_Slipbox/")
                        and is_scanned(rel)
                    ):
                        slipbox_inbound.setdefault(tgt, {}).setdefault(rel, []).append(line)
            elif t not in resolve and is_scanned(rel):
                dead_links.append({"source": rel, "target": t})

    scanned = [rel for rel in all_md if is_scanned(rel)]

    # 3차: 블록 앵커 — 대상 문서는 해석되는데 그 안에 블록 ID가 없는 링크
    anchors = {rel: extract_block_anchors(body_cache.get(rel, "")) for rel in all_md}
    broken_anchors = []
    for rel in scanned:
        for target, anchor in extract_anchor_links(body_cache.get(rel, "")):
            hit = target_index.get(target)
            if not hit:
                continue          # 문서 자체가 미해석이면 dead_links가 이미 잡는다
            if not any(anchor in anchors.get(tgt, set()) for tgt in hit):
                broken_anchors.append({
                    "source": rel,
                    "target": sorted(hit)[0],
                    "anchor": anchor,
                })

    orphans = [
        {"path": rel, "slipbox": rel.startswith("01_Slipbox/")}
        for rel in scanned
        if out_count.get(rel, 0) == 0 and in_degree.get(rel, 0) == 0
        and not rel.startswith(ORPHAN_EXCLUDE)
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

    base_scanned = [rel for rel in all_base if is_base_scanned(rel)]
    base_issues = scan_base_issues(root, base_scanned)

    slipbox_orphans = sum(1 for orphan in orphans if orphan["slipbox"])
    non_slipbox_orphans = len(orphans) - slipbox_orphans
    periodic_placeholders = [
        item for item in dead_links
        if is_periodic_placeholder(item["source"], item["target"])
    ]
    series_placeholders = [
        item for item in dead_links
        if is_series_placeholder(item["source"], fm_cache)
    ]
    meaning_dead_links = [
        item for item in dead_links
        if not is_periodic_placeholder(item["source"], item["target"])
        and not is_series_placeholder(item["source"], fm_cache)
    ]
    reused_blog_notes = {source for source, _ in blog_to_slipbox_edges}
    reused_slipbox_notes = {target for _, target in blog_to_slipbox_edges}

    # 재사용 판정 — 영구 노트가 Slipbox 밖에서 다시 쓰였는가.
    # type 필터(permanent/hub)는 여기서 걸지 않는다. 기계 집계만 하고
    # 의미 구분은 Base 뷰와 review-zettelkasten이 맡는다.
    slipbox_notes = sorted(rel for rel in scanned if rel.startswith("01_Slipbox/"))
    reuse_by_note = []
    reuse_edges = excluded_edges = pending_edges = 0
    for tgt in slipbox_notes:
        scalars, _ = fm_cache.get(tgt, (None, {}))
        entry = {
            "path": tgt,
            "status": (scalars or {}).get("status", "").strip("'\""),
            "reuse_count": 0,
            "reused_by": [],
            "excluded": [],
            "pending": [],
        }
        for src, lines in sorted(slipbox_inbound.get(tgt, {}).items()):
            verdict, why = classify_reuse_edge(
                reuse_source_kind(src),
                any(m in " ".join(lines) for m in REUSE_PROVENANCE_MARKERS),
                src in out_targets.get(tgt, set()),
            )
            record = {"path": src, "reason": why}
            if verdict == "reuse":
                entry["reused_by"].append(record)
                reuse_edges += 1
            elif verdict == "excluded":
                entry["excluded"].append(record)
                excluded_edges += 1
            else:
                entry["pending"].append(record)
                pending_edges += 1
        entry["reuse_count"] = len(entry["reused_by"])
        reuse_by_note.append(entry)

    reuse_by_note.sort(key=lambda e: (-e["reuse_count"], e["path"]))
    notes_reused = sum(1 for e in reuse_by_note if e["reuse_count"] > 0)
    seedling_with_reuse = sum(
        1 for e in reuse_by_note if e["reuse_count"] > 0 and e["status"] == "seedling"
    )

    print(json.dumps({
        "stats": {
            "vault_root": root,
            "md_total": len(all_md),
            "notes_scanned": len(scanned),
            "orphans": len(orphans),
            "dead_links": len(dead_links),
            "periodic_placeholders": len(periodic_placeholders),
            "series_placeholders": len(series_placeholders),
            "frontmatter_issues": len(frontmatter_issues),
            "broken_anchors": len(broken_anchors),
            "base_total": len(all_base),
            "base_issues": len(base_issues),
            "reuse": {
                "blog_to_slipbox_edges": len(blog_to_slipbox_edges),
                "blog_notes_with_slipbox_refs": len(reused_blog_notes),
                "slipbox_notes_reused_by_blog": len(reused_slipbox_notes),
                "slipbox_notes_total": len(slipbox_notes),
                "slipbox_notes_reused": notes_reused,
                "slipbox_notes_unused": len(slipbox_notes) - notes_reused,
                "reuse_edges": reuse_edges,
                "excluded_edges": excluded_edges,
                "pending_edges": pending_edges,
            },
        },
        "priorities": {
            "mechanical": {
                "frontmatter_issues": len(frontmatter_issues),
                "base_issues": len(base_issues),
            },
            "meaning_review": {
                "slipbox_orphans": slipbox_orphans,
                "dead_links": len(meaning_dead_links),
                "broken_anchors": len(broken_anchors),
            },
            "informational": {
                "non_slipbox_orphans": non_slipbox_orphans,
                "periodic_placeholders": len(periodic_placeholders),
                "series_placeholders": len(series_placeholders),
                "seedling_with_reuse": seedling_with_reuse,
                "pending_reuse_edges": pending_edges,
            },
        },
        "reuse_by_note": reuse_by_note,
        "orphans": orphans,
        "dead_links": dead_links,
        "broken_anchors": broken_anchors,
        "periodic_placeholders": periodic_placeholders,
        "series_placeholders": series_placeholders,
        "frontmatter_issues": frontmatter_issues,
        "base_issues": base_issues,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
