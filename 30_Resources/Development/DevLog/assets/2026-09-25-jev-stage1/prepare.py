"""Jev 1단계 표본 준비: 게시된 공개 노트에서 단일 문단을 뽑는다. 외부 호출 없음.

python3 prepare.py  (이 폴더에서 실행)
"""
import hashlib, json, random, re, subprocess
from pathlib import Path

ROOT = Path(subprocess.run(["git", "-C", str(Path(__file__).resolve().parent), "rev-parse", "--show-toplevel"],
                          capture_output=True, text=True, check=True).stdout.strip())
OUT = Path(__file__).resolve().parent
PRIOR = ROOT / "30_Resources/Development/DevLog/assets/2026-09-24-jev"
REF = "origin/main"
SEED = 20260925
PER_NOTE = 4
# 노트 수: (조정용, 최종 평가용). 경험 서술이 많은 폴더를 두 배로 둔다
STRATA = {
    "30_Resources/Development/Troubleshooting": (2, 2),
    "20_Projects/blog": (2, 2),
    "01_Slipbox": (1, 1),
    "30_Resources/Development/Concepts": (1, 1),
}
# 링크는 없지만 같은 경험을 다시 쓴 글. 제목에 이 말이 들어간 노트를 한 묶음으로 본다
MANUAL_GROUPS = {
    "HEXACO": "작성자의 HEXACO 검사 결과를 연재와 단독 글에서 다시 다룬다",
}
TAIL_SECTIONS = re.compile(r"^## (연관된 노트|연관된 글|출처|참고 자료|참고)\s*$", re.M)


def git(*args):
    return subprocess.run(["git", "-C", str(ROOT), *args], capture_output=True, text=True, check=True).stdout


def frontmatter(text):
    m = re.match(r"---\n(.*?)\n---\n", text, re.S)
    if not m:
        return {}, text
    fm, meta, key = m.group(1), {}, None
    for line in fm.splitlines():
        if re.match(r"^[\w-]+:", line):
            key, _, val = line.partition(":")
            meta[key] = val.strip().strip('"')
        elif key and line.strip().startswith("- "):
            meta[key] = (meta[key] + "\n" if meta[key] else "") + line.strip()[2:].strip('"')
    return meta, text[m.end():]


def wikitargets(s):
    return {re.split(r"[|#]", t)[0].strip() for t in re.findall(r"\[\[([^\]]+)\]\]", s or "")}


def clean(p):
    p = re.sub(r"\[\[([^\]|#]*)(?:#[^\]|]*)?\|([^\]]*)\]\]", r"\2", p)
    p = re.sub(r"\[\[([^\]|#]*)(?:#[^\]]*)?\]\]", r"\1", p)
    p = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", p)
    p = re.sub(r"\[\^[^\]]+\]", "", p)
    p = re.sub(r"\*\*|__|==", "", p)
    p = re.sub(r"\s*\^[\w-]+$", "", p)
    return re.sub(r"\s+", " ", p).strip()


def paragraphs(body):
    body = re.sub(r"%%.*?%%", "", body, flags=re.S)
    body = re.sub(r"```.*?```", "", body, flags=re.S)
    tail = TAIL_SECTIONS.search(body)
    if tail:
        body = body[: tail.start()]
    out = []
    non_prose = re.compile(r"(#|\||[-*+] |\d+\\?\. |>|!\[|\[\^|<)")
    for block in re.split(r"\n\s*\n", body):
        # 산문 문단만: 헤딩·표·목록·인용·콜아웃·이미지·각주 정의는 뺀다. 산문 뒤에 붙은 목록은 잘라 낸다
        lines = []
        for line in block.strip().splitlines():
            if non_prose.match(line.strip()):
                break
            lines.append(line)
        b = "\n".join(lines).strip()
        if not b:
            continue
        c = clean(b)
        if 60 <= len(c) <= 700:
            out.append(c)
    return out


def norm(s):
    return re.sub(r"[\s\W_]+", "", s)


def labelled_sentences():
    """이전 실험에서 사람이(당시 Claude가) 라벨을 붙이며 읽은 본문 문장."""
    occ = {o["id"]: o["sentence"] for o in json.loads((PRIOR / "exp1_occurrences.json").read_text())}
    s = [occ[i] for i in json.loads((PRIOR / "exp1_sample_ids.json").read_text())]
    s += [r["sentence"] for r in json.loads((PRIOR / "exp4_sample.json").read_text())]
    s += [r["sentence"] for r in json.loads((PRIOR / "exp5_holdout.json").read_text())]
    return [norm(x)[:25] for x in s if len(norm(x)) >= 12]


def eligible(path, meta):
    if path.startswith("01_Slipbox/"):
        return meta.get("type") == "permanent"
    if path.startswith("20_Projects/blog/"):
        return meta.get("status") == "published" and meta.get("type") != "series"
    return True


def main():
    commit = git("rev-parse", REF).strip()
    files = [f for f in git("ls-tree", "-r", "--name-only", REF, "--", *STRATA).splitlines()
             if f.endswith(".md") and not any(p.startswith(("_", ".")) for p in f.split("/"))]
    seen = labelled_sentences()
    notes, excluded_para = {}, 0
    for f in files:
        text = git("show", f"{REF}:{f}")
        meta, body = frontmatter(text)
        if not eligible(f, meta):
            continue
        paras = []
        for p in paragraphs(body):
            if any(k in norm(p) for k in seen):
                excluded_para += 1
                continue
            paras.append(p)
        notes[f] = {"meta": meta, "paras": paras, "title": Path(f).stem}

    # 같은 연재, related·used_in으로 이어진 글은 한 묶음으로 본다
    parent = {f: f for f in notes}
    by_title = {n["title"]: f for f, n in notes.items()}
    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    def union(a, b):
        parent[find(a)] = find(b)
    series = {}
    for f, n in notes.items():
        if n["meta"].get("series"):
            series.setdefault(n["meta"]["series"], []).append(f)
        for t in wikitargets(n["meta"].get("related")) | wikitargets(n["meta"].get("used_in")):
            if t in by_title:
                union(f, by_title[t])
    for key in MANUAL_GROUPS:
        series.setdefault(f"manual:{key}", []).extend(f for f, n in notes.items() if key in n["title"])
    for members in series.values():
        for m in members[1:]:
            union(members[0], m)

    rng = random.Random(SEED)
    used_groups, sources, items = set(), [], []
    for folder, (n_tune, n_final) in STRATA.items():
        pool = sorted(f for f, n in notes.items() if f.startswith(folder + "/") and len(n["paras"]) >= PER_NOTE)
        rng.shuffle(pool)
        picked = []
        for f in pool:
            if find(f) in used_groups:
                continue
            used_groups.add(find(f))
            picked.append(f)
            if len(picked) == n_tune + n_final:
                break
        for i, f in enumerate(picked):
            split = "tune" if i < n_tune else "final"
            n = notes[f]
            chosen = sorted(rng.sample(range(len(n["paras"])), PER_NOTE))
            sid = f"N{len(sources) + 1:02d}"
            sources.append({"id": sid, "path": f, "title": n["title"], "split": split, "folder": folder,
                            "eligible_paragraphs": len(n["paras"]), "paragraph_indexes": chosen,
                            "blob": git("rev-parse", f"{REF}:{f}").strip()})
            for k, idx in enumerate(chosen):
                p = n["paras"][idx]
                items.append({"id": f"{sid}-P{k + 1}", "source": sid, "split": split, "title": n["title"],
                              "folder": folder.split("/")[-1], "paragraph_index": idx, "text": p,
                              "sha256": hashlib.sha256(p.encode()).hexdigest()[:16]})

    # 검토 순서는 분할 안에서 섞는다. 같은 노트 문단이 이어지면 앞 문단의 판단이 뒤로 번진다
    ordered = []
    for split in ("tune", "final"):
        part = [x for x in items if x["split"] == split]
        rng.shuffle(part)
        ordered += part

    (OUT / "sources.json").write_text(json.dumps(sources, ensure_ascii=False, indent=2))
    with (OUT / "items.jsonl").open("w") as fh:
        for x in ordered:
            fh.write(json.dumps(x, ensure_ascii=False) + "\n")
    manifest = {
        "dataset_version": "stage1-draft-1", "created": "2026-09-25", "ref": REF, "commit": commit, "seed": SEED,
        "eligible_notes": len(notes), "groups": len({find(f) for f in notes}),
        "excluded_paragraphs_prior_labels": excluded_para, "prior_label_keys": len(seen),
        "sources": len(sources), "items": len(ordered),
        "tune_items": sum(x["split"] == "tune" for x in ordered),
        "final_items": sum(x["split"] == "final" for x in ordered),
        "human_reviewed_count": 0, "model_calls": 0, "cost_usd": 0,
    }
    (OUT / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2))

    html = (OUT / "review_template.html").read_text()
    (OUT / "review.html").write_text(html.replace("/*ITEMS*/[]", json.dumps(ordered, ensure_ascii=False)))
    print(json.dumps(manifest, ensure_ascii=False, indent=2))
    for s in sources:
        print(s["id"], s["split"], s["eligible_paragraphs"], s["path"])


if __name__ == "__main__":
    main()
