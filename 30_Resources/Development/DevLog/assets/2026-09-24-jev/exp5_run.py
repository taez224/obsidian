import json, os, time
from concurrent.futures import ThreadPoolExecutor
from typesafe_sdk import Noul, TypeSafeClient
D = os.path.dirname(os.path.abspath(__file__))
client = TypeSafeClient()
PREVIEW = Noul(instructions=(
    "Is the main job of the Korean sentence `sentence` to announce what the text, the post, or its next part will cover or do "
    "(for example 'in this post we will look at X', 'next, let us build Y', 'let us move on'), rather than stating information itself?"))
tok = [0]
def judge(r):
    for attempt in range(4):
        try:
            res = client.system_one({"sentence": r["sentence"]}, {"preview": PREVIEW})
            tok[0] += getattr(getattr(res, "usage", None), "input_tokens", 0) or 0
            return {**r, "preview": res.nouls["preview"].noul}
        except Exception as e:
            time.sleep(2 * (attempt + 1)); err = repr(e)
    return {**r, "preview": None, "error": err}
hold = json.load(open(f"{D}/exp5_holdout.json"))
unseen = json.load(open(f"{D}/exp5_unseen.json"))
t0 = time.time()
with ThreadPoolExecutor(8) as ex:
    h = list(ex.map(judge, hold))
    u = list(ex.map(judge, unseen))
json.dump(h, open(f"{D}/exp5_holdout_jev.json", "w"), ensure_ascii=False, indent=1)
json.dump(u, open(f"{D}/exp5_unseen_jev.json", "w"), ensure_ascii=False)
print(f"requests={len(h)+len(u)} errors={sum(1 for x in h+u if x.get('error'))} tokens={tok[0]} cost=${tok[0]*0.042/1e6:.4f} time={time.time()-t0:.0f}s")
