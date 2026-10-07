#!/usr/bin/env bash
# Build all logo files and render the comparison sheet (1600x1000) with headless Chrome.
set -euo pipefail
cd "$(dirname "$0")"
python3 build_logo.py
python3 sheet.py
CHROME=${CHROME:-$(command -v google-chrome || command -v chromium || command -v chromium-browser)}
"$CHROME" --headless=new --disable-gpu --hide-scrollbars --force-device-scale-factor=1 \
  --window-size=1600,1000 --virtual-time-budget=3000 --allow-file-access-from-files \
  --screenshot="$PWD/comparison.png" "file://$PWD/comparison.html" >/dev/null 2>&1
echo "rendered comparison.png"
