"""Original pixel sprites and icons for Tapaia mockups (GPL v3, part of the Tapaia repo).

Sprites are char maps. Symmetric sprites are written as their left half and mirrored.
Colors come from design/visual-reference.md (canon-anchored where the book describes them).
"""
from PIL import Image

OUT = '#2b1d2e'  # warm near-black outline

ROBE = {'R': '#2e1a40', 'r': '#45275e', 'L': '#64408a', 'l': '#8a64b0'}
BAND = {'n': '#d9cfe6', 'N': '#a99bc2'}
SKINS = {
    'fair':   ('#f6d7b8', '#e0b48f'),
    'warm':   ('#e8b98c', '#c98e62'),
    'tan':    ('#c68a5a', '#a06a40'),
    'deep':   ('#8d5a3b', '#6c4029'),
}
HAIRS = {
    'chestnut': ('#7a4a2a', '#a0673a'),
    'black':    ('#2e2630', '#4a3f4f'),
    'blonde':   ('#d9a441', '#f0c96a'),
    'ginger':   ('#b5522b', '#d8743f'),
    'silver':   ('#9aa0ad', '#c7ccd6'),
    'plum':     ('#5a2f5e', '#7e4a84'),
}


def mirror(rows, odd=False):
    out = []
    for r in rows:
        right = r[::-1] if not odd else r[:-1][::-1]
        out.append(r + right)
    return out


def check(rows, w):
    for i, r in enumerate(rows):
        assert len(r) == w, (i, r, len(r), w)
    return rows


def render(rows, pal, scale=1):
    h = len(rows); w = len(rows[0])
    img = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    px = img.load()
    for y, row in enumerate(rows):
        for x, c in enumerate(row):
            if c == '.' or c == ' ':
                continue
            col = OUT if c == 'o' else pal[c]
            px[x, y] = hex2rgba(col)
    if scale != 1:
        img = img.resize((w * scale, h * scale), Image.NEAREST)
    return img


def hex2rgba(h, a=255):
    h = h.lstrip('#')
    return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), a)

# ---------------------------------------------------------------- avatars 16x24
HEAD_HAIR = [            # rows 0-11, left half
    "....oooo",
    "..oohhhh",
    ".ohhhHHh",
    ".ohhHhhh",
    "ohhhhhhh",
    "ohhhhhhh",
    "ohhsshhs",
    "ohssesss",
    "ohssesss",
    "ohsbssss",
    ".osssssS",
    "..oossss",
]
HEAD_HOOD = [            # hood up + face cover (strap 't' across the nose line)
    "....oooo",
    "..oorrrr",
    ".orrrLLr",
    ".orrLrrr",
    "orrLrrrr",
    "orrRRRRR",
    "orRccccc",
    "orRcgccc",
    "orRcgccc",
    "orRttttt",
    ".orRcccc",
    "..orRRcc",
]
BODY_ROBE = [            # rows 12-23; the hood lies on the shoulders when down
    "...onnnn",
    "..oLLLLL",
    ".oLRRRRR",
    ".oLrrrrr",
    ".oLrrRrr",
    "oLrrrRrr",
    "osSrrRrr",
    ".oLrrRrr",
    ".orrrrrr",
    ".oRRRRRR",
    "..offfo.",
    "..ooooo.",
]
BODY_SHIRT = [
    "...ossss",
    "..oTTTTT",
    ".oTTTTTT",
    ".oTTTTTT",
    "osTTTTTT",
    "osTTTTTT",
    ".oTTTTTT",
    ".oPPPPPP",
    "..oPPPPo",
    "..oPPPPo",
    "..obbbbo",
    "..oooooo",
]


def avatar(outfit='robe', hood=False, skin='warm', hair='chestnut', hairstyle='short',
           band=True, shirt='#5c9a3e', pants='#4a3f4f', slogan=False):
    head = HEAD_HOOD if hood else HEAD_HAIR
    body = BODY_ROBE if outfit == 'robe' else BODY_SHIRT
    rows = mirror(check(head, 8) + check(body, 8))
    rows = [list(r) for r in rows]
    if outfit == 'robe':
        # dark purple robe shoes with a high heel and uneven soles [ch1]:
        # left sole tilts down at the toe, right shoe stands on a taller heel
        rows[22] = list('..offfo..offfo..')
        rows[23] = list('.oooooo..ooFFo..')
        rows.append(list('...........oo...'))
    if outfit == 'shirt' and not band:
        rows[12][4:12] = list('ssssssss')
    if outfit == 'robe' and not band:
        rows[12][4:12] = list('RRRRRRRR')
    if outfit == 'shirt' and band:
        rows[12][4:12] = list('nnnnnnnn')
    if outfit == 'shirt' and slogan:
        for x in range(5, 11):
            rows[15][x] = 'w' if x % 2 else 'T'
    if not hood and hairstyle == 'long':
        for y in range(6, 14):
            rows[y][1] = 'h'; rows[y][14] = 'h'
            rows[y][0] = 'o'; rows[y][15] = 'o'
        rows[13][2] = 'h'; rows[13][13] = 'h'
    if not hood and hairstyle == 'bun':
        rows.insert(0, list('......oooo......'))
        rows.insert(1, list('.....ohhHho.....'))
        rows[2][4:12] = list('oohhhhoo')
    rows = [''.join(r) for r in rows]
    s, S = SKINS[skin]
    h, H = HAIRS[hair]
    pal = dict(ROBE); pal.update(BAND)
    pal.update({'s': s, 'S': S, 'b': '#e88a8a' if skin in ('fair', 'warm') else S,
                'h': h, 'H': H, 'e': '#2b1d2e', 'c': '#231430', 'g': '#d8c8ff',
                't': '#7a5a9a', 'f': ROBE['R'], 'F': '#1d1029', 'T': shirt,
                'P': pants, 'w': '#fbf1d6'})
    pal['b'] = pal['b'] if outfit == 'robe' or True else pal['b']
    # shirt shoes are brown
    if outfit == 'shirt':
        pal['b2'] = '#6b3f1f'
    img = render(rows, pal)
    if outfit == 'shirt':
        # recolor shoe pixels drawn with 'b' in body rows (bottom two rows)
        px = img.load()
        for y in range(img.height - 2, img.height):
            for x in range(16):
                if px[x, y][:3] == hex2rgba(pal['b'])[:3]:
                    px[x, y] = hex2rgba('#6b3f1f')
    return img


# ---------------------------------------------------------------- mini 9x13 for scenes
MINI_ROBE = ["..ooo", ".ohhh", "ohhhh", "ohses", "ohsss", ".osss", "..onn", ".orrr",
             "orrrr", "osrrr", ".orrr", ".oRRR", ".ofo."]
MINI_HOOD = ["..ooo", ".orrr", "orLrr", "orRcc", "orcgc", ".orttt"[:5], "..oRR", ".orrr",
             "orrrr", "osrrr", ".orrr", ".oRRR", ".ofo."]
MINI_SHIRT = ["..ooo", ".ohhh", "ohhhh", "ohses", "ohsss", ".osss", "..oss", ".oTTT",
              "oTTTT", "osTTT", ".oPPP", ".oPoP"[:5], ".ofo."]


def mini(kind='robe', skin='warm', hair='chestnut', shirt='#c8452e', pants='#4a3f4f'):
    base = {'robe': MINI_ROBE, 'hood': MINI_HOOD, 'shirt': MINI_SHIRT}[kind]
    rows = mirror(check(base, 5), odd=True)
    s, S = SKINS[skin]; h, H = HAIRS[hair]
    pal = dict(ROBE); pal.update(BAND)
    pal.update({'s': s, 'S': S, 'h': h, 'H': H, 'e': OUT, 'c': '#231430', 'g': '#d8c8ff',
                't': '#7a5a9a', 'f': ROBE['R'] if kind != 'shirt' else '#6b3f1f',
                'T': shirt, 'P': pants})
    return render(rows, pal)


# ---------------------------------------------------------------- icons 12x12
ICONS = {
    'coin': (["...oooooo...", ".ooyyyyyyoo.", ".oyYYYYYYyo.", "oyYZZZZZZYyo", "oyYYYYYZZYyo",
              "oyYYYYZZYYyo", "oyYYYZZYYYdo", "oyYYZZYYYYdo", "oyYZZZZZZYdo", ".oyYYYYYYdo.",
              ".ooddddddoo.", "...oooooo..."],
             {'y': '#e0a526', 'Y': '#ffd95a', 'Z': '#7a4a10', 'd': '#9c6a17'}),
    'flame': ([".....oo.....", "....orro....", "....orro....", "...orOOro...", "..orOOOOro..",
               "..orOYYOro..", ".orOYYYYOro.", ".orOYYYYOro.", ".orOOYYOOro.", "..orOOOOro..",
               "...orrrro...", "....oooo...."],
              {'r': '#d8452b', 'O': '#f08a24', 'Y': '#ffd95a'}),
    'door': (["...oooooo...", "..oddddddo..", ".odwWwwWwdo.", ".odwWwwWwdo.", ".odwWwwWwdo.",
              ".odwWwwWwdo.", ".odwWwwWkdo.", ".odwWwwWwdo.", ".odwWwwWwdo.", ".odwWwwWwdo.",
              ".oddddddddo.", ".oooooooooo."],
             {'w': '#9a6235', 'W': '#c98d4f', 'd': '#6b3f1f', 'k': '#ffd95a'}),
    'circle': (["...gggggg...", "..gGGGGGGg..", ".gGg....gGg.", "gGg......gGg", "gG........Gg",
                "gG........Gg", "gG........Gg", "gG........Gg", "gGg......gGg", ".gGg....gGg.",
                "..gGGGGGGg..", "...gggggg..."],
               {'g': '#1f9e52', 'G': '#39e07a'}),
    'book': (["..ooooooooo.", ".ocCCCCCCCo.", ".ocCYYYYCCo.", ".ocCYYYYCCo.", ".ocCCCCCCCo.",
              ".ocCCCCCCCo.", ".ocCCCCCCCo.", ".ocCCCCCCCo.", ".ocoooooooo.", ".ocppppppppo",
              "..ooooooooo.", "............"],
             {'c': '#2e1a40', 'C': '#64408a', 'Y': '#ffd95a', 'p': '#f4e4bc'}),
    'scroll': ([".oooooooooo.", "odPPPPPPPPdo", ".oooooooooo.", "..oppppppo..", "..oplllppo..",
                "..oppppppo..", "..opllllpo..", "..oppppppo..", "..oplllppo..", ".oooooooooo.",
                "odPPPPPPPPdo", ".oooooooooo."],
               {'p': '#fbf1d6', 'P': '#e8cf98', 'd': '#9a6235', 'l': '#9a7a55'}),
    'tea': (["...s..s.....", "....s..s....", "...s..s.....", ".oooooooo...", ".otttttto...",
             ".occccccooo.", ".occccccoco.", ".occccccooo.", "..occccCo...", "...oooooo...",
             ".oCCCCCCCCo.", "..oooooooo.."],
            {'s': '#c9d6e0', 't': '#7aa64a', 'c': '#fbf1d6', 'C': '#d8ccb4'}),
    'bubble': (["............", ".oooooooooo.", "owwwwwwwwwwo", "owwwwwwwwwwo", "owwowwowwowo",
                "owwwwwwwwwwo", ".oooowwoooo.", "....owo.....", "....oo......", "............",
                "............", "............"],
               {'w': '#fbf1d6'}),
    'stall': ([".oooooooooo.", "oaaAAaaAAaao", "oaaAAaaAAaao", ".oooooooooo.", ".d........d.",
               ".d..yy....d.", ".d.yyyy.k.d.", "oooooooooooo", "owwwwwwwwwwo", "owWWWWWWWWwo",
               "owwwwwwwwwwo", "oooooooooooo"],
              {'a': '#3f7a37', 'A': '#f4e4bc', 'd': '#6b3f1f', 'y': '#ffd95a', 'k': '#c8452e',
               'w': '#9a6235', 'W': '#c98d4f'}),
    'help': ([".oooooooooo.", "ogggWWWWgggo", "oggWWggWWggo", "oggggggWWggo", "ogggggWWgggo",
              "oggggWWggggo", "oggggggggggo", "oggggWWggggo", ".oooogoooo..", "....oo......",
              "............", "............"],
             {'g': '#3f7a37', 'W': '#fbf1d6'}),
    'terminal': (["oooooooooooo", "obbbbbbbbbbo", "oooooooooooo", "onnnnnnnnnno", "onGnnnnnnnno",
                  "onnGnnnnnnno", "onGnnGGGnnno", "onnnnnnnnnno", "onnnnnnnnnno", "oooooooooooo",
                  "............", "............"],
                 {'b': '#64408a', 'n': '#0a0e27', 'G': '#7fbcff'}),
    'robot': ([".....oo.....", "....oeeo....", "..oooooooo..", ".oMmmmmmmMo.", ".omeemmeemo.",
               ".omeemmeemo.", ".ommmmmmmmo.", ".ommoooommo.", ".oMmmmmmmMo.", "..oooooooo..",
               "...oMmmMo...", "...oooooo..."],
              {'m': '#c7ccd6', 'M': '#8a92a0', 'e': '#39e07a'}),
    'bench': (["............", "............", "............", ".oooooooooo.", ".oWWWWWWWWo.",
               ".oooooooooo.", ".oWWWWWWWWo.", "oooooooooooo", "owwwwwwwwwwo", "oooooooooooo",
               ".od......do.", ".oo......oo."],
              {'w': '#9a6235', 'W': '#c98d4f', 'd': '#6b3f1f'}),
    'medal': ([".ooo....ooo.", ".orRo..oRro.", "..orRooRro..", "...orRRro...", "...oooooo...",
               "..oYYYYYYo..", ".oYYYggYYdo.", ".oYYgggYYdo.", ".oYgggYYYdo.", ".oYYgYYYYdo.",
               "..oddddddo..", "...oooooo..."],
              {'r': '#64408a', 'R': '#8a64b0', 'Y': '#ffd95a', 'd': '#c08a20', 'g': '#3f7a37'}),
    'shield': ([".oooooooooo.", ".otttttttTo.", ".ottttttWTo.", ".otttttWtTo.", ".oWtttWttTo.",
                ".otWtWtttTo.", ".ottWttttTo.", "..otttttTo..", "..otttttTo..", "...otttTo...",
                "....otTo....", ".....oo....."],
               {'t': '#3f7a37', 'T': '#24452a', 'W': '#fbf1d6'}),
    'bell': ([".....oo.....", "....oYYo....", "...oYYYdo...", "..oYYYYYdo..", "..oYYYYYdo..",
              "..oYYYYYdo..", ".oYYYYYYYdo.", "oYYYYYYYYYdo", "oooooooooooo", ".....oo.....",
              "............", "............"],
             {'Y': '#ffd95a', 'd': '#c08a20'}),
    'lock': (["....oooo....", "...oMMMMo...", "..oMo..oMo..", "..oMo..oMo..", ".oooooooooo.",
              ".oYYYYYYYdo.", ".oYYYooYYdo.", ".oYYYooYYdo.", ".oYYYYYYYdo.", ".oddddddddo.",
              ".oooooooooo.", "............"],
             {'M': '#8a92a0', 'Y': '#e0a526', 'd': '#9c6a17'}),
    'clock': (["...oooooo...", "..oWWWWWWo..", ".oWWWWoWWWo.", "oWWWWWoWWWWo", "oWWWWWoWWWWo",
               "oWWWWWooooWo", "oWWWWWWWWWWo", "oWWWWWWWWWWo", ".oWWWWWWWWo.", "..oWWWWWWo..",
               "...oooooo...", "............"],
              {'W': '#fbf1d6'}),
    'speaker': (["............", "............", ".....oo.....", "....oMo..o..", ".oooMMo...o.",
                 ".oMMMMo.o.o.", ".oMMMMo.o.o.", ".oooMMo...o.", "....oMo..o..", ".....oo.....",
                 "............", "............"],
                {'M': '#c7ccd6'}),
    'tree': (["...oooooo...", "..oLLggggo..", ".oLLggggggo.", "oLggggggggGo", "ogggggggggGo",
              "ogggggggGGGo", ".oggggGGGGo.", "..oooddooo..", "....oddo....", "....oddo....",
              "...ooddoo...", "..oooooooo.."],
             {'L': '#8cc152', 'g': '#5c9a3e', 'G': '#2f5a2e', 'd': '#6b3f1f'}),
    'wallet': (["............", ".oooooooooo.", "owwwwwwwwwwo", "oWWWWWWWWWWo", "owwwwwwwoooo",
                "owwwwwwwoyyo", "owwwwwwwoyyo", "owwwwwwwoooo", "oWWWWWWWWWWo", ".oooooooooo.",
                "............", "............"],
               {'w': '#9a6235', 'W': '#6b3f1f', 'y': '#ffd95a'}),
    'star': ([".....oo.....", ".....oYo....", "....oYYo....", "oooooYYYoooo", "oYYYYYYYYYdo",
              ".oYYYYYYYdo.", "..oYYYYYdo..", "..oYYoYYdo..", ".oYYo.oYYdo.", ".oYo...oYdo.",
              ".oo.....oo..", "............"],
             {'Y': '#ffd95a', 'd': '#c08a20'}),
    'pin': (["....oooo....", "...orrrro...", "..orRrrrro..", "..orrrrrro..", "...orrrro...",
             "....oooo....", ".....oo.....", ".....oo.....", ".....oo.....", "......o.....",
             "............", "............"],
            {'r': '#d8452b', 'R': '#f08a8a'}),
}


def icon(name):
    rows, pal = ICONS[name]
    return render(check(rows, 12), pal)

# ---------------------------------------------------------------- wallet picker icons (original pixel art,
# evocative of each wallet's name; NOT the official logos)
WALLET_ICONS = {
    'rabby': (["..oo....oo..", ".oWo....oWo.", ".oWpo..opWo.", ".oWpo..opWo.", "..oWWooWWo..",
               ".oWWWWWWWWo.", "oWWeWWWWeWWo", "oWWWWppWWWWo", "oWWWWWWWWWWo", ".oWWWWWWWWo.",
               "..oooooooo..", "............"],
              {'W': '#a9b8ff', 'p': '#f6b0c8', 'e': '#2b1d2e'}),       # a friendly rabbit
    'metamask': (["o..........o", "oOo......oOo", "oOOooooooOOo", "oOOOOOOOOOOo", "oOwwOOOOwwOo",
                  "oOweOOOOewOo", ".oOOOOOOOOo.", ".oOOwwwwOOo.", "..oOwkkwOo..", "...oOwwOo...",
                  "....oooo....", "............"],
                 {'O': '#f08a24', 'w': '#fbf1d6', 'e': '#2b1d2e', 'k': '#2b1d2e'}),  # a fox face
    'coinbase': (["...oooooo...", ".oobbbbbboo.", ".obbbbbbbbo.", "obbbwwwwbbbo", "obbwwbbbbbbo",
                  "obbwbbbbbbbo", "obbwbbbbbbbo", "obbwwbbbbbbo", "obbbwwwwbbbo", ".obbbbbbbbo.",
                  ".oobbbbbboo.", "...oooooo..."],
                 {'b': '#3f6fd8', 'w': '#fbf1d6'}),       # blue coin with a pixel C
    'rainbow': (["............", "...oooooo...", "..orrrrrro..", ".orOOOOOOro.", "orOYYYYYYOro",
                 "oOYggggggYOo", "oYgbo..obgYo", "ogbo....obgo", "obo......obo", "oo........oo",
                 "............", "............"],
                {'r': '#d8452b', 'O': '#f08a24', 'Y': '#ffd95a', 'g': '#5c9a3e', 'b': '#3f6fd8'}),
    'trust': ([".oooooooooo.", ".obbbbbbbBo.", ".obbbbbbbBo.", ".obwwwwwbBo.", ".obbbwbbbBo.",
               ".obbbwbbbBo.", "..obbwbbBo..", "..obbbbbBo..", "...obbbBo...", "....obBo....",
               ".....oo.....", "............"],
              {'b': '#3f6fd8', 'B': '#2a4aa0', 'w': '#fbf1d6'}),   # shield with a T
    'walletconnect': (["............", "............", "............", ".oo......oo.", "obbo....obbo",
                       "obbbo..obbbo", ".obbboobbbo.", "..obbbbbbo..", "...obbbbo...", "....oooo....",
                       "............", "............"],
                      {'b': '#4f8ff7'}),   # a blue "bridge" wave
    'qr': (["oooo.o.oooo.", "o..o..oo..o.", "o..o.o.o..o.", "oooo.o.oooo.", "......o.....",
            "o.ooo.oo.oo.", ".o..o....o..", "oooo.oo.o.o.", "o..o..o.oo..", "o..o.o..o.o.",
            "oooo.oo.ooo.", "............"], {}),
}


def wallet_icon(name):
    rows, pal = WALLET_ICONS[name]
    return render(check(rows, 12), pal)
