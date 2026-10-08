"""Build the character deliverables: raw sprites/busts, the character sheet, builder-part samples and bust sizes.
Run: python3 build.py   (needs Pillow + numpy).  Original art, GPL v3."""
import os, sys, re
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.dont_write_bytecode = True
from PIL import Image, ImageDraw, ImageFont
import charkit as K
import citizens

OUT = os.path.join(HERE, 'art')
FONT = os.path.join(HERE, '..', 'mockups-v2', 'fonts', 'Inter-Variable.ttf')
BG, INK, INK2, INK3, LINE = '#faf7f2', '#1f1a24', '#5f5768', '#8d8496', '#e8e0d3'
ROBE7, TILE = '#45275e', ['#e9e1f3', '#ddefd9', '#f3e6cf', '#dce9f2', '#f6dfda', '#ece6dc']
DARK_BG, DARK_TILE = '#1d1724', ['#3a2d4c', '#26402b', '#4a3c25', '#24384a', '#4a2c2a', '#3a332b']


def font(size, w=400):
    f = ImageFont.truetype(FONT, size)
    try:
        f.set_variation_by_axes([min(32, max(14, size)), w])
    except Exception:
        pass
    return f


def slug(n):
    return re.sub(r'[^a-z]+', '-', n.lower()).strip('-')


def text(d, xy, s, size, w=400, fill=INK, anchor='la'):
    d.text(xy, s, font=font(size, w), fill=fill, anchor=anchor)


def shadow(im, cx, y, rx, a=46):
    lay = Image.new('RGBA', im.size, (0, 0, 0, 0))
    ImageDraw.Draw(lay).ellipse([cx - rx, y - rx * .26, cx + rx, y + rx * .26], fill=(59, 36, 64, a))
    im.alpha_composite(lay)


def header(d, W, title, sub):
    text(d, (48, 40), title, 40, 800, ROBE7)
    text(d, (50, 94), sub, 17, 500, INK2)


CAST = citizens.CAST
BYNAME = {n: c for n, _, c in CAST}


def raw():
    for sub in ('sprites', 'busts'):
        os.makedirs(f'{OUT}/{sub}', exist_ok=True)
    for n, _, c in CAST:
        K.sprite(c).save(f'{OUT}/sprites/{slug(n)}.png')
        for s in (24, 32, 40, 64):
            K.bust(c, s).save(f'{OUT}/busts/{slug(n)}-{s}.png')
    for n in citizens.TURNED:
        K.sprite(dict(BYNAME[n], turn=.8)).save(f'{OUT}/sprites/{slug(n)}-3q.png')


def character_sheet():
    W, H = 1680, 1640
    im = Image.new('RGBA', (W, H), BG)
    d = ImageDraw.Draw(im)
    header(d, W, 'Tapaia citizens', 'Cozy HD pixel · 32×48 sprites shown at 4x · head ≈ 40% of height · 4 hue-shifted tones per material · '
           'soft coloured outlines · original art, GPL v3')
    # 12 citizens, 2 rows of 6
    cw, ch, top = 264, 330, 140
    for i, (n, role, c) in enumerate(CAST):
        col, row = i % 6, i // 6
        x0, y0 = 48 + col * (cw + 8), top + row * (ch + 12)
        d.rounded_rectangle([x0, y0, x0 + cw, y0 + ch], 18, fill='#ffffff', outline=LINE)
        d.rounded_rectangle([x0 + 10, y0 + 10, x0 + cw - 10, y0 + 236], 12, fill=TILE[i % 6])
        spr = K.up(K.sprite(c), 4)
        shadow(im, x0 + cw // 2, y0 + 10 + 22 + 186, 44)
        im.alpha_composite(spr, (x0 + cw // 2 - 64, y0 + 30))
        text(d, (x0 + 18, y0 + 250), n, 19, 650)
        text(d, (x0 + 18, y0 + 278), role, 14, 450, INK2)
        bits = [c['outfit'].replace('bandtee', 'band shirt').replace('hood', 'robe · hood up'), c.get('hairstyle', 'hood') if c['outfit'] != 'hood' else 'face cover', c['expr']]
        text(d, (x0 + 18, y0 + 302), ' · '.join(bits), 12, 500, INK3)
    # 3/4 views
    y = top + 2 * (ch + 12) + 22
    text(d, (48, y), 'Front and 3/4 views', 22, 750, ROBE7)
    text(d, (48, y + 32), 'The same config with turn = 0.8: features compress toward the far side, the near ear and back of the head show, the far arm tucks behind.', 14, 450, INK2)
    x = 48
    for j, n in enumerate(citizens.TURNED):
        bx = x + j * 560
        d.rounded_rectangle([bx, y + 64, bx + 540, y + 330], 18, fill='#ffffff', outline=LINE)
        for k_, t in enumerate((0, .8)):
            d.rounded_rectangle([bx + 14 + k_ * 176, y + 76, bx + 176 + k_ * 176, y + 300], 12, fill=TILE[(j * 2 + k_ + 1) % 6])
            spr = K.up(K.sprite(dict(BYNAME[n], turn=t)), 4)
            shadow(im, bx + 95 + k_ * 176, y + 76 + 210, 44)
            im.alpha_composite(spr, (bx + 31 + k_ * 176, y + 88))
            text(d, (bx + 95 + k_ * 176, y + 306), 'front' if t == 0 else '3/4', 13, 600, INK3, 'ma')
        text(d, (bx + 372, y + 84), n, 19, 650)
        # actual size + 2x on light and dark
        d.rounded_rectangle([bx + 372, y + 132, bx + 524, y + 300], 12, fill=DARK_BG)
        for k_, t in enumerate((0, .8)):
            s1 = K.sprite(dict(BYNAME[n], turn=t))
            im.alpha_composite(s1, (bx + 384 + k_ * 36, y + 144))
            im.alpha_composite(K.up(s1, 2), (bx + 384 + k_ * 70, y + 200))
        text(d, (bx + 372, y + 112), '1x and 2x on dark', 12, 500, INK3)
    # right column: actual-size line-up
    rx = 48 + 2 * 560
    d.rounded_rectangle([rx, y + 64, W - 48, y + 330], 18, fill='#ffffff', outline=LINE)
    text(d, (rx + 18, y + 80), 'Actual size (1x) and 2x', 16, 650)
    strip = Image.new('RGBA', (12 * 34, 48), (0, 0, 0, 0))
    for i, (n, _, c) in enumerate(CAST):
        strip.alpha_composite(K.sprite(c), (i * 34, 0))
    im.alpha_composite(strip, (rx + 18, y + 110))
    s2 = K.up(strip.crop((0, 0, 6 * 34, 48)), 2)
    im.alpha_composite(s2, (rx + 18, y + 170))
    # portraits row
    y2 = y + 360
    text(d, (48, y2), 'Chat portraits (64 px native, shown at 2x = 128 px)', 22, 750, ROBE7)
    text(d, (48, y2 + 32), 'Re-rasterised from the same config, not upscaled: the bust always matches the sprite.', 14, 450, INK2)
    for i, (n, _, c) in enumerate(CAST):
        bx, by = 48 + i * 132, y2 + 64
        tile = Image.new('RGBA', (128, 128), TILE[i % 6])
        tile.alpha_composite(K.up(K.bust(c, 64), 2), (0, 0))
        m = Image.new('L', (128, 128), 0)
        ImageDraw.Draw(m).rounded_rectangle([0, 0, 127, 127], 30, fill=255)
        im.paste(tile, (bx, by), m)
        text(d, (bx + 64, by + 136), n.split()[0], 13, 600, INK2, 'ma')
    im = im.crop((0, 0, W, y2 + 230))
    im.convert('RGB').save(f'{HERE}/character-sheet.png')


def builder_parts():
    W = 1680
    im = Image.new('RGBA', (W, 2300), BG)
    d = ImageDraw.Draw(im)
    header(d, W, 'Avatar builder parts', 'Every option is a parameter of one renderer, so any combination stays on-model. '
           'Shown as 64 px portraits at 2x and 32×48 sprites at 3x.')
    base = dict(skin='warm', hair='chestnut', eyes='brown', expr='smile', outfit='tee', top='leaf', bottom='charcoal')

    def section(y, title, note):
        text(d, (48, y), title, 22, 750, ROBE7)
        text(d, (48, y + 30), note, 14, 450, INK2)
        return y + 62

    def tile_bust(cfg, x, y, label, i, size=64, sc=2):
        T = size * sc
        tile = Image.new('RGBA', (T, T), TILE[i % 6])
        tile.alpha_composite(K.up(K.bust(cfg, size), sc), (0, 0))
        m = Image.new('L', (T, T), 0)
        ImageDraw.Draw(m).rounded_rectangle([0, 0, T - 1, T - 1], int(T * .22), fill=255)
        im.paste(tile, (x, y), m)
        text(d, (x + T // 2, y + T + 8), label, 13, 600, INK2, 'ma')

    def tile_sprite(cfg, x, y, label, i, sc=3, w=120):
        d.rounded_rectangle([x, y, x + w, y + 48 * sc + 24], 14, fill=TILE[i % 6])
        shadow(im, x + w // 2, y + 12 + 46 * sc, 13 * sc / 1.0 * .9)
        im.alpha_composite(K.up(K.sprite(cfg), sc), (x + w // 2 - 16 * sc, y + 12))
        text(d, (x + w // 2, y + 48 * sc + 32), label, 13, 600, INK2, 'ma')

    y = section(132, 'Hairstyles (11)', 'Strand clumps radiate from the parting, a broken shine band sits on the lit side; '
                'curls are lit one by one. Old keys short / long / bun map 1:1.')
    styles = ['short', 'crop', 'swept', 'bob', 'long', 'wavy', 'braid', 'ponytail', 'bun', 'elderbun', 'curly']
    for i, st in enumerate(styles):
        tile_bust(dict(base, hairstyle=st, hair=['chestnut', 'auburn', 'black', 'auburn', 'black', 'espresso', 'plum', 'blonde', 'ginger', 'silver', 'black'][i],
                       skin=['warm', 'fair', 'tan', 'warm', 'olive', 'brown', 'olive', 'porcelain', 'fair', 'brown', 'deep'][i]),
                  48 + i * 144, y, st, i)
    y += 128 + 40
    y = section(y, 'Hair colours (8) and skin tones (7)', 'Each colour expands to a 4-tone hue-shifted ramp + specular + outline '
                '(shadows lean plum or rose, lights lean warm). Black hair gets a cool lilac sheen.')
    for i, h in enumerate(K.HAIRS):
        x = 48 + i * 98
        tile_bust(dict(base, hairstyle='long' if i % 2 else 'short', hair=h), x, y, h, i, size=40, sc=2)
        r = K.Citizen(dict(base, hair=h)).ramps()['hair']
        for j, c in enumerate(r[:5]):
            d.rectangle([x + j * 16, y + 108, x + j * 16 + 15, y + 122], fill=c)
    sx = 48 + 8 * 98 + 30
    for i, s in enumerate(K.SKINS):
        x = sx + i * 98
        tile_bust(dict(base, skin=s, hair=['chestnut', 'blonde', 'espresso', 'black', 'black', 'black', 'silver'][i], hairstyle='crop'), x, y, s, i + 2, size=40, sc=2)
        r = K.skin_ramp(K.SKINS[s])
        for j, c in enumerate(r[:5]):
            d.rectangle([x + j * 16, y + 108, x + j * 16 + 15, y + 122], fill=c)
    y += 140 + 30
    y = section(y, 'Expressions (9) and eye colours (6)', 'Hand-placed pixel templates per size (sprite, 40 px, 64 px): '
                'eyes with lash line, iris and a highlight, brows, mouths, blush.')
    exprs = ['smile', 'grin', 'laugh', 'content', 'surprised', 'thoughtful', 'shy', 'wink', 'calm']
    for i, e in enumerate(exprs):
        tile_bust(dict(base, expr=e, hairstyle='bob', hair='auburn', skin='fair', eyes='green', top='sage'), 48 + i * 144, y, e, i)
    ex = 48 + 9 * 144 + 4
    for i, e in enumerate(K.EYES):
        x = ex + (i % 3) * 92
        yy = y + (i // 3) * 104 - 6
        tile_bust(dict(base, eyes=e, hairstyle='crop', hair='black', skin='porcelain', expr='smile'), x, yy, e, i, size=40, sc=2)
    y += 128 + 70
    y = section(y, 'Outfits (9)', 'Plain and band shirts and the privacy robe are canon [ch1]; tunic, cardigan, apron and coat are '
                'everyday-Veridia design choices. Robe shoes keep the high heel and uneven sole.')
    outfits = [('tee', dict(outfit='tee', top='hydra')), ('band shirt', dict(outfit='bandtee', top='charcoal', accent='hydra', bottom='denim')),
               ('tunic', dict(outfit='tunic', top='leaf', bottom='brown')), ('cardigan', dict(outfit='cardigan', top='plum', accent='cream', bottom='moss', bottom_kind='skirt')),
               ('apron', dict(outfit='apron', top='skyblue', over='parchment', rolled=True)), ('coat', dict(outfit='coat', top='wallblue')),
               ('robe, hood down', dict(outfit='robe')), ('robe + neck band', dict(outfit='robe', neckband=True)), ('robe, hood up', dict(outfit='hood'))]
    for i, (lab, o) in enumerate(outfits):
        tile_sprite(dict(base, hairstyle='bob', hair='espresso', skin='olive', **o), 48 + i * 132, y, lab, i)
    y += 48 * 3 + 24 + 60
    y = section(y, 'Accessories', 'Held items swap the arm to a holding pose. Satchel strap crosses the chest; the neck band is the silk band from the book.')
    acc = [('tea cup', dict(held='tea', pose='hold')), ('book', dict(held='book', pose='hold')), ('satchel', dict(satchel=True)),
           ('glasses', dict(glasses=True)), ('neck band', dict(outfit='robe', neckband=True)), ('scarf', dict(scarf='maple')),
           ('beard', dict(beard=True, hair='auburn')), ('freckles', dict(freckles=True, skin='fair', hair='ginger'))]
    for i, (lab, a) in enumerate(acc):
        cfg = dict(base, hairstyle='short', **a)
        tile_sprite(cfg, 48 + i * 132, y, lab, i + 3)
    ax = 48 + 8 * 132 + 20
    for i, (lab, a) in enumerate([acc[3], acc[6], acc[4]]):
        tile_bust(dict(base, hairstyle='short', **a), ax + i * 0 + (i % 3) * 0 + [0, 140, 280][i] - (0 if i < 2 else 0), y, lab, i + 1) if ax + [0, 140, 280][i] + 128 < 1680 - 40 else None
    y += 48 * 3 + 24 + 50
    im = im.crop((0, 0, W, y))
    im.convert('RGB').save(f'{HERE}/builder-parts.png')


def bust_sizes():
    """The three chat sizes at true display size (light + dark) and magnified."""
    names = ['Wren Halloway', 'Nessa Quill', 'Alder Meadows', 'Tobin Larkspur', 'Odessa Brightmoss', 'Juniper Vale']
    W, H = 1360, 760
    im = Image.new('RGBA', (W, H), BG)
    d = ImageDraw.Draw(im)
    header(d, W, 'Chat avatar busts: 40, 64 and 128 px', '40 px = native 40×40 · 64 px = native 64×64 · 128 px = the 64 px bust at 2x (nearest). '
           'Tiles use the app\'s .av radius and c1–c6 colours.')

    def tile(img, size, x, y, i, dark=False, scale=1):
        T = size
        t = Image.new('RGBA', (T, T), (DARK_TILE if dark else TILE)[i % 6])
        t.alpha_composite(K.up(img, scale) if scale > 1 else img, (0, 0))
        m = Image.new('L', (T, T), 0)
        ImageDraw.Draw(m).rounded_rectangle([0, 0, T - 1, T - 1], {40: 12, 64: 18, 128: 30}[T], fill=255)
        im.paste(t, (x, y), m)

    for half, dark in ((0, False), (1, True)):
        x0 = 48 + half * 640
        lab = '#b9afc4' if dark else INK3
        d.rounded_rectangle([x0, 128, x0 + 616, 128 + 372], 18, fill=DARK_BG if dark else '#ffffff', outline=None if dark else LINE)
        text(d, (x0 + 20, 142), 'dark theme' if dark else 'light theme', 13, 650, lab)
        rows = ((40, 172), (64, 232), (128, 316))
        for size, ry in rows:
            text(d, (x0 + 20, ry + size // 2 - 8), f'{size} px', 13, 650, lab)
        for i, n in enumerate(names):
            c = BYNAME[n]
            cx = x0 + 92 + i * 86
            tile(K.bust(c, 40), 40, cx + 12, 172, i, dark)
            tile(K.bust(c, 64), 64, cx, 232, i, dark)
        for i, n in enumerate(names[:3]):
            tile(K.bust(BYNAME[n], 64), 128, x0 + 92 + i * 172, 316, i, dark, scale=2)
    # magnified 40 px bust to show its pixels
    text(d, (48, 524), 'The 40 px bust magnified 3x (what a 3x-density phone draws for a 40 px tile):', 14, 600, INK2)
    for i, n in enumerate(names):
        b = K.up(K.bust(BYNAME[n], 40), 3)
        t = Image.new('RGBA', b.size, TILE[i % 6]); t.alpha_composite(b)
        im.paste(t, (48 + i * 130, 552))
    im = im.crop((0, 0, W, 700))
    im.convert('RGB').save(f'{HERE}/busts.png')


if __name__ == '__main__':
    raw()
    character_sheet()
    builder_parts()
    bust_sizes()
    print('built: character-sheet.png, builder-parts.png, busts.png, art/sprites, art/busts')
