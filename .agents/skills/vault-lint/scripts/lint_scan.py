#!/usr/bin/env python3
"""vault-lint 기계 검사 스캐너 — 읽기 전용, vault 파일을 절대 수정하지 않는다.

사용: python3 lint_scan.py [vault_root] [--holds PATH]   (기본: 현재 디렉토리, 스킬 폴더의 holds.json)
출력: JSON {stats, priorities, reuse_by_note, orphans, dead_links, broken_anchors, hub_gaps,
           periodic_placeholders, series_placeholders, frontmatter_issues, style_suggestions, base_issues,
           held, stale_holds, hold_errors}

관리 지침
- 스키마 출처는 99_Templates/_property-schema.md다. 스키마가 바뀌면 아래 설정 블록만 갱신한다.
- FOLDER_RULES는 폴더별 필수·허용 속성, 공개 여부(public: slug와 날짜 형식 검사), created 대신 쓰는
  날짜 키를 관리한다. 가장 구체적인 prefix 하나를 적용하며 규칙끼리 상속하지 않는다.
- 공개 노트의 날짜 규칙은 사이트 저장소의 src/lib/dates.mjs와 같다. 한쪽을 바꾸면 다른 쪽도 고친다.
- 블로그 공개 조건과 프로젝트 status 조건은 이름 있는 함수로, 문체 제안은 형식 오류와 별도로 유지한다.
- 스캔 제외는 SCAN_EXCLUDE_TOP, Base 검사는 BASE_INVALID_KEYS에서 관리한다. .base 파일에서 새로운
  미인식 키를 발견하면 BASE_INVALID_KEYS에 추가한다.
- 보류 목록의 종류와 키는 HOLD_KEYS에서 관리한다.
- 스캐너를 고친 뒤에는 test_lint_scan.py로 회귀를 확인한다.
"""
import json
import os
import re
import sys
import unicodedata
from dataclasses import dataclass
from datetime import date, datetime, timedelta, timezone
from typing import Optional

# ── 설정 블록 ──────────────────────────────────────────────
SCAN_EXCLUDE_TOP = {"40_Archive", "99_Templates", "_workspace", "_attachments"}
# 각 폴더 규칙이 생략한 값의 기본값이다. 명시한 값은 덮어쓰지 않으며 다른 규칙과 병합하지 않는다.
@dataclass(frozen=True)
class FolderRule:
    required: tuple = ()
    allowed: Optional[frozenset] = None  # None은 스키마 밖 속성도 허용한다.
    public: bool = False             # 사이트에 페이지가 생기는 폴더. slug와 날짜 형식을 사이트 빌드 기준으로 검사한다.
    created_key: str = "created"
    required_label: str = ""         # 기존 진단 메시지의 분류명을 유지한다.
    review_summary: bool = False     # 오류가 아닌 문맥 검토 제안이다.


DEVELOPMENT_RULE = FolderRule(
    required=("summary",), public=True, required_label="development", review_summary=True,
    allowed=frozenset({"created", "published", "updated", "slug", "summary", "tags", "aliases"}),
)
# _property-schema.md의 공통 필드와 각 노트 유형 절. 경로가 겹치면 가장 구체적인 규칙 하나를 쓴다.
# 규칙 사이의 상속은 없고, 생략한 값은 FolderRule의 공통 기본값을 쓴다.
FOLDER_RULES = {
    "": FolderRule(),  # 별도 규칙이 없는 폴더에만 적용한다.
    "01_Slipbox/": FolderRule(required=("type", "status"), public=True),  # Slipbox
    "20_Projects/blog/": FolderRule(public=True, review_summary=True),  # Blog Posts: 공개 조건은 별도 검사
    "30_Resources/References/Articles/": FolderRule(required=("source", "published", "status")),
    "30_Resources/References/Clippings/": FolderRule(required=("status",)),
    "30_Resources/Development/DevLog/": FolderRule(created_key="date"),  # DevLog
    "30_Resources/Development/Concepts/": DEVELOPMENT_RULE,
    "30_Resources/Development/Troubleshooting/": DEVELOPMENT_RULE,
    "30_Resources/Development/Tools/": DEVELOPMENT_RULE,
}
DEV_ROOT = "30_Resources/Development/"  # 이 폴더 바로 아래에는 노트를 두지 않는다 (AGENTS).
# 공개 노트의 날짜 규칙은 사이트 저장소 src/lib/dates.mjs와 같다. 한쪽을 바꾸면 다른 쪽도 고친다.
PUBLIC_DATE_FIELDS = ("created", "published", "updated")
DAY_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
KST = timezone(timedelta(hours=9))
# summary는 답·질문·용도·관점을 말하는 문장이다. 노트가 하는 일로 끝나면 보고한다. 표현 목록이 아니라 세 가지 형태로 본다.
# 목록으로 맞춘 이전 정규식은 만들 때 보지 않은 summary에서 "~한 운영 경험"을 하나도 잡지 못했다(2026-09-24 검증).
SUMMARY_TAIL_RE = re.compile(
    # 노트의 활동을 서술어로 쓴다: "~를 정리한다", "~를 살펴본다"
    r"((정리|확인|점검|설명|소개|제안|제시|해석|성찰|분석|기록)(한다|했다)|다룬다|살펴본다|돌아본다)\.?$"
    # 서술어 없이 관형형 뒤 명사구로 끝난다: "~한 방식과 기준". 마지막 어절이 서술·의문 어미면 제외한다
    r"|[한은는던된할]\s(?:\S+\s){0,3}\S*[^다요까죠가\s.]\.?$"
    # 글이 스스로를 장르 명사로 부른다: "~다룬 구현 기록", "~정리한 글이다"
    r"|(글|기록|후기|과정|방법|경험|사례)(이다)?\.?$"
)
ORPHAN_EXCLUDE = (             # 날짜 기반 노트 — 위키링크 연결이 목적이 아니라 orphan 판정 제외
    "10_Periodic Notes/",
    "30_Resources/Development/DevLog/",
)
BASE_INVALID_KEYS = {"sortBy"}  # .base 파일에 없는 키인데 흔히 착각해서 쓰는 것들. 발견되는 대로 추가.

# 재사용 판정 — "이 영구 노트가 다른 맥락에서 다시 쓰였는가"를 센다.
# 출처(이 자료에서 노트가 나왔다)는 재사용이 아니다. X에서 파생된 것은 X를 입증하지 못한다.
REUSE_PROVENANCE_MARKERS = (   # 링크 옆 설명에 이 표현이 있으면 출처로 보고 재사용에서 뺀다
    "로 승격", "으로 승격",
    "압축한 영구 노트", "정제한 영구 노트", "정제한 결과",
    "에서 출발한",
    "출처 후보",
)
# 맨 "승격"·"출발점"은 마커에 넣지 않는다. 본문 개념어로도 쓰이고,
# "출발점"은 화자가 누구냐에 따라 출처와 재사용이 뒤집힌다.

# 보류 목록 — 사용자가 거부·보류한 의미 검토 후보를 다음 lint에서 다시 제안하지 않는다.
# 키에는 판단이 기댄 값까지 넣는다. 그 값이 바뀌면 키가 달라져 자동으로 다시 제안된다.
# 형식 오류(frontmatter·base)는 결정적으로 고칠 수 있으므로 보류 대상이 아니다.
HOLD_KEYS = {
    "dead_link": ("source", "target"),
    "broken_anchor": ("source", "target", "anchor"),
    "orphan": ("path",),
    "hub_gap": ("path",),
    "used_in": ("note", "source"),
    "summary": ("path", "summary"),
    "title": ("path",),
}
DEFAULT_HOLDS = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir, "holds.json")
# ───────────────────────────────────────────────────────────

WIKILINK_RE = re.compile(r"!?\[\[([^\[\]]+?)\]\]")
FENCED_RE = re.compile(r"```.*?```", re.DOTALL)
INLINE_CODE_RE = re.compile(r"`[^`\n]*`")
KEY_RE = re.compile(r"^([A-Za-z_][\w-]*):\s*(.*)$")
LIST_ITEM_RE = re.compile(r"^\s*-\s+(.+)$")
BASE_KEY_RE = re.compile(r"^\s*([A-Za-z_][\w-]*)\s*:")
PERIODIC_PLACEHOLDER_RE = re.compile(
    r"^(?:\d{4}-\d{2}(?:-\d{2})?|\d{4}-W\d{2})$"
)
# 블록 ID는 줄 끝에서만 인식된다 — 단독 줄(`^id`)과 텍스트 뒤(`본문 ^id`) 둘 다 유효하다.
# 줄 앞에 두면(`^id 본문`) Obsidian이 블록 ID로 보지 않는다.
BLOCK_ANCHOR_RE = re.compile(r"(?:^|\s)\^([A-Za-z0-9-]+)[ \t]*$")
ANCHOR_LINK_RE = re.compile(r"!?\[\[([^\[\]]+?)\]\]")


def folder_rule(rel):
    """끝의 /까지 일치하는 가장 구체적인 규칙을 선택한다."""
    prefix = max((prefix for prefix in FOLDER_RULES if rel.startswith(prefix)), key=len)
    return prefix, FOLDER_RULES[prefix]


def scalar_value(raw):
    """사이트 파서처럼 null 표기와 따옴표로 감싼 문자열을 구분한다."""
    if raw is None:
        return None
    value = raw.strip()
    if value in ("null", "~"):
        return None
    quoted = re.fullmatch(r"(['\"])(.*)\1", value, re.DOTALL)
    return quoted.group(2) if quoted else value


def has_public_blog_page(rel, scalars):
    # 블로그 초안과 아웃라인은 사이트 주소가 없으므로 slug와 날짜를 검사하지 않는다. 다른 폴더는 표의 설정을 따른다.
    return (not rel.startswith("20_Projects/blog/")
            or scalar_value(scalars.get("status")) == "published"
            or scalar_value(scalars.get("type")) == "series")


def needs_project_status(rel, scalars):
    return rel.startswith("20_Projects/") and scalars.get("project_id") and not scalars.get("status")


def kst_today():
    # 사이트 빌드와 같은 기준일이다. CI는 UTC로 돌지만 날짜는 한국 날짜로 센다.
    return datetime.now(KST).date().isoformat()


def is_calendar_day(value):
    # fromisoformat은 20260910 같은 다른 ISO 형식도 받으므로 모양을 먼저 확인한다.
    if not DAY_RE.match(value):
        return False
    try:
        date.fromisoformat(value)
    except ValueError:
        return False
    return True


def date_issues(scalars, lists, today):
    """사이트 빌드가 멈추는 날짜를 찾는다. created 누락은 필수 필드 검사가 따로 알린다."""
    issues = []
    for field in PUBLIC_DATE_FIELDS:
        # 이 파서는 줄 목록을 lists에만 담고 scalars에는 빈 값을 둔다. 사이트는 목록 날짜를 거부한다.
        if lists.get(field):
            issues.append(f"날짜 형식 오류 ({field}): 날짜 하나만 적는다")
            continue
        # 따옴표 없는 null·~만 빈 값이다. "null"과 짝이 맞지 않는 따옴표는 문자열로 검증한다.
        value = scalar_value(scalars.get(field))
        if value is None or value == "":
            continue
        if not is_calendar_day(value):
            issues.append(f"날짜 형식 오류 ({field}): {value}")
        elif value > today:
            issues.append(f"미래 날짜 ({field}): {value} (오늘 {today})")
    return issues


SUGGEST_SUMMARY = "summary 꼬리 검토: 답·질문·용도인지 문맥 확인"
SUGGEST_TITLE = "제목의 ' - ' 검토: 실제 부제인지 오류 문자열인지 확인"
SUGGESTION_HOLD_KIND = {SUGGEST_SUMMARY: "summary", SUGGEST_TITLE: "title"}


def summary_text(scalars):
    return (scalars or {}).get("summary", "").strip().strip("'\"")


def check_frontmatter(rel, scalars, lists, today=None):
    """한 노트의 형식 오류와 문체 제안을 분리해 반환한다."""
    issues, suggestions = [], []
    if scalars is None:
        issues.append("frontmatter 블록 없음")
    else:
        prefix, rule = folder_rule(rel)
        if not scalar_value(scalars.get(rule.created_key)):
            issues.append(f"필수 필드 누락: {rule.created_key}")
        for tag in lists.get("tags", []):
            if tag.startswith("#"):
                issues.append(f"태그에 # 포함: {tag}")
        for key in rule.required:
            if not scalars.get(key):
                issues.append(f"필수 필드 누락 ({rule.required_label or prefix}): {key}")
        if needs_project_status(rel, scalars):
            issues.append("필수 필드 누락 (project): status")
        public_page = rule.public and has_public_blog_page(rel, scalars)
        # 한글 제목의 긴 인코딩 주소를 피하고, 외부 링크가 걸리기 전에 주소를 정하도록 slug를 미리 확인한다.
        if public_page and not scalars.get("slug"):
            issues.append("공개 노트 slug 없음")
        # 날짜 오류는 사이트 빌드를 멈추고 CI 실패로만 드러나므로 쓰는 단계에서 먼저 알린다.
        if public_page:
            issues.extend(date_issues(scalars, lists, today or kst_today()))
        if rule.allowed is not None:
            for key in scalars:
                if key not in rule.allowed:
                    issues.append(f"스키마에 없는 필드: {key}")
        if rule.review_summary and SUMMARY_TAIL_RE.search(summary_text(scalars)):
            suggestions.append(SUGGEST_SUMMARY)
        # 구두점만으로 제목의 의미를 판정할 수 없으므로 오류가 아닌 문맥 검토 제안으로 남긴다.
        if rel.startswith("30_Resources/Development/Troubleshooting/") and " - " in os.path.basename(rel):
            suggestions.append(SUGGEST_TITLE)
    if rel.startswith(DEV_ROOT) and rel.count("/") == DEV_ROOT.count("/"):
        issues.append("Development 루트 노트: Concepts·Troubleshooting·Tools 중 하나로")
    return issues, suggestions


def nfc(s):
    return unicodedata.normalize("NFC", s)


def split_frontmatter(text):
    if not text.startswith("---\n"):
        return None, text
    end = text.find("\n---", 4)
    if end == -1:
        return None, text
    return text[4:end].splitlines(), text[end + 4:]


def parse_frontmatter(lines):
    """최상위 스칼라 키 + 리스트 키 항목을 뽑는 미니 파서 (stdlib에 YAML 없음)."""
    scalars, lists = {}, {}
    current = None
    for line in lines:
        m = KEY_RE.match(line)
        if m:
            current = m.group(1)
            val = m.group(2).strip()
            scalars[current] = val
            if val.startswith("[") and val.endswith("]"):
                lists[current] = [t.strip().strip("'\"") for t in val[1:-1].split(",") if t.strip()]
        elif current is not None:
            lm = LIST_ITEM_RE.match(line)
            if lm:
                lists.setdefault(current, []).append(lm.group(1).strip().strip("'\""))
    return scalars, lists


def extract_links_with_context(body):
    """(target, 링크가 있던 줄) 목록.

    재사용 판정은 링크 자체가 아니라 링크 옆에 적은 관계 설명을 봐야 해서
    줄 텍스트가 필요하다. 관계 설명은 본문 문장이나 ``## 연관된 노트``
    항목 어느 쪽에도 있을 수 있다.
    """
    body = FENCED_RE.sub("", body)
    body = INLINE_CODE_RE.sub("", body)
    out = []
    for line in body.splitlines():
        for m in WIKILINK_RE.finditer(line):
            # 표 안의 위키링크는 파이프를 \| 로 이스케이프함 — 풀어준 뒤 분리
            t = m.group(1).replace("\\|", "|").split("|")[0].split("#")[0].strip()
            if t:
                out.append((nfc(t), line.strip()))
    return out


def extract_links(body):
    return [t for t, _ in extract_links_with_context(body)]


def extract_block_anchors(body):
    """이 문서가 실제로 정의한 블록 ID 집합."""
    body = FENCED_RE.sub("", body)
    return {m.group(1) for line in body.splitlines()
            for m in [BLOCK_ANCHOR_RE.search(line)] if m}


def extract_anchor_links(body):
    """(대상 문서, 블록 ID) 목록 — `[[문서#^id]]` 형태만.

    블록 링크는 앵커가 없어도 문서로는 해석되므로 링크가 살아 있는 것처럼 보인다.
    그래서 죽은 링크 검사만으로는 잡히지 않고 출처 정밀도가 조용히 문서 단위로 퇴화한다.
    """
    body = FENCED_RE.sub("", body)
    body = INLINE_CODE_RE.sub("", body)
    out = []
    for m in ANCHOR_LINK_RE.finditer(body):
        raw = m.group(1).replace("\\|", "|").split("|")[0].strip()
        if "#^" not in raw:
            continue
        target, _, anchor = raw.partition("#^")
        target, anchor = target.strip(), anchor.strip()
        if target and anchor:
            out.append((nfc(target), anchor))
    return out


def reuse_source_kind(rel):
    if rel.startswith("00_Inbox/"):
        return "inbox"
    if rel.startswith("30_Resources/References/"):
        return "reference"
    if rel.startswith("20_Projects/blog/"):
        return "blog"
    if rel.startswith("20_Projects/"):
        return "project"
    return "operational"          # 운영 문서·MOC 등 — 자료가 아니라 적용처다


def classify_reuse_edge(kind, marked, mutual):
    """(판정, 사유). 판정은 reuse | excluded | pending."""
    if kind == "inbox":
        # README 원칙: Inbox는 탐색 단서일 뿐 현재 입장의 근거가 아니다.
        # Inbox를 벗어나 승격·흡수될 때 다시 판정한다.
        return "pending", "Inbox 초안 — 근거로 세지 않음"
    if marked:
        return "excluded", "출처 표지 문구"
    if kind == "blog":
        # 블로그는 노트를 낳기도 하고 인용하기도 해서 상호 여부로 갈리지 않는다.
        # 표지 문구가 없으면 인용으로 본다.
        return "reuse", "블로그 인용"
    if mutual and kind == "reference":
        return "excluded", "상호 + 읽은 자료"
    if mutual:
        return "reuse", "상호지만 상대가 적용처"
    return "reuse", "단방향"


def is_scanned(rel):
    parts = rel.split("/")
    if len(parts) == 1:  # 루트 인프라 문서 (README/CLAUDE/AGENTS) — 노트 아님
        return False
    if parts[0] in SCAN_EXCLUDE_TOP:
        return False
    # _ 접두 규칙은 파일명뿐 아니라 중간 폴더에도 적용 (예: blog/_candidates/)
    return not any(p.startswith("_") for p in parts)


def is_base_scanned(rel):
    # .base 대시보드는 관례상 파일명이 _로 시작하므로(_index.base 등) is_scanned의
    # _ 제외 규칙을 그대로 쓰면 전부 걸러진다 — 최상위 제외 폴더만 적용한다.
    parts = rel.split("/")
    top = parts[0] if len(parts) > 1 else None
    return top not in SCAN_EXCLUDE_TOP


def is_periodic_placeholder(source, target):
    return (
        source.startswith("10_Periodic Notes/")
        and PERIODIC_PLACEHOLDER_RE.fullmatch(target) is not None
    )


def is_series_placeholder(source, fm_cache):
    """진행 중·잠정 중단 시리즈 허브의 미해결 링크는 예정 글로 취급한다."""
    scalars, _ = fm_cache.get(source, (None, {}))
    if scalars is None:
        return False
    note_type = scalars.get("type", "").strip("'\"")
    status = scalars.get("status", "").strip("'\"")
    return note_type == "series" and status != "completed"


def scan_base_issues(root, all_base):
    issues = []
    for rel in all_base:
        try:
            with open(os.path.join(root, rel), encoding="utf-8") as f:
                lines = f.read().splitlines()
        except (OSError, UnicodeDecodeError):
            continue
        for i, line in enumerate(lines, start=1):
            m = BASE_KEY_RE.match(line)
            if m and m.group(1) in BASE_INVALID_KEYS:
                issues.append({"path": rel, "line": i, "key": m.group(1)})
    return issues


def resolve_by_suffix(target, all_files):
    """폴더가 붙은 링크(`assets/그림.svg`)는 Obsidian처럼 경로 끝부분이 일치하는 파일로 푼다."""
    if "/" not in target:
        return set()
    suffix = "/" + target
    return {p for p in all_files
            if p.endswith(suffix) or (p.endswith(".md") and p[:-3].endswith(suffix))}


def recorded_reuse(lists, target_index):
    """used_in에 적힌 값을 노트 경로로 푼다. (풀린 경로 집합, 풀리지 않은 원문 목록)."""
    resolved, unresolved = set(), []
    for raw in lists.get("used_in", []):
        m = WIKILINK_RE.search(raw)
        name = (m.group(1) if m else raw).replace("\\|", "|").split("|")[0].split("#")[0].strip()
        hit = target_index.get(nfc(name))
        if hit:
            resolved.update(hit)
        else:
            unresolved.append(raw)
    return resolved, unresolved


def hold_key(kind, item):
    return (kind,) + tuple(nfc(item[field]) for field in HOLD_KEYS[kind])


def load_holds(path):
    """(유효한 보류 목록, 오류 목록). 파일이 없으면 둘 다 비어 있다."""
    if not os.path.exists(path):
        return [], []
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
    except (OSError, ValueError) as e:
        return [], [{"error": f"보류 목록을 읽지 못함: {e}"}]
    entries = data.get("holds") if isinstance(data, dict) else None
    if not isinstance(entries, list):
        return [], [{"error": "최상위는 {\"holds\": [...]} 형식이어야 한다"}]
    holds, errors = [], []
    for i, entry in enumerate(entries):
        fields = HOLD_KEYS.get(entry.get("kind")) if isinstance(entry, dict) else None
        if not fields or not all(isinstance(entry.get(k), str) and entry[k] for k in fields):
            errors.append({"index": i, "hold": entry, "error": "알 수 없는 kind이거나 키 필드가 비어 있음"})
        else:
            holds.append(entry)
    return holds, errors


class Holds:
    """발견 항목을 보류 목록과 대조한다. 맞은 보류는 held, 끝까지 안 맞은 보류는 stale로 보고한다."""

    def __init__(self, holds):
        self.index = {hold_key(h["kind"], h): h for h in holds}
        self.matched = {}

    def take(self, kind, item):
        key = hold_key(kind, item)
        if key not in self.index:
            return False
        self.matched[key] = self.index[key]
        return True

    def held(self):
        return list(self.matched.values())

    def stale(self):
        return [h for key, h in self.index.items() if key not in self.matched]


def parse_args(argv):
    root, holds_path = ".", DEFAULT_HOLDS
    args = list(argv)
    while args:
        arg = args.pop(0)
        if arg == "--holds" and args:
            holds_path = args.pop(0)
        else:
            root = arg
    return os.path.abspath(root), holds_path


def main():
    root, holds_path = parse_args(sys.argv[1:])
    hold_list, hold_errors = load_holds(holds_path)
    holds = Holds(hold_list)

    all_md, all_base, all_files, resolve, target_index = [], [], [], set(), {}
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if not d.startswith(".")]
        for fn in filenames:
            rel = nfc(os.path.relpath(os.path.join(dirpath, fn), root))
            all_files.append(rel)
            if fn.endswith(".base"):
                all_base.append(rel)
            if fn.endswith(".md"):
                all_md.append(rel)
                keys = {nfc(fn[:-3]), rel, rel[:-3]}
            else:
                keys = {nfc(fn), rel}
            resolve.update(keys)
            if fn.endswith(".md"):
                for k in keys:
                    target_index.setdefault(k, set()).add(rel)

    # 1차: frontmatter 캐시 + aliases를 해석 집합에 등록
    fm_cache, body_cache = {}, {}
    for rel in all_md:
        try:
            with open(os.path.join(root, rel), encoding="utf-8") as f:
                text = f.read()
        except (OSError, UnicodeDecodeError):
            continue
        fm_lines, body = split_frontmatter(text)
        body_cache[rel] = body
        if fm_lines is None:
            fm_cache[rel] = (None, {})
            continue
        scalars, lists = parse_frontmatter(fm_lines)
        fm_cache[rel] = (scalars, lists)
        for alias in lists.get("aliases", []):
            a = nfc(alias)
            resolve.add(a)
            target_index.setdefault(a, set()).add(rel)

    # 2차: 링크 그래프 (in-link는 Archive 포함 전체에서 수집)
    in_degree = {rel: 0 for rel in all_md}
    out_count, dead_links, blog_to_slipbox_edges = {}, [], set()
    out_targets = {rel: set() for rel in all_md}
    slipbox_inbound = {}          # tgt → {src: [링크가 있던 줄]}
    for rel in all_md:
        links = extract_links_with_context(body_cache.get(rel, ""))
        out_count[rel] = len(links)
        for t, line in links:
            hit = target_index.get(t)
            if not hit and t not in resolve:
                found = resolve_by_suffix(t, all_files)
                if not found:
                    if is_scanned(rel):
                        dead_links.append({"source": rel, "target": t})
                    continue
                hit = {p for p in found if p.endswith(".md")}  # 비어 있으면 첨부 파일로 풀린 링크
            if hit:
                for tgt in hit:
                    if tgt != rel:
                        in_degree[tgt] += 1
                        out_targets[rel].add(tgt)
                    if (
                        rel.startswith("20_Projects/blog/")
                        and tgt.startswith("01_Slipbox/")
                    ):
                        blog_to_slipbox_edges.add((rel, tgt))
                    if (
                        tgt.startswith("01_Slipbox/")
                        and not rel.startswith("01_Slipbox/")
                        and is_scanned(rel)
                    ):
                        slipbox_inbound.setdefault(tgt, {}).setdefault(rel, []).append(line)

    scanned = [rel for rel in all_md if is_scanned(rel)]

    # 3차: 블록 앵커 — 대상 문서는 해석되는데 그 안에 블록 ID가 없는 링크
    anchors = {rel: extract_block_anchors(body_cache.get(rel, "")) for rel in all_md}
    broken_anchors = []
    for rel in scanned:
        for target, anchor in extract_anchor_links(body_cache.get(rel, "")):
            hit = target_index.get(target)
            if not hit:
                continue          # 문서 자체가 미해석이면 dead_links가 이미 잡는다
            if not any(anchor in anchors.get(tgt, set()) for tgt in hit):
                item = {"source": rel, "target": sorted(hit)[0], "anchor": anchor}
                if not holds.take("broken_anchor", item):
                    broken_anchors.append(item)

    orphans = [
        {"path": rel, "slipbox": rel.startswith("01_Slipbox/")}
        for rel in scanned
        if out_count.get(rel, 0) == 0 and in_degree.get(rel, 0) == 0
        and not rel.startswith(ORPHAN_EXCLUDE)
        and not holds.take("orphan", {"path": rel})
    ]

    # 허브 공백: 01_Slipbox의 permanent 노트 중 어느 허브(type: hub)도 링크하지 않는 노트.
    # 허브가 모든 노트를 실어야 한다는 뜻은 아니다 — 등록 여부를 review-zettelkasten이
    # 판단하도록 목록만 보고한다.
    def note_type(rel):
        scalars, _ = fm_cache.get(rel, (None, {}))
        return (scalars or {}).get("type", "").strip("'\"")

    hubs = [rel for rel in scanned if rel.startswith("01_Slipbox/") and note_type(rel) == "hub"]
    hub_targets = set().union(*(out_targets[h] for h in hubs)) if hubs else set()
    hub_gaps = [
        {"path": rel, "status": (fm_cache[rel][0] or {}).get("status", "").strip("'\"")}
        for rel in scanned
        if rel.startswith("01_Slipbox/") and note_type(rel) == "permanent"
        and rel not in hub_targets
        and not holds.take("hub_gap", {"path": rel})
    ]

    frontmatter_issues = []
    style_suggestions = []
    today = kst_today()
    for rel in scanned:
        scalars, lists = fm_cache.get(rel, (None, {}))
        issues, suggestions = check_frontmatter(rel, scalars, lists, today=today)
        if issues:
            frontmatter_issues.append({"path": rel, "issues": issues})
        summary = summary_text(scalars)
        suggestions = [
            s for s in suggestions
            if not holds.take(SUGGESTION_HOLD_KIND[s], {"path": rel, "summary": summary})
        ]
        if suggestions:
            entry = {"path": rel, "suggestions": suggestions}
            if SUGGEST_SUMMARY in suggestions:
                entry["summary"] = summary  # 보류 목록에 옮겨 적을 키 값
            style_suggestions.append(entry)

    base_scanned = [rel for rel in all_base if is_base_scanned(rel)]
    base_issues = scan_base_issues(root, base_scanned)

    slipbox_orphans = sum(1 for orphan in orphans if orphan["slipbox"])
    non_slipbox_orphans = len(orphans) - slipbox_orphans
    dead_links = [item for item in dead_links if not holds.take("dead_link", item)]
    periodic_placeholders = [
        item for item in dead_links
        if is_periodic_placeholder(item["source"], item["target"])
    ]
    series_placeholders = [
        item for item in dead_links
        if is_series_placeholder(item["source"], fm_cache)
    ]
    meaning_dead_links = [
        item for item in dead_links
        if not is_periodic_placeholder(item["source"], item["target"])
        and not is_series_placeholder(item["source"], fm_cache)
    ]
    reused_blog_notes = {source for source, _ in blog_to_slipbox_edges}
    reused_slipbox_notes = {target for _, target in blog_to_slipbox_edges}

    # 재사용 판정 — 영구 노트가 Slipbox 밖에서 다시 쓰였는가.
    # type 필터(permanent/hub)는 여기서 걸지 않는다. 기계 집계만 하고
    # 의미 구분은 Base 뷰와 review-zettelkasten이 맡는다.
    slipbox_notes = sorted(rel for rel in scanned if rel.startswith("01_Slipbox/"))
    reuse_by_note = []
    reuse_edges = excluded_edges = pending_edges = 0
    for tgt in slipbox_notes:
        scalars, lists = fm_cache.get(tgt, (None, {}))
        entry = {
            "path": tgt,
            "status": (scalars or {}).get("status", "").strip("'\""),
            "reuse_count": 0,
            "reused_by": [],
            "excluded": [],
            "pending": [],
            "used_in_candidates": [],
            "recorded_only": [],
        }
        for src, lines in sorted(slipbox_inbound.get(tgt, {}).items()):
            verdict, why = classify_reuse_edge(
                reuse_source_kind(src),
                any(m in " ".join(lines) for m in REUSE_PROVENANCE_MARKERS),
                src in out_targets.get(tgt, set()),
            )
            record = {"path": src, "reason": why}
            if verdict == "reuse":
                entry["reused_by"].append(record)
                reuse_edges += 1
            elif verdict == "excluded":
                entry["excluded"].append(record)
                excluded_edges += 1
            else:
                entry["pending"].append(record)
                pending_edges += 1
        entry["reuse_count"] = len(entry["reused_by"])
        # used_in은 사람이 승인한 재사용 기록이다. 스캐너가 찾은 재사용 중 아직 기록되지 않은 것만
        # 후보로 내고, 링크 없이 기록된 재사용은 결함이 아니라 스캐너가 볼 수 없는 기록으로 알린다.
        recorded, unresolved = recorded_reuse(lists, target_index)
        detected = {r["path"] for r in entry["reused_by"]}
        entry["used_in_candidates"] = [
            src for src in sorted(detected - recorded)
            if not holds.take("used_in", {"note": tgt, "source": src})
        ]
        entry["recorded_only"] = (
            [{"path": p} for p in sorted(recorded - detected)]
            + [{"value": v, "unresolved": True} for v in unresolved]
        )
        reuse_by_note.append(entry)

    reuse_by_note.sort(key=lambda e: (-e["reuse_count"], e["path"]))
    notes_reused = sum(1 for e in reuse_by_note if e["reuse_count"] > 0)
    seedling_with_reuse = sum(
        1 for e in reuse_by_note if e["reuse_count"] > 0 and e["status"] == "seedling"
    )
    used_in_candidates = sum(len(e["used_in_candidates"]) for e in reuse_by_note)
    recorded_only = sum(len(e["recorded_only"]) for e in reuse_by_note)
    held, stale_holds = holds.held(), holds.stale()

    print(json.dumps({
        "stats": {
            "vault_root": root,
            "md_total": len(all_md),
            "notes_scanned": len(scanned),
            "orphans": len(orphans),
            "dead_links": len(dead_links),
            "periodic_placeholders": len(periodic_placeholders),
            "series_placeholders": len(series_placeholders),
            "frontmatter_issues": len(frontmatter_issues),
            "broken_anchors": len(broken_anchors),
            "hub_gaps": len(hub_gaps),
            "base_total": len(all_base),
            "base_issues": len(base_issues),
            "reuse": {
                "blog_to_slipbox_edges": len(blog_to_slipbox_edges),
                "blog_notes_with_slipbox_refs": len(reused_blog_notes),
                "slipbox_notes_reused_by_blog": len(reused_slipbox_notes),
                "slipbox_notes_total": len(slipbox_notes),
                "slipbox_notes_reused": notes_reused,
                "slipbox_notes_unused": len(slipbox_notes) - notes_reused,
                "reuse_edges": reuse_edges,
                "excluded_edges": excluded_edges,
                "pending_edges": pending_edges,
                "used_in_candidates": used_in_candidates,
                "recorded_only": recorded_only,
            },
            "held": len(held),
            "stale_holds": len(stale_holds),
        },
        "priorities": {
            "mechanical": {
                "frontmatter_issues": len(frontmatter_issues),
                "base_issues": len(base_issues),
                "hold_errors": len(hold_errors),
            },
            "meaning_review": {
                "style_suggestions": len(style_suggestions),
                "slipbox_orphans": slipbox_orphans,
                "dead_links": len(meaning_dead_links),
                "broken_anchors": len(broken_anchors),
                "used_in_candidates": used_in_candidates,
            },
            "informational": {
                "non_slipbox_orphans": non_slipbox_orphans,
                "periodic_placeholders": len(periodic_placeholders),
                "series_placeholders": len(series_placeholders),
                "seedling_with_reuse": seedling_with_reuse,
                "pending_reuse_edges": pending_edges,
                "recorded_only": recorded_only,
                "hub_gaps": len(hub_gaps),
                "held": len(held),
                "stale_holds": len(stale_holds),
            },
        },
        "reuse_by_note": reuse_by_note,
        "orphans": orphans,
        "dead_links": dead_links,
        "broken_anchors": broken_anchors,
        "hub_gaps": hub_gaps,
        "periodic_placeholders": periodic_placeholders,
        "series_placeholders": series_placeholders,
        "frontmatter_issues": frontmatter_issues,
        "style_suggestions": style_suggestions,
        "base_issues": base_issues,
        "held": held,
        "stale_holds": stale_holds,
        "hold_errors": hold_errors,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
