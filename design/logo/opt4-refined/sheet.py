"""Writes comparison.html for the refined Tea & Chat variants."""
import os
from build import VARIANTS
HERE = os.path.dirname(os.path.abspath(__file__))
OLD = '../opt4-tea-chat/opt4-tea-chat'

def ph(letter, bg, fg='#fff'):
    return f'<span class="ph" style="background:{bg};color:{fg}">{letter}</span>'

def col(slug, v):
    p = f'{slug}/{slug}'
    def tok(theme):
        return f'''<div class="tok {theme}"><img class="px" src="{p}-64.png" width="64" height="64"><img class="px" src="{p}-32.png" width="32" height="32"><img class="px" src="{p}-16.png" width="16" height="16"></div>'''
    def hdr(theme):
        return f'''<div class="hdr {theme}"><img class="px" src="{p}-32.png" width="32" height="32"><div><div class="nm">Tapaia</div><div class="sub">$ZC community</div></div>
          <svg class="chev" viewBox="0 0 20 20" width="16" height="16"><path d="M6 8l4 4 4-4" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/></svg></div>'''
    rows = [
        (12, ph('A', 'linear-gradient(135deg,#7d8ca3,#56657c)'), 'Placeholder A', 'PHA', '+1.2%', 'up'),
        (13, f'<img src="{p}-24.png" width="24" height="24">', 'Tapaia', 'TAPAIA', 'new', 'nw'),
        (14, ph('B', 'linear-gradient(135deg,#d9a35b,#b5762f)'), 'Placeholder B', 'PHB', '\u22120.4%', 'dn'),
    ]
    table = ''.join(f'<div class="mr{" me" if n == "Tapaia" else ""}"><span class="rk">{r}</span>{ic}<b>{n}</b><span class="sym">{s}</span><span class="chg {c}">{ch}</span></div>'
                    for r, ic, n, s, ch, c in rows)
    return f'''<section class="opt">
      <div class="h"><span class="n">{v['letter']}</span><h2>{v['title']}</h2></div>
      <p class="why">{v['why']}</p>
      <div class="hero"><div class="lt"><img class="px" src="{p}.svg" width="160" height="160"></div><div class="dk"><img class="px" src="{p}.svg" width="160" height="160"></div></div>
      <div class="lbl">Token icon · 64 / 32 / 16 px</div>
      <div class="toks">{tok('light')}{tok('dark')}</div>
      <div class="lbl">App icon &amp; chat header</div>
      <div class="row2"><img class="appi" src="{p}-app-icon-128.png" width="88" height="88"><div class="hdrs">{hdr('light')}{hdr('dark')}</div></div>
      <div class="lbl">Market list (24 px) · favicon · X profile</div>
      <div class="mkt">{table}</div>
      <div class="row3">
        <div class="tabs"><div class="tab"><img class="px" src="{p}-16.png" width="16" height="16"><span>Tapaia · #general</span><i>×</i></div>
        <div class="tab dk"><img class="px" src="{p}-16.png" width="16" height="16"><span>Tapaia · #general</span><i>×</i></div></div>
        <div class="xp"><img src="{p}-x-pfp-400.png" width="72" height="72"><div><b>Tapaia Square</b><span>@TapaiaSquare</span></div></div>
      </div>
    </section>'''

html = f'''<!doctype html><html><head><meta charset="utf-8"><style>
@font-face {{ font-family: Inter; src: url('../../mockups-v2/fonts/Inter-Variable.ttf') format('truetype'); font-weight: 100 900; }}
* {{ box-sizing: border-box; }}
body {{ margin: 0; width: 1600px; height: 1000px; overflow: hidden; background: #faf7f2; color: #1f1a24;
  font-family: Inter, system-ui, sans-serif; -webkit-font-smoothing: antialiased; font-feature-settings: 'cv11','ss01'; }}
.px {{ image-rendering: pixelated; display: block; }}
header {{ height: 68px; display: flex; align-items: center; gap: 14px; padding: 0 28px; border-bottom: 1px solid #e8e0d3; }}
header h1 {{ font-size: 22px; font-weight: 750; letter-spacing: -.02em; margin: 0; }}
header .tag {{ color: #5f5768; font-size: 14px; }}
.before {{ margin-left: auto; display: flex; align-items: center; gap: 10px; font-size: 12px; color: #8d8496; background: #fff; border: 1px solid #e8e0d3; border-radius: 10px; padding: 6px 12px; }}
.before b {{ color: #5f5768; font-weight: 600; }}
.grid {{ display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 14px; padding: 14px 22px; }}
.opt {{ background: #fff; border: 1px solid #e8e0d3; border-radius: 16px; padding: 14px 15px; box-shadow: 0 1px 2px rgba(35,20,47,.06); height: 902px; display: flex; flex-direction: column; }}
.h {{ display: flex; align-items: center; gap: 10px; }}
.n {{ width: 26px; height: 26px; border-radius: 8px; background: #5b3a86; color: #fff; display: grid; place-items: center; font-weight: 700; font-size: 14px; }}
h2 {{ margin: 0; font-size: 18px; font-weight: 700; letter-spacing: -.01em; }}
.why {{ margin: 6px 0 10px; font-size: 12.5px; line-height: 1.42; color: #5f5768; height: 54px; }}
.hero {{ display: grid; grid-template-columns: minmax(0,1fr) minmax(0,1fr); border-radius: 12px; overflow: hidden; height: 196px; flex: none; }}
.hero > div {{ display: grid; place-items: center; }}
.hero .lt {{ background: #f3eee6; }} .hero .dk {{ background: #17121d; }}
.lbl {{ font-size: 10.5px; font-weight: 600; color: #8d8496; letter-spacing: .04em; text-transform: uppercase; margin: 15px 0 8px; }}
.toks {{ display: grid; grid-template-columns: 1fr 1fr; gap: 8px; }}
.tok {{ height: 92px; border-radius: 12px; display: flex; align-items: center; justify-content: center; gap: 13px; }}
.tok.light {{ background: #fff; border: 1px solid #e8e0d3; }} .tok.dark {{ background: #1d1724; }}
.row2 {{ display: flex; gap: 12px; align-items: center; }}
.appi {{ border-radius: 20px; box-shadow: 0 6px 18px rgba(35,20,47,.18); flex: none; }}
.hdrs {{ flex: 1; display: flex; flex-direction: column; gap: 7px; }}
.hdr {{ height: 50px; border-radius: 10px; display: flex; align-items: center; gap: 10px; padding: 0 11px; }}
.hdr.light {{ background: #f3eee6; border: 1px solid #e8e0d3; color: #8d8496; }}
.hdr.dark {{ background: #17121d; color: #8a8096; }}
.hdr .nm {{ font-weight: 700; font-size: 15px; letter-spacing: -.01em; line-height: 1.15; }}
.hdr.light .nm {{ color: #1f1a24; }} .hdr.dark .nm {{ color: #f1ecf5; }}
.hdr .sub {{ font-size: 11.5px; }} .hdr .chev {{ margin-left: auto; }}
.mkt {{ border: 1px solid #e8e0d3; border-radius: 10px; overflow: hidden; }}
.mr {{ height: 42px; display: flex; align-items: center; gap: 9px; padding: 0 11px; font-size: 13px; border-top: 1px solid #f0ebe3; }}
.mr:first-child {{ border-top: 0; }}
.mr.me {{ background: #f7f3fb; }}
.mr .rk {{ width: 16px; color: #8d8496; font-size: 11.5px; }}
.mr b {{ font-weight: 650; }} .mr .sym {{ color: #8d8496; font-size: 11.5px; }}
.mr .chg {{ margin-left: auto; font-size: 12px; font-weight: 600; }}
.up {{ color: #2f9a55; }} .dn {{ color: #d8452b; }} .nw {{ color: #5b3a86; background: #efe8f7; border-radius: 6px; padding: 1px 6px; }}
.ph {{ width: 24px; height: 24px; border-radius: 50%; display: grid; place-items: center; font-weight: 800; font-size: 12px; flex: none; }}
.row3 {{ margin-top: 12px; display: flex; gap: 10px; align-items: stretch; }}
.tabs {{ flex: 1; display: flex; flex-direction: column; gap: 6px; }}
.tab {{ height: 36px; border-radius: 8px 8px 0 0; background: #fff; border: 1px solid #e8e0d3; border-bottom: 2px solid #5b3a86; display: flex; align-items: center; gap: 7px; padding: 0 9px; font-size: 12px; white-space: nowrap; }}
.tab i {{ margin-left: auto; font-style: normal; color: #8d8496; }}
.tab.dk {{ background: #241d2d; border-color: #241d2d; border-bottom-color: #8a64b0; color: #f1ecf5; }}
.xp {{ width: 150px; border-radius: 12px; background: #000; color: #e7e9ea; display: flex; flex-direction: column; align-items: flex-start; gap: 6px; padding: 8px 10px; }}
.xp img {{ border-radius: 50%; border: 3px solid #000; margin-top: 0; }}
.xp b {{ display: block; font-size: 12.5px; }} .xp span {{ color: #71767b; font-size: 11.5px; }}
.xp > div {{ line-height: 1.2; }}
</style></head><body>
<header><h1>Tapaia: Tea &amp; Chat, refined</h1><span class="tag">Option 4 pushed toward a premium token / app mark · same cozy idea</span>
<div class="before"><b>Before</b><img class="px" src="{OLD}-64.png" width="48" height="48"><img class="px" src="{OLD}-32.png" width="32" height="32"><img class="px" src="{OLD}-16.png" width="16" height="16"></div></header>
<div class="grid">{''.join(col(s, v) for s, v in VARIANTS.items())}</div>
</body></html>'''
open(os.path.join(HERE, 'comparison.html'), 'w').write(html)
print('wrote comparison.html')
