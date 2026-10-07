#!/usr/bin/env bash
# Golden Hour style studies: render scene art, then 1500x500, 3000x1000 @2x and X-profile previews, then comparison.png
set -euo pipefail
cd "$(dirname "$0")"
python3 hd.py            # A pixel scene  -> art/A-scene-750x250.png
python3 painterly.py     # B painterly    -> art/B-scene-1500x500.png
python3 flat.py          # C illustrated  -> art/C-scene.svg (vector)
python3 compose_styles.py
CHROME=${CHROME:-$(command -v google-chrome || command -v chromium || command -v chromium-browser)}
shot() { "$CHROME" --headless=new --disable-gpu --hide-scrollbars --force-device-scale-factor="$3" \
  --window-size="$2" --virtual-time-budget=3000 --allow-file-access-from-files \
  --screenshot="$PWD/$4" "file://$PWD/$1" >/dev/null 2>&1; }
for s in ${STUDIES:-A-golden-hour-hd B-golden-hour-painterly C-golden-hour-illustrated}; do
  [ -f "$s.html" ] || continue
  shot "$s.html" 1500,500 1 "$s.png"
  shot "$s.html" 1500,500 2 "$s@2x.png"
  shot "$s-preview.html" 1280,660 2 "$s-preview.png"
  echo "rendered $s"
done
python3 comparison.py
rm -rf __pycache__ ../__pycache__
