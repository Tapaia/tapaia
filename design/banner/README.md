# @TapaiaSquare X header banners

1500x500 (`banner-<v>.png`) and 3000x1000 (`banner-<v>@2x.png`), plus X profile mocks (`preview-<v>.png`, light + dark).

- `day`: Tapaia Square on a clear afternoon. Lockup sits in the open sky, right of center.
- `dusk`: golden hour with lamp-lit windows, glowing lamps and a hazy mountain. Lockup in cream and gold.
- `clean`: robe-purple gradient, centered lockup, and a lamp-lit strip of the square along the bottom.

Original pixel art at 375x125, scaled 4x and 8x, made with the scene kit in `design/mockups/art` (`scene_banner.py`).
The logo (C premium coin) and the Inter type are vector and are composed in `compose.py`. Rebuild with `./render.sh`.
Safe zones: no critical content in the bottom-left (X profile picture), and the lockup stays in the middle band (y about 100-260).
