# @TapaiaSquare X header: final (Golden Hour, style A "Cozy HD pixel")

- `tapaia-x-header.png`: 1500x500, about 0.3 MB. This is the file to upload to X (the limit is 2 MB).
- `tapaia-x-header@2x.png`: 3000x1000.
- `tapaia-x-header-preview.png`: an X profile mock in light and dark themes, with the D-hybrid profile picture.
- `art/scene-750x250.png`: the pixel scene, shown at 2x/4x with nearest-neighbour scaling.

Rebuild with `./render.sh`. It runs `header.py`, then `compose.py`, then headless Chrome.

`header.py` builds on the style-A study (`../styles/hd.py`) with these final fixes:
- **Soft cumulus pixel clouds** replace the thin stratus streaks. Each cloud is a smooth density field lit from its gradient, backlit near the sun and pink-lit away from it, with gold undersides and dithered edges. One bank crowns the coin and wordmark and another rests under the tagline, so the lockup is framed.
- **People about 1.45x larger** (42 px at 750x250). They have clearer silhouettes, violet shadow sides, gold sun-side rims and selective outlines with no pure black.
- **A calmer mountain forest** in a lower-contrast, regular canopy. The castle-tower apartments get contact outlines [ch1:30]. The staircase is cut through the trees with shaded edges, and the stone tower at the top has a sun-side rim and the green glow [ch6:325-327].

Unchanged from the studies:
- The coin is the setting sun. Sky glow, rays, cloud light, rim lights and paving glints all centre on the coin.
- The wordmark CSS (Inter 800 / 112px / -.045em) and the plum-on-afterglow treatment.
- The X safe zones: the lockup sits in the right-middle band, clear of the profile picture.
- Every lore element listed in `../styles/README.md`.
