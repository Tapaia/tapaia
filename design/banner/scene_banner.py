"""Pixel-art Tapaia Square scenes for the @TapaiaSquare X header (original art).
Native 375x125 canvas, upscaled 4x (1500x500) and 8x (3000x1000).
Reuses the scene kit in design/mockups/art (scene.py / sprites.py); see design/visual-reference.md for sources."""
import os, sys, random
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'mockups', 'art'))
sys.dont_write_bytecode = True
import scene  # noqa: E402
from scene import Canvas, C, hex2rgba  # noqa: E402
from sprites import mini  # noqa: E402

W, H = 375, 125

SKY = {
    'day': ['#5f9fd8', '#6fa8dc', '#83b6e2', '#9cc6e8', '#b8d8ea', '#d4e4e4', '#efe4c8'],
    'dusk': ['#33204f', '#45285c', '#5e3166', '#86416c', '#b45c66', '#de8a5e', '#f4b764', '#ffd98a'],
}
CLOUD = {'day': ('#fbf8f0', '#d4e2ee'), 'dusk': ('#f6b48e', '#b8677a')}


def sky_layer(mode, horizon=H):
    c = Canvas(W, H)
    bands = SKY[mode]
    n = len(bands)
    for y in range(H):
        t = min(1, y / max(1, horizon - 1)) * (n - 1)
        i = int(t); f = t - i
        a, b = bands[min(i, n - 1)], bands[min(i + 1, n - 1)]
        for x in range(W):
            c.p(x, y, b if (f > .75 or (f > .5 and (x + y) % 2 == 0) or (f > .25 and (x % 2 == 0 and y % 2 == 0))) else a)
    return c


def cloud(c, x, y, s, cols):
    blobs = [(0, 3, 4), (5, 0, 6), (12, 2, 5), (17, 4, 3)]
    for bx, by, r in blobs:
        c.disc(x + int(bx * s), y + int(by * s) + 1, int(r * s), cols[1])
    for bx, by, r in blobs:
        c.disc(x + int(bx * s), y + int(by * s), int(r * s), cols[0])
    c.rect(x - int(3 * s), y + int(5 * s), int(23 * s), max(1, int(2 * s)), cols[1])


def tea_cart(c, x, base):
    """Design choice: a wooden tea cart with a striped awning (the square is where 'you can sit down, drink tea' [ch6])."""
    wood = C['wood']
    # awning poles + striped canopy
    c.rect(x + 1, base - 22, 1, 14, wood[0]); c.rect(x + 20, base - 22, 1, 14, wood[0])
    for i in range(24):
        col = ['#3f7a37', '#f4e4bc'][(i // 3) % 2]
        c.rect(x - 1 + i, base - 25, 1, 4, col)
        if i % 3 == 1:
            c.p(x - 1 + i, base - 21, col)
    c.rect(x - 1, base - 26, 24, 1, wood[1])
    # cart body
    c.rect(x, base - 9, 22, 6, wood[2]); c.rect(x, base - 9, 22, 1, wood[3]); c.rect(x, base - 4, 22, 1, wood[1])
    for xx in range(x + 3, x + 22, 5):
        c.rect(xx, base - 8, 1, 4, wood[1])
    # counter: teapot + cups + a green pay circle [ch3, ch6]
    c.rect(x + 3, base - 12, 5, 3, '#fbf1d6'); c.rect(x + 4, base - 13, 3, 1, '#fbf1d6'); c.p(x + 8, base - 11, '#fbf1d6')
    c.p(x + 2, base - 11, '#e6d3a8')
    for xx in (x + 11, x + 14):
        c.rect(xx, base - 11, 2, 2, '#fbf1d6')
    for i, (dx, dy) in enumerate(((4, 15), (5, 16), (4, 17), (12, 13), (13, 14))):
        c.p(x + dx, base - dy, '#ffffff' if i % 2 else '#e9e4dc')
    for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
        c.p(x + 18 + dx, base - 11 + dy, C['green_circle'])
    # wheels
    for wx in (x + 4, x + 17):
        c.disc(wx, base - 2, 2, wood[0]); c.p(wx, base - 2, wood[3])


TOWER_WARM = ['#8f8679', '#b9ad99', '#d9cfba']


def world_layer(L, mode, seed=11):
    C['tower'] = TOWER_WARM          # warmer stone towers for the banner (cozier than the mockup grey)
    rnd = random.Random(seed)
    back = Canvas(W, H)
    c = back
    base = L['base']
    m = L.get('mountain')
    if m:
        scene.mountain(c, m[0], m[1], base - 6, m[2], rnd)
    for t in L.get('towers', []):
        tx, th, tw, lift = t
        scene.castle_tower(c, tx, base - 6 - lift, th, tw)
    for t in L.get('towers', []):
        tx, th, tw, lift = t
        by = base - 6 - lift
        for k in range(-1, tw + 2, 3):
            r = rnd.randint(2, 3 + tw // 4)
            c.disc(tx + k, by - rnd.randint(0, 2), r, C['mtn'][0])
            c.disc(tx + k - 1, by - rnd.randint(1, 3), max(1, r - 1), C['mtn'][2])
    c = Canvas(W, H)
    for x in range(-4, W + 4, 7):
        r = rnd.randint(5, 8)
        c.disc(x, base - 6, r, C['tree'][1])
        c.disc(x - 1, base - 7, max(2, r - 3), C['tree'][2])
    for bx, by in L.get('birds', []):
        scene.bird(c, bx, by)
    lit = mode == 'dusk'
    orig_window = scene.window
    def win(cc, x, y, w, h, lit=False, books=False, rnd=None, _dusk=lit):
        return orig_window(cc, x, y, w, h, lit=lit or (_dusk and not books), books=books, rnd=rnd)
    scene.window = win
    try:
        for kind, x, *args in L['buildings']:
            if kind == 'library':
                scene.library(c, x, base, rnd)
            elif kind == 'tea':
                scene.tea_house(c, x, base, rnd)
            elif kind == 'house':
                w, h, wall, roof, sk, rg = args
                scene.small_house(c, x, base, w, h, C[wall], C[roof], sk, rg, lit=False, rnd=rnd)
    finally:
        scene.window = orig_window
    scene.plaza(c, base, rnd)
    lamps = []
    for kind, x, y, *args in sorted(L['props'], key=lambda p: p[2]):
        y = base + y
        if kind == 'tree':
            scene.shadow(c, x, y, args[1] + 2)
            scene.tree(c, x, y, args[0], args[1], rnd, maple=args[2] if len(args) > 2 else False)
        elif kind == 'lamp':
            h = args[0] if args else 14
            scene.lamp(c, x, y, h)
            lamps.append((x, y - h - 2))
        elif kind == 'bench':
            scene.bench(c, x, y)
        elif kind == 'table':
            scene.table(c, x, y)
        elif kind == 'circle':
            scene.green_circle_pole(c, x, y)
        elif kind == 'cart':
            scene.shadow(c, x + 11, y, 13)
            tea_cart(c, x, y)
        elif kind == 'grass':
            w = args[0]
            c.d.ellipse([x - w, y - 4, x + w, y + 4], fill=hex2rgba(C['grass'][1]))
            c.d.ellipse([x - w + 2, y - 4, x + w - 2, y + 2], fill=hex2rgba(C['grass'][2]))
            for _ in range(w):
                c.p(x + rnd.randint(-w + 2, w - 2), y + rnd.randint(-3, 2), C['grass'][0])
        elif kind == 'flowerbed':
            scene.flowerbed(c, x, y, args[0], rnd)
        elif kind == 'person':
            k, skin, hair, shirt = args
            scene.shadow(c, x + 4, y, 4)
            c.blit(mini(k, skin, hair, shirt), x, y - 13)
    for x in range(-6, W + 6, 9):          # foreground hedge framing the bottom edge
        r = rnd.randint(5, 8)
        c.disc(x, H + 2, r, C['tree'][1]); c.disc(x - 1, H + 1, r - 2, C['tree'][2])
        c.disc(x - 2, H, max(1, r - 5), C['tree'][3])
        if rnd.random() < .6:
            c.p(x + rnd.randint(-3, 3), H - rnd.randint(2, 5), rnd.choice(C['flower']))
    return back, c, lamps


EMISSIVE = {hex2rgba(h)[:3] for h in ('#ffe9a8', '#39e07a', '#e8c070', '#ffd95a')}


def grade_dusk(img):
    """Golden-hour grade: warm highlights, violet shadows; emissive pixels (lamps, lit windows, green circles) untouched."""
    px = img.load()
    for y in range(img.height):
        for x in range(img.width):
            r, g, b, a = px[x, y]
            if a == 0 or (r, g, b) in EMISSIVE:
                continue
            lum = (0.3 * r + 0.59 * g + 0.11 * b) / 255
            k = 0.62 + 0.25 * lum
            nr = r * k * 1.06 + 16 * lum
            ng = g * k * 0.86 + 4 * lum
            nb = b * k * 0.86 + 22 * (1 - lum)
            px[x, y] = (min(255, int(nr)), min(255, int(ng)), min(255, int(nb)), a)
    return img


def add_glows(img, lamps, cols=('#ffc36a',), r=11, alpha=70):
    """Additive warm light around lamp heads plus a pool on the paving, in stepped (pixel) rings."""
    from PIL import ImageChops
    m = Image.new('L', img.size, 0)
    d = ImageDraw.Draw(m)
    for (x, y) in lamps:
        steps = [(r, alpha * .25), (r * .7, alpha * .45), (r * .45, alpha * .7)]
        for rr, a in steps:
            d.ellipse([x - rr, y - rr, x + rr, y + rr], fill=int(a))
        for rx, ry, a in ((13, 3, alpha * .3), (8, 2, alpha * .5)):
            d.ellipse([x - rx, y + 17 - ry, x + rx, y + 17 + ry], fill=int(a))
    col = Image.new('RGB', img.size, hex2rgba(cols[0])[:3])
    light = ImageChops.multiply(col, Image.merge('RGB', (m, m, m)))
    rgb = ImageChops.add(img.convert('RGB'), light)
    img.paste(Image.merge('RGBA', (*rgb.split(), img.split()[3])), (0, 0))
    return img


LAYOUT = dict(
    base=94,
    clouds=[(14, 10, 1.1), (118, 6, 0.8), (205, 16, 0.7)],
    mountain=(-10, 228, 30),
    towers=[(58, 30, 7, 6), (92, 38, 8, 20), (132, 34, 8, 14), (170, 28, 7, 6)],
    birds=[(196, 12), (202, 10), (208, 13)],
    buildings=[
        ('house', 2, 28, 22, 'grey', 'roof_slate', 'bread', False),
        ('tea', 104, ),
        ('library', 160, ),
        ('house', 36, 28, 20, 'beige', 'terracotta', 'flower', True),
        ('house', 68, 28, 23, 'blue', 'roof_slate', 'robe', False),
        ('house', 206, 28, 19, 'beige', 'terracotta', 'flower', False),
    ],
    props=[
        ('tree', 16, 26, 30, 14),
        ('flowerbed', 0, 31, 120),
        ('lamp', 98, 8, 16), ('table', 112, 9), ('table', 138, 9),
        ('person', 120, 9, 'robe', 'warm', 'chestnut', ''), ('person', 146, 10, 'shirt', 'fair', 'ginger', '#5c9a3e'),
        ('person', 176, 11, 'hood', 'warm', 'black', ''),
        ('bench', 196, 14), ('person', 210, 14, 'robe', 'deep', 'black', ''),
        ('tree', 244, 12, 24, 11),
        ('cart', 262, 16), ('circle', 288, 16), ('person', 276, 19, 'robe', 'fair', 'silver', ''),
        ('person', 294, 19, 'shirt', 'deep', 'black', '#64408a'),
        ('lamp', 314, 14, 16), ('bench', 322, 20), ('person', 330, 21, 'hood', 'tan', 'plum', ''),
        ('tree', 362, 18, 26, 13, True),
        ('grass', 240, 30, 30), ('grass', 352, 32, 26),
        ('person', 232, 27, 'shirt', 'tan', 'black', '#f2c84b'),
        ('flowerbed', 200, 33, 175),
        ('person', 158, 22, 'robe', 'tan', 'chestnut', ''), ('person', 186, 24, 'shirt', 'fair', 'blonde', '#3f6fd8'),
        ('person', 300, 27, 'robe', 'warm', 'black', ''), ('grass', 130, 31, 16),
        ('circle', 132, 10),
    ],
)


def render(mode, layout=LAYOUT, clouds=True, sky=True):
    if not sky:
        back, world, lamps = world_layer(layout, mode)
        img = grade_dusk(world.img) if mode == 'dusk' else world.img
        if mode == 'dusk':
            add_glows(img, lamps, r=15, alpha=120)
        out = haze(grade_dusk(back.img), '#4f3276', .62) if mode == 'dusk' else back.img
        out.alpha_composite(img)
        return out
    sky = sky_layer(mode)
    if clouds:
        for x, y, s in layout['clouds']:
            cloud(sky, x, y, s, CLOUD[mode])
    back, world, lamps = world_layer(layout, mode)
    bk = back.img
    if mode == 'dusk':
        bk = haze(grade_dusk(bk), '#9a4f6e', .45)
        img = grade_dusk(world.img)
        add_glows(img, lamps, r=17, alpha=150)
    else:
        bk = haze(bk, '#c9dbe6', .22)
        img = world.img
    out = sky.img.copy()
    out.alpha_composite(bk)
    out.alpha_composite(img)
    return out


def haze(img, col, k):
    r0, g0, b0, _ = hex2rgba(col)
    px = img.load()
    for y in range(img.height):
        for x in range(img.width):
            r, g, b, a = px[x, y]
            if a:
                px[x, y] = (int(r + (r0 - r) * k), int(g + (g0 - g) * k), int(b + (b0 - b) * k), a)
    return img


STRIP = dict(
    base=112,
    mountain=(150, 375, 62),
    towers=[(214, 26, 6, 10), (246, 32, 7, 20), (284, 28, 6, 12), (320, 22, 6, 4)],
    buildings=[
        ('house', -6, 28, 22, 'grey', 'roof_slate', 'bread', False),
        ('house', 26, 28, 20, 'beige', 'terracotta', 'flower', True),
        ('tea', 62, ),
        ('library', 118, ),
        ('house', 166, 28, 23, 'blue', 'roof_slate', 'robe', False),
        ('house', 200, 28, 19, 'beige', 'terracotta', 'flower', False),
        ('house', 296, 28, 22, 'blue', 'terracotta', None, True),
        ('house', 336, 30, 21, 'grey', 'roof_slate', 'bread', False),
    ],
    props=[
        ('lamp', 56, 6, 14), ('table', 70, 6), ('table', 96, 6),
        ('person', 80, 6, 'robe', 'warm', 'chestnut', ''), ('person', 104, 7, 'shirt', 'fair', 'ginger', '#5c9a3e'),
        ('person', 140, 7, 'hood', 'warm', 'black', ''), ('tree', 160, 6, 18, 10),
        ('bench', 176, 7), ('person', 188, 7, 'robe', 'deep', 'black', ''),
        ('tree', 240, 6, 20, 11), ('cart', 252, 7), ('circle', 278, 7),
        ('person', 266, 8, 'robe', 'fair', 'silver', ''), ('person', 284, 8, 'shirt', 'deep', 'black', '#64408a'),
        ('lamp', 300, 6, 14), ('person', 318, 7, 'hood', 'tan', 'plum', ''),
        ('tree', 368, 6, 20, 11, True), ('tree', 14, 6, 18, 10),
    ],
)


if __name__ == '__main__':
    for m in ('day', 'dusk'):
        im = render(m)
        im.save(f'/tmp/logo/scene_{m}.png')
        im.resize((W * 4, H * 4), Image.NEAREST).save(f'/tmp/logo/scene_{m}_4x.png')
    print('ok')
