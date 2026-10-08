# $TAPAIA tokenomics card for X

- `tapaia-tokenomics.png`: 1600x900 (X 16:9), the file to post.
- `tapaia-tokenomics@2x.png`: 3200x1800.
- `tapaia-tokenomics.html`: the layout. `art.py` draws the pixel background (`art/bg-400x225.png`, shown at 4x with nearest-neighbour scaling) and the 16x16 icons (`art/icon-*.png`, shown at 4x).

Rebuild with `./render.sh` (runs `art.py`, then headless Chrome).

Style follows the official kit: the D-hybrid coin logo (`../../logo/opt4-refined/D-hybrid/`), the "Tapaia" wordmark with the same CSS as `../../banner/final/` (Inter Variable from `../../mockups-v2/fonts/`, weight 800, -.045em tracking, plum on the coin-sun afterglow), Inter for body text, and the book palette: robe purple, green-circle rings, warm gold and parchment. All art is original. The pixel scene echoes the header: the coin as the setting sun, the mountain with castle-tower apartments, the staircase and stone tower with the green glow [ch1, ch6], and a lamp-lit street with a green "check in" circle on a pole [ch5].

The text matches [docs/tokenomics.md](../../../docs/tokenomics.md) (working plan, decided Oct 7, 2026). If the numbers change, update the HTML and re-render. The footer carries "Numbers may change before launch · Not financial advice" and the non-affiliation line.
