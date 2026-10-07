"""Compose the three Golden Hour style studies (A cozy HD pixel, B painterly pixel, C illustrated flat):
scene art + the C premium coin + Inter wordmark, 1500x500 (@2x via Chrome scale 2), plus X-profile previews.
The wordmark CSS (Inter 800 / 112px / -.045em, tagline 600 / 31px) is unchanged from ../compose.py.
Integration: the coin IS the setting sun. Every scene centres its sun, sky glow, cloud rims, rays and
paving reflection on the coin centre (975,179), so the lockup is lit by the scene rather than pasted on."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import compose as base  # reuse the X-profile mock (BIO, layout) from the main banner set

COIN = '../../logo/opt4-refined/C-premium-coin/C-premium-coin.svg'
PFP = '../../logo/opt4-refined/D-hybrid/D-hybrid-x-pfp-400.png'
FONT = "@font-face { font-family: Inter; src: url('../../mockups-v2/fonts/Inter-Variable.ttf') format('truetype'); font-weight: 100 900; }"

CSS = FONT + """
* { box-sizing: border-box; } html, body { margin: 0; }
body { width: 1500px; height: 500px; overflow: hidden; position: relative; font-family: Inter, sans-serif;
  -webkit-font-smoothing: antialiased; font-feature-settings: 'cv11','ss01'; }
.bg { position: absolute; left: 0; top: 0; width: 1500px; height: 500px; }
.px { image-rendering: pixelated; }
.lock { position: absolute; display: flex; align-items: center; gap: 30px; left: 900px; top: 104px; }
.cw { position: relative; width: 150px; height: 150px; flex: none; }
.cw img.coin { width: 150px; height: 150px; display: block; }
/* the coin sits in the sunset: warm sheen from the glow behind it, plum occlusion on the far side */
.cw .sheen { position: absolute; inset: 3px; border-radius: 50%; mix-blend-mode: screen;
  background: radial-gradient(circle at 72% 22%, rgba(255,214,150,.42), rgba(255,214,150,0) 46%); }
.cw .occl { position: absolute; inset: 3px; border-radius: 50%; mix-blend-mode: multiply;
  background: radial-gradient(circle at 28% 88%, rgba(120,52,110,.30), rgba(120,52,110,0) 55%); }
.wm { font-weight: 800; font-size: 112px; letter-spacing: -.045em; line-height: .9; }
.tag { font-weight: 600; font-size: 31px; letter-spacing: -.01em; margin-top: 14px; }
.tag b { font-weight: 800; }
"""

# the sun (coin) sits behind/in front of the glow; coin filter = halo of the scene's own sun colours
STYLES = {
    'A': dict(slug='A-golden-hour-hd', name='A · Cozy HD pixel', bg='art/A-scene-750x250.png', px=True,
              coin='drop-shadow(0 0 10px rgba(255,240,190,.95)) drop-shadow(0 0 34px rgba(255,196,110,.75)) drop-shadow(0 0 80px rgba(255,140,90,.45))',
              wm='#2a1640', wm_sh='-2px 0 0 rgba(255,232,176,.55), 0 0 34px rgba(255,226,160,.55)',
              tag='#3a1f52', tag_sh='0 0 18px rgba(255,226,160,.6)', zc='#6b2f86'),
    'B': dict(slug='B-golden-hour-painterly', name='B · Painterly pixel', bg='art/B-scene-1500x500.png', px=True,
              coin='drop-shadow(0 0 10px rgba(255,240,190,.95)) drop-shadow(0 0 40px rgba(255,196,110,.8)) drop-shadow(0 0 100px rgba(255,140,90,.5))',
              wm='#2a1640', wm_sh='-2px 0 0 rgba(255,232,176,.5), 0 0 40px rgba(255,226,160,.6)',
              tag='#3a1f52', tag_sh='0 0 18px rgba(255,226,160,.6)', zc='#6b2f86'),
    'C': dict(slug='C-golden-hour-illustrated', name='C · Illustrated flat', bg='art/C-scene.svg', px=False,
              coin='drop-shadow(0 0 8px rgba(255,240,190,.9)) drop-shadow(0 0 36px rgba(255,190,110,.7)) drop-shadow(0 0 90px rgba(255,140,90,.4))',
              wm='#2a1640', wm_sh='-2px 0 0 rgba(255,232,176,.45), 0 0 30px rgba(255,226,160,.5)',
              tag='#3a1f52', tag_sh='0 0 16px rgba(255,226,160,.55)', zc='#6b2f86'),
}


def banner_html(k):
    s = STYLES[k]
    return f'''<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body>
<img class="bg{' px' if s['px'] else ''}" src="{s['bg']}">
<div class="lock">
  <div class="cw"><img class="coin" src="{COIN}" style="filter:{s['coin']}"><div class="occl"></div><div class="sheen"></div></div>
  <div><div class="wm" style="color:{s['wm']};text-shadow:{s['wm_sh']}">Tapaia</div>
  <div class="tag" style="color:{s['tag']};text-shadow:{s['tag_sh']}">The town square for <b style="color:{s['zc']}">$ZC</b></div></div>
</div></body></html>'''


def preview_html(k):
    slug = STYLES[k]['slug']
    html = base.preview_html('X').replace('../mockups-v2/', '../../mockups-v2/').replace(base.PFP, PFP)
    return html.replace('banner-X.png', f'{slug}.png')


if __name__ == '__main__':
    for k in (sys.argv[1:] or STYLES):
        s = STYLES[k]
        open(f'{HERE}/{s["slug"]}.html', 'w').write(banner_html(k))
        open(f'{HERE}/{s["slug"]}-preview.html', 'w').write(preview_html(k))
        print(s['slug'])
