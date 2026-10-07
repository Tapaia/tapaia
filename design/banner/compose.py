"""Compose the @TapaiaSquare X header variants (pixel scene + vector logo/type) and the X-profile preview mocks.
Run ./render.sh. Outputs land in this folder."""
import os
from PIL import Image
import scene_banner as sb

HERE = os.path.dirname(os.path.abspath(__file__))
COIN = '../logo/opt4-refined/C-premium-coin/C-premium-coin.svg'
PFP = '../logo/opt4-refined/D-hybrid/D-hybrid-x-pfp-400.png'
FONT = "@font-face { font-family: Inter; src: url('../mockups-v2/fonts/Inter-Variable.ttf') format('truetype'); font-weight: 100 900; }"


def scenes():
    os.makedirs(f'{HERE}/art', exist_ok=True)
    sb.render('day').save(f'{HERE}/art/scene-day.png')
    sb.render('dusk').save(f'{HERE}/art/scene-dusk.png')
    sb.render('dusk', sb.STRIP, sky=False).save(f'{HERE}/art/strip-dusk.png')


BASE_CSS = FONT + """
* { box-sizing: border-box; } html, body { margin: 0; }
body { width: 1500px; height: 500px; overflow: hidden; position: relative; font-family: Inter, sans-serif;
  -webkit-font-smoothing: antialiased; font-feature-settings: 'cv11','ss01'; }
.px { image-rendering: pixelated; position: absolute; left: 0; top: 0; width: 1500px; height: 500px; }
.lock { position: absolute; display: flex; align-items: center; gap: 30px; }
.lock img.coin { width: 150px; height: 150px; filter: drop-shadow(0 10px 22px rgba(30,12,48,.35)); }
.wm { font-weight: 800; font-size: 112px; letter-spacing: -.045em; line-height: .9; }
.tag { font-weight: 600; font-size: 31px; letter-spacing: -.01em; margin-top: 14px; }
.tag b { font-weight: 800; }
"""

VARIANTS = {
    'day': dict(name='Day in the Square', body="""
<img class="px" src="art/scene-day.png">
<div style="position:absolute;inset:0;background:radial-gradient(ellipse 560px 250px at 1135px 175px, rgba(255,251,240,.62), rgba(255,251,240,.28) 55%, rgba(255,251,240,0) 100%)"></div>
<div class="lock" style="right:70px;top:104px">
  <img class="coin" src="%COIN%">
  <div><div class="wm" style="color:#2e1a40">Tapaia</div>
  <div class="tag" style="color:#45275e">The town square for <b style="color:#5b3a86">$ZC</b></div></div>
</div>"""),
    'dusk': dict(name='Golden Hour', body="""
<img class="px" src="art/scene-dusk.png">
<div style="position:absolute;inset:0;background:radial-gradient(ellipse 600px 260px at 1130px 170px, rgba(36,18,56,.42), rgba(36,18,56,0) 100%)"></div>
<div class="lock" style="right:70px;top:104px">
  <img class="coin" src="%COIN%">
  <div><div class="wm" style="color:#fff8ec;text-shadow:0 4px 24px rgba(30,10,40,.45)">Tapaia</div>
  <div class="tag" style="color:#ffe2a8;text-shadow:0 2px 12px rgba(30,10,40,.5)">The town square for <b style="color:#ffd95a">$ZC</b></div></div>
</div>"""),
    'clean': dict(name='Clean + Scene Strip', body="""
<div style="position:absolute;inset:0;background:radial-gradient(ellipse 900px 420px at 760px 120px, #6a4796 0%, #4a2d70 45%, #2e1a40 100%)"></div>
<div style="position:absolute;inset:0;background-image:radial-gradient(circle at 1px 1px, rgba(255,255,255,.07) 1px, transparent 1.5px);background-size:16px 16px;-webkit-mask-image:linear-gradient(#000, transparent 70%)"></div>
<div style="position:absolute;left:0;right:0;bottom:0;height:300px;background:linear-gradient(rgba(46,26,64,0), rgba(46,26,64,.0) 40%, rgba(30,16,42,.35))"></div>
<img class="px" src="art/strip-dusk.png">
<div style="position:absolute;inset:0;background:radial-gradient(ellipse 330px 150px at 750px 190px, rgba(47,197,106,.16), rgba(47,197,106,0) 100%)"></div>
<div class="lock" style="left:0;right:0;justify-content:center;top:92px">
  <img class="coin" src="%COIN%" style="width:140px;height:140px">
  <div><div class="wm" style="color:#fff8ec">Tapaia</div>
  <div class="tag" style="color:#d9cfe6">The town square for <b style="color:#2fc56a">$ZC</b></div></div>
</div>"""),
}


def banner_html(key):
    v = VARIANTS[key]
    return f'<!doctype html><html><head><meta charset="utf-8"><style>{BASE_CSS}</style></head><body>{v["body"].replace("%COIN%", COIN)}</body></html>'


BIO = ['The town square for $ZC 🌳', 'Chat • Role-play • Burn to be heard', 'Set in Veridia, from Snowmoon 📖', 'Open source | Not affiliated w/ Vitalik']


def profile(key, theme):
    dark = theme == 'dark'
    bg, fg, sub, line = ('#000', '#e7e9ea', '#71767b', '#2f3336') if dark else ('#fff', '#0f1419', '#536471', '#eff3f4')
    btn = 'background:#eff3f4;color:#0f1419' if dark else 'background:#0f1419;color:#fff'
    bio = '<br>'.join(BIO).replace('$ZC', f'<span style="color:#1d9bf0">$ZC</span>')
    return f'''<div class="xp" style="background:{bg};color:{fg};border-color:{line}">
  <div class="top" style="border-color:{line}"><span class="back">←</span><div><b>Tapaia</b><div style="color:{sub};font-size:13px">0 posts</div></div></div>
  <div class="hdr"><img src="banner-{key}.png"></div>
  <div class="pfprow"><img class="pfp" src="{PFP}" style="border-color:{bg}"><span class="follow" style="{btn}">Follow</span></div>
  <div class="who"><div class="nm">Tapaia</div><div style="color:{sub}">@TapaiaSquare</div></div>
  <div class="bio">{bio}</div>
  <div class="meta" style="color:{sub}">📅 Joined October 2026</div>
  <div class="meta" style="color:{sub}"><b style="color:{fg}">0</b> Following &nbsp; <b style="color:{fg}">0</b> Followers</div>
  <div class="tabs" style="border-color:{line};color:{sub}"><span class="on" style="color:{fg}">Posts</span><span>Replies</span><span>Media</span><span>Likes</span></div>
</div>'''


def preview_html(key):
    css = FONT + """
* { box-sizing: border-box; } html, body { margin: 0; }
body { width: 1280px; padding: 20px; background: #e9e4dc; display: flex; gap: 40px; font-family: 'Segoe UI', Inter, system-ui, sans-serif; -webkit-font-smoothing: antialiased; }
.xp { width: 600px; border-left: 1px solid; border-right: 1px solid; font-size: 15px; line-height: 20px; padding-bottom: 0; }
.top { height: 53px; display: flex; align-items: center; gap: 30px; padding: 0 16px; }
.top b { font-size: 20px; } .back { font-size: 20px; }
.hdr img { display: block; width: 600px; height: 200px; }
.pfprow { height: 68px; position: relative; display: flex; justify-content: flex-end; align-items: flex-start; padding: 12px 16px 0; }
.pfp { position: absolute; left: 16px; top: -67px; width: 134px; height: 134px; border-radius: 50%; border: 4px solid; }
.follow { font-weight: 700; padding: 0 16px; height: 36px; display: flex; align-items: center; border-radius: 18px; }
.who { padding: 4px 16px 0; } .nm { font-weight: 800; font-size: 20px; line-height: 24px; }
.bio { padding: 12px 16px 0; }
.meta { padding: 12px 16px 0; } .meta + .meta { padding-top: 10px; }
.tabs { margin-top: 16px; display: flex; justify-content: space-around; border-bottom: 1px solid; height: 53px; align-items: center; font-weight: 600; }
.tabs .on { border-bottom: 4px solid #1d9bf0; padding: 15px 0 12px; }
"""
    return f'<!doctype html><html><head><meta charset="utf-8"><style>{css}</style></head><body>{profile(key, "light")}{profile(key, "dark")}</body></html>'


if __name__ == '__main__':
    scenes()
    for k in VARIANTS:
        open(f'{HERE}/banner-{k}.html', 'w').write(banner_html(k))
        open(f'{HERE}/preview-{k}.html', 'w').write(preview_html(k))
    print('wrote html')
