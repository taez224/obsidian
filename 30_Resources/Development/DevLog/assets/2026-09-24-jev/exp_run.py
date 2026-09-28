"""세 실험을 TypeSafe로 실행한다. 입력은 exp_prepare.py가 공개 노트에서 추출한 것뿐이다."""
import json, os, re, time
from concurrent.futures import ThreadPoolExecutor
from typesafe_sdk import Choice, Noul, TypeSafeClient

D = os.path.dirname(os.path.abspath(__file__))
VAULT = "/Users/taez/Projects/obsidian"
client = TypeSafeClient()
usage = {"requests": 0, "input_tokens": 0}


def call(state, questions):
    r = client.system_one(state, questions)
    usage["requests"] += 1
    usage["input_tokens"] += getattr(getattr(r, "usage", None), "input_tokens", 0) or 0
    return r


def pmap(f, xs):
    with ThreadPoolExecutor(8) as ex:
        return list(ex.map(f, xs))


# 실험 1: 양분법 판정 (Pre-parsed extraction 패턴: 정규식 후보 + 문맥 판정)
CONTRAST = Choice(
    instructions=(
        "The sentence `sentence` (Korean) contains a negation such as '아니라', '아니었', or '아닙니다'. "
        "Classify how that negation is used. Use `before` and `after` only as context."
    ),
    criteria={
        "informative": "A 'not X but Y' contrast where X is a belief a reader plausibly holds or an alternative the writer actually considered or observed. Removing 'not X' would lose information.",
        "rhetorical": "A 'not X but Y' contrast where X is a straw man or vague foil set up only to make Y sound important, as in slogans like 'this is not simply X, it is Y'. Removing 'not X' would lose little.",
        "not_contrast": "Not a 'not X but Y' contrast at all: an additive 'not only X but also Y' (뿐만 아니라, 뿐 아니라), or a plain denial with no opposing Y.",
    },
)
occ = json.load(open(f"{D}/exp1_occurrences.json"))
exp1 = pmap(lambda o: {**o, "jev": (lambda a: {"choice": a.choice, "confidence": a.confidence, "probabilities": dict(a.probabilities)})(
    call({"post_title": o["post"], "before": o["before"], "sentence": o["sentence"], "after": o["after"]},
         {"contrast": CONTRAST}).choices["contrast"])}, occ)
json.dump(exp1, open(f"{D}/exp1_results.json", "w"), ensure_ascii=False, indent=1)

# 실험 2: summary 꼬리 판정
META = Noul(instructions=(
    "The Korean sentence `summary` is the one-line summary of a note or blog post. "
    "Does its main predicate describe what the note does (for example: introduces, explains, organizes, covers, looks at, "
    "proposes, reflects on, or is a record or post about X) instead of directly stating the question, the answer, "
    "the distinction, or the claim itself?"
))
summ = json.load(open(f"{D}/exp2_summaries.json"))
exp2 = pmap(lambda s: {**s, "jev": call({"summary": s["summary"]}, {"meta": META}).nouls["meta"].noul}, summ)
json.dump(exp2, open(f"{D}/exp2_results.json", "w"), ensure_ascii=False, indent=1)

# 실험 3: 링크 후보 관계 판정 (Re-ranking 패턴: 후보 쌍마다 질문)
def excerpt(name, n):
    t = open(f"{VAULT}/01_Slipbox/{name}.md", encoding="utf-8").read()
    body = re.sub(r"^---\n.*?\n---\n?", "", t, flags=re.S)
    body = re.sub(r"\[\[([^\]|]*\|)?([^\]]*)\]\]", r"\2", body)
    body = re.split(r"\n## (연관된 노트|출처|연관된 글)", body)[0]
    return re.sub(r"\s+", " ", body).strip()[:n]


RELATION = Choice(
    instructions=(
        "`source` and `candidate` are two Korean notes, each stating one claim. "
        "What is the most specific relation between the claim of `source` and the claim of `candidate`?"
    ),
    criteria={
        "evidence": "One note gives a reason, cause, or evidence for the other's claim.",
        "application": "One note applies the other's claim to a concrete situation, practice, or case.",
        "tension": "The claims conflict, or one sets a limit or counterexample to the other.",
        "broader_narrower": "One claim is a general principle and the other is a special case or a component of it.",
        "same_topic_only": "Same topic, but no specific relation between the two claims.",
        "unrelated": "Different topics.",
    },
)
USEFUL = Noul(instructions=(
    "Would a reader of `source` gain something specific by following a link to `candidate`, "
    "because the two claims have a relation that can be stated in one sentence?"
))
links = json.load(open(f"{D}/exp3_links.json"))
pairs = [(x, c) for x in links for c in x["candidates"]]
cache = {}


def judge(pair):
    x, c = pair
    for n in (x["note"], c):
        cache.setdefault(n, excerpt(n, 1200))
    r = call({"source": {"title": x["note"], "text": cache[x["note"]]}, "candidate": {"title": c, "text": cache[c]}},
             {"relation": RELATION, "useful": USEFUL})
    a = r.choices["relation"]
    return {"note": x["note"], "candidate": c, "linked": c in x["linked"], "relation": a.choice,
            "confidence": a.confidence, "probabilities": dict(a.probabilities), "useful": r.nouls["useful"].noul}


t0 = time.time()
exp3 = pmap(judge, pairs)
json.dump(exp3, open(f"{D}/exp3_results.json", "w"), ensure_ascii=False, indent=1)
print(json.dumps({**usage, "cost_usd": round(usage["input_tokens"] * 0.042 / 1e6, 5),
                  "exp1": len(exp1), "exp2": len(exp2), "exp3_pairs": len(exp3)}))
