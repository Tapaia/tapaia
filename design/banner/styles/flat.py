"""Style C, "illustrated flat": the same Golden Hour composition as A/B redrawn as a clean vector illustration
(no pixel grid) with soft gradients, hue-shifted shading (violet shadows, gold light) and the sun behind the coin.
Coordinates = A coordinates x2. Output: art/C-scene.svg (vector, used directly as the banner background)."""
import os, math, random
import hd
from kit import SUN, BASE

S = 2
SX, SY = SUN[0] * S, SUN[1] * S
GY = BASE * S          # 376: plaza line
R = random.Random(5)
out, defs = [], []
_id = [0]


def nid(p='g'):
    _id[0] += 1
    return f'{p}{_id[0]}'


def lg(stops, x1=0, y1=0, x2=0, y2=1, units=None):
    i = nid('lg')
    u = f' gradientUnits="{units}"' if units else ''
    defs.append(f'<linearGradient id="{i}" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}"{u}>' +
                ''.join(f'<stop offset="{o}" stop-color="{c}" stop-opacity="{a}"/>' for o, c, a in _st(stops)) + '</linearGradient>')
    return f'url(#{i})'


def rg(stops, cx=.5, cy=.5, r=.5, fx=None, fy=None, units=None, extra=''):
    i = nid('rg')
    u = f' gradientUnits="{units}"' if units else ''
    f = f' fx="{fx}" fy="{fy}"' if fx is not None else ''
    defs.append(f'<radialGradient id="{i}" cx="{cx}" cy="{cy}" r="{r}"{f}{u} {extra}>' +
                ''.join(f'<stop offset="{o}" stop-color="{c}" stop-opacity="{a}"/>' for o, c, a in _st(stops)) + '</radialGradient>')
    return f'url(#{i})'


def _st(stops):
    return [(s[0], s[1], s[2] if len(s) > 2 else 1) for s in stops]


def add(s):
    out.append(s)


def rect(x, y, w, h, fill, rx=0, extra=''):
    add(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx}" fill="{fill}" {extra}/>')


def circ(x, y, r, fill, extra=''):
    add(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" fill="{fill}" {extra}/>')


def ell(x, y, rx, ry, fill, extra=''):
    add(f'<ellipse cx="{x:.1f}" cy="{y:.1f}" rx="{rx:.1f}" ry="{ry:.1f}" fill="{fill}" {extra}/>')


def poly(pts, fill, extra=''):
    add(f'<polygon points="{" ".join(f"{x:.1f},{y:.1f}" for x, y in pts)}" fill="{fill}" {extra}/>')


def path(d, fill, extra=''):
    add(f'<path d="{d}" fill="{fill}" {extra}/>')


def warm(x, y, r=700):
    """0..1 proximity to the sun (coin)."""
    return max(0.0, 1 - math.hypot(x - SX, (y - SY) * 1.4) / r)


# ------------------------------------------------------------------ sky
def sky():
    rect(0, 0, 1500, 500, lg([(0, '#26164a'), (.32, '#4f2768'), (.55, '#9a3f70'), (.74, '#e2735f'), (.9, '#ffad6a'), (1, '#ffc98a')]))
    ell(SX, SY, 760, 420, rg([(0, '#ffb070', .55), (.5, '#ff8a68', .22), (1, '#ff7a68', 0)]))           # broad warm bloom
    ell(1200, 192, 560, 200, rg([(0, '#ffe2a6', .62), (.55, '#ffc68a', .25), (1, '#ffc08a', 0)]))       # afterglow behind wordmark
    circ(SX, SY, 300, rg([(0, '#fff7d8'), (.18, '#ffe7a8', .95), (.42, '#ffbe72', .45), (1, '#ff9a62', 0)]))
    # soft rays
    rays = []
    rr = random.Random(9)
    for i in range(22):
        a = math.radians(i * 360 / 22 + rr.uniform(-4, 4)); w = math.radians(rr.uniform(1.5, 3.2)); L = rr.uniform(380, 640)
        rays.append(f'<polygon points="{SX:.0f},{SY:.0f} {SX + L * math.cos(a - w):.0f},{SY + L * math.sin(a - w):.0f} {SX + L * math.cos(a + w):.0f},{SY + L * math.sin(a + w):.0f}" fill="#fff0c8" opacity="{rr.uniform(.07, .16):.2f}"/>')
    defs.append('<filter id="soft6" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="6"/></filter>')
    defs.append('<filter id="soft14" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="14"/></filter>')
    defs.append('<filter id="soft3" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="3"/></filter>')
    rm = rg([(0, '#fff', 1), (.6, '#fff', .6), (1, '#fff', 0)], SX, SY, 640, units='userSpaceOnUse')
    defs.append(f'<mask id="raymask"><circle cx="{SX}" cy="{SY}" r="640" fill="{rm}"/></mask>')
    add(f'<g filter="url(#soft6)" mask="url(#raymask)">' + ''.join(rays) + '</g>')


def cloud(x0, x1, y, th):
    x0, x1, y, th = x0 * S, x1 * S, y * S, th * S * 1.15
    cx = (x0 + x1) / 2
    w0 = warm(cx, y, 760)
    top = '#c27aa2' if w0 < .45 else '#8f4877'
    top = top if w0 < .7 else '#7e3d70'
    bot = '#ffc89a' if w0 < .5 else '#ffe1a6'
    g = lg([(0, top), (.55, top), (.82, '#f59a86'), (1, bot)], 0, y - th, 0, y + th * .4, units='userSpaceOnUse')
    i = nid('cc')
    defs.append(f'<clipPath id="{i}"><rect x="{x0 - 50}" y="{y - th * 2}" width="{x1 - x0 + 100}" height="{th * 2 + th * .4}"/></clipPath>')
    parts = [f'<rect x="{x0:.0f}" y="{y - th * .35:.0f}" width="{x1 - x0:.0f}" height="{th * .8:.0f}" rx="{th * .4:.0f}"/>']
    n = max(3, int((x1 - x0) / 70))
    rr = random.Random(int(x0 * 7 + y))
    for k in range(n):
        u = (k + .5) / n
        px = x0 + (x1 - x0) * u
        env = math.sin(math.pi * u) ** .6
        parts.append(f'<ellipse cx="{px + rr.uniform(-15, 15):.0f}" cy="{y - th * .1:.0f}" rx="{(x1 - x0) / n * rr.uniform(.55, 1.0):.0f}" ry="{th * env * rr.uniform(.45, 1.05):.0f}"/>')
        if rr.random() < .5:
            parts.append(f'<circle cx="{px + rr.uniform(-20, 20):.0f}" cy="{y - th * env * .55:.0f}" r="{th * env * rr.uniform(.35, .6):.0f}"/>')
    add(f'<g clip-path="url(#{i})" fill="{g}">' + ''.join(parts) + '</g>')
    # bright lit underside rim
    add(f'<rect x="{x0 + th * .4:.0f}" y="{y + th * .34:.1f}" width="{x1 - x0 - th * .8:.0f}" height="{max(2, th * .07):.1f}" rx="2" fill="#fff0c0" opacity="{.35 + .5 * w0:.2f}"/>')


# ------------------------------------------------------------------ landscape
def hills():
    for (amp, base, cf, cn, ph, f, op) in ((7, 166, '#8c5079', '#e59a70', 1.3, .021, 1), (6, 174, '#6f3f6e', '#c77a68', 4.0, .03, 1)):
        pts = []
        for x in range(0, 751, 6):
            pts.append((x * S, (base - amp * (math.sin(x * f + ph) * .6 + math.sin(x * f * 2.7 + ph * 2) * .4)) * S))
        d = 'M0,400 ' + ' '.join(f'L{x:.0f},{y:.1f}' for x, y in pts) + ' L1500,400 Z'
        path(d, lg([(0, cf), (.45, cf), (.65, cn), (.85, cf), (1, cf)], 0, 0, 1, 0))


def mountain():
    prof = [(x * S, hd.mountain_profile(x) * S) for x in range(-10, 431, 3)]
    d = f'M{prof[0][0]},{GY + 4} ' + ' '.join(f'L{x:.0f},{y:.1f}' for x, y in prof) + f' L{prof[-1][0]},{GY + 4} Z'
    defs.append(f'<clipPath id="mclip"><path d="{d}"/></clipPath>')
    path(d, lg([(0, '#2b3446'), (.42, '#3c5446'), (.62, '#5f7c4a'), (1, '#8a8f52')], 0, 0, 1, 0))
    # forest crowns: layered soft discs, violet-shadowed on the left, gold-lit on the right
    crowns = []
    rr = random.Random(3)
    for y in range(int(min(p[1] for p in prof)) - 10, GY, 11):
        for x in range(-20, 880, 13):
            xx = x + rr.uniform(-8, 8) + (6 if (y // 11) % 2 else 0); yy = y + rr.uniform(-6, 6)
            u = max(0, min(1, (xx - 160) / 680 + rr.uniform(-.12, .12)))
            r = rr.choice([8, 10, 12, 14, 18, 22])
            dark = ['#2a3242', '#2e4040', '#354c40', '#3c5640'][int(u * 3.99)]
            mid = ['#3a4a4c', '#455e46', '#557248', '#68844a'][int(u * 3.99)]
            lit = ['#4f5e58', '#6c8052', '#929a58', '#bdb064'][int(u * 3.99)]
            gid = nid('cr')
            defs.append(f'<radialGradient id="{gid}" cx=".62" cy=".32" r=".75"><stop offset="0" stop-color="{lit}"/><stop offset=".45" stop-color="{mid}"/><stop offset="1" stop-color="{dark}"/></radialGradient>')
            crowns.append(f'<circle cx="{xx:.0f}" cy="{yy:.0f}" r="{r:.1f}" fill="url(#{gid})"/>')
    add('<g clip-path="url(#mclip)">' + ''.join(crowns) +
        f'<rect x="0" y="0" width="900" height="{GY}" fill="{lg([(0, "#d98aa0", .38), (.5, "#c07a98", .14), (1, "#c07a98", 0)])}"/>' +
        f'<rect x="0" y="0" width="900" height="{GY}" fill="{lg([(0, "#ffb070", 0), (.55, "#ffb070", 0), (1, "#ffb070", .22)], 0, 0, 1, 0)}"/></g>')
    # rim light along the ridge on the sun side
    ridge = [(x, y) for x, y in prof if x > 392]
    add('<polyline points="' + ' '.join(f'{x:.0f},{y + 1:.1f}' for x, y in ridge) + '" fill="none" stroke="#ffd9a0" stroke-width="2.4" opacity=".55" filter="url(#soft3)"/>')
    # staircase [ch6:325]: straight, 200 m, up the mountain side
    (ax, ay), (bx, by) = [(p[0] * S, p[1] * S) for p in hd.STAIR]
    L = math.hypot(bx - ax, by - ay); nx, ny = -(by - ay) / L, (bx - ax) / L
    hw = 5
    poly([(ax + nx * hw, ay + ny * hw), (bx + nx * hw * 1.6, by + ny * hw * 1.6), (bx - nx * hw * 1.6, by - ny * hw * 1.6), (ax - nx * hw, ay - ny * hw)],
         lg([(0, '#c9a08e'), (1, '#f0caa0')], ax, ay, bx, by, units='userSpaceOnUse'))
    steps = ''.join(f'<line x1="{ax + (bx - ax) * t + nx * hw:.1f}" y1="{ay + (by - ay) * t + ny * hw:.1f}" x2="{ax + (bx - ax) * t - nx * hw:.1f}" y2="{ay + (by - ay) * t - ny * hw:.1f}"/>'
                    for t in [i / 46 for i in range(1, 46)])
    add(f'<g stroke="#8d6a76" stroke-width="1.1" opacity=".7">{steps}</g>')
    add(f'<line x1="{ax - nx * hw:.1f}" y1="{ay - ny * hw:.1f}" x2="{bx - nx * hw * 1.6:.1f}" y2="{by - ny * hw * 1.6:.1f}" stroke="#ffe0b0" stroke-width="1.4" opacity=".8"/>')
    # castle-tower apartments [ch1:30]
    for (x, top, w) in hd.TOWERS:
        castle(x * S, top * S, w * S)
    # tree clumps around the tower feet
    for (x, top, w) in hd.TOWERS:
        for k in range(5):
            cx = x * S + k * w * S / 4 + R.uniform(-6, 6); cy = 352 + R.uniform(-8, 6)
            circ(cx, cy, R.uniform(13, 19), rg([(0, '#7f9150'), (.5, '#4d6844'), (1, '#2c3c3e')], .6, .3, .75))
    # stone tower at the top [ch6:327], larger brighter green circle
    x, top, w, h = [v * S for v in hd.ORDER_TOWER]
    rect(x, top + 6, w, h, lg([(0, '#6d5872'), (.55, '#b48f88'), (1, '#e8bf98')], 0, 0, 1, 0))
    rect(x - 3, top + 2, w + 6, 8, lg([(0, '#5f4b68'), (1, '#d8ae8e')], 0, 0, 1, 0))
    for i in range(6):
        rect(x - 3 + i * (w + 6) / 6 + 1, top - 5, (w + 6) / 6 - 3, 8, '#b08a86' if i < 4 else '#e2b892')
    rect(x + w * .3, top + 22, 5, 11, '#3a2a48', 2); rect(x + w * .62, top + 42, 5, 11, '#3a2a48', 2)
    circ(x + w / 2, top - 14, 22, rg([(0, '#5dff9c', .55), (1, '#39e07a', 0)]))
    circ(x + w / 2, top - 14, 7, 'none', 'stroke="#39e07a" stroke-width="3.2"')
    circ(x + w / 2, top - 14, 4.5, '#1d4a36')


def castle(x, top, w):
    rect(x, top + 16, w, GY - top - 16, lg([(0, '#5a4870'), (.35, '#8f7484'), (.75, '#d2a990'), (1, '#f4cfa0')], 0, 0, 1, 0))
    rect(x - 4, top + 10, w + 8, 8, lg([(0, '#4e3f66'), (1, '#e0b896')], 0, 0, 1, 0))
    for i in range(0, int(w + 8), 6):
        rect(x - 4 + i, top + 5, 4, 6, '#9a7c88' if i < w * .6 else '#e8c29c')
    cx = x + w / 2
    poly([(x - 4, top + 6), (cx, top - 20), (x + w + 4, top + 6)], lg([(0, '#3b3460'), (.6, '#6a5a86'), (1, '#b48a96')], 0, 0, 1, 0))
    line = f'<line x1="{cx}" y1="{top - 20}" x2="{cx}" y2="{top - 27}" stroke="#3b3460" stroke-width="2"/>'
    add(line)
    rr = random.Random(int(x))
    for row in range(15):
        yy = top + 24 + row * 8
        if yy > GY - 8:
            break
        for col in range(3):
            xx = x + 5 + col * (w - 14) / 2
            lit = rr.random() < .3
            rect(xx, yy, 4, 4.5, '#ffd27a' if lit else '#3e2e52', 1)
            if lit:
                circ(xx + 2, yy + 2, 6, '#ffc870', 'opacity=".25"')


def treeline():
    g = []
    rr = random.Random(21)
    for x in range(-12, 1520, 18):
        y = GY - 12 - rr.uniform(0, 12); r = rr.uniform(16, 22)
        w0 = warm(x, y, 620)
        lit = '#7f8a52' if w0 < .4 else '#c9b064'
        g.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r:.0f}" fill="url(#tl{1 if w0 >= .4 else 0})"/>')
    defs.append('<radialGradient id="tl0" cx=".62" cy=".3" r=".75"><stop offset="0" stop-color="#6f7c50"/><stop offset=".5" stop-color="#3e5240"/><stop offset="1" stop-color="#26303a"/></radialGradient>')
    defs.append('<radialGradient id="tl1" cx=".45" cy=".25" r=".8"><stop offset="0" stop-color="#e2c070"/><stop offset=".45" stop-color="#6c7a4c"/><stop offset="1" stop-color="#3a3f44"/></radialGradient>')
    add('<g>' + ''.join(g) + '</g>')
    rect(0, GY - 8, 1500, 14, '#2c3a38')
    rect(0, 330, 1500, 50, lg([(0, '#ffb08a', 0), (1, '#ffb08a', .18)]))     # aerial haze


# ------------------------------------------------------------------ buildings
def win(x, y, w, h, lit=True):
    rect(x - 2, y - 2, w + 4, h + 4, '#6a4a3a', 2)
    if lit:
        rect(x, y, w, h, lg([(0, '#ffe9a8'), (1, '#f7a95a')]), 1)
        circ(x + w / 2, y + h / 2, w * 1.1, '#ffcf7a', 'opacity=".22" filter="url(#soft14)"')
    else:
        rect(x, y, w, h, lg([(0, '#4a3a5e'), (1, '#2e2440')]), 1)
    add(f'<line x1="{x + w / 2}" y1="{y}" x2="{x + w / 2}" y2="{y + h}" stroke="#6a4a3a" stroke-width="2"/>')


def green_circle(cx, cy, r=5):
    circ(cx, cy, r * 2.6, rg([(0, '#5dff9c', .45), (1, '#39e07a', 0)]))
    circ(cx, cy, r, '#1d4a36', 'stroke="#39e07a" stroke-width="2.4"')


def door(x, y, w, h, side=-1):
    rect(x, y, w, h, lg([(0, '#5a3426'), (1, '#8a5638')], 0, 0, 1, 0), 3)
    circ(x + w - 5, y + h / 2, 1.6, '#f0c060')
    green_circle(x - 8 if side < 0 else x + w + 8, y + h * .42, 4.5)


def roof(x, y, w, h, c1, c2, over=8):
    poly([(x - over, y + h), (x + 10, y), (x + w - 10, y), (x + w + over, y + h)], lg([(0, c1), (.7, c2), (1, '#f0b088')], 0, 0, 1, 0))
    for k in range(1, 4):
        yy = y + h * k / 4
        add(f'<line x1="{x - over * k / 4 + 10 * (1 - k / 4):.0f}" y1="{yy:.0f}" x2="{x + w + over * k / 4 - 10 * (1 - k / 4):.0f}" y2="{yy:.0f}" stroke="#000" stroke-opacity=".12" stroke-width="1.5"/>')
    rect(x - over, y + h, w + over * 2, 3, '#2e2240', 0, 'opacity=".35"')


def wall(x, y, w, h, c):
    rect(x, y, w, h, lg([(0, c[0]), (.7, c[1]), (1, c[2])], 0, 0, 1, 0))
    rect(x + w - 3, y, 3, h, '#ffdca0', 0, 'opacity=".55"')                 # rim light from the sun


def house(x, w, h, wallc, roofc, sign=None, garden=False):
    x, w, h = x * S, w * S, h * S
    y = GY - h
    wall(x, y, w, h, wallc)
    roof(x, y - 30, w, 30, *roofc)
    if garden:
        for k in range(9):
            circ(x + 6 + k * (w - 12) / 8, y - 30 - 4, 8, '#4f7a46')
            circ(x + 8 + k * (w - 12) / 8, y - 30 - 8, 2.4, ['#ff8fa0', '#ffd36b', '#c9a0ff'][k % 3])
    for wx in (x + 14, x + w - 38):
        win(wx, y + 18, 24, 26)
        rect(wx - 3, y + 46, 30, 5, '#7a4a3a', 2)
        for k in range(4):
            circ(wx + 2 + k * 7, y + 45, 2.6, ['#ff8fa0', '#ffd36b', '#fff2d8', '#c9a0ff'][k])
    win(x + 14, y + 72, 30, 30)
    door(x + w - 40, GY - 50, 24, 50, -1)
    if sign:
        add(f'<line x1="{x + w / 2 - 6}" y1="{y + 64}" x2="{x + w / 2 + 14}" y2="{y + 64}" stroke="#3a2a3e" stroke-width="2"/>')
        rect(x + w / 2 - 4, y + 66, 18, 14, '#c89a5a', 2)
    rect(x, GY - 8, w, 8, '#9a7a80')


def tea_house(x):
    x, w, h = x * S, 92 * S, 58 * S
    y = GY - h
    wall(x, y, w, h, ('#b08060', '#d9a878', '#f2c290'))
    for k in range(0, w + 1, 46):
        rect(x + k - 3, y, 6, 70, '#5a3828')
    rect(x, y + 66, w, 6, '#5a3828')
    add(f'<path d="M{x + 46} {y + 4} L{x + 92} {y + 66} M{x + 138} {y + 4} L{x + 92} {y + 66}" stroke="#5a3828" stroke-width="4"/>')
    roof(x, y - 34, w, 34, '#8a3a32', '#c8604a')
    win(x + 22, y + 18, 30, 28); win(x + w - 52, y + 18, 30, 28)
    rect(x + w / 2 - 18, y + 16, 36, 28, '#e8d0a0', 3, 'stroke="#5a3828" stroke-width="2"')
    add(f'<path d="M{x + w / 2 - 10} {y + 26} h16 v8 a6 6 0 0 1 -6 6 h-4 a6 6 0 0 1 -6 -6 z M{x + w / 2 + 6} {y + 28} a4 4 0 0 1 0 8" fill="#7a4a3a" stroke="#7a4a3a" stroke-width="1.5"/>')
    # striped awning
    n = 12
    for k in range(n):
        poly([(x - 6 + k * (w + 12) / n, y + 74), (x - 6 + (k + 1) * (w + 12) / n, y + 74), (x - 6 + (k + 1) * (w + 12) / n, y + 90), (x - 6 + k * (w + 12) / n, y + 90)],
             '#4c7a42' if k % 2 == 0 else '#f3e4c0')
    for k in range(n):
        circ(x - 6 + (k + .5) * (w + 12) / n, y + 90, (w + 12) / n / 2, '#3e6838' if k % 2 == 0 else '#e2d0a8')
    rect(x + 10, y + 96, 120, 18, lg([(0, '#ffe9a8'), (1, '#f7a95a')]), 2)       # counter window
    for k in range(6):
        circ(x + 22 + k * 19, y + 106, 4, '#fff4dc')
    door(x + w - 44, GY - 44, 22, 44, 1)
    rect(x, GY - 8, w, 8, '#9a7a80')


def library(x):
    x, w, h = x * S, 80 * S, 66 * S
    y = GY - h
    wall(x, y, w, h, ('#8a7480', '#b8a096', '#e6c4a2'))
    for r_ in range(0, h, 10):
        off = 0 if (r_ // 10) % 2 else 12
        for c in range(off, w, 24):
            add(f'<rect x="{x + c}" y="{y + r_}" width="22" height="8" fill="none" stroke="#5a4660" stroke-opacity=".18"/>')
    roof(x, y - 30, w, 30, '#3b3460', '#6a5a86')
    rect(x + w / 2 - 44, y + 10, 88, 22, '#f6ead2', 3, 'stroke="#5a3828" stroke-width="2"')
    add(f'<text x="{x + w / 2}" y="{y + 26.5}" text-anchor="middle" font-family="Inter" font-weight="800" font-size="13" letter-spacing="1.5" fill="#3a2a3e">LIBRARY</text>')
    rr = random.Random(4)
    for wx in (x + 16, x + w - 56):          # dull business books with the odd gold band
        rect(wx - 3, y + 42, 46, 62, '#6a4a3a', 2)
        rect(wx, y + 45, 40, 56, '#f2dcae', 1)
        for shelf in range(3):
            sy = y + 47 + shelf * 18
            bx = wx + 2
            while bx < wx + 37:
                bw = rr.choice([3, 4, 4, 5])
                c = rr.choice(['#7c6a74', '#8a7a68', '#6a6e7a', '#9a8a7a', '#5e5a6a'])
                rect(bx, sy + rr.choice([0, 2]), bw, 15 - rr.choice([0, 2]), c)
                if rr.random() < .2:
                    rect(bx, sy + 6, bw, 2, '#d8b060')
                bx += bw + 1
            rect(wx, sy + 15, 40, 2, '#6a4a3a')
    door(x + w / 2 - 12, GY - 48, 24, 48, -1)
    rect(x + w / 2 - 16, GY - 54, 32, 4, '#cdb9a8')
    rect(x, GY - 8, w, 8, '#9a7a80')


def empty_shop(x):
    x, w, h = x * S, 58 * S, 52 * S
    y = GY - h
    wall(x, y, w, h, ('#c8aa98', '#ead2b6', '#fbe2bc'))
    roof(x, y - 28, w, 28, '#8a3a32', '#c8604a')
    win(x + 16, y + 12, 20, 20); win(x + w - 36, y + 12, 20, 20)
    rect(x + 10, y + 46, 70, 44, '#f6efe2', 2, 'stroke="#6a4a3a" stroke-width="3"')
    add(f'<text x="{x + 45}" y="{y + 62}" text-anchor="middle" font-family="Inter" font-weight="800" font-size="12" letter-spacing="1.5" fill="#2e8a54">OPEN</text>')
    rect(x + 34, y + 74, 22, 4, '#8a5638', 1)                                   # the lone stool nobody wants [ch6:225]
    rect(x + 36, y + 78, 3, 10, '#6a4030'); rect(x + 51, y + 78, 3, 10, '#6a4030')
    rect(x + 30, y + 88, 30, 3, '#b8a090')
    door(x + w - 30, GY - 44, 20, 44, -1)
    rect(x, GY - 8, w, 8, '#9a7a80')


# ------------------------------------------------------------------ square
def plaza():
    rect(0, GY, 1500, 124, lg([(0, '#c99a86'), (.4, '#a07282'), (1, '#5e4064')]))
    # paving rows in perspective
    y, k = GY, 0
    while y < 500:
        hh = 7 + k * 2.2
        add(f'<line x1="0" y1="{y:.1f}" x2="1500" y2="{y:.1f}" stroke="#4a2e50" stroke-opacity=".22" stroke-width="1.2"/>')
        off = (k % 2) * (18 + k * 4)
        step = 36 + k * 8
        for x in range(-int(off), 1500, int(step)):
            add(f'<line x1="{x}" y1="{y:.1f}" x2="{x - (x - 750) * .02:.1f}" y2="{y + hh:.1f}" stroke="#4a2e50" stroke-opacity=".14" stroke-width="1"/>')
        y += hh; k += 1
    # warm light wash on the sun side + sun reflection leading the eye up to the coin
    rect(0, GY, 1500, 124, lg([(0, '#ffb070', 0), (.45, '#ffb070', .05), (.65, '#ffc080', .28), (.9, '#ffb070', .08), (1, '#ffb070', 0)], 0, 0, 1, 0))
    path(f'M{SX - 20},{GY} L{SX + 20},{GY} L{SX + 70},500 L{SX - 70},500 Z', lg([(0, '#fff0c0', .55), (1, '#ffd890', 0)]), 'filter="url(#soft6)"')
    for (wx, wy) in [(9, 14), (71, 14), (131, 14), (192, 58)]:
        ell((wx + 8) * S + 14, GY + 22, 16, 10, '#ffd88a', 'opacity=".18" filter="url(#soft3)"')


def shadow(x, y, rx, ry=5):
    ell(x, y, rx, ry, '#3b2440', 'opacity=".35"')


def lamp(x, gy):
    x, gy = x * S, gy * S
    shadow(x + 2, gy, 16, 4)
    ell(x + 2, gy, 60, 12, '#ffcf80', 'opacity=".22" filter="url(#soft6)"')
    rect(x - 1, gy - 92, 5, 92, lg([(0, '#3a2c48'), (1, '#7a6a8a')], 0, 0, 1, 0))
    rect(x - 7, gy - 4, 17, 4, '#3a2c48', 1)
    circ(x + 2, gy - 100, 46, rg([(0, '#ffe2a0', .55), (.4, '#ffc070', .2), (1, '#ffb060', 0)]))
    poly([(x - 7, gy - 92), (x + 11, gy - 92), (x + 8, gy - 108), (x - 4, gy - 108)], '#fff0c0', 'stroke="#3a2c48" stroke-width="2.5"')
    poly([(x - 9, gy - 108), (x + 13, gy - 108), (x + 2, gy - 116)], '#3a2c48')


def tea_table(x, gy):
    x, gy = x * S, gy * S
    shadow(x + 14, gy, 22)
    rect(x, gy - 24, 30, 5, lg([(0, '#7a4a30'), (1, '#c8885a')], 0, 0, 1, 0), 2)
    rect(x + 13, gy - 20, 4, 20, '#5a3424')
    green_circle(x + 21, gy - 27, 3.5)                       # green circle on the tabletop [ch6:271]
    for k in (x + 4, x + 10):
        rect(k, gy - 31, 5, 6, '#fbf1d6', 1)


def tea_cart(x, gy):
    x, gy = x * S, gy * S
    shadow(x + 46, gy, 54)
    for px in (x + 4, x + 86):
        rect(px, gy - 84, 4, 60, '#5a3424')
    n = 10
    for k in range(n):
        rect(x - 8 + k * 104 / n, gy - 96, 104 / n + .5, 14, '#4c7a42' if k % 2 == 0 else '#f3e4c0')
        circ(x - 8 + (k + .5) * 104 / n, gy - 82, 104 / n / 2, '#3e6838' if k % 2 == 0 else '#e2d0a8')
    rect(x, gy - 42, 92, 24, lg([(0, '#7a4a30'), (.7, '#c8885a'), (1, '#f0b880')], 0, 0, 1, 0), 3)
    rect(x, gy - 44, 92, 4, '#e0a878', 2)
    add(f'<path d="M{x + 12} {gy - 44} h18 v-10 a9 7 0 0 0 -18 0 z" fill="#f4ead2"/><path d="M{x + 30} {gy - 52} l7 -4" stroke="#f4ead2" stroke-width="3"/>')
    for k in (x + 44, x + 56, x + 68):
        rect(k, gy - 50, 8, 6, '#fbf1d6', 1.5)
    add(f'<path d="M{x + 20} {gy - 60} q-5 -8 0 -14 q5 -6 0 -12" stroke="#fff6e6" stroke-width="2" fill="none" opacity=".7"/>')
    green_circle(x + 80, gy - 30, 4)
    for wx in (x + 16, x + 74):
        circ(wx, gy - 10, 10, '#4a2c22'); circ(wx, gy - 10, 6, '#b07a50'); circ(wx, gy - 10, 2, '#4a2c22')


def pole(x, gy):
    """'a green circle on top of a one meter tall pole, labeled "Check in"' [ch5:46]"""
    x, gy = x * S, gy * S
    shadow(x + 2, gy, 10, 3)
    rect(x, gy - 34, 4, 34, lg([(0, '#5a5470'), (1, '#c3bcd4')], 0, 0, 1, 0))
    rect(x - 4, gy - 3, 12, 3, '#5a5470', 1)
    green_circle(x + 2, gy - 44, 8)


def bench(x, gy, w=26):
    x, gy, w = x * S, gy * S, w * S
    shadow(x + w / 2, gy, w / 2 + 4, 4)
    for j in range(3):
        rect(x, gy - 26 + j * 5, w, 3.5, '#b07a50' if j % 2 == 0 else '#8a5638', 1.5)
    rect(x, gy - 12, w, 4, '#c8885a', 1.5)
    for lx in (x + 4, x + w - 8):
        rect(lx, gy - 12, 4, 12, '#352743')


def playground(x, gy):
    """bare, basic, empty [ch6:221]"""
    x, gy = x * S, gy * S
    shadow(x + 50, gy, 54, 5)
    st = 'stroke="#8a84a0" stroke-width="4" stroke-linecap="round"'
    add(f'<path d="M{x} {gy} L{x + 8} {gy - 60} M{x + 60} {gy} L{x + 52} {gy - 60} M{x + 4} {gy - 61} L{x + 56} {gy - 61}" {st} fill="none"/>')
    add(f'<path d="M{x + 22} {gy - 59} V{gy - 18} M{x + 38} {gy - 59} V{gy - 18}" stroke="#b3acc4" stroke-width="1.6"/>')
    rect(x + 18, gy - 19, 24, 4, '#8a5638', 1.5)
    sx = x + 72
    add(f'<path d="M{sx} {gy} V{gy - 36} M{sx + 12} {gy} V{gy - 36} M{sx} {gy - 28} h12 M{sx} {gy - 18} h12 M{sx} {gy - 8} h12" stroke="#8a84a0" stroke-width="3" fill="none"/>')
    add(f'<path d="M{sx + 12} {gy - 36} Q{sx + 30} {gy - 30} {sx + 42} {gy}" stroke="#c3bcd4" stroke-width="5" fill="none" stroke-linecap="round"/>')


def tree(x, gy, h, r, maple=False):
    x, gy, h, r = x * S, gy * S, h * S, r * S
    shadow(x + 4, gy, r * .8, 6)
    rect(x - 5, gy - h, 10, h, lg([(0, '#3a2430'), (1, '#8a5a40')], 0, 0, 1, 0), 3)
    cols = ('#ffc070', '#e0703f', '#9a3434', '#4a1c2e') if maple else ('#d8c070', '#6f8a4a', '#3a5640', '#24302c')
    g = rg([(0, cols[0]), (.3, cols[1]), (.7, cols[2]), (1, cols[3])], .66, .28, .8)
    for (dx, dy, rr_) in ((0, -h - r * .3, r), (-r * .6, -h + r * .15, r * .7), (r * .6, -h + r * .2, r * .72), (r * .1, -h - r * .9, r * .62)):
        circ(x + dx, gy + dy, rr_, g)
    circ(x + r * .4, gy - h - r * .6, r * .5, '#fff0b0', 'opacity=".12"')


SKIN = {'warm': '#d9a07a', 'fair': '#f0c8a8', 'tan': '#c08a62', 'deep': '#8a5a3e'}
HAIR = {'chestnut': '#6a3a26', 'ginger': '#c8582e', 'black': '#2a1e2a', 'blonde': '#e8c060', 'silver': '#c8c4d0'}


def person(x, fy, kind, skin, hair, shirt, pants, long_hair):
    x, fy = x * S + 14, fy * S
    sk, hr = SKIN[skin], HAIR[hair]
    shadow(x, fy, 16, 4)
    rim = 'stroke="#ffd9a0" stroke-width="0"'
    if kind in ('robe', 'hood'):
        robe = lg([(0, '#2a1a40'), (.6, '#4a2e6a'), (1, '#8a62a8')], 0, 0, 1, 0)
        path(f'M{x - 9} {fy - 44} Q{x} {fy - 50} {x + 9} {fy - 44} L{x + 13} {fy} L{x - 13} {fy} Z', robe)
        path(f'M{x + 8} {fy - 42} L{x + 12} {fy - 2}', 'none', 'stroke="#ffcf98" stroke-width="1.6" opacity=".7"')
    else:
        rect(x - 7, fy - 22, 6, 22, pants, 2); rect(x + 1, fy - 22, 6, 22, pants, 2)
        rect(x - 9, fy - 46, 18, 26, lg([(0, shirt), (1, shirt)]), 5)
        rect(x - 9, fy - 46, 18, 26, lg([(0, '#2a1640', .25), (.6, '#2a1640', 0), (1, '#ffd9a0', .3)], 0, 0, 1, 0), 5)
        rect(x - 12, fy - 44, 4, 18, shirt, 2); rect(x + 8, fy - 44, 4, 18, shirt, 2)
    if kind == 'hood':
        circ(x, fy - 52, 10.5, '#3a2456')
        circ(x + 1, fy - 51, 6.5, '#2a1840')                                 # face cover [ch1:140]
        add(f'<line x1="{x - 5}" y1="{fy - 49}" x2="{x + 7}" y2="{fy - 49}" stroke="#6a4a8e" stroke-width="1.6"/>')
        circ(x + 3.5, fy - 53, 1, '#120a1c')
    else:
        if long_hair:
            rect(x - 9, fy - 60, 18, 22, hr, 6)
        circ(x, fy - 54, 8.5, lg([(0, sk), (1, sk)]))
        circ(x, fy - 54, 8.5, lg([(0, '#2a1640', .18), (.6, '#2a1640', 0), (1, '#ffe0b0', .3)], 0, 0, 1, 0))
        path(f'M{x - 9} {fy - 54} Q{x - 9} {fy - 65} {x} {fy - 64} Q{x + 9} {fy - 65} {x + 9} {fy - 55} Q{x + 3} {fy - 59} {x - 9} {fy - 54} Z', hr)
        circ(x + 3.5, fy - 54, 1.1, '#2a1e2a')


def hedge():
    g = []
    rr = random.Random(8)
    for x in range(-16, 1530, 22):
        r = rr.uniform(18, 24)
        g.append(f'<circle cx="{x:.0f}" cy="{500 + rr.uniform(-2, 6):.0f}" r="{r:.0f}" fill="url(#hg)"/>')
    defs.append('<radialGradient id="hg" cx=".6" cy=".25" r=".8"><stop offset="0" stop-color="#8a9a56"/><stop offset=".4" stop-color="#3b5538"/><stop offset="1" stop-color="#1d2626"/></radialGradient>')
    for _ in range(120):
        x = rr.uniform(0, 1500); y = 500 - rr.uniform(4, 16)
        g.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{rr.uniform(1.6, 2.8):.1f}" fill="{rr.choice(["#ff8fa0", "#ffd36b", "#c9a0ff", "#fff2d8", "#ff7a5c"])}"/>')
    add('<g>' + ''.join(g) + '</g>')


def build():
    sky()
    for c in hd.CLOUDS:
        cloud(*c)
    hills()
    mountain()
    treeline()
    house(2, 56, 62, ('#7e8498', '#a9adb8', '#e6d2c0'), ('#3b3460', '#6a5a86'), sign=True)
    house(64, 54, 58, ('#b89a86', '#e3c9a2', '#fbe2bc'), ('#8a3a32', '#c8604a'), sign=True, garden=True)
    house(124, 52, 64, ('#7890a8', '#9cb6c8', '#e6d4c4'), ('#3b3460', '#6a5a86'), sign=True)
    tea_house(184)
    library(284)
    empty_shop(372)
    plaza()
    items = [('tree', 24, 236, 26, 28, False), ('tree', 506, 214, 24, 22, False), ('tree', 724, 230, 28, 27, True),
             ('table', 214, 208), ('table', 266, 210), ('cart', 520, 222), ('pole', 610, 224), ('bench', 620, 236),
             ('playground', 384, 228), ('lamp', 176, 206), ('lamp', 446, 224), ('lamp', 690, 236)]
    items += [('person',) + p for p in hd.PEOPLE]
    items.sort(key=lambda it: it[2])
    for it in items:
        k = it[0]
        if k == 'tree': tree(*it[1:])
        elif k == 'table': tea_table(*it[1:])
        elif k == 'cart': tea_cart(*it[1:])
        elif k == 'pole': pole(*it[1:])
        elif k == 'bench': bench(*it[1:])
        elif k == 'playground': playground(*it[1:])
        elif k == 'lamp': lamp(*it[1:])
        elif k == 'person': person(*it[1:])
    hedge()
    # final warm grade: light wraps from the sun across the whole picture
    ell(SX, SY + 40, 900, 420, rg([(0, '#ffcf90', .22), (1, '#ffcf90', 0)]), 'style="mix-blend-mode:screen"')
    rect(0, 0, 1500, 500, rg([(0, '#000', 0), (.7, '#000', 0), (1, '#1a0c2a', .35)], .62, .4, .8))   # vignette
    return ('<svg xmlns="http://www.w3.org/2000/svg" width="1500" height="500" viewBox="0 0 1500 500">'
            '<defs>' + ''.join(defs) + '</defs>' + ''.join(out) + '</svg>')


if __name__ == '__main__':
    here = os.path.dirname(os.path.abspath(__file__))
    open(f'{here}/art/C-scene.svg', 'w').write(build())
    print('C scene ok')
