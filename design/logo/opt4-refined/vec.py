"""Vector geometry for the refined Tea & Chat mark (64-unit grid; straight edges on even units so 32px stays crisp)."""

CREAM = '#fbf1d6'
CREAM_SH = '#ecdcb4'
ROBE = '#5b3a86'
ROBE_DK = '#45275e'
ROBE_DEEP = '#2e1a40'
GLOW = '#2fc56a'
GLOW_DK = '#1f9a50'
GOLD = '#e0a526'
LEAF = '#3f7a37'

BUBBLE = 'M26 12H38A6 6 0 0 1 44 18V22A6 6 0 0 1 38 28H31C29 30.5 26.5 32.2 23 33C24.2 31.4 24.6 29.8 24.4 28A6 6 0 0 1 20 22V18A6 6 0 0 1 26 12Z'
CUP = 'M18 34H40V41A7 7 0 0 1 33 48H25A7 7 0 0 1 18 41Z'
HANDLE = 'M40 36.5H41.5A3.75 3.75 0 0 1 41.5 44H39.5'
SAUCER = dict(x=16, y=50, w=30, h=2.6, r=1.3)
DOTS = ((26, 20), (32, 20), (38, 20))

# pixel-flavoured parts for the hybrid: square dots and a stepped steam tail
BUBBLE_STEP = 'M26 12H38A6 6 0 0 1 44 18V22A6 6 0 0 1 38 28H28V30H26V32H22V30H24V28A6 6 0 0 1 20 22V18A6 6 0 0 1 26 12Z'


def content(style):
    s = style
    fill = s.get('fill', CREAM)
    out = []
    if s.get('shadow'):
        out.append(f'<g opacity=".28" transform="translate(0 1.4)" fill="{s["shadow"]}">'
                   f'<path d="{s.get("bubble", BUBBLE)}"/><path d="{CUP}"/>'
                   f'<path d="{HANDLE}" fill="none" stroke="{s["shadow"]}" stroke-width="3.2"/>'
                   f'<rect x="{SAUCER["x"]}" y="{SAUCER["y"]}" width="{SAUCER["w"]}" height="{SAUCER["h"]}" rx="{SAUCER["r"]}"/></g>')
    out.append(f'<path d="{s.get("bubble", BUBBLE)}" fill="{fill}"/>')
    if s.get('square_dots'):
        for x, y in DOTS:
            out.append(f'<rect x="{x - 2}" y="{y - 2}" width="4" height="4" fill="{s["dot"]}"/>')
    else:
        for x, y in DOTS:
            out.append(f'<circle cx="{x}" cy="{y}" r="2" fill="{s["dot"]}"/>')
    out.append(f'<path d="{HANDLE}" fill="none" stroke="{s.get("handle", fill)}" stroke-width="3.2"/>')
    out.append(f'<path d="{CUP}" fill="{fill}"/>')
    if s.get('tea'):
        out.append(f'<path d="M20 34H38V35.2Q29 37 20 35.2Z" fill="{s["tea"]}"/>')
    if s.get('band'):
        out.append(f'<rect x="18" y="38" width="22" height="2" fill="{s["band"]}"/>')
    out.append(f'<rect x="{SAUCER["x"]}" y="{SAUCER["y"]}" width="{SAUCER["w"]}" height="{SAUCER["h"]}" rx="{SAUCER["r"]}" fill="{s.get("saucer", fill)}"/>')
    return '\n'.join(out)


def svg(body, defs='', size=512, vb=64):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {vb} {vb}" width="{size}" height="{size}">'
            f'<defs>{defs}</defs>{body}</svg>\n')


# ------------------------------------------------------------------ B: clean flat vector
def mark_B():
    st = dict(dot=ROBE, tea=GOLD)
    return svg(f'<circle cx="32" cy="32" r="32" fill="{ROBE}"/>' + content(st))


# ------------------------------------------------------------------ C: premium coin (green pay-circle ring, bevel, gradients)
DEFS_C = f'''
<linearGradient id="ring" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#7ff0a8"/><stop offset=".45" stop-color="{GLOW}"/><stop offset="1" stop-color="#17804a"/></linearGradient>
<linearGradient id="ringIn" x1="1" y1="1" x2="0" y2="0"><stop offset="0" stop-color="#8ff5b5"/><stop offset=".5" stop-color="{GLOW}"/><stop offset="1" stop-color="#1a8a4c"/></linearGradient>
<radialGradient id="field" cx=".42" cy=".32" r=".75"><stop offset="0" stop-color="#7350a3"/><stop offset=".6" stop-color="{ROBE}"/><stop offset="1" stop-color="#3a2257"/></radialGradient>
<linearGradient id="cream" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fffaee"/><stop offset="1" stop-color="#f1e1bb"/></linearGradient>
'''


def coin_C(field='url(#field)'):
    return (f'<circle cx="32" cy="32" r="32" fill="url(#ring)"/>'
            f'<circle cx="32" cy="32" r="29" fill="url(#ringIn)"/>'
            f'<circle cx="32" cy="32" r="27.6" fill="#1d6b3c"/>'
            f'<circle cx="32" cy="32" r="27" fill="{field}"/>')


def mark_C():
    st = dict(fill='url(#cream)', dot=ROBE, tea=GOLD, shadow='#1a0f26')
    return svg(coin_C() + content(st), DEFS_C)


# ------------------------------------------------------------------ D: hybrid (flat coin, green pay ring, pixel dots + stepped steam)
def coin_D():
    return (f'<circle cx="32" cy="32" r="32" fill="{GLOW}"/>'
            f'<circle cx="32" cy="32" r="28" fill="{ROBE_DK}"/>')


def mark_D():
    st = dict(dot=ROBE_DK, tea=GOLD, square_dots=True, bubble=BUBBLE_STEP)
    return svg(coin_D() + content(st))
