# Tea & Chat, refined (Oct 7, 2026)

Option 4 (teacup whose steam becomes a chat bubble, "you can sit down, drink tea" [ch6]) pushed toward a
premium token / app mark. All original art. Sheet: `comparison.png` (rebuild with `./render.sh`).

| Variant | Folder | Notes |
|---|---|---|
| A Refined Pixel | `A-refined-pixel/` | 32x32 pixel master; cream shapes, no outlines, leaf-green coin |
| B Flat Vector | `B-flat-vector/` | robe purple + cream + gold tea line; `-small.svg` is the grid-aligned drawing used for 64/32/24 px |
| C Premium Coin | `C-premium-coin/` | green pay-circle bevelled rim, gradient field, lit cream, soft shadow |
| D Hybrid | `D-hybrid/` | flat coin, solid green pay-circle rim, square typing dots + stepped steam |

Each folder: `<slug>.svg` (master), PNGs at 512/256/64/32 (+24 for list rows), a hand-tuned `<slug>-16.png` /
`-16.svg` pixel version, `-app-icon-512.png` (+128, and `-app-icon.svg` for vector variants), and
`-x-pfp-400.png` (square for the @TapaiaSquare avatar; X crops it to a circle).

Shared geometry lives in `vec.py` (64-unit grid, straight edges on even units so 32 px stays crisp);
pixel art in `px.py`; exports in `build.py`; sheet in `sheet.py`.
