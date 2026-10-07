# Golden Hour: style studies (A / B / C)

These are three treatments of the same Golden Hour composition for the @TapaiaSquare X header. Each comes as a 1500x500 header, a 3000x1000 @2x and an X-profile preview in light and dark. `comparison.png` puts all three side by side, with each also shown at X desktop scale under the profile picture.

| Study | Files | Technique |
|---|---|---|
| A · Cozy HD pixel | `A-golden-hour-hd.png`, `@2x`, `-preview.png` | 750x250 pixel art (`hd.py`), shown at 2x with nearest-neighbour scaling. It has a Bayer-dithered sky, hue-shifted ramps (violet shadows, gold lights), selective 2-3 tone outlines, rim light, haze layers, volumetric lamp halos and pools, emissive bloom, and horizontal sun glints on the paving. |
| B · Painterly pixel | `B-golden-hour-painterly.*` | `painterly.py` reuses the A layers. The town, square and people stay crisp at 2x. The sky is smooth and grain-painted. Mountain, hills and clouds are blurred for depth of field, and the foreground hedge is blurred for a tilt-shift look. It adds an aerial haze band, crepuscular light shafts from the sun, bloom and a vignette. |
| C · Illustrated flat | `C-golden-hour-illustrated.*` | `flat.py` draws the scene as a vector SVG (`art/C-scene.svg`) in the same palette and layout, with no pixel grid. It uses soft gradients, gradient tree crowns and blurred glows. |

Build everything with `./render.sh`, which needs Python 3, Pillow, numpy and Chrome.

## How the art connects to the text (all three studies)
- **The coin is the setting sun.** The sky's radial glow, the light rays and shafts, the gold undersides of the clouds, the column of glints on the paving, `sun_warm` tinting and every rim light share one centre: the coin at (975,179). The coin carries a halo in the sunset colours, a warm sheen on its upper right and a plum occlusion on its lower left, so it reads as backlit by the scene.
- **The text is lit from behind.** A wide gold afterglow sits behind the wordmark and tagline. The wordmark is deep plum `#2a1640`, with a soft gold glow and a faint gold edge on the side facing the sun.
- **Clouds frame the lockup.** One bank arcs over the coin and wordmark, and a second underlines the tagline.
- **Leading lines.** The mountain's right ridge and the staircase descend toward the right, the treeline gets lighter as it approaches the sun, and the paving glints run straight up to the coin.
- **Balance.** The left carries the mountain, the stone tower and the town. The right carries the sun, the lockup and the red maple as a counterweight.
- The wordmark CSS is unchanged from `../compose.py`: Inter 800, 112px, -.045em; tagline 600, 31px.

## Lore (Snowmoon, GPL v3) kept from the previous pass, plus restorations
- ch1:30: the castle-tower apartments are **restored**. They are ~15 storeys, "shaped like over-sized medieval castle towers though with far more windows", and poke above the trees on the lower slope. Each tower has 15 rows of windows.
- ch6:325-327: a straight outdoor staircase up the mountain side leads to the open-topped stone tower. A brighter green circle glows at the top.
- ch6:221: tea tables and a tea cart; a basic, empty playground (bare swing and slide); a quiet square.
- ch6:223: a library of dull business books, with a few gold-banded spines.
- ch6:225: a gamed "active use" shop, an OPEN sign over one lone stool.
- ch5:46 / ch6:10 / ch20:154 / ch6:271: green circles appear on a check-in pole, beside doors and on tabletops, not on the ground.
- ch1:132 / ch1:140: privacy robes are a minority. One is worn hood down, one hood up with the dark face cover and its strap below the eyes.

All art is original and drawn in code. Nothing is traced or copied from any game.
