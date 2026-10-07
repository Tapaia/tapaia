"""Build every pixel asset for the Tapaia mockups. Run: python3 build_art.py"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from sprites import avatar, icon, ICONS, wallet_icon, WALLET_ICONS, mini
from scene import draw_scene, HEADER, LANDING

OUT = os.path.join(os.path.dirname(__file__), '..', 'assets')
os.makedirs(OUT, exist_ok=True)

draw_scene(410, 48, HEADER).save(f'{OUT}/scene-header.png')
draw_scene(320, 200, LANDING).save(f'{OUT}/scene-landing.png')
for n in ICONS:
    icon(n).save(f'{OUT}/icon-{n}.png')
for n in WALLET_ICONS:
    wallet_icon(n).save(f'{OUT}/wallet-{n}.png')

AVATARS = {
    # fictional original citizens (no canon characters)
    'corvin':  dict(outfit='robe', skin='warm', hair='chestnut'),
    'nessa':   dict(outfit='robe', skin='fair', hair='ginger', hairstyle='long'),
    'pim':     dict(outfit='shirt', skin='tan', hair='black', shirt='#f2c84b', band=False),
    'tobin':   dict(outfit='robe', hood=True, skin='warm'),
    'wren':    dict(outfit='robe', skin='deep', hair='black', hairstyle='bun'),
    'odessa':  dict(outfit='shirt', skin='fair', hair='silver', shirt='#5c9a3e', band=True),
    'ilse':    dict(outfit='robe', skin='tan', hair='plum', hairstyle='long'),
    'juniper': dict(outfit='shirt', skin='deep', hair='black', shirt='#64408a', slogan=True, band=False),
    'marek':   dict(outfit='robe', hood=True, skin='fair'),
    'bram':    dict(outfit='shirt', skin='warm', hair='blonde', shirt='#3f6fd8', band=False),
    'orla':    dict(outfit='robe', skin='fair', hair='blonde', hairstyle='bun'),
    'sorrel':  dict(outfit='shirt', skin='tan', hair='ginger', shirt='#c8452e', band=True),
    'lumi':    dict(outfit='robe', skin='warm', hair='silver', band=False),
    'builder': dict(outfit='robe', skin='warm', hair='plum', hairstyle='long'),
    'team':    dict(outfit='shirt', skin='warm', hair='chestnut', shirt='#2f5a2e', band=True),
}
for name, kw in AVATARS.items():
    av = avatar(**kw)
    av.save(f'{OUT}/av-{name}.png')
    av.crop((0, 0, 16, 16)).save(f'{OUT}/bust-{name}.png')

# builder option previews
opts = {
    'robe-down': dict(outfit='robe', skin='warm', hair='plum', hairstyle='long'),
    'robe-up': dict(outfit='robe', hood=True, skin='warm'),
    'shirt-plain': dict(outfit='shirt', skin='warm', hair='plum', hairstyle='long', shirt='#5c9a3e', band=False),
    'shirt-band': dict(outfit='shirt', skin='warm', hair='plum', hairstyle='long', shirt='#2e2630', slogan=True, band=False),
}
for name, kw in opts.items():
    avatar(**kw).save(f'{OUT}/opt-{name}.png')

# ---- UI tiles (design choice: cozy wood + grass, original)
import random
from PIL import Image
from sprites import hex2rgba
rnd = random.Random(3)
g = Image.new('RGBA', (16, 16), hex2rgba('#2f5a2e')); px = g.load()
for _ in range(40):
    x, y = rnd.randrange(16), rnd.randrange(16)
    px[x, y] = hex2rgba(rnd.choice(['#24452a', '#3f7a37', '#3f7a37', '#5c9a3e']))
for x, y in [(3, 4), (11, 12), (7, 9)]:
    px[x, y] = hex2rgba('#5c9a3e'); px[x, y - 1] = hex2rgba('#8cc152')
g.save(f'{OUT}/tile-grass.png')

# 9-slice wood frame, 15x15 with 5px edges: outline, highlight, grain, brass rivets in corners
W = ['#3e2415', '#6b3f1f', '#9a6235', '#c98d4f', '#e2ad6c']
f = Image.new('RGBA', (15, 15), (0, 0, 0, 0)); fp = f.load()
for y in range(15):
    for x in range(15):
        edge = min(x, y, 14 - x, 14 - y)
        if edge >= 5:
            continue
        col = [W[0], W[3], W[2], W[2], W[1]][edge]
        if edge in (2, 3) and ((x + 2 * y) % 5 == 0):
            col = W[1]
        if edge == 1 and (x > 13 - 1 or y > 13 - 1):
            col = W[1]
        fp[x, y] = hex2rgba(col)
for cx, cy in [(2, 2), (12, 2), (2, 12), (12, 12)]:
    fp[cx, cy] = hex2rgba('#ffd95a'); fp[cx + 1, cy + 1] = hex2rgba('#9c6a17') if cx < 12 and cy < 12 else fp[cx, cy]
f.save(f'{OUT}/frame-wood.png')

# wood plank tile for toolbars
t = Image.new('RGBA', (32, 8), hex2rgba(W[2])); tp = t.load()
for x in range(32):
    tp[x, 0] = hex2rgba(W[3]); tp[x, 7] = hex2rgba(W[1])
    if (x * 7) % 11 == 0:
        tp[x, 3] = hex2rgba(W[1])
    if (x * 5) % 13 == 0:
        tp[x, 5] = hex2rgba(W[3])
tp[0, 1] = tp[0, 2] = tp[0, 3] = tp[0, 4] = tp[0, 5] = tp[0, 6] = hex2rgba(W[1])
t.save(f'{OUT}/tile-plank.png')
print('assets written to', os.path.abspath(OUT))
