"""Tapaia character kit: 'Cozy HD pixel' citizens (original art, GPL v3).

Every citizen is described by a small config (skin, hair style + colour, eyes, expression, outfit,
colours, accessories) and rasterised natively at any size from shapes defined in *sprite space*
(a 32x48 grid, head centre (16, 12.5), head radius 8.5). The same config renders:
  - the 32x48 full-body sprite (1 art px = 1 sprite unit)
  - the 32/40/64 px chat busts (head + shoulders, re-rasterised at k = 1.2 / 1.5 / 2.4)
so the portrait always matches the walking sprite, without upscaling blur.

Pipeline per render:  shapes -> (material, tone) grid -> orphan cleanup -> cast-shadow contours
                      -> hand-placed face templates -> soft coloured outline (no pure black).
Shading: top-left key light, 4 tones per material + 1 specular, hue-shifted (shadows toward plum /
rose, lights toward warm cream), same idea as design/banner/styles/kit.py `shade()`.
"""
import math
import numpy as np
from PIL import Image

# ------------------------------------------------------------------ colour helpers
def rgb(c):
    if isinstance(c, tuple):
        return c[:3]
    c = c.lstrip('#')
    return tuple(int(c[i:i + 2], 16) for i in (0, 2, 4))


def mix(a, b, k):
    a, b = rgb(a), rgb(b)
    return tuple(int(round(a[i] + (b[i] - a[i]) * k)) for i in range(3))


SHADOW = (52, 26, 78)        # hue-shifted shadow target (plum-violet), never black
LIGHT = (255, 243, 212)      # warm cream key light
OUTL = (38, 20, 50)          # outline target (deep plum)


def make_ramp(base, sh=(.58, .30), li=(.24, .48), shadow=SHADOW, light=LIGHT, ol=.70):
    b = rgb(base)
    return [mix(b, shadow, sh[0]), mix(b, shadow, sh[1]), b, mix(b, light, li[0]), mix(b, light, li[1]), mix(b, OUTL, ol)]


def light_of(c):
    return sum(rgb(c)) / 765.0


def skin_ramp(base):
    # skin shadows go rosy-plum, not grey; outline is a warm deep brown-plum
    b = rgb(base)
    r = make_ramp(b, sh=(.42, .2), li=(.26, .5), shadow=(128, 52, 86), light=(255, 240, 222), ol=.66)
    r[5] = mix(b, (70, 28, 44), .72)
    return r


# ------------------------------------------------------------------ palettes (book palette + design choices)
SKINS = {   # 7 tones, light -> deep
    'porcelain': '#f7dfca', 'fair': '#f0c8a4', 'warm': '#e2a87c', 'olive': '#c99968',
    'tan': '#b47a4f', 'brown': '#8d5839', 'deep': '#663c2a',
}
HAIRS = {   # first 6 are the current app keys (shared/avatar.ts), last 2 new
    'black': '#2f2738', 'chestnut': '#7c4a2b', 'ginger': '#c25a2c', 'blonde': '#e2b456',
    'plum': '#6c3a74', 'silver': '#bcb8cb', 'espresso': '#4a2c25', 'auburn': '#94372b',
}
EYES = {'brown': '#6b3d24', 'hazel': '#7a6a2a', 'green': '#3d7d47', 'blue': '#3f6fae', 'grey': '#6b7590', 'amber': '#a8641e'}
CLOTH = {   # garment colours drawn from design/visual-reference.md (leaf, robe, wood, parchment, walls, maple, hydrafill)
    'leaf': '#4f8a3e', 'moss': '#2f5a2e', 'sage': '#93b98a', 'robe': '#45275e', 'lilac': '#8a64b0',
    'wood': '#9a6235', 'tan': '#c98d4f', 'parchment': '#f4e4bc', 'cream': '#fbf1d6', 'stone': '#8f877b',
    'wallblue': '#8ea3b5', 'skyblue': '#a9c8db', 'beige': '#e6d3a8', 'maple': '#c8452e', 'rust': '#b4542e',
    'hydra': '#f2c84b', 'navy': '#3b4466', 'plum': '#5b3a86', 'charcoal': '#4a4250', 'white': '#f3efe6',
    'teal': '#3f7f7a', 'rose': '#d98a9a', 'mustard': '#d9a441', 'denim': '#55688f', 'brown': '#6b3f1f',
}
ROBE_BASE = '#45275e'   # "loose-fitting dark purple dress ... shoes of the same dark purple colour" [ch1]
BAND_BASE = '#d9cfe6'   # silken neck band [ch1]

LX, LY, LZ = -.52, -.58, .63   # key light from top-left, towards the viewer


def quant(L, t=(-.12, .32, .80)):
    """light value -> tone 0..3"""
    return np.where(L < t[0], 0, np.where(L < t[1], 1, np.where(L < t[2], 2, 3)))


# ------------------------------------------------------------------ canvas
class Canvas:
    def __init__(self, w, h, k=1.0, ox=0.0, oy=0.0):
        self.w, self.h, self.k, self.ox, self.oy = w, h, k, ox, oy
        xs = ox + (np.arange(w) + .5) / k
        ys = oy + (np.arange(h) + .5) / k
        self.X, self.Y = np.meshgrid(xs, ys)
        self.mat = np.zeros((h, w), int)
        self.tone = np.zeros((h, w), int)
        self.grp = np.zeros((h, w), int)
        self.z = np.zeros((h, w), int)
        self.mats = [None]
        self.ramps = {}
        self.over = {}
        self._z = 0

    # sprite space <-> canvas
    def cx(self, sx):
        return (sx - self.ox) * self.k

    def cy(self, sy):
        return (sy - self.oy) * self.k

    def mid(self, name, ramp):
        if name not in self.ramps:
            self.ramps[name] = ramp
            self.mats.append(name)
        return self.mats.index(name)

    def paint(self, mask, name, ramp, tone, grp):
        if not np.any(mask):
            return
        self._z += 1
        m = self.mid(name, ramp)
        self.mat[mask] = m
        t = tone if np.isscalar(tone) else tone[mask]
        self.tone[mask] = t
        self.grp[mask] = grp
        self.z[mask] = self._z

    def put(self, x, y, c):
        x, y = int(x), int(y)
        if 0 <= x < self.w and 0 <= y < self.h:
            self.over[(x, y)] = rgb(c)

    def matname(self, x, y):
        if 0 <= x < self.w and 0 <= y < self.h:
            return self.mats[self.mat[y, x]]
        return None

    # passes
    def cleanup(self):
        """Remove orphan tone pixels (a tone with no same-tone 4-neighbour inside the same material)."""
        t, m = self.tone.copy(), self.mat
        h, w = t.shape
        for y in range(h):
            for x in range(w):
                if not m[y, x]:
                    continue
                nb = [(t[y + dy, x + dx]) for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))
                      if 0 <= x + dx < w and 0 <= y + dy < h and m[y + dy, x + dx] == m[y, x]]
                if len(nb) >= 3 and t[y, x] not in nb:
                    vals, cnt = np.unique(nb, return_counts=True)
                    self.tone[y, x] = vals[np.argmax(cnt)]

    def contours(self, strength=2, width=None):
        """Cast-shadow contour: a pixel touching (from above/left/right) a different object painted in
        front of it drops `strength` tones (1 px at sprite scale, ~2 px on the 64 px portrait).
        Separates hair from forehead, arms from torso, chin from neck."""
        g, z, m = self.grp, self.z, self.mat
        h, w = g.shape
        width = width or max(1, int(round(self.k * .8)))
        out = self.tone.copy()
        for y in range(h):
            for x in range(w):
                if not m[y, x]:
                    continue
                hit = 0
                for d in range(1, width + 1):
                    for dx, dy in ((0, -d), (-d, 0), (d, 0)):
                        xx, yy = x + dx, y + dy
                        if 0 <= xx < w and 0 <= yy < h and m[yy, xx] and g[yy, xx] != g[y, x] and z[yy, xx] > z[y, x]:
                            hit = d
                            break
                    if hit:
                        break
                if hit:
                    out[y, x] = max(0, self.tone[y, x] - (strength if hit == 1 else strength - 1))
        self.tone = out

    def image(self, outline=True):
        h, w = self.mat.shape
        im = Image.new('RGBA', (w, h), (0, 0, 0, 0))
        px = im.load()
        for y in range(h):
            for x in range(w):
                if self.mat[y, x]:
                    r = self.ramps[self.mats[self.mat[y, x]]]
                    px[x, y] = r[self.tone[y, x]] + (255,)
        for (x, y), c in self.over.items():
            if self.mat[y, x]:
                px[x, y] = c + (255,)
        if outline:
            src = im.copy(); sp = src.load()
            for y in range(h):
                for x in range(w):
                    if sp[x, y][3]:
                        continue
                    best = None
                    for dx, dy, lit in ((0, 1, True), (1, 0, True), (-1, 0, False), (0, -1, False)):
                        xx, yy = x + dx, y + dy
                        if 0 <= xx < w and 0 <= yy < h and sp[xx, yy][3]:
                            r = self.ramps[self.mats[self.mat[yy, xx]]]
                            # sel-out: the lit (top/left) rim uses the material's deep tone, the shadow side its outline
                            c = mix(r[0], r[5], .45) if lit else r[5]
                            if best is None or not lit:
                                best = c
                    if best:
                        px[x, y] = best + (255,)
        return im


# ------------------------------------------------------------------ shapes (sprite space)
def ell(C, cx, cy, rx, ry):
    nx, ny = (C.X - cx) / rx, (C.Y - cy) / ry
    d = nx * nx + ny * ny
    nz = np.sqrt(np.clip(1 - d, 0, 1))
    return d <= 1, nx * LX + ny * LY + nz * LZ


def poly(C, pts):
    X, Y = C.X, C.Y
    inside = np.zeros_like(X, bool)
    n = len(pts); j = n - 1
    for i in range(n):
        xi, yi = pts[i]; xj, yj = pts[j]
        cond = ((yi > Y) != (yj > Y)) & (X < (xj - xi) * (Y - yi) / (yj - yi + 1e-12) + xi)
        inside ^= cond
        j = i
    return inside


def capsule(C, x0, y0, x1, y1, r0, r1=None):
    r1 = r0 if r1 is None else r1
    X, Y = C.X, C.Y
    dx, dy = x1 - x0, y1 - y0
    L2 = dx * dx + dy * dy
    t = np.clip(((X - x0) * dx + (Y - y0) * dy) / L2, 0, 1)
    px, py = x0 + t * dx, y0 + t * dy
    r = r0 + (r1 - r0) * t
    ddx, ddy = X - px, Y - py
    d = np.sqrt(ddx * ddx + ddy * ddy)
    nx = ddx / np.maximum(r, 1e-6)
    ny = ddy / np.maximum(r, 1e-6) * .35
    nz = np.sqrt(np.clip(1 - nx * nx, 0, 1))
    return d <= r, nx * LX + ny * LY + nz * LZ - .05 * t


def cyl_light(C, cx, half, top, bot, bias=0.0):
    nx = np.clip((C.X - cx) / half, -1, 1)
    nz = np.sqrt(np.clip(1 - nx * nx, 0, 1))
    v = np.clip((C.Y - top) / max(1e-6, bot - top), 0, 1)
    return nx * LX + nz * LZ + (.18 - .3 * v) + bias


# ------------------------------------------------------------------ the citizen renderer
HC = (16.0, 12.5)
HR = 8.5
G_BACKHAIR, G_LEG, G_SHOE, G_LOW, G_TORSO, G_NECK, G_ARM_FAR, G_ARM, G_OVER, G_STRAP, G_SCARF, G_HEAD, G_BEARD, G_HAIR, G_HOOD, G_ITEM, G_BAND, G_COWL = range(1, 19)


class Citizen:
    def __init__(self, cfg):
        self.c = dict(DEFAULT)
        self.c.update(cfg)

    # ---------------------------------------------------------------- ramps
    def ramps(self):
        c = self.c
        R = {}
        R['skin'] = skin_ramp(SKINS[c['skin']])
        h = rgb(HAIRS[c['hair']])
        R['hair'] = make_ramp(h, sh=(.5, .25), li=(.30, .58), light=(255, 214, 150), ol=.62)
        if c['hair'] == 'black':   # black hair: cool lilac sheen instead of washed grey
            R['hair'] = [rgb('#1f1a28'), rgb('#2f2738'), rgb('#433a52'), rgb('#62587a'), rgb('#8f86ad'), rgb('#18121f')]
        if c['hair'] == 'silver':
            R['hair'] = [rgb('#7a7592'), rgb('#9a96ae'), rgb('#bcb8cb'), rgb('#dcd8e6'), rgb('#f6f3fb'), rgb('#4e4862')]
        for k in ('top', 'bottom', 'over', 'accent'):
            if c.get(k):
                R[k] = make_ramp(CLOTH.get(c[k], c[k]))
        R['robe'] = [rgb('#24143a'), rgb('#331d4f'), rgb('#45275e'), rgb('#5e3a7e'), rgb('#7c58a0'), rgb('#1a0f28')]
        R['band'] = [rgb('#a99bc2'), rgb('#bfb3d6'), rgb('#d9cfe6'), rgb('#efe9f7'), rgb('#ffffff'), rgb('#5e4f78')]
        R['shoe'] = make_ramp('#5a3a2c', ol=.6)
        R['leather'] = make_ramp('#7a4a2c')
        R['cup'] = [rgb('#c9b9a4'), rgb('#e2d6c2'), rgb('#f6efe2'), rgb('#fffaf0'), rgb('#ffffff'), rgb('#7d6656')]
        R['tea'] = make_ramp('#7e9a3e')
        R['book'] = make_ramp(CLOTH.get(c.get('book_col', 'moss')))
        R['pages'] = [rgb('#c9b28a'), rgb('#e2cfa6'), rgb('#f4e4bc'), rgb('#fbf1d6'), rgb('#fffaf0'), rgb('#6e5a40')]
        R['hoodsh'] = [rgb('#140b20'), rgb('#1d1029'), rgb('#271539'), rgb('#33204a'), rgb('#3f2a58'), rgb('#0f0818')]
        R['gold'] = make_ramp('#e0a526')
        return R

    # ---------------------------------------------------------------- render
    def render(self, C, detail='S'):
        c, R = self.c, self.ramps()
        turn = c.get('turn', 0.0)          # 0 front, +1 = facing viewer's right (3/4)
        robe = c['outfit'] in ('robe', 'hood')
        hood = c['outfit'] == 'hood'
        self.C, self.R, self.turn, self.detail = C, R, turn, detail
        self.bc = 16 + turn * 1.9          # centre line for front details (collars, buttons, aprons)
        hx = HC[0] + turn * .6
        # 1. back hair
        if not hood:
            self.hair(C, R, back=True)
        # 2. legs + shoes, lower garment
        if robe:
            self.robe_body(C, R, hood)
        else:
            self.legs(C, R)
            self.torso(C, R)
        # 3. neck
        if not hood:
            d = turn * 1.0
            m = poly(C, [(14.1 + d, 17.5), (17.9 + d, 17.5), (17.9 + d, 23.2), (14.1 + d, 23.2)])
            C.paint(m, 'skin', R['skin'], np.where(C.X < 15.2 + turn, 1, 1), G_NECK)
            if robe:
                self.cowl(C, R)
            if c.get('neckband'):
                m = poly(C, [(14.0, 19.7), (18.0, 19.7), (18.0, 21.5), (14.0, 21.5)])
                L = cyl_light(C, 16, 2.4, 19.7, 21.5)
                C.paint(m, 'band', R['band'], quant(L, (-.3, .3, .9)), G_BAND)
        # 4. overlays (scarf over the neck)
        if not robe:
            self.overlays(C, R)
        # 5. head
        if hood:
            self.hood(C, R)
        else:
            self.head(C, R)
            if c.get('beard'):
                self.beard(C, R)
            self.hair(C, R, back=False)
            if abs(turn) > .2:
                self.ear_turned(C, R)
        # 6. held items
        self.items(C, R)
        C.cleanup()
        C.contours()
        # 7. face templates (after shading so they stay crisp)
        if hood:
            self.hood_face(C)
        else:
            self.face(C)
        if c.get('glasses'):
            self.glasses(C)
        return C.image()

    # ---------------------------------------------------------------- body parts
    def legs(self, C, R):
        c = self.c
        skirt = c.get('bottom_kind') == 'skirt'
        for side in (-1, 1):
            x = 16 + side * (2.6 - abs(self.turn) * .5) + self.turn * .7
            m, L = capsule(C, x, 33.5, x + side * .15, 43.0, 2.25, 2.0)
            if skirt:   # legs show below the skirt (stockings = bottom colour darkened, else skin)
                C.paint(m & (C.Y > 38), 'legs', make_ramp(CLOTH[c.get('stockings', 'charcoal')]), quant(L), G_LEG)
            else:
                C.paint(m, 'bottom', R['bottom'], quant(L), G_LEG)
            # shoes
            sm, sL = ell(C, x + side * .5 + self.turn * 1.0, 44.9, 2.7, 1.55)
            sm &= C.Y > 43.4
            C.paint(sm, 'shoe', R['shoe'], np.where(quant(sL) > 2, 2, quant(sL)), G_SHOE)
        if skirt:
            m = poly(C, [(11.2, 31.0), (20.8, 31.0), (22.6, 39.6), (9.4, 39.6)])
            L = cyl_light(C, 16, 6.8, 31, 39.6)
            t = quant(L)
            # pleats
            pl = (np.abs(((C.X - 16) * 1.1 + (C.Y - 31) * .0) % 3.0 - 1.5) < .35) & (C.Y > 33)
            t = np.where(pl, np.maximum(0, t - 1), t)
            t = np.where(C.Y > 38.8, np.minimum(t, 1), t)
            C.paint(m, 'bottom', R['bottom'], t, G_LOW)
        else:
            m = poly(C, [(11.0, 31.0), (21.0, 31.0), (21.0, 35.5), (11.0, 35.5)])
            C.paint(m, 'bottom', R['bottom'], quant(cyl_light(C, 16, 6, 31, 36)), G_LOW)

    def torso_shape(self, C, top=22.0, bot=32.6, flare=0.0):
        t = self.turn
        sw = 6.7 - abs(t) * 1.1
        o = t * .7
        return poly(C, [(16 - sw + o, top + .6), (16 - sw + 1.2 + o, top), (16 + sw - 1.2 + o, top), (16 + sw + o, top + .6),
                        (16 + sw - .9 + flare + o, bot), (16 - sw + .9 - flare + o, bot)])

    def torso(self, C, R):
        c = self.c
        kind = c['outfit']
        long_sleeve = kind in ('tunic', 'cardigan', 'coat') or c.get('long_sleeve')
        bot = {'tunic': 37.6, 'coat': 39.2}.get(kind, 32.6)
        flare = {'tunic': 1.6, 'coat': 1.4}.get(kind, 0)
        top_ramp = 'top'
        # arms first only for the far arm in 3/4
        m = self.torso_shape(C, bot=bot, flare=flare)
        if abs(self.turn) > .2:
            self.arms(C, R, long_sleeve, only='far')
        L = cyl_light(C, 16 + self.turn * 1.2, 7.0, 22, bot)
        t = quant(L)
        if kind == 'tunic':   # V-neck + belt + hem band
            b = self.bc
            v = poly(C, [(b - 1.4, 21.6), (b + 1.4, 21.6), (b, 25.4)])
            t = np.where((C.Y > bot - 1.1), np.minimum(t, 1), t)
            C.paint(m, 'top', R['top'], t, G_TORSO)
            C.paint(v & m, 'skin', R['skin'], 2, G_TORSO)
            bm = m & (C.Y > 30.6) & (C.Y < 32.2)
            C.paint(bm, 'leather', R['leather'], quant(cyl_light(C, 16, 7, 30, 32)), G_STRAP)
            bk = (np.abs(C.X - self.bc) < 1.0) & (C.Y > 30.6) & (C.Y < 32.2)
            C.paint(bk, 'gold', R['gold'], 3, G_STRAP + 20)
        elif kind == 'coat':
            C.paint(m, 'top', R['top'], np.where(np.abs(C.X - self.bc) < .5, np.maximum(0, t - 1), t), G_TORSO)
            b = self.bc
            for side in (-1, 1):   # lapels
                lap = poly(C, [(b, 21.8), (b + side * 3.6, 22.0), (b + side * 2.0, 27.5), (b + side * .2, 26.0)])
                C.paint(lap, 'top', R['top'], 3 if side < 0 else 1, G_OVER)
        else:
            C.paint(m, 'top', R['top'], t, G_TORSO)
            if kind in ('tee', 'bandtee'):   # crew collar
                col, _ = ell(C, self.bc - self.turn * .6, 21.6, 2.6, 1.4)
                C.paint(col & (C.Y > 21.6), 'top', R['top'], 0, G_TORSO)
        if kind == 'bandtee':   # band-shirt slogan graphic [ch1: "slogans of their favorite bands"]
            g, gL = ell(C, self.bc, 26.6, 2.6 - abs(self.turn) * .5, 2.1)
            C.paint(g, 'accent', R['accent'], np.where(gL > .62, 3, 2), G_OVER)
            star = (np.abs(C.X - self.bc) < .6) & (np.abs(C.Y - 26.6) < 1.3) | (np.abs(C.Y - 26.6) < .6) & (np.abs(C.X - self.bc) < 1.3)
            C.paint(star & g, 'cream', make_ramp(CLOTH['cream']), 2, G_OVER + 30)
        self.arms(C, R, long_sleeve, only='near' if abs(self.turn) > .2 else None)

    def arms(self, C, R, long_sleeve, sleeve_ramp='top', robe=False, only=None):
        c = self.c
        t = self.turn
        pose = c.get('pose', 'down')
        for side in (-1, 1):
            far = (t > .2 and side > 0) or (t < -.2 and side < 0)
            if (only == 'far' and not far) or (only == 'near' and far):
                continue
            sx = 16 + side * (7.2 - abs(t) * (2.0 if far else .3)) + t * .7
            if pose == 'hold' and side == (c.get('hold_side', 1)):
                hx, hy = 16 + side * 3.6 + t * 1.6, 29.6
                x1, y1 = hx, hy
                mid = (sx + side * .6, 27.0)
            else:
                hx, hy = sx + side * .5, 32.4
                mid = None
            grp = G_ARM_FAR if far else G_ARM
            if mid:
                m1, L1 = capsule(C, sx, 23.6, mid[0], mid[1], 1.75)
                m2, L2 = capsule(C, mid[0], mid[1], x1, y1, 1.6)
                m, L = m1 | m2, np.where(m1, L1, L2)
            else:
                m, L = capsule(C, sx, 23.6, hx, hy - .6, 1.75, 1.6)
            if long_sleeve:
                C.paint(m, sleeve_ramp, R[sleeve_ramp], quant(L), grp)
                cuff = m & (np.hypot(C.X - hx, C.Y - hy) < 2.6) & (np.hypot(C.X - hx, C.Y - hy) > 1.3)
                C.paint(cuff, sleeve_ramp, R[sleeve_ramp], np.maximum(0, quant(L) - 1), grp)
            else:
                C.paint(m, 'skin', R['skin'], quant(L), grp)
                sl = m & (C.Y < 26.8 if not mid else (C.Y < 26.0))
                C.paint(sl, sleeve_ramp, R[sleeve_ramp], quant(L), grp)
                if c.get('rolled'):
                    rb = m & (C.Y >= 26.0) & (C.Y < 27.3)
                    C.paint(rb, sleeve_ramp, R[sleeve_ramp], 3, grp)
            hm, hL = ell(C, hx, hy + .3, 1.45, 1.35)
            C.paint(hm, 'skin', R['skin'], np.minimum(quant(hL), 2), grp)

    def overlays(self, C, R):
        c = self.c
        kind = c['outfit']
        if kind == 'cardigan':   # open cardigan over the inner shirt (inner = 'accent')
            b = self.bc
            inner = poly(C, [(b - 1.7, 21.8), (b + 1.7, 21.8), (b + 1.7, 32.6), (b - 1.7, 32.6)])
            C.paint(inner, 'accent', R['accent'], quant(cyl_light(C, 16, 4, 22, 33)), G_OVER)
            for y in (25.0, 28.0, 31.0):   # buttons on the placket edge
                bt, _ = ell(C, b - 2.1, y, .6, .55)
                C.paint(bt, 'cream', make_ramp(CLOTH['cream']), 2, G_OVER + 31)
            hem = self.torso_shape(C) & (C.Y > 31.4) & ~inner
            C.paint(hem, 'top', R['top'], 1, G_OVER + 1)
            for side in (-1, 1):
                pk = poly(C, [(b + side * 3.0, 28.4), (b + side * 4.6, 28.4), (b + side * 4.6, 30.6), (b + side * 3.0, 30.6)])
                C.paint(pk, 'top', R['top'], 1, G_OVER + 2)
        if kind == 'apron':      # bib apron with neck strap, waist ties and pocket (tea house)
            d = self.bc - 16
            bib = poly(C, [(13.0 + d, 24.2), (19.0 + d, 24.2), (19.6 + d, 30.6), (21.6 + d * .4, 31.0), (22.4 + d * .4, 40.2), (9.6 + d * .8, 40.2), (10.4 + d * .8, 31.0), (12.4 + d, 30.6)])
            L = cyl_light(C, 16, 6.5, 24, 40)
            t = quant(L)
            t = np.where(C.Y > 39.2, np.minimum(t, 1), t)
            C.paint(bib, 'over', R['over'], t, G_OVER)
            pk = poly(C, [(14.0 + d, 33.2), (18.0 + d, 33.2), (18.0 + d, 36.0), (14.0 + d, 36.0)])
            C.paint(pk, 'over', R['over'], np.where(C.Y < 33.8, 0, 1), G_OVER + 1)
            for side in (-1, 1):
                st = capsule(C, 16 + d + side * 2.6, 24.4, 16 + d * .6 + side * 2.0, 21.4, .45)[0]
                C.paint(st & (C.Y < 24.6), 'over', R['over'], 1, G_OVER + 2)
            tie = (C.Y > 30.6) & (C.Y < 31.6) & self.torso_shape(C, bot=33)
            C.paint(tie & ~bib, 'over', R['over'], 1, G_OVER + 3)
        if c.get('satchel'):     # strap from the near shoulder to the opposite hip
            s = c.get('satchel_side', 1)
            st = capsule(C, 16 - s * 5.2, 22.6, 16 + s * 4.8, 31.2, .55)[0]
            C.paint(st, 'leather', R['leather'], 1, G_STRAP)
            bag = poly(C, [(16 + s * 3.0, 30.2), (16 + s * 8.6, 30.2), (16 + s * 8.4, 36.4), (16 + s * 3.2, 36.4)])
            L = cyl_light(C, 16 + s * 5.8, 3.2, 30, 36.4)
            C.paint(bag, 'leather', R['leather'], quant(L), G_ITEM - 1)
            flap = bag & (C.Y < 32.8)
            C.paint(flap, 'leather', R['leather'], np.minimum(quant(L) + 1, 3), G_ITEM - 1)
            bk = (np.abs(C.X - (16 + s * 5.8)) < .8) & (np.abs(C.Y - 32.9) < .7)
            C.paint(bk, 'gold', R['gold'], 3, G_ITEM)
        if c.get('scarf'):       # knit scarf wrapped at the neck with one tail down the front
            sr = make_ramp(CLOTH.get(c['scarf'], c['scarf']))
            d = (self.bc - 16) * .5
            wrap = capsule(C, 11.6 + d, 21.8, 20.4 + d, 21.8, 1.9)[0]
            L = cyl_light(C, 16, 5, 20, 24)
            t = quant(L)
            t = np.where((np.round(C.Y * 1.0) % 2 == 0) & (t > 1), t - 1, t) if self.detail != 'S' else t
            C.paint(wrap, 'scarf', sr, t, G_SCARF)
            d = self.bc - 16
            tail = poly(C, [(13.0 + d, 22.4), (16.0 + d, 22.4), (15.6 + d, 31.2), (12.6 + d, 31.2)])
            stripes = (np.floor(C.Y) % 3 == 0)
            C.paint(tail, 'scarf', sr, np.where(stripes, 1, np.where(C.X < 14, 3, 2)), G_SCARF + 1)
            fr = poly(C, [(12.6 + d, 31.2), (15.6 + d, 31.2), (15.6 + d, 32.4), (12.6 + d, 32.4)]) & (np.floor(C.X * (1 if self.detail == 'S' else 2)) % 2 == 0)
            C.paint(fr, 'scarf', sr, 1, G_SCARF + 1)

    def robe_body(self, C, R, hood):
        """Veridian Privacy Robe: loose dark purple dress, hood to ankles; same dark purple shoes with a high
        heel and deliberately uneven soles [ch1]."""
        t = self.turn
        for side, heel in ((-1, 0.0), (1, .8)):   # uneven: the right shoe stands on a taller heel
            x = 16 + side * 2.6
            sm, sL = ell(C, x + side * .4, 44.9 - heel * .5, 2.5, 1.5)
            sm &= C.Y > 43.0
            C.paint(sm, 'robe', R['robe'], np.minimum(quant(sL), 2), G_SHOE)
            hl = (np.abs(C.X - (x - side * 1.2)) < .7) & (C.Y > 44.5 - heel * .5) & (C.Y < 46.6)
            C.paint(hl, 'robe', R['robe'], 0, G_SHOE)
        body = poly(C, [(16 - 6.0 + t * .4, 22.4), (16 - 4.8 + t * .4, 21.6), (16 + 4.8 + t * .4, 21.6), (16 + 6.0 + t * .4, 22.4),
                        (16 + 8.2 + t * .3, 43.8), (16 - 8.2 + t * .3, 43.8)])
        L = cyl_light(C, 16 + t * .4, 8.0, 22, 44)
        tn = quant(L)
        folds = ((np.abs(C.X - (13.3 + t * .4)) < .45) | (np.abs(C.X - (18.9 + t * .4)) < .45)) & (C.Y > 31) & (C.Y < 43.4)
        tn = np.where(folds, np.maximum(0, tn - 1), tn)
        tn = np.where(C.Y > 42.8, np.minimum(tn, 1), tn)
        C.paint(body, 'robe', R['robe'], tn, G_TORSO)
        hemhi = body & (C.Y > 42.8) & (C.Y < 43.8) & (np.floor(C.X) % 4 == 1)
        C.paint(hemhi, 'robe', R['robe'], 2, G_TORSO)
        # wide bell sleeves, hands peeking out
        for side in (-1, 1):
            far = (t > .2 and side > 0) or (t < -.2 and side < 0)
            sx = 16 + side * (6.0 - (1.6 if far else .2) * abs(t)) + t * .6
            m, sl = capsule(C, sx, 23.4, sx + side * 1.7, 31.4, 1.9, 2.7)
            st = quant(sl)
            C.paint(m, 'robe', R['robe'], st, G_ARM)
            op, _ = ell(C, sx + side * 1.8, 32.3, 2.3, .95)
            C.paint(op & m, 'robe', R['robe'], 0, G_ARM)
            hm, hL = ell(C, sx + side * 1.7, 33.4, 1.35, 1.15)
            C.paint(hm & (C.Y > 32.6), 'skin', R['skin'], np.minimum(quant(hL), 2), G_ARM + 20)

    def cowl(self, C, R):
        """Hood down, bunched around the shoulders behind the neck."""
        m, L = ell(C, 16, 22.4, 7.4, 2.6)
        t = quant(L, (-.2, .25, .7))
        ridges = (np.abs(C.X - 12.5) < .45) | (np.abs(C.X - 19.5) < .45)
        C.paint(m & (C.Y > 20.6), 'robe', R['robe'], np.where(ridges, np.maximum(0, t - 1), t), G_COWL)

    # ---------------------------------------------------------------- head, face, hair
    def uv(self, C, shift=0.0):
        return (C.X - HC[0] - shift) / HR, (C.Y - HC[1]) / HR

    def face_mask(self, C):
        U, V = self.uv(C)
        w = np.where(V <= .3, .95 * np.sqrt(np.clip(1 - V * V, 0, 1)),
                     .906 + (.40 - .906) * np.clip((V - .3) / .7, 0, 1) ** 1.25)
        return (np.abs(U) <= w) & (V >= -1) & (V <= 1.0)

    def head(self, C, R):
        t = self.turn
        U, V = self.uv(C)
        fm = self.face_mask(C)
        nx = U / .95
        ny = V
        nz = np.sqrt(np.clip(1 - nx * nx * .9 - ny * ny * .5, 0, 1))
        L = nx * LX + ny * LY * .6 + nz * LZ + .1
        tn = quant(L, (-.2, .29, .86))
        tn = np.where((V > .55) & (np.abs(U) > .25), np.minimum(tn, 1), tn)
        # ears (near ear only when turned)
        for side in (-1, 1):
            if abs(t) > .2:
                continue
            em, eL = ell(C, 16 + side * 8.25, 14.3, 1.25, 1.75)
            C.paint(em & ~fm, 'skin', R['skin'], 1 if side > 0 else 2, G_HEAD - 1)
        C.paint(fm, 'skin', R['skin'], tn, G_HEAD)

    def ear_turned(self, C, R):
        t = self.turn
        s = -1 if t > 0 else 1
        ex = 16 + s * HR * (.95 - .5 * abs(t))
        em, eL = ell(C, ex, 14.4, 1.2, 1.7)
        C.paint(em, 'skin', R['skin'], np.where(C.X < ex, 2, 1), G_HEAD + 50)
        inner = ell(C, ex + .2, 14.6, .45, .8)[0]
        C.paint(inner & em, 'skin', R['skin'], 0, G_HEAD + 50)

    def fx(self, du):   # face x position in sprite space; a 3/4 turn compresses and shifts the features
        t = self.turn
        return HC[0] + (du * (1 - .3 * abs(t)) + t * .3) * HR

    def face(self, C):
        c, R = self.c, self.R
        det = self.detail
        sk = R['skin']
        eyec = rgb(EYES[c['eyes']])
        K = mix(R['hair'][5], OUTL, .35) if det != 'L' else mix(R['hair'][5], OUTL, .2)
        D = mix(eyec, OUTL, .55)
        I = eyec
        Ih = mix(eyec, (255, 255, 255), .35)
        W = (255, 251, 240)
        S = mix(sk[2], (255, 255, 255), .55)   # sclera (warm white)
        M = mix(rgb('#b04a5e'), sk[2], .15)
        Md = mix(rgb('#7a2a44'), OUTL, .2)
        T = rgb('#fffaf2')
        Tg = rgb('#e2788a')
        B = mix(sk[2], rgb('#ff7f8e'), .45)
        expr = c['expr']
        tpl = TEMPLATES[det]
        eye_dy = {'S': 13.9, 'M': 13.9, 'L': 13.7}[det]
        ex = tpl['eye_dx']
        # eyes
        ek = {'laugh': 'closed', 'content': 'closed', 'wink': 'open', 'surprised': 'wide'}.get(expr, 'open')
        for side in (-1, 1):
            key = ek
            if expr == 'wink' and side > 0:
                key = 'closed'
            if expr == 'shy':
                key = 'side'
            rows = tpl['eye'][key]
            far = (self.turn > .3 and side < 0) or (self.turn < -.3 and side > 0)
            if far and len(rows[0]) > 2:
                rows = [r[1:] for r in rows]
            self.stamp(C, rows, self.fx(side * ex), eye_dy, side, {'K': K, 'D': D, 'I': I, 'i': Ih, 'W': W, 'S': S}, mirror=side > 0)
        # brows
        bk = {'surprised': 'up', 'thoughtful': 'raise', 'shy': 'soft', 'content': 'soft', 'laugh': 'up'}.get(expr, 'base')
        for side in (-1, 1):
            rows = tpl['brow'][bk if not (bk == 'raise' and side < 0) else 'base']
            self.stamp(C, rows, self.fx(side * ex), eye_dy - tpl['brow_dy'], side, {'H': mix(R['hair'][1], OUTL, .25), 'h': R['hair'][2]}, mirror=side > 0)
        # nose
        if tpl.get('nose'):
            self.stamp(C, tpl['nose'], self.fx(.02 + self.turn * .05), eye_dy + tpl['nose_dy'], 1, {'n': sk[1], 'N': sk[0], 'h': sk[3]})
        # blush
        if c.get('blush', True):
            for side in (-1, 1):
                self.stamp(C, tpl['blush'], self.fx(side * (ex + tpl['blush_dx'])), eye_dy + tpl['blush_dy'], side, {'b': B, 'f': mix(sk[1], (150, 70, 60), .3)}, mirror=side > 0)
        if c.get('freckles'):
            for side in (-1, 1):
                self.stamp(C, tpl['freckles'], self.fx(side * (ex + .02)), eye_dy + tpl['blush_dy'] - .6, side, {'f': mix(sk[1], (120, 60, 40), .35)}, mirror=side > 0)
        # mouth
        mk = {'smile': 'smile', 'grin': 'grin', 'laugh': 'laugh', 'content': 'smile', 'surprised': 'o', 'thoughtful': 'flat',
              'shy': 'small', 'wink': 'smirk', 'calm': 'small'}[expr]
        if not c.get('beard') or det != 'S' or True:
            mp = {'M': M, 'm': Md, 'T': T, 't': Tg, 'l': sk[1], 'L': sk[3]}
            if c.get('beard'):
                mp = {'M': mix(R['hair'][0], Md, .5), 'm': mix(R['hair'][0], OUTL, .4), 'T': T, 't': Tg}
            self.stamp(C, tpl['mouth'][mk], self.fx(0), eye_dy + tpl['mouth_dy'], 1, mp)

    def stamp(self, C, rows, sx, sy, side, pal, mirror=False):
        """Place a pixel template centred on sprite point (sx, sy); right-side features mirror the template.
        Mirrored templates are snapped symmetric to the left one around the face axis."""
        h, w = len(rows), len(rows[0])
        if mirror:
            rows = [r[::-1] for r in rows]
        x0 = int(round(C.cx(sx) - w / 2))
        y0 = int(round(C.cy(sy) - h / 2))
        for j, r in enumerate(rows):
            for i, ch in enumerate(r):
                if ch in pal:
                    C.put(x0 + i, y0 + j, pal[ch])

    def beard(self, C, R):
        U, V = self.uv(C)
        fm = self.face_mask(C)
        m = fm & (V > .42) & ~((V < .78) & (np.abs(U) < .30)) & (np.abs(U) < .9)
        mu = fm & (V > .44) & (V < .58) & (np.abs(U) < .42)
        nx = U; L = nx * LX + .45
        C.paint(m | mu, 'hair', R['hair'], quant(L + .1 * np.sin(C.X * 3.1)), G_BEARD)

    def hood_face(self, C):
        det = self.detail
        tpl = TEMPLATES[det]
        g1, g2 = rgb('#d8c8ff'), rgb('#ffffff')
        for side in (-1, 1):
            self.stamp(C, tpl['glint'], self.fx(side * tpl['eye_dx'] * .92), 13.6, side, {'g': g1, 'G': g2, 'd': rgb('#5c4482')}, mirror=side > 0)

    def hood(self, C, R):
        """Hood up with the front face cover; a strap across below the eyes tightens it [ch1:132, ch1:140]."""
        t = self.turn
        U, V = self.uv(C, shift=t * .6)
        m1, L1 = ell(C, 16 - t * .3, 11.9, 9.6 - abs(t) * .3, 9.8)
        peak = poly(C, [(14.0 + t * .6, 2.9), (16.2 + t * .6, 1.2), (18.0 + t * .6, 2.9)])
        drape = poly(C, [(8.9, 15.0), (23.1, 15.0), (22.7, 23.4), (9.3, 23.4)])
        hm = m1 | peak | drape
        tn = quant(L1 + .05)
        tn = np.where(drape & ~m1, np.clip(quant(cyl_light(C, 16, 7.5, 15, 24)) - 1, 0, 3), tn)
        tn = np.where(peak & ~m1, 2, tn)
        C.paint(hm, 'robe', R['robe'], tn, G_HOOD - 1)
        # face opening: deep shadow above the strap, cover below
        om, oL = ell(C, 16 + t * 2.6, 14.0, 6.3, 7.0)
        C.paint(om, 'hoodsh', R['hoodsh'], np.where(C.Y < 11.6, 1, 2), G_HOOD)
        # inner rim of the hood: lit on the left
        rim = ell(C, 16 + t * 2.6, 14.0, 7.2, 7.9)[0] & ~om & m1
        C.paint(rim, 'robe', R['robe'], np.where(C.X < 16 + t * 2.6, 3, 1), G_HOOD - 1)
        strap_y0, strap_y1 = 15.5, 16.9
        cover = om & (C.Y >= strap_y1)
        cl = cyl_light(C, 16 + t * 2.6, 6.3, 16, 21)
        ct = quant(cl)
        pleat = (np.abs(C.X - (16 + t * 2.6)) < .45) & (C.Y > 17.5)
        C.paint(cover, 'robe', R['robe'], np.where(pleat, np.maximum(0, ct - 1), np.minimum(ct, 3)), G_HOOD + 1)
        strap = om & (C.Y >= strap_y0) & (C.Y < strap_y1)
        C.paint(strap, 'band', R['band'], np.where(C.X < 15 + t * 2.6, 3, 1), G_HOOD + 2)
        buckle = strap & (np.abs(C.X - (21.0 + t * 2.6)) < .8)
        C.paint(buckle, 'gold', R['gold'], 2, G_HOOD + 3)

    def hair(self, C, R, back):
        c = self.c
        st = c['hairstyle']
        t = self.turn
        U, V = self.uv(C, shift=t * .5)
        part = c.get('part', 0.0) + t * .25
        hr = R['hair']
        # base ellipsoid light for the hair mass
        def hlight(cx=0.0, cy=-.12, rx=1.12, ry=1.06):
            nx, ny = (U - cx) / rx, (V - cy) / ry
            nz = np.sqrt(np.clip(1 - nx * nx - ny * ny, 0, 1))
            return nx * LX + ny * LY + nz * LZ, np.sqrt(nx * nx + ny * ny)

        big = self.detail == 'L'

        def strands(tn, ang_k=11.0, w=.18, cx=None, cy=-1.15):
            cx = part if cx is None else cx
            th = np.arctan2(V - cy, U - cx)
            k_ = ang_k * (1.55 if big else 1.0)
            ph = (th * k_ / math.pi + .07 * np.sin(V * 9)) % 1.0
            line = ph < w
            tn = np.where(line & (tn >= 2), tn - 1, tn)
            if big:   # lighter strand ridges between the clump lines
                tn = np.where((ph > .5) & (ph < .62) & (tn == 2), 3, tn)
            return tn

        def shine(tn, rho, lo=.5, hi=.7):
            band = (rho > lo) & (rho < hi) & (U < .25 - (V + .4) * .2) & (V < -.15) & (V > -1.0)
            brk = ((np.arctan2(V + 1.15, U - part) * 13 / math.pi) % 1.0) < .62
            return np.where(band & brk, np.where(U < -.25, 4, 3), tn)

        if back:
            if st in ('long', 'wavy', 'bob', 'braid'):
                Lb = {'long': 2.25, 'wavy': 1.75, 'bob': .95, 'braid': .9}[st]
                wb = {'long': 1.18, 'wavy': 1.26, 'bob': 1.16, 'braid': 1.1}[st]
                yy = np.clip((V + .2) / (Lb + .2), 0, 1)
                width = wb * (1 - .12 * yy ** 3)
                edge = Lb + (.07 * np.sin(U * 17) if st != 'wavy' else .12 * np.sin(U * 9))
                m = (np.abs(U) < width) & (V > -.4) & (V < edge)
                L = -np.abs(U) / width * .5 + .25 - .25 * yy
                tn = quant(L, (-.2, .12, .5))
                if st == 'wavy':
                    tn = np.where((np.sin(V * 9 + np.abs(U) * 4) > .55) & (tn > 0), tn - 1, tn)
                tn = strands(tn, 14, .2, cx=0, cy=-1.5)
                C.paint(m, 'hair', hr, np.minimum(tn, 2), G_BACKHAIR)
            if st == 'ponytail':   # tail swings out behind the head on one side
                s = c.get('tail_side', 1)
                m, L = capsule(C, 16 + s * 6.0, 6.0, 16 + s * 9.4, 17.5, 2.5, 1.0)
                m2, _ = capsule(C, 16 + s * 9.4, 17.5, 16 + s * 8.4, 21.5, 1.0, .5)
                tn = quant(L, (-.25, .15, .6))
                C.paint(m | m2, 'hair', hr, np.minimum(tn, 3), G_BACKHAIR)
            return

        L, rho = hlight()
        if st == 'curly':   # a cloud of individual curls, each lit like a little sphere
            rnd = np.random.RandomState(4)
            curls = []
            for ring, n, rr in ((.94, 14, .27), (.72, 10, .27), (.46, 7, .26), (.18, 3, .26)):
                for i in range(n):
                    a = -math.pi * 1.1 + (i + .5) / n * math.pi * 1.2 * (1 if ring > .3 else 1)
                    a = math.pi + (i / (n - 1) if n > 1 else .5) * math.pi * (1.0 + .25 * (ring > .9)) - .125 * math.pi * (ring > .9)
                    cu_, cv_ = math.cos(a) * ring * 1.06, -.2 + math.sin(a) * ring * .98
                    if ring > .9 or cv_ < -.28:
                        curls.append((cu_, cv_, rr + rnd.uniform(-.03, .03)))
            # fringe curls along the hairline
            for i in range(6):
                u_ = -.66 + i * .264
                curls.append((u_, -.47 - .04 * (i % 2), .2))
            curls.sort(key=lambda p: (p[1] < -.3, -abs(p[0])))
            for j, (cu_, cv_, rr) in enumerate(curls):
                cxs, cys = HC[0] + t * .5 + cu_ * HR, HC[1] + cv_ * HR
                m, Lc = ell(C, cxs, cys, rr * HR, rr * HR)
                C.paint(m, 'hair', hr, quant(Lc * .9 + .06, (-.05, .38, .82)), G_HAIR + 40 + (j % 2))
            return
        if st == 'crop':
            cap = ((U / 1.04) ** 2 + ((V + .16) / .98) ** 2 <= 1)
            edge = np.where(np.abs(U) < .8, -.52 + .06 * np.abs(np.sin(U * 9)), .05)
            m = cap & (V < edge)
            tn = quant(L - .05)
            tn = np.where(((np.floor(C.X) + np.floor(C.Y)) % 3 == 0) & (tn == 2), 1, tn) if self.detail != 'S' else tn
            C.paint(m, 'hair', hr, tn, G_HAIR)
            return
        cap = ((U / 1.11) ** 2 + ((V + .12) / 1.05) ** 2 <= 1)
        if st == 'short':        # tousled short: tufted fringe, cropped sides
            fringe = -.40 + .16 * np.abs(np.sin((U - part) * 7.5))
            side = .12
            tuft = poly(C, [(13.0, 4.6), (14.4, 2.4), (16.2, 3.0), (17.6, 1.7), (18.4, 3.4), (19.6, 4.6)])
            m = (cap & (V < np.where(np.abs(U) < .8, fringe, side))) | (tuft & (V < -.6))
        elif st == 'swept':      # long side-swept fringe that covers one brow
            # a long sweep falling from the parting across the forehead to the opposite brow
            k_ = np.clip((U - part + .25) / 1.25, 0, 1)
            fringe = -.62 + .52 * k_ ** .8 + .06 * np.abs(np.sin(U * 10))
            fringe = np.where(U < part - .25, -.62 + .1 * np.abs(np.sin(U * 8)), fringe)
            m = cap & (V < np.where(np.abs(U) < .82, fringe, np.where(U > 0, .32, .1)))
        elif st in ('long', 'wavy', 'braid'):   # middle / side part, curtain fringe, locks framing the face
            fringe = -.70 + .55 * np.abs(U - part) ** .9 + .05 * np.abs(np.sin(U * 12))
            m = cap & (V < np.where(np.abs(U) < .74, fringe, 9))
            lock_len = {'long': 1.75, 'wavy': 1.45, 'braid': .65}[st]
            wave = .06 * np.sin(V * 10) if st == 'wavy' else 0
            locks = (np.abs(U) > .72 + wave) & (np.abs(U) < 1.13 + wave) & (V > -.3) & (V < lock_len - .25 * (np.abs(U) - .72))
            m = m | locks
        elif st == 'bob':
            fringe = -.42 + .08 * np.abs(np.sin(U * 10)) + .1 * (U - part)
            m = cap & (V < np.where(np.abs(U) < .76, fringe, 9))
            locks = (np.abs(U) > .72) & (np.abs(U) < 1.16) & (V > -.3) & (V < .82 + .05 * np.sin(U * 15))
            m = m | locks
        elif st == 'ponytail':
            fringe = -.6 + .1 * np.abs(np.sin(U * 6))
            m = cap & (V < np.where(np.abs(U) < .82, fringe, .05))
        elif st in ('bun', 'elderbun'):
            fringe = -.52 + .07 * np.abs(np.sin(U * 11)) if st == 'bun' else -.5 + .22 * np.abs(U) ** 1.5
            m = cap & (V < np.where(np.abs(U) < .8, fringe, .1 if st == 'bun' else 0))
            if st == 'bun':   # loose tendrils at the temples
                for s in (-1, 1):
                    m = m | (capsule(C, 16 + s * 7.6, 10.5, 16 + s * 7.9, 17.5, .55)[0])
        else:
            m = cap & (V < -.4)
        if abs(t) > .2:   # 3/4: the back of the head shows on the near side, behind the ear
            s = -1 if t > 0 else 1
            Uh = (C.X - HC[0]) / HR
            back_m = ((Uh / 1.1) ** 2 + ((V + .1) / 1.06) ** 2 <= 1) & (Uh * s > .95 - .5 * abs(t) - .1) & (V < .42)
            m = m | back_m
        tn = quant(L, (-.18, .28, .8))
        tn = strands(tn)
        tn = shine(tn, rho)
        # locks hanging at the sides: cylinder shading so they don't look pasted on
        side_px = (np.abs(U) > .74) & (V > -.05)
        tn = np.where(side_px, np.where(U < 0, np.where(np.abs(U) > .98, 1, 2), np.where(np.abs(U) > .98, 0, 1)), tn)
        C.paint(m, 'hair', hr, tn, G_HAIR)
        if st in ('bun', 'elderbun'):   # drawn after the cap so it casts a contour onto it
            by = -1.17 if st == 'bun' else -1.1
            bm, bL = ell(C, 16 + t * .5, HC[1] + by * HR, 3.7 if st == 'bun' else 4.0, 2.7 if st == 'bun' else 2.3)
            btn = quant(bL)
            btn = np.where(((np.arctan2(C.Y - (HC[1] + by * HR), C.X - 16) * 4 / math.pi) % 1 < .22) & (btn >= 2), btn - 1, btn)
            C.paint(bm, 'hair', hr, btn, G_HAIR + 30)
        if st == 'braid':   # side braid over the shoulder
            s = c.get('braid_side', 1)
            for i in range(6):
                y = 18.2 + i * 2.35
                x = 16 + s * (7.0 - i * .45)
                bm, bL = ell(C, x, y, 1.75 - i * .07, 1.35)
                C.paint(bm, 'hair', hr, quant(bL, (-.3, .2, .7)), G_HAIR + 1 + i)
            tie, _ = ell(C, 16 + s * 4.3, 32.0, 1.0, .65)
            C.paint(tie, 'accent' if 'accent' in R else 'band', R.get('accent', R['band']), 2, G_HAIR + 8)
            tip, tL = ell(C, 16 + s * 4.2, 33.4, 1.1, 1.0)
            C.paint(tip, 'hair', hr, quant(tL), G_HAIR + 9)

    # ---------------------------------------------------------------- accessories
    def items(self, C, R):
        c = self.c
        held = c.get('held')
        s = c.get('hold_side', 1)
        if held == 'tea':
            x, y = 16 + s * 3.6 + self.turn * 1.6, 28.4
            cup = poly(C, [(x - 2.0, y - 1.8), (x + 2.0, y - 1.8), (x + 1.6, y + 1.2), (x - 1.6, y + 1.2)])
            L = cyl_light(C, x, 2.0, y - 2, y + 1)
            C.paint(cup, 'cup', R['cup'], quant(L), G_ITEM)
            hd, _ = ell(C, x - s * 2.6, y - .4, 1.05, 1.05)
            hole, _ = ell(C, x - s * 2.6, y - .4, .45, .45)
            C.paint(hd & ~hole & ~cup, 'cup', R['cup'], 1, G_ITEM)
            tea = poly(C, [(x - 1.6, y - 1.9), (x + 1.6, y - 1.9), (x + 1.6, y - 1.1), (x - 1.6, y - 1.1)])
            C.paint(tea, 'tea', R['tea'], 2, G_ITEM + 1)
            sau, _ = ell(C, x, y + 1.6, 3.0, .75)
            C.paint(sau, 'cup', R['cup'], np.where(C.X < x, 3, 1), G_ITEM + 2)
            # hand under the saucer
            hm, hL = ell(C, x + s * .4, y + 2.5, 1.5, 1.0)
            C.paint(hm, 'skin', R['skin'], 2, G_ITEM + 3)
        if held == 'book':   # a book held against the chest: cover, page edge, title band
            x, y = 16 + s * 3.4 + self.turn * 1.6, 28.8
            cov = poly(C, [(x - 2.4, y - 3.2), (x + 2.4, y - 3.2), (x + 2.4, y + 3.0), (x - 2.4, y + 3.0)])
            C.paint(cov, 'book', R['book'], np.where(C.X < x - 1.5, 3, np.where(C.X > x + 1.6, 1, 2)), G_ITEM)
            pg = poly(C, [(x + 1.6, y - 2.8), (x + 2.6, y - 2.8), (x + 2.6, y + 2.6), (x + 1.6, y + 2.6)]) if s > 0 else \
                poly(C, [(x - 2.6, y - 2.8), (x - 1.6, y - 2.8), (x - 1.6, y + 2.6), (x - 2.6, y + 2.6)])
            C.paint(pg, 'pages', R['pages'], 2, G_ITEM + 1)
            band = cov & (np.abs(C.Y - (y - .8)) < .55) & ~pg
            C.paint(band, 'gold', R['gold'], 3, G_ITEM + 2)
            hm, hL = ell(C, x - s * .6, y + 3.1, 1.5, 1.1)
            C.paint(hm, 'skin', R['skin'], 2, G_ITEM + 3)

    def glasses(self, C):
        det = self.detail
        tpl = TEMPLATES[det]
        col = rgb('#8a6038') if det == 'S' else rgb('#7a5530')
        hi = rgb('#e8d2a0')
        for side in (-1, 1):
            self.stamp(C, tpl['glasses'], self.fx(side * tpl['eye_dx']), 13.9, side, {'o': col, 'h': hi}, mirror=side > 0)
        self.stamp(C, tpl['bridge'], self.fx(0), 13.9 - tpl['bridge_dy'], 1, {'o': col})


# ------------------------------------------------------------------ face templates (hand-placed pixels)
# Left eye as seen by the viewer; the right one is mirrored. K lash/lid, D dark iris, I iris, i light iris,
# W highlight, S sclera. Mouth: M lip, m dark mouth, T teeth, t tongue, l/L skin shade/light.
TEMPLATES = {
    'S': {   # 32x48 sprite and the 32 px bust (head ~17 px wide)
        'eye_dx': .37, 'brow_dy': 2.6, 'mouth_dy': 3.7, 'nose_dy': 1.9, 'blush_dx': .17, 'blush_dy': 1.75,
        'bridge_dy': .3,
        'eye': {
            'open': ['KK', 'DW', 'II'],
            'wide': ['KK', 'DW', 'II', '.K'],
            'closed': ['...', 'K.K', '.K.'][::-1],
            'side': ['KK', 'WD', 'II'],
        },
        'brow': {'base': ['HHH'], 'up': ['HHH', '...'][::-1][::-1], 'raise': ['.HH', 'H..'], 'soft': ['HH.']},
        'nose': ['n'],
        'blush': ['bb'],
        'freckles': ['f.f'],
        'mouth': {
            'smile': ['l..l', '.MM.'],
            'grin': ['mmmm', '.TT.'],
            'laugh': ['mmmm', 'mttm', '.mm.'],
            'o': ['mm', 'mm'],
            'flat': ['.mm.'],
            'small': ['l.l', '.M.'],
            'smirk': ['...m', 'mmm.'],
        },
        'glint': ['gG'],
        'glasses': ['oooo', 'o..o', 'o..o', '.oo.'],
        'bridge': ['oo'],
    },
    'M': {   # 40 px bust (head ~25 px wide)
        'eye_dx': .37, 'brow_dy': 3.0, 'mouth_dy': 3.85, 'nose_dy': 2.0, 'blush_dx': .2, 'blush_dy': 1.9,
        'bridge_dy': .5,
        'eye': {
            'open': ['.KK.', 'KDWK', 'SIiS'[0:0] + 'KIIi'[0:0] + '.II.' if False else 'SDIS', '.II.'],
            'wide': ['.KK.', 'KDWK', 'SDIS', 'SIIS', '.KK.'],
            'closed': ['K..K', '.KK.'],
            'side': ['.KK.', 'KWDK', 'SIDS', '.II.'],
        },
        'brow': {'base': ['.HHH', 'HH..'], 'up': ['HHHH'], 'raise': ['..HH', '.H..', 'H...'], 'soft': ['HHH.']},
        'nose': ['n.', 'Nn'],
        'blush': ['bbb'],
        'freckles': ['f.f.', '.f..'],
        'mouth': {
            'smile': ['m...m', '.mmm.'],
            'grin': ['mmmmm', 'mTTTm', '.mmm.'],
            'laugh': ['mmmmm', 'mTTTm', 'mtttm', '.mmm.'],
            'o': ['.mm.', 'm..m', '.mm.'],
            'flat': ['.mmm.'],
            'small': ['m..m', '.mm.'],
            'smirk': ['....m', 'mmmm.'],
        },
        'glint': ['dgG', '.d.'],
        'glasses': ['.oooo.', 'o....o', 'o....o', 'o....o', '.oooo.'],
        'bridge': ['oo'],
    },
    'L': {   # 64 px portrait (head ~40 px wide)
        'eye_dx': .36, 'brow_dy': 3.2, 'mouth_dy': 3.85, 'nose_dy': 1.8, 'blush_dx': .22, 'blush_dy': 2.0,
        'bridge_dy': .4,
        'eye': {
            'open': ['..KKKK..', '.KKKKKKK', 'KSDDWWDK', '.SDDWDDS', '.SDIIDDS', '..IiiI..', '...ll...'[0:0] + '........'],
            'wide': ['..KKKK..', '.KKKKKKK', 'KSDDWWDS', 'SSDDWDDS', 'SSDIIDDS', '.SIiiIS.', '..SSSS..'],
            'closed': ['........', 'K......K', '.KK..KK.', '...KK...'],
            'side': ['..KKKK..', '.KKKKKKK', 'KWWDDSSK', '.WDDDSS.', '.IDDDSS.', '..iIS...'],
        },
        'brow': {'base': ['..HHHHH', 'HHHhh..'], 'up': ['.HHHHH.', 'HH...HH'], 'raise': ['....HHH', '..HHH..', 'HH.....'],
                 'soft': ['.HHHHH.', 'H......']},
        'nose': ['.h.', '.n.', 'nN.'],
        'blush': ['.bbb.', 'bbbbb'],
        'freckles': ['f.f..', '..f.f'],
        'mouth': {
            'smile': ['m......m', '.mm..mm.', '...mm...'],
            'grin': ['mmmmmmmm', 'mTTTTTTm', '.mTTTTm.', '..mmmm..'],
            'laugh': ['mmmmmmmm', 'mTTTTTTm', 'mmttttmm', '.mttttm.', '..mmmm..'],
            'o': ['..mm..', '.mmmm.', 'mmttmm', '.mmmm.', '..mm..'],
            'flat': ['.mmmmm.', '..LLL..'],
            'small': ['m....m', '.mmmm.', '..LL..'],
            'smirk': ['.......m', '.mmmmmm.', 'm.......'],
        },
        'glint': ['.dd..', 'dgGd.', '.dgd.', '..d..'],
        'glasses': ['..oooooo..', '.o......o.', 'o........o', 'o.h......o', 'o........o', '.o......o.', '..oooooo..'],
        'bridge': ['oooo'],
    },
}

DEFAULT = dict(skin='warm', hair='chestnut', hairstyle='short', eyes='brown', expr='smile', outfit='tee',
               top='leaf', bottom='charcoal', over=None, accent=None, neckband=False, blush=True)


# ------------------------------------------------------------------ public render helpers
def sprite(cfg):
    """32x48 full-body sprite (1x)."""
    C = Canvas(32, 48)
    return Citizen(cfg).render(C, 'S')


BUSTS = {   # size -> (frame width in sprite units, detail). Small tiles crop tighter so the face carries;
    24: (25.0, 'S'), 28: (25.0, 'S'), 32: (25.0, 'S'),     # the 64 px portrait keeps the shoulders.
    36: (25.0, 'M'), 40: (25.0, 'M'),
    64: (27.0, 'L'),
}


def bust(cfg, size=32):
    frame, det = BUSTS[size]
    k = size / frame
    ox = 16 - frame / 2
    oy = .8 if frame < 27 else 1.2
    C = Canvas(size, size, k=k, ox=ox, oy=oy)
    return Citizen(cfg).render(C, det)


def up(im, s):
    return im.resize((im.width * s, im.height * s), Image.NEAREST)


def figure(cfg, k=1.5):
    """Full body re-rasterised natively at scale k (e.g. 1.5 -> 48x72 for the arrival card, 2.5 -> 80x120 hero)."""
    det = 'S' if k < 1.3 else ('M' if k < 2 else 'L')
    C = Canvas(int(round(32 * k)), int(round(48 * k)), k=k)
    return Citizen(cfg).render(C, det)
