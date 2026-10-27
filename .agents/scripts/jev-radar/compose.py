"""한 화면 레이더: 전체 목록에서 훑어볼 항목만 추리고, 같은 주장에 닿은 저장 자료를 짝 후보로 붙인다.

전체 목록(`날짜-전체.md`)을 읽어 요즘 관심사·화제·관심 질문·믿고 보는 저자에서 몇 건씩 고른다.
기존 자리 하나는 믿고 보는 저자나 관심사의 소식·논의에서 주장 연결과 별개로 골라 대체한다.
이 탐색용 글을 제외한 원문을 2,500자 조각으로 나눠 게시된 주장과 잇고, 안 읽은 자료카드와 참고노트 중 같은 주장에 닿은 것을 짝 후보로 보인다.
짝은 후보일 뿐이라 결론 대신 질문으로 보인다. 같이 읽을 이유와 읽을 대목은 Claude가 미리 준비한 묶음(`날짜-함께읽기.md`)이나 사용자가 고른 항목에만 붙인다.
외부로는 공개 글과 저장 자료의 원문(원문 URL에서 새로 가져온 공개 텍스트)과 게시된 주장 제목만 나간다.

미리보기: uv run --with typesafe-sdk --with feedparser python .agents/scripts/jev-radar/compose.py 2026-09-28
"""
import math
import re
from concurrent.futures import ThreadPoolExecutor
from datetime import date

from feeds import balanced
from reading import canonical, eligible, events_at, feedback_state, title_key

DEFAULT = dict(enabled=True, topic_cases=2, topic_news=1, hot=10, interest=4, trusted=2, engineering=4,
               item_floor=0.8, item_confidence=0.6, ref_floor=0.8, max_pairs=5, discovery=True)
ITEM = re.compile(r"^- (?:\[[ xX]\] )?(.*?)\[(.+?)\]\((https?://[^)\s]+)\) - (.+)$")


def parse_report(text, interest_labels):
    """전체 목록에서 절별 항목을 꺼낸다. 각 항목: {group, title, url, line}."""
    groups, sec, sub, current = {}, None, None, None
    for line in text.splitlines():
        if line.startswith("## "):
            sec, sub, current = line[3:].strip(), None, None
            continue
        if line.startswith("### "):
            sub, current = line[4:].strip(), None
            continue
        if current is not None and line.startswith("    - → [["):
            current["claim_linked"] = True
            continue
        m = ITEM.match(line)
        if not m or sec is None:
            continue
        if sec.startswith("요즘 관심사: "):
            key = ("topic", sec.split(": ", 1)[1], "case" if sub == "활용 사례" else "news")
        elif sec in interest_labels:
            key = ("interest",)
        elif sec == "이번 주 AI" and sub == "화제" and m[4].strip() == "Hacker News":
            key = ("hot",)
        elif sec == "엔지니어링 읽을거리":
            key = ("engineering",)
        elif sec == "믿고 보는 저자":
            key = ("trusted",)
        else:
            continue
        head = m[1].strip()
        body = f"{head} [{m[2]}]({m[3]}) - {m[4]}" if head else f"[{m[2]}]({m[3]}) - {m[4]}"
        current = {"title": m[2], "url": m[3], "line": body, "head": head,
                   "source": m[4].strip().split(", ", 1)[0], "claim_linked": False}
        groups.setdefault(key, []).append(current)
        if key == ("interest",):
            groups.setdefault(("axis", sec), []).append(current)
    return groups


def skim(groups, cfg, day=None):
    """훑어볼 항목. (절 제목, [항목]) 목록."""
    out = []
    for (kind, *rest), items in groups.items():
        if kind != "topic" or rest[1] != "case":
            continue
        name = rest[0]
        # 활용 사례는 출처마다 첫 항목(HN 점수와 GitHub 별 수는 한 순위표에 섞지 않는다)
        firsts, seen = [], set()
        for x in items:
            src = x["line"].rsplit(" - ", 1)[-1]
            if src not in seen:
                seen.add(src)
                firsts.append(x)
        pick = firsts[: cfg["topic_cases"]] + groups.get(("topic", name, "news"), [])[: cfg["topic_news"]]
        out.append((f"요즘 관심사: {name}", pick))
    for (kind, *rest), items in groups.items():  # 활용 사례가 없는 관심사
        if kind == "topic" and rest[1] == "news" and ("topic", rest[0], "case") not in groups:
            out.append((f"요즘 관심사: {rest[0]}", items[: cfg["topic_news"]]))
    score = lambda x: float(x["head"]) if re.fullmatch(r"\d\.\d+", x["head"]) else 0
    out.append(("화제", groups.get(("hot",), [])[: cfg["hot"]]))
    interest_items = sorted(groups.get(("interest",), []), key=lambda x: -score(x))
    if cfg.get("interest_balanced"):
        candidates = []
        for (kind, *rest), items in groups.items():
            if kind == "axis":
                candidates.extend({**x, "source": rest[0], "original": x} for x in sorted(items, key=lambda x: -score(x)))
        interest_items = [x["original"] for x in balanced(candidates, cfg["interest"], day, newest=False)]
    out.append(("관심 질문 근처", interest_items[: cfg["interest"]]))
    out.append(("믿고 보는 저자", balanced(groups.get(("trusted",), []), cfg["trusted"], day)))
    out.append(("엔지니어링 읽을거리", balanced(groups.get(("engineering",), []), cfg.get("engineering", 4), day)))
    return [(h, xs) for h, xs in out if xs]


def discover(sections, groups, cfg, excluded=(), states=None, today=None, snooze_days=7, excluded_titles=()):
    """기존 자리 하나를 주장 연결 없이 고른 글로 대체한다. 추가 호출·피드백 쓰기 없음."""
    if not cfg.get("discovery", True):
        return sections
    blocked = {canonical(u) for u in excluded}
    seen, titles, baseline = set(), {title_key(t) for t in excluded_titles if title_key(t)}, []
    for head, items in sections:
        kept = []
        for x in items:
            url, title = canonical(x["url"]), title_key(x["title"])
            if url in blocked or url in seen or (title and title in titles):
                continue
            seen.add(url)
            titles.add(title)
            kept.append(x)
        if kept:
            baseline.append((head, kept))
    if not baseline:
        return baseline

    # 같은 글이 여러 절에 나오면 다른 절에서 확인한 주장 연결도 함께 적용한다.
    linked = [x for items in groups.values() for x in items if x.get("claim_linked")]
    linked_urls = {canonical(x["url"]) for x in linked}
    linked_titles = {title_key(x["title"]) for x in linked if title_key(x["title"])}
    pool = []
    for key, items in groups.items():
        if key == ("trusted",):
            reason = "믿고 보는 저자의 글을 관심 질문 점수와 별개로 골랐다."
        elif key[0] == "topic" and key[2] == "news":
            reason = f"요즘 관심사 '{key[1]}'의 소식·논의를 활용 사례 여부와 별개로 골랐다."
        else:
            continue
        for x in items:
            url, title = canonical(x["url"]), title_key(x["title"])
            if url in linked_urls or url in seen or (title and (title in linked_titles or title in titles)):
                continue
            if eligible(x, states or {}, blocked, today or date.today(), {"snooze_days": snooze_days}):
                pool.append((x, reason))
    if not pool:
        return baseline
    sources = {x.get("source") for _, items in baseline for x in items}
    chosen, reason = min(pool, key=lambda candidate: candidate[0].get("source") in sources)
    # 관심 질문의 마지막 자리부터 빌리고, 없으면 기존 다른 절의 마지막 자리를 쓴다.
    priority = ["관심 질문 근처", "화제", "믿고 보는 저자"]
    victim = min(range(len(baseline)), key=lambda i: priority.index(baseline[i][0])
                 if baseline[i][0] in priority else len(priority))
    head, items = baseline[victim]
    baseline[victim] = (head, items[:-1])
    return [(h, xs) for h, xs in baseline if xs] + [
        ("다른 글도 한 편", [{**chosen, "discovery_reason": reason}])]


def pair(items, refs, cfg):
    """새 글 items와 저장 자료 refs(각각 links 보유)에서 url → (ref, claim)을 고른다. 외부 호출 없음.

    여러 자료에 걸리는 넓은 주장은 무게를 낮추고, 저장 자료 하나는 한 번만 짝짓는다."""
    counts = {}
    for r in refs:
        for f in r["links"]:
            if f["p"] >= cfg["ref_floor"]:
                counts[f["claim"]] = counts.get(f["claim"], 0) + 1
    idf = {k: math.log(1 + len(refs) / v) for k, v in counts.items()}
    cands = []
    for x in items:
        for f in x["links"]:
            if f["p"] < cfg["item_floor"] or f["confidence"] < cfg["item_confidence"]:
                continue
            for r in refs:
                for g in r["links"]:
                    if g["claim"] == f["claim"] and g["p"] >= cfg["ref_floor"]:
                        s = f["p"] * f["confidence"] * g["p"] * g["confidence"] * idf[f["claim"]]
                        cands.append((s, x["url"], r["card"], f["claim"]))
    chosen, used_items, used_refs = {}, set(), set()
    for s, url, ref, claim in sorted(cands, reverse=True):
        if url in used_items or ref in used_refs:
            continue
        chosen[url] = (ref, claim)
        used_items.add(url)
        used_refs.add(ref)
        if len(chosen) == cfg["max_pairs"]:
            break
    return chosen


def josa(word, pair="과와"):
    """받침이 있으면 앞 글자, 없으면 뒤 글자."""
    c = word[-1]
    has = "가" <= c <= "힣" and (ord(c) - 0xAC00) % 28 != 0
    return pair[0] if has else pair[1]


def render(day, sections, pairs, full_name, prepared=""):
    lines = [f"# Jev 레이더 {day}", "",
             "> 훑어보다가 궁금한 것 하나면 충분하다. 체크는 \"읽고 도움이 됐다\"는 뜻이고, 줄 끝에 `이미앎`·`관심밖`·`지금아님`을 적을 수도 있다. "
             "↔ 는 같은 주장에 닿은 저장 자료 후보이고, 같이 읽을 이유는 아직 확인하지 않았다. "
             f"깊게 보고 싶은 항목은 Claude에게 말하면 읽을 대목을 붙여 준다. 전체 목록은 [[{full_name}]]에 있다.", ""]
    if prepared.strip():
        lines += ["## 이번 주 함께 읽기", "", prepared.strip(), ""]
    for head, xs in sections:
        lines += [f"## {head}", ""]
        if head == "엔지니어링 읽을거리":
            lines += ["최근 RSS에서 출처별로 고른 수집 후보다. AI 관심 질문·품질 판정은 거치지 않았다.", ""]
        for x in xs:
            lines.append(f"- [ ] {x['line']}")
            if x.get("discovery_reason"):
                lines.append(f"    - {x['discovery_reason']}")
            elif x["url"] in pairs:
                ref, claim = pairs[x["url"]]
                lines.append(f"    - ↔ [[{ref}]]: 두 글은 [[{claim}]]{josa(claim)} 닿는 현상을 어디서 다르게 볼까?")
        lines.append("")
    return "\n".join(lines)


def saved_refs(vault):
    """짝 후보가 될 저장 자료: 안 읽은 자료카드와 참고노트."""
    from backlog import unread_cards
    refs = unread_cards(vault)
    for p in sorted((vault / "30_Resources/References/Articles").glob("*.md")):
        head = p.read_text(errors="ignore")[:3000]
        src = re.search(r"^source:\s*\"?(https?://\S+?)\"?\s*$", head, re.M)
        if src:
            refs.append({"card": p.stem, "url": src.group(1), "title": p.stem})
    return refs


def make_page(vault, out, day, full_text, client, config, full_name, excluded=()):
    """(page, 토큰, 실패)."""
    from backlog import DEFAULT as BDEF, cached_text, card_links
    from claims import published_claims
    cfg = {**DEFAULT, **config.get("compose", {})}
    bcfg = {**BDEF, **config.get("backlog", {})}
    link_cfg = config.get("claim_links", {})
    cache = out / "backlog-cache"
    cache.mkdir(parents=True, exist_ok=True)
    labels = {v["label"] for v in config["interests"].values()}
    groups = parse_report(full_text, labels)
    sections = skim(groups, cfg, day)
    claims = published_claims(vault)
    failures, tokens = [], []

    def links_for(x):
        try:
            c = cached_text({"url": x["url"]}, cache, bcfg)
            if len(c["text"]) < bcfg["min_chars"]:
                return {**x, "links": []}
            ls, t = card_links({"url": x["url"], "title": x["title"]}, c["text"], claims, client, cache, bcfg, link_cfg)
            tokens.append(t)
            return {**x, "links": ls}
        except Exception as e:
            failures.append(f"짝 후보 {x['title'][:30]}: {type(e).__name__}")
            return {**x, "links": []}

    prep = out / f"{day}-함께읽기.md"  # Claude가 미리 준비한 묶음이 있으면 맨 위에 두고, 훑어보기에서는 뺀다
    prepared = prep.read_text() if prep.exists() else ""
    prepared_links = re.findall(r"\[([^\]\n]+)\]\((https?://[^)\s]+)\)", prepared)
    taken = {url for _, url in prepared_links}
    sections = [(h, [x for x in xs if x["url"] not in taken]) for h, xs in sections]
    sections = [(h, xs) for h, xs in sections if xs]
    sections = discover(sections, groups, cfg, set(excluded) | taken, feedback_state(events_at(out)),
                        date.fromisoformat(day), config.get("reading", {}).get("snooze_days", 7),
                        excluded_titles=[title for title, _ in prepared_links])
    items = [x for _, xs in sections for x in xs if not x.get("discovery_reason") and x not in dict(sections).get("엔지니어링 읽을거리", [])]
    used = set(re.findall(r"\[\[([^\]|#]+)", prepared))  # 함께 읽기에 이미 쓴 저장 자료는 짝 후보에서 뺀다
    refs = [r for r in saved_refs(vault) if r["card"] not in used]
    with ThreadPoolExecutor(4) as ex:
        items = list(ex.map(links_for, items))
        refs = [r for r in ex.map(links_for, refs) if r["links"]]
    return render(day, sections, pair(items, refs, cfg), full_name, prepared), sum(tokens), failures


if __name__ == "__main__":
    import os, sys
    from pathlib import Path
    from typesafe_sdk import TypeSafeClient
    here = Path(__file__).resolve().parent
    sys.path.insert(0, str(here))
    import radar
    if not os.environ.get("TYPESAFE_API_KEY"):
        radar.api_key()
    day = sys.argv[1]
    full = radar.OUT / f"{day}-전체.md"
    page, tokens, failures = make_page(radar.VAULT, radar.OUT, day, full.read_text(), TypeSafeClient(), radar.CONFIG,
                                      full.stem, excluded=radar.saved_sources())
    print(page)
    print(f"(${tokens * radar.PRICE_PER_M / 1e6:.4f}, 실패 {failures})", file=sys.stderr)
