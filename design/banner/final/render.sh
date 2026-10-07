#!/usr/bin/env bash
# Final @TapaiaSquare X header: tapaia-x-header.png (1500x500), @2x (3000x1000), X-profile preview (light + dark)
set -euo pipefail
cd "$(dirname "$0")"
python3 header.py
python3 compose.py
CHROME=${CHROME:-$(command -v google-chrome || command -v chromium || command -v chromium-browser)}
shot() { "$CHROME" --headless=new --disable-gpu --hide-scrollbars --force-device-scale-factor="$3" \
  --window-size="$2" --virtual-time-budget=3000 --allow-file-access-from-files \
  --screenshot="$PWD/$4" "file://$PWD/$1" >/dev/null 2>&1; }
shot tapaia-x-header.html 1500,500 1 tapaia-x-header.png
shot tapaia-x-header.html 1500,500 2 tapaia-x-header@2x.png
shot tapaia-x-header-preview.html 1280,660 2 tapaia-x-header-preview.png
rm -rf __pycache__ ../styles/__pycache__ ../__pycache__
ls -la tapaia-x-header*.png
