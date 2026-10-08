// Fictional demo citizens (from design/mockups-v2) and a few seed messages.
// Avatars: the Cozy HD cast (design/characters/citizens.py -> shared/cast.ts) for the 11 citizens who are in it;
// Tobin keeps his hood up (his lines are about it), so he wears the cast's hooded robe with his own skin tone.
import type { AvatarCfg } from '../shared/avatar';
import { castAvatar as cast } from '../shared/cast';
import type { Badge, Channel, Presence, Tile } from '../shared/types';

export const ZC_ADDRESS = '0x4E67DB19044549fF420860834c91b45BaD298722';
export const X_URL = 'https://x.com/TapaiaSquare';

export interface SeedUser {
  id: string; handle: string; citizenName: string; tile: Tile; badges: Badge[];
  avatar: AvatarCfg; status: string; presence: Presence; entry?: 'founder' | 'burn'; arrivalText?: string;
  wallet?: string; district?: string; about?: string; room?: string; kind?: 'seed' | 'bot'; linked?: boolean;
  /** DEMO Zipcoin name (sample data, not a real zipcoin.cash registration). Picked from names that were unclaimed on Oct 7, 2026. */
  zipDemo?: string;
}

/** Citizens outside the reference cast get v2 configs in the same style. */
const A = (a: Omit<AvatarCfg, 'v'>): AvatarCfg => ({ v: 2, eyes: 'brown', expr: 'smile', ...a });

export const SEED_USERS: SeedUser[] = [
  { id: 'ilse', handle: 'ilseh', citizenName: 'Ilse Hartwood', tile: 'c1', badges: ['founder'], avatar: A({ skin: 'tan', hair: 'plum', hairstyle: 'long', part: -0.2, eyes: 'hazel', expr: 'grin', outfit: 'robe', neckband: true }), status: 'just arrived', presence: 'here', entry: 'founder', arrivalText: 'Hello Tapaia! I brought cards and a terrible sense of direction.', wallet: '0x3fA1…c07e', district: 'Kalimar', room: 'square' },
  { id: 'nessa', handle: 'nessaq', citizenName: 'Nessa Quill', tile: 'c5', badges: ['founder'], avatar: cast('Nessa Quill'), status: 'at the tea cart', presence: 'here', entry: 'founder', arrivalText: 'First cup of tea in the square is on me.', wallet: '0x88b2…41d0', room: 'square', zipDemo: 'nessaq' },
  { id: 'corvin', handle: 'ashdale', citizenName: 'Corvin Ashdale', tile: 'c3', badges: ['founder'], avatar: cast('Corvin Ashdale'), status: 'idle', presence: 'idle', entry: 'founder', arrivalText: 'Keeper of the tea cart schedule. Ask me anything about jasmine.', wallet: '0x1c9e…77aa', room: 'square' },
  { id: 'wren', handle: 'wrenh', citizenName: 'Wren Halloway', tile: 'c2', badges: ['onchain'], avatar: cast('Wren Halloway'), status: 'herb swap at 6 lh', presence: 'here', entry: 'burn', arrivalText: 'Hello Tapaia! Herb grower from Kalimar, here for the tea and the talk.', wallet: '0x5d0F…e912', district: 'Kalimar', room: 'square', zipDemo: 'wrenh' },
  { id: 'orla', handle: 'orlaf', citizenName: 'Orla Fenwick', tile: 'c4', badges: ['onchain'], avatar: cast('Orla Fenwick'), status: 'by the maple', presence: 'here', entry: 'burn', arrivalText: 'Here for the maple and the benches.', wallet: '0xa7E3…0b5c', room: 'square' },
  { id: 'tobin', handle: 'tobinl', citizenName: 'Tobin Larkspur', tile: 'c1', badges: ['onchain'], avatar: { ...cast('Alder Meadows'), skin: 'deep' }, status: 'hood up', presence: 'here', entry: 'burn', arrivalText: 'Hood up, ears open.', wallet: '0x29Cc…a3f1', room: 'square' },
  { id: 'pim', handle: 'tallowpim', citizenName: 'Pim Tallow', tile: 'c3', badges: ['onchain'], avatar: cast('Pim Tallow'), status: 'in the library', presence: 'idle', entry: 'burn', arrivalText: 'Looking for a book that is not about business.', wallet: '0x6b41…9e2d', room: 'square' },
  { id: 'juniper', handle: 'jvale', citizenName: 'Juniper Vale', tile: 'c4', badges: ['onchain'], avatar: cast('Juniper Vale'), status: 'saving the bench', presence: 'here', entry: 'burn', arrivalText: 'Hi all, Juniper here. Bench enthusiast.', wallet: '0x71C4…9A3f', room: 'square' },
  { id: 'marek', handle: 'stonebrook', citizenName: 'Marek Stonebrook', tile: 'c6', badges: ['onchain'], avatar: A({ skin: 'fair', hair: 'black', outfit: 'hood', eyes: 'grey', expr: 'calm' }), status: 'back later', presence: 'off', entry: 'burn', arrivalText: 'Quiet type. Good listener.', wallet: '0x0e5A…d4c8' },
  { id: 'bram', handle: 'bram', citizenName: 'Bram Teasel', tile: 'c4', badges: ['team'], avatar: cast('Bram Teasel'), status: 'shipping the beta', presence: 'here', entry: 'founder', arrivalText: 'Team here. Welcome to the square!', wallet: '0xB7a0…12e4', about: 'Tapaia team. Builds things, breaks things, fixes things.', linked: true },
  { id: 'odessa', handle: 'brightmoss', citizenName: 'Odessa Brightmoss', tile: 'c2', badges: ['mod', 'founder'], avatar: cast('Odessa Brightmoss'), status: 'here to help', presence: 'here', entry: 'founder', arrivalText: 'Moderator on duty. Be kind, have tea.', wallet: '0x44dE…8b19' },
  { id: 'lumi', handle: 'lumi_a', citizenName: 'Lumi Ardent', tile: 'c6', badges: ['mod', 'onchain'], avatar: cast('Lumi Ardent'), status: 'reading the repo', presence: 'here', entry: 'burn', arrivalText: 'Reading every line of the repo so you do not have to.', wallet: '0x9F02…c6b3' },
  { id: 'sorrel', handle: 'sorrelf', citizenName: 'Sorrel Finch', tile: 'c5', badges: ['onchain'], avatar: cast('Sorrel Finch'), status: 'new citizen 🎉', presence: 'here', entry: 'burn', arrivalText: 'Finally made it! Hello everyone.', wallet: '0x3E7b…5a21' },
  { id: 'pricebot', handle: 'zc-price', citizenName: 'ZC Price Bot', tile: 'c2', badges: ['bot'], avatar: A({ skin: 'warm', hair: 'silver', hairstyle: 'crop', eyes: 'grey', expr: 'calm', outfit: 'coat', top: 'moss', glasses: true }), status: 'GeckoTerminal feed', presence: 'here', kind: 'bot', about: 'Read-only bot. Posts ZC price and pool liquidity from GeckoTerminal. Holds no wallet.' },
  { id: 'bookbot', handle: 'book-feed', citizenName: 'Book Feed Bot', tile: 'c3', badges: ['bot'], avatar: A({ skin: 'warm', hair: 'black', outfit: 'hood', eyes: 'brown', expr: 'calm' }), status: 'sample feed', presence: 'here', kind: 'bot', about: 'Read-only bot. In this prototype it posts SAMPLE Book posts and burns, not live data.' },
];

export const CHANNELS: Channel[] = [
  { id: 'announcements', name: 'announcements', layer: 'ooc', topic: 'News from the Tapaia team. Read-only.', pinned: `The only real ZC is <code>0x4E67…8722</code>. Our only X account is <a href="${X_URL}" target="_blank" rel="noreferrer">@TapaiaSquare</a>.` },
  { id: 'general', name: 'general', layer: 'ooc', topic: 'Everyday community talk. Price talk lives in #market.', pinned: 'the only real ZC is <code>0x4E67…8722</code>. Staff never DM first or ask for your seed phrase.' },
  { id: 'market', name: 'market', layer: 'ooc', topic: 'Price talk. No paid promotion, no “guaranteed” calls, no team price talk.' },
  { id: 'support', name: 'support', layer: 'ooc', topic: 'Ask anything. Helpers answer in public.', pinned: 'Staff never DM first and never ask for your seed phrase. Get help here, in public.' },
  { id: 'dev-updates', name: 'dev-updates', layer: 'ooc', topic: 'Changelogs, repo and running-commit links. Team posts, everyone replies.' },
  { id: 'feeds', name: 'feeds', layer: 'ooc', topic: 'Read-only bots: ZC price, burns and Book posts.' },
  { id: 'lobby', name: 'lobby', layer: 'ooc', topic: 'Say hi and look around. Become a citizen to post everywhere.' },
  { id: 'square', name: 'Tapaia Square', layer: 'ic', topic: 'Tea cart’s open. Say hello to new arrivals, and speak as your citizen.' },
];

type SeedMsg = { ch: string; u?: string; text: string; ago: number; kind?: 'text' | 'system' | 'arrival' | 'speak'; sys?: 'enter' | 'leave' | 'citizen'; replyTo?: number; react?: Record<string, string[]>; card?: { url: string; title: string; desc: string }; sample?: boolean; simulated?: boolean };

// `ago` = minutes before server start. replyTo indexes into this array.
export const SEED_MESSAGES: SeedMsg[] = [
  /* 0 */ { ch: 'announcements', u: 'bram', ago: 600, text: `Welcome to the Tapaia prototype! This is a demo build of the Phase 1 hub. Nothing here touches real ZC. Follow us on X at ${X_URL} (@TapaiaSquare), our only account.` },
  /* 1 */ { ch: 'announcements', u: 'bram', ago: 45, text: 'Founding Citizen slots are open in the demo. Claim one from #lobby to get the badge. Reminder: staff never DM first and never ask for your seed phrase.' },
  /* 2 */ { ch: 'general', u: 'bram', ago: 300, text: 'Phase 1 beta notes are up in #dev-updates. Big one: push notifications now work when you add Tapaia to your home screen on iPhone and Android.', react: { '🎉': ['nessa', 'wren', 'orla', 'sorrel', 'pim', 'odessa', 'lumi', 'tobin', 'corvin', 'ilse', 'marek', 'juniper'], '🙌': ['nessa', 'wren', 'orla', 'sorrel', 'pim'], '🍵': ['corvin', 'nessa', 'ilse'] } },
  /* 3 */ { ch: 'general', u: 'odessa', ago: 292, text: 'Installed it on my phone and the first mention came through instantly. Honestly smoother than the old group chat 👋' },
  /* 4 */ { ch: 'general', u: 'sorrel', ago: 288, text: 'Same here. Is there a way to schedule dark mode for after sunset?', replyTo: 3 },
  /* 5 */ { ch: 'general', u: 'lumi', ago: 281, text: 'Source is up if anyone wants to dig in, prompts and art generators included:', card: { url: 'github.com/tapaia/tapaia', title: 'Tapaia: an open-source town square in Veridia', desc: 'GPL v3 · based on Snowmoon by Vitalik Buterin · not affiliated' } },
  /* 6 */ { ch: 'general', kind: 'system', sys: 'citizen', u: 'sorrel', ago: 276, text: 'just became a citizen. Say hi!' },
  /* 7 */ { ch: 'general', u: 'odessa', ago: 274, text: '@jvale did your arrival post confirm okay?' },
  /* 8 */ { ch: 'general', u: 'juniper', ago: 272, text: 'Yep, about a minute. The preview made it really clear what I was burning before I signed.' },
  /* 9 */ { ch: 'market', u: 'pim', ago: 200, text: 'Reminder that price talk lives here, not in #general. Keep it civil and no “guaranteed” calls 🙏' },
  /* 10 */ { ch: 'market', u: 'sorrel', ago: 150, text: 'Liquidity looks a bit deeper on the WETH pool today. The #feeds bot has the numbers.' },
  /* 11 */ { ch: 'support', u: 'odessa', ago: 500, text: 'Hi! I’m a moderator. If you have trouble signing in or with your arrival post, ask here. We will never DM you first.' },
  /* 12 */ { ch: 'support', u: 'orla', ago: 120, text: 'Does the founder slot cost anything?' },
  /* 13 */ { ch: 'support', u: 'odessa', ago: 118, text: '@orlaf nope, founder slots are free. Only the arrival-post path burns ZC, and in this demo nothing is burned at all.', replyTo: 12 },
  /* 14 */ { ch: 'dev-updates', u: 'bram', ago: 330, text: 'v0.1 prototype: demo sign-in, wallet sign-in (SIWE), live chat over WebSockets, Tapaia Square with the Meldan clock, light and dark themes. Repo: github.com/tapaia/tapaia', react: { '🚀': ['lumi', 'odessa', 'wren'] } },
  /* 15 */ { ch: 'lobby', u: 'bram', ago: 400, text: 'Welcome to Tapaia! Make your arrival post to join, or ask anything in #support.' },
  /* 16 */ { ch: 'lobby', u: 'odessa', ago: 60, text: 'New here? Claim a free Founding Citizen slot while they last, or make an arrival post. Both get you into Tapaia Square.' },
  /* 17 */ { ch: 'feeds', u: 'bookbot', ago: 90, sample: true, text: 'SAMPLE · New Book post: “The tea cart opens at 2 longhours.” · burned 1,000 ZC' },
  /* 18 */ { ch: 'feeds', u: 'bookbot', ago: 40, sample: true, text: 'SAMPLE · Notable burn: 25,000 ZC burned in one Speak post.' },
  /* 19 */ { ch: 'square', kind: 'system', sys: 'enter', u: 'juniper', ago: 32, text: 'has entered the square' },
  /* 20 */ { ch: 'square', u: 'corvin', ago: 30, text: 'Morning, all. The tea cart is open again, jasmine today ☕' },
  /* 21 */ { ch: 'square', u: 'nessa', ago: 28, text: 'Save me a cup! Is the library still all business books?' },
  /* 22 */ { ch: 'square', kind: 'arrival', u: 'ilse', ago: 26, text: 'Hello Tapaia! I brought cards and a terrible sense of direction.', react: { '👋': ['nessa', 'corvin', 'wren', 'orla', 'tobin', 'pim'] } },
  /* 23 */ { ch: 'square', u: 'tobin', ago: 24, text: 'Welcome, Ilse! Fair warning, the slide is cold this time of year.', replyTo: 22, react: { '👋': ['ilse', 'nessa', 'orla', 'wren'], '🃏': ['ilse', 'pim'] } },
  /* 24 */ { ch: 'square', kind: 'speak', u: 'wren', ago: 21, text: 'Herb swap at the tea cart at 6 longhours. Bring cuttings, take cuttings 🌿', simulated: true },
  /* 25 */ { ch: 'square', u: 'orla', ago: 18, text: '@Ilse Hartwood come sit with us by the maple, there’s room on the bench.' },
  /* 26 */ { ch: 'square', kind: 'system', sys: 'leave', u: 'marek', ago: 15, text: 'left the square' },
];

// Ambient demo chatter so rooms feel alive. Clearly simulated (see README).
export const AMBIENT: { ch: string; u: string; text: string }[] = [
  { ch: 'square', u: 'nessa', text: 'The jasmine is gone already. Mint it is.' },
  { ch: 'square', u: 'corvin', text: 'Tea cart closes at 8 longhours today, get your cups in.' },
  { ch: 'square', u: 'wren', text: 'Brought rosemary cuttings, anyone want some?' },
  { ch: 'square', u: 'pim', text: 'Found a book in the library that is not about business! It is about… business ethics. Close enough.' },
  { ch: 'square', u: 'orla', text: 'The maple is turning red. Best bench in the square right now.' },
  { ch: 'square', u: 'tobin', text: 'Hood up, it’s windy by the fountain.' },
  { ch: 'square', u: 'ilse', text: 'Got lost on the way to the library. Again.' },
  { ch: 'square', u: 'juniper', text: 'Bench by the maple is free if anyone wants it.' },
  { ch: 'general', u: 'sorrel', text: 'Dark mode toggle is in the top bar now, nice.' },
  { ch: 'general', u: 'lumi', text: 'Reading the WebSocket code tonight. Very readable so far.' },
  { ch: 'general', u: 'odessa', text: 'Friendly reminder: staff never DM first. If someone does, report them.' },
  { ch: 'general', u: 'nessa', text: 'Anyone else just leave Tapaia Square open in a tab all day?' },
  { ch: 'general', u: 'pim', text: 'gm everyone ☕' },
  { ch: 'lobby', u: 'odessa', text: 'Welcome to everyone arriving today! Ask in #support if you get stuck.' },
  { ch: 'support', u: 'lumi', text: 'Tip: you can sign in with any EIP-6963 wallet, Rabby and MetaMask both show up as “Detected”.' },
];

export const AUTO_REPLIES = [
  'Ha, good to see you here!', 'Welcome! Pull up a bench.', 'Tea cart is that way →', 'Agreed 🙂',
  'I’ll be by the maple if you need me.', 'Have you tried the mint tea yet?', 'Love that. Tell me more?',
];
