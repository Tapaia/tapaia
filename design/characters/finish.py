"""Post-process the Chrome screenshots: trim the page background, stitch the phone pair, phone-size previews."""
import os, sys
from PIL import Image, ImageChops, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__))
FONT = os.path.join(HERE, '..', 'mockups-v2', 'fonts', 'Inter-Variable.ttf')
BG = (239, 233, 224)


def trim(path, pad=24):
    im = Image.open(path).convert('RGB')
    diff = ImageChops.difference(im, Image.new('RGB', im.size, BG)).getbbox()
    if diff:
        im = im.crop((0, 0, im.width, min(im.height, diff[3] + pad)))
    im.save(path)
    return im


def phone_pair(before, after, out):
    a, b = Image.open(before).convert('RGB'), Image.open(after).convert('RGB')
    gap = 90
    W = Image.new('RGB', (a.width + b.width + gap * 3, a.height + 150), BG)
    d = ImageDraw.Draw(W)
    f = ImageFont.truetype(FONT, 54); f.set_variation_by_axes([32, 750])
    g = ImageFont.truetype(FONT, 34); g.set_variation_by_axes([20, 500])
    d.text((gap, 34), 'Phone (390 pt, 3x density): current vs new', font=f, fill=(46, 26, 64))
    W.paste(a, (gap, 130)); W.paste(b, (gap * 2 + a.width, 130))
    W = W.crop((0, 0, W.width, ImageChops.difference(W, Image.new('RGB', W.size, BG)).getbbox()[3] + 40))
    W.save(out)
    # what it looks like held at arm's length: the same image at 1/3 (1 CSS px per px)
    W.resize((W.width // 3, W.height // 3), Image.LANCZOS).save(out.replace('.png', '-1x.png'))


if __name__ == '__main__':
    trim(f'{HERE}/comparison.png')
    trim(f'{HERE}/comparison@2x.png', 48)
    for p in ('before', 'after'):
        trim(f'/tmp/tapaia-phone-{p}.png', 30)
    phone_pair('/tmp/tapaia-phone-before.png', '/tmp/tapaia-phone-after.png', f'{HERE}/comparison-phone.png')
    print('finished screenshots')
