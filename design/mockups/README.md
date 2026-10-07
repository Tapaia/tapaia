# Phase 1 mockups

Static HTML/CSS mockups of Tapaia's Phase 1 community hub, in an 8-bit cozy take on a late-90s AOL chat room. Spec: [`docs/phase1-spec.md`](../../docs/phase1-spec.md). Where the colors and decor come from: [`design/visual-reference.md`](../visual-reference.md).

| Screen | HTML | PNG (1280x800) |
|---|---|---|
| Welcome / sign in (wallet picker + SIWE) | `01-sign-in.html` | `png/01-sign-in.png` |
| Arrival: become a citizen (founder slots, burn notice) | `02-arrival.html` | `png/02-arrival.png` |
| Tapaia Square chat room | `03-tapaia-square.html` | `png/03-tapaia-square.png` |
| Profile card + avatar builder | `04-profile-builder.html` | `png/04-profile-builder.png` |

All screens share `tapaia.css`. Usernames are fictional original citizens. Letters such as **X**, **E** and **S** are placeholders, not decided values.

## Rebuilding

```bash
python3 art/build_art.py   # regenerates every pixel asset in assets/ (needs Pillow)
./render.sh                # renders png/ with headless Chrome or Chromium
```

## Art and fonts

- All pixel art (scene, sprites, icons, wallet icons, frames) is **original**, drawn by code in `art/` and released under the repo's GPL v3. The wallet icons are made-up pixel pictures that hint at each wallet's name (a rabbit, a fox, a rainbow…), **not** the official logos.
- Fonts: Press Start 2P and VT323, both SIL Open Font License 1.1, bundled in `fonts/` with their license files.
