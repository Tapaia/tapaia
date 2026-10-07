"""Build the refined Tea & Chat variants (A-D) and the comparison sheet HTML.
Run ./render.sh (needs Pillow, cairosvg, headless Chrome)."""
import os, io
import cairosvg
from PIL import Image, ImageDraw
import vec, px

HERE = os.path.dirname(os.path.abspath(__file__))


def png(svg_text, size):
    return Image.open(io.BytesIO(cairosvg.svg2png(bytestring=svg_text.encode(), output_width=size, output_height=size))).convert('RGBA')


def scaled(body, k):
    return f'<g transform="translate(32 32) scale({k}) translate(-32 -32)">{body}</g>'


SQ = 'M0 18C0 4.5 4.5 0 18 0H46C59.5 0 64 4.5 64 18V46C64 59.5 59.5 64 46 64H18C4.5 64 0 59.5 0 46Z'   # squircle-ish

# ---------------------------------------------------------------- variant definitions
def B_body(k=1.1):
    return f'<circle cx="32" cy="32" r="32" fill="{vec.ROBE}"/>' + scaled(vec.content(dict(dot=vec.ROBE, tea=vec.GOLD)), k)


VARIANTS = {}

# A: refined pixel
gA = px.pixel_A(32)
VARIANTS['A-refined-pixel'] = dict(
    title='Refined Pixel', letter='A',
    why='The original, cleaned up: one cream shape language, no outlines, symmetric bubble, a gold tea line. Keeps the most pixel charm.',
    master=gA.svg(512), pixel32=gA, px16=px.pixel_A(16),
    app=None, pfp_bg='#24452a', app_bg=('#4f9442', '#2f5a2e'))

# B: clean flat vector
B_master = vec.svg(B_body())
VARIANTS['B-flat-vector'] = dict(
    title='Flat Vector', letter='B',
    why='Two colours plus a gold tea line, no outlines or effects. Reads instantly at any size and prints anywhere.',
    master=B_master, small=vec.svg(B_body(1.0)), px16=px.px16_B(),
    app=vec.svg(f'<path d="{SQ}" fill="{vec.ROBE}"/>' + scaled(vec.content(dict(dot=vec.ROBE, tea=vec.GOLD)), 1.2)),
    pfp=vec.svg(f'<rect width="64" height="64" fill="{vec.ROBE}"/>' + scaled(vec.content(dict(dot=vec.ROBE, tea=vec.GOLD)), 1.2)))

# C: premium coin
C_content = vec.content(dict(fill='url(#cream)', dot=vec.ROBE, tea=vec.GOLD, shadow='#1a0f26'))
VARIANTS['C-premium-coin'] = dict(
    title='Premium Coin', letter='C',
    why='A minted coin: the book\u2019s glowing green pay circle as a bevelled rim, a soft purple field, gently lit cream. The most \u201ctoken\u201d of the four.',
    master=vec.mark_C(), px16=px.px16_C(),
    app=vec.svg(f'<path d="{SQ}" fill="url(#field)"/><circle cx="32" cy="32" r="25.5" fill="none" stroke="url(#ring)" stroke-width="2.2" opacity=".9"/>'
                + scaled(C_content, 1.0), vec.DEFS_C),
    pfp=vec.svg(f'<rect width="64" height="64" fill="#17804a"/>' + vec.coin_C() + C_content, vec.DEFS_C))

# D: hybrid
D_content = vec.content(dict(dot=vec.ROBE_DK, tea=vec.GOLD, square_dots=True, bubble=vec.BUBBLE_STEP))
VARIANTS['D-hybrid'] = dict(
    title='Hybrid', letter='D',
    why='Flat, confident vector coin with a solid green pay-circle rim; pixel heritage lives in the square typing dots and the stepped steam.',
    master=vec.mark_D(), px16=px.px16_D(),
    app=vec.svg(f'<path d="{SQ}" fill="{vec.ROBE_DEEP}"/>' + scaled(vec.coin_D() + D_content, .8)),
    pfp=vec.svg(f'<rect width="64" height="64" fill="{vec.GLOW}"/>' + vec.coin_D() + D_content))


def pixel_app_icon(g, top, bot, size=512, k=12):
    t, b = Image.new('RGBA', (1, 2)), None
    bg = Image.new('RGBA', (size, size))
    d = ImageDraw.Draw(bg)
    hx = lambda c: tuple(int(c.lstrip('#')[i:i + 2], 16) for i in (0, 2, 4))
    T, B = hx(top), hx(bot)
    for y in range(size):
        f = y / (size - 1)
        d.line([(0, y), (size, y)], fill=tuple(round(T[i] + (B[i] - T[i]) * f) for i in range(3)) + (255,))
    mask = Image.new('L', (size * 4, size * 4), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, size * 4 - 1, size * 4 - 1], radius=int(size * 4 * .225), fill=255)
    out = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    out.paste(bg, (0, 0), mask.resize((size, size), Image.LANCZOS))
    m = g.image(k)
    o = (size - m.width) // 2
    out.alpha_composite(m, (o, o))
    return out


def build():
    for slug, v in VARIANTS.items():
        d = os.path.join(HERE, slug)
        os.makedirs(d, exist_ok=True)
        open(f'{d}/{slug}.svg', 'w').write(v['master'])
        open(f'{d}/{slug}-16.svg', 'w').write(v['px16'].svg(256))
        v['px16'].image(1).save(f'{d}/{slug}-16.png')
        if 'pixel32' in v:
            for s in (512, 256, 64, 32):
                v['pixel32'].image(s // 32).save(f'{d}/{slug}-{s}.png')
            v['pixel32'].image(1).resize((24, 24), Image.LANCZOS).save(f'{d}/{slug}-24.png')
            pixel_app_icon(v['pixel32'], *v['app_bg']).save(f'{d}/{slug}-app-icon-512.png')
            pixel_app_icon(v['pixel32'], *v['app_bg'], size=128, k=3).save(f'{d}/{slug}-app-icon-128.png')
            pf = Image.new('RGBA', (400, 400), v['pfp_bg'])
            m = v['pixel32'].image(12)
            pf.alpha_composite(m, (8, 8))
            pf.save(f'{d}/{slug}-x-pfp-400.png')
        else:
            for s in (512, 256):
                png(v['master'], s).save(f'{d}/{slug}-{s}.png')
            small = v.get('small', v['master'])     # optical sizing: grid-aligned drawing for 64/32
            if 'small' in v:
                open(f'{d}/{slug}-small.svg', 'w').write(small)
            for s in (64, 32, 24):
                png(small, s).save(f'{d}/{slug}-{s}.png')
            open(f'{d}/{slug}-app-icon.svg', 'w').write(v['app'])
            png(v['app'], 512).save(f'{d}/{slug}-app-icon-512.png')
            png(v['app'], 128).save(f'{d}/{slug}-app-icon-128.png')
            open(f'{d}/{slug}-x-pfp.svg', 'w').write(v['pfp'])
            png(v['pfp'], 400).save(f'{d}/{slug}-x-pfp-400.png')
        print('built', slug)


if __name__ == '__main__':
    build()
