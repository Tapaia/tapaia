"""Build all Tapaia logo option files + the comparison sheet.
Usage: python3 build_logo.py   (then render the sheet with ./render.sh)"""
import os
from PIL import Image, ImageDraw
from designs import OPTIONS, EXTRA

HERE = os.path.dirname(os.path.abspath(__file__))
APP_BG = {  # rounded-square app-icon backgrounds (top, bottom)
    'opt1-pay-circle-lamp': ('#3a2350', '#1f1229'),
    'opt1b-pay-circle-tree': ('#3a2350', '#1f1229'),
    'opt2-square-tree': ('#fbf1d6', '#ecd9ac'),
    'opt3-robe-hood': ('#4f9442', '#2f5a2e'),
    'opt4-tea-chat': ('#6a4796', '#45275e'),
}


def hx(c):
    c = c.lstrip('#')
    return tuple(int(c[i:i + 2], 16) for i in (0, 2, 4))


def app_icon(slug, mark32, size, k):
    top, bot = hx(APP_BG[slug][0]), hx(APP_BG[slug][1])
    bg = Image.new('RGBA', (size, size))
    d = ImageDraw.Draw(bg)
    for y in range(size):
        t = y / (size - 1)
        d.line([(0, y), (size, y)], fill=tuple(round(top[i] + (bot[i] - top[i]) * t) for i in range(3)) + (255,))
    mask = Image.new('L', (size * 4, size * 4), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, size * 4 - 1, size * 4 - 1], radius=int(size * 4 * .225), fill=255)
    mask = mask.resize((size, size), Image.LANCZOS)
    out = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    out.paste(bg, (0, 0), mask)
    m = mark32.image(k)
    o = (size - m.width) // 2
    shadow = Image.new('RGBA', m.size, (0, 0, 0, 0))
    shadow.paste(Image.new('RGBA', m.size, (20, 10, 30, 70)), (0, 0), m)
    out.alpha_composite(shadow, (o, o + max(1, k // 2)))
    out.alpha_composite(m, (o, o))
    return out


def build(slug, name, fn):
    d = os.path.join(HERE, slug)
    os.makedirs(d, exist_ok=True)
    g32, g16 = fn(32), fn(16)
    open(f'{d}/{slug}.svg', 'w').write(g32.svg(512))
    open(f'{d}/{slug}-16.svg', 'w').write(g16.svg(256))
    for s in (512, 256, 64, 32):
        g32.image(s // 32).save(f'{d}/{slug}-{s}.png')
    g16.image(1).save(f'{d}/{slug}-16.png')
    app_icon(slug, g32, 512, 12).save(f'{d}/{slug}-app-icon-512.png')
    app_icon(slug, g32, 128, 3).save(f'{d}/{slug}-app-icon-128.png')
    return d


if __name__ == '__main__':
    for o in OPTIONS + EXTRA:
        print('built', build(*o))
