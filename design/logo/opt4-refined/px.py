"""Pixel versions: A (refined pixel master, 32 grid) and the hand-tuned 16px grids for A-D."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from pixel import Grid, disc, edge, rect, N8  # noqa: E402

CREAM, SH = '#fbf1d6', '#e6d3a8'
ROBE, ROBE_DK, GOLD, GLOW = '#5b3a86', '#45275e', '#e0a526', '#2fc56a'
LEAF, LEAF_DK, LEAF_DKK = '#3f7a37', '#2f5a2e', '#24452a'

# A: refined pixel master (32x32). w cream, s cream shade, t tea, d dots
A32 = [
    "................................",
    "................................",
    "................................",
    "................................",
    "................................",
    "................................",
    "..........wwwwwwwwwwww..........",
    ".........wwwwwwwwwwwwww.........",
    ".........wwwwwwwwwwwwws.........",
    ".........wwddwwddwwddws.........",
    ".........wwddwwddwwddws.........",
    ".........wwwwwwwwwwwwws.........",
    ".........wwwwwwwwwwwwss.........",
    "..........wwwwssssssss..........",
    "...........ws...................",
    "..........ws....................",
    "................................",
    ".........wttttttttttw...........",
    ".........wwwwwwwwwwwwwww........",
    ".........wwwwwwwwwwwws..ws......",
    ".........wwwwwwwwwwwws..ws......",
    ".........wwwwwwwwwwwws..ws......",
    "..........wwwwwwwwwwswws........",
    "...........wwwwwwwwss...........",
    "............wwwwwss.............",
    "................................",
    "........wwwwwwwwwwwwwwwss.......",
    "................................",
    "................................",
    "................................",
    "................................",
    "................................",
]

# 16px hand-tuned art shared by all variants (k = saucer shade)
T16 = [
    "................",
    "................",
    ".....wwwwwww....",
    "....wwdwdwdww...",
    ".....wwwwwww....",
    ".....w..........",
    "....w...........",
    "................",
    "....wtttttw.....",
    "....wwwwwwwww...",
    "....wwwwwww.w...",
    ".....wwwwwww....",
    "................",
    "....wwwwwwwww...",
    "................",
    "................",
]
T16_D = T16


def pixel_A(n):
    g = Grid(n)
    D = disc(n)
    g.fill(D, LEAF)
    g.fill(edge(D, N8), LEAF_DKK)
    if n == 32:
        g.fill(edge(D - edge(D, N8), N8) & {(x, y) for x, y in D if x + y < 30}, '#4a8a40')
        g.sprite(A32, dict(w=CREAM, s=SH, t=GOLD, d=ROBE), 0, 0)
    else:
        g.sprite(T16, dict(w=CREAM, s=SH, t=GOLD, d=ROBE, k=SH), 0, 0)
    return g


def px16_B():
    g = Grid(16)
    D = disc(16)
    g.fill(D, ROBE)
    g.sprite(T16, dict(w=CREAM, s=CREAM, t=GOLD, d=ROBE, k=CREAM), 0, 0)
    return g


def px16_C():
    g = Grid(16)
    D = disc(16)
    g.fill(D, ROBE)
    e = edge(D, N8)
    g.fill(e, GLOW)
    g.fill({p for p in e if p[0] + p[1] > 17}, '#1f9a50')
    g.fill({p for p in e if p[0] + p[1] < 12}, '#7ff0a8')
    g.sprite(T16, dict(w=CREAM, s=SH, t=GOLD, d=ROBE, k=SH), 0, 0)
    return g


def px16_D():
    g = Grid(16)
    D = disc(16)
    g.fill(D, ROBE_DK)
    g.fill(edge(D, N8), GLOW)
    g.sprite(T16_D, dict(w=CREAM, s=CREAM, t=GOLD, d=ROBE_DK, k=CREAM), 0, 0)
    return g
