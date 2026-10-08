// Tapaia "Cozy HD pixel" citizens: a TypeScript port of design/characters/charkit.py (original art, GPL v3).
//
// Every citizen is a small config (skin, hair style + colour, eyes, expression, outfit, colours, accessories)
// rasterised natively at any size from shapes defined in *sprite space* (a 32x48 grid, head centre (16, 12.5),
// head radius 8.5). The same config renders the 32x48 sprite, the chat busts (24-64 px, re-rasterised, never
// upscaled) and larger figures (48x72, 80x120).
//
// Pipeline: shapes -> (material, tone) grid -> orphan cleanup -> cast-shadow contours -> hand-placed face
// templates -> soft coloured outline (no pure black). Top-left key light, 4 hue-shifted tones + 1 specular per
// material. The port mirrors the Python operation for operation (same float order, Python's round-half-even and
// modulo) so `scripts/test-avatar2.ts` can hold it to the Python goldens in design/characters/art/.
// Pure: no DOM. Returns RGBA pixels; the browser turns them into data URLs (src/ui.tsx).

export type RGB = [number, number, number];
export type Detail = 'S' | 'M' | 'L';

export type SkinKey = 'porcelain' | 'fair' | 'warm' | 'olive' | 'tan' | 'brown' | 'deep';
export type HairKey = 'black' | 'chestnut' | 'ginger' | 'blonde' | 'plum' | 'silver' | 'espresso' | 'auburn';
export type EyeKey = 'brown' | 'hazel' | 'green' | 'blue' | 'grey' | 'amber';
export type HairStyle = 'short' | 'swept' | 'long' | 'wavy' | 'braid' | 'bob' | 'ponytail' | 'bun' | 'elderbun' | 'curly' | 'crop';
export type Expr = 'smile' | 'grin' | 'laugh' | 'content' | 'surprised' | 'thoughtful' | 'shy' | 'wink' | 'calm';
export type Outfit2 = 'robe' | 'hood' | 'tee' | 'bandtee' | 'tunic' | 'cardigan' | 'apron' | 'coat';
export type Held = 'tea' | 'book';

/** Render config. Keys match charkit.py so the reference cast (design/characters/citizens.py) ports 1:1.
 *  Colour fields take a CLOTH key or a #rrggbb hex. */
export interface CitizenCfg {
  skin: SkinKey;
  hair: HairKey;
  hairstyle: HairStyle;
  eyes: EyeKey;
  expr: Expr;
  outfit: Outfit2;
  top: string;
  bottom: string;
  over?: string | null;      // apron colour
  accent?: string | null;    // cardigan inner shirt / band-shirt graphic / braid tie
  bottom_kind?: 'skirt';
  stockings?: string;
  neckband?: boolean;
  scarf?: string;
  satchel?: boolean;
  satchel_side?: number;
  glasses?: boolean;
  beard?: boolean;
  freckles?: boolean;
  blush?: boolean;
  held?: Held;
  pose?: 'down' | 'hold';
  hold_side?: number;
  book_col?: string;
  part?: number;
  tail_side?: number;
  braid_side?: number;
  rolled?: boolean;
  long_sleeve?: boolean;
  turn?: number;
}

// ------------------------------------------------------------------ Python-compatible numerics
/** Python's round(): half to even. */
export function pyRound(x: number): number {
  const f = Math.floor(x);
  const d = x - f;
  if (d > 0.5) return f + 1;
  if (d < 0.5) return f;
  return f % 2 === 0 ? f : f + 1;
}
/** numpy remainder / Python %: result takes the sign of the divisor. */
const pmod = (a: number, b: number) => { const m = a % b; return m !== 0 && (m < 0) !== (b < 0) ? m + b : m; };
const clip = (x: number, lo: number, hi: number) => Math.min(Math.max(x, lo), hi);
const abs = Math.abs, sqrt = Math.sqrt, sin = Math.sin, atan2 = Math.atan2, floor = Math.floor, PI = Math.PI;

// ------------------------------------------------------------------ colour helpers
export function rgb(c: string | RGB): RGB {
  if (typeof c !== 'string') return [c[0], c[1], c[2]];
  const h = c.replace('#', '');
  return [parseInt(h.slice(0, 2), 16), parseInt(h.slice(2, 4), 16), parseInt(h.slice(4, 6), 16)];
}
export function mix(a: string | RGB, b: string | RGB, k: number): RGB {
  const A = rgb(a), B = rgb(b);
  return [0, 1, 2].map((i) => pyRound(A[i] + (B[i] - A[i]) * k)) as RGB;
}
const SHADOW: RGB = [52, 26, 78];      // hue-shifted shadow target (plum-violet), never black
const LIGHT: RGB = [255, 243, 212];    // warm cream key light
const OUTL: RGB = [38, 20, 50];        // outline target (deep plum)
type Ramp = RGB[];

function makeRamp(base: string | RGB, sh: [number, number] = [0.58, 0.30], li: [number, number] = [0.24, 0.48], shadow: RGB = SHADOW, light: RGB = LIGHT, ol = 0.70): Ramp {
  const b = rgb(base);
  return [mix(b, shadow, sh[0]), mix(b, shadow, sh[1]), b, mix(b, light, li[0]), mix(b, light, li[1]), mix(b, OUTL, ol)];
}
function skinRamp(base: string): Ramp {
  // skin shadows go rosy-plum, not grey; outline is a warm deep brown-plum
  const b = rgb(base);
  const r = makeRamp(b, [0.42, 0.2], [0.26, 0.5], [128, 52, 86], [255, 240, 222], 0.66);
  r[5] = mix(b, [70, 28, 44], 0.72);
  return r;
}
const R6 = (...hs: string[]): Ramp => hs.map((h) => rgb(h));

// ------------------------------------------------------------------ palettes (book palette + design choices)
export const SKINS: Record<SkinKey, string> = {
  porcelain: '#f7dfca', fair: '#f0c8a4', warm: '#e2a87c', olive: '#c99968', tan: '#b47a4f', brown: '#8d5839', deep: '#663c2a',
};
export const HAIRS: Record<HairKey, string> = {
  black: '#2f2738', chestnut: '#7c4a2b', ginger: '#c25a2c', blonde: '#e2b456', plum: '#6c3a74', silver: '#bcb8cb', espresso: '#4a2c25', auburn: '#94372b',
};
export const EYES: Record<EyeKey, string> = { brown: '#6b3d24', hazel: '#7a6a2a', green: '#3d7d47', blue: '#3f6fae', grey: '#6b7590', amber: '#a8641e' };
/** Garment colours from design/visual-reference.md (leaf, robe, wood, parchment, walls, maple, hydrafill). */
export const CLOTH: Record<string, string> = {
  leaf: '#4f8a3e', moss: '#2f5a2e', sage: '#93b98a', robe: '#45275e', lilac: '#8a64b0',
  wood: '#9a6235', tan: '#c98d4f', parchment: '#f4e4bc', cream: '#fbf1d6', stone: '#8f877b',
  wallblue: '#8ea3b5', skyblue: '#a9c8db', beige: '#e6d3a8', maple: '#c8452e', rust: '#b4542e',
  hydra: '#f2c84b', navy: '#3b4466', plum: '#5b3a86', charcoal: '#4a4250', white: '#f3efe6',
  teal: '#3f7f7a', rose: '#d98a9a', mustard: '#d9a441', denim: '#55688f', brown: '#6b3f1f',
};
export const HAIRSTYLES: HairStyle[] = ['short', 'swept', 'crop', 'curly', 'long', 'wavy', 'bob', 'braid', 'ponytail', 'bun', 'elderbun'];
export const EXPRS: Expr[] = ['smile', 'grin', 'laugh', 'content', 'calm', 'shy', 'wink', 'surprised', 'thoughtful'];
export const OUTFITS2: Outfit2[] = ['robe', 'hood', 'tee', 'bandtee', 'tunic', 'cardigan', 'apron', 'coat'];
const cloth = (c: string) => CLOTH[c] ?? c;

const [LX, LY, LZ] = [-0.52, -0.58, 0.63];   // key light from top-left, towards the viewer
type Th = [number, number, number];
const QT: Th = [-0.12, 0.32, 0.80];
/** light value -> tone 0..3 */
const quant = (L: number, t: Th = QT) => (L < t[0] ? 0 : L < t[1] ? 1 : L < t[2] ? 2 : 3);

// ------------------------------------------------------------------ canvas
type Mask = Uint8Array;
type Arr = Float64Array;
type Tone = number | ArrayLike<number>;

class Canvas {
  n: number;
  X: Arr; Y: Arr;
  mat: Int32Array; tone: Int32Array; grp: Int32Array; z: Int32Array;
  mats: (string | null)[] = [null];
  ramps = new Map<string, Ramp>();
  over = new Map<number, RGB>();
  private _z = 0;
  constructor(public w: number, public h: number, public k = 1.0, public ox = 0.0, public oy = 0.0) {
    this.n = w * h;
    this.X = new Float64Array(this.n); this.Y = new Float64Array(this.n);
    for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) { const i = y * w + x; this.X[i] = ox + (x + 0.5) / k; this.Y[i] = oy + (y + 0.5) / k; }
    this.mat = new Int32Array(this.n); this.tone = new Int32Array(this.n); this.grp = new Int32Array(this.n); this.z = new Int32Array(this.n);
  }
  cx(sx: number) { return (sx - this.ox) * this.k; }
  /** pixel range [x0, x1) x [y0, y1) covering a sprite-space box, padded by a pixel */
  box(sx0: number, sx1: number, sy0: number, sy1: number): [number, number, number, number] {
    const f = (v: number, hi: number) => Math.min(hi, Math.max(0, v));
    return [f(floor(this.cx(sx0)) - 1, this.w), f(Math.ceil(this.cx(sx1)) + 1, this.w), f(floor(this.cy(sy0)) - 1, this.h), f(Math.ceil(this.cy(sy1)) + 1, this.h)];
  }
  cy(sy: number) { return (sy - this.oy) * this.k; }
  mid(name: string, ramp: Ramp) {
    if (!this.ramps.has(name)) { this.ramps.set(name, ramp); this.mats.push(name); }
    return this.mats.indexOf(name);
  }
  /** per-pixel helpers (the numpy expressions of charkit.py, one lambda per array) */
  F(f: (i: number) => number): Arr { const a = new Float64Array(this.n); for (let i = 0; i < this.n; i++) a[i] = f(i); return a; }
  M(f: (i: number) => boolean | number): Mask { const a = new Uint8Array(this.n); for (let i = 0; i < this.n; i++) a[i] = f(i) ? 1 : 0; return a; }
  paint(mask: Mask, name: string, ramp: Ramp, tone: Tone, grp: number) {
    let any = false;
    for (let i = 0; i < this.n; i++) if (mask[i]) { any = true; break; }
    if (!any) return;
    this._z += 1;
    const m = this.mid(name, ramp);
    const scalar = typeof tone === 'number';
    for (let i = 0; i < this.n; i++) {
      if (!mask[i]) continue;
      this.mat[i] = m;
      this.tone[i] = scalar ? (tone as number) : (tone as ArrayLike<number>)[i];
      this.grp[i] = grp;
      this.z[i] = this._z;
    }
  }
  put(x: number, y: number, c: RGB) {
    x = Math.trunc(x); y = Math.trunc(y);
    if (x >= 0 && x < this.w && y >= 0 && y < this.h) { const i = y * this.w + x; this.over.delete(i); this.over.set(i, c); }
  }
  /** Remove orphan tone pixels (a tone with no same-tone 4-neighbour inside the same material). */
  cleanup() {
    const { w, h, mat: m } = this;
    const t = this.tone.slice();
    const D = [[1, 0], [-1, 0], [0, 1], [0, -1]];
    for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) {
      const i = y * w + x;
      if (!m[i]) continue;
      const nb: number[] = [];
      for (const [dx, dy] of D) {
        const xx = x + dx, yy = y + dy;
        if (xx >= 0 && xx < w && yy >= 0 && yy < h && m[yy * w + xx] === m[i]) nb.push(t[yy * w + xx]);
      }
      if (nb.length >= 3 && !nb.includes(t[i])) {
        const cnt = new Map<number, number>();
        for (const v of nb) cnt.set(v, (cnt.get(v) ?? 0) + 1);
        let best = Infinity, bc = -1;
        for (const [v, c] of cnt) if (c > bc || (c === bc && v < best)) { best = v; bc = c; }
        this.tone[i] = best;
      }
    }
  }
  /** Cast-shadow contour: a pixel touching (from above/left/right) a different object painted in front of it drops
   *  `strength` tones. Separates hair from forehead, arms from torso, chin from neck. */
  contours(strength = 2, width?: number) {
    const { w, h, grp: g, z, mat: m } = this;
    width = width || Math.max(1, Math.trunc(pyRound(this.k * 0.8)));
    const out = this.tone.slice();
    for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) {
      const i = y * w + x;
      if (!m[i]) continue;
      let hit = 0;
      for (let d = 1; d <= width && !hit; d++) {
        for (let q = 0; q < 3; q++) {   // above, left, right
          const xx = q === 0 ? x : q === 1 ? x - d : x + d, yy = q === 0 ? y - d : y;
          if (xx >= 0 && xx < w && yy >= 0 && yy < h) {
            const j = yy * w + xx;
            if (m[j] && g[j] !== g[i] && z[j] > z[i]) { hit = d; break; }
          }
        }
      }
      if (hit) out[i] = Math.max(0, this.tone[i] - (hit === 1 ? strength : strength - 1));
    }
    this.tone = out;
  }
  image(outline = true): Pixels {
    const { w, h } = this;
    const data = new Uint8ClampedArray(w * h * 4);
    const byMat = this.mats.map((nm) => (nm ? this.ramps.get(nm)! : []));
    const ramp = (i: number) => byMat[this.mat[i]];
    const set = (i: number, c: RGB) => { data[i * 4] = c[0]; data[i * 4 + 1] = c[1]; data[i * 4 + 2] = c[2]; data[i * 4 + 3] = 255; };
    for (let i = 0; i < this.n; i++) if (this.mat[i]) set(i, ramp(i)[this.tone[i]]);
    for (const [i, c] of this.over) if (this.mat[i]) set(i, c);
    if (outline) {
      const src = data.slice();
      for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) {
        const i = y * w + x;
        if (src[i * 4 + 3]) continue;
        let best: RGB | null = null;
        for (const [dx, dy, lit] of [[0, 1, true], [1, 0, true], [-1, 0, false], [0, -1, false]] as [number, number, boolean][]) {
          const xx = x + dx, yy = y + dy;
          if (xx >= 0 && xx < w && yy >= 0 && yy < h && src[(yy * w + xx) * 4 + 3]) {
            const r = ramp(yy * w + xx);
            // sel-out: the lit (top/left) rim uses the material's deep tone, the shadow side its outline
            const c = lit ? mix(r[0], r[5], 0.45) : r[5];
            if (best === null || !lit) best = c;
          }
        }
        if (best) set(i, best);
      }
    }
    return { w, h, data };
  }
}

export interface Pixels { w: number; h: number; data: Uint8ClampedArray }

// ------------------------------------------------------------------ shapes (sprite space)
function ell(C: Canvas, cx: number, cy: number, rx: number, ry: number): [Mask, Arr] {
  // Only pixels whose centre can fall inside are evaluated (light outside an ellipse is never read: every caller
  // masks it, and the golden test would catch one that didn't).
  const m = new Uint8Array(C.n), L = new Float64Array(C.n);
  const [x0, x1, y0, y1] = C.box(cx - rx, cx + rx, cy - ry, cy + ry);
  for (let y = y0; y < y1; y++) for (let x = x0; x < x1; x++) {
    const i = y * C.w + x;
    const nx = (C.X[i] - cx) / rx, ny = (C.Y[i] - cy) / ry;
    const d = nx * nx + ny * ny;
    const nz = sqrt(clip(1 - d, 0, 1));
    m[i] = d <= 1 ? 1 : 0;
    L[i] = nx * LX + ny * LY + nz * LZ;
  }
  return [m, L];
}
function poly(C: Canvas, pts: [number, number][]): Mask {
  const out = new Uint8Array(C.n);
  const n = pts.length;
  const xs = pts.map((p) => p[0]), ys = pts.map((p) => p[1]);
  const [bx0, bx1, by0, by1] = C.box(Math.min(...xs), Math.max(...xs), Math.min(...ys), Math.max(...ys));
  for (let y = by0; y < by1; y++) for (let x = bx0; x < bx1; x++) {
    const p = y * C.w + x;
    const X = C.X[p], Y = C.Y[p];
    let inside = false;
    let j = n - 1;
    for (let i = 0; i < n; i++) {
      const xi = xs[i], yi = ys[i], xj = xs[j], yj = ys[j];
      if ((yi > Y) !== (yj > Y) && X < (xj - xi) * (Y - yi) / (yj - yi + 1e-12) + xi) inside = !inside;
      j = i;
    }
    out[p] = inside ? 1 : 0;
  }
  return out;
}
function capsule(C: Canvas, x0: number, y0: number, x1: number, y1: number, r0: number, r1?: number): [Mask, Arr] {
  const R1 = r1 === undefined ? r0 : r1;
  const dx = x1 - x0, dy = y1 - y0;
  const L2 = dx * dx + dy * dy;
  const m = new Uint8Array(C.n), L = new Float64Array(C.n);
  for (let i = 0; i < C.n; i++) {
    const X = C.X[i], Y = C.Y[i];
    const t = clip(((X - x0) * dx + (Y - y0) * dy) / L2, 0, 1);
    const px = x0 + t * dx, py = y0 + t * dy;
    const r = r0 + (R1 - r0) * t;
    const ddx = X - px, ddy = Y - py;
    const d = sqrt(ddx * ddx + ddy * ddy);
    const nx = ddx / Math.max(r, 1e-6);
    const ny = ddy / Math.max(r, 1e-6) * 0.35;
    const nz = sqrt(clip(1 - nx * nx, 0, 1));
    m[i] = d <= r ? 1 : 0;
    L[i] = nx * LX + ny * LY + nz * LZ - 0.05 * t;
  }
  return [m, L];
}
function cylLight(C: Canvas, cx: number, half: number, top: number, bot: number, bias = 0.0): Arr {
  return C.F((i) => {
    const nx = clip((C.X[i] - cx) / half, -1, 1);
    const nz = sqrt(clip(1 - nx * nx, 0, 1));
    const v = clip((C.Y[i] - top) / Math.max(1e-6, bot - top), 0, 1);
    return nx * LX + nz * LZ + (0.18 - 0.3 * v) + bias;
  });
}
const AND = (...ms: Mask[]) => { const o = ms[0].slice(); for (let i = 0; i < o.length; i++) for (let k = 1; k < ms.length; k++) o[i] &= ms[k][i]; return o; };
const OR = (...ms: Mask[]) => { const o = ms[0].slice(); for (let i = 0; i < o.length; i++) for (let k = 1; k < ms.length; k++) o[i] |= ms[k][i]; return o; };
const NOT = (m: Mask) => m.map((v) => (v ? 0 : 1));
const Q = (C: Canvas, L: Arr, t: Th = QT) => C.F((i) => quant(L[i], t));

// ------------------------------------------------------------------ the citizen renderer
const HC: [number, number] = [16.0, 12.5];
const HR = 8.5;
const [G_BACKHAIR, G_LEG, G_SHOE, G_LOW, G_TORSO, G_NECK, G_ARM_FAR, G_ARM, G_OVER, G_STRAP, G_SCARF, G_HEAD, G_BEARD, G_HAIR, G_HOOD, G_ITEM, G_BAND, G_COWL] =
  Array.from({ length: 18 }, (_, i) => i + 1);

export const DEFAULT_CITIZEN: CitizenCfg = {
  skin: 'warm', hair: 'chestnut', hairstyle: 'short', eyes: 'brown', expr: 'smile', outfit: 'tee',
  top: 'leaf', bottom: 'charcoal', over: null, accent: null, neckband: false, blush: true,
};

class Citizen {
  c: CitizenCfg;
  C!: Canvas; R!: Record<string, Ramp>; turn = 0; detail: Detail = 'S'; bc = 16;
  constructor(cfg: Partial<CitizenCfg>) { this.c = { ...DEFAULT_CITIZEN, ...cfg }; }

  // ---------------------------------------------------------------- ramps
  ramps(): Record<string, Ramp> {
    const c = this.c;
    const R: Record<string, Ramp> = {};
    R.skin = skinRamp(SKINS[c.skin]);
    R.hair = makeRamp(HAIRS[c.hair], [0.5, 0.25], [0.30, 0.58], SHADOW, [255, 214, 150], 0.62);
    if (c.hair === 'black') R.hair = R6('#1f1a28', '#2f2738', '#433a52', '#62587a', '#8f86ad', '#18121f');   // cool lilac sheen
    if (c.hair === 'silver') R.hair = R6('#7a7592', '#9a96ae', '#bcb8cb', '#dcd8e6', '#f6f3fb', '#4e4862');
    for (const k of ['top', 'bottom', 'over', 'accent'] as const) { const v = c[k]; if (v) R[k] = makeRamp(cloth(v)); }
    R.robe = R6('#24143a', '#331d4f', '#45275e', '#5e3a7e', '#7c58a0', '#1a0f28');
    R.band = R6('#a99bc2', '#bfb3d6', '#d9cfe6', '#efe9f7', '#ffffff', '#5e4f78');
    R.shoe = makeRamp('#5a3a2c', undefined, undefined, undefined, undefined, 0.6);
    R.leather = makeRamp('#7a4a2c');
    R.cup = R6('#c9b9a4', '#e2d6c2', '#f6efe2', '#fffaf0', '#ffffff', '#7d6656');
    R.tea = makeRamp('#7e9a3e');
    R.book = makeRamp(cloth(c.book_col ?? 'moss'));
    R.pages = R6('#c9b28a', '#e2cfa6', '#f4e4bc', '#fbf1d6', '#fffaf0', '#6e5a40');
    R.hoodsh = R6('#140b20', '#1d1029', '#271539', '#33204a', '#3f2a58', '#0f0818');
    R.gold = makeRamp('#e0a526');
    return R;
  }

  // ---------------------------------------------------------------- render
  render(C: Canvas, detail: Detail = 'S'): Pixels {
    const c = this.c, R = this.ramps();
    const turn = c.turn ?? 0.0;   // 0 front, +1 = facing viewer's right (3/4)
    const robe = c.outfit === 'robe' || c.outfit === 'hood';
    const hood = c.outfit === 'hood';
    Object.assign(this, { C, R, turn, detail });
    this.bc = 16 + turn * 1.9;   // centre line for front details (collars, buttons, aprons)
    if (!hood) this.hair(C, R, true);
    if (robe) this.robeBody(C, R);
    else { this.legs(C, R); this.torso(C, R); }
    if (!hood) {
      const d = turn * 1.0;
      const m = poly(C, [[14.1 + d, 17.5], [17.9 + d, 17.5], [17.9 + d, 23.2], [14.1 + d, 23.2]]);
      C.paint(m, 'skin', R.skin, 1, G_NECK);
      if (robe) this.cowl(C, R);
      if (c.neckband) {
        const m2 = poly(C, [[14.0, 19.7], [18.0, 19.7], [18.0, 21.5], [14.0, 21.5]]);
        const L = cylLight(C, 16, 2.4, 19.7, 21.5);
        C.paint(m2, 'band', R.band, Q(C, L, [-0.3, 0.3, 0.9]), G_BAND);
      }
    }
    if (!robe) this.overlays(C, R);
    if (hood) this.hood(C, R);
    else {
      this.head(C, R);
      if (c.beard) this.beard(C, R);
      this.hair(C, R, false);
      if (abs(turn) > 0.2) this.earTurned(C, R);
    }
    this.items(C, R);
    C.cleanup();
    C.contours();
    if (hood) this.hoodFace(C); else this.face(C);
    if (c.glasses) this.glasses(C);
    return C.image();
  }

  // ---------------------------------------------------------------- body parts
  legs(C: Canvas, R: Record<string, Ramp>) {
    const c = this.c, t = this.turn;
    const skirt = c.bottom_kind === 'skirt';
    for (const side of [-1, 1]) {
      const x = 16 + side * (2.6 - abs(t) * 0.5) + t * 0.7;
      const [m, L] = capsule(C, x, 33.5, x + side * 0.15, 43.0, 2.25, 2.0);
      if (skirt) C.paint(C.M((i) => m[i] && C.Y[i] > 38), 'legs', makeRamp(cloth(c.stockings ?? 'charcoal')), Q(C, L), G_LEG);
      else C.paint(m, 'bottom', R.bottom, Q(C, L), G_LEG);
      const [sm, sL] = ell(C, x + side * 0.5 + t * 1.0, 44.9, 2.7, 1.55);
      C.paint(C.M((i) => sm[i] && C.Y[i] > 43.4), 'shoe', R.shoe, C.F((i) => Math.min(quant(sL[i]), 2)), G_SHOE);
    }
    if (skirt) {
      const m = poly(C, [[11.2, 31.0], [20.8, 31.0], [22.6, 39.6], [9.4, 39.6]]);
      const L = cylLight(C, 16, 6.8, 31, 39.6);
      const tn = C.F((i) => {
        let v = quant(L[i]);
        const pl = abs(pmod((C.X[i] - 16) * 1.1 + (C.Y[i] - 31) * 0.0, 3.0) - 1.5) < 0.35 && C.Y[i] > 33;   // pleats
        if (pl) v = Math.max(0, v - 1);
        if (C.Y[i] > 38.8) v = Math.min(v, 1);
        return v;
      });
      C.paint(m, 'bottom', R.bottom, tn, G_LOW);
    } else {
      const m = poly(C, [[11.0, 31.0], [21.0, 31.0], [21.0, 35.5], [11.0, 35.5]]);
      C.paint(m, 'bottom', R.bottom, Q(C, cylLight(C, 16, 6, 31, 36)), G_LOW);
    }
  }

  torsoShape(C: Canvas, top = 22.0, bot = 32.6, flare = 0.0) {
    const t = this.turn;
    const sw = 6.7 - abs(t) * 1.1;
    const o = t * 0.7;
    return poly(C, [[16 - sw + o, top + 0.6], [16 - sw + 1.2 + o, top], [16 + sw - 1.2 + o, top], [16 + sw + o, top + 0.6],
      [16 + sw - 0.9 + flare + o, bot], [16 - sw + 0.9 - flare + o, bot]]);
  }

  torso(C: Canvas, R: Record<string, Ramp>) {
    const c = this.c, kind = c.outfit, turn = this.turn;
    const longSleeve = kind === 'tunic' || kind === 'cardigan' || kind === 'coat' || !!c.long_sleeve;
    const bot = kind === 'tunic' ? 37.6 : kind === 'coat' ? 39.2 : 32.6;
    const flare = kind === 'tunic' ? 1.6 : kind === 'coat' ? 1.4 : 0;
    const m = this.torsoShape(C, 22.0, bot, flare);
    if (abs(turn) > 0.2) this.arms(C, R, longSleeve, 'top', 'far');
    const L = cylLight(C, 16 + turn * 1.2, 7.0, 22, bot);
    let t = Q(C, L);
    const b = this.bc;
    if (kind === 'tunic') {   // V-neck + belt + hem band
      const v = poly(C, [[b - 1.4, 21.6], [b + 1.4, 21.6], [b, 25.4]]);
      t = C.F((i) => (C.Y[i] > bot - 1.1 ? Math.min(t[i], 1) : t[i]));
      C.paint(m, 'top', R.top, t, G_TORSO);
      C.paint(AND(v, m), 'skin', R.skin, 2, G_TORSO);
      const bm = C.M((i) => m[i] && C.Y[i] > 30.6 && C.Y[i] < 32.2);
      C.paint(bm, 'leather', R.leather, Q(C, cylLight(C, 16, 7, 30, 32)), G_STRAP);
      const bk = C.M((i) => abs(C.X[i] - b) < 1.0 && C.Y[i] > 30.6 && C.Y[i] < 32.2);
      C.paint(bk, 'gold', R.gold, 3, G_STRAP + 20);
    } else if (kind === 'coat') {
      C.paint(m, 'top', R.top, C.F((i) => (abs(C.X[i] - b) < 0.5 ? Math.max(0, t[i] - 1) : t[i])), G_TORSO);
      for (const side of [-1, 1]) {   // lapels
        const lap = poly(C, [[b, 21.8], [b + side * 3.6, 22.0], [b + side * 2.0, 27.5], [b + side * 0.2, 26.0]]);
        C.paint(lap, 'top', R.top, side < 0 ? 3 : 1, G_OVER);
      }
    } else {
      C.paint(m, 'top', R.top, t, G_TORSO);
      if (kind === 'tee' || kind === 'bandtee') {   // crew collar
        const [col] = ell(C, b - turn * 0.6, 21.6, 2.6, 1.4);
        C.paint(C.M((i) => col[i] && C.Y[i] > 21.6), 'top', R.top, 0, G_TORSO);
      }
    }
    if (kind === 'bandtee') {   // band-shirt slogan graphic [ch1: "slogans of their favorite bands"]
      const [g, gL] = ell(C, b, 26.6, 2.6 - abs(turn) * 0.5, 2.1);
      C.paint(g, 'accent', R.accent, C.F((i) => (gL[i] > 0.62 ? 3 : 2)), G_OVER);
      const star = C.M((i) => (abs(C.X[i] - b) < 0.6 && abs(C.Y[i] - 26.6) < 1.3) || (abs(C.Y[i] - 26.6) < 0.6 && abs(C.X[i] - b) < 1.3));
      C.paint(AND(star, g), 'cream', makeRamp(CLOTH.cream), 2, G_OVER + 30);
    }
    this.arms(C, R, longSleeve, 'top', abs(turn) > 0.2 ? 'near' : null);
  }

  arms(C: Canvas, R: Record<string, Ramp>, longSleeve: boolean, sr = 'top', only: 'far' | 'near' | null = null) {
    const c = this.c, t = this.turn;
    const pose = c.pose ?? (c.held ? 'hold' : 'down');
    for (const side of [-1, 1]) {
      const far = (t > 0.2 && side > 0) || (t < -0.2 && side < 0);
      if ((only === 'far' && !far) || (only === 'near' && far)) continue;
      const sx = 16 + side * (7.2 - abs(t) * (far ? 2.0 : 0.3)) + t * 0.7;
      let hx: number, hy: number, mid: [number, number] | null = null;
      if (pose === 'hold' && side === (c.hold_side ?? 1)) { hx = 16 + side * 3.6 + t * 1.6; hy = 29.6; mid = [sx + side * 0.6, 27.0]; }
      else { hx = sx + side * 0.5; hy = 32.4; }
      const grp = far ? G_ARM_FAR : G_ARM;
      let m: Mask, L: Arr;
      if (mid) {
        const [m1, L1] = capsule(C, sx, 23.6, mid[0], mid[1], 1.75);
        const [m2, L2] = capsule(C, mid[0], mid[1], hx, hy, 1.6);
        m = OR(m1, m2); L = C.F((i) => (m1[i] ? L1[i] : L2[i]));
      } else [m, L] = capsule(C, sx, 23.6, hx, hy - 0.6, 1.75, 1.6);
      const q = Q(C, L);
      if (longSleeve) {
        C.paint(m, sr, R[sr], q, grp);
        const cuff = C.M((i) => { const d = Math.hypot(C.X[i] - hx, C.Y[i] - hy); return m[i] && d < 2.6 && d > 1.3; });
        C.paint(cuff, sr, R[sr], C.F((i) => Math.max(0, q[i] - 1)), grp);
      } else {
        C.paint(m, 'skin', R.skin, q, grp);
        const sl = C.M((i) => m[i] && (mid ? C.Y[i] < 26.0 : C.Y[i] < 26.8));
        C.paint(sl, sr, R[sr], q, grp);
        if (c.rolled) C.paint(C.M((i) => m[i] && C.Y[i] >= 26.0 && C.Y[i] < 27.3), sr, R[sr], 3, grp);
      }
      const [hm, hL] = ell(C, hx, hy + 0.3, 1.45, 1.35);
      C.paint(hm, 'skin', R.skin, C.F((i) => Math.min(quant(hL[i]), 2)), grp);
    }
  }

  overlays(C: Canvas, R: Record<string, Ramp>) {
    const c = this.c, kind = c.outfit, b = this.bc;
    if (kind === 'cardigan') {   // open cardigan over the inner shirt (inner = accent)
      const inner = poly(C, [[b - 1.7, 21.8], [b + 1.7, 21.8], [b + 1.7, 32.6], [b - 1.7, 32.6]]);
      C.paint(inner, 'accent', R.accent, Q(C, cylLight(C, 16, 4, 22, 33)), G_OVER);
      for (const y of [25.0, 28.0, 31.0]) {   // buttons on the placket edge
        const [bt] = ell(C, b - 2.1, y, 0.6, 0.55);
        C.paint(bt, 'cream', makeRamp(CLOTH.cream), 2, G_OVER + 31);
      }
      const ts = this.torsoShape(C);
      C.paint(C.M((i) => ts[i] && C.Y[i] > 31.4 && !inner[i]), 'top', R.top, 1, G_OVER + 1);
      for (const side of [-1, 1]) {
        const pk = poly(C, [[b + side * 3.0, 28.4], [b + side * 4.6, 28.4], [b + side * 4.6, 30.6], [b + side * 3.0, 30.6]]);
        C.paint(pk, 'top', R.top, 1, G_OVER + 2);
      }
    }
    if (kind === 'apron') {   // bib apron with neck strap, waist ties and pocket (tea house)
      const d = b - 16;
      const bib = poly(C, [[13.0 + d, 24.2], [19.0 + d, 24.2], [19.6 + d, 30.6], [21.6 + d * 0.4, 31.0], [22.4 + d * 0.4, 40.2], [9.6 + d * 0.8, 40.2], [10.4 + d * 0.8, 31.0], [12.4 + d, 30.6]]);
      const L = cylLight(C, 16, 6.5, 24, 40);
      C.paint(bib, 'over', R.over, C.F((i) => (C.Y[i] > 39.2 ? Math.min(quant(L[i]), 1) : quant(L[i]))), G_OVER);
      const pk = poly(C, [[14.0 + d, 33.2], [18.0 + d, 33.2], [18.0 + d, 36.0], [14.0 + d, 36.0]]);
      C.paint(pk, 'over', R.over, C.F((i) => (C.Y[i] < 33.8 ? 0 : 1)), G_OVER + 1);
      for (const side of [-1, 1]) {
        const [st] = capsule(C, 16 + d + side * 2.6, 24.4, 16 + d * 0.6 + side * 2.0, 21.4, 0.45);
        C.paint(C.M((i) => st[i] && C.Y[i] < 24.6), 'over', R.over, 1, G_OVER + 2);
      }
      const ts = this.torsoShape(C, 22.0, 33);
      C.paint(C.M((i) => C.Y[i] > 30.6 && C.Y[i] < 31.6 && ts[i] && !bib[i]), 'over', R.over, 1, G_OVER + 3);
    }
    if (c.satchel) {   // strap from the near shoulder to the opposite hip
      const s = c.satchel_side ?? 1;
      const [st] = capsule(C, 16 - s * 5.2, 22.6, 16 + s * 4.8, 31.2, 0.55);
      C.paint(st, 'leather', R.leather, 1, G_STRAP);
      const bag = poly(C, [[16 + s * 3.0, 30.2], [16 + s * 8.6, 30.2], [16 + s * 8.4, 36.4], [16 + s * 3.2, 36.4]]);
      const L = cylLight(C, 16 + s * 5.8, 3.2, 30, 36.4);
      C.paint(bag, 'leather', R.leather, Q(C, L), G_ITEM - 1);
      C.paint(C.M((i) => bag[i] && C.Y[i] < 32.8), 'leather', R.leather, C.F((i) => Math.min(quant(L[i]) + 1, 3)), G_ITEM - 1);
      C.paint(C.M((i) => abs(C.X[i] - (16 + s * 5.8)) < 0.8 && abs(C.Y[i] - 32.9) < 0.7), 'gold', R.gold, 3, G_ITEM);
    }
    if (c.scarf) {   // knit scarf wrapped at the neck with one tail down the front
      const sr = makeRamp(cloth(c.scarf));
      let d = (b - 16) * 0.5;
      const [wrap] = capsule(C, 11.6 + d, 21.8, 20.4 + d, 21.8, 1.9);
      const L = cylLight(C, 16, 5, 20, 24);
      const S = this.detail === 'S';
      C.paint(wrap, 'scarf', sr, C.F((i) => { const v = quant(L[i]); return !S && pmod(pyRound(C.Y[i] * 1.0), 2) === 0 && v > 1 ? v - 1 : v; }), G_SCARF);
      d = b - 16;
      const tail = poly(C, [[13.0 + d, 22.4], [16.0 + d, 22.4], [15.6 + d, 31.2], [12.6 + d, 31.2]]);
      C.paint(tail, 'scarf', sr, C.F((i) => (pmod(floor(C.Y[i]), 3) === 0 ? 1 : C.X[i] < 14 ? 3 : 2)), G_SCARF + 1);
      const fr0 = poly(C, [[12.6 + d, 31.2], [15.6 + d, 31.2], [15.6 + d, 32.4], [12.6 + d, 32.4]]);
      C.paint(C.M((i) => fr0[i] && pmod(floor(C.X[i] * (S ? 1 : 2)), 2) === 0), 'scarf', sr, 1, G_SCARF + 1);
    }
  }

  /** Veridian Privacy Robe: loose dark purple dress, hood to ankles; same dark purple shoes with a high heel and
   *  deliberately uneven soles [ch1]. */
  robeBody(C: Canvas, R: Record<string, Ramp>) {
    const t = this.turn;
    for (const [side, heel] of [[-1, 0.0], [1, 0.8]]) {   // uneven: the right shoe stands on a taller heel
      const x = 16 + side * 2.6;
      const [sm, sL] = ell(C, x + side * 0.4, 44.9 - heel * 0.5, 2.5, 1.5);
      C.paint(C.M((i) => sm[i] && C.Y[i] > 43.0), 'robe', R.robe, C.F((i) => Math.min(quant(sL[i]), 2)), G_SHOE);
      C.paint(C.M((i) => abs(C.X[i] - (x - side * 1.2)) < 0.7 && C.Y[i] > 44.5 - heel * 0.5 && C.Y[i] < 46.6), 'robe', R.robe, 0, G_SHOE);
    }
    const body = poly(C, [[16 - 6.0 + t * 0.4, 22.4], [16 - 4.8 + t * 0.4, 21.6], [16 + 4.8 + t * 0.4, 21.6], [16 + 6.0 + t * 0.4, 22.4],
      [16 + 8.2 + t * 0.3, 43.8], [16 - 8.2 + t * 0.3, 43.8]]);
    const L = cylLight(C, 16 + t * 0.4, 8.0, 22, 44);
    const tn = C.F((i) => {
      let v = quant(L[i]);
      const X = C.X[i], Y = C.Y[i];
      const folds = (abs(X - (13.3 + t * 0.4)) < 0.45 || abs(X - (18.9 + t * 0.4)) < 0.45) && Y > 31 && Y < 43.4;
      if (folds) v = Math.max(0, v - 1);
      if (Y > 42.8) v = Math.min(v, 1);
      return v;
    });
    C.paint(body, 'robe', R.robe, tn, G_TORSO);
    C.paint(C.M((i) => body[i] && C.Y[i] > 42.8 && C.Y[i] < 43.8 && pmod(floor(C.X[i]), 4) === 1), 'robe', R.robe, 2, G_TORSO);
    for (const side of [-1, 1]) {   // wide bell sleeves, hands peeking out
      const far = (t > 0.2 && side > 0) || (t < -0.2 && side < 0);
      const sx = 16 + side * (6.0 - (far ? 1.6 : 0.2) * abs(t)) + t * 0.6;
      const [m, sl] = capsule(C, sx, 23.4, sx + side * 1.7, 31.4, 1.9, 2.7);
      C.paint(m, 'robe', R.robe, Q(C, sl), G_ARM);
      const [op] = ell(C, sx + side * 1.8, 32.3, 2.3, 0.95);
      C.paint(AND(op, m), 'robe', R.robe, 0, G_ARM);
      const [hm, hL] = ell(C, sx + side * 1.7, 33.4, 1.35, 1.15);
      C.paint(C.M((i) => hm[i] && C.Y[i] > 32.6), 'skin', R.skin, C.F((i) => Math.min(quant(hL[i]), 2)), G_ARM + 20);
    }
  }

  /** Hood down, bunched around the shoulders behind the neck. */
  cowl(C: Canvas, R: Record<string, Ramp>) {
    const [m, L] = ell(C, 16, 22.4, 7.4, 2.6);
    const tn = C.F((i) => { const v = quant(L[i], [-0.2, 0.25, 0.7]); const ridge = abs(C.X[i] - 12.5) < 0.45 || abs(C.X[i] - 19.5) < 0.45; return ridge ? Math.max(0, v - 1) : v; });
    C.paint(C.M((i) => m[i] && C.Y[i] > 20.6), 'robe', R.robe, tn, G_COWL);
  }

  // ---------------------------------------------------------------- head, face, hair
  uv(C: Canvas, shift = 0.0): [Arr, Arr] {
    return [C.F((i) => (C.X[i] - HC[0] - shift) / HR), C.F((i) => (C.Y[i] - HC[1]) / HR)];
  }
  faceMask(C: Canvas) {
    const [U, V] = this.uv(C);
    return C.M((i) => {
      const v = V[i];
      const w = v <= 0.3 ? 0.95 * sqrt(clip(1 - v * v, 0, 1)) : 0.906 + (0.40 - 0.906) * clip((v - 0.3) / 0.7, 0, 1) ** 1.25;
      return abs(U[i]) <= w && v >= -1 && v <= 1.0;
    });
  }
  head(C: Canvas, R: Record<string, Ramp>) {
    const t = this.turn;
    const [U, V] = this.uv(C);
    const fm = this.faceMask(C);
    const tn = C.F((i) => {
      const nx = U[i] / 0.95, ny = V[i];
      const nz = sqrt(clip(1 - nx * nx * 0.9 - ny * ny * 0.5, 0, 1));
      const L = nx * LX + ny * LY * 0.6 + nz * LZ + 0.1;
      const v = quant(L, [-0.2, 0.29, 0.86]);
      return V[i] > 0.55 && abs(U[i]) > 0.25 ? Math.min(v, 1) : v;
    });
    for (const side of [-1, 1]) {   // ears (near ear only when turned)
      if (abs(t) > 0.2) continue;
      const [em] = ell(C, 16 + side * 8.25, 14.3, 1.25, 1.75);
      C.paint(C.M((i) => em[i] && !fm[i]), 'skin', R.skin, side > 0 ? 1 : 2, G_HEAD - 1);
    }
    C.paint(fm, 'skin', R.skin, tn, G_HEAD);
  }
  earTurned(C: Canvas, R: Record<string, Ramp>) {
    const t = this.turn;
    const s = t > 0 ? -1 : 1;
    const ex = 16 + s * HR * (0.95 - 0.5 * abs(t));
    const [em] = ell(C, ex, 14.4, 1.2, 1.7);
    C.paint(em, 'skin', R.skin, C.F((i) => (C.X[i] < ex ? 2 : 1)), G_HEAD + 50);
    const [inner] = ell(C, ex + 0.2, 14.6, 0.45, 0.8);
    C.paint(AND(inner, em), 'skin', R.skin, 0, G_HEAD + 50);
  }
  /** face x position in sprite space; a 3/4 turn compresses and shifts the features */
  fx(du: number) { const t = this.turn; return HC[0] + (du * (1 - 0.3 * abs(t)) + t * 0.3) * HR; }

  face(C: Canvas) {
    const c = this.c, R = this.R, det = this.detail;
    const sk = R.skin;
    const eyec = rgb(EYES[c.eyes]);
    const K = det !== 'L' ? mix(R.hair[5], OUTL, 0.35) : mix(R.hair[5], OUTL, 0.2);
    const D = mix(eyec, OUTL, 0.55), I = eyec, Ih = mix(eyec, [255, 255, 255], 0.35);
    const W: RGB = [255, 251, 240];
    const S = mix(sk[2], [255, 255, 255], 0.55);   // sclera (warm white)
    const Mc = mix(rgb('#b04a5e'), sk[2], 0.15);
    const Md = mix(rgb('#7a2a44'), OUTL, 0.2);
    const T = rgb('#fffaf2'), Tg = rgb('#e2788a');
    const B = mix(sk[2], rgb('#ff7f8e'), 0.45);
    const expr = c.expr;
    const tpl = TEMPLATES[det];
    const eyeDy = { S: 13.9, M: 13.9, L: 13.7 }[det];
    const ex = tpl.eye_dx;
    const ek = ({ laugh: 'closed', content: 'closed', wink: 'open', surprised: 'wide' } as Record<string, string>)[expr] ?? 'open';
    for (const side of [-1, 1]) {   // eyes
      let key = ek;
      if (expr === 'wink' && side > 0) key = 'closed';
      if (expr === 'shy') key = 'side';
      let rows = tpl.eye[key];
      const far = (this.turn > 0.3 && side < 0) || (this.turn < -0.3 && side > 0);
      if (far && rows[0].length > 2) rows = rows.map((r) => r.slice(1));
      this.stamp(C, rows, this.fx(side * ex), eyeDy, { K, D, I, i: Ih, W, S }, side > 0);
    }
    const bk = ({ surprised: 'up', thoughtful: 'raise', shy: 'soft', content: 'soft', laugh: 'up' } as Record<string, string>)[expr] ?? 'base';
    for (const side of [-1, 1]) {   // brows
      const rows = tpl.brow[bk === 'raise' && side < 0 ? 'base' : bk];
      this.stamp(C, rows, this.fx(side * ex), eyeDy - tpl.brow_dy, { H: mix(R.hair[1], OUTL, 0.25), h: R.hair[2] }, side > 0);
    }
    if (tpl.nose) this.stamp(C, tpl.nose, this.fx(0.02 + this.turn * 0.05), eyeDy + tpl.nose_dy, { n: sk[1], N: sk[0], h: sk[3] });
    if (c.blush ?? true) for (const side of [-1, 1])
      this.stamp(C, tpl.blush, this.fx(side * (ex + tpl.blush_dx)), eyeDy + tpl.blush_dy, { b: B, f: mix(sk[1], [150, 70, 60], 0.3) }, side > 0);
    if (c.freckles) for (const side of [-1, 1])
      this.stamp(C, tpl.freckles, this.fx(side * (ex + 0.02)), eyeDy + tpl.blush_dy - 0.6, { f: mix(sk[1], [120, 60, 40], 0.35) }, side > 0);
    const mk = ({ smile: 'smile', grin: 'grin', laugh: 'laugh', content: 'smile', surprised: 'o', thoughtful: 'flat', shy: 'small', wink: 'smirk', calm: 'small' } as Record<string, string>)[expr] ?? 'smile';
    let mp: Record<string, RGB> = { M: Mc, m: Md, T, t: Tg, l: sk[1], L: sk[3] };
    if (c.beard) mp = { M: mix(R.hair[0], Md, 0.5), m: mix(R.hair[0], OUTL, 0.4), T, t: Tg };
    this.stamp(C, tpl.mouth[mk], this.fx(0), eyeDy + tpl.mouth_dy, mp);
  }

  /** Place a pixel template centred on sprite point (sx, sy); right-side features mirror the template. */
  stamp(C: Canvas, rows: string[], sx: number, sy: number, pal: Record<string, RGB>, mirror = false) {
    const h = rows.length, w = rows[0].length;
    if (mirror) rows = rows.map((r) => r.split('').reverse().join(''));
    const x0 = pyRound(C.cx(sx) - w / 2);
    const y0 = pyRound(C.cy(sy) - h / 2);
    rows.forEach((r, j) => r.split('').forEach((ch, i) => { if (ch in pal) C.put(x0 + i, y0 + j, pal[ch]); }));
  }

  beard(C: Canvas, R: Record<string, Ramp>) {
    const [U, V] = this.uv(C);
    const fm = this.faceMask(C);
    const m = C.M((i) => {
      const u = U[i], v = V[i];
      const a = fm[i] && v > 0.42 && !(v < 0.78 && abs(u) < 0.30) && abs(u) < 0.9;
      const mu = fm[i] && v > 0.44 && v < 0.58 && abs(u) < 0.42;
      return a || mu;
    });
    C.paint(m, 'hair', R.hair, C.F((i) => quant(U[i] * LX + 0.45 + 0.1 * sin(C.X[i] * 3.1))), G_BEARD);
  }

  hoodFace(C: Canvas) {
    const tpl = TEMPLATES[this.detail];
    const g1 = rgb('#d8c8ff'), g2 = rgb('#ffffff');
    for (const side of [-1, 1]) this.stamp(C, tpl.glint, this.fx(side * tpl.eye_dx * 0.92), 13.6, { g: g1, G: g2, d: rgb('#5c4482') }, side > 0);
  }

  /** Hood up with the front face cover; a strap across below the eyes tightens it [ch1:132, ch1:140]. */
  hood(C: Canvas, R: Record<string, Ramp>) {
    const t = this.turn;
    const [m1, L1] = ell(C, 16 - t * 0.3, 11.9, 9.6 - abs(t) * 0.3, 9.8);
    const peak = poly(C, [[14.0 + t * 0.6, 2.9], [16.2 + t * 0.6, 1.2], [18.0 + t * 0.6, 2.9]]);
    const drape = poly(C, [[8.9, 15.0], [23.1, 15.0], [22.7, 23.4], [9.3, 23.4]]);
    const hm = OR(m1, peak, drape);
    const dl = cylLight(C, 16, 7.5, 15, 24);
    const tn = C.F((i) => {
      let v = quant(L1[i] + 0.05);
      if (drape[i] && !m1[i]) v = clip(quant(dl[i]) - 1, 0, 3);
      if (peak[i] && !m1[i]) v = 2;
      return v;
    });
    C.paint(hm, 'robe', R.robe, tn, G_HOOD - 1);
    const ocx = 16 + t * 2.6;   // face opening: deep shadow above the strap, cover below
    const [om] = ell(C, ocx, 14.0, 6.3, 7.0);
    C.paint(om, 'hoodsh', R.hoodsh, C.F((i) => (C.Y[i] < 11.6 ? 1 : 2)), G_HOOD);
    const [rimE] = ell(C, ocx, 14.0, 7.2, 7.9);   // inner rim of the hood: lit on the left
    C.paint(C.M((i) => rimE[i] && !om[i] && m1[i]), 'robe', R.robe, C.F((i) => (C.X[i] < ocx ? 3 : 1)), G_HOOD - 1);
    const strapY0 = 15.5, strapY1 = 16.9;
    const cl = cylLight(C, ocx, 6.3, 16, 21);
    C.paint(C.M((i) => om[i] && C.Y[i] >= strapY1), 'robe', R.robe,
      C.F((i) => { const ct = quant(cl[i]); const pleat = abs(C.X[i] - ocx) < 0.45 && C.Y[i] > 17.5; return pleat ? Math.max(0, ct - 1) : Math.min(ct, 3); }), G_HOOD + 1);
    const strap = C.M((i) => om[i] && C.Y[i] >= strapY0 && C.Y[i] < strapY1);
    C.paint(strap, 'band', R.band, C.F((i) => (C.X[i] < 15 + t * 2.6 ? 3 : 1)), G_HOOD + 2);
    C.paint(C.M((i) => strap[i] && abs(C.X[i] - (21.0 + t * 2.6)) < 0.8), 'gold', R.gold, 2, G_HOOD + 3);
  }

  hair(C: Canvas, R: Record<string, Ramp>, back: boolean) {
    const c = this.c, st = c.hairstyle, t = this.turn;
    const [U, V] = this.uv(C, t * 0.5);
    const part = (c.part ?? 0.0) + t * 0.25;
    const hr = R.hair;
    const big = this.detail === 'L';
    const n = C.n;
    const strands = (tn: Arr, angK = 11.0, w = 0.18, cx: number = part, cy = -1.15) => {
      const k_ = angK * (big ? 1.55 : 1.0);
      return C.F((i) => {
        const th = atan2(V[i] - cy, U[i] - cx);
        const ph = pmod(th * k_ / PI + 0.07 * sin(V[i] * 9), 1.0);
        let v = tn[i];
        if (ph < w && v >= 2) v = v - 1;
        if (big && ph > 0.5 && ph < 0.62 && v === 2) v = 3;   // lighter strand ridges between the clump lines
        return v;
      });
    };
    if (back) {
      if (st === 'long' || st === 'wavy' || st === 'bob' || st === 'braid') {
        const Lb = { long: 2.25, wavy: 1.75, bob: 0.95, braid: 0.9 }[st];
        const wb = { long: 1.18, wavy: 1.26, bob: 1.16, braid: 1.1 }[st];
        const m = new Uint8Array(n);
        let tn: Arr = new Float64Array(n);
        for (let i = 0; i < n; i++) {
          const u = U[i], v = V[i];
          const yy = clip((v + 0.2) / (Lb + 0.2), 0, 1);
          const width = wb * (1 - 0.12 * yy ** 3);
          const edge = Lb + (st !== 'wavy' ? 0.07 * sin(u * 17) : 0.12 * sin(u * 9));
          m[i] = abs(u) < width && v > -0.4 && v < edge ? 1 : 0;
          const L = -abs(u) / width * 0.5 + 0.25 - 0.25 * yy;
          let q = quant(L, [-0.2, 0.12, 0.5]);
          if (st === 'wavy' && sin(v * 9 + abs(u) * 4) > 0.55 && q > 0) q = q - 1;
          tn[i] = q;
        }
        tn = strands(tn, 14, 0.2, 0, -1.5);
        C.paint(m, 'hair', hr, C.F((i) => Math.min(tn[i], 2)), G_BACKHAIR);
      }
      if (st === 'ponytail') {   // tail swings out behind the head on one side
        const s = c.tail_side ?? 1;
        const [m, L] = capsule(C, 16 + s * 6.0, 6.0, 16 + s * 9.4, 17.5, 2.5, 1.0);
        const [m2] = capsule(C, 16 + s * 9.4, 17.5, 16 + s * 8.4, 21.5, 1.0, 0.5);
        C.paint(OR(m, m2), 'hair', hr, C.F((i) => Math.min(quant(L[i], [-0.25, 0.15, 0.6]), 3)), G_BACKHAIR);
      }
      return;
    }
    // base ellipsoid light for the hair mass
    const L = new Float64Array(n), rho = new Float64Array(n);
    for (let i = 0; i < n; i++) {
      const nx = (U[i] - 0.0) / 1.12, ny = (V[i] - -0.12) / 1.06;
      const nz = sqrt(clip(1 - nx * nx - ny * ny, 0, 1));
      L[i] = nx * LX + ny * LY + nz * LZ; rho[i] = sqrt(nx * nx + ny * ny);
    }
    if (st === 'curly') {   // a cloud of individual curls, each lit like a little sphere
      CURLS.forEach(([cu, cv, rr], j) => {
        const [m, Lc] = ell(C, HC[0] + t * 0.5 + cu * HR, HC[1] + cv * HR, rr * HR, rr * HR);
        C.paint(m, 'hair', hr, C.F((i) => quant(Lc[i] * 0.9 + 0.06, [-0.05, 0.38, 0.82])), G_HAIR + 40 + (j % 2));
      });
      return;
    }
    if (st === 'crop') {
      const S = this.detail === 'S';
      const m = C.M((i) => {
        const u = U[i], v = V[i];
        const a = u / 1.04, b = (v + 0.16) / 0.98;
        const edge = abs(u) < 0.8 ? -0.52 + 0.06 * abs(sin(u * 9)) : 0.05;
        return a * a + b * b <= 1 && v < edge;
      });
      C.paint(m, 'hair', hr, C.F((i) => { const v = quant(L[i] - 0.05); return !S && pmod(floor(C.X[i]) + floor(C.Y[i]), 3) === 0 && v === 2 ? 1 : v; }), G_HAIR);
      return;
    }
    const cap = C.M((i) => { const a = U[i] / 1.11, b = (V[i] + 0.12) / 1.05; return a * a + b * b <= 1; });
    let m: Mask;
    if (st === 'short') {   // tousled short: tufted fringe, cropped sides
      const tuft = poly(C, [[13.0, 4.6], [14.4, 2.4], [16.2, 3.0], [17.6, 1.7], [18.4, 3.4], [19.6, 4.6]]);
      m = C.M((i) => {
        const u = U[i], v = V[i];
        const fringe = -0.40 + 0.16 * abs(sin((u - part) * 7.5));
        return (cap[i] && v < (abs(u) < 0.8 ? fringe : 0.12)) || (tuft[i] && v < -0.6);
      });
    } else if (st === 'swept') {   // a long sweep falling from the parting across the forehead to the opposite brow
      m = C.M((i) => {
        const u = U[i], v = V[i];
        const k_ = clip((u - part + 0.25) / 1.25, 0, 1);
        let fringe = -0.62 + 0.52 * k_ ** 0.8 + 0.06 * abs(sin(u * 10));
        if (u < part - 0.25) fringe = -0.62 + 0.1 * abs(sin(u * 8));
        return cap[i] && v < (abs(u) < 0.82 ? fringe : u > 0 ? 0.32 : 0.1);
      });
    } else if (st === 'long' || st === 'wavy' || st === 'braid') {   // curtain fringe, locks framing the face
      const lockLen = { long: 1.75, wavy: 1.45, braid: 0.65 }[st];
      m = C.M((i) => {
        const u = U[i], v = V[i];
        const fringe = -0.70 + 0.55 * abs(u - part) ** 0.9 + 0.05 * abs(sin(u * 12));
        const wave = st === 'wavy' ? 0.06 * sin(v * 10) : 0;
        const locks = abs(u) > 0.72 + wave && abs(u) < 1.13 + wave && v > -0.3 && v < lockLen - 0.25 * (abs(u) - 0.72);
        return (cap[i] && v < (abs(u) < 0.74 ? fringe : 9)) || locks;
      });
    } else if (st === 'bob') {
      m = C.M((i) => {
        const u = U[i], v = V[i];
        const fringe = -0.42 + 0.08 * abs(sin(u * 10)) + 0.1 * (u - part);
        const locks = abs(u) > 0.72 && abs(u) < 1.16 && v > -0.3 && v < 0.82 + 0.05 * sin(u * 15);
        return (cap[i] && v < (abs(u) < 0.76 ? fringe : 9)) || locks;
      });
    } else if (st === 'ponytail') {
      m = C.M((i) => { const u = U[i]; const fringe = -0.6 + 0.1 * abs(sin(u * 6)); return cap[i] && V[i] < (abs(u) < 0.82 ? fringe : 0.05); });
    } else if (st === 'bun' || st === 'elderbun') {
      const bun = st === 'bun';
      m = C.M((i) => {
        const u = U[i];
        const fringe = bun ? -0.52 + 0.07 * abs(sin(u * 11)) : -0.5 + 0.22 * abs(u) ** 1.5;
        return cap[i] && V[i] < (abs(u) < 0.8 ? fringe : bun ? 0.1 : 0);
      });
      if (bun) for (const s of [-1, 1]) m = OR(m, capsule(C, 16 + s * 7.6, 10.5, 16 + s * 7.9, 17.5, 0.55)[0]);   // loose tendrils
    } else {
      m = C.M((i) => cap[i] && V[i] < -0.4);
    }
    if (abs(t) > 0.2) {   // 3/4: the back of the head shows on the near side, behind the ear
      const s = t > 0 ? -1 : 1;
      const lim = 0.95 - 0.5 * abs(t) - 0.1;
      const mm = m;
      m = C.M((i) => {
        const Uh = (C.X[i] - HC[0]) / HR;
        const a = Uh / 1.1, b = (V[i] + 0.1) / 1.06;
        return mm[i] || (a * a + b * b <= 1 && Uh * s > lim && V[i] < 0.42);
      });
    }
    let tn = Q(C, L, [-0.18, 0.28, 0.8]);
    tn = strands(tn);
    const tn2 = C.F((i) => {   // shine band, then cylinder shading on the side locks so they don't look pasted on
      const u = U[i], v = V[i];
      let q = tn[i];
      const band = rho[i] > 0.5 && rho[i] < 0.7 && u < 0.25 - (v + 0.4) * 0.2 && v < -0.15 && v > -1.0;
      const brk = pmod(atan2(v + 1.15, u - part) * 13 / PI, 1.0) < 0.62;
      if (band && brk) q = u < -0.25 ? 4 : 3;
      if (abs(u) > 0.74 && v > -0.05) q = u < 0 ? (abs(u) > 0.98 ? 1 : 2) : (abs(u) > 0.98 ? 0 : 1);
      return q;
    });
    C.paint(m, 'hair', hr, tn2, G_HAIR);
    if (st === 'bun' || st === 'elderbun') {   // drawn after the cap so it casts a contour onto it
      const bun = st === 'bun';
      const by = bun ? -1.17 : -1.1;
      const cy = HC[1] + by * HR;
      const [bm, bL] = ell(C, 16 + t * 0.5, cy, bun ? 3.7 : 4.0, bun ? 2.7 : 2.3);
      C.paint(bm, 'hair', hr, C.F((i) => { const q = quant(bL[i]); return pmod(atan2(C.Y[i] - cy, C.X[i] - 16) * 4 / PI, 1) < 0.22 && q >= 2 ? q - 1 : q; }), G_HAIR + 30);
    }
    if (st === 'braid') {   // side braid over the shoulder
      const s = c.braid_side ?? 1;
      for (let i = 0; i < 6; i++) {
        const [bm, bL] = ell(C, 16 + s * (7.0 - i * 0.45), 18.2 + i * 2.35, 1.75 - i * 0.07, 1.35);
        C.paint(bm, 'hair', hr, Q(C, bL, [-0.3, 0.2, 0.7]), G_HAIR + 1 + i);
      }
      const [tie] = ell(C, 16 + s * 4.3, 32.0, 1.0, 0.65);
      C.paint(tie, R.accent ? 'accent' : 'band', R.accent ?? R.band, 2, G_HAIR + 8);
      const [tip, tL] = ell(C, 16 + s * 4.2, 33.4, 1.1, 1.0);
      C.paint(tip, 'hair', hr, Q(C, tL), G_HAIR + 9);
    }
  }

  // ---------------------------------------------------------------- accessories
  items(C: Canvas, R: Record<string, Ramp>) {
    const c = this.c, held = c.held, s = c.hold_side ?? 1;
    if (held === 'tea') {
      const x = 16 + s * 3.6 + this.turn * 1.6, y = 28.4;
      const cup = poly(C, [[x - 2.0, y - 1.8], [x + 2.0, y - 1.8], [x + 1.6, y + 1.2], [x - 1.6, y + 1.2]]);
      C.paint(cup, 'cup', R.cup, Q(C, cylLight(C, x, 2.0, y - 2, y + 1)), G_ITEM);
      const [hd] = ell(C, x - s * 2.6, y - 0.4, 1.05, 1.05);
      const [hole] = ell(C, x - s * 2.6, y - 0.4, 0.45, 0.45);
      C.paint(C.M((i) => hd[i] && !hole[i] && !cup[i]), 'cup', R.cup, 1, G_ITEM);
      const tea = poly(C, [[x - 1.6, y - 1.9], [x + 1.6, y - 1.9], [x + 1.6, y - 1.1], [x - 1.6, y - 1.1]]);
      C.paint(tea, 'tea', R.tea, 2, G_ITEM + 1);
      const [sau] = ell(C, x, y + 1.6, 3.0, 0.75);
      C.paint(sau, 'cup', R.cup, C.F((i) => (C.X[i] < x ? 3 : 1)), G_ITEM + 2);
      const [hm] = ell(C, x + s * 0.4, y + 2.5, 1.5, 1.0);   // hand under the saucer
      C.paint(hm, 'skin', R.skin, 2, G_ITEM + 3);
    }
    if (held === 'book') {   // a book held against the chest: cover, page edge, title band
      const x = 16 + s * 3.4 + this.turn * 1.6, y = 28.8;
      const cov = poly(C, [[x - 2.4, y - 3.2], [x + 2.4, y - 3.2], [x + 2.4, y + 3.0], [x - 2.4, y + 3.0]]);
      C.paint(cov, 'book', R.book, C.F((i) => (C.X[i] < x - 1.5 ? 3 : C.X[i] > x + 1.6 ? 1 : 2)), G_ITEM);
      const pg = s > 0 ? poly(C, [[x + 1.6, y - 2.8], [x + 2.6, y - 2.8], [x + 2.6, y + 2.6], [x + 1.6, y + 2.6]])
        : poly(C, [[x - 2.6, y - 2.8], [x - 1.6, y - 2.8], [x - 1.6, y + 2.6], [x - 2.6, y + 2.6]]);
      C.paint(pg, 'pages', R.pages, 2, G_ITEM + 1);
      C.paint(C.M((i) => cov[i] && abs(C.Y[i] - (y - 0.8)) < 0.55 && !pg[i]), 'gold', R.gold, 3, G_ITEM + 2);
      const [hm] = ell(C, x - s * 0.6, y + 3.1, 1.5, 1.1);
      C.paint(hm, 'skin', R.skin, 2, G_ITEM + 3);
    }
  }

  glasses(C: Canvas) {
    const det = this.detail, tpl = TEMPLATES[det];
    const col = rgb(det === 'S' ? '#8a6038' : '#7a5530'), hi = rgb('#e8d2a0');
    for (const side of [-1, 1]) this.stamp(C, tpl.glasses, this.fx(side * tpl.eye_dx), 13.9, { o: col, h: hi }, side > 0);
    this.stamp(C, tpl.bridge, this.fx(0), 13.9 - tpl.bridge_dy, { o: col });
  }
}

// ------------------------------------------------------------------ face templates (hand-placed pixels)
// Left eye as seen by the viewer; the right one is mirrored. K lash/lid, D dark iris, I iris, i light iris,
// W highlight, S sclera. Mouth: M lip, m dark mouth, T teeth, t tongue, l/L skin shade/light.
// S: 32x48 sprite and <=32 px busts; M: 36-48 px busts; L: 64 px portraits and large figures.
interface Tpl {
  eye_dx: number; brow_dy: number; mouth_dy: number; nose_dy: number; blush_dx: number; blush_dy: number; bridge_dy: number;
  eye: Record<string, string[]>; brow: Record<string, string[]>; nose: string[]; blush: string[]; freckles: string[];
  mouth: Record<string, string[]>; glint: string[]; glasses: string[]; bridge: string[];
}
const CURLS: [number, number, number][] = [[-0.9923113300096694, -0.1166324355857375, 0.27283393495054337], [0.9923113300096694, -0.11663243558573703, 0.29177959413595334], [-0.920553566194246, 0.15252797789472078, 0.2980217903408206], [0.920553566194246, 0.15252797789472083, 0.2990040406305188], [-0.9742070994719119, -0.3933424712221374, 0.2983610615978931], [0.9742070994719118, -0.3933424712221381, 0.2518611044760152], [-0.8678803623235316, -0.6525437477304679, 0.2828889596204619], [0.8678803623235316, -0.6525437477304679, 0.2867629753076252], [-0.7171734081838053, -0.4413294131305918, 0.24983053448428194], [0.7171734081838053, -0.44132941313059176, 0.2969386384068938], [0.6829598836146339, -0.870763446710376, 0.2660874919442668], [-0.6829598836146338, -0.8707634467103762, 0.28186372947583627], [-0.66, -0.47, 0.2], [0.66, -0.51, 0.2], [-0.584645118988404, -0.6535509373948221, 0.27584003663597156], [0.5846451189884039, -0.6535509373948223, 0.2661687988127879], [-0.4361917414267448, -1.0282399704007106, 0.2529653697348226], [0.43619174142674444, -1.0282399704007108, 0.25517894174300665], [-0.4222739868852924, -0.4253999999999999, 0.27717835915610367], [0.4222739868852924, -0.4253999999999999, 0.2660445632826662], [-0.396, -0.51, 0.2], [0.396, -0.47, 0.2], [-0.3816000000000004, -0.8110675249102997, 0.2405391658600533], [0.3815999999999995, -0.8110675249103001, 0.29739917806285415], [-0.24380000000000024, -0.5904042520260249, 0.2819773579149019], [0.2437999999999997, -0.5904042520260251, 0.23449691522078642], [-0.14992283106299373, -1.1107125177255806, 0.2985764672865745], [0.14992283106299337, -1.1107125177255806, 0.24037381531227542], [-0.13252828919540124, -0.8948803505254139, 0.2631942769586178], [0.13252828919540094, -0.8948803505254139, 0.24264960347588999], [-0.132, -0.47, 0.2], [0.132, -0.51, 0.2], [-8.957066688963741e-17, -0.6508, 0.2403899252897569], [-3.5049391391597244e-17, -0.3764, 0.24007833102310425]];
const TEMPLATES: Record<Detail, Tpl> = {
  S: {
    eye_dx: 0.37,
    brow_dy: 2.6,
    mouth_dy: 3.7,
    nose_dy: 1.9,
    blush_dx: 0.17,
    blush_dy: 1.75,
    bridge_dy: 0.3,
    eye: {"open": ["KK", "DW", "II"], "wide": ["KK", "DW", "II", ".K"], "closed": [".K.", "K.K", "..."], "side": ["KK", "WD", "II"]},
    brow: {"base": ["HHH"], "up": ["HHH", "..."], "raise": [".HH", "H.."], "soft": ["HH."]},
    nose: ["n"],
    blush: ["bb"],
    freckles: ["f.f"],
    mouth: {"smile": ["l..l", ".MM."], "grin": ["mmmm", ".TT."], "laugh": ["mmmm", "mttm", ".mm."], "o": ["mm", "mm"], "flat": [".mm."], "small": ["l.l", ".M."], "smirk": ["...m", "mmm."]},
    glint: ["gG"],
    glasses: ["oooo", "o..o", "o..o", ".oo."],
    bridge: ["oo"],
  },
  M: {
    eye_dx: 0.37,
    brow_dy: 3.0,
    mouth_dy: 3.85,
    nose_dy: 2.0,
    blush_dx: 0.2,
    blush_dy: 1.9,
    bridge_dy: 0.5,
    eye: {"open": [".KK.", "KDWK", "SDIS", ".II."], "wide": [".KK.", "KDWK", "SDIS", "SIIS", ".KK."], "closed": ["K..K", ".KK."], "side": [".KK.", "KWDK", "SIDS", ".II."]},
    brow: {"base": [".HHH", "HH.."], "up": ["HHHH"], "raise": ["..HH", ".H..", "H..."], "soft": ["HHH."]},
    nose: ["n.", "Nn"],
    blush: ["bbb"],
    freckles: ["f.f.", ".f.."],
    mouth: {"smile": ["m...m", ".mmm."], "grin": ["mmmmm", "mTTTm", ".mmm."], "laugh": ["mmmmm", "mTTTm", "mtttm", ".mmm."], "o": [".mm.", "m..m", ".mm."], "flat": [".mmm."], "small": ["m..m", ".mm."], "smirk": ["....m", "mmmm."]},
    glint: ["dgG", ".d."],
    glasses: [".oooo.", "o....o", "o....o", "o....o", ".oooo."],
    bridge: ["oo"],
  },
  L: {
    eye_dx: 0.36,
    brow_dy: 3.2,
    mouth_dy: 3.85,
    nose_dy: 1.8,
    blush_dx: 0.22,
    blush_dy: 2.0,
    bridge_dy: 0.4,
    eye: {"open": ["..KKKK..", ".KKKKKKK", "KSDDWWDK", ".SDDWDDS", ".SDIIDDS", "..IiiI..", "........"], "wide": ["..KKKK..", ".KKKKKKK", "KSDDWWDS", "SSDDWDDS", "SSDIIDDS", ".SIiiIS.", "..SSSS.."], "closed": ["........", "K......K", ".KK..KK.", "...KK..."], "side": ["..KKKK..", ".KKKKKKK", "KWWDDSSK", ".WDDDSS.", ".IDDDSS.", "..iIS..."]},
    brow: {"base": ["..HHHHH", "HHHhh.."], "up": [".HHHHH.", "HH...HH"], "raise": ["....HHH", "..HHH..", "HH....."], "soft": [".HHHHH.", "H......"]},
    nose: [".h.", ".n.", "nN."],
    blush: [".bbb.", "bbbbb"],
    freckles: ["f.f..", "..f.f"],
    mouth: {"smile": ["m......m", ".mm..mm.", "...mm..."], "grin": ["mmmmmmmm", "mTTTTTTm", ".mTTTTm.", "..mmmm.."], "laugh": ["mmmmmmmm", "mTTTTTTm", "mmttttmm", ".mttttm.", "..mmmm.."], "o": ["..mm..", ".mmmm.", "mmttmm", ".mmmm.", "..mm.."], "flat": [".mmmmm.", "..LLL.."], "small": ["m....m", ".mmmm.", "..LL.."], "smirk": [".......m", ".mmmmmm.", "m......."]},
    glint: [".dd..", "dgGd.", ".dgd.", "..d.."],
    glasses: ["..oooooo..", ".o......o.", "o........o", "o.h......o", "o........o", ".o......o.", "..oooooo.."],
    bridge: ["oooo"],
  },
};
// ------------------------------------------------------------------ public render helpers
/** 32x48 full-body sprite (1x). */
export function renderSprite(cfg: Partial<CitizenCfg>): Pixels {
  return new Citizen(cfg).render(new Canvas(32, 48), 'S');
}

/** size -> [frame width in sprite units, detail]. Small tiles crop tighter so the face carries; 64 keeps the shoulders. */
export function bustSpec(size: number): [number, Detail] {
  if (size <= 32) return [25.0, 'S'];
  if (size <= 48) return [25.0, 'M'];
  return [27.0, 'L'];
}

/** Head-and-shoulders bust re-rasterised natively at `size` px (24-64). */
export function renderBust(cfg: Partial<CitizenCfg>, size = 40): Pixels {
  const [frame, det] = bustSpec(size);
  const k = size / frame;
  const ox = 16 - frame / 2;
  const oy = frame < 27 ? 0.8 : 1.2;
  return new Citizen(cfg).render(new Canvas(size, size, k, ox, oy), det);
}

/** Full body re-rasterised natively at scale k (1 -> 32x48, 1.5 -> 48x72 arrival card, 2.5 -> 80x120 hero). */
export function renderFigure(cfg: Partial<CitizenCfg>, k = 1.5): Pixels {
  const det: Detail = k < 1.3 ? 'S' : k < 2 ? 'M' : 'L';
  return new Citizen(cfg).render(new Canvas(pyRound(32 * k), pyRound(48 * k), k), det);
}
