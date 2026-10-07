// Pixel avatar renderer: a TypeScript port of design/mockups/art/sprites.py `avatar()`.
// Same char maps, same palette, same edits, so avatars match the mockup PNGs pixel for pixel.
// Original art, GPL v3 (part of the Tapaia repo).

export type Outfit = 'robe' | 'hood' | 'plain' | 'slogan';
export type HairKey = 'black' | 'chestnut' | 'ginger' | 'blonde' | 'plum' | 'silver';
export type SkinKey = 'fair' | 'warm' | 'tan' | 'deep';
export type HairStyle = 'short' | 'long' | 'bun';

export interface AvatarCfg {
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
export function avatarPixels(cfg: AvatarCfg): (string | null)[][] {
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

export const DEFAULT_AVATAR: AvatarCfg = { outfit: 'robe', hair: 'chestnut', hairstyle: 'short', skin: 'warm', band: true };

export function randomAvatar(rand: () => number = Math.random): AvatarCfg {
  const pick = <T,>(xs: readonly T[]) => xs[Math.floor(rand() * xs.length)];
  return {
    outfit: pick(['robe', 'robe', 'hood', 'plain', 'slogan'] as const),
    hair: pick(Object.keys(HAIRS) as HairKey[]),
    hairstyle: pick(['short', 'long', 'bun'] as const),
    skin: pick(Object.keys(SKINS) as SkinKey[]),
    band: rand() < 0.4,
    shirt: pick(SHIRTS),
  };
}

export function isAvatarCfg(a: any): a is AvatarCfg {
  return a && ['robe', 'hood', 'plain', 'slogan'].includes(a.outfit) && a.hair in HAIRS && a.skin in SKINS &&
    ['short', 'long', 'bun'].includes(a.hairstyle) && typeof a.band === 'boolean' &&
    (a.shirt === undefined || (typeof a.shirt === 'string' && /^#[0-9a-f]{6}$/i.test(a.shirt)));
}
