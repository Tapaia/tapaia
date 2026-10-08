# Tapaia characters: Cozy HD pixel citizens (Phase 1 study)

This is the upgraded character system for the Tapaia prototype. It matches the official **Cozy HD pixel** style of the final X header (`../banner/final/`, style A in `../banner/styles/hd.py`) and aims for a cozy, Stardew-Valley-like feel. **Everything is original art drawn in code. Nothing is traced, copied or derived from Stardew Valley or any other game.** Licence: GPL v3, same as the repo.

Phase 1 is a study only. Nothing in `app/` has changed. The integration plan is at the end of this README.

## Deliverables

| File | What it is |
|---|---|
| `comparison.png` / `comparison@2x.png` | Current vs new **inside the real app UI**: the Tapaia Square banner, chat rows, the arrival card, the dark theme and avatar tiles at 40/64/128 px. It uses the prototype's own `app.css` and `screens.css` at real CSS sizes, at 1x and retina 2x. |
| `comparison-phone.png` / `-1x.png` | The same at phone size (390 pt wide, 3x density), plus a 1/3 downscale to show it at arm's length. |
| `character-sheet.png` | 12 citizens front-facing at 4x, front and 3/4 views of Nessa and Alder, an actual-size line-up and 64 px portraits. |
| `builder-parts.png` | Avatar-builder options: 11 hairstyles, 8 hair colours and 7 skin tones (with their ramps), 9 expressions, 6 eye colours, 9 outfits and 8 accessories. |
| `busts.png` | Chat busts at 40, 64 and 128 px in light and dark tiles, plus a 3x magnification of the 40 px bust. |
| `out/sprites/*.png` | Raw 32×48 sprites (and `-3q` 3/4 views). |
| `out/busts/*-{24,32,40,64}.png` | Raw native busts. |
| `out/scene-square-750x250.png` | The final-header plaza with the new citizens in it (1500×500 @2x is alongside). |
| `out/scene-square-empty-750x250.png` | The same plaza with nobody in it, PNG8 at 38 KB, as an app banner background with live citizens drawn on top. |

Scripts: `charkit.py` (renderer), `citizens.py` (cast), `build.py` (sheets and raw PNGs), `scene.py` (HD Square), `compare.py` + `finish.py` (before/after pages and screenshots) and `render.sh` (runs everything; needs Python 3, Pillow, numpy and Chrome).

## 1. How characters are drawn today (audit)

| Where | Source | Size and format |
|---|---|---|
| Avatar builder / every avatar | `app/shared/avatar.ts` (`avatarPixels`), a TS port of `design/mockups/art/sprites.py avatar()` | **16×24** char map (8 columns mirrored), +1 row for robe heels, +2 for a bun (16×25–27). A 1 px near-black outline `#2b1d2e`, 2 tones per material, flat. Head = 12 of 24 rows (50%, chibi), with 1 px eyes and no mouth. Options: outfit robe/hood/plain/slogan, 6 hair colours, 3 hairstyles, 4 skins, neck band, shirt colour. |
| Rendering | `app/src/ui.tsx` `avatarUrl()` | Drawn to a 16×N canvas → data URL, cached per config. `image-rendering: pixelated`. |
| Chat avatar `.av` | `Av` in `ui.tsx` + `app.css` | Top **16×16** crop shown at 32 px in a 40 px rounded tile (2x). `s28/s32/s48/s64` variants up to 4x. Stacks use 24 px tiles (16 px image). Reply lines use 18 px. |
| Full body `Figure` | `ui.tsx` | The 16×24 sprite at width 48 (3x, arrival card and profile card), 80 (5x, profile hero / sign-in) and 32 (mobile). |
| Tapaia Square banner | `design/mockups/art/scene.py` → `scene-header.png` (410×48) | Shown at **1230×144** (3x, desktop), 820×96 (mobile) and 900×105. People are baked-in **9×13 `mini()`** sprites, 39 CSS px tall. |
| Static busts / figures | `design/mockups-v2/assets/av-*.png` (16×24), `bust-*.png` (16×16), `opt-*.png` | Mockup copies of the same sprites. |
| Badges | `icon-medal/flame/shield/robot/star.png` | 12×12 icons at 14–16 px. They are not characters and are unchanged here. |

## 2. The new system

**Sprite:** 32×48, which is 4x the pixels of a 16×24 sprite. The head is about 40% of the height (head radius 8.5, centre (16, 12.5)), with a narrower body and real arms, hands, legs and shoes. That's Stardew-like proportions without copying any sprite.

**One renderer, any size.** Each citizen is a small config (skin, hair style and colour, eyes, expression, outfit plus colours, accessories). Shapes are defined in a continuous 32×48 *sprite space* and rasterised **natively** at any scale:
- the sprite (k = 1)
- busts at 24/28/32/36/40 px (tighter head-and-shoulders frame, 25 units) and 64 px (27 units, with shoulders)
- full-body figures at any width, e.g. 48×72 for the arrival card and 80×120 for the profile hero

So a 40 px avatar is a real 40×40 pixel drawing, not a blurry or chunky upscale, and it always matches the walking sprite. Faces use **hand-placed pixel templates** for each detail level (sprite / 40 px / 64 px), so eyes and mouths stay crisp and intentional at every size.

**Shading and outline pipeline:**
1. Shapes produce a (material, tone) grid.
2. Orphan tone pixels are cleaned up.
3. A **cast-shadow contour** darkens a pixel that touches an object painted in front of it (hair onto the forehead, arm onto the torso, chin onto the neck). It's 1 px at sprite scale and about 2 px on the 64 px portrait.
4. Face templates are placed.
5. A **soft coloured sel-out outline** is added: each material's own deep tone on the lit top/left rim and its outline colour on the shadow side. There's **never pure black**.

Light is a top-left key. Every material has **4 tones plus a specular**, hue-shifted with shadows toward plum-violet (skin toward rose-plum) and lights toward warm cream, the same idea as `kit.shade()` in the banner. Hair has strand clumps that radiate from the parting and a broken shine band on the lit side. On the 64 px portrait it also gets lighter strand ridges. Curly hair is built from individually lit curls.

**Options:**
- **Skin (7):** porcelain, fair, warm, olive, tan, brown, deep.
- **Hair colour (8):** the 6 current keys plus espresso and auburn. Black hair gets a cool lilac sheen.
- **Hairstyles (11):** short, crop, swept, bob, long, wavy, braid, ponytail, bun, elderbun, curly.
- **Eyes (6):** brown, hazel, green, blue, grey, amber.
- **Expressions (9):** smile, grin, laugh, content, surprised, thoughtful, shy, wink, calm.
- **Outfits (8):** tee, band tee, tunic, cardigan (with skirt or trousers), apron, coat, robe (hood down), robe with hood up and face cover.
- **Accessories:** neck band, scarf, satchel, glasses, beard, freckles, held tea cup or book.
- **3/4 view:** `turn` from 0 to 1.

**Colours** come from the book palette in `../visual-reference.md`: robe purples, leaf and mountain greens, wood, parchment, house walls (beige, light blue, blue-grey), maple red and Hydrafill yellow.

**Lore** [Snowmoon, GPL v3]:
- **Privacy robe:** a loose dark purple dress down to the ankles, with **same-colour shoes with a high heel and a deliberately uneven sole** (the right shoe stands taller) [ch1].
- **Hood up:** the hood frames a deep shadow, and the **front face cover has a strap across below the eyes**, drawn as a lighter silk band with a small buckle [ch1:132, ch1:140]. Two soft eye glints keep hooded citizens friendly (an existing design choice).
- **Hood down:** the hood bunches around the shoulders, worn "without putting on the face cover or hood" [ch6, ch17].
- **Silk neck band** [ch1].
- **Plain and band shirts** [ch1]. The band-shirt graphic is invented.
- **Our design choices:** tunics, cardigans, aprons, coats and scarves for everyday Veridia.

## 3. Honest critique

**What works:**
- Characters now have readable faces: eyes with lash line, iris and highlight, plus brows, mouths and blush. They have personality (Nessa's grin, Tobin's laugh, Juniper's wink) and silhouettes you can tell apart (bun, curls, braid, hood).
- Busts match the sprite exactly.
- The hood-up robe with the strap reads as clearly as anything on the sheet.
- In the comparison, the new chat rows look more premium at the same footprint, and the arrival card gets a proper little figure.

**Weak spots, to fix in Phase 2:**
1. **At 36–40 px on a 1x monitor, the new busts lose some punch** against the old chunky 2x busts. Faces are finer and the old flat 16×16 shapes read from further away. On retina and phones (most users) the new busts are clearly better. I tightened the small-bust crop to help.
2. **The face shading is a fairly hard cel crescent** on the right side, and hands are small blobs with no fingers or thumbs.
3. **Hair is procedural.** It's good at the sprite scale and decent on the portrait, but a human pixel artist would still beat it on the portrait's hair clumps and on the curly style's top silhouette, which is a bit helmet-like.
4. **The 3/4 view is modest.** Features compress and shift, the near ear and back of the head show and the far arm tucks behind, but it's not a true turnaround, and there are no side or back views or walk cycle yet.
5. **The new Square banner is busier.** The HD golden-hour scene at 1x is richer but busier behind the banner text than the old flat 3x strip, and its characters are about the same size as before, so they don't pop as much. It's also dusk-only, with no daytime or light-theme version.
6. Some colour pairs need care. Espresso hair on brown skin, for example, is low contrast, so the builder should warn or nudge.

## 4. Integration plan (Phase 2, not done here)

**Approach:** keep today's architecture, where `shared/avatar.ts` is a TS port of a Python sprite script and `ui.tsx` renders to a canvas and caches a data URL. Port `charkit.py` to TS the same way. There are no part atlases to ship. The renderer is about 900 lines of Python and roughly 12 KB of minified, gzipped TS, which costs less than a single sprite sheet and makes every combination and every size possible.

**Files that change** (all under `app/`):

| File | Change |
|---|---|
| `shared/avatar2.ts` (new) | Port of `charkit.py`: ramps, shapes, face templates and the pipeline. `renderCitizen(cfg, {mode: 'sprite' \| 'bust' \| 'figure', size \| k}) → {w, h, rgba}`. Pure, no DOM, so the server and scripts can use it too. |
| `shared/avatar.ts` | Keep the v1 types for stored data. Add `AvatarCfgV2`, `migrateAvatar(v1) → v2`, a v1-or-v2 `isAvatarCfg` that always normalises to v2, and `randomAvatar()` for v2. |
| `shared/types.ts` | `PublicUser.avatar: AvatarCfgV2`. |
| `server/store.ts`, `server/index.ts` | Migrate stored avatars on load. PATCH `/api/profile` accepts v1 or v2 and stores v2. |
| `server/seed.ts` | Re-cast the seed citizens with v2 configs. `citizens.py` is the reference cast. |
| `src/ui.tsx` | `avatarUrl(cfg, kind, size)`. `Av` renders a **native bust at the tile size** (24/28/32/36/40/48/64), with 128 = the 64 bust at 2x. `Figure` renders a native figure at `k = w/32` (32 → 1x, 48 → 1.5x, 80 → 2.5x). Cache key = cfg + kind + size, kept in an LRU of about 300 entries. |
| `src/styles/app.css`, `screens.css` | `.av img` fills the tile (`width/height: 100%`) instead of 32 px inside 40. Update `.stack .avs .av img`, `.replyline .av img` and `.hero .proof .av img` to match. `.card-arrival .fig img` becomes 48×72 (the mobile fig grows from 52×60 to 64×76 with a 48 px figure, since 32 px is small for the new detail). The banner `background` moves to the new HD plaza at 1x (`750px 250px`, plus a plum fill colour for very wide screens). |
| `src/components/Profile.tsx` | Builder. Swatch rows grow from Hair (6), Style (3) and Skin (4) to: hairstyle (11, as bust thumbnails), hair colour (8), skin (7), eyes (6), expression (9, as face chips), outfit (8 figure buttons, like today's `outfits` grid), top/bottom colour swatches (from `CLOTH`), and accessory toggles (neck band stays, plus scarf, satchel, glasses, beard, freckles, held item). Randomize and Undo stay as they are. |
| `src/components/SignIn.tsx`, `Arrival.tsx`, `Main.tsx` | Use v2 configs and the new Figure sizes. In `Main.tsx`, the Square banner's citizen layer can draw the present citizens' sprites live, absolutely positioned at preset plaza spots over the empty background, instead of baked-in people (optional phase 2b). |
| `scripts/copy-assets.mjs` | Also copy `design/characters/out/scene-square-empty-750x250.png`. |
| `scripts/verify.mjs` | Golden test: the TS port must match `out/sprites/*.png` and `out/busts/*.png`, with ≤0.5% of pixels allowed to differ for float edge cases. Add a builder smoke test. |

**Mapping current builder → new parts** (migration, lossless for everything that exists today):

| v1 | v2 |
|---|---|
| `outfit: robe` / `hood` / `plain` / `slogan` | `robe` / `hood` / `tee` / `bandtee` |
| `shirt: #hex` | `top: #hex` (hex is accepted anywhere a cloth key is) |
| `hair`: black, chestnut, ginger, blonde, plum, silver | Same keys (adds espresso and auburn) |
| `hairstyle`: short, long, bun | Same keys (adds 8 more) |
| `skin`: fair, warm, tan, deep | Same keys (adds porcelain, olive, brown) |
| `band: true` | `neckband: true` |
| (none) | Defaults: `eyes: brown`, `expr: smile`, `bottom: charcoal`, no accessories |

**Performance and size budget:**
- **JS:** about 12 KB gzipped for the renderer, which replaces about 2 KB today.
- **Assets:** the HD plaza background is 38 KB (PNG8), compared with 9.5 KB for the current banner strip. The per-avatar PNGs in `mockups-v2/assets` (`av-*`, `bust-*`, `opt-*`) can be dropped.
- **Render time:** Python takes 6 ms for a 40 px bust, 16 ms for a 64 px bust and 17 ms for a sprite. JS with typed arrays should be about 5–10x faster. The target is ≤2 ms per bust and ≤4 ms per sprite on a mid-range phone.
- **Rendering strategy:** render on demand with a cache, and pre-warm the visible member list in `requestIdleCallback`. The worst case is about 30 citizens in the Square, roughly 100 ms spread over idle frames.
- **Memory:** data URLs are about 1.2–3 KB each, so 300 cached entries come to under 1 MB.
- **Network:** the server keeps sending configs only (~150 bytes per user) and never images.

**Rollout:**
1. Port the renderer and pass the golden test.
2. Switch avatars over (`Av`/`Figure` and the CSS sizes), including migration.
3. Expand the builder UI.
4. Switch the Square banner, with live citizens as an option.
5. Phase 2 art polish (critique items 1–4): softer face shading, hands with a thumb pixel, a hand-tuned portrait hair pass, and a walk cycle and side view if the Square becomes interactive.
