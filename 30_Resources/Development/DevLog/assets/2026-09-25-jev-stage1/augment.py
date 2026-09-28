"""최종 평가용 보강: 이미 뽑은 최종 평가용 노트의 남은 문단에서 더 뽑는다. 외부 호출 없음."""
import hashlib, json, random, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import prepare as P

OUT = Path(__file__).resolve().parent
SEED = 20260926
manifest = json.loads((OUT / "manifest.json").read_text())
sources = json.loads((OUT / "sources.json").read_text())
items = [json.loads(l) for l in (OUT / "items.jsonl").open()]
seen = P.labelled_sentences()
rng = random.Random(SEED)
new = []
for s in sources:
    if s["split"] != "final":
        continue
    _, body = P.frontmatter(P.git("show", f"{manifest['commit']}:{s['path']}"))
    paras = [p for p in P.paragraphs(body) if not any(k in P.norm(p) for k in seen)]
    assert len(paras) == s["eligible_paragraphs"], s["path"]
    rest = [i for i in range(len(paras)) if i not in s["paragraph_indexes"]]
    k = 3 if s["folder"].endswith(("Troubleshooting", "blog")) else 2
    chosen = sorted(rng.sample(rest, min(k, len(rest))))
    s["augment_indexes"] = chosen
    for j, idx in enumerate(chosen):
        p = paras[idx]
        new.append({"id": f"{s['id']}-A{j + 1}", "source": s["id"], "split": "final", "batch": "보강",
                    "title": s["title"], "folder": s["folder"].split("/")[-1], "paragraph_index": idx, "text": p,
                    "sha256": hashlib.sha256(p.encode()).hexdigest()[:16]})
rng.shuffle(new)
items += new
(OUT / "sources.json").write_text(json.dumps(sources, ensure_ascii=False, indent=2))
with (OUT / "items.jsonl").open("w") as fh:
    for x in items:
        fh.write(json.dumps(x, ensure_ascii=False) + "\n")
manifest.update({"dataset_version": "stage1-draft-2", "items": len(items), "final_items": sum(x["split"] == "final" for x in items),
                 "augmented_items": len(new), "augment_seed": SEED})
(OUT / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2))
html = (OUT / "review_template.html").read_text()
(OUT / "review.html").write_text(html.replace("/*ITEMS*/[]", json.dumps(items, ensure_ascii=False)))
print(len(new), "added;", {s["id"]: s.get("augment_indexes") for s in sources if s["split"] == "final"})
