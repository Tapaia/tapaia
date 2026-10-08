#!/usr/bin/env bash
# $TAPAIA tokenomics card for X: tapaia-tokenomics.png (1600x900) and @2x (3200x1800)
set -euo pipefail
cd "$(dirname "$0")"
python3 art.py
CHROME=${CHROME:-$(command -v google-chrome || command -v chromium || command -v chromium-browser)}
shot() { "$CHROME" --headless=new --disable-gpu --hide-scrollbars --force-device-scale-factor="$2" \
  --window-size=1600,900 --virtual-time-budget=3000 --allow-file-access-from-files \
  --screenshot="$PWD/$3" "file://$PWD/$1" >/dev/null 2>&1; }
shot tapaia-tokenomics.html 1 tapaia-tokenomics.png
shot tapaia-tokenomics.html 2 tapaia-tokenomics@2x.png
ls -la tapaia-tokenomics*.png
