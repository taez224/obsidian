"""안 읽은 자료카드에서 이번 주 읽을 카드를 고른다.

카드의 원문 주소에서 공개 텍스트를 새로 가져와 게시된 Slipbox 주장과 문장 단위로 잇는다.
카드에 적은 요약·my_take는 외부로 보내지 않는다. 원문과 판정은 캐시해서, 매주 비용은 새 카드분만 든다.

미리보기: uv run --with typesafe-sdk --with feedparser python .agents/scripts/jev-radar/backlog.py
"""
import hashlib
import json
import math
import os
import re
import shutil
import subprocess
import time
import urllib.request
import xml.etree.ElementTree as ET
from functools import lru_cache
from pathlib import Path

from claims import link_claims, published_claims, sentences

DEFAULT = dict(enabled=True, picks=3, chunk_size=2500, max_chunks=12, retry_fail_days=30, min_chars=400,
               defuddle_path="defuddle")
ATOM = "{http://www.w3.org/2005/Atom}"


def unread_cards(vault):
    cards = []
    for p in sorted((vault / "30_Resources/References/Clippings").glob("*.md")):
        head = p.read_text(errors="ignore")[:3000]
        if not re.search(r"^status:\s*unread\s*$", head, re.M):
            continue
        src = re.search(r"^source:\s*\"?(\S+?)\"?\s*$", head, re.M)
        title = re.search(r"^title:\s*\"?(.+?)\"?\s*$", head, re.M)
        if src:
            cards.append({"card": p.stem, "url": src.group(1), "title": title.group(1) if title else p.stem})
    return cards


def _key(*parts):
    return hashlib.sha256("\n".join(parts).encode()).hexdigest()[:20]


@lru_cache(maxsize=None)
def defuddle_command(configured="defuddle"):
    """defuddle 실행 파일과 실행 환경. 설정 경로, nvm의 최신 Node부터, PATH 순으로 찾는다.
    defuddle은 `#!/usr/bin/env node` 스크립트라 찾은 bin 폴더를 PATH 앞에 둬야 같은 Node로 돈다(post-commit 훅과 같은 방식).
    Node를 올려도 설정을 고칠 필요가 없다."""
    version = lambda p: [int(x) for x in re.findall(r"\d+", p.parent.parent.name)]
    nvm = sorted(Path.home().glob(".nvm/versions/node/*/bin/defuddle"), key=version, reverse=True)
    candidates = ([Path(configured)] if os.path.isabs(configured) else []) + nvm
    candidates += [Path(p) for p in (shutil.which(configured), "/opt/homebrew/bin/defuddle", "/usr/local/bin/defuddle") if p]
    for c in candidates:
        if not (c.is_file() and os.access(c, os.X_OK)):
            continue
        env = {**os.environ, "PATH": f"{c.parent}:{os.environ.get('PATH', '')}"}
        try:
            if subprocess.run([str(c), "--version"], capture_output=True, env=env, timeout=30).returncode == 0:
                return str(c), env
        except (OSError, subprocess.TimeoutExpired):
            continue
    return configured, None


def fetch_text(url, cfg):
    m = re.search(r"arxiv\.org/(?:abs|pdf|html)/(\d{4}\.\d{4,5})", url)
    if m:
        x = urllib.request.urlopen(f"https://export.arxiv.org/api/query?id_list={m.group(1)}", timeout=60).read()
        e = ET.fromstring(x).find(f"{ATOM}entry")
        return " ".join(e.find(f"{ATOM}summary").text.split()), "arxiv-api"
    if re.search(r"youtube\.com|youtu\.be", url):
        return "", "video"
    exe, env = defuddle_command(cfg.get("defuddle_path") or "defuddle")
    md = subprocess.run([exe, "parse", url, "--md"], capture_output=True, text=True, timeout=90, env=env).stdout
    md = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", md)
    md = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", md)
    return " ".join(re.sub(r"[#>*_`|]", " ", md).split()), "defuddle"


def cached_text(card, cache, cfg):
    path = cache / f"text-{_key(card['url'])}.json"
    if path.exists():
        c = json.loads(path.read_text())
        fresh = time.time() - c["at"] < cfg["retry_fail_days"] * 86400
        if len(c["text"]) >= cfg["min_chars"] or fresh:
            return c
    try:
        text, how = fetch_text(card["url"], cfg)
    except Exception as e:
        text, how = "", f"fail {type(e).__name__}"
    c = {"text": text, "how": how, "at": time.time()}
    path.write_text(json.dumps(c, ensure_ascii=False))
    return c


def chunks(text, size):
    if len(text) <= size + 500:
        return [text]
    out, cur = [], ""
    for s in sentences(text) or [text]:
        if len(cur) + len(s) > size and cur:
            out.append(cur)
            cur = ""
        cur += (" " if cur else "") + s
    return out + ([cur] if cur else [])


def card_links(card, text, claims, client, cache, cfg, link_cfg):
    """카드 하나의 연결. 원문과 주장 목록이 같으면 지난 판정을 쓴다."""
    path = cache / f"links-{_key(card['url'], text, *claims)}.json"
    if path.exists():
        return json.loads(path.read_text()), 0
    pieces = [{"title": card["title"], "summary": c, "url": f"{card['url']}#chunk{i}"}
              for i, c in enumerate(chunks(text, cfg["chunk_size"])[: cfg["max_chunks"]])]
    raw, tokens = link_claims(pieces, claims, client, {**link_cfg, "max_links": 3})
    best = {}
    for found in raw.values():
        for f in found:
            if f["claim"] not in best or f["p"] * f["confidence"] > best[f["claim"]]["p"] * best[f["claim"]]["confidence"]:
                best[f["claim"]] = f
    links = sorted(best.values(), key=lambda f: -f["p"] * f["confidence"])[:3]
    path.write_text(json.dumps(links, ensure_ascii=False))
    return links, tokens


def pick(cards, picks):
    """넓은 주장이 여러 카드에 걸리면 그 주장의 무게를 낮추고, 같은 주장으로만 이어진 카드는 하나만 고른다."""
    counts = {}
    for c in cards:
        for f in c["links"]:
            counts[f["claim"]] = counts.get(f["claim"], 0) + 1
    total = max(1, len(cards))
    weight = {k: math.log(1 + total / v) for k, v in counts.items()}
    for c in cards:
        c["score"] = sum(f["p"] * f["confidence"] * weight[f["claim"]] for f in c["links"])
    chosen, used = [], set()
    for c in sorted((c for c in cards if c["links"]), key=lambda c: -c["score"]):
        top = max(c["links"], key=lambda f: f["p"] * f["confidence"] * weight[f["claim"]])["claim"]
        if top in used:
            continue
        chosen.append(c)
        used.add(top)
        if len(chosen) == picks:
            break
    return chosen


def make_section(vault, out, client, config):
    cfg = {**DEFAULT, **config.get("backlog", {})}
    link_cfg = config.get("claim_links", {})
    cache = out / "backlog-cache"
    cache.mkdir(parents=True, exist_ok=True)
    claims = published_claims(vault)
    cards, missing, tokens = [], [], 0
    for card in unread_cards(vault):
        c = cached_text(card, cache, cfg)
        if len(c["text"]) < cfg["min_chars"]:
            missing.append(card)
            continue
        links, t = card_links(card, c["text"], claims, client, cache, cfg, link_cfg)
        tokens += t
        cards.append({**card, "links": links})
    chosen = pick(cards, cfg["picks"])
    lines = ["## 안 읽은 자료카드", "",
             f"`unread` 카드 {len(cards) + len(missing)}개 중 원문을 가져온 {len(cards)}개를 게시된 주장과 이었다. "
             f"원문을 가져오지 못한 {len(missing)}개는 직접 열어 봐야 한다. 참고노트를 쓰고 `status`를 바꾸면 이 목록에서 빠진다.", ""]
    for c in chosen:
        lines.append(f"- [[{c['card']}]]")
        for f in c["links"]:
            s = f["sentence"] if len(f["sentence"]) <= 220 else f["sentence"][:217] + "..."
            lines.append(f"    - → [[{f['claim']}]] ← \"{s}\"")
    if not chosen:
        lines.append("- 주장과 이어진 카드가 없다")
    return "\n".join(lines), tokens


if __name__ == "__main__":
    import os, sys
    from typesafe_sdk import TypeSafeClient
    here = Path(__file__).resolve().parent
    vault = here.parents[2]
    if not os.environ.get("TYPESAFE_API_KEY"):
        os.environ["TYPESAFE_API_KEY"] = subprocess.run(
            ["security", "find-generic-password", "-a", os.environ.get("USER", ""), "-s", "TYPESAFE_API_KEY", "-w"],
            capture_output=True, text=True).stdout.strip()
    config = json.loads((here / "config.json").read_text())
    section, tokens = make_section(vault, vault / "_workspace/radar", TypeSafeClient(), config)
    print(section)
    print(f"\n(${tokens * 0.042 / 1e6:.4f})", file=sys.stderr)
