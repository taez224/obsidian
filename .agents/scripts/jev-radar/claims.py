"""레이더 항목을 게시된 Slipbox 주장과 문장 단위로 잇고, 주간 목록의 체크박스 반응을 기록한다.

외부로는 공개 제목·초록과, 게시된(origin/main) Slipbox 영구 노트의 제목만 보낸다.
"""
import re
import json
import subprocess
from pathlib import Path

from typesafe_sdk import Choice, Noul

from reading import add_feedback, canonical, events_at, atomic_json

SAME = ("Does the text `text` report, discuss, or give evidence about the same phenomenon that the claim `{claim}` is about? "
        "Answer yes only if the text itself addresses that phenomenon, not merely a related topic. The claim is written in Korean.")
PICK = ("Which sentence from the text most directly reports an observation, evidence, or argument about the same phenomenon "
        "as the Korean claim `claim`? Choose none if no sentence does.")
DEFAULT = dict(enabled=True, claim_floor=0.7, sentence_confidence=0.5, max_links=2, min_summary_chars=200)

# 목록 줄 끝에 적는 반응 표시. 체크만 하면 도움 됨이다
MARKERS = {"이미앎": "already_known", "관심밖": "off_topic", "지금아님": "not_now"}
URL_RE = re.compile(r"\]\((https?://[^)\s]+)\)")


def published_claims(vault):
    """게시된 Slipbox 영구 노트의 제목. 로컬에만 있는 노트는 외부로 보내지 않는다."""
    git = lambda *a: subprocess.run(["git", "-C", str(vault), *a], capture_output=True, text=True).stdout
    claims = []
    for f in git("ls-tree", "-r", "--name-only", "origin/main", "--", "01_Slipbox").splitlines():
        if not f.endswith(".md") or "/_" in f:
            continue
        head = git("show", f"origin/main:{f}")[:800]
        if re.search(r"^type:\s*permanent\s*$", head, re.M):
            claims.append(Path(f).stem)
    return claims


def sentences(text):
    parts = [s.strip() for s in re.split(r"(?<=[.!?])\s+(?=[A-Z\"“(])", text) if len(s.strip()) > 30]
    return parts[:250]  # Choice 선택지 한도(255) 안


def link_claims(items, claims, client, cfg=None):
    """항목 URL → [{claim, p, sentence, confidence}]. 주장 점수와 문장 확신도를 모두 넘은 것만 남긴다."""
    cfg = {**DEFAULT, **(cfg or {})}
    usage, links = [], {}
    todo = [x for x in items if len(x.get("summary") or "") >= cfg["min_summary_chars"]]
    for x in todo:
        try:
            qs = {f"c{i}": Noul(instructions=SAME.replace("{claim}", c)) for i, c in enumerate(claims)}
            r = client.system_one({"title": x["title"], "text": x["summary"][:6000]}, qs)
            usage.append(getattr(getattr(r, "usage", None), "input_tokens", 0) or 0)
            ranked = sorted(((r.nouls[f"c{i}"].noul, c) for i, c in enumerate(claims)), reverse=True)
            ss = sentences(x["summary"])
            found = []
            for p, claim in ranked[: cfg["max_links"]]:
                if p < cfg["claim_floor"] or not ss:
                    break
                crit = {f"s{i}": s[:400] for i, s in enumerate(ss)}
                crit["none"] = "No sentence in the text addresses the claim's phenomenon."
                a = client.system_one({"claim": claim}, {"pick": Choice(instructions=PICK, criteria=crit)})
                usage.append(getattr(getattr(a, "usage", None), "input_tokens", 0) or 0)
                a = a.choices["pick"]
                if a.choice != "none" and a.confidence >= cfg["sentence_confidence"]:
                    found.append({"claim": claim, "p": round(p, 2), "sentence": crit[a.choice], "confidence": round(a.confidence, 2)})
            if found:
                links[x["url"]] = found
        except Exception:
            continue  # 연결은 덧붙이는 정보라 실패해도 목록은 그대로 낸다
    return links, sum(usage)


def checkbox_controls(path):
    """Parse reaction suffix only; titles, URLs and quoted lines are never markers."""
    controls, counts = {}, {}
    for line in path.read_text().splitlines():
        checked = re.match(r'^- \[([ xX])\] ', line)
        m = URL_RE.search(line)
        if not checked or not m:
            continue
        url = canonical(m[1])
        tail = line[m.end():]
        marker = re.search(r'(?:^|\s)(이미\s*앎|관심\s*밖|지금\s*아님)\s*$', tail)
        action = MARKERS[re.sub(r'\s+', '', marker[1])] if marker else ('useful' if checked[1].lower() == 'x' else None)
        counts[url] = counts.get(url, 0) + 1
        control = f'{path.name}:{url}:{counts[url]}'
        controls[control] = {'url': url, 'action': action}
    return controls


def checkbox_snapshot(out):
    path = out / 'checkbox-state.json'
    return json.loads(path.read_text()) if path.exists() else {}


def register_checkbox_snapshot(out, path):
    """Record generated defaults, so regeneration is not mistaken for a user undo."""
    state = checkbox_snapshot(out)
    for key, control in checkbox_controls(path).items():
        if key not in state or state[key]['action'] != control['action']:
            state[key] = {**control, 'event_id': None}
    atomic_json(out / 'checkbox-state.json', state)


def import_checkbox_feedback(out, lookback=4):
    """Observe per-control changes and retract only that control's previous event."""
    state = checkbox_snapshot(out)
    days = sorted({p.name[:10] for p in out.glob('20??-??-??*.md')
                   if re.fullmatch(r'\d{4}-\d{2}-\d{2}(?:-reading|-전체)?\.md', p.name)})[-lookback:]
    paths = [p for p in out.glob('20??-??-??*.md') if p.name[:10] in days
             and re.fullmatch(r'\d{4}-\d{2}-\d{2}(?:-reading|-전체)?\.md', p.name)]
    added = []
    for path in sorted(paths, key=lambda p: (p.stat().st_mtime_ns, p.name)):
        for key, control in checkbox_controls(path).items():
            old = state.get(key)
            if old is not None and old['action'] == control['action']:
                continue
            if old and old.get('event_id'):
                add_feedback(out, control['url'], 'retract', retracts=old['event_id'], control=key)
                added.append((control['url'], 'retract'))
            event = None
            if control['action']:
                event = add_feedback(out, control['url'], control['action'], control=key)
                added.append((control['url'], control['action']))
            state[key] = {**control, 'event_id': event['event_id'] if event else None}
            # Save after every change so repeated imports remain idempotent.
            atomic_json(out / 'checkbox-state.json', state)
    return added
