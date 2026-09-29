"""모의 심사에 넘길 텍스트를 전용본 HTML에서 추출한다.

사용법: python3 resume_text.py <전용본.html> <출력.txt>
"""

import html
import re
import sys


def extract(source):
    text = re.sub(r"<head>.*?</head>", "", source, flags=re.S)
    text = re.sub(r'<div class="print-hint">.*?</div>', "", text, flags=re.S)
    text = re.sub(r"</(li|div|h1|h2|section|header)>", "\n", text)
    text = re.sub(r"<li>", "- ", text)
    text = html.unescape(re.sub(r"<[^>]+>", " ", text))
    lines = [re.sub(r"\s+", " ", line).strip() for line in text.split("\n")]
    return "\n".join(line for line in lines if line) + "\n"


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    with open(sys.argv[1], encoding="utf-8") as f:
        result = extract(f.read())
    with open(sys.argv[2], "w", encoding="utf-8") as f:
        f.write(result)
    print(f"{result.count(chr(10))} lines -> {sys.argv[2]}")
