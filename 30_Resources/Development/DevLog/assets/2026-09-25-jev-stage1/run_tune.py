"""조정용 표본에만 Jev Noul을 돌린다. 최종 평가용은 읽지 않는다.

uv run --with typesafe-sdk python run_tune.py  (이 폴더에서 실행)
"""
import json, os, time
from concurrent.futures import ThreadPoolExecutor
from typesafe_sdk import Noul, TypeSafeClient

D = os.path.dirname(os.path.abspath(__file__))
q = json.load(open(f"{D}/question.json"))
items = [json.loads(l) for l in open(f"{D}/items.jsonl")]
tune = [x for x in items if x["split"] == "tune"]
client = TypeSafeClient()
Q = {"present": Noul(instructions=q["instructions"])}
tok, errors = [], []

def run(x):
    for attempt in range(3):
        try:
            t = time.time()
            res = client.system_one({q["state_key"]: x["text"]}, Q)
            tok.append(getattr(getattr(res, "usage", None), "input_tokens", 0) or 0)
            return {"id": x["id"], "sha256": x["sha256"], "p_present": res.nouls["present"].noul,
                    "seconds": round(time.time() - t, 3)}
        except Exception as e:
            last = repr(e)
            time.sleep(1 + attempt)
    errors.append({"id": x["id"], "error": last})
    return {"id": x["id"], "sha256": x["sha256"], "p_present": None, "error": last}

start = time.time()
with ThreadPoolExecutor(8) as ex:
    out = list(ex.map(run, tune))
meta = {"question_version": q["version"], "model": "jev-1.13.0", "split": "tune", "requests": len(out),
        "errors": len(errors), "input_tokens": sum(tok), "cost_usd": round(sum(tok) * 0.042 / 1e6, 6),
        "wall_seconds": round(time.time() - start, 2)}
json.dump({"meta": meta, "results": out}, open(f"{D}/runs/tune_{q['version']}_jev.json", "w"), ensure_ascii=False, indent=1)
print(json.dumps(meta, ensure_ascii=False))
