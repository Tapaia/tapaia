"""Side-by-side sheet of the three Golden Hour style studies (full size + as seen on an X profile)."""
import os
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__))
FONT = os.path.join(HERE, '../../mockups-v2/fonts/Inter-Variable.ttf')
PFP = os.path.join(HERE, '../../logo/opt4-refined/D-hybrid/D-hybrid-x-pfp-400.png')
STUDIES = [('A-golden-hour-hd', 'A · Cozy HD pixel', '750x250 hand-placed pixel art shown at 2x: dithered sky, rim light, haze, volumetric lamps'),
           ('B-golden-hour-painterly', 'B · Painterly pixel', 'crisp pixel town over a soft painted sky + mountain: depth of field, light shafts, bloom'),
           ('C-golden-hour-illustrated', 'C · Illustrated flat', 'vector illustration, no pixel grid: soft gradients, same palette + composition')]


def font(sz, wght):
    f = ImageFont.truetype(FONT, sz)
    try:
        f.set_variation_by_axes([min(32, max(14, sz)), wght])
    except Exception:
        pass
    return f


def main():
    pad, gap = 50, 34
    W = 1500 + pad * 2
    thumb_w, thumb_h = (1500 - 2 * 30) // 3, (1500 - 2 * 30) // 9
    H = 120 + len(STUDIES) * (500 + 70 + gap) + 60 + thumb_h + 110
    sheet = Image.new('RGB', (W, H), '#f3ede4')
    d = ImageDraw.Draw(sheet)
    d.text((pad, 40), 'Tapaia · Golden Hour · style studies', fill='#2a1640', font=font(40, 800))
    y = 120
    pfp = Image.open(PFP).convert('RGBA')
    for slug, name, note in STUDIES:
        d.text((pad, y), name, fill='#2a1640', font=font(30, 800))
        d.text((pad + 330, y + 8), note, fill='#6a5a78', font=font(20, 500))
        im = Image.open(os.path.join(HERE, f'{slug}.png')).convert('RGB')
        sheet.paste(im, (pad, y + 50))
        y += 500 + 70 + gap
    d.text((pad, y), 'As seen on X (desktop header scale, with profile picture)', fill='#2a1640', font=font(26, 700))
    y += 50
    for i, (slug, name, _) in enumerate(STUDIES):
        im = Image.open(os.path.join(HERE, f'{slug}.png')).convert('RGB').resize((thumb_w, thumb_h), Image.LANCZOS)
        x = pad + i * (thumb_w + 30)
        sheet.paste(im, (x, y))
        pr = int(thumb_h * 134 / 200)
        p = pfp.resize((pr, pr), Image.LANCZOS)
        m = Image.new('L', (pr, pr), 0); ImageDraw.Draw(m).ellipse([0, 0, pr - 1, pr - 1], fill=255)
        bx = int(x + thumb_w * 16 / 600); by = int(y + thumb_h - pr / 2)
        ImageDraw.Draw(sheet).ellipse([bx - 3, by - 3, bx + pr + 2, by + pr + 2], fill='#f3ede4')
        sheet.paste(p, (bx, by), m)
        d.text((x + pr + 30, y + thumb_h + 12), name, fill='#2a1640', font=font(20, 700))
    sheet.save(os.path.join(HERE, 'comparison.png'))
    print('comparison ok')


if __name__ == '__main__':
    main()
