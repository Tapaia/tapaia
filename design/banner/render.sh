#!/usr/bin/env bash
# Build the @TapaiaSquare X header variants (1500x500 + 3000x1000 @2x) and the X-profile previews.
set -euo pipefail
cd "$(dirname "$0")"
python3 compose.py
CHROME=${CHROME:-$(command -v google-chrome || command -v chromium || command -v chromium-browser)}
shot() { "$CHROME" --headless=new --disable-gpu --hide-scrollbars --force-device-scale-factor="$3" \
  --window-size="$2" --virtual-time-budget=3000 --allow-file-access-from-files \
  --screenshot="$PWD/$4" "file://$PWD/$1" >/dev/null 2>&1; }
for v in day dusk clean; do
  shot "banner-$v.html" 1500,500 1 "banner-$v.png"
  shot "banner-$v.html" 1500,500 2 "banner-$v@2x.png"
  shot "preview-$v.html" 1280,660 2 "preview-$v.png"
  echo "rendered $v"
done
rm -rf __pycache__
