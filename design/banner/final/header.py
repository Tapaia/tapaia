"""FINAL @TapaiaSquare X header: Golden Hour in the official style A (cozy HD pixel).
Builds on ../styles/hd.py (style A) with the finalisation fixes:
  * cumulus pixel clouds (backlit by the sun = coin) instead of thin stratus streaks, still framing the lockup
  * people ~1.45x larger (42 px tall at 750x250) with clearer silhouettes, so they read at X display size
  * calmer mountain forest so the castle-tower apartments [ch1:30], staircase and stone tower [ch6:325-327] read
Output: art/scene-750x250.png (shown at 2x / 4x with nearest-neighbour scaling by header.html)."""
import os, sys, math, random
import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'styles'))
import hd                                                    # noqa: E402
from kit import W, H, SUN, BASE, BAYER, Layer, rgb, shade, mix  # noqa: E402

# ------------------------------------------------------------------ cumulus clouds
CLOUD_RAMP = ['#4a2a62', '#5e3372', '#783e84', '#97508c', '#b8628e', '#d7798b', '#f09486', '#ffb489', '#ffd39c', '#fff0c6']

# (x0, x1, base_y, height): tall puffy banks arcing over the coin + wordmark, a bank under the tagline,
# and two smaller clouds on the left for balance
CUMULUS = [
    (404, 760, 38, 24),     # crown over the lockup
    (600, 760, 22, 12),     # high wisp top right
    (436, 772, 163, 20),    # bank under the tagline, resting on the far hills
    (262, 384, 62, 14),     # mid-left, between the stone tower and the coin
    (-14, 128, 40, 15),     # far left, above the castle towers
    (96, 178, 18, 8),
]


def puffs_for(x0, x1, base, hgt, rnd):
    ps = []
    n = max(3, int((x1 - x0) / 15))
    for k in range(n):
        u = (k + .5) / n
        env = math.sin(math.pi * min(1, max(0, u))) ** .7
        r = (hgt * .45 + hgt * .55 * env) * rnd.uniform(.75, 1.05)
        cx = x0 + (x1 - x0) * u + rnd.uniform(-4, 4)
        ps.append((cx, base - r * .55, r))
        if env > .45 and rnd.random() < .6:                     # second tier of billows
            r2 = r * rnd.uniform(.5, .7)
            ps.append((cx + rnd.uniform(-8, 8), base - r * .55 - r * .7, r2))
    ps.append(((x0 + x1) / 2, base - hgt * .12, (x1 - x0) * .5))  # flat-bottomed body (squashed below)
    return ps


def cloud_layer(rnd=None):
    """Soft cumulus: each cloud is a smooth density field (soft union of billows, flat base); lighting comes
    from the field's gradient, so billows shade as one soft mass, backlit near the sun and pink-lit away from it."""
    from PIL import ImageFilter
    rnd = rnd or random.Random(4)
    ys, xs = np.mgrid[0:H, 0:W].astype(np.float32)
    out = np.zeros((H, W, 4), np.float32)
    ramp = np.array([rgb(c) for c in CLOUD_RAMP], np.float32)
    n = len(ramp)
    sxv, syv = SUN[0] - xs, (SUN[1] - ys) * 1.3
    dist = np.hypot(sxv, syv) + 1e-3
    warm = np.clip(1 - dist / 330, 0, 1)
    for (x0, x1, base, hgt) in CUMULUS:
        ps = puffs_for(x0, x1, base, hgt, rnd)[:-1]
        F = np.zeros((H, W), np.float32)
        for (cx, cy, r) in ps:
            F += np.exp(-(((xs - cx) / r) ** 2 + ((ys - cy) / (r * .8)) ** 2) * 1.6)
        bx = np.exp(-(((xs - (x0 + x1) / 2) / ((x1 - x0) * .5)) ** 6))      # flat body along the base
        F += .9 * bx * np.exp(-(((ys - (base - hgt * .15)) / (hgt * .28)) ** 2))
        bl = base + 1.2 * np.sin(xs * .045 + x0) + .8 * np.sin(xs * .13 + hgt)   # gently uneven flat base
        F *= (ys <= bl)
        Fs = np.array(Image.fromarray(F).filter(ImageFilter.GaussianBlur(1.5)), np.float32) if False else F
        gy, gx = np.gradient(F)
        inside = F > .5
        z = np.sqrt(np.clip(F - .5, 0, None))
        nx, ny, nz = -gx * 3, -gy * 3, np.ones_like(F) * .9
        nl = np.sqrt(nx ** 2 + ny ** 2 + nz ** 2)
        lx, ly = sxv / dist, syv / dist
        lz = .6 * (1 - warm) - .3 * warm
        ll = np.sqrt(lx ** 2 + ly ** 2 + lz ** 2)
        lam = (nx * lx + ny * ly + nz * lz) / (nl * ll)
        up = np.clip(-ny / nl, 0, 1)                                    # skylight on the billow tops
        v = .20 + .46 * lam + .28 * warm + .16 * up + .06 * np.clip(z, 0, 1)
        if SUN[1] > base:                                              # gold underside when the sun is below
            v += np.clip(1 - (bl - ys) / 3, 0, 1) * (.18 + .3 * warm)
        v = np.clip(v, 0, 1)
        th = BAYER[ys.astype(int) % 4, xs.astype(int) % 4]
        edge_ok = (F > .5 + .14 * th)                                  # dithered soft edge
        m = inside & edge_ok
        idx = np.clip(np.round(v * (n - 1) + (th - .5) * .9), 0, n - 1).astype(int)
        out[m, :3] = ramp[idx][m]
        out[m, 3] = 255
    L = Layer()
    L.im = Image.fromarray(out.astype(np.uint8))
    from PIL import ImageDraw
    L.d = ImageDraw.Draw(L.im); L.px = L.im.load()
    return L


# ------------------------------------------------------------------ calmer mountain forest
CALM = ['#26333a', '#2f4639', '#3a5a3f', '#4a6c44', '#5f8049', '#7a9150']


def calm_crown(L, cx, cy, r, rnd):
    L.disc(cx + 1, cy + 1, r, CALM[0])
    L.disc(cx, cy, r, CALM[1])
    L.disc(cx + r * .22, cy - r * .22, r * .74, CALM[2])
    L.disc(cx + r * .4, cy - r * .4, max(1, r * .38), CALM[3])
    for _ in range(int(r * r * .12)):                          # sparse, low-contrast leaf flecks
        a = rnd.random() * 6.283; rr = rnd.random() * r * .8
        L.p(cx + math.cos(a) * rr, cy + math.sin(a) * rr, CALM[3] if math.cos(a) - math.sin(a) > 0 else CALM[1])


def mountain_layer(emit, rnd=None):
    rnd = rnd or random.Random(11)
    L = Layer()
    prof = [hd.mountain_profile(x) for x in range(W)]
    for x in range(0, 430):
        L.rect(x, int(prof[x]), 1, BASE - int(prof[x]) + 2, CALM[1])
    pts = []
    for row, y in enumerate(range(42, BASE, 6)):
        for x in range(-10, 432, 8):
            xx = x + (4 if row % 2 else 0) + rnd.randint(-1, 1); yy = y + rnd.randint(-1, 1)
            if 0 <= xx < W and yy >= prof[min(W - 1, max(0, xx))] - 1:
                pts.append((xx, yy))
    pts.sort(key=lambda p: p[1])
    for (x, y) in pts:
        calm_crown(L, x, y, rnd.choice([5, 6, 6, 7]), rnd)
    # ridge highlight on the sun side
    for x in range(196, 430):
        L.p(x, prof[x], mix(CALM[4], '#e8c070', .5))
    # staircase cut through the forest: shaded clearing either side, then lit stone steps [ch6:325]
    (x0, y0), (x1, y1) = hd.STAIR
    n = int(max(abs(x1 - x0), abs(y1 - y0)))
    for i in range(n + 1):
        x = x0 + (x1 - x0) * i / n; y = y0 + (y1 - y0) * i / n
        L.p(x - 3, y, CALM[0]); L.p(x - 2, y, '#4a3a4a')
        step = (i // 2) % 2
        L.p(x - 1, y, hd.STONE[2]); L.p(x, y, hd.STONE[5] if step else hd.STONE[4]); L.p(x + 1, y, hd.STONE[5] if step else hd.STONE[4])
        L.p(x + 2, y, hd.STONE[3]); L.p(x + 3, y, CALM[0])
    # castle-tower apartments [ch1:30], with a dark contact outline so they separate from the trees
    for (x, top, w) in hd.TOWERS:
        for yy in range(top + 6, 178):
            L.p(x - 1, yy, '#2a2234'); L.p(x + w, yy, mix('#2a2234', '#c2a68e', .3))
        hd.castle_tower(L, x, top, w, rnd, emit)
        for k in range(-3, w + 5, 6):
            calm_crown(L, x + k, top + 50 + rnd.randint(-2, 2), rnd.choice([5, 6]), rnd)
            calm_crown(L, x + k + 3, top + 58 + rnd.randint(-2, 2), 6, rnd)
    # open-topped stone tower at the top [ch6:327]
    tx, ty, tw, th = hd.ORDER_TOWER
    for yy in range(ty - 3, ty + th):
        L.p(tx - 1, yy, '#2a2234')
    for i in range(tw):
        u = i / (tw - 1)
        L.rect(tx + i, ty, 1, th, shade(hd.STONE[3], -.5 + 1.05 * u ** 1.2))
    for yy in range(ty + 3, ty + th, 4):
        off = 0 if (yy // 4) % 2 else 3
        for xx in range(tx + off, tx + tw, 6):
            L.p(xx, yy, shade(hd.STONE[1], -.2))
        L.rect(tx, yy + 2, tw, 1, shade(hd.STONE[2], -.25))
    L.rect(tx + tw - 1, ty, 1, th, '#f6d6a6')                   # sun-side rim
    for i in range(0, tw, 4):
        L.rect(tx + i, ty - 3, 3, 3, shade(hd.STONE[3], -.3 + .8 * i / tw))
    L.rect(tx + 9, ty + 12, 3, 6, '#2c1f36'); L.rect(tx + 14, ty + 8, 2, 4, '#2c1f36')
    emit.ell(tx + 4, ty - 6, tx + tw - 4, ty - 1, '#5af09a', 180)   # larger, brighter green circle glows up from inside
    for (x, y) in [(tx - 4, ty + th - 2), (tx + tw + 3, ty + th - 1), (tx + 4, ty + th + 2), (tx + tw - 3, ty + th + 3)]:
        calm_crown(L, x, y, 5, rnd)
    return L


# ------------------------------------------------------------------ larger people (~1.45x, 42 px)
def person(kind='shirt', skin='warm', hair='chestnut', shirt='#c8452e', pants='#3d3550', long_hair=False):
    Wd, Ht = 22, 44
    sk, hr = hd.SKINS[skin], hd.HAIRS[hair]
    R = hd.ROBE
    g = [[None] * Wd for _ in range(Ht)]

    def put(x, y, c):
        if 0 <= x < Wd and 0 <= y < Ht:
            g[y][x] = c

    def ellipse(cx, cy, rx, ry, c, ymin=-99, ymax=99):
        for y in range(Ht):
            for x in range(Wd):
                if ((x + .5 - cx) / rx) ** 2 + ((y + .5 - cy) / ry) ** 2 <= 1 and ymin <= y <= ymax:
                    put(x, y, c)

    robe = kind in ('robe', 'hood')
    # body
    if robe:
        for y in range(14, 41):
            half = 6 + (y - 14) * 3.2 / 26
            for x in range(int(11 - half), int(11 + half + .5)):
                put(x, y, 'R')
        for x in range(6, 10): put(x, 41, 'U'); put(x, 42, 'U')
        for x in range(12, 16): put(x, 41, 'U'); put(x, 42, 'U')
        for y in range(18, 37):                                  # fold line
            put(11 + (y % 7 == 0), y, 'r')
        for y in range(16, 30):                                  # sleeves
            put(4, y, 'R'); put(17, y, 'R')
        put(4, 30, 'S'); put(17, 30, 'S')
    else:
        for y in range(14, 28):
            half = 7 if y < 17 else 6
            for x in range(11 - half, 11 + half):
                put(x, y, 'T')
        for y in range(15, 27):                                  # arms
            put(3, y, 'T' if y < 22 else 'S'); put(18, y, 'T' if y < 22 else 'S')
            put(4, y, 't'); put(17, y, 't')
        for y in range(28, 40):                                  # legs
            for x in range(6, 10): put(x, y, 'P')
            for x in range(12, 16): put(x, y, 'P')
        for x in range(5, 10): put(x, 40, 'B'); put(x, 41, 'B')
        for x in range(12, 17): put(x, 40, 'B'); put(x, 41, 'B')
        for x in range(5, 17): put(x, 27, 'b')                   # belt
    # head
    if kind == 'hood':                                           # hood up + face cover with strap [ch1:132, ch1:140]
        ellipse(11, 8, 7.2, 8, 'R', ymax=15)
        ellipse(11, 9.2, 4.4, 4.6, 'F')
        put(9, 8, 'E'); put(13, 8, 'E')
        for x in range(7, 15): put(x, 10, 'N')
    else:
        if long_hair:                                            # long hair falls at the sides, not over the chin
            ellipse(11, 9, 7, 9.5, 'H', ymax=17)
            for y in range(11, 18):
                for x in range(8, 15):
                    g[y][x] = None
        put(10, 13, 'S'); put(11, 13, 'S'); put(12, 13, 'S')     # neck
        ellipse(11, 8, 5.4, 6, 'S')
        ellipse(11, 5, 6.2, 4.6, 'H', ymax=5)                    # hair cap + fringe
        put(6, 6, 'H'); put(16, 6, 'H'); put(6, 7, 'H'); put(16, 7, 'H'); put(15, 6, 'H')
        put(9, 8, 'E'); put(13, 8, 'E')
        put(8, 10, 'K'); put(14, 10, 'K')
        if kind == 'robe':                                       # hood down, bunched at the neck
            for x in range(6, 17): put(x, 14, 'r')
            for x in range(7, 16): put(x, 15, 'R')
    pal = {'H': hr, 'S': sk, 'E': '#2a1a30', 'K': shade(sk, -.12), 'T': shirt, 't': shade(shirt, -.28), 'P': pants,
           'B': '#3a2a2e', 'b': shade(pants, -.35), 'R': R[2], 'r': R[1], 'U': R[0],
           'F': '#2a1840', 'N': R[3]}
    im = Image.new('RGBA', (Wd + 2, Ht + 2), (0, 0, 0, 0)); px = im.load()
    for y in range(Ht):
        xs = [x for x in range(Wd) if g[y][x]]
        if not xs:
            continue
        lo, hi = min(xs), max(xs)
        for x in xs:
            ch = g[y][x]
            c = pal[ch]
            if ch not in 'ENK':
                if x <= lo + 1:
                    c = shade(c, -.3)                            # violet shadow side
                elif x >= hi - 1:
                    c = shade(c, .32)                            # gold sun side
                if ch == 'H' and y < 3:
                    c = shade(c, .18)
            px[x + 1, y + 1] = rgb(c) + (255,)
    # selective outline (no pure black): dark hue-shifted on the shadow side, warm rim on the sun side
    src = im.copy(); sp = src.load()
    for y in range(Ht + 2):
        for x in range(Wd + 2):
            if sp[x, y][3]:
                continue
            nb = [(sp[x + dx, y + dy], dx) for dx, dy in ((-1, 0), (1, 0), (0, 1), (0, -1))
                  if 0 <= x + dx < Wd + 2 and 0 <= y + dy < Ht + 2 and sp[x + dx, y + dy][3]]
            if nb:
                c, dx = nb[0]
                px[x, y] = (shade(c[:3], .45) if dx == -1 else shade(c[:3], -.7)) + (255,)
    return im


# people positions shifted so the larger figures don't collide with props
hd.PEOPLE = [
    (200, 216, 'shirt', 'warm', 'chestnut', '#c4513a', '#3d3550', False),
    (244, 218, 'robe', 'fair', 'ginger', None, None, True),
    (314, 214, 'shirt', 'tan', 'black', '#7f93ad', '#4a3a34', False),
    (358, 240, 'shirt', 'fair', 'blonde', '#e8b84a', '#4a5a78', True),
    (552, 228, 'shirt', 'deep', 'black', '#4f8a4a', '#3d3550', False),
    (584, 232, 'hood', 'warm', 'black', None, None, False),
    (654, 236, 'shirt', 'fair', 'silver', '#5a78b8', '#3d3550', False),
    (466, 242, 'shirt', 'warm', 'chestnut', '#d07a9a', '#3d3550', True),
]
hd.cloud_layer = cloud_layer
hd.mountain_layer = mountain_layer
hd.person = person


def render():
    layers, emit, heads = hd.build()
    return hd.compose(layers, emit, heads)


if __name__ == '__main__':
    img = render()
    img.save(f'{HERE}/art/scene-750x250.png')
    if len(sys.argv) > 1:
        img.resize((1500, 500), Image.NEAREST).save(f'/tmp/logo/tapaia_final_{sys.argv[1]}.png')
    print('final scene ok')
