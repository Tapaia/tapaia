# Phase 1 mockups, v2 (current direction)

A clean, modern chat app (think Discord, Telegram or Slack polish) with pixel art kept as small charm accents. v1, the full 8-bit AOL take, stays in [`../mockups/`](../mockups/) for reference. Spec: [`docs/phase1-spec.md`](../../docs/phase1-spec.md). Where the colors come from: [`design/visual-reference.md`](../visual-reference.md).

| Screen | HTML | PNG |
|---|---|---|
| Sign in: wallet picker + Sign-In with Ethereum | `01-sign-in.html` | `png/01-sign-in.png` (1440x900) |
| Arrival: become a citizen (founder slots, burn notice) | `02-arrival.html` | `png/02-arrival.png` (1440x900) |
| Tapaia Square, the in-character room (Say / Speak) | `03-tapaia-square.html` | `png/03-tapaia-square.png` (1440x900) |
| #general, an out-of-character channel, dark theme | `04-general-dark.html` | `png/04-general-dark.png` (1440x900) |
| Tapaia Square on a phone | `05-mobile-square.html` | `png/05-mobile-square.png` (390x844 at 2x = 780x1688) |
| Profile and avatar on a phone | `06-mobile-profile.html` | `png/06-mobile-profile.png` (390x844 at 2x) |

Usernames are fictional citizens. Letters such as **X**, **E** and **S** (dashed gold boxes) are placeholders, not decided values. Times in the Square use the shared Meldan clock in ticks; out-of-character channels use normal local time.

## Design system

- **Type:** Inter for all UI text. Press Start 2P only for tiny accents (the Meldan tick clock).
- **Color:** robe purple (`#5b3a86`) is the primary/brand color; Veridian leaf green (`#3f7a37`) and the book's glowing circle green (`#2fc56a`) mean verified/online; ember (`#ea7a2a`) marks anything that burns ZC; gold (`#e0a526`) is for Founding Citizens, mentions and placeholders; neutrals are warm parchment and stone. A dark theme (`[data-theme="dark"]`) uses the same accents on deep plum.
- **Shape:** 8/12/16/22 px radii, soft shadows, generous spacing, 1px warm borders.
- **Pixel art, only as accents:** the compact Tapaia Square banner, the sign-in hero, avatars (16px sprites at whole-number scales only, `image-rendering: pixelated`), badges and small room icons, the arrival and Speak cards, and the wallet icons.
- **AOL nod:** "has entered the square" lines and buddy-list style presence dots.
- All tokens and components are in `app.css`. Screens are generated from `build.py` (icons, helpers, sidebar) and `screens.py` (one function per screen).

## Rebuilding

```bash
python3 art_v2.py    # writes the v2-only pixel assets into assets/ (uses the v1 sprite code in ../mockups/art; needs Pillow)
python3 build.py     # writes the six HTML files
./render.sh          # renders png/ with headless Chrome or Chromium (or ./render.sh 03-tapaia-square.html)
```

`assets/` starts as a copy of v1's `assets/`. If you copy it again, re-run `art_v2.py` afterwards.

## Art and fonts

- All pixel art is **original**, drawn by code in `../mockups/art/` and `art_v2.py`, released under the repo's GPL v3. The wallet icons are made-up pixel pictures that hint at each wallet's name, **not** the official logos. The UI icons are simple hand-written SVG line icons in `build.py`.
- Fonts: Inter and Press Start 2P, both SIL Open Font License 1.1, bundled in `fonts/` with their license files (`OFL-Inter.txt`, `OFL-PressStart2P.txt`).
