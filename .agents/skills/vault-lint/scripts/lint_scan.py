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
        # 표 안의 위키링크는 파이프를 \| 로 이스케이프함 — 풀어준 뒤 분리
        t = m.group(1).replace("\\|", "|").split("|")[0].split("#")[0].strip()
        if t:
            out.append(nfc(t))
    return out


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
    for rel in all_md:
        links = extract_links(body_cache.get(rel, ""))
        out_count[rel] = len(links)
        for t in links:
            hit = target_index.get(t)
            if hit:
                for tgt in hit:
                    if tgt != rel:
                        in_degree[tgt] += 1
                    if (
                        rel.startswith("20_Projects/blog/")
                        and tgt.startswith("01_Slipbox/")
                    ):
                        blog_to_slipbox_edges.add((rel, tgt))
            elif t not in resolve and is_scanned(rel):
                dead_links.append({"source": rel, "target": t})

    scanned = [rel for rel in all_md if is_scanned(rel)]

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
            "base_total": len(all_base),
            "base_issues": len(base_issues),
            "reuse": {
                "blog_to_slipbox_edges": len(blog_to_slipbox_edges),
                "blog_notes_with_slipbox_refs": len(reused_blog_notes),
                "slipbox_notes_reused_by_blog": len(reused_slipbox_notes),
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
            },
            "informational": {
                "non_slipbox_orphans": non_slipbox_orphans,
                "periodic_placeholders": len(periodic_placeholders),
                "series_placeholders": len(series_placeholders),
            },
        },
        "orphans": orphans,
        "dead_links": dead_links,
        "periodic_placeholders": periodic_placeholders,
        "series_placeholders": series_placeholders,
        "frontmatter_issues": frontmatter_issues,
        "base_issues": base_issues,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
