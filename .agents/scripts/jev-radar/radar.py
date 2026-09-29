"""Jev 주간 레이더: 양이 많은 출처는 Slipbox 관심 질문으로 거르고, 믿고 보는 저자는 그대로 모은다.

결과는 _workspace/radar/<실행일>.md에 쓴다. 이미 자료카드로 저장했거나 지난 목록에 올린 글은 뺀다.
launchd(~/Library/LaunchAgents/com.taez.jev-radar.plist)가 매주 토요일 08:00에 실행한다.

수동 실행: uv run --with typesafe-sdk --with feedparser python .agents/scripts/jev-radar/radar.py
"""
import calendar, html, json, os, re, subprocess, sys, time, urllib.parse, urllib.request
import xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import feedparser
from typesafe_sdk import Noul, TypeSafeClient

HERE = Path(__file__).resolve().parent
VAULT = HERE.parents[2]
OUT = VAULT / "_workspace" / "radar"
CONFIG = json.loads((HERE / "config.json").read_text())
UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) jev-radar"}
NOW = int(time.time())
SINCE = NOW - 7 * 86400
PRICE_PER_M = 0.042


def text(s, n=1500):
    s = html.unescape(re.sub(r"<[^>]+>", " ", s or ""))
    return " ".join(s.split())[:n]


def norm_url(u):
    """같은 글을 같은 주소로 본다. arXiv API는 http와 버전(v1)을 붙여 준다."""
    u = (u or "").split("#")[0].rstrip("/")
    u = re.sub(r"^https?://(www\.)?", "https://", u)
    return re.sub(r"(arxiv\.org/abs/\d{4}\.\d{4,5})v\d+$", r"\1", u)


def get(url, timeout=60):
    try:
        return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=timeout).read()
    except (TimeoutError, urllib.error.URLError):
        time.sleep(15)  # 깨어난 직후처럼 잠깐 끊긴 경우가 많아 한 번만 다시 시도한다
        return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=timeout).read()


def rss(source, url):
    feed = feedparser.parse(get(url))
    out = []
    for e in feed.entries:
        t = e.get("published_parsed") or e.get("updated_parsed")
        ts = calendar.timegm(t) if t else None
        if not ts or ts < SINCE:
            continue
        body = e.get("summary") or (e.get("content") or [{}])[0].get("value", "")
        link = e.get("link") or ""
        if link.startswith("/"):  # HBR 피드는 상대 경로를 준다
            link = CONFIG.get("link_base", {}).get(source, "") + link
        out.append({"source": source, "title": text(e.get("title"), 300), "summary": text(body),
                    "url": link, "date": time.strftime("%Y-%m-%d", time.gmtime(ts))})
    return out


def hacker_news():
    q = urllib.parse.urlencode({"tags": "story", "hitsPerPage": 1000,
                                "numericFilters": f"created_at_i>{SINCE},points>{CONFIG['hacker_news_min_points']}"})
    hits = json.loads(get(f"https://hn.algolia.com/api/v1/search_by_date?{q}"))["hits"]
    return [{"source": "Hacker News", "title": h["title"], "summary": text(h.get("story_text") or ""),
             "url": h.get("url") or f"https://news.ycombinator.com/item?id={h['objectID']}",
             "date": h["created_at"][:10], "points": h.get("points") or 0} for h in hits]


def hf_papers():
    """Hugging Face Daily Papers. 추천 수가 화제성 신호다."""
    out = []
    for d in range(8):
        day = time.strftime("%Y-%m-%d", time.gmtime(NOW - d * 86400))
        for x in json.loads(get(f"https://huggingface.co/api/daily_papers?date={day}&limit=100")):
            p = x["paper"]
            out.append({"source": "Hugging Face Papers", "title": p["title"], "url": f"https://huggingface.co/papers/{p['id']}",
                        "date": day, "points": p.get("upvotes") or 0})
    return out


def arxiv():
    ns = {"a": "http://www.w3.org/2005/Atom"}
    cats = "+OR+".join(f"cat:{c}" for c in CONFIG["arxiv"]["categories"])
    span = f"{time.strftime('%Y%m%d%H%M', time.gmtime(SINCE))}+TO+{time.strftime('%Y%m%d%H%M', time.gmtime(NOW))}"
    out, start = [], 0
    while True:
        url = (f"https://export.arxiv.org/api/query?search_query=({cats})+AND+submittedDate:%5B{span}%5D"
               f"&start={start}&max_results=1000&sortBy=submittedDate&sortOrder=descending")
        entries = ET.fromstring(get(url, 120)).findall("a:entry", ns)
        for e in entries:
            out.append({"source": "arXiv", "title": " ".join(e.find("a:title", ns).text.split()),
                        "summary": " ".join(e.find("a:summary", ns).text.split())[:1500],
                        "url": e.find("a:id", ns).text, "date": e.find("a:published", ns).text[:10]})
        if len(entries) < 1000:
            return out
        start += 1000
        time.sleep(3)


def saved_sources():
    """자료카드로 이미 저장한 URL."""
    urls = set()
    for p in (VAULT / "30_Resources" / "References").rglob("*.md"):
        m = re.search(r"^source:\s*(\S+)", p.read_text(errors="ignore")[:3000], re.M)
        if m:
            urls.add(norm_url(m.group(1).strip("\"'")))
    from reading import source_aliases
    urls.update(source_aliases(VAULT))
    return urls


def api_key():
    if os.environ.get("TYPESAFE_API_KEY"):
        return
    key = subprocess.run(["security", "find-generic-password", "-a", os.environ.get("USER", ""), "-s", "TYPESAFE_API_KEY", "-w"],
                         capture_output=True, text=True).stdout.strip()
    if not key:
        sys.exit("TYPESAFE_API_KEY를 키체인에서 읽지 못했다")
    os.environ["TYPESAFE_API_KEY"] = key


def notify(message):
    subprocess.run(["osascript", "-e", f'display notification "{message}" with title "Jev 레이더"'], capture_output=True)


def main():
    api_key()
    OUT.mkdir(parents=True, exist_ok=True)
    state_path = OUT / "state.json"
    state = json.loads(state_path.read_text()) if state_path.exists() else {"shown": []}
    state["shown"] = sorted({norm_url(u) for u in state["shown"]})
    skip = saved_sources() | set(state["shown"])

    failures, trusted, pool = [], [], []
    feedback_added = []
    try:  # 지난 목록의 체크박스와 반응 표시를 먼저 기록한다
        from claims import import_checkbox_feedback
        feedback_added = import_checkbox_feedback(OUT)
    except Exception as e:
        failures.append(f"반응 기록: {type(e).__name__}: {e}")
    for name, fn in [("arXiv", arxiv), ("Hacker News", hacker_news)] + \
                    [(s, (lambda s=s, u=u: rss(s, u))) for s, u in CONFIG["filtered"].items()]:
        try:
            pool += fn()
        except Exception as e:
            failures.append(f"{name}: {e!r}")
    for s, u in CONFIG["trusted"].items():
        try:
            trusted += rss(s, u)
        except Exception as e:
            failures.append(f"{s}: {e!r}")
    trend = CONFIG["trend"]
    papers, community, official, digest = [], [], [], []
    for name, fn in [("Hugging Face Papers", hf_papers)] + \
                    [(s, (lambda s=s, u=u: rss(s, u))) for s, u in trend["community"].items()] + \
                    [(s, (lambda s=s, u=u: rss(s, u))) for s, u in trend["official"].items()] + \
                    [(s, (lambda s=s, u=u: rss(s, u))) for s, u in trend["digest"].items()]:
        try:
            got = fn()
        except Exception as e:
            failures.append(f"{name}: {e!r}")
            continue
        if name == "Hugging Face Papers":
            papers = got
        elif name in trend["community"]:
            community += got[: trend["community_top"]]  # 주간 상위 RSS라 앞에서부터 자른다
        elif name in trend["official"]:
            official += got
        else:
            digest += [x for x in got if trend["digest_match"] in x["url"]]
    pool = [x for x in pool if norm_url(x["url"]) not in skip]
    trusted = [x for x in trusted if norm_url(x["url"]) not in skip]

    interests = CONFIG["interests"]
    questions = {k: Noul(instructions=v["question"]) for k, v in interests.items()}
    questions["is_ai"] = Noul(instructions=trend["is_ai_question"])
    client, tokens = TypeSafeClient(), []

    def judge(x):
        for attempt in range(3):
            try:
                res = client.system_one({"title": x["title"], "summary": x["summary"]}, questions)
                tokens.append(getattr(getattr(res, "usage", None), "input_tokens", 0) or 0)
                return {**x, **{k: res.nouls[k].noul for k in questions}}
            except Exception as e:
                last = repr(e)
                time.sleep(1 + attempt)
        return {**x, "error": last}

    started = time.time()
    with ThreadPoolExecutor(8) as ex:
        scored = list(ex.map(judge, pool))
    # 요약이 짧은 출처는 가능성 있는 글만 본문을 가져와 다시 판정한다
    ff = CONFIG.get("fetch_full", {})
    if ff.get("sources"):
        try:
            from backlog import cached_text, DEFAULT as BACKLOG_DEFAULT
            bcfg = {**BACKLOG_DEFAULT, **CONFIG.get("backlog", {})}
            cache = OUT / "backlog-cache"
            cache.mkdir(parents=True, exist_ok=True)
            idx = [i for i, x in enumerate(scored) if x["source"] in ff["sources"] and "error" not in x
                   and max(x.get(k, 0) for k in interests) >= ff.get("floor", 0.5)]

            def deepen(i):
                x = scored[i]
                c = cached_text({"url": x["url"]}, cache, bcfg)
                return judge({**x, "summary": c["text"][:6000]}) if len(c["text"]) >= bcfg["min_chars"] else x

            with ThreadPoolExecutor(4) as ex:
                for i, y in zip(idx, ex.map(deepen, idx)):
                    scored[i] = y
        except Exception as e:
            failures.append(f"본문 다시 판정: {type(e).__name__}: {e}")
    errors = [x for x in scored if "error" in x]
    release_q = {"release": Noul(instructions=trend["release_question"])}

    def judge_release(x):
        try:
            res = client.system_one({"title": x["title"], "summary": x["summary"]}, release_q)
            tokens.append(getattr(getattr(res, "usage", None), "input_tokens", 0) or 0)
            return {**x, "release": res.nouls["release"].noul}
        except Exception as e:
            return {**x, "release": 0, "error": repr(e)}

    with ThreadPoolExecutor(8) as ex:
        official = [x for x in ex.map(judge_release, official) if x["release"] >= CONFIG["threshold"]]
    hn_ai = sorted((x for x in scored if x["source"] == "Hacker News" and x.get("is_ai", 0) >= CONFIG["threshold"]),
                   key=lambda x: -x["points"])[: trend["hn_top"]]
    papers = sorted(papers, key=lambda x: -x["points"])[: trend["papers_top"]]
    cost = sum(tokens) * PRICE_PER_M / 1e6

    # 출처별로 따로 뽑는다. 같은 순위표에 두면 arXiv가 목록을 차지한다
    shown, sections = set(), {}
    for k in interests:
        picks = []
        for group, cap in (("arXiv", CONFIG["arxiv"]["per_interest"]), ("other", CONFIG["filtered_per_interest"])):
            cand = sorted((x for x in scored if x.get(k, 0) >= CONFIG["threshold"]
                           and (x["source"] == "arXiv") == (group == "arXiv")), key=lambda x: -x[k])
            n = 0
            for x in cand:
                u = norm_url(x["url"])
                if u in shown or n == cap:
                    continue
                shown.add(u)
                picks.append(x)
                n += 1
        sections[k] = sorted(picks, key=lambda x: -x[k])

    topic_section = ""
    if CONFIG.get("topics", {}).get("enabled", False):
        try:
            from topics import make_sections as topic_sections
            topic_section, topic_shown, topic_tokens, topic_failures = topic_sections(
                OUT / "관심사.md", scored + trusted, SINCE, NOW, client, CONFIG, norm_url, skip | shown)
            shown |= topic_shown
            cost += topic_tokens * PRICE_PER_M / 1e6
            failures += topic_failures
        except Exception as e:
            failures.append(f"요즘 관심사: {type(e).__name__}: {e}")

    links, link_cfg = {}, CONFIG.get("claim_links", {})
    if link_cfg.get("enabled", False):
        try:
            from claims import link_claims, published_claims
            section_items = [x for k in interests for x in sections[k]]
            links, link_tokens = link_claims(section_items, published_claims(VAULT), client, link_cfg)
            cost += link_tokens * PRICE_PER_M / 1e6
        except Exception as e:
            failures.append(f"주장 연결: {type(e).__name__}: {e}")

    backlog_section = ""
    if CONFIG.get("backlog", {}).get("enabled", False):
        try:
            from backlog import make_section
            backlog_section, backlog_tokens = make_section(VAULT, OUT, client, CONFIG)
            cost += backlog_tokens * PRICE_PER_M / 1e6
        except Exception as e:
            failures.append(f"안 읽은 자료카드: {type(e).__name__}: {e}")

    reading_report, reading_usage = "", {"cost_usd": 0, "errors": []}
    if CONFIG.get("reading", {}).get("enabled", False):
        try:
            from reading import make_report
            reading_report, reading_result = make_report(
                scored, OUT, CONFIG, saved_sources(), client, record_shown=True)
            reading_usage = reading_result["usage"]
            cost += reading_usage["cost_usd"]
        except Exception as e:
            failures.append(f"읽기 묶음: {type(e).__name__}: {e}")

    day = time.strftime("%Y-%m-%d", time.localtime(NOW))
    span = f"{time.strftime('%Y-%m-%d', time.localtime(SINCE))} ~ {day}"
    counts = {}
    for x in pool:
        counts[x["source"]] = counts.get(x["source"], 0) + 1
    lines = [f"# Jev 레이더 {day}", "",
             f"> {span}에 올라온 {len(pool)}건을 관심 질문 {len(interests)}개로 판정했다. "
             f"{CONFIG['threshold']} 이상만 올렸다. 저장할 글은 Claude에게 자료카드로 저장해 달라고 하면 된다.", "",
             "> 읽고 도움이 된 글은 체크한다. 줄 끝에 `이미앎`, `관심밖`, `지금아님` 중 하나를 적으면 그 반응으로 남는다. "
             "다음 실행 때 기록되며, 체크 해제나 반응 표시 삭제는 해당 항목의 반응을 취소한다. 열어 보거나 저장한 것만으로는 반응으로 치지 않는다. "
             "→ 표시는 초록에서 내 주장과 같은 현상을 다룬 문장이다. 강화인지 반박인지는 직접 판단한다.", ""]
    if topic_section:
        lines += [topic_section]
    if CONFIG.get("suggest", {}).get("enabled", False):
        try:
            from suggest import make_section as suggest_section
            lines += [suggest_section(VAULT, OUT / "관심사.md", CONFIG), ""]
        except Exception as e:
            failures.append(f"관심사 후보: {type(e).__name__}: {e}")
    for k, v in interests.items():
        lines += [f"## {v['label']}", "", f"관련 노트: {', '.join(v['notes'])}", ""]
        for x in sections[k]:
            lines.append(f"- [ ] {x[k]:.2f} [{x['title']}]({x['url']}) - {x['source']}")
            for f in links.get(x["url"], []):
                s_ = f["sentence"] if len(f["sentence"]) <= 220 else f["sentence"][:217] + "..."
                lines.append(f"    - → [[{f['claim']}]] ← \"{s_}\"")
        if not sections[k]:
            lines.append("- 없음")
        lines.append("")
    if backlog_section:
        lines += [backlog_section, ""]
    if reading_report:
        lines += [reading_report, ""]
    lines += ["## 이번 주 AI", "", "관심 질문과 상관없이 화제성(점수·추천 수) 순으로 뽑았다.", "", "### 화제", ""]
    lines += [f"- {x['points']}점 [{x['title']}]({x['url']}) - Hacker News" for x in hn_ai]
    lines += [f"- 추천 {x['points']} [{x['title']}]({x['url']}) - Hugging Face Papers" for x in papers]
    lines += [f"- [{x['title']}]({x['url']}) - {x['source']}" for x in community]
    lines += ["", "### 공식 발표", ""]
    lines += [f"- [{x['title']}]({x['url']}) - {x['source']}, {x['date']}" for x in official] or ["- 없음"]
    lines += ["", "### 주간 요약", ""]
    lines += [f"- [{x['title']}]({x['url']}) - {x['source']}, {x['date']}" for x in digest] or ["- 없음"]
    lines.append("")
    lines += ["## 믿고 보는 저자", ""]
    lines += [f"- [{x['title']}]({x['url']}) - {x['source']}, {x['date']}" for x in sorted(trusted, key=lambda x: x["source"])] or ["- 없음"]
    lines += ["", "## 실행 기록", "",
              f"- 출처별 건수: {', '.join(f'{s} {n}' for s, n in counts.items())}",
              f"- 판정 {len(scored)}건, 오류 {len(errors)}건, {time.time() - started:.0f}초, ${cost:.4f}",
              f"- 주장 연결 {sum(len(v) for v in links.values())}건, 지난 목록에서 기록한 반응 {len(feedback_added)}건"]
    lines += [f"- 가져오기 실패: {f}" for f in failures]
    from claims import register_checkbox_snapshot
    report_path = OUT / f"{day}-전체.md"
    report_path.write_text("\n".join(lines) + "\n")
    register_checkbox_snapshot(OUT, report_path)
    # 한 화면 목록: 전체 목록에서 훑어볼 것만 추리고 저장 자료 짝 후보를 붙인다
    if CONFIG.get("compose", {}).get("enabled", False):
        try:
            from compose import make_page
            page, compose_tokens, compose_failures = make_page(VAULT, OUT, day, report_path.read_text(), client, CONFIG, report_path.stem)
            cost += compose_tokens * PRICE_PER_M / 1e6
            if compose_failures:
                page += "\n" + "\n".join(f"- 짝 후보 실패: {f}" for f in compose_failures) + "\n"
            (OUT / f"{day}.md").write_text(page)
            register_checkbox_snapshot(OUT, OUT / f"{day}.md")
        except Exception as e:
            (OUT / f"{day}.md").write_text(f"# Jev 레이더 {day}\n\n한 화면 목록을 만들지 못했다({type(e).__name__}: {e}). [[{report_path.stem}]]를 본다.\n")

    trend_urls = {norm_url(x["url"]) for x in hn_ai + papers + community + official + digest}
    state["shown"] = sorted(set(state["shown"]) | shown | trend_urls | {norm_url(x["url"]) for x in trusted})
    state_path.write_text(json.dumps(state, ensure_ascii=False, indent=1))
    (OUT / f"{day}.json").write_text(json.dumps({"scored": scored, "trusted": trusted}, ensure_ascii=False))
    total = sum(len(v) for v in sections.values())
    notify(f"{total}건을 골랐습니다 ({len(pool)}건 판정, ${cost:.3f})" + (" · 일부 출처/분류 실패" if failures or errors or reading_usage["errors"] else ""))
    print(f"{OUT / f'{day}.md'}: picked {total}, pool {len(pool)}, cost ${cost:.4f}, failures {failures}")


if __name__ == "__main__":
    main()
