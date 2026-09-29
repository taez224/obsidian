#!/usr/bin/env bash
# Print a resume HTML to A4 PDF with headless Chrome and report the page count.
# Usage: print_pdf.sh <resume.html> <output.pdf>
# Write the PDF to a scratch directory, not next to the resume HTML. The script
# refuses to overwrite an existing file unless PRINT_PDF_OVERWRITE=1, because
# submitted PDFs in the resume folder are not recoverable from Git.
# Keep the flags minimal. With --virtual-time-budget or --user-data-dir the
# process did not exit (2026-09-29).
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

python3 - "$out" <<'EOF'
import re, sys
data = open(sys.argv[1], "rb").read()
pages = len(re.findall(rb"/Type\s*/Page[^s]", data))
print(f"pages: {pages}")
sys.exit(0 if pages == 2 else 1)
EOF
