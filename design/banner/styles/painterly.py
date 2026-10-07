"""Style B, "painterly pixel" (HD-2D-ish): crisp 2x pixel sprites + buildings over a softly painted,
depth-of-field-blurred mountain and sky, with light shafts from the sun (= the coin) and bloom.
Reuses the A layers from hd.py so composition and lore stay identical. Output: art/B-scene-1500x500.png"""
import os, math, random
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import hd
from kit import W, H, SUN, add_light

S = 2
WW, HH = W * S, H * S
SX, SY = SUN[0] * S, SUN[1] * S


def blur_rgba(im, r):
    """Gaussian blur with premultiplied alpha (no dark fringes)."""
    a = np.array(im).astype(np.float32) / 255
    al = a[..., 3:4]
    pre = np.concatenate([a[..., :3] * al, al], -1)
    chans = [np.array(Image.fromarray((pre[..., i] * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(r))).astype(np.float32) / 255
             for i in range(4)]
    out = np.stack(chans, -1)
    al2 = np.maximum(out[..., 3:4], 1e-4)
    rgb = np.clip(out[..., :3] / al2, 0, 1)
    return Image.fromarray((np.concatenate([rgb, out[..., 3:4]], -1) * 255).astype(np.uint8))


def up(layer, smooth):
    im = layer.im if hasattr(layer, 'im') else layer
    return im.resize((WW, HH), Image.BILINEAR if smooth else Image.NEAREST)


def shafts():
    """Crepuscular rays fanning from the sun across sky, mountain and square."""
    rnd = random.Random(11)
    L = Image.new('RGB', (WW, HH))
    d = ImageDraw.Draw(L)
    for i in range(26):
        a = math.radians(rnd.uniform(95, 265) if i % 3 else rnd.uniform(-60, 80))
        w = math.radians(rnd.uniform(1.2, 3.4))
        R = 1700
        p = [(SX, SY), (SX + R * math.cos(a - w), SY + R * math.sin(a - w)), (SX + R * math.cos(a + w), SY + R * math.sin(a + w))]
        k = rnd.uniform(.35, 1)
        d.polygon(p, fill=(int(70 * k), int(48 * k), int(24 * k)))
    L = L.filter(ImageFilter.GaussianBlur(10))
    # fade with distance from the sun and towards the foreground
    ys, xs = np.mgrid[0:HH, 0:WW]
    f = np.clip(1 - np.hypot(xs - SX, (ys - SY) * 1.3) / 1100, 0, 1) ** 1.2
    f *= np.clip(1.25 - ys / HH, 0, 1)
    return Image.fromarray((np.array(L) * f[..., None]).astype(np.uint8))


def painted_sky():
    sky = hd.sky_layer(WW, HH, dither=False)
    # soft painted clouds: A cloud shapes, upscaled smooth, blurred and softened at the edges
    cl = blur_rgba(up(hd.cloud_layer(), True), 3.2)
    sky.alpha_composite(cl)
    # canvas-like grain so the gradient feels painted, not digital
    rnd = np.random.default_rng(3)
    g = rnd.normal(0, 3.2, (HH // 2, WW // 2)).astype(np.float32)
    g = np.array(Image.fromarray(g + 128).resize((WW, HH), Image.BILINEAR)) - 128
    a = np.array(sky).astype(np.float32)
    a[..., :3] += g[..., None]
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))


def build():
    layers, emit, heads = hd.build()
    img = painted_sky()
    img.alpha_composite(blur_rgba(up(layers['hills'], True), 6))
    m = blur_rgba(up(layers['mountain'], True), 1.7)
    ma = np.array(m).astype(np.float32)                                   # painted: richer, contrastier greens
    mean = ma[..., :3].mean(-1, keepdims=True)
    ma[..., :3] = np.clip((ma[..., :3] - mean) * 1.35 + (mean - 128) * 1.12 + 128, 0, 255)
    img.alpha_composite(Image.fromarray(ma.astype(np.uint8)))      # depth of field: far = soft
    img.alpha_composite(blur_rgba(up(layers['treeline'], True), 1.8))
    # aerial haze band between the mountain and the square
    ys = np.arange(HH)[:, None]
    hz = np.clip(1 - np.abs(ys - 340) / 70, 0, 1) * .14
    a = np.array(img).astype(np.float32)
    a[..., :3] += (np.array((255, 176, 140), np.float32) - a[..., :3]) * hz[..., None]
    img = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))
    for k in ('buildings', 'plaza', 'props'):                               # focal plane: crisp pixels
        img.alpha_composite(up(layers[k], False))
    img.alpha_composite(blur_rgba(up(layers['fg'], False), 4.5))            # near foreground: tilt-shift blur
    rgb = hd.light_pass(img.convert('RGB'), emit, heads, scale=S)
    rgb = add_light(rgb, shafts(), 1.25)
    # bloom from the brightest areas (sun glow, windows, lamps)
    a = np.array(rgb).astype(np.float32)
    lum = a.mean(-1, keepdims=True)
    hi = np.clip((lum - 190) / 65, 0, 1) * a
    bloom = Image.fromarray(hi.astype(np.uint8)).filter(ImageFilter.GaussianBlur(16))
    rgb = add_light(rgb, bloom, .55)
    # gentle warm grade + vignette
    a = np.array(rgb).astype(np.float32)
    ys, xs = np.mgrid[0:HH, 0:WW]
    v = np.clip(1 - .28 * (np.hypot((xs - WW / 2) / WW, (ys - HH * .45) / HH) * 1.6) ** 2, .6, 1)
    a *= v[..., None]
    a[..., 2] *= .97
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))


if __name__ == '__main__':
    import sys
    here = os.path.dirname(os.path.abspath(__file__))
    img = build()
    img.save(f'{here}/art/B-scene-1500x500.png')
    if len(sys.argv) > 1:
        img.save(f'/tmp/logo/B_{sys.argv[1]}.png')
    print('B scene ok')
