"""Tiny pixel-grid toolkit for the Tapaia logo options (original art)."""
import math
from PIL import Image


def circle(cx, cy, r):
    """Pixels whose centres fall inside a circle (grid units)."""
    out = set()
    for y in range(int(cy - r) - 1, int(cy + r) + 2):
        for x in range(int(cx - r) - 1, int(cx + r) + 2):
            if (x + .5 - cx) ** 2 + (y + .5 - cy) ** 2 <= r * r:
                out.add((x, y))
    return out


def ellipse(cx, cy, rx, ry):
    out = set()
    for y in range(int(cy - ry) - 1, int(cy + ry) + 2):
        for x in range(int(cx - rx) - 1, int(cx + rx) + 2):
            if ((x + .5 - cx) / rx) ** 2 + ((y + .5 - cy) / ry) ** 2 <= 1:
                out.add((x, y))
    return out


def rect(x0, y0, w, h):
    return {(x, y) for x in range(x0, x0 + w) for y in range(y0, y0 + h)}


N4 = ((1, 0), (-1, 0), (0, 1), (0, -1))
N8 = N4 + ((1, 1), (1, -1), (-1, 1), (-1, -1))


def edge(mask, nb=N4):
    """Pixels of mask touching a pixel outside mask."""
    return {(x, y) for (x, y) in mask if any((x + dx, y + dy) not in mask for dx, dy in nb)}


def shift(mask, dx, dy):
    return {(x + dx, y + dy) for (x, y) in mask}


def lit(mask, k=1, d=(-1, -1)):
    """Pixels whose neighbour k steps toward the light is outside the mask (lit edge)."""
    return {(x, y) for (x, y) in mask if (x + d[0] * k, y + d[1] * k) not in mask}


class Grid:
    def __init__(self, n):
        self.n = n
        self.px = {}

    def fill(self, mask, c, clip=None):
        for p in mask:
            if 0 <= p[0] < self.n and 0 <= p[1] < self.n and (clip is None or p in clip):
                self.px[p] = c
        return self

    def sprite(self, rows, legend, ox, oy, clip=None):
        for j, row in enumerate(rows):
            for i, ch in enumerate(row):
                if ch in legend and legend[ch] is not None:
                    p = (ox + i, oy + j)
                    if clip is None or p in clip:
                        self.px[p] = legend[ch]
        return self

    def image(self, scale=1):
        im = Image.new('RGBA', (self.n, self.n), (0, 0, 0, 0))
        for (x, y), c in self.px.items():
            if 0 <= x < self.n and 0 <= y < self.n:
                im.putpixel((x, y), hexrgba(c))
        if scale != 1:
            im = im.resize((self.n * scale, self.n * scale), Image.NEAREST)
        return im

    def svg(self, size=512):
        n = self.n
        parts = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {n} {n}" width="{size}" height="{size}" shape-rendering="crispEdges">']
        for y in range(n):
            x = 0
            while x < n:
                c = self.px.get((x, y))
                if c is None:
                    x += 1
                    continue
                x1 = x
                while x1 + 1 < n and self.px.get((x1 + 1, y)) == c:
                    x1 += 1
                parts.append(f'<rect x="{x}" y="{y}" width="{x1 - x + 1}" height="1" fill="{c}"/>')
                x = x1 + 1
        parts.append('</svg>')
        return '\n'.join(parts) + '\n'


def hexrgba(c):
    c = c.lstrip('#')
    return tuple(int(c[i:i + 2], 16) for i in (0, 2, 4)) + (255,)


DISC16 = [(5, 10), (3, 12), (2, 13), (1, 14), (1, 14)] + [(0, 15)] * 6 + [(1, 14), (1, 14), (2, 13), (3, 12), (5, 10)]


def disc(n, inset=0.15):
    if n == 16:   # hand-tuned 16px circle (smoother than the sampled one)
        return {(x, y) for y, (a, b) in enumerate(DISC16) for x in range(a, b + 1)}
    return circle(n / 2, n / 2, n / 2 - inset)


def coin(g, mask, outline, base, hi, lo, rim=1, hi2=None):
    """Fill a round coin: outline ring, then `rim` px bevel shaded top-left light / bottom-right dark."""
    n = g.n
    c = n / 2
    g.fill(mask, base)
    inner = set(mask)
    rings = []
    o = edge(inner, N8)
    g.fill(o, outline)
    inner -= o
    for _ in range(rim):
        r = edge(inner, N8)
        rings.append(r)
        inner -= r
    for i, r in enumerate(rings):
        for (x, y) in r:
            vx, vy = x + .5 - c, y + .5 - c
            m = math.hypot(vx, vy) or 1
            d = (-vx - vy) / (m * math.sqrt(2))
            if d > 0.35:
                g.px[(x, y)] = hi2 if (hi2 and i == 0 and d > 0.8) else hi
            elif d < -0.35:
                g.px[(x, y)] = lo
    return inner
