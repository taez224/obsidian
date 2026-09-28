import json, os
from concurrent.futures import ThreadPoolExecutor
from typesafe_sdk import Noul, TypeSafeClient
D = os.path.dirname(os.path.abspath(__file__))
client = TypeSafeClient()
Q = {
    "preview": Noul(instructions=(
        "Is the main job of the Korean sentence `sentence` to announce what the text, the post, or its next part will cover or do "
        "(for example 'in this post we will look at X', 'next, let us build Y', 'let us move on'), rather than stating information itself?")),
    "recap": Noul(instructions=(
        "Does the Korean sentence `sentence` only restate something already said in `before`, adding no new information?")),
    "define": Noul(instructions=(
        "Does the Korean sentence `sentence` announce that the writer will call or define a term in a certain way from now on "
        "(for example 'from now on I will call this X')? Reporting a name that someone else uses does not count.")),
}
sample = json.load(open(f"{D}/exp4_sample.json"))
tok = []
def run(r):
    res = client.system_one({"before": r["before"], "sentence": r["sentence"]}, Q)
    tok.append(getattr(getattr(res, "usage", None), "input_tokens", 0) or 0)
    return {**r, **{k: res.nouls[k].noul for k in Q}}
with ThreadPoolExecutor(8) as ex:
    out = list(ex.map(run, sample))
json.dump(out, open(f"{D}/exp4_results.json", "w"), ensure_ascii=False, indent=1)
print(f"requests={len(out)} tokens={sum(tok)} cost=${sum(tok)*0.042/1e6:.5f}")
