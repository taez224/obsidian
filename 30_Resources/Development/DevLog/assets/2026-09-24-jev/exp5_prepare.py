"""검증용 데이터: 설계에 쓰지 않은 발행 글 문장 40개와 초안 summary. 정규식·Jev 결과는 출력하지 않는다."""
import glob, json, os, random, re

D = os.path.dirname(os.path.abspath(__file__))
os.chdir("/Users/taez/Projects/obsidian")
exec(open(f"{D}/exp_prepare.py").read().split("published = []")[0])  # split_fm, scalar, prose_lines, sentences
CUE = re.compile(r"(살펴보|알아보|다뤄\s?보|다루겠|다룹니다|이야기해\s?보|소개하겠|설명하겠|정리하면|정리해\s?보|요약하면|앞서|앞에서|위에서|"
                 r"다시 말해|이 글에서|이번 글|다음 글|다음으로|이제|부르겠|부르기로|정의하겠|라고 부르|이라 부르)")

rows = []
drafts = []
for p in sorted(glob.glob("20_Projects/blog/*.md")):
    fm, body = split_fm(open(p, encoding="utf-8").read())
    if scalar(fm, "type") == "series":
        continue
    if scalar(fm, "status") != "published":
        if scalar(fm, "summary"):
            drafts.append({"path": p, "summary": scalar(fm, "summary")})
        continue
    paras = [l for l in prose_lines(body) if l.strip() and not l.lstrip().startswith(("#", "|", "!", "^"))]
    sents = [re.sub(r"\*\*|\s\^[\w-]+$", "", s) for para in paras for s in sentences(para)]
    for i, s in enumerate(sents):
        if 15 <= len(s) <= 220:
            rows.append({"post": scalar(fm, "title") or os.path.basename(p)[:-3], "sentence": s, "cue": bool(CUE.search(s))})

used = {r["sentence"] for r in json.load(open(f"{D}/exp4_sample.json"))}
unseen = [r for r in rows if r["sentence"] not in used]
random.seed(97)
cued = [r for r in unseen if r["cue"]]
plain = [r for r in unseen if not r["cue"]]
hold = random.sample(cued, 20) + random.sample(plain, 20)
random.shuffle(hold)
for i, r in enumerate(hold):
    r["id"] = i
json.dump(hold, open(f"{D}/exp5_holdout.json", "w"), ensure_ascii=False, indent=1)
json.dump(unseen, open(f"{D}/exp5_unseen.json", "w"), ensure_ascii=False)
json.dump(drafts, open(f"{D}/exp5_drafts.json", "w"), ensure_ascii=False, indent=1)
print(f"unseen={len(unseen)} holdout={len(hold)} drafts_with_summary={len(drafts)}")
for r in hold:
    print(f"[{r['id']}] {r['sentence']}")
print("---- draft summaries")
for i, d in enumerate(drafts):
    print(f"<{i}> {d['summary']}")
