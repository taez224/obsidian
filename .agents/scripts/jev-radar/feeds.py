"""RSS 목록을 출처별로 고르게 고른다. 품질·관련성 판정은 하지 않는다."""
from collections import defaultdict
from datetime import date
import re


def balanced(items, limit, day=None, *, newest=True):
    groups = defaultdict(list)
    for item in items:
        groups[item["source"]].append(item)
    names = sorted(groups) if day else list(groups)
    if not names:
        return []
    offset = (date.fromisoformat(day).toordinal() // 7) % len(names) if day else 0
    names = names[offset:] + names[:offset]
    def published(item):
        match = re.search(r"\d{4}-\d{2}-\d{2}$", item.get("line", ""))
        return item.get("date") or (match.group(0) if match else "")

    if newest:
        for group in groups.values():
            group.sort(key=published, reverse=True)
    result, seen = [], set()
    while len(result) < limit and any(groups.values()):
        for name in names:
            if not groups[name]:
                continue
            item = groups[name].pop(0)
            url = item["url"].split("#")[0].rstrip("/")
            if url in seen:
                continue
            result.append(item)
            seen.add(url)
            if len(result) == limit:
                break
    return result
