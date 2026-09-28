"""Slipbox 영구 노트의 성숙도를 Score로 매기고 사람이 붙인 status와 견준다. 노트는 수정하지 않는다."""
import glob, json, os, re
from concurrent.futures import ThreadPoolExecutor
from typesafe_sdk import Noul, Score, TypeSafeClient

VAULT = "/Users/taez/Projects/obsidian"
D = os.path.dirname(os.path.abspath(__file__))
TAIL = re.compile(r"\n## (출처|연관된 노트|연관된 글|참고 자료)\b.*", re.S)  # 링크 수로 판정하지 않도록 뺀다


def load(p):
    t = open(p, encoding="utf-8").read()
    fm, body = re.match(r"---\n(.*?)\n---\n?(.*)", t, re.S).groups()
    get = lambda k: (re.search(rf"^{k}:\s*(.*)$", fm, re.M) or [None, ""])[1].strip()
    body = TAIL.sub("", body)
    body = re.sub(r"%%.*?%%", "", body, flags=re.S)
    body = re.sub(r"!\[\[[^\]]*\]\]", "", body)
    body = re.sub(r"\[\[([^\]|]*\|)?([^\]]*)\]\]", r"\2", body)
    body = re.sub(r"\s\^[\w-]+$", "", body, flags=re.M)
    used = len(re.findall(r"^\s+-\s", (re.search(r"^used_in:\s*\n((?:\s+-.*\n?)+)", fm + "\n", re.M) or [None, ""])[1], re.M))
    return {"path": p[len(VAULT) + 1:], "status": get("status"), "type": get("type"), "used_in": used,
            "title": os.path.basename(p)[:-3], "body": body.strip()[:4000]}


notes = [n for n in map(load, sorted(glob.glob(f"{VAULT}/01_Slipbox/*.md"))) if n["type"] == "permanent"]

SUPPORT = Score(
    instructions=(
        "How much support does this Korean note give its central claim, beyond stating and explaining the claim? "
        "Count only what the note body contains: concrete evidence or reasons from experience or sources, "
        "a counterexample or a stated limit of the claim, or a real case where the claim was applied."),
    criteria=[
        "Only the claim: the note states and explains its central claim, but gives no concrete evidence, "
        "no counterexample or limit, and no real case where it was applied.",
        "One kind of support: besides the claim, the note gives exactly one of concrete evidence, "
        "a counterexample or limit, or a real case where the claim was applied.",
        "Several kinds of support: the note gives two or more of concrete evidence, "
        "a counterexample or limit, and a real case where the claim was applied.",
    ],
)
PARTS = {
    "evidence": Noul(instructions="Does the note give concrete evidence or a reason from experience or a source for its central claim, beyond explaining the claim?"),
    "limit": Noul(instructions="Does the note state a counterexample to its central claim, or a condition where the claim does not hold?"),
    "application": Noul(instructions="Does the note describe a real case where its central claim was applied or tested?"),
}

client = TypeSafeClient()


def run(n):
    r = client.system_one({"title": n["title"], "body": n["body"]}, {"support": SUPPORT, **PARTS})
    s = r.scores["support"]
    return {k: v for k, v in n.items() if k != "body"} | {
        "score": s.score, "confidence": s.confidence, "probabilities": dict(s.probabilities),
        **{k: r.nouls[k].noul for k in PARTS}}


with ThreadPoolExecutor(8) as ex:
    out = list(ex.map(run, notes))
json.dump(out, open(f"{D}/exp6_results.json", "w"), ensure_ascii=False, indent=1)
print(f"notes={len(out)}")
