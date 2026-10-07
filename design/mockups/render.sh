#!/usr/bin/env bash
# Render each mockup to a 1280x800 PNG with headless Chrome/Chromium.
set -euo pipefail
cd "$(dirname "$0")"
CHROME=${CHROME:-$(command -v google-chrome || command -v chromium || command -v chromium-browser)}
mkdir -p png
for f in "${@:-01-sign-in.html 02-arrival.html 03-tapaia-square.html 04-profile-builder.html}"; do
  for page in $f; do
    out="png/${page%.html}.png"
    "$CHROME" --headless=new --disable-gpu --hide-scrollbars --force-device-scale-factor=1 \
      --window-size=1280,800 --virtual-time-budget=3000 --allow-file-access-from-files \
      --screenshot="$out" "file://$PWD/$page" >/dev/null 2>&1
    echo "rendered $out"
  done
done
