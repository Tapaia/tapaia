"""The four Tapaia logo options, each drawn on a 32x32 master grid and a hand-tuned 16x16 small-size grid.
All art is original; colours come from design/visual-reference.md and mockups-v2/app.css."""
from pixel import Grid, circle, ellipse, rect, edge, lit, shift, disc, coin, N4, N8

# palette (visual-reference.md / app.css)
ROBE = dict(d='#23142f', k='#2e1a40', m='#45275e', b='#5b3a86', l='#64408a', h='#8a64b0', x='#a98bcc')
LEAF = dict(d='#24452a', k='#2f5a2e', m='#3f7a37', l='#5c9a3e', h='#8cc152')
GLOW = dict(d='#17663a', m='#2fc56a', g='#39e07a', h='#a8ffbf')
GOLD = dict(d='#7a4d0c', k='#b9851a', m='#e0a526', l='#ffd95a', h='#ffe9a8')
SILK = dict(m='#d9cfe6', d='#a99bc2', w='#f7f3fb')
WOOD = dict(d='#3e2415', k='#6b3f1f', m='#9a6235', l='#c98d4f')
PARCH = dict(w='#fbf1d6', m='#f4e4bc', d='#e8cf98', k='#c9a96e')


# ---------------------------------------------------------------- 1. green pay circle + lamp
LAMP32 = [
    ".....pp.....",
    "....pwwp....",
    "...pwwwwp...",
    "..pwwwwwwp..",
    ".pppppppppp.",
    ".dddddddddd.",
    "..dHHlllld..",
    "..dHllllmd..",
    "..dHllllmd..",
    "..dlllllmd..",
    "..dllllmmd..",
    "..dlllmmmd..",
    ".dddddddddd.",
    "...ddppdd...",
    ".....pd.....",
    ".....pd.....",
    ".....pd.....",
    ".....pd.....",
    ".....pd.....",
    ".....pd.....",
    "....ppdd....",
    "...pppddd...",
]
LAMP16 = [
    ".pp.",
    "pppp",
    "dlld",
    "dlmd",
    ".pd.",
    ".pd.",
    ".pd.",
    "ppdd",
]


def opt1(n):
    g = Grid(n)
    D = disc(n)
    lamp_leg = dict(p=SILK['m'], w=SILK['w'], d=SILK['d'], H=GOLD['h'], l=GOLD['l'], m=GOLD['m'])
    if n == 32:
        inner = coin(g, D, GLOW['d'], GLOW['m'], GLOW['h'], '#21a356', rim=2)
        g.fill(inner, ROBE['k'])
        g.fill(edge(inner, N8), '#24493f')                 # green light spilling inward
        halo2 = circle(16, 13, 8.5) & inner - edge(inner, N8)
        halo1 = circle(16, 13, 6) & inner
        g.fill(halo2, '#3a2350').fill(halo1, '#4a2d66')
        g.fill(rect(11, 27, 10, 1) & inner, '#24152f')       # ground shadow
        g.sprite(LAMP32, lamp_leg, 10, 5, clip=inner)
    else:
        inner = coin(g, D, GLOW['d'], GLOW['m'], GLOW['h'], '#21a356', rim=1)
        g.fill(inner, ROBE['k'])
        g.fill(circle(8, 6, 3.2) & inner, '#4a2d66')
        g.sprite(LAMP16, lamp_leg, 6, 4, clip=inner)
    return g


# ---------------------------------------------------------------- 2. Tapaia Square tree on robe-purple disc
def canopy(g, lobes, clip, outline=True, hl=True):
    union = set()
    for cx, cy, r in lobes:
        union |= circle(cx, cy, r)
    union &= clip
    g.fill(union, LEAF['m'])
    g.fill(lit(union, 2, (1, 1)) | lit(union, 1, (1, 1)), LEAF['k'])
    if hl:
        for cx, cy, r in lobes:
            g.fill(circle(cx - r * .3, cy - r * .3, r * .5) & union - lit(union, 1, (1, 1)), LEAF['l'])
        for cx, cy, r in lobes:
            if cy < 15:
                g.fill(circle(cx - r * .42, cy - r * .42, r * .22) & union, LEAF['h'])
    if outline:
        g.fill(edge(union, N4), LEAF['d'])
    return union


def opt2(n):
    g = Grid(n)
    D = disc(n)
    if n == 32:
        inner = coin(g, D, ROBE['d'], ROBE['b'], ROBE['h'], ROBE['m'], rim=1)
        g.fill(ellipse(16, 26.5, 8.5, 1.6) & inner, ROBE['m'])             # shade under the tree
        trunk = rect(14, 18, 4, 9) | rect(13, 25, 6, 2)
        g.fill(trunk, WOOD['m']).fill(lit(trunk, 1, (1, 0)) | rect(16, 18, 2, 3), WOOD['k'])
        g.fill(edge(trunk, N4) - rect(14, 18, 4, 2), WOOD['d'])
        canopy(g, [(10.5, 15, 5.2), (21.5, 15, 5.2), (16, 9.5, 6.8), (16, 15.5, 5.5)], inner)
    else:
        inner = coin(g, D, ROBE['d'], ROBE['b'], ROBE['h'], ROBE['m'], rim=0)
        trunk = rect(7, 9, 2, 5)
        g.fill(trunk, WOOD['m']).fill({(8, 9), (8, 10), (8, 11), (8, 12), (8, 13)}, WOOD['k'])
        u = canopy(g, [(8, 5.6, 3.9), (5.4, 8, 2.6), (10.6, 8, 2.6)], inner, outline=False, hl=False)
        g.fill({(6, 4), (7, 3), (6, 3), (4, 7)} & u, LEAF['h'])
        g.fill({(7, 4), (5, 5), (8, 3), (5, 8), (9, 6)} & u, LEAF['l'])
    return g


# ---------------------------------------------------------------- 3. hooded privacy-robe mascot on lamp-gold disc
def opt3(n):
    g = Grid(n)
    D = disc(n)
    if n == 32:
        inner = coin(g, D, GOLD['d'], '#f2c84b', GOLD['h'], GOLD['m'], rim=1)
        body = (ellipse(16, 33, 13, 9) | ellipse(16, 14, 9.5, 10) | ellipse(16, 6.5, 3, 4.5)) & D
        hood = body
        g.fill(hood, ROBE['l'])
        g.fill(lit(hood, 1, (1, 1)) | lit(hood, 2, (1, 1)), ROBE['m'])
        g.fill(lit(hood, 1, (-1, -1)), ROBE['h'])
        # fold line between hood and shoulders
        g.fill((ellipse(16, 33, 13, 9) & D) - ellipse(16, 14, 9.5, 10), ROBE['b'])
        g.fill({(15, 25), (16, 25), (15, 26), (16, 26), (15, 27), (16, 27), (15, 28), (16, 28), (15, 29), (16, 29), (15, 30), (16, 30)}, ROBE['m'])
        face = ellipse(16, 15.5, 6.5, 6)
        g.fill(edge(face | shift(face, 0, -1), N8) - face, ROBE['m'])   # hood depth around the opening
        g.fill(face, '#170c22')
        g.fill(rect(10, 17, 12, 4) & face, ROBE['m'])                    # face cover (below the nose)
        g.fill(rect(10, 16, 12, 1) & face, SILK['m'])                    # the nose strap
        for ex in (12, 18):
            g.fill(rect(ex, 13, 2, 2), GLOW['h'])
            g.fill({(ex, 13)}, '#ffffff')
        g.fill(edge(body, N4) - edge(D, N8), ROBE['d'])
        g.fill(edge(D, N8) & body, GOLD['d'])
    else:
        inner = coin(g, D, GOLD['d'], '#f2c84b', GOLD['h'], GOLD['m'], rim=0)
        body = (ellipse(8, 16.5, 6.5, 4.5) | ellipse(8, 7.5, 4.6, 5) | ellipse(8, 4, 1.2, 1.4)) & (inner | {(x, y) for x in range(16) for y in range(11, 16)}) & D
        g.fill(body, ROBE['l'])
        g.fill(lit(body, 1, (-1, -1)), ROBE['h'])
        face = rect(5, 6, 6, 4) - {(5, 6), (10, 6), (5, 9), (10, 9)}
        g.fill(face, '#170c22')
        g.fill(rect(5, 8, 6, 1) & face, SILK['m'])
        g.fill(rect(5, 9, 6, 1) & face, ROBE['m'])
        g.fill({(6, 7), (9, 7)}, GLOW['h'])
        g.fill(edge(body, N4) - edge(D, N8), ROBE['d'])
        g.fill(edge(D, N8) & body, GOLD['d'])
    return g


# ---------------------------------------------------------------- 4. tea cup whose steam is a chat bubble
def rrect(x0, y0, w, h, cut=1):
    m = rect(x0, y0, w, h)
    for i in range(cut):
        k = cut - i
        for x in range(k):
            m -= {(x0 + x, y0 + i), (x0 + w - 1 - x, y0 + i), (x0 + x, y0 + h - 1 - i), (x0 + w - 1 - x, y0 + h - 1 - i)}
    return m


def dilate(m, nb=N4):
    return m | {(x + dx, y + dy) for x, y in m for dx, dy in nb}


TEA16 = [
    "................",
    "................",
    ".....wwwwwww....",
    "....wwwwwwwws...",
    "....wwpwpwpws...",
    "....wwwwwwwws...",
    ".....wwwwwss....",
    "......ws........",
    "................",
    "...wtttttw......",
    "...wwwwwwsss....",
    "...wwwwwws.s....",
    "....wwwwsss.....",
    "..wwwwwwwwwss...",
    "....kkkkkkk.....",
    "................",
]


def opt4(n):
    g = Grid(n)
    D = disc(n)
    CREAM, SH, SH2, OUT = PARCH['w'], PARCH['d'], PARCH['k'], '#1c3a20'
    if n == 32:
        inner = coin(g, D, LEAF['d'], LEAF['m'], LEAF['l'], LEAF['k'], rim=1)
        bubble = rrect(8, 4, 16, 9, 2) | {(11, 13), (12, 13), (11, 14)}
        steam = {(12, 16), (11, 15)}
        cup = rrect(8, 17, 13, 8, 0) - {(8, 23), (8, 24), (9, 24), (20, 23), (20, 24), (19, 24)}
        handle = {(21, 18), (22, 18), (23, 19), (23, 20), (23, 21), (22, 22), (21, 22)}
        saucer = rect(5, 25, 20, 1) | rect(7, 26, 16, 1)
        shape = bubble | steam | cup | handle | saucer
        g.fill(dilate(shape) & inner, OUT)
        g.fill(shape, CREAM)
        g.fill({(x, y) for x, y in bubble if y == 12 or x == 23 or (x, y) in {(22, 11), (11, 14), (12, 13)}} & bubble, SH)
        for dx in (11, 15, 19):
            g.fill(rect(dx, 7, 2, 2), ROBE['b'])
        g.fill(rect(9, 17, 11, 1), WOOD['m'])            # tea surface
        g.fill(rect(10, 17, 4, 1), WOOD['l'])
        g.fill(rect(8, 20, 13, 2) & cup, ROBE['b'])       # robe-purple band on the cup
        g.fill({(x, 20) for x in range(8, 21)} & cup, ROBE['l'])
        g.fill({(x, y) for x, y in cup if x >= 18 and y not in (20, 21)} | {(x, 24) for x in range(10, 19)}, SH)
        g.fill({(22, 22), (23, 21)} | rect(7, 26, 16, 1) | {(24, 25)}, SH)
        g.fill(rect(10, 26, 10, 1), SH2)
    else:
        inner = coin(g, D, LEAF['d'], LEAF['m'], LEAF['l'], LEAF['k'], rim=0)
        g.sprite(TEA16, dict(w=CREAM, s=SH, p=ROBE['b'], t=WOOD['m'], b=ROBE['b'], k=SH2), 0, 0, clip=inner)
    return g


def opt1b(n):
    g = Grid(n)
    D = disc(n)
    if n == 32:
        inner = coin(g, D, GLOW['d'], GLOW['m'], GLOW['h'], '#21a356', rim=2)
        g.fill(inner, ROBE['k'])
        g.fill(edge(inner, N8), '#24493f')
        g.fill(ellipse(16, 26.5, 7, 1.4) & inner, '#24152f')
        trunk = rect(14, 19, 4, 8)
        g.fill(trunk, WOOD['m']).fill(lit(trunk, 1, (1, 0)) | rect(16, 19, 2, 2), WOOD['k'])
        canopy(g, [(11.5, 15, 4.3), (20.5, 15, 4.3), (16, 10.5, 5.8), (16, 15.5, 4.8)], inner)
    else:
        inner = coin(g, D, GLOW['d'], GLOW['m'], GLOW['h'], '#21a356', rim=1)
        g.fill(inner, ROBE['k'])
        g.fill(rect(7, 9, 2, 4), WOOD['m']).fill({(8, 9), (8, 10), (8, 11), (8, 12)}, WOOD['k'])
        u = canopy(g, [(8, 6, 3.1), (6, 8, 2), (10, 8, 2)], inner, outline=False, hl=False)
        g.fill({(6, 5), (7, 4), (5, 7)} & u, LEAF['h'])
    return g


OPTIONS = [
    ('opt1-pay-circle-lamp', 'Green Pay Circle + Lamp', opt1),
    ('opt2-square-tree', 'Square Tree', opt2),
    ('opt3-robe-hood', 'Robe Hood', opt3),
    ('opt4-tea-chat', 'Tea & Chat', opt4),
]
EXTRA = [('opt1b-pay-circle-tree', 'Green Pay Circle + Tree (alt of 1)', opt1b)]
