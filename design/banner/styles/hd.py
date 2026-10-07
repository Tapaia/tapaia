"""Style A, 'Cozy HD pixel': Tapaia Square at golden hour on a 750x250 pixel canvas (shown at 2x / 4x).
Layers are returned separately so style B can reuse the pixel foreground over a painted background.
Lore refs (Snowmoon text): ch1:30 mountain + castle-tower apartments; ch6:221-225 Tapaia Square, basic playground,
library of dull books, gamed ground-floor 'active use' shops; ch6:325-327 staircase + stone tower;
ch5:46 / ch6:10 / ch6:271 green circles on a pole, beside doors, on tables; ch1 privacy robes."""
import math, random
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from kit import *  # noqa

R = random.Random(7)

# ------------------------------------------------------------------ palettes (dusk-tuned, hue-shifted)
SKY_RAMP = ['#211338', '#2a1844', '#341d50', '#43225b', '#552964', '#6a316d', '#813a72', '#9a4674', '#b45572',
            '#cb676d', '#dd7f67', '#ea9a63', '#f3b664', '#f9cf74', '#fde39a', '#fff1c4']
GREENS = ['#1f2a2c', '#2a3a35', '#37503f', '#4b6844', '#6b874b', '#a3a75a', '#d8c070']
STONE = ['#6f5a62', '#8c7470', '#a88e80', '#c2a68e', '#d8bd9c', '#ead2ae']
WOOD = ['#3a2228', '#5a3229', '#7d4a30', '#a2663c', '#c4864f', '#e0a96a']
SLATE = ['#2f2a48', '#3d3659', '#4d456b', '#61597e', '#7d7493']
TERRA = ['#5e2a2e', '#7f3a33', '#a24e3b', '#c06646', '#d98a5c']
GLASS_LIT = ['#f08e4a', '#f7ad5a', '#fdcb73', '#ffe3a0', '#fff3cf']
ROBE = ['#24143a', '#331d4f', '#432863', '#563479', '#6e4592']
CIRCLE = '#39e07a'


# ------------------------------------------------------------------ sky + clouds + far hills
def sky_layer(w=W, h=H, dither=True):
    ys, xs = np.mgrid[0:h, 0:w].astype(np.float32)
    sx, sy = SUN[0] * w / W, SUN[1] * h / H
    d = np.hypot((xs - sx) * .78, (ys - sy) * 1.25) / (w * .42)
    gx, gy = 600 * w / W, 96 * h / H                      # wide afterglow behind the wordmark
    d2 = np.hypot((xs - gx) / (w * .40), (ys - gy) / (h * .42))
    ang = np.arctan2(ys - sy, xs - sx)
    rays = np.clip(np.sin(ang * 23 + 1.3) * .5 + np.sin(ang * 9 + .4) * .5, 0, 1) * np.clip(1 - d * 1.1, 0, 1) * .07
    v = .10 + .40 * (ys / h) ** 1.2 + .62 * np.clip(1 - d, 0, 1) ** 1.8 + .34 * np.clip(1 - d2, 0, 1) ** 1.3 + rays
    v = np.clip(v, 0, 1)
    ramp = np.array([rgb(c) for c in SKY_RAMP], np.float32)
    n = len(ramp)
    if dither:
        t = v * (n - 1) + (BAYER[ys.astype(int) % 4, xs.astype(int) % 4] - .5) * .95
        idx = np.clip(np.round(t), 0, n - 1).astype(int)
        out = ramp[idx]
    else:
        t = v * (n - 1)
        i0 = np.clip(np.floor(t), 0, n - 1).astype(int); i1 = np.clip(i0 + 1, 0, n - 1)
        f = (t - i0)[..., None]
        out = ramp[i0] * (1 - f) + ramp[i1] * f
    return Image.fromarray(out.astype(np.uint8)).convert('RGBA')


CLOUDS = [  # (x0, x1, y, thickness) stratus banks that arc over the wordmark and underline the tagline
    (380, 760, 30, 15), (560, 770, 41, 7), (300, 470, 46, 6),
    (440, 640, 146, 8), (590, 770, 152, 11),
    (-20, 170, 26, 12), (110, 300, 16, 7), (230, 360, 62, 6),
]


def cloud_layer(rnd=None):
    rnd = rnd or random.Random(3)
    L = Layer()
    for (x0, x1, y, th) in CLOUDS:
        ph = rnd.random() * 6
        for x in range(int(x0), int(x1)):
            u = (x - x0) / (x1 - x0)
            t = th * math.sin(math.pi * u) ** .55 * (.72 + .22 * math.sin(x * .07 + ph) + .14 * abs(math.sin(x * .19 + ph)))
            if t < .6:
                continue
            top, bot = y - t * .62, y + t * .38      # puffy top, flat lit base
            for yy in range(int(top), int(bot) + 1):
                rel = (yy - top) / max(1, bot - top)
                dsun = math.hypot((x - SUN[0]) * .8, (yy - SUN[1]) * 1.3) / 320
                warm = max(0, 1 - dsun)
                body = mix('#c983a6', '#7e3a68', min(1, warm * 1.25))       # far: lit pink; near sun: backlit violet
                if rel > .8:
                    c = mix('#ffb88f', '#fff0bc', warm)                       # gold underside rim
                elif rel > .62:
                    c = mix(body, '#ffb07a', .45 + .3 * warm)
                elif rel < .14:
                    c = mix(body, '#ffd7b0', .35 * (1 - warm) + .15)          # soft top edge
                else:
                    c = body
                edge = yy == int(top) or yy == int(bot)
                if edge and (x + yy) % 2:
                    continue
                L.p(x, yy, c)
    return L


def far_hills_layer():
    L = Layer()
    for (amp, base, col_far, col_near, ph, f) in ((7, 166, '#8c5079', '#e59a70', 1.3, .021), (6, 174, '#6f3f6e', '#c77a68', 4.0, .03)):
        for x in range(W):
            y = base - amp * (math.sin(x * f + ph) * .6 + math.sin(x * f * 2.7 + ph * 2) * .4)
            dsun = abs(x - SUN[0]) / 330
            c = mix(col_far, col_near, max(0, 1 - dsun) ** 1.4)
            for yy in range(int(y), BASE + 2):
                L.p(x, yy, c)
            L.p(x, int(y), mix(c, '#ffd9a0', .45 * max(0, 1 - dsun)))
    return L


# ------------------------------------------------------------------ canopy (trees, forest texture)
def blob_tree(L, cx, cy, r, ramp, rnd, light=(1, -1)):
    """One leafy cluster: violet-shadow base, mid, sunlit highlight toward the sun (right/up), leaf flecks."""
    L.disc(cx + 1, cy + 1, r, ramp[0])
    L.disc(cx, cy, r, ramp[1])
    L.disc(cx + light[0] * r * .2, cy + light[1] * r * .2, r * .72, ramp[2])
    L.disc(cx + light[0] * r * .42, cy + light[1] * r * .42, max(1, r * .38), ramp[3])
    for _ in range(int(r * r * .5)):
        a = rnd.random() * 6.283; rr = rnd.random() * r
        x, y = cx + math.cos(a) * rr, cy + math.sin(a) * rr
        L.p(x, y, ramp[0] if math.cos(a) * light[0] + math.sin(a) * light[1] < 0 else ramp[min(4, len(ramp) - 1)])


def mountain_profile(x):
    peak, top, foot = 196, 50, 180
    s = 214 if x < peak else 198
    v = max(0, 1 - ((x - peak) / s) ** 2) ** 1.15
    return foot - (foot - top) * v + 2.5 * math.sin(x * .13) + 1.5 * math.sin(x * .41)


TOWERS = [(14, 92, 16), (50, 76, 15), (318, 82, 15), (352, 98, 14)]   # castle-tower apartments: (x, top_y, width) [ch1:30]
STAIR = ((206, 58), (300, 170))                                       # straight outdoor staircase [ch6:325]
ORDER_TOWER = (186, 28, 22, 32)                                       # stone tower at the top [ch6:327]


def castle_tower(L, x, top, w, rnd, emit):
    """~15-storey apartment tower 'shaped like an over-sized medieval castle tower though with far more windows' [ch1:30]."""
    body_h = 178 - top
    for i in range(w):
        u = i / (w - 1)
        t = -.55 + 1.15 * u ** 1.3                    # cylinder shading, sun on the right
        col = shade(STONE[3], t)
        L.rect(x + i, top + 8, 1, body_h, col)
    # corbelled parapet + crenellations
    L.rect(x - 2, top + 5, w + 4, 4, shade(STONE[3], -.1))
    L.rect(x - 2, top + 8, w + 4, 1, shade(STONE[2], -.4))
    for i in range(0, w + 4, 3):
        L.rect(x - 2 + i, top + 3, 2, 2, shade(STONE[3], -.05 + .4 * (i / (w + 4))))
    # conical slate roof
    cx = x + w / 2
    for j in range(13):
        half = (w / 2 + 2) * (j + 1) / 13
        for xx in range(int(cx - half), int(cx + half) + 1):
            u = (xx - (cx - half)) / max(1, 2 * half)
            L.p(xx, top - 9 + j, shade(SLATE[3], -.5 + 1.0 * u))
    L.p(cx, top - 10, SLATE[1])
    # 'far more windows': 15 storeys of small windows, some lit
    for row in range(15):
        yy = top + 12 + row * 4
        if yy > 176:
            break
        for col in range(3):
            xx = x + 3 + col * ((w - 6) // 2)
            lit = rnd.random() < .3
            c = GLASS_LIT[2] if lit else '#3a2a4c'
            L.rect(xx, yy, 2, 2, c)
            if lit:
                emit.rect(xx, yy, 2, 2, GLASS_LIT[3])


def mountain_layer(emit, rnd=None):
    rnd = rnd or random.Random(11)
    L = Layer()
    prof = [mountain_profile(x) for x in range(W)]
    for x in range(-10, 430):
        if 0 <= x < W:
            L.rect(x, int(prof[x]), 1, BASE - int(prof[x]) + 2, GREENS[1])
    # forest texture: crowns everywhere inside the silhouette, the ridge made of crowns
    pts = []
    for y in range(40, BASE, 4):
        for x in range(-10, 430, 5):
            xx = x + rnd.randint(-2, 2); yy = y + rnd.randint(-2, 2)
            if 0 <= xx < W and yy >= prof[min(W - 1, max(0, xx))] - 1:
                pts.append((xx, yy))
    pts.sort(key=lambda p: p[1])
    ramp = GREENS[1:7]
    for (x, y) in pts:
        blob_tree(L, x, y, rnd.choice([3, 4, 4, 5, 6]), ramp, rnd)
    for (x, top, w) in TOWERS:
        castle_tower(L, x, top, w, rnd, emit)
        for k in range(-3, w + 5, 5):                 # trees hug the tower bases ('poked up high above the trees')
            for j in range(3):
                blob_tree(L, x + k, top + 46 + j * 9 + rnd.randint(-2, 2), rnd.choice([4, 5, 6]), ramp, rnd)
    # straight outdoor staircase up the side of the mountain [ch6:325]
    (x0, y0), (x1, y1) = STAIR
    n = int(max(abs(x1 - x0), abs(y1 - y0)))
    for i in range(n + 1):
        x = x0 + (x1 - x0) * i / n; y = y0 + (y1 - y0) * i / n
        step = (i // 2) % 2
        L.p(x - 1, y, STONE[1]); L.p(x, y, STONE[4] if step else STONE[3]); L.p(x + 1, y, STONE[5] if step else STONE[4])
        L.p(x + 2, y, STONE[2])
    for i in range(6):                                  # a few crowns overlapping the stair edge
        t = .12 + i * .15
        blob_tree(L, x0 + (x1 - x0) * t - 4, y0 + (y1 - y0) * t + 3, 3, ramp, rnd)
    # stone tower at the top, open to the sky [ch6:327]
    tx, ty, tw, th = ORDER_TOWER
    for i in range(tw):
        u = i / (tw - 1)
        L.rect(tx + i, ty, 1, th, shade(STONE[3], -.5 + 1.0 * u ** 1.2))
    for yy in range(ty + 3, ty + th, 4):
        off = 0 if (yy // 4) % 2 else 3
        for xx in range(tx + off, tx + tw, 6):
            L.p(xx, yy, shade(STONE[1], -.2))
        L.rect(tx, yy + 2, tw, 1, shade(STONE[2], -.25))
    for i in range(0, tw, 4):
        L.rect(tx + i, ty - 3, 3, 3, shade(STONE[3], -.3 + .8 * i / tw))
    L.rect(tx + 9, ty + 12, 3, 6, '#2c1f36'); L.rect(tx + 14, ty + 8, 2, 4, '#2c1f36')
    emit.ell(tx + 4, ty - 6, tx + tw - 4, ty - 1, '#5af09a', 160)   # the larger, brighter green circle inside glows up
    return L


def treeline_layer(rnd=None):
    rnd = rnd or random.Random(21)
    L = Layer()
    ramp = ['#22292e', '#2c3a35', '#3d503d', '#5a6a44', '#9a8f55']
    xs = list(range(-6, W + 8, 9))
    for x in xs:
        r = rnd.randint(7, 11)
        y = BASE - 6 - rnd.randint(0, 6)
        blob_tree(L, x, y, r, ramp, rnd)
        blob_tree(L, x + 4, y + 6, r - 3, ramp, rnd)
    L.rect(0, BASE - 4, W, 8, ramp[1])
    return L


# ------------------------------------------------------------------ buildings
def door_circle(L, emit, cx, cy):
    """Glowing green circle beside a door [ch6:10]."""
    ring = [(-1, -2), (0, -2), (1, -2), (-2, -1), (2, -1), (-2, 0), (2, 0), (-2, 1), (2, 1), (-1, 2), (0, 2), (1, 2)]
    for dx, dy in ring:
        L.p(cx + dx, cy + dy, CIRCLE); emit.p(cx + dx, cy + dy, CIRCLE)
    L.rect(cx - 1, cy - 1, 3, 3, '#1d5a3c')


def wall_texture(L, x, y, w, h, base, rnd, bricks=False):
    for i in range(w):
        u = i / max(1, w - 1)
        L.rect(x + i, y, 1, h, shade(base, -.32 + .5 * u ** 1.6))
    if bricks:
        for row, yy in enumerate(range(y + 1, y + h, 4)):
            off = 0 if row % 2 else 4
            L.rect(x, yy + 3, w, 1, shade(base, -.38))
            for xx in range(x + off, x + w, 8):
                L.rect(xx, yy, 1, 3, shade(base, -.3))
                bw = 7
                k = rnd.uniform(-.12, .12)
                for b in range(1, bw):
                    if x <= xx + b < x + w and rnd.random() < .85:
                        c = L.get(xx + b, yy)[:3]
                        L.rect(xx + b, yy, 1, 3, shade(c, k))
    else:
        for _ in range(w * h // 9):
            xx = x + rnd.randrange(w); yy = y + rnd.randrange(h)
            c = L.get(xx, yy)[:3]
            L.p(xx, yy, shade(c, rnd.choice([-.08, .06])))


def roof(L, x, y, w, h, ramp, rnd, over=4):
    for j in range(h):
        k = j / h
        x0 = x - over + int((h - j) * .55); x1 = x + w + over - int((h - j) * .55)
        rowc = ramp[2] if (j % 4) else ramp[1]
        for xx in range(x0, x1):
            u = (xx - x0) / max(1, x1 - x0)
            c = shade(rowc, -.35 + .65 * u ** 1.4)
            if j % 4 and (xx + (j // 4) * 3) % 6 == 0:
                c = shade(c, -.25)
            L.p(xx, y - h + j, c)
    L.rect(x - over, y, w + 2 * over, 1, shade(ramp[0], -.2))
    L.rect(x, y + 1, w, 2, shade(ramp[0], -.1), 150)       # eave shadow on the wall
    L.rect(x - over + int(h * .55), y - h - 1, w + 2 * over - int(h * 1.1), 1, shade(ramp[3], .2))


def window(L, emit, x, y, w, h, lit=True, kind='plain', rnd=None):
    L.rect(x - 1, y - 1, w + 2, h + 2, WOOD[1])
    if lit:
        for j in range(h):
            c = GLASS_LIT[min(4, int(4 - 3.5 * j / h))]
            L.rect(x, y + j, w, 1, c); emit.rect(x, y + j, w, 1, c, 200)
    else:
        L.rect(x, y, w, h, '#3c2c4d')
        L.rect(x, y, w, 1, '#6b5a80')
    if kind == 'plain':
        L.rect(x + w // 2, y, 1, h, WOOD[2]); L.rect(x, y + h // 2, w, 1, WOOD[2])
    L.rect(x - 2, y + h + 1, w + 4, 1, WOOD[4])
    L.rect(x - 2, y + h + 2, w + 4, 1, WOOD[2])


def flowerbox(L, x, y, w, rnd):
    L.rect(x, y, w, 2, WOOD[2]); L.rect(x, y + 2, w, 1, WOOD[1])
    for i in range(w):
        L.p(x + i, y - 1, rnd.choice(['#3f6a3a', '#567a40']))
        if rnd.random() < .45:
            L.p(x + i, y - 2, rnd.choice(['#ff8fa0', '#ffd36b', '#c9a0ff', '#fff2d8', '#ff7a5c']))


def door(L, emit, x, y, w, h, circle_side=-1):
    L.rect(x - 1, y - 1, w + 2, h + 1, WOOD[0])
    for i in range(w):
        L.rect(x + i, y, 1, h, shade(WOOD[3], -.35 + .45 * (i / (w - 1))) if i % 3 else WOOD[2])
    L.p(x + w - 3, y + h // 2, '#ffd95a')
    L.rect(x - 2, y + h, w + 4, 1, STONE[4])
    door_circle(L, emit, x - 5 if circle_side < 0 else x + w + 4, y + h // 2 - 2)


def sign_board(L, x, y, w, h, icon=None):
    L.rect(x, y, w, h, WOOD[4]); L.rect(x, y, w, 1, WOOD[5]); L.rect(x, y + h - 1, w, 1, WOOD[2])
    L.rect(x - 1, y, 1, h, WOOD[1]); L.rect(x + w, y, 1, h, WOOD[1])


def house(L, emit, x, w, h, wall, roofr, rnd, sign=None, garden=False):
    y = BASE - h
    wall_texture(L, x, y, w, h, wall, rnd)
    L.rect(x, BASE - 5, w, 5, STONE[2]); L.rect(x, BASE - 5, w, 1, STONE[4])
    if garden:   # 'a garden on the roof' [ch1]
        L.rect(x - 2, y - 3, w + 4, 3, STONE[2]); L.rect(x - 2, y - 3, w + 4, 1, STONE[4])
        for k in range(0, w, 6):
            blob_tree(L, x + k + 3, y - 6, 3, ['#24332c', '#33503a', '#4f7040', '#83964e', '#c2b46a'], rnd)
        for k in range(4, w, 11):
            L.p(x + k, y - 9, '#ff8fa0'); L.p(x + k + 2, y - 8, '#ffd36b')
    else:
        roof(L, x, y, w, 15, roofr, rnd)
    # upper floor windows with flower boxes
    for wx in (x + 7, x + w - 16):
        window(L, emit, wx, y + 8, 9, 11, lit=rnd.random() < .75)
        flowerbox(L, wx - 1, y + 22, 11, rnd)
    # ground floor: shop window + door
    window(L, emit, x + 5, y + 31, 14, 12, lit=True, kind='shop')
    door(L, emit, x + w - 17, y + h - 25, 10, 20, circle_side=-1)
    if sign:
        L.rect(x + w // 2 - 1, y + 28, 7, 1, '#3a2a40'); L.rect(x + w // 2 + 4, y + 28, 1, 3, '#3a2a40')
        sign_board(L, x + w // 2 + 1, y + 31, 8, 7)
        ico = {'bread': [('#c98d4f', 2, 3, 5, 2)], 'flower': [('#ff8fa0', 3, 2, 3, 2), ('#4f7a40', 4, 4, 1, 2)],
               'robe': [(ROBE[3], 3, 1, 3, 5)]}[sign]
        for c, dx, dy, ww, hh in ico:
            L.rect(x + w // 2 + 1 + dx - 1, y + 31 + dy, ww, hh, c)


def tea_house(L, emit, x, rnd, w=92, h=58):
    y = BASE - h
    wall_texture(L, x, y + 26, w, h - 26, STONE[3], rnd, bricks=True)
    wall_texture(L, x, y, w, 26, WOOD[4], rnd)
    for xx in range(x, x + w, 9):
        L.rect(xx, y, 2, 26, WOOD[2]); L.rect(xx, y, 1, 26, WOOD[1])
    L.rect(x, y, w, 2, WOOD[1]); L.rect(x, y + 25, w, 2, WOOD[1])
    for k in range(2):
        L.line([(x + 18 + k * 47, y + 2), (x + 27 + k * 47, y + 24)], WOOD[2])
    roof(L, x, y, w, 17, TERRA, rnd)
    window(L, emit, x + 7, y + 7, 12, 12); window(L, emit, x + w - 19, y + 7, 12, 12)
    # hanging tea sign
    sign_board(L, x + 40, y + 6, 13, 10)
    L.rect(x + 43, y + 9, 6, 4, '#fbf1d6'); L.rect(x + 49, y + 10, 2, 2, '#fbf1d6'); L.p(x + 45, y + 8, '#e8d8ff')
    # striped awning with scalloped edge
    ay = y + 28
    for i in range(w + 8):
        stripe = (i // 5) % 2
        base = '#4c7a42' if stripe else '#f1e2bf'
        for j in range(7):
            L.p(x - 4 + i, ay + j, shade(base, -.25 + .2 * (j / 6) + .25 * (i / (w + 8)) ** 2))
        if i % 5 in (1, 2, 3):
            L.p(x - 4 + i, ay + 7, shade(base, -.2))
    L.rect(x - 4, ay - 1, w + 8, 1, WOOD[1])
    L.rect(x - 4, ay + 9, w + 8, 1, shade(STONE[2], -.4), 140)
    # big warm counter window with silhouettes of cups/teapots
    gx, gy, gw, gh = x + 8, ay + 11, w - 34, h - 41
    window(L, emit, gx, gy, gw, gh, kind='shop')
    for k in range(gx + 4, gx + gw - 3, 7):
        L.rect(k, gy + gh - 4, 3, 3, '#a9614a'); L.p(k + 3, gy + gh - 3, '#a9614a')
    door(L, emit, x + w - 22, BASE - 22, 11, 22, circle_side=1)


DULL = ['#5f646e', '#6e6556', '#535d6b', '#857b69', '#4b5058', '#8f8676', '#6a6f78', '#776a5c']


def library(L, emit, x, rnd, w=80, h=66):
    """'All the books are either some boring business books, or things in foreign languages nobody understands,
    either Old Belpakian or something from Haragmir.' [ch6:223]"""
    y = BASE - h
    wall_texture(L, x, y, w, h, STONE[2], rnd, bricks=True)
    roof(L, x, y, w, 16, SLATE, rnd)
    # plain signboard
    L.rect(x + 18, y + 5, 44, 11, '#efe4c8'); L.rect(x + 18, y + 5, 44, 1, '#fff6dc')
    L.rect(x + 17, y + 5, 1, 11, WOOD[1]); L.rect(x + 62, y + 5, 1, 11, WOOD[1]); L.rect(x + 18, y + 15, 44, 1, WOOD[2])
    text3(L, x + 26, y + 8, 'LIBRARY', '#2b2230')
    # window displays of dull spines: business books (gold title bands) + foreign-script spines (pale squiggles)
    for wx in (x + 7, x + w - 27):
        wy = y + 24
        L.rect(wx - 2, wy - 2, 24, 30, WOOD[1]); L.rect(wx, wy, 20, 26, '#2b2028')
        for sy in (wy + 8, wy + 16, wy + 25):
            L.rect(wx, sy, 20, 1, WOOD[4]); L.rect(wx, sy + 1, 20, 1, WOOD[2]) if sy < wy + 25 else None
            for i in range(20):
                c = DULL[(i * 5 + sy) % len(DULL)]
                hh = 6 + (i * 7 + sy) % 2
                L.rect(wx + i, sy - hh, 1, hh, shade(c, -.1 + .25 * (i / 19)))
                if (i + sy) % 5 == 0:
                    L.p(wx + i, sy - hh + 2, '#d8cfbb'); L.p(wx + i, sy - hh + 4, '#d8cfbb')
                elif (i + sy) % 5 == 2:
                    L.p(wx + i, sy - 3, '#b9a46a')
        for j in range(26):                         # warm interior light catching the glass
            if j % 3 == 0:
                L.p(wx + 19, wy + j, '#f7c98a'); emit.p(wx + 19, wy + j, '#f7c98a', 120)
        L.rect(wx - 3, wy + 28, 26, 1, WOOD[4])
    door(L, emit, x + w // 2 - 6, BASE - 24, 12, 24, circle_side=-1)
    L.rect(x + w // 2 - 8, BASE - 27, 16, 2, STONE[4])


def empty_shop(L, emit, x, rnd, w=58, h=52):
    """Ground-floor 'active use' storefront nobody wants [ch6:225]: one stool on a plinth under an OPEN sign.
    (The contents are our joke, not canon.)"""
    y = BASE - h
    wall_texture(L, x, y, w, h, '#e3c9a2', rnd)
    roof(L, x, y, w, 14, TERRA, rnd)
    window(L, emit, x + 8, y + 7, 9, 10, lit=False); window(L, emit, x + w - 17, y + 7, 9, 10, lit=False)
    gx, gy, gw, gh = x + 5, y + 24, 34, 23
    L.rect(gx - 2, gy - 2, gw + 4, gh + 4, WOOD[1])
    for j in range(gh):
        L.rect(gx, gy + j, gw, 1, mix('#f4efe2', '#d9d2c2', j / gh))
    emit.rect(gx, gy, gw, gh, '#fff6e0', 70)
    text3(L, gx + 10, gy + 3, 'OPEN', '#3f7a37')
    L.rect(gx + 12, gy + gh - 5, 11, 5, STONE[3]); L.rect(gx + 12, gy + gh - 5, 11, 1, STONE[5])
    L.rect(gx + 14, gy + gh - 10, 7, 2, WOOD[3])
    for lx in (gx + 14, gx + 20):
        L.rect(lx, gy + gh - 8, 1, 3, WOOD[1])
    door(L, emit, x + w - 15, BASE - 22, 10, 22, circle_side=-1)


# ------------------------------------------------------------------ plaza
def plaza_layer(emit, rnd=None, lamps=(), lit_windows=()):
    rnd = rnd or random.Random(5)
    L = Layer()
    y = BASE
    rowh = 3
    while y < H:
        x = -rnd.randint(0, 8)
        while x < W:
            sw = int(rowh * 2.6 + rnd.randint(-2, 3))
            base = mix(STONE[2], STONE[4], rnd.random() * .6)
            dsun = abs(x - SUN[0]) / 300
            base = mix(base, '#f0b27a', max(0, 1 - dsun) * .45)
            base = shade(base, -.38 + .25 * (y - BASE) / (H - BASE))
            L.rect(x, y, sw, rowh, base)
            L.rect(x, y, sw, 1, shade(base, .25))
            L.rect(x + sw - 1, y, 1, rowh, shade(base, -.35))
            x += sw
        L.rect(0, y + rowh - 1, W, 1, '#5d3f55')
        y += rowh
        rowh = min(9, rowh + (1 if rnd.random() < .55 else 0))
    # glossy reflections: the low sun streaks across the paving toward the viewer, plus lit-window drips
    for yy in range(BASE, H):          # horizontal glints on polished stone, a column of light under the sun/coin
        k = (yy - BASE) / (H - BASE)
        width = 8 + 30 * k
        xx = int(SUN[0] - width)
        while xx < SUN[0] + width:
            seg = rnd.randint(2, 7)
            f = 1 - abs(xx + seg / 2 - SUN[0]) / width
            if rnd.random() < f * .75 * (1 - k * .45):
                for x2 in range(xx, xx + seg):
                    L.p(x2, yy, mix(L.get(x2, yy)[:3], '#ffe6ae', .35 + .3 * f))
            xx += seg + rnd.randint(1, 4)
    for (wx, ww) in lit_windows:
        for yy in range(BASE + 1, BASE + 14):
            if (yy % 3) and rnd.random() < .55:
                xx = wx + rnd.randrange(ww)
                L.p(xx, yy, mix(L.get(xx, yy)[:3], '#ffc77a', .4))
    return L


# ------------------------------------------------------------------ props
def lamp(L, emit, x, gy, h=46):
    iron = '#352743'
    L.rect(x - 3, gy - 3, 7, 3, iron); L.rect(x - 2, gy - 4, 5, 1, iron)
    L.rect(x, gy - h, 2, h - 3, iron); L.rect(x + 1, gy - h, 1, h - 3, '#5a4560')
    L.rect(x - 3, gy - h + 6, 8, 1, iron)
    # lantern
    lx, ly = x - 3, gy - h - 9
    L.rect(lx + 1, ly - 2, 6, 2, iron); L.p(lx + 3, ly - 3, iron); L.p(lx + 4, ly - 3, iron)
    L.rect(lx, ly, 8, 9, iron)
    for j in range(7):
        c = GLASS_LIT[4 - j // 2]
        L.rect(lx + 1, ly + 1 + j, 6, 1, c); emit.rect(lx + 1, ly + 1 + j, 6, 1, c)
    L.rect(lx + 3, ly + 1, 1, 7, '#e6a35a')
    L.rect(lx, ly + 9, 8, 1, iron)
    return (x + 1, ly + 4)


def tea_table(L, emit, x, gy):
    L.ell(x - 9, gy - 2, x + 9, gy + 2, '#3b2440', 90)
    for cx in (x - 10, x + 9):                       # chairs
        L.rect(cx, gy - 12, 2, 12, WOOD[2]); L.rect(cx - 1, gy - 6, 4, 2, WOOD[3])
    L.rect(x - 1, gy - 9, 2, 9, WOOD[1])
    L.ell(x - 8, gy - 12, x + 8, gy - 8, WOOD[3]); L.ell(x - 8, gy - 12, x + 8, gy - 10, WOOD[4])
    L.rect(x - 5, gy - 14, 2, 2, '#fbf1d6'); L.rect(x + 4, gy - 14, 2, 2, '#fbf1d6')
    L.rect(x - 1, gy - 11, 3, 1, CIRCLE); emit.rect(x - 1, gy - 11, 3, 1, CIRCLE)   # green circle on the tabletop [ch6:271]


def tea_cart(L, emit, x, gy):
    L.ell(x - 4, gy - 3, x + 50, gy + 3, '#3b2440', 100)
    for px in (x + 2, x + 43):
        L.rect(px, gy - 42, 2, 30, WOOD[1])
    for i in range(52):
        stripe = (i // 5) % 2
        base = '#4c7a42' if stripe else '#f1e2bf'
        for j in range(6):
            L.p(x - 4 + i, gy - 47 + j, shade(base, -.15 + .3 * (i / 52) - .05 * j))
        if i % 5 in (1, 2, 3):
            L.p(x - 4 + i, gy - 41, shade(base, -.25))
    L.rect(x - 4, gy - 48, 52, 1, WOOD[1])
    # body
    for i in range(46):
        L.rect(x + i, gy - 20, 1, 11, shade(WOOD[3], -.35 + .55 * (i / 45)))
    L.rect(x, gy - 21, 46, 2, WOOD[4]); L.rect(x, gy - 10, 46, 1, WOOD[1])
    for k in range(x + 7, x + 44, 9):
        L.rect(k, gy - 18, 1, 7, WOOD[2])
    # teapot, cups, steam
    L.rect(x + 6, gy - 28, 9, 7, '#f4ead2'); L.rect(x + 8, gy - 30, 5, 2, '#f4ead2'); L.rect(x + 15, gy - 26, 2, 2, '#f4ead2')
    L.rect(x + 6, gy - 28, 2, 7, '#d8c6a4')
    for k in (x + 21, x + 27, x + 33):
        L.rect(k, gy - 24, 4, 3, '#fbf1d6'); L.p(k + 4, gy - 23, '#fbf1d6')
    for j, (dx, dy) in enumerate([(10, 32), (11, 34), (10, 36), (9, 38), (10, 40)]):
        L.p(x + dx, gy - dy, '#fff6e6', 200 - j * 30)
    door_circle(L, emit, x + 40, gy - 15)
    for wx in (x + 8, x + 37):                       # wheels
        L.disc(wx, gy - 5, 5, WOOD[1]); L.disc(wx, gy - 5, 3, WOOD[3]); L.disc(wx, gy - 5, 1, WOOD[1])


def check_in_pole(L, emit, x, gy):
    """'a green circle on top of a one meter tall pole, which was labeled "Check in"' [ch5:46]"""
    L.rect(x, gy - 17, 2, 17, '#7c7690'); L.rect(x + 1, gy - 17, 1, 17, '#b3acc4')
    L.rect(x - 2, gy - 1, 6, 1, '#5b5470')
    cx, cy = x + 1, gy - 22
    for a in range(0, 360, 12):
        px = cx + 4.2 * math.cos(math.radians(a)); py = cy + 4.2 * math.sin(math.radians(a))
        L.p(px, py, CIRCLE); emit.p(px, py, CIRCLE)
    L.disc(cx, cy, 3, '#1d4a36')
    L.rect(cx - 2, cy, 4, 1, '#a8ffc8')


def bench(L, x, gy, w=26):
    for j, c in enumerate([WOOD[4], WOOD[2], WOOD[4], WOOD[2]]):
        L.rect(x, gy - 13 + j * 2, w, 1, shade(c, .1 if j % 2 == 0 else -.1))
    L.rect(x, gy - 6, w, 2, WOOD[4]); L.rect(x, gy - 4, w, 1, WOOD[1])
    for lx in (x + 2, x + w - 4):
        L.rect(lx, gy - 6, 2, 6, '#352743')


def playground(L, x, gy):
    """'the playground is much more basic, my son says it's not even comfortable' [ch6:221] - bare, empty."""
    g, gd, gl = '#7f7a92', '#5a5470', '#aaa4bd'
    L.ell(x - 2, gy - 2, x + 50, gy + 3, '#3b2440', 70)
    L.line([(x, gy), (x + 4, gy - 30)], g, 2); L.line([(x + 30, gy), (x + 26, gy - 30)], g, 2)
    L.rect(x + 2, gy - 31, 27, 2, gd); L.rect(x + 2, gy - 31, 27, 1, gl)
    L.rect(x + 11, gy - 29, 1, 20, gl); L.rect(x + 19, gy - 29, 1, 20, gl)
    L.rect(x + 10, gy - 9, 11, 2, WOOD[2])
    sx = x + 36
    L.rect(sx, gy - 18, 2, 18, g); L.rect(sx + 5, gy - 18, 2, 18, g)
    for yy in range(gy - 16, gy, 4):
        L.rect(sx, yy, 7, 1, gd)
    for i in range(14):
        L.rect(sx + 7 + i, gy - 18 + i, 1, 2, gl)


def big_tree(L, x, gy, h, r, rnd, maple=False):
    ramp = ['#4a1c2e', '#7a2a32', '#b2443a', '#e0703f', '#ffb066'] if maple else ['#24302c', '#2f4537', '#45613f', '#6f8a4a', '#b5ad62']
    L.ell(x - r - 2, gy - 3, x + r + 4, gy + 3, '#3b2440', 110)
    for i in range(5):
        L.rect(x - 2 + i, gy - h, 1, h, shade(WOOD[2], -.4 + .2 * i))
    L.rect(x - 4, gy - 3, 9, 3, WOOD[1])
    L.line([(x, gy - h + 8), (x - 8, gy - h - 2)], WOOD[2], 2); L.line([(x + 2, gy - h + 6), (x + 9, gy - h - 3)], WOOD[2], 2)
    cy = gy - h - r * .3
    clusters = [(0, -r * .55, r * .62), (-r * .55, -r * .1, r * .55), (r * .55, -r * .05, r * .55),
                (-r * .2, r * .3, r * .55), (r * .3, r * .35, r * .5), (0, 0, r * .6)]
    for dx, dy, rr in clusters:
        blob_tree(L, x + dx, cy + dy, rr, ramp, rnd)


# ------------------------------------------------------------------ people (sel-out outlines, rim light)
HEAD = [".....HHHH.....", "...HHHHHHHH...", "..HHHHHHHHHH..", "..HHHHHHHHHH..", "..HHSSSSSSHH..",
        "..HSSSSSSSSH..", "..HSSESSESSH..", "..HSSSSSSSSH..", "...SSSSSSSS...", "....SSSSSS....", ".....SSSS....."]
HEAD_LONG = HEAD[:8] + ["..HSSSSSSSSH..", "..HHSSSSSSHH..", "..HH.SSSS.HH.."]
HOOD = [".....RRRR.....", "...RRRRRRRR...", "..RRRRRRRRRR..", "..RRRRRRRRRR..", "..RRFFFFFFRR..",
        "..RFFFFFFFFR..", "..RFFEFFEFFR..", "..RNNNNNNNNR..", "..RCCCCCCCCR..", "...RCCCCCCR...", "...RRRRRRRR..."]
SHIRT = ["...TTTTTTTT...", "..TTTTTTTTTT..", ".TTTTTTTTTTTT.", ".TtTTTTTTTTtT.", ".TtTTTTTTTTtT.",
         ".TtTTTTTTTTtT.", ".TtTTTTTTTTtT.", ".STTTTTTTTTTS.", "..TTTTTTTTTT..", "...PPPPPPPP...",
         "...PPPPPPPP...", "...PPP..PPP...", "...PPP..PPP...", "...PPP..PPP...", "...PPP..PPP...",
         "...PPP..PPP...", "...BBB..BBB...", "..BBBB..BBBB.."]
ROBE_BODY = ["...RRRRRRRR...", "..RRRRRRRRRR..", ".RRRRRRRRRRRR.", ".RrRRRRRRRRrR.", ".RrRRRRRRRRrR.",
             ".RrRRRRRRRRrR.", ".RrRRRRRRRRrR.", ".SRRRRRRRRRRS.", ".RRRRRrRRRRRR.", ".RRRRRrRRRRRR.",
             ".RRRRRrRRRRRR.", ".RRRRRrRRRRRR.", ".RRRRRrRRRRRR.", ".RRRRRrRRRRRR.", ".RRRRRRRRRRRR.",
             "..RRRRRRRRRR..", "..UUU....UUU..", "..UUU....UUU.."]
SKINS = {'fair': '#f2cfae', 'warm': '#dda57a', 'tan': '#b97d52', 'deep': '#7d4c34'}
HAIRS = {'chestnut': '#6e3f26', 'black': '#2c2232', 'blonde': '#d9a548', 'ginger': '#b0522c', 'silver': '#b4b0c4'}


def person(kind='shirt', skin='warm', hair='chestnut', shirt='#c8452e', pants='#3d3550', long_hair=False):
    if kind == 'hood':
        rows = HOOD + ROBE_BODY
    elif kind == 'robe':
        head = list(HEAD_LONG if long_hair else HEAD)
        head[10] = "...rrSSSSrr..."              # hood down, bunched behind the neck
        rows = head + ROBE_BODY
    else:
        rows = (HEAD_LONG if long_hair else HEAD) + SHIRT
    pal = {'H': HAIRS[hair], 'S': SKINS[skin], 'E': '#2a1a30', 'T': shirt, 't': shade(shirt, -.3), 'P': pants,
           'B': '#3a2a2e', 'R': ROBE[2], 'r': ROBE[1], 'F': '#170c22', 'N': '#e2d8ee', 'C': ROBE[1], 'U': ROBE[0]}
    if kind == 'hood':   # hood + face cover up, strap across below the eyes [ch1:132, ch1:140]
        pal.update(F='#2a1840', E='#120a1c', N=ROBE[3] if len(ROBE) > 3 else ROBE[2])
    w, h = 16, len(rows) + 2
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); px = im.load()
    for y, row in enumerate(rows):
        filled = [i for i, ch in enumerate(row) if ch != '.']
        lo, hi = (min(filled), max(filled)) if filled else (0, 0)
        for x, ch in enumerate(row):
            if ch == '.':
                continue
            c = pal[ch]
            if ch not in 'EN':
                if x <= lo + 1:
                    c = shade(c, -.32)
                elif x >= hi:
                    c = shade(c, .38)
                if ch == 'H' and y < 3:
                    c = shade(c, .15)
            px[x + 1, y + 1] = rgb(c) + (255,)
    # selective outline: darker hue-shifted version of the neighbouring colour; gold rim on the sun side
    src = im.copy(); sp = src.load()
    for y in range(h):
        for x in range(w):
            if sp[x, y][3]:
                continue
            nb = [(sp[x + dx, y + dy], dx) for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)) if 0 <= x + dx < w and 0 <= y + dy < h and sp[x + dx, y + dy][3]]
            if nb:
                c, dx = nb[0]
                px[x, y] = (shade(c[:3], .5) if dx == -1 else shade(c[:3], -.72)) + (255,)
    return im


PEOPLE = [  # (x, feet_y, kind, skin, hair, shirt, pants, long)  -- 2 of 8 in privacy robes
    (204, 214, 'shirt', 'warm', 'chestnut', '#c4513a', '#3d3550', False),
    (246, 216, 'robe', 'fair', 'ginger', None, None, True),
    (312, 212, 'shirt', 'tan', 'black', '#7f93ad', '#4a3a34', False),
    (360, 236, 'shirt', 'fair', 'blonde', '#e8b84a', '#4a5a78', True),
    (532, 226, 'shirt', 'deep', 'black', '#4f8a4a', '#3d3550', False),
    (582, 228, 'hood', 'warm', 'black', None, None, False),
    (652, 232, 'shirt', 'fair', 'silver', '#5a78b8', '#3d3550', False),
    (470, 238, 'shirt', 'warm', 'chestnut', '#d07a9a', '#3d3550', True),
]


# ------------------------------------------------------------------ assemble
def build(seed=7):
    rnd = random.Random(seed)
    emit = Layer()
    layers = {}
    layers['sky'] = sky_layer()
    layers['clouds'] = cloud_layer()
    layers['hills'] = far_hills_layer()
    m = mountain_layer(emit)
    rim_light(m, .35)
    haze(m, '#a35c7c', .30, top_extra=.12); sun_warm(m, .30)
    layers['mountain'] = m
    t = treeline_layer(); rim_light(t, .4); haze(t, '#8a4a70', .16); sun_warm(t, .3)
    layers['treeline'] = t
    b = Layer()
    house(b, emit, 2, 56, 62, '#a9adb8', SLATE, rnd, sign='bread')
    house(b, emit, 64, 54, 58, '#e3c9a2', TERRA, rnd, sign='flower', garden=True)
    house(b, emit, 124, 52, 64, '#9cb6c8', SLATE, rnd, sign='robe')
    tea_house(b, emit, 184, rnd)
    library(b, emit, 284, rnd)
    empty_shop(b, emit, 372, rnd)
    rim_light(b, .45); sun_warm(b, .22)
    layers['buildings'] = b
    lit_windows = [(9, 14), (71, 14), (131, 14), (192, 58)]
    lamps_xy = [(176, 206), (446, 224), (690, 236)]
    layers['plaza'] = sun_warm(plaza_layer(emit, lit_windows=lit_windows), .2)
    props = Layer()
    lamp_heads = []
    items = []
    items += [('tree', 24, 236, 26, 28, False), ('tree', 506, 214, 24, 22, False), ('tree', 724, 230, 28, 27, True)]
    items += [('table', 214, 208), ('table', 266, 210), ('cart', 520, 222), ('pole', 610, 224), ('bench', 620, 236),
              ('playground', 384, 228)]
    items += [('lamp', x, y) for x, y in lamps_xy]
    items += [('person',) + p for p in PEOPLE]
    items.sort(key=lambda it: it[2])
    for it in items:
        k = it[0]
        if k == 'tree':
            big_tree(props, it[1], it[2], it[3], it[4], rnd, maple=it[5])
        elif k == 'table':
            tea_table(props, emit, it[1], it[2])
        elif k == 'cart':
            tea_cart(props, emit, it[1], it[2])
        elif k == 'pole':
            check_in_pole(props, emit, it[1], it[2])
        elif k == 'bench':
            bench(props, it[1], it[2])
        elif k == 'playground':
            playground(props, it[1], it[2])
        elif k == 'lamp':
            lamp_heads.append(lamp(props, emit, it[1], it[2]))
        elif k == 'person':
            _, x, fy, kind, skin, hair, shirt, pants, lh = it
            props.ell(x - 1, fy - 2, x + 15, fy + 2, '#3b2440', 110)
            props.blit(person(kind, skin, hair, shirt or '#000000', pants or '#000000', lh), x, fy - 31)
    rim_light(props, .25); sun_warm(props, .18)
    layers['props'] = props
    # foreground hedge with flowers (frames the bottom edge)
    fg = Layer()
    for x in range(-8, W + 10, 11):
        blob_tree(fg, x, H + 3, rnd.randint(8, 11), ['#1d2626', '#273a31', '#3b5538', '#5f7a44', '#a8a25c'], rnd)
    for _ in range(140):
        x = rnd.randrange(W); y = H - rnd.randint(2, 9)
        if fg.get(x, y)[3]:
            fg.p(x, y, rnd.choice(['#ff8fa0', '#ffd36b', '#c9a0ff', '#fff2d8', '#ff7a5c']))
    sun_warm(fg, .15)
    layers['fg'] = fg
    return layers, emit, lamp_heads


def light_pass(img, emit, lamp_heads, scale=1, smooth=False):
    """Volumetric light: sun bloom behind the coin, lamp halos + pools, window/circle bloom."""
    w, h = img.size
    light = Image.new('RGB', (w, h), (0, 0, 0))
    d = ImageDraw.Draw(light)
    for (x, y) in lamp_heads:
        x, y = x * scale, y * scale
        for r, a in ((34, 26), (22, 40), (12, 70)):
            r *= scale
            d.ellipse([x - r, y - r, x + r, y + r], fill=(int(a * 1.0), int(a * .72), int(a * .4)))
        gy = y + 50 * scale
        d.ellipse([x - 26 * scale, gy - 6 * scale, x + 26 * scale, gy + 6 * scale], fill=(46, 32, 16))
    light = light.filter(ImageFilter.GaussianBlur(6 * scale))
    e = emit.im.resize((w, h), Image.NEAREST) if emit.im.size != (w, h) else emit.im
    bloom = Image.new('RGB', (w, h)); bloom.paste(e, (0, 0), e)
    bloom = bloom.filter(ImageFilter.GaussianBlur(3.5 * scale))
    out = add_light(img, light, 1.0)
    out = add_light(out, bloom, .55)
    return out


def compose(layers, emit, lamp_heads):
    img = layers['sky'].copy()
    for k in ('clouds', 'hills', 'mountain', 'treeline', 'buildings', 'plaza', 'props', 'fg'):
        im = layers[k].im if hasattr(layers[k], 'im') else layers[k]
        img.alpha_composite(im)
    return light_pass(img.convert('RGB'), emit, lamp_heads)


if __name__ == '__main__':
    import os, sys
    here = os.path.dirname(os.path.abspath(__file__))
    os.makedirs(f'{here}/art', exist_ok=True)
    layers, emit, heads = build()
    img = compose(layers, emit, heads)
    img.save(f'{here}/art/A-scene-750x250.png')
    if len(sys.argv) > 1:
        img.resize((1500, 500), Image.NEAREST).save(f'/tmp/logo/hdA_2x_{sys.argv[1]}.png')
    print('A scene ok')
