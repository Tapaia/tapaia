"""Pixel art for the $TAPAIA tokenomics card (original art).
bg-400x225.png is shown at 4x (1600x900) with nearest-neighbour scaling; icons are 16x16, shown at 4x."""
import math, random
import numpy as np
from PIL import Image

random.seed(7)
W, H = 400, 225
BAYER = np.array([[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]]) / 16.0


def rgb(h):
    h = h.lstrip('#'); return np.array([int(h[i:i + 2], 16) for i in (0, 2, 4)], float)


def lerp(a, b, t):
    return a + (b - a) * t


img = np.zeros((H, W, 3))
# --- sky: deep robe purple, a touch lighter in the middle band
top, mid, low = rgb('#1f1030'), rgb('#3a2052'), rgb('#2a1740')
for y in range(H):
    t = y / H
    c = lerp(top, mid, t / .45) if t < .45 else lerp(mid, low, (t - .45) / .55)
    img[y, :] = c

# --- coin-as-sun glow behind the logo (logo centre ~ (104,96) px -> (26,24) art px)
SX, SY = 28.0, 23.5
ramp = [(0.00, '#ffe9a8'), (0.16, '#ffd27a'), (0.34, '#f29b5e'), (0.56, '#b4507a'), (0.80, '#5e2c6e'), (1.0, None)]
for y in range(H):
    for x in range(W):
        d = math.hypot((x - SX) * .46, (y - SY) * 1.08) / 80.0
        if d >= 1: continue
        # dithered band pick
        dd = min(.999, max(0.0, d + (BAYER[y % 4, x % 4] - .5) * .07))
        for (a, ca), (b, cb) in zip(ramp, ramp[1:]):
            if a <= dd < b:
                k = (dd - a) / (b - a)
                c0 = rgb(ca)
                c1 = rgb(cb) if cb else img[y, x]
                # posterise mixing into 3 steps with dithering for a pixel look
                q = min(2, int(k * 3 + BAYER[(y + 1) % 4, (x + 2) % 4] * .9))
                col = lerp(c0, c1, q / 2.6)
                alpha = 1 - max(0, (d - .55) / .45) ** 1.4 if cb is None else 1
                img[y, x] = lerp(img[y, x], col, alpha * .95)
                break

# --- pixel stars on the dark side
for _ in range(70):
    x, y = random.randrange(150, W), random.randrange(2, 60)
    if math.hypot(x - SX, y - SY) < 110: continue
    c = rgb(random.choice(['#d9cfe6', '#a99bc2', '#ffe9a8']))
    img[y, x] = lerp(img[y, x], c, .85)
    if random.random() < .12:
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            img[y + dy, x + dx] = lerp(img[y + dy, x + dx], c, .45)

# --- mountain with castle-tower apartments + stone tower, top right (behind header) [ch1, ch6]
mt = rgb('#3a2a55'); mt_l = rgb('#6a4672'); rim = rgb('#d79a86')
def ridge(x):
    return 18 + 22 * (abs(x - 330) / 70) ** 1.25 + 1.5 * math.sin(x * .7)
for x in range(250, W):
    r = ridge(x)
    for y in range(int(r), 44):
        k = (y - r) / 26
        c = lerp(mt_l, mt, min(1, k * 1.2)) if x < 330 else mt
        # canopy texture
        if (x * 3 + y * 5) % 7 == 0 and BAYER[y % 4, x % 4] > .5:
            c = c * .8
        elif (x * 5 + y * 3) % 11 == 0:
            c = lerp(c, rgb('#4f5a6a'), .5)
        img[y, x] = c
    if x < 330:
        img[int(r), x] = rim
# staircase cut through the trees
for i in range(26):
    x, y = 300 + i, int(40 - i * .85)
    if y > ridge(x) + 1:
        img[y, x] = rgb('#c79a8a'); img[y, x + 1] = rgb('#7a4f6a')
def tower(x0, y0, w, h, lit=True):
    for y in range(y0, y0 + h):
        for x in range(x0, x0 + w):
            img[y, x] = rgb('#5a3d66') if x == x0 else rgb('#3e2a52')
    for x in range(x0, x0 + w, 2):  # crenellations
        img[y0 - 1, x] = rgb('#3e2a52')
    if lit:
        for y in range(y0 + 2, y0 + h - 1, 3):
            for x in range(x0 + 1, x0 + w - 1, 2):
                if random.random() < .7:
                    img[y, x] = rgb('#ffd95a') if random.random() < .7 else rgb('#e0a526')
tower(281, 22, 6, 20); tower(355, 24, 6, 18); tower(372, 30, 5, 13)
tower(327, 9, 6, 11, lit=False)  # stone tower at the top
img[13, 329] = rgb('#39e07a'); img[13, 330] = rgb('#a8ffbf')  # green glow [ch6]

# --- pixel clouds lit from the coin-sun
def cloud(cx, cy, w, h):
    for y in range(cy - h, cy + h):
        for x in range(cx - w, cx + w):
            if not (0 <= x < W and 0 <= y < H): continue
            v = ((x - cx) / w) ** 2 + ((y - cy) / h) ** 2 * 1.6 - .15 * math.sin(x * .45) - .1 * math.cos(x * .23 + y)
            if v < 1 - BAYER[y % 4, x % 4] * .25:
                up = (y - (cy - h)) / (2 * h)
                c = lerp(rgb('#ffcf8a'), rgb('#9a4f7e'), min(1, up * 1.3 + (x - cx + w) / (2 * w) * .3))
                img[y, x] = lerp(img[y, x], c, .78)
cloud(160, 14, 26, 4); cloud(205, 31, 18, 3); cloud(120, 36, 14, 3)

# --- town strip at the bottom: rooftops, lit windows, trees, a green circle on a pole
BASE = 214
walls = ['#4a3358', '#3f2c50', '#523a60', '#463052']
roofs = ['#2f1d40', '#5a2f3c', '#33264a']
x = -3
while x < W:
    w = random.choice([18, 22, 26, 30]); h = random.choice([14, 17, 20, 23])
    wall = rgb(random.choice(walls)); roof = rgb(random.choice(roofs))
    y0 = BASE - h
    for yy in range(y0, BASE):
        for xx in range(max(0, x), min(W, x + w)):
            img[yy, xx] = wall
    # pitched roof
    for i in range(w // 2 + 2):
        for xx in (x - 1 + i, x + w - i):
            for yy in range(y0 - i // 2 - 1, y0):
                if 0 <= xx < W and yy >= 0: img[yy, xx] = roof
    for xx in range(max(0, x - 1), min(W, x + w + 1)):
        img[y0, xx] = roof * .9
    # windows (warm, a few dark)
    for wy in range(y0 + 3, BASE - 4, 6):
        for wx in range(x + 3, x + w - 3, 6):
            if 0 <= wx < W - 2:
                c = rgb('#ffd95a') if random.random() < .65 else rgb('#2a1a3a')
                img[wy:wy + 3, wx:wx + 2] = c
                if c[0] > 200: img[wy + 3, wx:wx + 2] = rgb('#e0a526')
    x += w + random.choice([4, 7, 10])
# trees
for tx in (10, 96, 188, 262, 351, 392):
    for yy in range(BASE - 22, BASE):
        for xx in range(tx - 9, tx + 10):
            if 0 <= xx < W and ((xx - tx) / 9) ** 2 + ((yy - (BASE - 13)) / 9.5) ** 2 < 1 - BAYER[yy % 4, xx % 4] * .2:
                img[yy, xx] = rgb('#24452a') if (xx + yy) % 5 else rgb('#2f5a2e')
                if xx < tx - 3 and yy < BASE - 15: img[yy, xx] = rgb('#3f7a37')
# lamp posts with glow
for lx in (60, 228, 318):
    for yy in range(BASE - 16, BASE): img[yy, lx] = rgb('#1d1228')
    for yy in range(BASE - 22, BASE - 10):
        for xx in range(lx - 6, lx + 7):
            k = math.hypot(xx - lx, (yy - (BASE - 17)) * 1.2) / 7
            if k < 1 and BAYER[yy % 4, xx % 4] > k: img[yy, xx] = lerp(img[yy, xx], rgb('#ffe9a8'), .5 * (1 - k))
    img[BASE - 18:BASE - 15, lx - 1:lx + 2] = rgb('#ffe9a8')
# green circle on a pole ("Check in") [ch5]
gx = 140
for yy in range(BASE - 12, BASE): img[yy, gx] = rgb('#1d1228')
for yy in range(BASE - 18, BASE - 11):
    for xx in range(gx - 4, gx + 5):
        r = math.hypot(xx - gx, yy - (BASE - 15))
        if 2.2 < r < 3.8: img[yy, xx] = rgb('#39e07a')
        elif r <= 2.2: img[yy, xx] = rgb('#1d1228')
# plaza
for yy in range(BASE, H):
    for xx in range(W):
        c = rgb('#22132f')
        if (yy - BASE) % 4 == 0 or (xx + (yy // 4) * 3) % 9 == 0: c = rgb('#1a0e25')
        img[yy, xx] = c
img[BASE, :] = rgb('#3a2450')

Image.fromarray(np.clip(img, 0, 255).astype('uint8')).save('art/bg-400x225.png')

# ---------------- icons (16x16) ----------------
P = {'.': None, 'F': '#fbf1d6', 'f': '#e8cf98', 'G': '#ffd95a', 'g': '#e0a526', 'd': '#9a6a10', 'N': '#39e07a',
     'n': '#2fc56a', 'L': '#8a64b0', 'l': '#64408a', 'O': '#f2884b', 'R': '#d8452b', 'W': '#ffe9a8', 'w': '#9a6235',
     'b': '#6b3f1f', 'k': '#2e1a40'}
ICONS = {
 'lock': [
  "................",
  "......FFFF......",
  ".....FffffF.....",
  "....Ff....fF....",
  "....F......F....",
  "....F......F....",
  "....F......F....",
  "...GGGGGGGGGG...",
  "...GWWWWWWWWg...",
  "...GGGGkkGGGg...",
  "...GgggkkgggG...",
  "...GgggkkgggG...",
  "...GggggggggG...",
  "...gdddddddddg..",
  "....dddddddd....",
  "................"],
 'badge': [
  "................",
  ".......GG.......",
  "......GWWG......",
  "......GWWG......",
  "..GGGGGWWGGGGG..",
  "..GWWWWWWWWWWg..",
  "...gWWWWWWWWg...",
  "....gWWWWWWg....",
  "....GWWWWWWG....",
  "...GWWWggWWWG...",
  "...GWWg..gWWG...",
  "..GWgg....ggWg..",
  "..ggg......ggg..",
  "................",
  "................",
  "................"],
 'door': [
  "................",
  "....wwwwww......",
  "...wbbbbbbw.....",
  "..wbwwwwwwbw....",
  "..wbwwwwwwbw....",
  "..wbwwwwwwbw..N.",
  "..wbwwwwwwbw.NkN",
  "..wbwwwwGwbw..N.",
  "..wbwwwwGwbw....",
  "..wbwwwwwwbw....",
  "..wbwwwwwwbw....",
  "..wbwwwwwwbw....",
  "..wbwwwwwwbw....",
  ".ffffffffffff...",
  "ffffffffffffff..",
  "................"],
 'speak': [
  "................",
  "...FFFFFFFFFF...",
  "..FFFFFFFFFFFF..",
  "..FFFFFFFFFFFF..",
  "..FFkkFkkFkkFF..",
  "..FFkkFkkFkkFF..",
  "..FFFFFFFFFFFF..",
  "..FFFFFFFFFFFF..",
  "...FFFFFFFFFF...",
  "....FF.....O....",
  "...FF.....OGO...",
  "..........OGO...",
  ".........OGWGO..",
  ".........OGWGO..",
  "..........OOO...",
  "................"],
 'shop': [
  "................",
  "..NNFFNNFFNNFF..",
  ".NNFFNNFFNNFFNN.",
  ".NNFFNNFFNNFFNN.",
  "..nn..nn..nn....",
  "..LLLLLLLLLLLL..",
  "..LGGGLLwwwwLL..",
  "..LGWGLLwbbwLL..",
  "..LGGGLLwbbwLL..",
  "..LLLLLLwbGwLL..",
  "..LGGGLLwbbwLL..",
  "..LGWGLLwbbwLL..",
  "..LGGGLLwbbwLL..",
  "..llllllllllll..",
  ".ffffffffffffff.",
  "................"],
 'flame': [
  "................",
  ".......O........",
  "......OO........",
  "......ROO.......",
  ".....ROOO..O....",
  ".....ROGOO.OO...",
  "....ROOGGOOOO...",
  "....ROGGGGOOO...",
  "...ROOGWWGGOOO..",
  "...ROGWWWWGOOO..",
  "...ROGWWWWGGOR..",
  "...RROGWWGGOOR..",
  "....RROGGGOORR..",
  ".....RROOOORR...",
  "......RRRRR.....",
  "................"],
 'chest': [
  "................",
  "................",
  "....wwwwwwww....",
  "...wbbbbbbbbw...",
  "..wbwwwwwwwwbw..",
  "..wGGGGGGGGGGw..",
  "..GGGGGWWGGGGG..",
  "..wbwwwGGwwwbw..",
  "..wbwwwkkwwwbw..",
  "..wbwwwwwwwwbw..",
  "..wGGGGGGGGGGw..",
  "..wbwwwwwwwwbw..",
  "..wbbbbbbbbbbw..",
  "...wwwwwwwwww...",
  "................",
  "................"],
}
for name, rows in ICONS.items():
    im = Image.new('RGBA', (16, 16), (0, 0, 0, 0))
    for y, row in enumerate(rows):
        row = row.ljust(16, '.')[:16]
        for x, ch in enumerate(row):
            c = P[ch]
            if c: im.putpixel((x, y), tuple(int(c[i:i + 2], 16) for i in (1, 3, 5)) + (255,))
    im.save(f'art/icon-{name}.png')
print('ok')
