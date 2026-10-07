"""Extra / overridden pixel assets for the v2 mockups. Reuses the v1 sprite code (design/mockups/art)."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'mockups', 'art'))
sys.dont_write_bytecode = True
from sprites import avatar  # noqa: E402

OUT = os.path.join(HERE, 'assets')
EXTRA = {
    'lumi': dict(outfit='robe', skin='warm', hair='chestnut', hairstyle='long', band=False),
}
for name, kw in EXTRA.items():
    a = avatar(**kw)
    a.save(f'{OUT}/av-{name}.png')
    a.crop((0, 0, 16, 16)).save(f'{OUT}/bust-{name}.png')
# outfit previews for the mobile profile, drawn on Juniper's own skin and hair
J = dict(skin='deep', hair='black', band=False)
OPTS = {
    'robe': dict(outfit='robe', **J),
    'hood': dict(outfit='robe', hood=True, **J),
    'plain': dict(outfit='shirt', shirt='#64408a', **J),
    'slogan': dict(outfit='shirt', shirt='#64408a', slogan=True, **J),
}
for name, kw in OPTS.items():
    avatar(**kw).save(f'{OUT}/opt-j-{name}.png')
print('v2 extra assets written')
