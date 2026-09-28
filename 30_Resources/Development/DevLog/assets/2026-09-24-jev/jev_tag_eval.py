"""Jev 태그 정확도 실험: 공개 노트(Slipbox 전체 + 발행된 블로그 글)의 첫 태그를 정답으로 삼는다."""
import json, os, re, sys, time, glob
from concurrent.futures import ThreadPoolExecutor
from typesafe_sdk import Choice, TypeSafeClient

VAULT = "/Users/taez/Projects/obsidian"
OUT = os.path.join(os.path.dirname(__file__), "jev_results.json")
HIDDEN = {"slipbox", "blog", "inbox", "clippings"}

TOPICS = {
    "AI": "Artificial intelligence: LLMs, AI agents, prompting, and how people and teams work with AI tools.",
    "개발": "Software development: languages, frameworks, infrastructure, design, code quality, engineering methods.",
    "커리어": "Career and self-development: growth, skills and learning, self-management, motivation, job changes, seniority.",
    "조직": "Organizations: delegation, hiring, team performance, leadership; principles that still hold without AI.",
    "심리": "Psychology and self-understanding, including personality tests such as HEXACO or MBTI.",
    "철학": "Philosophy and judgment: by what standard one weighs and chooses, values, ways of thinking.",
    "글쓰기": "Writing and communication: how to write, edit, and convey ideas.",
    "지식관리": "Personal knowledge management: Obsidian, PARA, Zettelkasten, note-taking systems.",
    "none_of_the_above": "The note fits none of the topics above.",
}


def parse(path):
    text = open(path, encoding="utf-8").read()
    m = re.match(r"---\n(.*?)\n---\n?(.*)", text, re.S)
    if not m:
        return None
    fm, body = m.groups()
    tags = []
    tm = re.search(r"^tags:\s*\n((?:[ \t]+-.*\n?)+)", fm + "\n", re.M)
    if tm:
        tags = [x.strip()[1:].strip().strip("\"'") for x in tm.group(1).splitlines() if x.strip().startswith("-")]
    scalar = lambda k: (re.search(rf"^{k}:\s*(.*)$", fm, re.M) or [None, ""])[1].strip().strip("\"'")
    return {"tags": tags, "status": scalar("status"), "type": scalar("type"),
            "title": scalar("title") or os.path.basename(path)[:-3], "summary": scalar("summary"), "body": body}


def clean(body):
    body = re.sub(r"%%.*?%%", "", body, flags=re.S)
    body = re.sub(r"!\[\[[^\]]*\]\]", "", body)
    body = re.sub(r"\[\[([^\]|#]*)(?:#[^\]|]*)?\|([^\]]*)\]\]", r"\2", body)
    body = re.sub(r"\[\[([^\]|#]*)(?:#[^\]]*)?\]\]", r"\1", body)
    body = re.sub(r"\^[\w-]+\s*$", "", body, flags=re.M)
    return re.sub(r"\n{3,}", "\n\n", body).strip()[:2000]


notes = []
for path in sorted(glob.glob(f"{VAULT}/01_Slipbox/*.md") + glob.glob(f"{VAULT}/20_Projects/blog/*.md")):
    n = parse(path)
    if not n:
        continue
    if "/20_Projects/blog/" in path and (n["status"] != "published" or n["type"] == "series"):
        continue
    public = [t for t in n["tags"] if t not in HIDDEN and not t.startswith("프로젝트/")]
    if not public:
        continue
    n.update(path=path[len(VAULT) + 1:], first_tag=public[0], topic=public[0].split("/")[0])
    notes.append(n)

first_tags = sorted({n["first_tag"] for n in notes})
tag_criteria = {}
for t in first_tags:
    top, _, sub = t.partition("/")
    base = TOPICS.get(top, top)
    tag_criteria[t] = base if not sub else f"Subtopic '{sub}' within: {base}"
tag_criteria["none_of_the_above"] = TOPICS["none_of_the_above"]

questions = {
    "topic": Choice(
        instructions="Which topic is this note's main claim about? Judge by what the note argues, not by words it merely mentions. The note is written in Korean.",
        criteria=TOPICS,
    ),
    "first_tag": Choice(
        instructions="Which tag best names the axis this note's main claim belongs to? Judge by what the note argues, not by words it merely mentions. The note is written in Korean.",
        criteria=tag_criteria,
    ),
}

client = TypeSafeClient()


def run(n):
    state = {"title": n["title"], "summary": n["summary"], "body_excerpt": clean(n["body"])}
    t0 = time.time()
    r = client.system_one(state, questions)
    dt = time.time() - t0
    out = {"path": n["path"], "gold_topic": n["topic"], "gold_tag": n["first_tag"], "latency": dt,
           "input_tokens": r.usage.input_tokens if getattr(r, "usage", None) else None}
    for q in ("topic", "first_tag"):
        a = r.choices[q]
        out[q] = {"choice": a.choice, "confidence": a.confidence, "probabilities": dict(a.probabilities)}
    return out


print(f"notes={len(notes)} first_tags={len(first_tags)}", file=sys.stderr)
with ThreadPoolExecutor(8) as ex:
    results = list(ex.map(run, notes))
json.dump(results, open(OUT, "w"), ensure_ascii=False, indent=1)
print(f"saved {OUT}", file=sys.stderr)
