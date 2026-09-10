"""Validate local Markdown pointers in the agent entrypoint and common guides."""

from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit

LINK = re.compile(r"\[[^\]\n]+\]\((?:<([^>]+)>|([^\s)]+))\)")


def check_guides(root):
    root = Path(root)
    sources = [root / "AGENTS.md", *sorted((root / ".agents/guides").glob("*.md"))]
    errors = []
    for source in sources:
        if not source.is_file():
            errors.append(f"Missing guide: {source.relative_to(root)}")
            continue
        for number, line in enumerate(source.read_text(encoding="utf-8").splitlines(), 1):
            for match in LINK.finditer(line):
                target = match.group(1) or match.group(2)
                url = urlsplit(target)
                if url.scheme or url.netloc or not url.path:
                    continue
                resolved = source.parent / unquote(url.path)
                if not resolved.exists():
                    errors.append(f"{source.relative_to(root)}:{number}: missing target {target}")
    return errors


if __name__ == "__main__":
    root = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path(__file__).resolve().parents[2]
    errors = check_guides(root)
    if errors:
        print("\n".join(errors))
        sys.exit(1)
    print("Agent guide links: OK")
