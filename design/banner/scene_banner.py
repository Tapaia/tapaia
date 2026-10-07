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




# ---------------------------------------------------------------- lore pieces (Snowmoon refs in comments)
FONT3 = {  # 3x5 pixel letters for tiny signs
    'L': ["x..", "x..", "x..", "x..", "xxx"], 'I': ["xxx", ".x.", ".x.", ".x.", "xxx"],
    'B': ["xx.", "x.x", "xx.", "x.x", "xx."], 'R': ["xx.", "x.x", "xx.", "x.x", "x.x"],
    'A': [".x.", "x.x", "xxx", "x.x", "x.x"], 'Y': ["x.x", "x.x", ".x.", ".x.", ".x."],
    'O': ["xxx", "x.x", "x.x", "x.x", "xxx"], 'P': ["xx.", "x.x", "xx.", "x..", "x.."],
    'E': ["xxx", "x..", "xx.", "x..", "xxx"], 'N': ["x..x", "xx.x", "x.xx", "x..x", "x..x"],
}


def text3(c, x, y, word, col):
    for ch in word:
        for j, row in enumerate(FONT3[ch]):
            for k, v in enumerate(row):
                if v == 'x':
                    c.p(x + k, y + j, col)
        x += len(FONT3[ch][0]) + 1


def door_circle(c, cx, cy):
    """Glowing green circle beside a door: 'tapped his watch against a glowing green circle beside the door' [ch6:10]."""
    for dx, dy in ((0, -2), (1, -2), (-1, -1), (2, -1), (-1, 0), (2, 0), (0, 1), (1, 1)):
        c.p(cx + dx, cy + dy, C['green_circle'])
    for dx, dy in ((0, -1), (1, -1), (0, 0), (1, 0)):
        c.p(cx + dx, cy + dy, '#1f6e45')


DULL = ['#5f646e', '#6e6556', '#535d6b', '#857b69', '#4b5058', '#8f8676', '#6a6f78']


def library(c, x, base, rnd):
    """Tapaia's library: 'All the books are either some boring business books, or things in foreign languages
    nobody understands, either Old Belpakian or something from Haragmir.' [ch6:223]"""
    w, h = 40, 30
    scene.brick_wall(c, x, base - h, w, h)
    scene.pitched_roof(c, x, base - h, w, 7, C['roof_slate'])
    c.outline(x, base - h, w, h, C['stone'][0])
    # plain signboard
    c.rect(x + 4, base - 28, 32, 7, '#efe6cf'); c.outline(x + 4, base - 28, 32, 7, C['wood'][0])
    text3(c, x + 7, base - 27, 'LIBRARY', '#2b2530')
    # window displays: rows of identical dull spines; a few with unreadable foreign-script marks
    for wx in (x + 3, x + 27):
        c.rect(wx - 1, base - 20, 12, 11, C['wood'][1])
        c.rect(wx, base - 19, 10, 9, '#2f2a2a')
        for shelf_y in (base - 15, base - 10):
            c.rect(wx, shelf_y, 10, 1, C['wood'][3])
            for i in range(10):
                col = DULL[(i * 3 + shelf_y) % len(DULL)]
                c.rect(wx + i, shelf_y - 4, 1, 4, col)
                if (i + shelf_y) % 4 == 0:                  # pale squiggle = Old Belpakian / Haragmir script
                    c.p(wx + i, shelf_y - 3, '#d8cfbb')
                elif (i + shelf_y) % 4 == 2:                # thin gold title band = business books
                    c.p(wx + i, shelf_y - 2, '#b9a46a')
        c.rect(wx - 1, base - 9, 12, 1, C['wood'][3])
    # door + green circle beside it
    c.rect(x + 16, base - 12, 8, 12, C['wood'][1]); c.rect(x + 17, base - 11, 6, 11, C['wood'][2])
    c.p(x + 21, base - 6, '#ffd95a')
    door_circle(c, x + 14, base - 6)


def empty_shop(c, x, base, rnd, w=30, h=21):
    """A ground-floor 'active use' storefront that nobody wants: 'putting things in that theoretically qualify
    but that nobody actually wants to use' [ch6:225]. One lone stool on a plinth under an OPEN sign, no customers.
    (The exact contents are our joke, not canon.)"""
    wall = C['beige']
    c.rect(x, base - h, w, h, wall[1]); c.rect(x + w - 1, base - h, 1, h, wall[0]); c.rect(x, base - 1, w, 1, wall[0])
    scene.pitched_roof(c, x, base - h, w, 6, C['terracotta'])
    c.rect(x + 2, base - 17, 19, 14, C['wood'][1])           # big, nearly empty shop window
    c.rect(x + 3, base - 16, 17, 12, '#ece6d6')
    text3(c, x + 4, base - 15, 'OPEN', '#3f7a37')
    c.rect(x + 9, base - 6, 5, 2, '#b1a896')                 # plinth
    c.rect(x + 9, base - 9, 5, 1, C['wood'][2])              # the lone stool
    c.p(x + 9, base - 8, C['wood'][0]); c.p(x + 13, base - 8, C['wood'][0])
    c.p(x + 9, base - 7, C['wood'][0]); c.p(x + 13, base - 7, C['wood'][0])
    c.rect(x + 2, base - 3, 19, 1, C['wood'][3])
    c.rect(x + 22, base - 10, 6, 10, C['wood'][1]); c.rect(x + 23, base - 9, 4, 9, C['wood'][2])
    door_circle(c, x + 24, base - 13)


def basic_playground(c, x, base):
    """'the playground is much more basic, my son says it's not even comfortable' [ch6:221]:
    one bare swing frame with a single plank seat and a small plain slide. Nobody on it."""
    g, gd = '#8a92a0', '#6b7380'
    c.rect(x, base - 13, 1, 13, g); c.rect(x + 14, base - 13, 1, 13, g)
    c.rect(x, base - 14, 15, 1, gd)
    c.rect(x + 5, base - 13, 1, 9, '#a7adb1'); c.rect(x + 9, base - 13, 1, 9, '#a7adb1')
    c.rect(x + 4, base - 4, 7, 1, C['wood'][1])
    sx = x + 19
    c.rect(sx, base - 8, 1, 8, g); c.rect(sx + 2, base - 8, 1, 8, g)
    for yy in range(base - 7, base, 2):
        c.rect(sx, yy, 3, 1, g)
    for i in range(7):
        c.rect(sx + 3 + i, base - 8 + i, 1, 1, '#c7ccd6')
    c.rect(sx + 9, base - 1, 2, 1, '#c7ccd6')


def mountain_stair_and_tower(c, stair, tower):
    """'a straight, two-hundred-meter-tall outdoor staircase on the side of the mountain' and, at the top,
    'the top floor of a tower, surrounded by stone walls. He could see the sky above him.' [ch6:325-327]"""
    (x0, y0), (x1, y1) = stair
    n = max(abs(x1 - x0), abs(y1 - y0))
    for i in range(n + 1):
        x = round(x0 + (x1 - x0) * i / n); y = round(y0 + (y1 - y0) * i / n)
        c.p(x, y, '#d8cfbb'); c.p(x + 1, y, '#b1a896')
        if i % 2 == 0:
            c.p(x - 1, y, '#8f877b')
    tx, ty, tw, th = tower
    st = C['stone']
    c.rect(tx, ty, tw, th, st[2]); c.rect(tx, ty, 1, th, st[3]); c.rect(tx + tw - 1, ty, 1, th, st[1])
    for yy in range(ty + 2, ty + th, 3):
        c.rect(tx + 1, yy, tw - 2, 1, st[1])
    for xx in range(tx, tx + tw, 2):                       # open top, crenellated stone walls
        c.p(xx, ty - 1, st[2])
    c.rect(tx + tw // 2 - 1, ty + 4, 2, 3, '#4a4550')       # tunnel mouth / doorway


def world_layer(L, mode, seed=11):
    rnd = random.Random(seed)
    back = Canvas(W, H)
    c = back
    base = L['base']
    m = L.get('mountain')
    if m:
        scene.mountain(c, m[0], m[1], base - 6, m[2], rnd)
    if L.get('stair'):
        mountain_stair_and_tower(c, L['stair'], L['order_tower'])
        tx, ty, tw, th = L['order_tower']
        for k in range(-2, tw + 3, 3):                    # trees hug the tower's base
            c.disc(tx + k, ty + th + 1, 2, C['mtn'][0]); c.disc(tx + k - 1, ty + th, 1, C['mtn'][2])
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
                library(c, x, base, rnd)
            elif kind == 'empty_shop':
                empty_shop(c, x, base, rnd)
            elif kind == 'tea':
                scene.tea_house(c, x, base, rnd)
            elif kind == 'house':
                w, h, wall, roof, sk, rg = args
                scene.small_house(c, x, base, w, h, C[wall], C[roof], sk, rg, lit=False, rnd=rnd)
                door_circle(c, x + w // 2 - 5, base - 5)
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
            scene.green_circle_pole(c, x, y)   # 'a green circle on top of a one meter tall pole' [ch5:46]
        elif kind == 'playground':
            basic_playground(c, x, y)
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


EMISSIVE = {hex2rgba(h)[:3] for h in ('#ffe9a8', '#39e07a', '#e8c070', '#ffd95a', '#1f6e45')}


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
    mountain=(-10, 228, 30),                 # 'a mountain covered with trees' [ch1:30]
    stair=((150, 80), (113, 39)),            # straight outdoor staircase up its side [ch6:325]
    order_tower=(106, 26, 11, 13),           # stone tower at the top [ch6:327]
    birds=[(196, 12), (202, 10), (208, 13)],
    buildings=[
        ('house', 2, 28, 22, 'grey', 'roof_slate', 'bread', False),
        ('house', 36, 28, 20, 'beige', 'terracotta', 'flower', True),
        ('house', 68, 28, 23, 'blue', 'roof_slate', 'robe', False),
        ('tea', 104, ),
        ('library', 160, ),
        ('empty_shop', 206, ),
    ],
    props=[
        ('tree', 16, 26, 30, 14),
        ('flowerbed', 0, 31, 120),
        ('lamp', 98, 8, 16), ('table', 112, 9), ('table', 138, 9),
        ('person', 120, 9, 'shirt', 'warm', 'chestnut', '#c8452e'),
        ('person', 146, 10, 'robe', 'fair', 'ginger', ''),
        ('person', 184, 12, 'shirt', 'tan', 'black', '#8ea3b5'),
        ('playground', 196, 22),
        ('tree', 248, 12, 24, 11),
        ('cart', 262, 16), ('circle', 288, 16),
        ('person', 276, 19, 'shirt', 'deep', 'black', '#5c9a3e'),
        ('person', 294, 19, 'hood', 'warm', 'black', ''),
        ('lamp', 314, 14, 16), ('bench', 322, 20), ('person', 334, 21, 'shirt', 'fair', 'silver', '#3f6fd8'),
        ('tree', 362, 18, 26, 13, True),
        ('grass', 240, 30, 30), ('grass', 352, 32, 26), ('grass', 130, 31, 16),
        ('person', 160, 24, 'shirt', 'fair', 'blonde', '#f2c84b'),
        ('flowerbed', 200, 33, 175),
    ],
)


STRIP = dict(
    base=112,
    mountain=(150, 375, 62),
    stair=((312, 104), (284, 74)),
    order_tower=(276, 60, 11, 13),
    buildings=[
        ('house', -6, 28, 22, 'grey', 'roof_slate', 'bread', False),
        ('house', 26, 28, 20, 'beige', 'terracotta', 'flower', True),
        ('tea', 62, ),
        ('library', 118, ),
        ('empty_shop', 166, ),
        ('house', 200, 28, 19, 'beige', 'terracotta', 'flower', False),
        ('house', 296, 28, 22, 'blue', 'terracotta', None, True),
        ('house', 336, 30, 21, 'grey', 'roof_slate', 'bread', False),
    ],
    props=[
        ('lamp', 56, 6, 14), ('table', 70, 6), ('table', 96, 6),
        ('person', 80, 6, 'shirt', 'warm', 'chestnut', '#c8452e'), ('person', 104, 7, 'robe', 'fair', 'ginger', ''),
        ('person', 146, 7, 'shirt', 'tan', 'black', '#8ea3b5'),
        ('playground', 230, 7),
        ('cart', 252, 7), ('circle', 278, 7),
        ('person', 266, 8, 'shirt', 'deep', 'black', '#5c9a3e'), ('person', 284, 8, 'hood', 'warm', 'black', ''),
        ('lamp', 300, 6, 14), ('person', 318, 7, 'shirt', 'fair', 'blonde', '#3f6fd8'),
        ('tree', 368, 6, 20, 11, True), ('tree', 14, 6, 18, 10),
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


if __name__ == '__main__':
    for m in ('day', 'dusk'):
        im = render(m)
        im.save(f'/tmp/logo/scene_{m}.png')
        im.resize((W * 4, H * 4), Image.NEAREST).save(f'/tmp/logo/scene_{m}_4x.png')
    print('ok')
