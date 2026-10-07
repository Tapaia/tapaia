"""Writes comparison.html (rendered to comparison.png by render.sh)."""
import os
from designs import OPTIONS
HERE = os.path.dirname(os.path.abspath(__file__))
INFO = {
    'opt1-pay-circle-lamp': ('1', 'Green Pay Circle + Lamp',
        "The book's glowing green check-in / pay circle [ch1, ch5] with a Square lamp lit inside. Already our verify colour, and it reads as a coin."),
    'opt2-square-tree': ('2', 'Square Tree',
        "\u201cGood trees, good tea, good shade\u201d [ch6]: the Square's tree on robe purple. Our two core brand colours in one simple mark."),
    'opt3-robe-hood': ('3', 'Robe Hood',
        "The Veridian Privacy Robe, hood up, nose-strap face cover [ch1]. A friendly mascot with a face, on lamp-gold."),
    'opt4-tea-chat': ('4', 'Tea & Chat',
        "\u201cYou can sit down, drink tea\u201d [ch6]: the steam turns into a chat bubble. Says \u201cchat app\u201d even to people who never read the book."),
}

def col(slug):
    num, title, why = INFO[slug]
    p = f'{slug}/{slug}'
    alt = ''
    if slug.startswith('opt1'):
        alt = ('<div class="alt"><img class="px" src="opt1b-pay-circle-tree/opt1b-pay-circle-tree-64.png" width="40" height="40">'
               '<span>Alt: tree<br>inside (1b)</span></div>')
    def tok(theme):
        return f'''<div class="tok {theme}">
          <img class="px" src="{p}-64.png" width="64" height="64">
          <img class="px" src="{p}-32.png" width="32" height="32">
          <img class="px" src="{p}-16.png" width="16" height="16">
        </div>'''
    def header(theme):
        return f'''<div class="hdr {theme}">
          <img class="px" src="{p}-32.png" width="32" height="32">
          <div><div class="nm">Tapaia</div><div class="sub">$ZC community</div></div>
          <svg class="chev" viewBox="0 0 20 20" width="16" height="16"><path d="M6 8l4 4 4-4" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/></svg>
        </div>'''
    return f'''<section class="opt">
      <div class="h"><span class="n">{num}</span><h2>{title}</h2></div>
      <p class="why">{why}</p>
      <div class="hero"><div class="lt"><img class="px" src="{p}.svg" width="160" height="160"></div><div class="dk"><img class="px" src="{p}.svg" width="160" height="160"></div></div>
      <div class="lbl">Token icon · 64 / 32 / 16 px · light &amp; dark</div>
      <div class="toks">{tok('light')}{tok('dark')}</div>
      <div class="lbl">App icon &amp; chat-header lockup</div>
      <div class="row2">
        <img class="appi" src="{p}-app-icon-128.png" width="96" height="96">
        <div class="hdrs">{header('light')}{header('dark')}</div>
      </div>
      <div class="lbl">In context · wallet list &amp; browser tab</div>
      <div class="ctx">
        <div class="wal"><img class="px" src="{p}-32.png" width="32" height="32"><div><b>TAPAIA</b><span>Tapaia</span></div><div class="amt"><b>1,250.00</b><span>demo</span></div></div>
        <div class="wal dk"><img class="px" src="{p}-32.png" width="32" height="32"><div><b>TAPAIA</b><span>Tapaia</span></div><div class="amt"><b>1,250.00</b><span>demo</span></div></div>
        <div class="tabs"><div class="tab"><img class="px" src="{p}-16.png" width="16" height="16"><span>Tapaia · #general</span><i>×</i></div><div class="tab dk"><img class="px" src="{p}-16.png" width="16" height="16"><span>Tapaia · #general</span><i>×</i></div></div>
      </div>
      <div class="big {'' if not alt else 'with-alt'}">
        <img class="px" src="{p}-64.png" width="48" height="48"><span class="wm">Tapaia</span>{alt}
      </div>
    </section>'''

html = f'''<!doctype html><html><head><meta charset="utf-8"><style>
@font-face {{ font-family: Inter; src: url('../mockups-v2/fonts/Inter-Variable.ttf') format('truetype'); font-weight: 100 900; }}
* {{ box-sizing: border-box; }}
body {{ margin: 0; width: 1600px; height: 1000px; overflow: hidden; background: #faf7f2; color: #1f1a24;
  font-family: Inter, system-ui, sans-serif; -webkit-font-smoothing: antialiased; font-feature-settings: 'cv11','ss01'; }}
.px {{ image-rendering: pixelated; display: block; }}
header {{ height: 72px; display: flex; align-items: center; gap: 14px; padding: 0 32px; border-bottom: 1px solid #e8e0d3; }}
header h1 {{ font-size: 22px; font-weight: 750; letter-spacing: -.02em; margin: 0; }}
header .meta {{ color: #8d8496; font-size: 13px; margin-left: auto; }}
.grid {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; padding: 18px 24px; }}
.opt {{ background: #fff; border: 1px solid #e8e0d3; border-radius: 16px; padding: 16px; box-shadow: 0 1px 2px rgba(35,20,47,.06); height: 890px; display: flex; flex-direction: column; }}
.h {{ display: flex; align-items: center; gap: 10px; }}
.n {{ width: 26px; height: 26px; border-radius: 8px; background: #5b3a86; color: #fff; display: grid; place-items: center; font-weight: 700; font-size: 14px; }}
h2 {{ margin: 0; font-size: 18px; font-weight: 700; letter-spacing: -.01em; }}
.why {{ margin: 8px 0 12px; font-size: 13px; line-height: 1.45; color: #5f5768; height: 57px; }}
.hero {{ display: grid; grid-template-columns: 1fr 1fr; border-radius: 12px; overflow: hidden; height: 196px; }}
.hero > div {{ display: grid; place-items: center; }}
.hero .lt {{ background: #f3eee6; }} .hero .dk {{ background: #17121d; }}
.hero img {{ width: 160px; height: 160px; }}
.hero .lt img {{ margin-left: 0; }}
.lbl {{ font-size: 11px; font-weight: 600; color: #8d8496; letter-spacing: .03em; text-transform: uppercase; margin: 14px 0 8px; }}
.toks {{ display: grid; grid-template-columns: 1fr 1fr; gap: 8px; }}
.tok {{ height: 88px; border-radius: 12px; display: flex; align-items: center; justify-content: center; gap: 14px; }}
.tok.light {{ background: #ffffff; border: 1px solid #e8e0d3; }} .tok.dark {{ background: #1d1724; }}
.row2 {{ display: flex; gap: 12px; align-items: center; }}
.appi {{ border-radius: 22px; box-shadow: 0 6px 18px rgba(35,20,47,.18); flex: none; }}
.hdrs {{ flex: 1; display: flex; flex-direction: column; gap: 8px; }}
.hdr {{ height: 56px; border-radius: 10px; display: flex; align-items: center; gap: 10px; padding: 0 12px; }}
.hdr.light {{ background: #f3eee6; border: 1px solid #e8e0d3; color: #8d8496; }}
.hdr.dark {{ background: #17121d; color: #8a8096; }}
.hdr .nm {{ font-weight: 700; font-size: 16px; letter-spacing: -.01em; line-height: 1.15; }}
.hdr.light .nm {{ color: #1f1a24; }} .hdr.dark .nm {{ color: #f1ecf5; }}
.hdr .sub {{ font-size: 12px; }}
.hdr .chev {{ margin-left: auto; }}
.big {{ margin-top: auto; height: 96px; border-radius: 12px; background: linear-gradient(135deg, #f7f3fb, #efe8f7); display: flex; align-items: center; gap: 12px; padding: 0 20px; }}
.big .wm {{ font-size: 40px; font-weight: 800; letter-spacing: -.035em; color: #2e1a40; }}
.ctx {{ display: flex; flex-direction: column; gap: 8px; margin-bottom: 12px; }}
.wal {{ height: 52px; border-radius: 10px; border: 1px solid #e8e0d3; display: flex; align-items: center; gap: 10px; padding: 0 12px; font-size: 13px; }}
.wal b {{ display: block; font-weight: 650; }} .wal span {{ color: #8d8496; font-size: 12px; }}
.wal .amt {{ margin-left: auto; text-align: right; }}
.wal.dk {{ background: #1d1724; border-color: #1d1724; color: #f1ecf5; }}
.tabs {{ display: grid; grid-template-columns: 1fr 1fr; gap: 8px; }}
.tab {{ height: 34px; border-radius: 8px 8px 0 0; background: #fff; border: 1px solid #e8e0d3; border-bottom: 2px solid #5b3a86; display: flex; align-items: center; gap: 7px; padding: 0 9px; font-size: 12px; white-space: nowrap; overflow: hidden; }}
.tab i {{ margin-left: auto; font-style: normal; color: #8d8496; }}
.tab.dk {{ background: #241d2d; border-color: #241d2d; border-bottom-color: #8a64b0; color: #f1ecf5; }}
.alt {{ margin-left: auto; display: flex; align-items: center; gap: 8px; font-size: 11px; color: #5f5768; line-height: 1.3; }}
.alt img {{ width: 40px; height: 40px; }}
</style></head><body>
<header><h1>Tapaia: logo options</h1><span style="color:#5f5768;font-size:14px">One mark for the app and the $TAPAIA token · original pixel art, colours from the book</span>
<span class="meta">Draft · Oct 7, 2026</span></header>
<div class="grid">{''.join(col(s) for s, _, _ in OPTIONS)}</div>
</body></html>'''
open(os.path.join(HERE, 'comparison.html'), 'w').write(html)
print('wrote comparison.html')
