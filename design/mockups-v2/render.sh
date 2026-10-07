#!/usr/bin/env bash
# Render v2 mockups to PNG with headless Chrome/Chromium. Desktop 1440x900, mobile 390x844 (2x DPR).
set -euo pipefail
cd "$(dirname "$0")"
CHROME=${CHROME:-$(command -v google-chrome || command -v chromium || command -v chromium-browser)}
mkdir -p png
pages=${*:-$(ls [0-9]*.html)}
for page in $pages; do
  out="png/${page%.html}.png"
  if [[ $page == *mobile* ]]; then size=390,844; dpr=2; else size=1440,900; dpr=1; fi
  "$CHROME" --headless=new --disable-gpu --hide-scrollbars --force-device-scale-factor=$dpr \
    --window-size=$size --virtual-time-budget=3000 --screenshot="$out" "file://$PWD/$page" >/dev/null 2>&1
  echo "rendered $out"
done
