# @TapaiaSquare X header banners

1500x500 (`banner-<v>.png`) and 3000x1000 (`banner-<v>@2x.png`), plus X profile mocks (`preview-<v>.png`, light + dark).

- `day`: Tapaia Square on a clear afternoon. Lockup sits in the open sky, right of center.
- `dusk`: golden hour with lamp-lit windows, glowing lamps and a hazy mountain. Lockup in cream and gold.
- `clean`: robe-purple gradient, centered lockup, and a lamp-lit strip of the square along the bottom.

Original pixel art at 375x125, scaled 4x and 8x, made with the scene kit in `design/mockups/art` (`scene_banner.py`).
The logo (C premium coin) and the Inter type are vector and are composed in `compose.py`. Rebuild with `./render.sh`.
Safe zones: no critical content in the bottom-left (X profile picture), and the lockup stays in the middle band (y about 100-260).

## Lore pass (Oct 7, 2026)
Line refs are to `/workspace/snowmoon/text/`.
- Tapaia is a calm square where "you can sit down, drink tea, there are shops nearby," and it is "less lively than Galanar" [ch6:221]. Fewer people, standing about in a relaxed way.
- The playground is "much more basic ... not even comfortable" [ch6:221]: one bare swing and a small plain slide, with nobody on them.
- Library: "boring business books, or things in foreign languages nobody understands, either Old Belpakian or something from Haragmir" [ch6:223]. A plain LIBRARY sign; window shelves of dull spines, some with gold title bands and some with pale foreign-script marks.
- Gamed "ground-floor active use" rubric [ch6:225]: a storefront with an OPEN sign and a single stool in the window (the joke is our design choice).
- Green circles sit on a 1 m "Check in" pole [ch5:46], beside doors [ch6:10] and on tea tables [ch6:271]. None on the ground.
- Privacy robes [ch1] are worn by a minority: 2 of 8 citizens in the main scenes.
- The mountain: tree-covered [ch1:30], with a straight 200 m outdoor staircase up its side and an open-topped stone tower at the top [ch6:325-327]. The castle-tower apartments are removed.
- Design choices that are not canon: the tea cart, outdoor lamp posts, the red maple, the sign and shop contents, and the clouds.
