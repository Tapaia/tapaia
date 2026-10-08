#!/usr/bin/env bash
# Tapaia characters: sprites, busts, sheets, Square scene and the before/after comparison.
# Needs Python 3 + Pillow + numpy, and Chrome for the comparison screenshots.
set -euo pipefail
cd "$(dirname "$0")"
export PYTHONDONTWRITEBYTECODE=1
python3 build.py
python3 scene.py
python3 compare.py
CHROME=${CHROME:-$(command -v google-chrome || command -v chromium || command -v chromium-browser)}
shot() { "$CHROME" --headless=new --disable-gpu --hide-scrollbars --force-device-scale-factor="$3" \
  --window-size="$2" --virtual-time-budget=3000 --allow-file-access-from-files \
  --screenshot="$4" "file://$PWD/$1" >/dev/null 2>&1; }
shot comparison.html 1364,1700 1 "$PWD/comparison.png"
shot comparison.html 1364,1700 2 "$PWD/comparison@2x.png"
shot out/phone-before.html 390,800 3 /tmp/tapaia-phone-before.png
shot out/phone-after.html 390,800 3 /tmp/tapaia-phone-after.png
python3 finish.py
rm -rf __pycache__ ../banner/final/__pycache__ ../banner/styles/__pycache__ ../mockups/art/__pycache__
ls -la *.png
