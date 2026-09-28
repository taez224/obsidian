"""첫 공개 태그가 AI 계열인 커밋된 공개 노트에 새 AI 태그 기준을 묻는다. 노트는 수정하지 않는다."""
import glob, json, os, re, subprocess
from concurrent.futures import ThreadPoolExecutor
from typesafe_sdk import Choice, Noul, TypeSafeClient

VAULT = "/Users/taez/Projects/obsidian"
D = os.path.dirname(os.path.abspath(__file__))
HIDDEN = {"slipbox", "blog", "inbox", "clippings"}
tracked = set(subprocess.run(["git", "-C", VAULT, "ls-files"], capture_output=True, text=True).stdout.splitlines())


def parse(p):
    t = open(p, encoding="utf-8").read()
    m = re.match(r"---\n(.*?)\n---\n?(.*)", t, re.S)
    if not m:
        return None
    fm, body = m.groups()
    tm = re.search(r"^tags:\s*\n((?:[ \t]+-.*\n?)+)", fm + "\n", re.M)
    tags = [x.strip()[1:].strip().strip("\"'") for x in tm.group(1).splitlines() if x.strip().startswith("-")] if tm else []
    get = lambda k: (re.search(rf"^{k}:\s*(.*)$", fm, re.M) or [None, ""])[1].strip().strip("\"'")
    body = re.split(r"\n## (출처|연관된 노트|연관된 글|참고 자료)\b", body)[0]
    body = re.sub(r"\[\[([^\]|]*\|)?([^\]]*)\]\]", r"\2", body)
    body = re.sub(r"```.*?```", "", body, flags=re.S)
    return {"tags": tags, "status": get("status"), "type": get("type"), "title": get("title") or os.path.basename(p)[:-3],
            "summary": get("summary"), "body": re.sub(r"\n{3,}", "\n\n", body).strip()[:2000]}


notes = []
paths = glob.glob(f"{VAULT}/01_Slipbox/*.md") + glob.glob(f"{VAULT}/20_Projects/blog/*.md") + \
    glob.glob(f"{VAULT}/30_Resources/Development/Concepts/*.md") + glob.glob(f"{VAULT}/30_Resources/Development/Troubleshooting/*.md") + \
    glob.glob(f"{VAULT}/30_Resources/Development/Tools/*.md")
for p in sorted(paths):
    rel = p[len(VAULT) + 1:]
    if rel not in tracked:
        continue  # 커밋되지 않은 초안은 보내지 않는다
    n = parse(p)
    if not n:
        continue
    if rel.startswith("20_Projects/blog/") and (n["status"] != "published" or n["type"] == "series"):
        continue
    public = [t for t in n["tags"] if t not in HIDDEN and not t.startswith("프로젝트/")]
    if public and public[0].split("/")[0] == "AI":
        n.update(path=rel, first_tag=public[0], second_tag=public[1] if len(public) > 1 else "")
        notes.append(n)

AI_ESSENTIAL = Noul(instructions=(
    "Would the central claim of this Korean note stop making sense if AI were taken out of it? "
    "Answer yes if the claim is specifically about AI tools, AI models, or how people work with AI. "
    "Answer no if the claim is a general principle about organizations, careers, judgment, writing, knowledge management, "
    "or software that the note only applies to or illustrates with AI."))
OTHER_AXIS = Choice(
    instructions="Suppose every mention of AI were removed from this Korean note. Which topic would its central claim belong to?",
    criteria={
        "개발": "Software development: languages, frameworks, infrastructure, design, code quality, engineering methods.",
        "커리어": "Career and self-development: growth, skills and learning, self-management, motivation, job changes, seniority.",
        "조직": "Organizations: delegation, hiring, team performance, leadership; principles that hold without AI.",
        "심리": "Psychology and self-understanding through psychological concepts or tests.",
        "철학": "Philosophy and judgment: by what standard one weighs and chooses, values, ways of thinking.",
        "글쓰기": "Writing and communication: how to write, edit, and convey ideas.",
        "지식관리": "Personal knowledge management: Obsidian, PARA, Zettelkasten, note-taking systems.",
        "nothing_left": "Nothing meaningful remains: the claim only exists because of AI.",
    },
)
client = TypeSafeClient()


def run(n):
    r = client.system_one({"title": n["title"], "summary": n["summary"], "body_excerpt": n["body"]},
                          {"ai_essential": AI_ESSENTIAL, "other_axis": OTHER_AXIS})
    a = r.choices["other_axis"]
    return {k: v for k, v in n.items() if k not in ("body",)} | {
        "ai_essential": r.nouls["ai_essential"].noul, "other_axis": a.choice, "other_conf": a.confidence,
        "other_probs": dict(a.probabilities)}


with ThreadPoolExecutor(8) as ex:
    out = list(ex.map(run, notes))
json.dump(out, open(f"{D}/exp7_results.json", "w"), ensure_ascii=False, indent=1)
print(f"notes={len(out)}")
for r in sorted(out, key=lambda r: r["ai_essential"]):
    print(f"  ai={r['ai_essential']:.2f} other={r['other_axis']}({r['other_conf']:.2f}) tags=[{r['first_tag']}, {r['second_tag']}] {r['path'].split('/')[0][:2]} {r['title'][:48]}")
