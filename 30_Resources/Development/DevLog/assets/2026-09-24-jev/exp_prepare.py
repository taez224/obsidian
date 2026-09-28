"""세 실험의 입력 데이터를 공개 노트에서만 추출한다. TypeSafe 호출 없음."""
import glob, json, os, random, re, subprocess

VAULT = "/Users/taez/Projects/obsidian"
OUT = os.path.dirname(__file__)
os.chdir(VAULT)


def split_fm(text):
    m = re.match(r"---\n(.*?)\n---\n?(.*)", text, re.S)
    return (m.group(1), m.group(2)) if m else ("", text)


def scalar(fm, k):
    m = re.search(rf"^{k}:\s*(.*)$", fm, re.M)
    return m.group(1).strip().strip("\"'") if m else ""


def prose_lines(body):
    """코드펜스를 뺀 본문 줄. 인라인 코드·링크 URL은 지운다."""
    out, fence = [], False
    for line in body.split("\n"):
        if line.strip().startswith("```"):
            fence = not fence
            continue
        if fence:
            out.append("")
            continue
        line = re.sub(r"`[^`]*`", "", line)
        line = re.sub(r"\]\([^)]*\)", "]", line)
        line = re.sub(r"\[\[([^\]|]*\|)?([^\]]*)\]\]", r"\2", line)
        out.append(line)
    return out


def sentences(text):
    return [s.strip() for s in re.split(r"(?<=[.!?다요죠])\s+", text) if s.strip()]


published = []
for p in sorted(glob.glob("20_Projects/blog/*.md")):
    fm, body = split_fm(open(p, encoding="utf-8").read())
    if scalar(fm, "status") == "published" and scalar(fm, "type") != "series":
        published.append((p, fm, body))

# 실험 1: "아니라/아니었/아닙니다" 출현마다 문장과 앞뒤 문장
occ = []
for p, fm, body in published:
    paras = [l for l in prose_lines(body) if l.strip() and not l.lstrip().startswith(("#", "|", "!"))]
    sents = [s for para in paras for s in sentences(para)]
    for i, s in enumerate(sents):
        if re.search(r"아니라|아니었|아닙니다", s):
            occ.append({"id": len(occ), "post": scalar(fm, "title") or os.path.basename(p)[:-3], "path": p,
                        "before": sents[i - 1] if i else "", "sentence": s,
                        "after": sents[i + 1] if i + 1 < len(sents) else ""})
random.seed(7)
sample_ids = sorted(random.sample(range(len(occ)), min(40, len(occ))))
json.dump(occ, open(f"{OUT}/exp1_occurrences.json", "w"), ensure_ascii=False, indent=1)
json.dump(sample_ids, open(f"{OUT}/exp1_sample_ids.json", "w"))

# 실험 2: 공개 개발 노트와 발행 글의 summary
DEV_TAIL = re.compile(r"(정리|확인|점검|설명|소개|다룬)한다\.?$")
summ = []
for p in sorted(glob.glob("30_Resources/Development/Concepts/*.md") + glob.glob("30_Resources/Development/Troubleshooting/*.md")
                + glob.glob("30_Resources/Development/Tools/*.md")):
    fm, _ = split_fm(open(p, encoding="utf-8").read())
    s = scalar(fm, "summary")
    if s:
        summ.append({"path": p, "kind": p.split("/")[2], "summary": s, "regex": bool(DEV_TAIL.search(s))})
for p, fm, _ in published:
    s = scalar(fm, "summary")
    if s:
        summ.append({"path": p, "kind": "Blog", "summary": s, "regex": bool(DEV_TAIL.search(s))})
json.dump(summ, open(f"{OUT}/exp2_summaries.json", "w"), ensure_ascii=False, indent=1)

# 실험 3: Slipbox permanent 노트 중 다른 Slipbox 노트로 링크 3개 이상인 것 8개, qmd 후보 15개
slip = {os.path.basename(p)[:-3]: p for p in glob.glob("01_Slipbox/*.md")}
cands = []
for name, p in sorted(slip.items()):
    fm, body = split_fm(open(p, encoding="utf-8").read())
    if scalar(fm, "type") != "permanent":
        continue
    links = {re.split(r"[|#]", l)[0] for l in re.findall(r"\[\[([^\]]+)\]\]", body)}
    linked = sorted(l for l in links if l in slip and l != name)
    if len(linked) >= 3:
        cands.append((name, p, body, linked))
random.seed(11)
chosen = random.sample(cands, 8)
exp3 = []
for name, p, body, linked in chosen:
    first = re.sub(r"\s+", " ", "\n".join(l for l in body.split("\n") if l.strip() and not l.startswith("#"))[:400])
    r = subprocess.run(["qmd", "vsearch", f"{name} {first}", "-n", "30", "--json", "-c", "PKM"], capture_output=True, text=True)
    hits, seen = [], set()
    for h in json.loads(r.stdout or "[]"):
        f = h["file"].replace("qmd://PKM/", "")
        n = os.path.basename(f)[:-3]
        if f.startswith("01_Slipbox/") and n != name and n not in seen and n in slip:
            seen.add(n)
            hits.append(n)
    exp3.append({"note": name, "path": p, "linked": linked, "candidates": hits[:15]})
json.dump(exp3, open(f"{OUT}/exp3_links.json", "w"), ensure_ascii=False, indent=1)

print(f"exp1 occurrences={len(occ)} sample={len(sample_ids)}")
print(f"exp2 summaries={len(summ)} regex_flagged={sum(x['regex'] for x in summ)}")
print(f"exp3 notes={len(exp3)} candidates={[len(x['candidates']) for x in exp3]} "
      f"linked_in_candidates={[len(set(x['linked']) & set(x['candidates'])) for x in exp3]}/{[len(x['linked']) for x in exp3]}")
