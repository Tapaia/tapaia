"""Tapaia Square in the official 'Cozy HD pixel' style with the new citizens standing in it.
Reuses the final X-header scene (../banner/final/header.py on top of ../banner/styles/hd.py) and swaps its
42 px people for the new 32x48 citizen sprites, so they get the same golden-hour rim light, warmth and shadows.
Outputs: out/scene-square-750x250.png (1 art px = 1 CSS px in the app banner; 2x for X / marketing) and
out/scene-square-empty-750x250.png (same plaza with nobody in it, for live citizens on top)."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, '..', 'banner', 'final'))
sys.dont_write_bytecode = True
import header                     # noqa: E402  (sets the final-header overrides on hd)
import hd                         # noqa: E402
import charkit as K               # noqa: E402
import citizens                   # noqa: E402

CAST = {n: c for n, _, c in citizens.CAST}
# (x, feet_y, citizen, turn): spread over the plaza between the props of the final header
PLACES = [
    (198, 216, 'Wren Halloway', 0), (240, 218, 'Corvin Ashdale', 0), (312, 214, 'Orla Fenwick', 0),
    (356, 241, 'Pim Tallow', 0), (552, 228, 'Nessa Quill', .8), (586, 233, 'Alder Meadows', 0),
    (652, 237, 'Odessa Brightmoss', 0), (466, 243, 'Tobin Larkspur', 0), (150, 238, 'Juniper Vale', 0),
    (272, 237, 'Sorrel Finch', .8),
]


def new_person(kind, *a):
    name, turn = kind.split('|')
    cfg = dict(CAST[name]); cfg['turn'] = float(turn)
    im = K.sprite(cfg)
    return im.crop(im.getbbox())


def render(places=PLACES):
    hd.PEOPLE = [(x, fy, f'{n}|{t}', None, None, None, None, False) for x, fy, n, t in places]
    hd.person = new_person
    layers, emit, heads = hd.build()
    return hd.compose(layers, emit, heads)


if __name__ == '__main__':
    os.makedirs(f'{HERE}/out', exist_ok=True)
    img = render()
    img.save(f'{HERE}/out/scene-square-750x250.png')
    K.up(img, 2).save(f'{HERE}/out/scene-square-1500x500.png')
    # empty plaza for the app: citizens are drawn live on top (see README, integration plan)
    empty = render([]).convert('RGB')
    # PNG8 (256 colours, no dither): ~38 KB instead of ~110 KB, visually identical at 1x
    empty.quantize(256, method=0, dither=0).save(f'{HERE}/out/scene-square-empty-750x250.png', optimize=True)
    print('scene ok')
