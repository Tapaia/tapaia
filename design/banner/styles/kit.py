"""Shared toolkit + layout for the Golden Hour style studies (original art).
World canvas is 750x250 ('A units'); the setting sun sits exactly where the coin logo goes."""
import math, random
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageChops

W, H = 750, 250
BASE = 188                       # building base line / back edge of the plaza
SUN = (487.5, 89.5)              # = coin centre (975, 179) in 1500x500 screen space
SH = (44, 22, 70)                # hue-shifted shadow target (deep violet)
LI = (255, 214, 146)             # hue-shifted light target (warm gold)


def rgb(c):
    if isinstance(c, tuple):
        return c[:3]
    c = c.lstrip('#')
    return tuple(int(c[i:i + 2], 16) for i in (0, 2, 4))


def shade(c, t):
    """t<0 -> toward violet shadow, t>0 -> toward gold light (hue-shifted ramps, never black)."""
    c = rgb(c)
    if t < 0:
        k = min(1, -t * .8)
        return tuple(int(c[i] + (SH[i] - c[i]) * k) for i in range(3))
    k = min(1, t * .62)
    return tuple(int(c[i] + (LI[i] - c[i]) * k) for i in range(3))


def mix(a, b, k):
    a, b = rgb(a), rgb(b)
    return tuple(int(a[i] + (b[i] - a[i]) * k) for i in range(3))


BAYER = np.array([[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]]) / 16.0


class Layer:
    def __init__(self, w=W, h=H):
        self.w, self.h = w, h
        self.im = Image.new('RGBA', (w, h), (0, 0, 0, 0))
        self.d = ImageDraw.Draw(self.im)
        self.px = self.im.load()

    def p(self, x, y, c, a=255):
        x, y = int(x), int(y)
        if 0 <= x < self.w and 0 <= y < self.h:
            self.px[x, y] = rgb(c) + (a,)

    def get(self, x, y):
        if 0 <= x < self.w and 0 <= y < self.h:
            return self.px[x, y]
        return (0, 0, 0, 0)

    def rect(self, x, y, w, h, c, a=255):
        if w > 0 and h > 0:
            self.d.rectangle([x, y, x + w - 1, y + h - 1], fill=rgb(c) + (a,))

    def ell(self, x0, y0, x1, y1, c, a=255):
        self.d.ellipse([x0, y0, x1, y1], fill=rgb(c) + (a,))

    def disc(self, cx, cy, r, c, a=255):
        self.d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=rgb(c) + (a,))

    def poly(self, pts, c, a=255):
        self.d.polygon(pts, fill=rgb(c) + (a,))

    def line(self, pts, c, w=1):
        self.d.line(pts, fill=rgb(c) + (255,), width=w)

    def blit(self, im, x, y):
        self.im.alpha_composite(im, (int(x), int(y)))


def rim_light(layer, strength=.45, side=1, alpha_min=1, only=None):
    """Sun is to the right (behind the coin): brighten pixels whose right neighbour is empty, shade left edges."""
    a = np.array(layer.im).astype(np.float32)
    alpha = a[..., 3] > 0
    right_empty = np.zeros_like(alpha); right_empty[:, :-1] = ~alpha[:, 1:]; right_empty[:, -1] = True
    left_empty = np.zeros_like(alpha); left_empty[:, 1:] = ~alpha[:, :-1]; left_empty[:, 0] = True
    lit = alpha & right_empty
    dark = alpha & left_empty & ~lit
    if only is not None:
        lit &= only; dark &= only
    li = np.array(LI, np.float32); sh = np.array(SH, np.float32)
    a[lit, :3] = a[lit, :3] + (li - a[lit, :3]) * strength
    a[dark, :3] = a[dark, :3] + (sh - a[dark, :3]) * strength * .55
    layer.im = Image.fromarray(a.astype(np.uint8)); layer.d = ImageDraw.Draw(layer.im); layer.px = layer.im.load()
    return layer


def haze(layer, col, k, top_extra=0.0):
    a = np.array(layer.im).astype(np.float32)
    c = np.array(rgb(col), np.float32)
    ys = np.arange(layer.h)[:, None].astype(np.float32)
    kk = (k + top_extra * (1 - ys / layer.h))[..., None]
    a[..., :3] = a[..., :3] + (c - a[..., :3]) * kk
    layer.im = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)); layer.d = ImageDraw.Draw(layer.im); layer.px = layer.im.load()
    return layer


def sun_warm(layer, k=.35, r=330):
    """Tint pixels toward gold by proximity to the sun (light wrapping the scene from behind the coin)."""
    a = np.array(layer.im).astype(np.float32)
    ys, xs = np.mgrid[0:layer.h, 0:layer.w]
    d = np.hypot((xs - SUN[0] * layer.w / W), (ys - SUN[1] * layer.h / H) * 1.4) / (r * layer.w / W)
    f = (np.clip(1 - d, 0, 1) ** 1.5 * k)[..., None]
    li = np.array((255, 190, 120), np.float32)
    a[..., :3] = a[..., :3] + (li - a[..., :3]) * f
    layer.im = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)); layer.d = ImageDraw.Draw(layer.im); layer.px = layer.im.load()
    return layer


def add_light(base_rgb, light_rgb, k=1.0):
    """Additive light (screen-ish) of an RGB light image onto an RGB base image."""
    b = np.array(base_rgb).astype(np.float32)
    l = np.array(light_rgb).astype(np.float32)[..., :3] * k
    out = 255 - (255 - b) * (255 - l) / 255
    return Image.fromarray(np.clip(out, 0, 255).astype(np.uint8))


# ------------------------------------------------------------------ fonts for tiny signs
FONT3 = {
    'L': ["x..", "x..", "x..", "x..", "xxx"], 'I': ["xxx", ".x.", ".x.", ".x.", "xxx"],
    'B': ["xx.", "x.x", "xx.", "x.x", "xx."], 'R': ["xx.", "x.x", "xx.", "x.x", "x.x"],
    'A': [".x.", "x.x", "xxx", "x.x", "x.x"], 'Y': ["x.x", "x.x", ".x.", ".x.", ".x."],
    'O': ["xxx", "x.x", "x.x", "x.x", "xxx"], 'P': ["xx.", "x.x", "xx.", "x..", "x.."],
    'E': ["xxx", "x..", "xx.", "x..", "xxx"], 'N': ["x..x", "xx.x", "x.xx", "x..x", "x..x"],
    'T': ["xxx", ".x.", ".x.", ".x.", ".x."],
}


def text3(L, x, y, word, col):
    for ch in word:
        if ch == ' ':
            x += 3; continue
        for j, row in enumerate(FONT3[ch]):
            for k, v in enumerate(row):
                if v == 'x':
                    L.p(x + k, y + j, col)
        x += len(FONT3[ch][0]) + 1
