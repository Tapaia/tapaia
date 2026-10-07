"""Original pixel-art scene of Tapaia Square, Meldan, drawn from the book's description [ch6]:
seating, tea, shops nearby, a basic playground, a small library of dull business books,
trees and shade; the tree-covered mountain with castle-tower apartments on the skyline [ch1, ch32].
See design/visual-reference.md for sources and design choices.
"""
import random
from PIL import Image, ImageDraw
from sprites import hex2rgba, mini, OUT

C = {
    'sky': ['#6fa8dc', '#7fb3e0', '#93c1e6', '#a9cfea', '#c2dcec', '#d9e6e6', '#f2e4c4'],
    'cloud': '#fbf8f0', 'cloud_s': '#d4e2ee',
    'mtn': ['#5f8a62', '#7aa37a', '#93b98a'],
    'tower': ['#8e8a86', '#b4aea4', '#d2cbbd'], 'roof_slate': ['#4e5b70', '#6b7a92'],
    'tree': ['#24452a', '#2f5a2e', '#3f7a37', '#5c9a3e', '#8cc152'],
    'trunk': ['#3e2415', '#6b3f1f'],
    'stone': ['#6d655c', '#8f877b', '#b1a896', '#cfc6b2'],
    'beige': ['#c9b386', '#e6d3a8'], 'blue': ['#86a8bd', '#a9c8db'], 'grey': ['#878d91', '#a7adb1'],
    'wood': ['#3e2415', '#6b3f1f', '#9a6235', '#c98d4f', '#e2ad6c'],
    'terracotta': ['#8e3f2a', '#b5573a'],
    'pave': ['#a39784', '#b9ad9a', '#c8bda9'],
    'grass': ['#3f7a37', '#5c9a3e', '#7cb342'],
    'glass': ['#2c3e57', '#4a6a8a', '#ffe9a8'],
    'lamp': '#ffe9a8', 'iron': '#2b2530',
    'green_circle': '#39e07a', 'hydra_y': '#f2c84b', 'hydra_g': '#4caf50',
    'maple': ['#8e2f22', '#c8452e', '#e8743c'],
    'flower': ['#f08a8a', '#ffd95a', '#b48cff', '#fbf1d6', '#d8452b'],
    'awning': ['#3f7a37', '#f4e4bc'],
}


class Canvas:
    def __init__(self, w, h):
        self.w, self.h = w, h
        self.img = Image.new('RGBA', (w, h), (0, 0, 0, 0))
        self.d = ImageDraw.Draw(self.img)
        self.px = self.img.load()

    def p(self, x, y, col):
        if 0 <= x < self.w and 0 <= y < self.h:
            self.px[x, y] = hex2rgba(col) if isinstance(col, str) else col

    def rect(self, x, y, w, h, col):
        if w <= 0 or h <= 0:
            return
        self.d.rectangle([x, y, x + w - 1, y + h - 1], fill=hex2rgba(col))

    def outline(self, x, y, w, h, col=OUT):
        self.d.rectangle([x, y, x + w - 1, y + h - 1], outline=hex2rgba(col))

    def disc(self, cx, cy, r, col):
        self.d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=hex2rgba(col))

    def poly(self, pts, col):
        self.d.polygon(pts, fill=hex2rgba(col))

    def blit(self, im, x, y):
        self.img.alpha_composite(im, (x, y))

    def glow(self, cx, cy, r, col, alpha=70):
        ov = Image.new('RGBA', (self.w, self.h), (0, 0, 0, 0))
        dd = ImageDraw.Draw(ov)
        rgb = hex2rgba(col)[:3]
        for i, rr in enumerate(range(r, 0, -max(1, r // 3))):
            dd.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], fill=rgb + (alpha // 3,))
        self.img.alpha_composite(ov)


def sky(c, horizon):
    bands = C['sky']
    n = len(bands)
    for y in range(horizon):
        t = y / max(1, horizon - 1) * (n - 1)
        i = int(t); f = t - i
        col = bands[min(i, n - 1)]
        nxt = bands[min(i + 1, n - 1)]
        for x in range(c.w):
            # ordered dither between bands for the soft 16-bit gradient
            use = nxt if (f > 0.66 or (f > 0.33 and (x + y) % 2 == 0)) else col
            c.p(x, y, use)


def cloud(c, x, y, s=1.0):
    blobs = [(0, 3, 4), (5, 0, 6), (12, 2, 5), (17, 4, 3)]
    for bx, by, r in blobs:
        c.disc(x + int(bx * s), y + int(by * s) + 1, int(r * s), C['cloud_s'])
    for bx, by, r in blobs:
        c.disc(x + int(bx * s), y + int(by * s), int(r * s), C['cloud'])
    c.rect(x - int(3 * s), y + int(5 * s), int(23 * s), max(1, int(2 * s)), C['cloud_s'])


def mountain(c, x0, x1, base, peak_y, rnd):
    w = x1 - x0
    pts = [(x0, base)]
    for i in range(0, w + 1, 2):
        t = i / w
        # soft rounded hump, a little lopsided
        hgt = (1 - (2 * t - 1) ** 2) ** 1.1 * (base - peak_y)
        hgt = max(hgt, (1 - min(1, abs(t - 0.78) / 0.22) ** 2) * (base - peak_y) * 0.72)
        hgt *= 0.95 + 0.05 * ((i // 6) % 2)
        pts.append((x0 + i, int(base - hgt)))
    pts.append((x1, base))
    c.poly(pts, C['mtn'][1])
    # tree texture: dots of dark and light green
    for _ in range(w * (base - peak_y) // 7):
        x = rnd.randint(x0, min(x1, c.w - 2)); y = rnd.randint(peak_y, base)
        if c.px[x, y][:3] == hex2rgba(C['mtn'][1])[:3]:
            c.p(x, y, C['mtn'][0]); c.p(x + 1, y, C['mtn'][0])
            if y > 0 and c.px[x, y - 1][:3] == hex2rgba(C['mtn'][1])[:3]:
                c.p(x, y - 1, C['mtn'][2])
    return pts


def castle_tower(c, x, base, h, w=6):
    st = C['tower']
    c.rect(x, base - h, w, h, st[1])
    c.rect(x, base - h, 1, h, st[2])
    c.rect(x + w - 1, base - h, 1, h, st[0])
    # crenellations + slate cone roof
    for i in range(0, w, 2):
        c.p(x + i, base - h - 1, st[1])
    roof_h = max(3, w // 2 + 1)
    c.poly([(x - 1, base - h - 1), (x + w, base - h - 1), (x + (w - 1) / 2, base - h - 1 - roof_h)],
           C['roof_slate'][0])
    c.p(x + w // 2 - 1, base - h - roof_h + 1, C['roof_slate'][1])
    # "far more windows on the sides" [ch1]
    for yy in range(base - h + 2, base - 1, 2):
        for xx in range(x + 1, x + w - 1, 2):
            c.p(xx, yy, '#4a5560')


def tree(c, x, base, h, r, rnd, maple=False, shadow=True):
    pal = C['maple'] if maple else C['tree'][1:4] + [C['tree'][4]]
    c.rect(x - 1, base - h, 3, h, C['trunk'][1])
    c.rect(x - 1, base - h, 1, h, C['trunk'][0])
    cy = base - h
    blobs = [(0, 0, r), (-r * 0.6, r * 0.25, r * 0.7), (r * 0.6, r * 0.3, r * 0.7), (0, -r * 0.5, r * 0.7)]
    for bx, by, br in blobs:
        c.disc(int(x + bx) + 1, int(cy + by) + 1, int(br), (pal[0]))
    for bx, by, br in blobs:
        c.disc(int(x + bx), int(cy + by), int(br), pal[1])
    for bx, by, br in blobs:
        c.disc(int(x + bx - br * 0.25), int(cy + by - br * 0.3), max(1, int(br * 0.55)), pal[2])
    # leaf sparkle
    for _ in range(int(r * r * 0.5)):
        dx = rnd.randint(-r, r); dy = rnd.randint(-r, r // 2)
        xx, yy = int(x + dx), int(cy + dy - r * 0.3)
        if 0 <= xx < c.w and 0 <= yy < c.h and c.px[xx, yy][:3] == hex2rgba(pal[2])[:3]:
            c.p(xx, yy, pal[3] if len(pal) > 3 else pal[2])
    for _ in range(int(r * r * 0.4)):
        dx = rnd.randint(-r, r); dy = rnd.randint(-r // 2, r)
        xx, yy = int(x + dx), int(cy + dy)
        if 0 <= xx < c.w and 0 <= yy < c.h and c.px[xx, yy][:3] == hex2rgba(pal[1])[:3]:
            c.p(xx, yy, pal[0])


def shadow(c, x, y, w):
    ov = Image.new('RGBA', (c.w, c.h), (0, 0, 0, 0))
    ImageDraw.Draw(ov).ellipse([x - w, y - 2, x + w, y + 2], fill=(40, 30, 20, 60))
    c.img.alpha_composite(ov)


def brick_wall(c, x, y, w, h):
    st = C['stone']
    c.rect(x, y, w, h, st[2])
    for yy in range(y, y + h, 3):
        c.rect(x, yy + 2, w, 1, st[1])
        off = 0 if ((yy - y) // 3) % 2 == 0 else 3
        for xx in range(x + off, x + w, 6):
            c.p(xx, yy, st[1]); c.p(xx, yy + 1, st[1])
    c.rect(x, y, 1, h, st[3])


def window(c, x, y, w, h, lit=False, books=False, rnd=None):
    c.rect(x - 1, y - 1, w + 2, h + 2, C['wood'][1])
    c.rect(x, y, w, h, C['glass'][2] if lit else C['glass'][1])
    if not lit:
        c.p(x, y, '#7fa3c4')
    if books and rnd:
        # "boring business books" and foreign-script spines [ch6]
        for xx in range(x, x + w):
            col = rnd.choice(['#5b6a7a', '#7a6a55', '#4e5b70', '#8a7a5a', '#64408a'])
            top = y + h - rnd.randint(2, max(2, h - 1))
            c.rect(xx, top, 1, y + h - top, col)
        c.rect(x, y + h // 2, w, 1, C['wood'][2])
    c.rect(x - 1, y + h, w + 2, 1, C['wood'][3])


def sign(c, x, y, kind):
    c.rect(x, y, 7, 6, C['wood'][3]); c.outline(x, y, 7, 6, C['wood'][0])
    if kind == 'tea':
        c.rect(x + 2, y + 2, 3, 2, '#fbf1d6'); c.p(x + 5, y + 2, '#fbf1d6'); c.p(x + 2, y + 1, '#7aa64a')
    elif kind == 'flower':
        c.p(x + 3, y + 1, C['flower'][0]); c.p(x + 2, y + 2, C['flower'][0]); c.p(x + 4, y + 2, C['flower'][0])
        c.p(x + 3, y + 2, C['flower'][1]); c.p(x + 3, y + 3, '#3f7a37'); c.p(x + 3, y + 4, '#3f7a37')
    elif kind == 'robe':
        c.rect(x + 2, y + 1, 3, 4, '#45275e'); c.p(x + 1, y + 2, '#45275e'); c.p(x + 5, y + 2, '#45275e')
    elif kind == 'bread':
        c.rect(x + 1, y + 2, 5, 2, '#c98d4f'); c.p(x + 2, y + 2, '#e2ad6c'); c.p(x + 4, y + 2, '#e2ad6c')
    elif kind == 'book':
        c.rect(x + 2, y + 1, 3, 4, '#4e5b70'); c.rect(x + 3, y + 1, 1, 4, '#cfc6b2')


def pitched_roof(c, x, y, w, h, pal):
    c.poly([(x - 2, y), (x + w + 1, y), (x + w - 3, y - h), (x + 2, y - h)], pal[0])
    c.poly([(x - 1, y - 1), (x + w, y - 1), (x + w - 3, y - h + 1), (x + 2, y - h + 1)], pal[1])
    for xx in range(x, x + w, 3):
        c.rect(xx, y - h + 2, 1, h - 2, pal[0])


def library(c, x, base, rnd):
    w, h = 40, 26
    brick_wall(c, x, base - h, w, h)
    pitched_roof(c, x, base - h, w, 7, C['roof_slate'])
    c.outline(x, base - h, w, h, C['stone'][0])
    window(c, x + 4, base - 19, 9, 8, books=True, rnd=rnd)
    window(c, x + 27, base - 19, 9, 8, books=True, rnd=rnd)
    # door
    c.rect(x + 16, base - 12, 8, 12, C['wood'][1]); c.rect(x + 17, base - 11, 6, 11, C['wood'][2])
    c.p(x + 21, base - 6, '#ffd95a')
    c.rect(x + 14, base - 23, 12, 5, C['wood'][3]); c.outline(x + 14, base - 23, 12, 5, C['wood'][0])
    for i, col in enumerate(['#4e5b70', '#7a6a55', '#64408a', '#5b6a7a']):
        c.rect(x + 16 + i * 2, base - 22, 1, 3, col)
    # Hydrafill poster on the side wall: yellow and green bottle [ch1]
    c.rect(x + 1, base - 9, 5, 7, '#fbf1d6'); c.outline(x + 1, base - 9, 5, 7, C['wood'][1])
    c.rect(x + 3, base - 8, 1, 1, C['hydra_g']); c.rect(x + 2, base - 7, 3, 4, C['hydra_y'])
    c.rect(x + 2, base - 5, 3, 1, C['hydra_g'])


def tea_house(c, x, base, rnd):
    w, h = 46, 22
    # wood-and-stone style [ch1]: stone lower half, timber upper half
    brick_wall(c, x, base - 10, w, 10)
    c.rect(x, base - h, w, h - 10, C['wood'][3])
    for xx in range(x, x + w, 5):
        c.rect(xx, base - h, 1, h - 10, C['wood'][2])
    c.rect(x, base - h, w, 1, C['wood'][1]); c.rect(x, base - 11, w, 1, C['wood'][1])
    pitched_roof(c, x, base - h, w, 8, C['terracotta'])
    window(c, x + 6, base - 19, 6, 5, lit=True); window(c, x + 34, base - 19, 6, 5, lit=True)
    sign(c, x + 19, base - 20, 'tea')
    # striped awning
    for i in range(w + 4):
        col = C['awning'][(i // 3) % 2]
        c.rect(x - 2 + i, base - 11, 1, 3, col)
        if i % 3 == 1:
            c.p(x - 2 + i, base - 8, col)
    c.rect(x - 2, base - 12, w + 4, 1, C['wood'][1])
    c.rect(x + 4, base - 8, w - 8, 8, C['glass'][2])
    c.rect(x + 4, base - 8, w - 8, 1, '#e8c070')
    c.rect(x + 18, base - 8, 9, 8, C['wood'][2])
    # cups on counter
    for xx in range(x + 7, x + 16, 3):
        c.p(xx, base - 4, '#fbf1d6')
    for xx in range(x + 30, x + 40, 3):
        c.p(xx, base - 4, '#fbf1d6')


def small_house(c, x, base, w, h, wall, roof, signkind=None, rooftop_garden=False, lit=False, rnd=None):
    c.rect(x, base - h, w, h, wall[1])
    c.rect(x, base - h, 1, h, '#ffffff40' if False else wall[1])
    c.rect(x + w - 1, base - h, 1, h, wall[0])
    c.rect(x, base - 1, w, 1, wall[0])
    if rooftop_garden:  # "a garden on the roof" [ch1]
        c.rect(x - 1, base - h - 1, w + 2, 1, C['stone'][1])
        for xx in range(x, x + w):
            hh = (rnd.randint(1, 3) if rnd else 2)
            c.rect(xx, base - h - 1 - hh, 1, hh, rnd.choice(C['tree'][2:5]) if rnd else C['tree'][3])
        c.p(x + 3, base - h - 3, C['flower'][0]); c.p(x + w - 4, base - h - 3, C['flower'][1])
    else:
        pitched_roof(c, x, base - h, w, 6, roof)
    window(c, x + 3, base - h + 4, 4, 4, lit=lit)
    window(c, x + w - 7, base - h + 4, 4, 4, lit=lit)
    c.rect(x + w // 2 - 2, base - 8, 5, 8, C['wood'][1]); c.rect(x + w // 2 - 1, base - 7, 3, 7, C['wood'][2])
    if signkind:
        c.rect(x + w // 2 + 3, base - 11, 1, 2, C['iron'])
        sign(c, x + w // 2 + 2, base - 10, signkind)
    # flower boxes
    for wx in (x + 2, x + w - 8):
        c.rect(wx, base - h + 9, 6, 1, C['wood'][1])
        for i in range(6):
            c.p(wx + i, base - h + 8, rnd.choice(C['flower']) if rnd else C['flower'][0])


def lamp(c, x, base, h=14):
    c.rect(x, base - h, 1, h, C['iron'])
    c.rect(x - 1, base - 1, 3, 1, C['iron'])
    c.rect(x - 1, base - h - 3, 3, 3, C['lamp'])
    c.rect(x - 2, base - h - 4, 5, 1, C['iron'])
    c.p(x, base - h - 5, C['iron'])
    c.glow(x, base - h - 2, 6, C['lamp'], 90)


def green_circle_pole(c, x, base):
    # "a green circle on top of a one meter tall pole" [ch5]
    c.rect(x, base - 7, 1, 7, '#8a92a0')
    for dx, dy in [(-1, -9), (0, -10), (1, -9), (-2, -8), (2, -8), (-1, -7), (0, -7), (1, -7)]:
        pass
    pts = [(-1, -10), (0, -10), (1, -10), (-2, -9), (2, -9), (-2, -8), (2, -8), (-1, -7), (0, -7), (1, -7)]
    for dx, dy in pts:
        c.p(x + dx, base + dy, C['green_circle'])
    c.glow(x, base - 8, 4, C['green_circle'], 80)


def bench(c, x, base, w=12):
    c.rect(x, base - 5, w, 1, C['wood'][3]); c.rect(x, base - 4, w, 1, C['wood'][1])
    c.rect(x, base - 3, w, 1, C['wood'][3]); c.rect(x, base - 2, w, 1, C['wood'][1])
    c.rect(x + 1, base - 1, 1, 1, C['wood'][0]); c.rect(x + w - 2, base - 1, 1, 1, C['wood'][0])


def table(c, x, base):
    c.rect(x, base - 4, 7, 1, C['wood'][3]); c.rect(x, base - 3, 7, 1, C['wood'][1])
    c.rect(x + 3, base - 2, 1, 2, C['wood'][0])
    c.p(x + 1, base - 5, '#fbf1d6'); c.p(x + 5, base - 5, '#fbf1d6')
    # green circle on the tabletop [ch3, ch6]
    c.p(x + 3, base - 4, C['green_circle'])


def playground(c, x, base):
    # "much more basic ... not even comfortable" [ch6]: one plain slide and a sandbox
    c.rect(x, base - 10, 1, 10, '#8a92a0'); c.rect(x + 3, base - 10, 1, 10, '#8a92a0')
    for yy in range(base - 9, base, 3):
        c.rect(x, yy, 4, 1, '#8a92a0')
    c.rect(x, base - 11, 4, 1, '#6b7380')
    for i in range(10):
        c.rect(x + 4 + i, base - 10 + i, 2, 1, '#c7ccd6')
    c.rect(x + 16, base - 3, 12, 3, '#e8d49a'); c.outline(x + 16, base - 3, 12, 3, C['wood'][1])
    c.p(x + 20, base - 2, '#c8452e'); c.p(x + 24, base - 2, '#3f6fd8')


def flowerbed(c, x, base, w, rnd):
    c.rect(x, base - 3, w, 3, C['grass'][1])
    c.rect(x, base - 3, w, 1, C['grass'][2])
    for xx in range(x, x + w):
        if rnd.random() < 0.5:
            c.p(xx, base - 3 - rnd.randint(0, 1), rnd.choice(C['flower']))


def bird(c, x, y):
    c.p(x, y, '#3e3540'); c.p(x - 1, y - 1, '#3e3540'); c.p(x + 1, y - 1, '#3e3540')


def plaza(c, top, rnd):
    pv = C['pave']
    c.rect(0, top, c.w, c.h - top, pv[1])
    for yy in range(top, c.h, 3):
        c.rect(0, yy, c.w, 1, pv[0])
        off = 0 if ((yy - top) // 3) % 2 == 0 else 3
        for xx in range(off, c.w, 6):
            c.p(xx, yy + 1, pv[0]); c.p(xx, yy + 2, pv[0])
            if rnd.random() < 0.25:
                c.p(xx + 2, yy + 1, pv[2])
    c.rect(0, top, c.w, 1, pv[2])


def draw_scene(W, H, layout, seed=7):
    rnd = random.Random(seed)
    c = Canvas(W, H)
    base = layout['base']
    sky(c, base)
    for cx, cy, s in layout.get('clouds', []):
        cloud(c, cx, cy, s)
    m = layout['mountain']
    mountain(c, m[0], m[1], base - 6, m[2], rnd)
    for t in layout.get('towers', []):
        tx, th, tw = t[:3]; lift = t[3] if len(t) > 3 else layout.get('tower_lift', 0)
        # sit towers on the lower slope [ch1]
        castle_tower(c, tx, base - 6 - lift, th, tw)
    # tree clumps on the slope hide the tower bases ("poked up high above the trees") [ch1]
    for t in layout.get('towers', []):
        tx, th, tw = t[:3]; lift = t[3] if len(t) > 3 else layout.get('tower_lift', 0)
        by = base - 6 - lift
        for k in range(-1, tw + 2, 3):
            r = rnd.randint(2, 3 + tw // 4)
            c.disc(tx + k, by - rnd.randint(0, 2), r, C['mtn'][0])
            c.disc(tx + k - 1, by - rnd.randint(1, 3), max(1, r - 1), C['mtn'][2])
    # far treeline over the mountain foot (Meldan hides in trees)
    for x in range(-4, W + 4, 7):
        r = rnd.randint(5, 8)
        c.disc(x, base - 6, r, C['tree'][1])
        c.disc(x - 1, base - 7, max(2, r - 3), C['tree'][2])
    for bx, by in layout.get('birds', []):
        bird(c, bx, by)
    for kind, x, *args in layout['buildings']:
        if kind == 'library':
            library(c, x, base, rnd)
        elif kind == 'tea':
            tea_house(c, x, base, rnd)
        elif kind == 'house':
            w, h, wall, roof, sk, rg = args
            small_house(c, x, base, w, h, C[wall], C[roof], sk, rg, lit=False, rnd=rnd)
    plaza(c, base, rnd)
    for kind, x, y, *args in layout['props']:
        y = base + y
        if kind == 'tree':
            shadow(c, x, y, args[1] + 2)
            tree(c, x, y, args[0], args[1], rnd, maple=args[2] if len(args) > 2 else False)
        elif kind == 'lamp':
            lamp(c, x, y, args[0] if args else 14)
        elif kind == 'bench':
            bench(c, x, y)
        elif kind == 'table':
            table(c, x, y)
        elif kind == 'playground':
            playground(c, x, y)
        elif kind == 'circle':
            green_circle_pole(c, x, y)
        elif kind == 'grass':
            w = args[0]
            c.d.ellipse([x - w, y - 4, x + w, y + 4], fill=hex2rgba(C['grass'][1]))
            c.d.ellipse([x - w + 2, y - 4, x + w - 2, y + 2], fill=hex2rgba(C['grass'][2]))
            for _ in range(w):
                c.p(x + rnd.randint(-w + 2, w - 2), y + rnd.randint(-3, 2), C['grass'][0])
        elif kind == 'flowerbed':
            flowerbed(c, x, y, args[0], rnd)
        elif kind == 'person':
            k, skin, hair, shirt = args
            shadow(c, x + 4, y, 4)
            c.blit(mini(k, skin, hair, shirt), x, y - 13)
    return c.img


HEADER = dict(
    base=38,
    clouds=[(30, 3, 0.7), (150, 6, 0.6), (300, 2, 0.8), (375, 8, 0.5)],
    mountain=(150, 400, 2),
    towers=[(222, 15, 5), (247, 19, 6), (283, 17, 5), (330, 13, 5)],
    birds=[(110, 8), (116, 6), (122, 9)],
    buildings=[
        ('house', 6, 26, 20, 'grey', 'roof_slate', 'bread', False),
        ('tea', 44, ),
        ('library', 128, ),
        ('house', 196, 28, 19, 'beige', 'terracotta', 'flower', True),
        ('house', 230, 26, 21, 'blue', 'roof_slate', 'robe', False),
        ('house', 262, 28, 18, 'beige', 'terracotta', 'bread', False),
        ('house', 352, 28, 20, 'blue', 'terracotta', None, True),
    ],
    props=[
        ('tree', 34, 9, 18, 9), ('lamp', 96, 6, 14), ('circle', 100, 6),
        ('table', 50, 8), ('table', 76, 8),
        ('person', 58, 8, 'robe', 'warm', 'chestnut', ''), ('person', 84, 9, 'shirt', 'fair', 'ginger', '#5c9a3e'),
        ('tree', 116, 9, 20, 10), ('bench', 120, 9),
        ('person', 136, 9, 'hood', 'warm', 'black', ''),
        ('playground', 170, 9), ('person', 192, 9, 'shirt', 'tan', 'black', '#f2c84b'),
        ('tree', 300, 9, 18, 9, True), ('bench', 306, 9), ('person', 316, 9, 'robe', 'deep', 'black', ''),
        ('lamp', 336, 7, 14),
        ('person', 248, 9, 'robe', 'fair', 'silver', ''), ('person', 262, 9, 'shirt', 'deep', 'black', '#64408a'),
        ('tree', 392, 9, 20, 10), ('person', 400, 9, 'shirt', 'warm', 'blonde', '#3f6fd8'),
        ('flowerbed', 0, 10, 26), ('flowerbed', 150, 10, 16), ('flowerbed', 340, 10, 74),
    ],
)

LANDING = dict(
    base=150,
    clouds=[(20, 14, 1.2), (110, 30, 0.9), (230, 10, 1.3), (290, 44, 0.8)],
    mountain=(40, 330, 72),
    towers=[(126, 30, 8, 8), (168, 34, 9, 26), (210, 32, 9, 20), (258, 26, 8, 10)],
    tower_lift=10,
    birds=[(70, 40), (77, 37), (84, 41)],
    buildings=[
        ('house', 2, 30, 24, 'grey', 'roof_slate', 'bread', False),
        ('tea', 36, ),
        ('library', 132, ),
        ('house', 196, 28, 22, 'beige', 'terracotta', 'flower', True),
        ('house', 228, 28, 24, 'blue', 'roof_slate', 'robe', False),
        ('house', 262, 30, 21, 'beige', 'terracotta', 'bread', False),
        ('house', 296, 26, 23, 'blue', 'terracotta', None, True),
    ],
    props=[
        ('tree', 22, 14, 34, 16), ('lamp', 90, 8, 16), ('circle', 96, 9),
        ('table', 44, 10), ('table', 70, 10),
        ('person', 52, 10, 'robe', 'warm', 'chestnut', ''), ('person', 78, 11, 'shirt', 'fair', 'ginger', '#5c9a3e'),
        ('tree', 118, 16, 30, 14), ('bench', 112, 16), ('person', 126, 16, 'hood', 'warm', 'black', ''),
        ('playground', 160, 14), ('person', 182, 14, 'shirt', 'tan', 'black', '#f2c84b'),
        ('tree', 300, 18, 32, 15, True), ('bench', 268, 20), ('person', 276, 20, 'robe', 'deep', 'black', ''),
        ('lamp', 236, 14, 16), ('person', 214, 22, 'robe', 'fair', 'silver', ''),
        ('person', 226, 22, 'shirt', 'deep', 'black', '#64408a'),
        ('flowerbed', 0, 50, 70), ('flowerbed', 250, 50, 70), ('flowerbed', 100, 50, 120),
        ('grass', 20, 48, 22), ('grass', 306, 48, 22), ('grass', 22, 14, 14), ('grass', 300, 18, 14),
        ('tree', 8, 50, 26, 13), ('tree', 314, 50, 24, 12),
        ('person', 40, 38, 'robe', 'tan', 'plum', ''), ('person', 286, 40, 'hood', 'fair', 'black', ''),
    ],
)
