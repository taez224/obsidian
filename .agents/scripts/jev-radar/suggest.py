"""요즘 관심사 후보를 제안한다. 외부 호출 없이 로컬 노트에서 이름만 센다.

최근 2주 동안 만든 DevLog·Inbox·자료카드·일일 노트에 여러 번 나왔지만, 그 전 노트에는 드물었던 영문 이름을 고른다.
관심사 노트에 이미 있는 이름과 `## 제외` 절에 적은 이름은 빼고 보여 준다.

미리보기: python3 .agents/scripts/jev-radar/suggest.py
"""
import math
import re
import time
from datetime import date, datetime
from pathlib import Path

DEFAULT = dict(enabled=True, recent_days=14, min_docs=2, max_suggestions=5)
FOLDERS = {
    "DevLog": "30_Resources/Development/DevLog/daily",
    "Inbox": "00_Inbox",
    "자료카드": "30_Resources/References/Clippings",
    "일일 노트": "10_Periodic Notes",
}
# 어디에나 나오는 말. 나머지 흔한 말은 예전 노트에도 자주 나와 점수가 낮아진다
STOP = {"The", "This", "That", "These", "It", "In", "On", "For", "And", "But", "If", "When", "What", "How", "Why",
        "A", "An", "I", "We", "You", "My", "Our", "Of", "To", "With", "From", "By", "As", "At", "Is", "Are", "Not",
        "AI", "API", "UI", "URL", "PR", "OK", "TODO", "LLM", "GitHub", "Obsidian", "Claude", "Markdown", "Note",
        "Source", "Summary", "Choice", "Noul", "Score", "Slipbox", "Inbox", "Clippings", "RSS", "PARA", "MOC", "YES", "NO", "True", "False", "None", "JSON", "HTML", "CSS", "MD", "DevLog"}
# 한국어 조사가 바로 붙어도 이름으로 잡도록 영문자·숫자만 경계로 본다. 축약형(Don't)은 뺀다
WORD = r"(?:[A-Z][A-Za-z0-9+.-]*[A-Za-z0-9]|[A-Z]{2,})"
NAME = re.compile(rf"(?<![A-Za-z0-9]){WORD}(?:\s+{WORD}){{0,2}}(?![A-Za-z0-9'’])")


def doc_date(path, text):
    m = re.search(r"(\d{4}-\d{2}-\d{2})", path.name)
    if m:
        return date.fromisoformat(m.group(1))
    m = re.search(r"^(?:created|date):\s*\"?(\d{4}-\d{2}-\d{2})", text[:1500], re.M)
    if m:
        return date.fromisoformat(m.group(1))
    return datetime.fromtimestamp(path.stat().st_mtime).date()


def clean(text):
    text = re.sub(r"^---\n.*?\n---\n", "", text, flags=re.S)
    text = re.sub(r"```.*?```|`[^`]*`", " ", text, flags=re.S)
    text = re.sub(r"https?://\S+", " ", text)
    return re.sub(r"\[\[([^\]|]*\|)?([^\]]*)\]\]", r"\2", text)


def names(text):
    found = set()
    for m in NAME.finditer(clean(text)):
        words = [w for w in m.group(0).split() if w not in STOP]
        if words:
            found.add(" ".join(words))
    return found


def excluded(interest_path):
    """관심사 노트에 이미 있는 이름·검색어와 `## 제외` 절의 이름."""
    if not interest_path.exists():
        return set()
    text = interest_path.read_text()
    out = set()
    for line in text.splitlines():
        if line.startswith("- ") and "|" in line:
            name, *_, terms = [p.strip() for p in line[2:].split("|")]
            out.add(name.lower())
            out |= {t.strip().lower() for t in terms.replace("검색어:", "").split(",") if t.strip()}
    m = re.search(r"^## 제외\s*\n(.*?)(?=^## |\Z)", text, re.M | re.S)
    if m:
        out |= {l[2:].strip().lower() for l in m.group(1).splitlines() if l.startswith("- ")}
    return out


def radar_vocabulary(config):
    """레이더 자신의 출처 이름. 레이더 작업을 적은 DevLog가 이 이름들을 후보로 만들지 않게 한다."""
    names = set()
    for key in ("filtered", "trusted"):
        names |= set(config.get(key, {}))
    trend = config.get("trend", {})
    for key in ("community", "official", "digest"):
        names |= set(trend.get(key, {}))
    words = set()
    for n in names | {"Hacker News", "arXiv", "Hugging Face", "GeekNews"}:
        words.add(n.lower())
        words |= {re.sub(r"[()]", "", w).lower() for w in n.split() if len(w) > 2}
    return words


def suggest(vault, interest_path, config, today=None):
    cfg = {**DEFAULT, **config.get("suggest", {})}
    today = today or date.today()
    recent, base = {}, {}
    n_recent = n_base = 0
    for label, folder in FOLDERS.items():
        for p in (vault / folder).rglob("*.md"):
            text = p.read_text(errors="ignore")
            is_recent = (today - doc_date(p, text)).days <= cfg["recent_days"]
            n_recent += is_recent
            n_base += not is_recent
            for n in names(text):
                if is_recent:
                    recent.setdefault(n, {}).setdefault(label, set()).add(p.stem)
                else:
                    base[n] = base.get(n, 0) + 1
    skip = excluded(interest_path) | radar_vocabulary(config)
    scored = []
    for n, by in recent.items():
        docs = sum(len(v) for v in by.values())
        low = n.lower()
        if docs < cfg["min_docs"] or low in skip or any(w.lower() in skip for w in n.split()) \
                or any(low in s or s in low for s in skip if len(s) > 3):
            continue
        # 최근 문서 비율이 예전 문서 비율보다 얼마나 높은가
        lift = (docs / max(1, n_recent)) / ((base.get(n, 0) + 1) / max(1, n_base))
        scored.append((docs * math.log(1 + lift), n, by, base.get(n, 0)))
    scored.sort(key=lambda x: -x[0])
    return scored[: cfg["max_suggestions"]], n_recent


def make_section(vault, interest_path, config):
    rows, n_recent = suggest(vault, interest_path, config)
    days = {**DEFAULT, **config.get("suggest", {})}["recent_days"]
    lines = ["## 관심사 후보", "",
             f"지난 {days}일 동안 만든 노트 {n_recent}개에 여러 번 나왔지만 예전 노트에는 드물었던 이름이다. "
             "외부로 보낸 것은 없다. 채택하려면 `관심사.md`에 한 줄을 더하고, 다시 보고 싶지 않으면 `## 제외` 절에 이름을 적는다.", ""]
    for _, n, by, old in rows:
        where = ", ".join(f"{label} {len(v)}개" for label, v in by.items())
        lines.append(f"- {n} — {where}" + (f" (예전 노트 {old}개)" if old else " (예전 노트에는 없음)"))
    if not rows:
        lines.append("- 없음")
    return "\n".join(lines)


if __name__ == "__main__":
    import json
    here = Path(__file__).resolve().parent
    vault = here.parents[2]
    config = json.loads((here / "config.json").read_text())
    print(make_section(vault, vault / "_workspace/radar/관심사.md", config))
