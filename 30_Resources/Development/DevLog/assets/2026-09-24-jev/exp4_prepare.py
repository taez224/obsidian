"""실험 4 입력: 발행 글 문장에서 단서어가 있는 30개와 없는 30개를 뽑는다. TypeSafe 호출 없음."""
import json, os, random, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import glob

VAULT = "/Users/taez/Projects/obsidian"
OUT = os.path.dirname(os.path.abspath(__file__))
os.chdir(VAULT)
exec(open(f"{OUT}/exp_prepare.py").read().split("published = []")[0])  # split_fm, scalar, prose_lines, sentences

CUE = re.compile(r"(살펴보|알아보|다뤄\s?보|다루겠|다룹니다|이야기해\s?보|소개하겠|설명하겠|정리하면|정리해\s?보|요약하면|앞서|앞에서|위에서|"
                 r"다시 말해|이 글에서|이번 글|다음 글|다음으로|이제|부르겠|부르기로|정의하겠|라고 부르|이라 부르)")

rows = []
for p in sorted(glob.glob("20_Projects/blog/*.md")):
    fm, body = split_fm(open(p, encoding="utf-8").read())
    if scalar(fm, "status") != "published" or scalar(fm, "type") == "series":
        continue
    paras = [l for l in prose_lines(body) if l.strip() and not l.lstrip().startswith(("#", "|", "!", "^"))]
    sents = [re.sub(r"\*\*|\s\^[\w-]+$", "", s) for para in paras for s in sentences(para)]
    for i, s in enumerate(sents):
        if 15 <= len(s) <= 220:
            rows.append({"post": scalar(fm, "title") or os.path.basename(p)[:-3],
                         "before": " ".join(sents[max(0, i - 2):i])[-400:], "sentence": s, "cue": bool(CUE.search(s))})
random.seed(23)
cued = [r for r in rows if r["cue"]]
plain = [r for r in rows if not r["cue"]]
sample = random.sample(cued, 30) + random.sample(plain, 30)
random.shuffle(sample)
for i, r in enumerate(sample):
    r["id"] = i
json.dump(sample, open(f"{OUT}/exp4_sample.json", "w"), ensure_ascii=False, indent=1)
print(f"sentences={len(rows)} cued={len(cued)} plain={len(plain)} sample={len(sample)}")
for r in sample:
    print(f"[{r['id']}]{'C' if r['cue'] else ' '} ({r['post'][:18]}) 앞: …{r['before'][-110:]}\n     ★ {r['sentence']}")
