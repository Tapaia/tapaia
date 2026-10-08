// Golden-image test: the TS port (shared/avatar2.ts) must reproduce the Python reference renderer
// (design/characters/charkit.py) for the whole reference cast, at every size the app draws.
// Goldens: design/characters/art/{sprites,busts,figures}/*.png + cast.json (written by design/characters/build.py).
// Usage: npx tsx scripts/test-avatar2.ts   -> PASS/FAIL lines (verify.mjs runs it too)
import fs from 'node:fs';
import path from 'node:path';
import zlib from 'node:zlib';
import { fileURLToPath } from 'node:url';
import { renderBust, renderFigure, renderSprite, type CitizenCfg, type Pixels } from '../shared/avatar2';
import { normalizeAvatar, migrateAvatar } from '../shared/avatar';
import { CAST } from '../shared/cast';
import { SEED_USERS } from '../server/seed';

const DIR = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../../design/characters');
const TOL = 0.005;   // <=0.5% of pixels may differ (float edge cases between numpy/libm and V8)
let fails = 0;
const ok = (name: string, pass: boolean, extra = '') => { if (!pass) fails++; console.log(`${pass ? 'PASS' : 'FAIL'}  ${name}${extra ? '  ' + extra : ''}`); };

/** Minimal PNG reader for the 8-bit RGB/RGBA files Pillow writes. */
function readPng(file: string): Pixels {
  const buf = fs.readFileSync(file);
  let p = 8, w = 0, h = 0, type = 0;
  const idat: Buffer[] = [];
  while (p < buf.length) {
    const len = buf.readUInt32BE(p), kind = buf.toString('ascii', p + 4, p + 8), body = buf.subarray(p + 8, p + 8 + len);
    if (kind === 'IHDR') { w = body.readUInt32BE(0); h = body.readUInt32BE(4); type = body[9]; if (body[8] !== 8 || (type !== 6 && type !== 2)) throw new Error(`${file}: unsupported PNG`); }
    if (kind === 'IDAT') idat.push(body);
    p += 12 + len;
  }
  const bpp = type === 6 ? 4 : 3, stride = w * bpp;
  const raw = zlib.inflateSync(Buffer.concat(idat));
  const px = new Uint8Array(h * stride);
  for (let y = 0; y < h; y++) {
    const f = raw[y * (stride + 1)], row = raw.subarray(y * (stride + 1) + 1, (y + 1) * (stride + 1));
    for (let x = 0; x < stride; x++) {
      const a = x >= bpp ? px[y * stride + x - bpp] : 0, b = y ? px[(y - 1) * stride + x] : 0, c = x >= bpp && y ? px[(y - 1) * stride + x - bpp] : 0;
      const pa = Math.abs(b - c), pb = Math.abs(a - c), pc = Math.abs(a + b - 2 * c);
      const pred = [0, a, b, (a + b) >> 1, pa <= pb && pa <= pc ? a : pb <= pc ? b : c][f];
      px[y * stride + x] = (row[x] + pred) & 255;
    }
  }
  const data = new Uint8ClampedArray(w * h * 4);
  for (let i = 0; i < w * h; i++) { for (let k = 0; k < 3; k++) data[i * 4 + k] = px[i * bpp + k]; data[i * 4 + 3] = bpp === 4 ? px[i * bpp + 3] : 255; }
  return { w, h, data };
}

function diff(a: Pixels, b: Pixels) {
  if (a.w !== b.w || a.h !== b.h) return { frac: 1, n: -1 };
  let n = 0;
  for (let i = 0; i < a.w * a.h; i++) {
    const A = a.data[i * 4 + 3] ? [...a.data.subarray(i * 4, i * 4 + 4)] : [0, 0, 0, 0];
    const B = b.data[i * 4 + 3] ? [...b.data.subarray(i * 4, i * 4 + 4)] : [0, 0, 0, 0];
    if (A.some((v, k) => v !== B[k])) n++;
  }
  return { frac: n / (a.w * a.h), n };
}

const ref = JSON.parse(fs.readFileSync(path.join(DIR, 'cast.json'), 'utf8')) as { cast: { name: string; slug: string; cfg: CitizenCfg }[]; turned: string[]; busts: number[]; figures: number[] };
const cases: [string, () => Pixels, string][] = [];
for (const { slug, cfg } of ref.cast) {
  cases.push([`${slug} sprite`, () => renderSprite(cfg), `sprites/${slug}.png`]);
  for (const s of ref.busts) cases.push([`${slug} bust ${s}`, () => renderBust(cfg, s), `busts/${slug}-${s}.png`]);
  for (const k of ref.figures) cases.push([`${slug} figure ${Math.round(32 * k)}`, () => renderFigure(cfg, k), `figures/${slug}-${Math.round(32 * k)}.png`]);
  if (ref.turned.includes(slug)) cases.push([`${slug} 3/4 sprite`, () => renderSprite({ ...cfg, turn: 0.8 }), `sprites/${slug}-3q.png`]);
}
let exact = 0, worst = 0, worstName = '', total = 0;
const bad: string[] = [];
const t0 = performance.now();
for (const [name, fn, file] of cases) {
  const d = diff(fn(), readPng(path.join(DIR, 'art', file)));
  total++;
  if (d.n === 0) exact++;
  if (d.frac > worst) { worst = d.frac; worstName = `${name} (${d.n} px)`; }
  if (d.frac > TOL) bad.push(`${name}: ${d.n < 0 ? 'size mismatch' : (d.frac * 100).toFixed(2) + '%'}`);
}
const ms = performance.now() - t0;
ok(`avatar2 golden: TS port matches the Python reference (${total} images, ≤${TOL * 100}% px each)`, bad.length === 0,
  `${exact}/${total} pixel-exact, worst ${(worst * 100).toFixed(2)}% ${worstName}${bad.length ? ' · ' + bad.slice(0, 4).join('; ') : ''}`);

// the seed cast (shared/cast.ts) is the reference cast (citizens.py via cast.json)
const canon = (o: object) => JSON.stringify(Object.fromEntries(Object.entries(o).filter(([k]) => k !== 'v').sort(([a], [b]) => a.localeCompare(b))));
const mism = ref.cast.filter((r) => { const c = CAST.find((x) => x.name === r.name); return !c || canon(c.avatar) !== canon(r.cfg); });
ok('avatar2 cast: shared/cast.ts configs equal design/characters/citizens.py', mism.length === 0, mism.map((m) => m.name).join(', '));

// seed citizens: valid v2 configs, and everyone who is in the reference cast wears their cast look
{
  const invalid = SEED_USERS.filter((u) => JSON.stringify(normalizeAvatar(u.avatar)) !== JSON.stringify(u.avatar)).map((u) => u.id);
  const inCast = SEED_USERS.filter((u) => CAST.some((c) => c.name === u.citizenName));
  const wrong = inCast.filter((u) => canon(u.avatar) !== canon(CAST.find((c) => c.name === u.citizenName)!.avatar) && u.id !== 'tobin').map((u) => u.id);
  ok('seed citizens: v2 avatars; the 11 cast members in the seed wear their cast look (Tobin keeps his hood up)', !invalid.length && !wrong.length && inCast.length === 11,
    `${inCast.length} in cast${invalid.length ? ' · invalid ' + invalid : ''}${wrong.length ? ' · differ ' + wrong : ''}`);
}

// speed (render budget from the README: <=2 ms per bust, <=4 ms per sprite on a phone; this box is faster)
{
  const cfg = ref.cast[2].cfg;
  const N = 40, a = performance.now(); for (let i = 0; i < N; i++) renderBust(cfg, 40); const b40 = (performance.now() - a) / N;
  const c = performance.now(); for (let i = 0; i < N; i++) renderSprite(cfg); const sp = (performance.now() - c) / N;
  ok('avatar2 speed: 40 px bust and 32x48 sprite render fast enough for on-demand use', b40 < 8 && sp < 12, `bust40 ${b40.toFixed(2)} ms, sprite ${sp.toFixed(2)} ms, golden pass ${ms.toFixed(0)} ms`);
}

// migration: every v1 config maps losslessly onto v2, bad input is rejected
{
  const v1 = { outfit: 'slogan', hair: 'ginger', hairstyle: 'long', skin: 'tan', band: true, shirt: '#c8452e' };
  const m = migrateAvatar(v1 as never);
  const n = normalizeAvatar(v1);
  const robe = normalizeAvatar({ outfit: 'hood', hair: 'black', hairstyle: 'short', skin: 'warm', band: false });
  ok('avatar migration: v1 → v2 keeps outfit, colours, hair, skin and neck band',
    m.v === 2 && m.outfit === 'bandtee' && m.top === '#c8452e' && m.hair === 'ginger' && m.hairstyle === 'long' && m.skin === 'tan' && m.neckband === true &&
    JSON.stringify(n) === JSON.stringify(m) && robe?.outfit === 'hood' && robe.neckband === false);
  const v2 = normalizeAvatar({ ...CAST[1].avatar });
  ok('avatar validation: v2 round-trips, junk is rejected', JSON.stringify(v2) === JSON.stringify(CAST[1].avatar) &&
    normalizeAvatar({ v: 2, outfit: 'cape' }) === null && normalizeAvatar({ ...CAST[0].avatar, top: 'url(javascript:1)' }) === null &&
    normalizeAvatar(null) === null && normalizeAvatar({ ...CAST[0].avatar, extra: 'x' })?.hasOwnProperty('extra') === false);
}
process.exit(fails ? 1 : 0);
