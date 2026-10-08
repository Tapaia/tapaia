// Avatar configs. v2 ("Cozy HD pixel", rendered by shared/avatar2.ts) is what the app stores and draws.
// v1 (the original 16x24 sprites, a port of design/mockups/art/sprites.py `avatar()`) stays for stored data from
// before the switch: normalizeAvatar() migrates it losslessly, and avatarPixels() still draws it for the
// classic-avatars fallback (?avatars=classic). Original art, GPL v3 (part of the Tapaia repo).
import {
  CLOTH, EXPRS, rgb, EYES, HAIRS as HAIRS2, HAIRSTYLES, OUTFITS2, SKINS as SKINS2,
  type CitizenCfg, type EyeKey, type Expr, type HairKey as HairKey2, type HairStyle as HairStyle2, type Outfit2, type SkinKey as SkinKey2,
} from './avatar2';

export type Outfit = 'robe' | 'hood' | 'plain' | 'slogan';
export type HairKey = 'black' | 'chestnut' | 'ginger' | 'blonde' | 'plum' | 'silver';
export type SkinKey = 'fair' | 'warm' | 'tan' | 'deep';
export type HairStyle = 'short' | 'long' | 'bun';

/** v1 config (before the Cozy HD switch). */
export interface AvatarCfgV1 {
  outfit: Outfit;
  hair: HairKey;
  hairstyle: HairStyle;
  skin: SkinKey;
  band: boolean;
  shirt?: string; // shirt colour for plain/slogan outfits
}

const OUT = '#2b1d2e';
const ROBE: Record<string, string> = { R: '#2e1a40', r: '#45275e', L: '#64408a', l: '#8a64b0' };
const BAND: Record<string, string> = { n: '#d9cfe6', N: '#a99bc2' };
export const SKINS: Record<SkinKey, [string, string]> = {
  fair: ['#f6d7b8', '#e0b48f'],
  warm: ['#e8b98c', '#c98e62'],
  tan: ['#c68a5a', '#a06a40'],
  deep: ['#8d5a3b', '#6c4029'],
};
export const HAIRS: Record<HairKey, [string, string]> = {
  black: ['#2e2630', '#4a3f4f'],
  chestnut: ['#7a4a2a', '#a0673a'],
  ginger: ['#b5522b', '#d8743f'],
  blonde: ['#d9a441', '#f0c96a'],
  plum: ['#5a2f5e', '#7e4a84'],
  silver: ['#9aa0ad', '#c7ccd6'],
};
export const SHIRTS = ['#64408a', '#5c9a3e', '#3f6fd8', '#c8452e', '#f2c84b', '#2f5a2e', '#2e2630'];

const HEAD_HAIR = ['....oooo', '..oohhhh', '.ohhhHHh', '.ohhHhhh', 'ohhhhhhh', 'ohhhhhhh', 'ohhsshhs', 'ohssesss', 'ohssesss', 'ohsbssss', '.osssssS', '..oossss'];
const HEAD_HOOD = ['....oooo', '..oorrrr', '.orrrLLr', '.orrLrrr', 'orrLrrrr', 'orrRRRRR', 'orRccccc', 'orRcgccc', 'orRcgccc', 'orRttttt', '.orRcccc', '..orRRcc'];
const BODY_ROBE = ['...onnnn', '..oLLLLL', '.oLRRRRR', '.oLrrrrr', '.oLrrRrr', 'oLrrrRrr', 'osSrrRrr', '.oLrrRrr', '.orrrrrr', '.oRRRRRR', '..offfo.', '..ooooo.'];
const BODY_SHIRT = ['...ossss', '..oTTTTT', '.oTTTTTT', '.oTTTTTT', 'osTTTTTT', 'osTTTTTT', '.oTTTTTT', '.oPPPPPP', '..oPPPPo', '..oPPPPo', '..obbbbo', '..oooooo'];

const mirror = (rows: string[]) => rows.map((r) => r + r.split('').reverse().join(''));

/** Returns rows of hex colours (null = transparent). Width is always 16. */
export function avatarPixels(cfg: AvatarCfgV1): (string | null)[][] {
  const hood = cfg.outfit === 'hood';
  const outfit = cfg.outfit === 'robe' || cfg.outfit === 'hood' ? 'robe' : 'shirt';
  const slogan = cfg.outfit === 'slogan';
  const { band, hairstyle } = cfg;
  const rows: string[][] = mirror([...(hood ? HEAD_HOOD : HEAD_HAIR), ...(outfit === 'robe' ? BODY_ROBE : BODY_SHIRT)]).map((r) => r.split(''));
  const setRange = (y: number, a: number, s: string) => s.split('').forEach((c, i) => (rows[y][a + i] = c));
  if (outfit === 'robe') {
    // dark purple robe shoes with a high heel and uneven soles [ch1]
    rows[22] = '..offfo..offfo..'.split('');
    rows[23] = '.oooooo..ooFFo..'.split('');
    rows.push('...........oo...'.split(''));
  }
  if (outfit === 'shirt' && !band) setRange(12, 4, 'ssssssss');
  if (outfit === 'robe' && !band) setRange(12, 4, 'RRRRRRRR');
  if (outfit === 'shirt' && band) setRange(12, 4, 'nnnnnnnn');
  if (outfit === 'shirt' && slogan) for (let x = 5; x < 11; x++) rows[15][x] = x % 2 ? 'w' : 'T';
  if (!hood && hairstyle === 'long') {
    for (let y = 6; y < 14; y++) { rows[y][1] = 'h'; rows[y][14] = 'h'; rows[y][0] = 'o'; rows[y][15] = 'o'; }
    rows[13][2] = 'h'; rows[13][13] = 'h';
  }
  if (!hood && hairstyle === 'bun') {
    rows.splice(0, 0, '......oooo......'.split(''));
    rows.splice(1, 0, '.....ohhHho.....'.split(''));
    setRange(2, 4, 'oohhhhoo');
  }
  const [s, S] = SKINS[cfg.skin];
  const [h, H] = HAIRS[cfg.hair];
  const pal: Record<string, string> = {
    ...ROBE, ...BAND, s, S, b: cfg.skin === 'fair' || cfg.skin === 'warm' ? '#e88a8a' : S,
    h, H, e: '#2b1d2e', c: '#231430', g: '#d8c8ff', t: '#7a5a9a', f: ROBE.R, F: '#1d1029',
    T: cfg.shirt || '#5c9a3e', P: '#4a3f4f', w: '#fbf1d6',
  };
  const out = rows.map((r) => r.map((c) => (c === '.' || c === ' ' ? null : c === 'o' ? OUT : pal[c])));
  if (outfit === 'shirt') {
    // shirt shoes are brown (sprites.py recolours blush-coloured pixels in the bottom two rows)
    for (let y = out.length - 2; y < out.length; y++) for (let x = 0; x < 16; x++) if (out[y][x] === pal.b) out[y][x] = '#6b3f1f';
  }
  return out;
}


// ---------------------------------------------------------------------------------------------- v2
/** The stored / rendered avatar: the charkit render config (see CitizenCfg) tagged v: 2. Only outfit, skin and hair
 *  are required; the renderer fills the rest from DEFAULT_CITIZEN. */
export type AvatarCfg = { v: 2 } & Pick<CitizenCfg, 'outfit' | 'skin' | 'hair'> & Partial<Omit<CitizenCfg, 'outfit' | 'skin' | 'hair'>>;
export type { CitizenCfg };

const HEX = /^#[0-9a-f]{6}$/i;
const isColour = (c: unknown) => typeof c === 'string' && (c in CLOTH || HEX.test(c));
const side = (v: unknown) => v === 1 || v === -1;
const unit = (v: unknown) => typeof v === 'number' && Number.isFinite(v) && v >= -1 && v <= 1;
const bool = (v: unknown) => typeof v === 'boolean';
const oneOf = (xs: readonly string[]) => (v: unknown) => typeof v === 'string' && xs.includes(v);
/** Field validators: anything not listed here is dropped. */
const FIELDS: Record<string, (v: unknown) => boolean> = {
  v: (v) => v === 2,
  skin: (v) => typeof v === 'string' && v in SKINS2, hair: (v) => typeof v === 'string' && v in HAIRS2,
  hairstyle: oneOf(HAIRSTYLES), eyes: (v) => typeof v === 'string' && v in EYES, expr: oneOf(EXPRS), outfit: oneOf(OUTFITS2),
  top: isColour, bottom: isColour, over: (v) => v === null || isColour(v), accent: (v) => v === null || isColour(v),
  bottom_kind: (v) => v === 'skirt', stockings: isColour, neckband: bool, scarf: isColour, satchel: bool, satchel_side: side,
  glasses: bool, beard: bool, freckles: bool, blush: bool, held: oneOf(['tea', 'book']), pose: oneOf(['down', 'hold']),
  hold_side: side, book_col: isColour, part: unit, tail_side: side, braid_side: side, rolled: bool, long_sleeve: bool, turn: unit,
};

/** v1 -> v2, lossless for everything v1 has (see design/characters/README.md, "Mapping current builder -> new parts"). */
export function migrateAvatar(a: AvatarCfgV1): AvatarCfg {
  const outfit = ({ robe: 'robe', hood: 'hood', plain: 'tee', slogan: 'bandtee' } as const)[a.outfit];
  return {
    v: 2, skin: a.skin, hair: a.hair, hairstyle: a.hairstyle, eyes: 'brown', expr: 'smile', outfit,
    top: a.shirt ?? (outfit === 'tee' || outfit === 'bandtee' ? '#5c9a3e' : 'leaf'), bottom: 'charcoal',
    ...(outfit === 'bandtee' ? { accent: 'cream' } : {}), neckband: a.band,
  };
}

export function isAvatarCfgV1(a: any): a is AvatarCfgV1 {
  return !!a && typeof a === 'object' && ['robe', 'hood', 'plain', 'slogan'].includes(a.outfit) && a.hair in HAIRS && a.skin in SKINS &&
    ['short', 'long', 'bun'].includes(a.hairstyle) && typeof a.band === 'boolean' &&
    (a.shirt === undefined || (typeof a.shirt === 'string' && HEX.test(a.shirt)));
}

/** Accepts a v1 or v2 config from anywhere (API body, old db.json) and returns a clean v2 config, or null. */
export function normalizeAvatar(a: unknown): AvatarCfg | null {
  if (!a || typeof a !== 'object') return null;
  const o = a as Record<string, unknown>;
  if (o.v === undefined && isAvatarCfgV1(o)) return migrateAvatar(o);
  if (o.v !== 2) return null;
  const out: Record<string, unknown> = {};
  for (const [k, v] of Object.entries(o)) {
    if (!(k in FIELDS)) continue;
    if (v === undefined) continue;
    if (!FIELDS[k](v)) return null;
    out[k] = v;
  }
  if (!out.outfit || !out.skin || !out.hair) return null;
  return out as AvatarCfg;
}
export const isAvatarCfg = (a: unknown): a is AvatarCfg => normalizeAvatar(a) !== null;

/** v2 -> closest v1, only for the classic-avatars fallback. */
export function toV1(a: AvatarCfg): AvatarCfgV1 {
  const skin = ({ porcelain: 'fair', fair: 'fair', warm: 'warm', olive: 'warm', tan: 'tan', brown: 'deep', deep: 'deep' } as const)[a.skin];
  const hair = ({ espresso: 'black', auburn: 'ginger' } as Record<string, HairKey>)[a.hair] ?? (a.hair as HairKey);
  const hs = a.hairstyle ?? 'short';
  const hairstyle: HairStyle = ['long', 'wavy', 'braid', 'bob'].includes(hs) ? 'long' : ['bun', 'elderbun'].includes(hs) ? 'bun' : 'short';
  const outfit: Outfit = a.outfit === 'robe' || a.outfit === 'hood' ? a.outfit : a.outfit === 'bandtee' ? 'slogan' : 'plain';
  const top = a.top ?? 'leaf';
  return { outfit, skin, hair, hairstyle, band: !!a.neckband, shirt: CLOTH[top] ?? top };
}

export const DEFAULT_AVATAR: AvatarCfg = { v: 2, skin: 'warm', hair: 'chestnut', hairstyle: 'short', eyes: 'brown', expr: 'smile', outfit: 'robe', top: 'leaf', bottom: 'charcoal', neckband: true };

/** Builder colour rows (keys of CLOTH; hex also works anywhere). */
export const TOPS = ['leaf', 'moss', 'sage', 'skyblue', 'wallblue', 'teal', 'plum', 'lilac', 'maple', 'rust', 'hydra', 'mustard', 'cream', 'charcoal'];
export const BOTTOMS = ['charcoal', 'brown', 'denim', 'navy', 'moss', 'wood', 'stone', 'plum'];
export const ACCENTS = ['cream', 'white', 'parchment', 'hydra', 'rose', 'skyblue', 'sage', 'maple'];
export const SCARVES = ['maple', 'mustard', 'teal', 'rose', 'sage', 'plum', 'cream'];

const dist = (a: string, b: string) => { const A = rgb(CLOTH[a] ?? a), B = rgb(CLOTH[b] ?? b); return Math.hypot(A[0] - B[0], A[1] - B[1], A[2] - B[2]); };

export function randomAvatar(rand: () => number = Math.random): AvatarCfg {
  const pick = <T,>(xs: readonly T[]) => xs[Math.floor(rand() * xs.length)];
  const outfit = pick(['robe', 'robe', 'hood', 'tee', 'bandtee', 'tunic', 'cardigan', 'apron', 'coat'] as const);
  const skin = pick(Object.keys(SKINS2) as SkinKey2[]);
  // keep the parts readable against each other (no auburn hair + rust coat on deep skin): re-pick close colours
  let hair = pick(Object.keys(HAIRS2) as HairKey2[]);
  for (let i = 0; i < 20 && dist(HAIRS2[hair], SKINS2[skin]) < 55; i++) hair = pick(Object.keys(HAIRS2) as HairKey2[]);
  let top = pick(TOPS);
  for (let i = 0; i < 20 && (dist(top, SKINS2[skin]) < 70 || dist(top, HAIRS2[hair]) < 70); i++) top = pick(TOPS);
  let bottom = pick(BOTTOMS);
  for (let i = 0; i < 20 && dist(bottom, top) < 60; i++) bottom = pick(BOTTOMS);
  const a: AvatarCfg = {
    v: 2, skin, hair, hairstyle: pick(HAIRSTYLES), eyes: pick(Object.keys(EYES) as EyeKey[]),
    expr: pick(['smile', 'smile', 'grin', 'content', 'calm', 'laugh', 'wink', 'shy'] as const), outfit, top, bottom,
  };
  if (outfit === 'robe' || outfit === 'hood') a.neckband = rand() < 0.4;
  if (outfit === 'cardigan' || outfit === 'bandtee') { let ac = pick(ACCENTS); for (let i = 0; i < 20 && dist(ac, top) < 70; i++) ac = pick(ACCENTS); a.accent = ac; }
  if (outfit === 'apron') { let ov = pick(['parchment', 'cream', 'moss', 'wood']); for (let i = 0; i < 20 && dist(ov, top) < 70; i++) ov = pick(['parchment', 'cream', 'moss', 'wood']); a.over = ov; }
  if (outfit !== 'robe' && outfit !== 'hood') {
    if (rand() < 0.2) a.scarf = pick(SCARVES);
    if (rand() < 0.2) a.satchel = true;
    if (rand() < 0.15) a.held = pick(['tea', 'book'] as const);
  }
  if (a.hairstyle === 'braid') a.braid_side = -1;          // braid over the left shoulder, hands free on the right
  if (a.held) { a.pose = 'hold'; a.hold_side = a.satchel ? -1 : 1; }
  if (a.satchel) a.satchel_side = 1;
  if (a.held && a.hold_side === -1 && a.braid_side === -1) a.braid_side = 1;
  if (rand() < 0.12) a.glasses = true;
  if (rand() < 0.15) a.freckles = true;
  return a;
}
export type { EyeKey, Expr, HairKey2, HairStyle2, Outfit2, SkinKey2 };
