// The reference cast: the 12 citizens of design/characters/citizens.py (character sheet + Square banner), as v2
// avatar configs. Seed citizens use these (server/seed.ts); scripts/test-avatar2.ts checks they still equal the Python cast.
import type { AvatarCfg } from './avatar';

export interface CastMember { name: string; role: string; avatar: AvatarCfg }

export const CAST: CastMember[] = [
  { name: 'Wren Halloway', role: 'herb grower, tea-cart regular', avatar: { v: 2, skin: 'warm', hair: 'chestnut', hairstyle: 'short', eyes: 'green', expr: 'smile', outfit: 'tunic', top: 'leaf', bottom: 'brown', satchel: true, satchel_side: 1 } },
  { name: 'Nessa Quill', role: 'runs the tea cart', avatar: { v: 2, skin: 'fair', hair: 'ginger', hairstyle: 'bun', eyes: 'blue', expr: 'grin', freckles: true, outfit: 'apron', top: 'skyblue', over: 'parchment', bottom: 'charcoal', rolled: true, held: 'tea', pose: 'hold', hold_side: 1 } },
  { name: 'Orla Fenwick', role: 'reads in the library', avatar: { v: 2, skin: 'tan', hair: 'black', hairstyle: 'long', part: 0.18, eyes: 'brown', expr: 'calm', glasses: true, outfit: 'cardigan', top: 'plum', accent: 'cream', bottom: 'moss', bottom_kind: 'skirt', held: 'book', pose: 'hold', hold_side: 1, book_col: 'maple' } },
  { name: 'Corvin Ashdale', role: 'robe, hood down, neck band', avatar: { v: 2, skin: 'porcelain', hair: 'silver', hairstyle: 'swept', part: -0.3, eyes: 'grey', expr: 'content', beard: true, outfit: 'robe', neckband: true } },
  { name: 'Alder Meadows', role: 'robe, hood up, face cover', avatar: { v: 2, skin: 'warm', hair: 'black', outfit: 'hood', eyes: 'brown', expr: 'smile' } },
  { name: 'Tobin Larkspur', role: 'band shirt, laughs easily', avatar: { v: 2, skin: 'deep', hair: 'black', hairstyle: 'curly', eyes: 'brown', expr: 'laugh', outfit: 'bandtee', top: 'charcoal', accent: 'hydra', bottom: 'denim' } },
  { name: 'Odessa Brightmoss', role: 'elder, scarf and long coat', avatar: { v: 2, skin: 'brown', hair: 'silver', hairstyle: 'elderbun', eyes: 'amber', expr: 'content', outfit: 'coat', top: 'wallblue', scarf: 'maple', bottom: 'charcoal', held: 'tea', pose: 'hold', hold_side: -1 } },
  { name: 'Pim Tallow', role: 'new in town, yellow shirt', avatar: { v: 2, skin: 'porcelain', hair: 'blonde', hairstyle: 'ponytail', eyes: 'blue', expr: 'surprised', outfit: 'tee', top: 'hydra', bottom: 'denim', tail_side: 1 } },
  { name: 'Juniper Vale', role: 'braid, cardigan, satchel', avatar: { v: 2, skin: 'olive', hair: 'plum', hairstyle: 'braid', braid_side: -1, part: -0.25, eyes: 'hazel', expr: 'wink', outfit: 'cardigan', top: 'sage', accent: 'white', bottom: 'brown', satchel: true, satchel_side: 1 } },
  { name: 'Bram Teasel', role: 'tea house baker', avatar: { v: 2, skin: 'fair', hair: 'auburn', hairstyle: 'crop', eyes: 'green', expr: 'smile', beard: true, outfit: 'apron', top: 'cream', over: 'moss', bottom: 'brown', rolled: true } },
  { name: 'Lumi Ardent', role: 'robe, hood down, wavy hair', avatar: { v: 2, skin: 'brown', hair: 'black', hairstyle: 'wavy', eyes: 'brown', expr: 'shy', outfit: 'robe', neckband: false } },
  { name: 'Sorrel Finch', role: 'cosy cardigan, bob', avatar: { v: 2, skin: 'warm', hair: 'auburn', hairstyle: 'bob', part: 0.3, eyes: 'hazel', expr: 'thoughtful', outfit: 'tee', top: 'teal', bottom: 'charcoal', scarf: 'mustard' } },
];

export const castAvatar = (name: string): AvatarCfg => {
  const c = CAST.find((x) => x.name === name);
  if (!c) throw new Error(`no cast member ${name}`);
  return c.avatar;
};
