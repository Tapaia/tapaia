"""Before / after comparison in the real app UI: the chat feed rows, the arrival card and the Tapaia Square banner,
using the prototype's own stylesheets (../../app/src/styles, read only) at the app's real CSS sizes.
'Before' avatars come from the live renderer's source (design/mockups/art/sprites.py = shared/avatar.ts);
'after' from charkit. Screenshots via headless Chrome (render.sh)."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, '..', 'mockups', 'art'))
sys.dont_write_bytecode = True
from sprites import avatar as old_avatar   # noqa: E402
import charkit as K                         # noqa: E402
import citizens                             # noqa: E402

A = os.path.join(HERE, 'art', 'compare')
os.makedirs(A, exist_ok=True)
CAST = {n: c for n, _, c in citizens.CAST}
CLASSES = {'Orla Fenwick': 'c3', 'Alder Meadows': 'c1', 'Nessa Quill': 'c5', 'Tobin Larkspur': 'c4', 'Wren Halloway': 'c2', 'Odessa Brightmoss': 'c6'}


def old_cfg(c):
    """New config -> closest current-app AvatarCfg (the inverse of the migration table in the README)."""
    skin = {'porcelain': 'fair', 'fair': 'fair', 'warm': 'warm', 'olive': 'warm', 'tan': 'tan', 'brown': 'deep', 'deep': 'deep'}[c['skin']]
    hair = {'espresso': 'black', 'auburn': 'ginger'}.get(c['hair'], c['hair'])
    hs = c.get('hairstyle', 'short')
    hs = 'long' if hs in ('long', 'wavy', 'braid', 'bob') else 'bun' if hs in ('bun', 'elderbun') else 'short'
    o = c['outfit']
    kw = dict(skin=skin, hair=hair, hairstyle=hs, band=bool(c.get('neckband')))
    if o in ('robe', 'hood'):
        return dict(kw, outfit='robe', hood=o == 'hood')
    return dict(kw, outfit='shirt', shirt=K.CLOTH.get(c.get('top'), '#5c9a3e') if c.get('top') else '#5c9a3e', slogan=o == 'bandtee')


def assets():
    for n, c in CAST.items():
        s = n.split()[0].lower()
        o = old_avatar(**old_cfg(c))
        o.save(f'{A}/old-{s}-full.png')
        o.crop((0, 0, 16, 16)).save(f'{A}/old-{s}-bust.png')
        for size in (36, 40, 64):
            K.bust(c, size).save(f'{A}/new-{s}-{size}.png')
        K.figure(c, 1.5).save(f'{A}/new-{s}-fig48.png')
        K.sprite(c).save(f'{A}/new-{s}-fig32.png')


ROWS = [
    ('msg', 'Orla Fenwick', 'medal', '96731', '<span class="at">@Ilse Hartwood</span> come sit with us by the maple, there’s room on the bench.'),
    ('arrival', 'Alder Meadows', None, '04648', 'Hello Tapaia! Herb grower from Kalimar, here for the tea and the talk.'),
    ('msg', 'Nessa Quill', 'medal', '04651', 'Tea cart’s open. First pot of the longhour is on me 🍵'),
    ('msg', 'Tobin Larkspur', 'flame', '04655', 'ha! saving you a seat by the playground'),
]
MV2 = '../mockups-v2/assets'


def av(name, new, size=40):
    s = name.split()[0].lower()
    cls = CLASSES.get(name, 'c6')
    if new:
        return f'<span class="av {cls}" style="width:{size}px;height:{size}px"><img src="art/compare/new-{s}-{size}.png" style="width:{size}px;height:{size}px"></span>'
    return f'<span class="av {cls}" style="width:{size}px;height:{size}px"><img src="art/compare/old-{s}-bust.png"></span>'


def feed(new, mobile=False):
    out = []
    for kind, name, badge, t, txt in ROWS:
        s = name.split()[0].lower()
        if kind == 'arrival':
            fig = (f'art/compare/new-{s}-fig32.png' if mobile else f'art/compare/new-{s}-fig48.png') if new else f'art/compare/old-{s}-full.png'
            w = (32 if mobile else 48)
            out.append(f'''<div class="card-wrap"><div class="card-arrival"><div class="fig"><img class="px" src="{fig}" style="width:{w}px;height:auto"></div>
<div style="min-width:0"><div class="k"><img class="px badge-ic" src="{MV2}/icon-medal.png" style="width:14px;height:14px">New arrival · Founding Citizen</div>
<div class="q"><b>{name}</b> “{txt}”</div></div>
<div class="wave"><button class="btn-soft">👋 Wave hello</button><span class="time" style="font-size:12px;color:var(--text-3)">{t}</span></div></div></div>''')
        else:
            b = f'<img class="px badge-ic" src="{MV2}/icon-{badge}.png">' if badge else ''
            out.append(f'''<div class="msg">{av(name, new, 36 if mobile else 40)}<div class="content"><div class="meta"><span class="who">{name}</span>{b}<span class="time">{t}</span></div>
<div class="text">{txt}</div></div></div>''')
    return '\n'.join(out)


def banner(new, mobile=False):
    if mobile:
        bg = ("background:url(art/scene-square-750x250.png) 50% bottom / 750px 250px no-repeat, #3b2251" if new else
              f"background:url({MV2}/scene-header.png) 38% bottom / 820px 96px no-repeat, #93c1e6")
        return f'''<div class="mbanner" style="{bg};image-rendering:pixelated;display:block"><div class="over"><span class="pill glass" style="height:20px;font-size:11px;padding:0 8px"><img class="px" src="{MV2}/icon-tree.png" style="width:12px;height:12px">Meldan</span>
<b>Tea cart’s open</b><span class="s">Speak as your citizen</span></div><div class="clock"><span class="pixel">04650</span>ticks</div></div>'''
    bg = ("background:url(art/scene-square-750x250.png) 46% bottom / 750px 250px no-repeat, #3b2251" if new else
          f"background:url({MV2}/scene-header.png) center bottom / 1230px 144px no-repeat, #93c1e6")
    return f'''<div class="banner" style="{bg};image-rendering:pixelated;margin:0"><div class="over"><span class="pill glass"><img class="px" src="{MV2}/icon-tree.png">In character · Meldan</span>
<h2>Tapaia Square</h2><p>Sit down, drink tea, the shops are nearby. Speak as your citizen.</p></div>
<div class="clock"><span class="pixel">04650</span><span>ticks · 0 longhours</span></div></div>'''


def sizes(new):
    out = []
    for i, n in enumerate(['Wren Halloway', 'Alder Meadows']):
        s = n.split()[0].lower()
        cls = CLASSES[n]
        for size, r in ((40, 12), (64, 18), (128, 30)):
            if new:
                src, iw = (f'art/compare/new-{s}-{min(size, 64)}.png', size)
            else:
                src, iw = (f'art/compare/old-{s}-bust.png', {40: 32, 64: 64, 128: 128}[size])
            out.append(f'<span class="av {cls}" style="width:{size}px;height:{size}px;border-radius:{r}px"><img src="{src}" style="width:{iw}px;height:{iw}px"></span>')
        out.append('<span style="width:28px"></span>')
    return ''.join(out)


CSS = '''
@font-face { font-family: 'Inter'; src: url('../mockups-v2/fonts/Inter-Variable.ttf') format('truetype'); font-weight: 100 900; }
@font-face { font-family: 'Press Start 2P'; src: url('../mockups-v2/fonts/PressStart2P-Regular.ttf') format('truetype'); }
html, body { overflow: visible; }
body { background: #efe9e0; padding: 28px 32px; }
h1 { font-size: 26px; letter-spacing: -.02em; margin: 0 0 4px; color: #2e1a40; }
.sub { color: var(--text-2); font-size: 14px; margin-bottom: 18px; }
.cols { display: grid; grid-template-columns: 1fr 1fr; gap: 24px; }
.col { min-width: 0; }
.colh { display: flex; align-items: baseline; gap: 10px; font-weight: 750; font-size: 17px; margin: 0 0 10px; color: #2e1a40; }
.colh span { font-weight: 500; font-size: 13px; color: var(--text-3); }
.panel { background: var(--bg); border: 1px solid var(--line); border-radius: 18px; overflow: hidden; padding: 16px 0 10px; margin-bottom: 16px; }
.panel .banner { margin: 0 16px 6px !important; }
.lab { font-size: 11.5px; font-weight: 700; letter-spacing: .06em; text-transform: uppercase; color: var(--text-3); padding: 0 16px 8px; }
.sizes { display: flex; align-items: flex-end; gap: 10px; padding: 6px 16px 8px; flex-wrap: nowrap; }
.card-arrival { margin: 6px 16px 6px 68px; }
.av img { image-rendering: pixelated; }
.phone { width: 390px; }
.phone .panel { border-radius: 0; border: 0; padding: 4px 0; }
'''


def page(body, width):
    return f'''<!doctype html><html><head><meta charset="utf-8">
<link rel="stylesheet" href="../../app/src/styles/app.css"><link rel="stylesheet" href="../../app/src/styles/screens.css">
<style>{CSS} body {{ width: {width}px; }}</style></head><body data-theme="light">{body}</body></html>'''


def desktop():
    cols = []
    for new in (False, True):
        head = ('New · Cozy HD pixel', '32×48 sprites · native 40/64 busts · HD Square') if new else ('Current (live today)', '16×24 sprites · 16×16 busts at 2x · 3x Square')
        cols.append(f'''<div class="col"><div class="colh">{head[0]}<span>{head[1]}</span></div>
<div class="panel"><div class="lab">Tapaia Square banner · chat feed (light)</div>{banner(new)}{feed(new)}</div>
<div class="panel" data-theme="dark" style="background:var(--bg);color:var(--text)"><div class="lab">Dark theme</div>{feed(new)}</div>
<div class="panel"><div class="lab">Avatar tiles at 40 · 64 · 128 px</div><div class="sizes">{sizes(new)}</div></div></div>''')
    body = f'''<h1>In-app characters: current vs new</h1>
<div class="sub">Same app CSS, same display sizes (desktop, 1 CSS px = 1 device px). Original art, drawn in code.</div>
<div class="cols">{''.join(cols)}</div>'''
    return page(body, 1300)


def phone(new):
    head = 'New' if new else 'Current'
    body = f'''<div class="phone"><div class="colh" style="padding:0 12px">{head}</div><div class="panel">{banner(new, True)}
<div class="feed" style="display:block;padding-top:6px">{feed(new, True)}</div></div></div>'''
    return page(body, 390).replace('padding: 28px 32px', 'padding: 12px 0')


if __name__ == '__main__':
    assets()
    open(f'{HERE}/comparison.html', 'w').write(desktop())
    open(f'{HERE}/art/phone-before.html', 'w').write(phone(False).replace('art/', '').replace('../mockups-v2', '../../mockups-v2').replace('../../app', '../../../app'))
    open(f'{HERE}/art/phone-after.html', 'w').write(phone(True).replace('art/', '').replace('../mockups-v2', '../../mockups-v2').replace('../../app', '../../../app'))
    print('comparison html ok')
