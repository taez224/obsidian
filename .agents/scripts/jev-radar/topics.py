"""요즘 관심사: `_workspace/radar/관심사.md`에 적은 주제를 찾아오고, 주제 여부와 활용 사례 여부를 판정한다.

후보는 코드가 모은다(이미 수집한 글 중 검색어가 든 것 + 관심사별 HN·arXiv·GitHub 검색).
Jev는 "정말 이 주제인가"와 "실제로 만들거나 적용한 사례인가"만 판단하고, 순위는 화제성 숫자로 코드가 정한다.
외부로는 관심사의 이름·설명·검색어와 공개 글의 제목·요약만 나간다.

미리보기: uv run --with typesafe-sdk --with feedparser python .agents/scripts/jev-radar/topics.py
"""
import json
import re
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path


DEFAULT = dict(enabled=True, about_floor=0.7, case_floor=0.7, per_source=3, hn_min_points=5, github_min_stars=5)
ORDER = ["Hacker News", "GitHub", "arXiv"]  # 나머지 출처는 이 뒤에 온다
UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) jev-radar"}
ATOM = "{http://www.w3.org/2005/Atom}"
LINE = re.compile(r"^-\s+([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*검색어:\s*(.+?)\s*$")


def load_topics(path):
    topics = []
    if not path.exists():
        return topics
    for line in path.read_text().splitlines():
        m = LINE.match(line.strip())
        if m:
            terms = [t.strip() for t in m.group(3).split(",") if t.strip()]
            topics.append({"name": m.group(1), "desc": m.group(2), "terms": terms})
    return topics


def _get(url, timeout=60):
    return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=timeout).read()


def search_hn(term, since, min_points):
    q = urllib.parse.urlencode({"query": term, "tags": "story", "hitsPerPage": 100,
                                "numericFilters": f"created_at_i>{since},points>={min_points}"})
    hits = json.loads(_get(f"https://hn.algolia.com/api/v1/search?{q}"))["hits"]
    return [{"source": "Hacker News", "title": h["title"], "summary": re.sub(r"<[^>]+>", " ", h.get("story_text") or ""),
             "url": h.get("url") or f"https://news.ycombinator.com/item?id={h['objectID']}",
             "points": h.get("points") or 0} for h in hits]


def search_arxiv(term, since, now):
    span = f"{time.strftime('%Y%m%d%H%M', time.gmtime(since))}+TO+{time.strftime('%Y%m%d%H%M', time.gmtime(now))}"
    q = urllib.parse.quote(f'all:"{term}"')
    root = ET.fromstring(_get(f"https://export.arxiv.org/api/query?search_query={q}+AND+submittedDate:%5B{span}%5D&max_results=100", 120))
    return [{"source": "arXiv", "title": " ".join(e.find(f"{ATOM}title").text.split()),
             "summary": " ".join(e.find(f"{ATOM}summary").text.split())[:1500],
             "url": e.find(f"{ATOM}id").text, "points": 0} for e in root.findall(f"{ATOM}entry")]


_last_github = [0.0]


def search_github(term, since, min_stars):
    wait = 7 - (time.time() - _last_github[0])  # 인증 없는 검색 API는 분당 10회
    if wait > 0:
        time.sleep(wait)
    _last_github[0] = time.time()
    day = time.strftime("%Y-%m-%d", time.gmtime(since))
    q = urllib.parse.quote(f"{term} created:>={day}")
    data = json.loads(_get(f"https://api.github.com/search/repositories?q={q}&sort=stars&order=desc&per_page=30"))
    return [{"source": "GitHub", "title": r["full_name"], "summary": r.get("description") or "",
             "url": r["html_url"], "points": r.get("stargazers_count") or 0} for r in data.get("items", [])
            if (r.get("stargazers_count") or 0) >= min_stars]


def candidates(topic, pool, since, now, cfg, norm, skip, failures):
    """검색어가 든 수집 자료와 관심사별 검색 결과를 합친다. 이미 보여 준 글은 뺀다."""
    pat = re.compile("|".join(rf"\b{re.escape(t)}\b" for t in topic["terms"]), re.I)
    found = [{**x, "points": x.get("points") or 0} for x in pool if pat.search(f"{x['title']} {x.get('summary', '')[:1500]}")]
    for term in topic["terms"]:
        for name, fn in (("HN", lambda: search_hn(term, since, cfg["hn_min_points"])),
                         ("arXiv", lambda: search_arxiv(term, since, now)),
                         ("GitHub", lambda: search_github(term, since, cfg["github_min_stars"]))):
            try:
                found += fn()
            except Exception as e:
                failures.append(f"{topic['name']} {name} 검색({term}): {type(e).__name__}")
    out, seen = [], set()
    for x in found:
        u = norm(x["url"])
        if u in seen or u in skip:
            continue
        seen.add(u)
        out.append(x)
    return out


def judge(topic, items, client):
    from typesafe_sdk import Noul  # 판정할 때만 필요하다. 목록 읽기와 테스트는 SDK 없이 돈다

    q = {
        "about": Noul(instructions=f"Is this item mainly about {topic['name']} ({topic['desc']}), not a different thing that shares the name?"),
        "case": Noul(instructions=f"Does this item show a concrete project, tool, experiment, benchmark, or real-world use built with or applied to "
                                  f"{topic['name']}, rather than only news, an announcement, or opinion?"),
    }
    tokens = []

    def run(x):
        try:
            r = client.system_one({"title": x["title"], "summary": (x.get("summary") or "")[:3000]}, q)
            tokens.append(getattr(getattr(r, "usage", None), "input_tokens", 0) or 0)
            return {**x, "about": r.nouls["about"].noul, "case": r.nouls["case"].noul}
        except Exception:
            return {**x, "about": 0, "case": 0}

    with ThreadPoolExecutor(8) as ex:
        return list(ex.map(run, items)), sum(tokens)


def per_source(items, n, tiebreak):
    """출처마다 따로 상위 n건. HN 점수와 GitHub 별 수는 크기가 달라 한 순위표에 섞지 않는다."""
    out = []
    for src in ORDER + sorted({x["source"] for x in items} - set(ORDER)):
        group = sorted((x for x in items if x["source"] == src), key=lambda x: (-x["points"], -x[tiebreak]))
        out += group[:n]
    return out


def make_sections(interest_path, pool, since, now, client, config, norm, skip):
    cfg = {**DEFAULT, **config.get("topics", {})}
    failures, lines, shown, tokens = [], [], set(), 0
    for topic in load_topics(interest_path):
        judged, t = judge(topic, candidates(topic, pool, since, now, cfg, norm, skip, failures), client)
        tokens += t
        on = [x for x in judged if x["about"] >= cfg["about_floor"]]
        cases = per_source([x for x in on if x["case"] >= cfg["case_floor"]], cfg["per_source"], "case")
        news = per_source([x for x in on if x["case"] < cfg["case_floor"]], cfg["per_source"], "about")
        pop = lambda x: f"{x['points']}점 · " if x["source"] == "Hacker News" else (f"★{x['points']} · " if x["source"] == "GitHub" else "")
        lines += [f"## 요즘 관심사: {topic['name']}", "",
                  f"후보 {len(judged)}건 중 이 주제로 판정된 {len(on)}건. 활용 사례를 먼저, 화제성(HN 점수·GitHub 별) 순으로 보였다.", "",
                  "### 활용 사례", ""]
        lines += [f"- [ ] {pop(x)}[{x['title']}]({x['url']}) - {x['source']}" for x in cases] or ["- 없음"]
        lines += ["", "### 소식·논의", ""]
        lines += [f"- [ ] {pop(x)}[{x['title']}]({x['url']}) - {x['source']}" for x in news] or ["- 없음"]
        lines.append("")
        shown |= {norm(x["url"]) for x in cases + news}
    return "\n".join(lines), shown, tokens, failures


if __name__ == "__main__":
    import os, subprocess, sys
    from typesafe_sdk import TypeSafeClient
    here = Path(__file__).resolve().parent
    sys.path.insert(0, str(here))
    import radar
    if not os.environ.get("TYPESAFE_API_KEY"):
        radar.api_key()
    vault = here.parents[2]
    pool = json.loads((vault / "_workspace/radar" / sys.argv[1]).read_text())["scored"] if len(sys.argv) > 1 else []
    text, shown, tokens, failures = make_sections(vault / "_workspace/radar/관심사.md", pool, radar.SINCE, radar.NOW,
                                                  TypeSafeClient(), radar.CONFIG, radar.norm_url, set())
    print(text)
    print(f"(${tokens * 0.042 / 1e6:.4f}, 실패 {failures})", file=sys.stderr)
