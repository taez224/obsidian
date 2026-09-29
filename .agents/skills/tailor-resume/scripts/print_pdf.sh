#!/usr/bin/env bash
# 전용본 HTML을 헤드리스 Chrome으로 A4 PDF로 인쇄하고, 쪽수와 쪽별 인쇄 여유(mm)를 출력한다.
# 사용법: print_pdf.sh <전용본.html> <출력.pdf>
# 출력 PDF는 임시 작업 폴더에 둔다. 전용본 폴더에는 Git으로 복구할 수 없는 제출본 PDF가 있어서,
# 이미 있는 파일은 PRINT_PDF_OVERWRITE=1이 없으면 덮어쓰지 않는다.
# Chrome 플래그는 최소로 유지한다. --virtual-time-budget이나 --user-data-dir를 붙이면
# 프로세스가 끝나지 않았다(2026-09-29).
# 여유는 pdftotext -bbox가 낸 쪽별 마지막 글자의 yMax로 계산하고, @page 하단 여백은 10mm로 가정한다.
# 1쪽 여유가 10mm 미만이면 warn 줄을 출력한다. 넘침 판정은 SKILL.md가 하므로 종료 코드는 바꾸지 않는다.
# 종료 코드: 0 = 2쪽이고 폰트 정상, 1 = 인쇄 실패, 쪽수 불일치, 폰트 누락, 2 = 사용법 오류.
set -euo pipefail

if [ $# -ne 2 ]; then
  echo "usage: $0 <resume.html> <output.pdf>" >&2
  exit 2
fi

chrome="${CHROME:-/Applications/Google Chrome.app/Contents/MacOS/Google Chrome}"
html="$(cd "$(dirname "$1")" && pwd)/$(basename "$1")"
out="$2"

case "$out" in
  *.pdf) ;;
  *) echo "output path must end with .pdf: $out" >&2; exit 2 ;;
esac
if [ -e "$out" ] && [ "${PRINT_PDF_OVERWRITE:-}" != "1" ]; then
  echo "refusing to overwrite existing file: $out (set PRINT_PDF_OVERWRITE=1 to allow)" >&2
  exit 2
fi
rm -f "$out"

"$chrome" --headless=new --no-pdf-header-footer --print-to-pdf="$out" "file://$html" >/dev/null 2>&1 &
pid=$!
for _ in $(seq 1 30); do
  if ! kill -0 "$pid" 2>/dev/null; then break; fi
  sleep 1
done
if kill -0 "$pid" 2>/dev/null; then
  kill "$pid" 2>/dev/null || true
  echo "chrome did not exit within 30s" >&2
  exit 1
fi
[ -s "$out" ] || { echo "no PDF written" >&2; exit 1; }

python3 - "$out" "$html" <<'EOF'
import re
import subprocess
import sys

pdf, html = sys.argv[1], sys.argv[2]
BOTTOM_MARGIN_PT = 28.35  # @page 하단 여백 10mm

pages = len(re.findall(rb"/Type\s*/Page[^s]", open(pdf, "rb").read()))
print(f"pages: {pages}")
ok = pages == 2


def run(*cmd):
    try:
        return subprocess.run(cmd, capture_output=True, text=True, check=True).stdout
    except (FileNotFoundError, subprocess.CalledProcessError):
        return None


bbox = run("pdftotext", "-bbox", pdf, "-")
if bbox is None:
    print("spare: skipped (pdftotext를 찾지 못했거나 실패했다)")
else:
    for n, page in enumerate(re.split(r"<page ", bbox)[1:], 1):
        height = float(re.search(r'height="([\d.]+)"', page).group(1))
        ymax = [float(v) for v in re.findall(r'yMax="([\d.]+)"', page)]
        if not ymax:
            print(f"page {n}: no text")
            continue
        spare = (height - BOTTOM_MARGIN_PT - max(ymax)) / 72 * 25.4
        print(f"page {n}: spare {spare:.1f}mm")
        if n == 1 and spare < 10:
            print("warn: 1쪽 여유가 10mm 미만이다 (전용본 기준은 10mm 이상)")

if b"pretendard" in open(html, "rb").read().lower():
    fonts = run("pdffonts", pdf)
    if fonts is None:
        print("pretendard: unchecked (pdffonts를 찾지 못했거나 실패했다)")
    elif "pretendard" in fonts.lower():
        print("pretendard: embedded")
    else:
        print("pretendard: MISSING (폰트를 받지 못했다. 이 측정값은 쓰지 않는다)")
        ok = False
sys.exit(0 if ok else 1)
EOF
