"""Generate the Tapaia v2 mockup HTML files from shared partials. Run: python3 build.py"""
import os
HERE = os.path.dirname(os.path.abspath(__file__))

ICONS = {
    'search': '<circle cx="11" cy="11" r="6.5"/><path d="M16 16l4 4"/>',
    'bell': '<path d="M6.5 16.5V11a5.5 5.5 0 0 1 11 0v5.5l1.5 1.5H5z"/><path d="M10 20.5h4"/>',
    'users': '<circle cx="9" cy="8.5" r="3.5"/><path d="M2.5 19.5c.8-3.4 3.3-5 6.5-5s5.7 1.6 6.5 5"/><path d="M16 5.5a3.2 3.2 0 0 1 0 6.2M18 14.8c1.9.6 3.1 2.2 3.5 4.7"/>',
    'pin': '<path d="M9 3.5h6l-1 5 3 3.5H7l3-3.5z"/><path d="M12 12v8.5"/>',
    'plus': '<path d="M12 5v14M5 12h14"/>',
    'send': '<path d="M4.5 11.8L19.5 4.5l-4.3 15-3.4-6.3z"/><path d="M11.8 13.2l7.7-8.7"/>',
    'smile': '<circle cx="12" cy="12" r="8.5"/><path d="M8.5 14c.9 1.3 2.1 2 3.5 2s2.6-.7 3.5-2"/><path d="M9 9.5h.01M15 9.5h.01"/>',
    'chev-d': '<path d="M7 10l5 5 5-5"/>',
    'chev-l': '<path d="M14.5 6l-6 6 6 6"/>',
    'chev-r': '<path d="M9.5 6l6 6-6 6"/>',
    'sliders': '<path d="M4 7h9M17 7h3M4 17h3M11 17h9"/><circle cx="15" cy="7" r="2"/><circle cx="9" cy="17" r="2"/>',
    'more': '<circle cx="5.5" cy="12" r="1"/><circle cx="12" cy="12" r="1"/><circle cx="18.5" cy="12" r="1"/>',
    'image': '<rect x="3.5" y="5" width="17" height="14" rx="3"/><circle cx="9" cy="10" r="1.6"/><path d="M5 18l5-5 3 3 2.5-2.5L20 18"/>',
    'check': '<path d="M5 12.5l4.5 4.5L19 7.5"/>',
    'x': '<path d="M6 6l12 12M18 6L6 18"/>',
    'ext': '<path d="M13.5 5.5H18.5V10.5"/><path d="M18.5 5.5l-8 8"/><path d="M17 14v4.5a1 1 0 0 1-1 1H6.5a1 1 0 0 1-1-1V8a1 1 0 0 1 1-1H11"/>',
    'info': '<circle cx="12" cy="12" r="8.5"/><path d="M12 11v5.5M12 7.8h.01"/>',
    'shield': '<path d="M12 3.5l7 3v5c0 4.4-3 7.7-7 9-4-1.3-7-4.6-7-9v-5z"/><path d="M9 12l2.2 2.2L15.5 10"/>',
    'lock': '<rect x="5" y="10.5" width="14" height="10" rx="2.5"/><path d="M8.5 10.5V8a3.5 3.5 0 0 1 7 0v2.5"/>',
    'home': '<path d="M4 11l8-6.5 8 6.5v8.5a1 1 0 0 1-1 1h-4.5v-6h-5v6H5a1 1 0 0 1-1-1z"/>',
    'chat': '<path d="M4.5 6.5a2 2 0 0 1 2-2h11a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2H10l-4.5 3.5V16.5h1a2 2 0 0 1-2-2z"/>',
    'user': '<circle cx="12" cy="8.5" r="3.8"/><path d="M4.5 20c1-3.8 3.9-5.8 7.5-5.8s6.5 2 7.5 5.8"/>',
    'compass': '<circle cx="12" cy="12" r="8.5"/><path d="M15.5 8.5l-2 5-5 2 2-5z"/>',
    'hash': '<path d="M9 4.5L7.5 19.5M16.5 4.5L15 19.5M5 9h14.5M4.5 15h14.5"/>',
    'thread': '<path d="M6 5v8a3 3 0 0 0 3 3h9"/><path d="M15 13l3 3-3 3"/>',
    'mic': '<rect x="9" y="3.5" width="6" height="10.5" rx="3"/><path d="M6 11.5a6 6 0 0 0 12 0M12 17.5v3"/>',
    'shuffle': '<path d="M4 7h3.5c4 0 5 10 9 10H20M17 14l3 3-3 3M4 17h3.5M16.5 7H20M17 4l3 3-3 3"/>',
    'sparkle': '<path d="M12 4l1.8 5.2L19 11l-5.2 1.8L12 18l-1.8-5.2L5 11l5.2-1.8z"/>',
    'wallet': '<rect x="3.5" y="6" width="17" height="13" rx="3"/><path d="M16 12.5h4.5M3.5 9h13"/>',
    'qr': '<rect x="4" y="4" width="6" height="6" rx="1"/><rect x="14" y="4" width="6" height="6" rx="1"/><rect x="4" y="14" width="6" height="6" rx="1"/><path d="M14 14h2v2h-2zM18 18h2v2h-2zM14 18h2M18 14h2"/>',
    'edit': '<path d="M5 19l1-4L15.5 5.5l3 3L9 18z"/>',
    'moon': '<path d="M19 14.5A7.5 7.5 0 0 1 9.5 5a7.5 7.5 0 1 0 9.5 9.5z"/>',
}


def sprite():
    syms = ''.join(f'<symbol id="i-{k}" viewBox="0 0 24 24">{v}</symbol>' for k, v in ICONS.items())
    return f'<svg width="0" height="0" style="position:absolute">{syms}</svg>'


def i(name, cls=''):
    return f'<svg class="i {cls}"><use href="#i-{name}"/></svg>'


def av(name, c='c1', size='', dot=None, bust=True):
    src = f'assets/bust-{name}.png'
    d = f'<span class="dot {dot}"></span>' if dot is not None else ''
    tile = f'<span class="av {size} {c}"><img src="{src}" alt=""></span>'
    return f'<span class="av-wrap">{tile}{d}</span>' if d else tile


def page(title, body, theme='light', kind='desk', extra_css=''):
    return f'''<!doctype html>
<html lang="en" data-theme="{theme}"><head><meta charset="utf-8">
<title>Tapaia v2 mockup: {title}</title>
<link rel="stylesheet" href="app.css">
<style>{extra_css}</style></head>
<body class="{kind}">{sprite()}
{body}
</body></html>'''


PEOPLE = {
    # key: (display name, avatar color)
    'ilse': ('Ilse Hartwood', 'c1'), 'nessa': ('Nessa Quill', 'c5'), 'corvin': ('Corvin Ashdale', 'c3'),
    'wren': ('Wren Halloway', 'c2'), 'orla': ('Orla Fenwick', 'c4'), 'tobin': ('Tobin Larkspur', 'c1'),
    'pim': ('Pim Tallow', 'c3'), 'team': ('Bram Teasel', 'c2'), 'marek': ('Marek Stonebrook', 'c6'),
    'juniper': ('Juniper Vale', 'c4'), 'odessa': ('Odessa Brightmoss', 'c2'), 'sorrel': ('Sorrel Finch', 'c5'),
    'lumi': ('Lumi Ardent', 'c6'), 'bram': ('Bram Teasel', 'c4'),
}


def sidebar(active, unread=None, me=('juniper', 'Juniper Vale', 'In Tapaia Square')):
    unread = unread or {}
    def ch(name, label=None):
        cls = 'on' if name == active else ('unread' if name in unread else '')
        right = ''
        if name in unread and name != active:
            right = f'<span class="badge">{unread[name]}</span>' if (type(unread[name]) is int) else ''
        return f'<div class="ch {cls}"><span class="hash">#</span>{label or name}{right}</div>'
    sq_cls = 'on' if active == 'square' else ''
    return f'''
<aside class="side">
  <div class="ws"><span class="logo-tile"><img class="px" src="assets/icon-tea.png" alt=""></span>
    <div><div class="name">Tapaia</div><div class="sub">$ZC community</div></div><span class="chev">{i('chev-d','sm')}</span></div>
  <div class="search">{i('search','sm')}Search Tapaia<kbd>⌘K</kbd></div>
  <nav class="nav">
    <div class="sec-h">COMMUNITY</div>
    {ch('announcements')}{ch('general')}{ch('market')}{ch('support')}{ch('dev-updates')}{ch('feeds')}{ch('lobby')}
    <div class="sec-h">VERIDIA <span class="tag ic">in character</span></div>
    <div class="ch {sq_cls}"><img class="px" src="assets/icon-tree.png" alt="">Tapaia Square<span class="count">14 here</span></div>
    <div class="ch muted"><img class="px" src="assets/icon-lock.png" alt="" style="opacity:.55">More of Meldan<span class="lock">soon</span></div>
    <div class="sec-h">DIRECT MESSAGES</div>
    <div class="ch">{av('nessa','c5','s28')}Nessa Quill</div>
    <div class="ch">{av('orla','c4','s28')}Orla Fenwick</div>
  </nav>
  <div class="me">{av(me[0], PEOPLE[me[0]][1], '', '')}
    <div><div class="nm">{me[1]}</div><div class="st">{me[2]}</div></div>
    <div class="icons">{i('bell','sm')}{i('sliders','sm')}</div></div>
</aside>'''


def write(name, html):
    with open(os.path.join(HERE, name), 'w') as f:
        f.write(html)
    print('wrote', name)


if __name__ == '__main__':
    import screens
    screens.build()
