// Read-only bots + ambient demo chatter.
// - ZC Price Bot: real data from GeckoTerminal's public API (no key). Posts nothing if the fetch fails.
// - Book Feed Bot: SAMPLE data only (labelled), not the live zipcoin feed.
// - Ambient chatter + replies from the fictional seeded citizens so rooms feel alive (simulated).
import { db } from './store';
import { AMBIENT, AUTO_REPLIES, ZC_ADDRESS } from './seed';
import { postMessage, connectedCount, broadcastUser } from './index';
import type { Channel, Message } from '../shared/types';
import type { User } from './store';

const GT = 'https://api.geckoterminal.com/api/v2/networks/eth';
const PRICE_EVERY = 30 * 60_000;

const usd = (n: number, d = 0) => '$' + n.toLocaleString('en-US', { maximumFractionDigits: d, minimumFractionDigits: d });
const compact = (n: number) => '$' + Intl.NumberFormat('en-US', { notation: 'compact', maximumFractionDigits: 1 }).format(n);

async function postPrice() {
  try {
    const [tok, pools] = await Promise.all([
      fetch(`${GT}/tokens/${ZC_ADDRESS.toLowerCase()}`, { headers: { accept: 'application/json' } }).then((r) => r.json()),
      fetch(`${GT}/tokens/${ZC_ADDRESS.toLowerCase()}/pools?page=1`, { headers: { accept: 'application/json' } }).then((r) => r.json()),
    ]);
    const a = tok?.data?.attributes;
    const price = Number(a?.price_usd);
    if (!price) throw new Error('no price');
    const top = pools?.data?.[0]?.attributes;
    const ch24 = top?.price_change_percentage?.h24 !== undefined ? Number(top.price_change_percentage.h24) : null;
    const liq = Number(a.total_reserve_in_usd || 0);
    const vol = Number(a.volume_usd?.h24 || 0);
    const parts = [`ZC ${usd(price, price < 1 ? 5 : 2)}`];
    if (ch24 !== null) parts.push(`24h ${ch24 >= 0 ? '+' : '−'}${Math.abs(ch24).toFixed(1)}% (${top.name})`);
    parts.push(`liquidity ${compact(liq)}`, `24h volume ${compact(vol)}`);
    const poolAddr = pools?.data?.[0]?.attributes?.address;
    postMessage({
      channel: 'feeds', userId: 'pricebot', kind: 'text', text: parts.join(' · ') + '. Source: GeckoTerminal. Data only, not advice.',
      card: poolAddr ? { url: `geckoterminal.com/eth/pools/${poolAddr}`, title: `${top.name} on GeckoTerminal`, desc: 'Live pool data · opens GeckoTerminal' } : undefined,
    });
  } catch (e) {
    console.warn('price bot: fetch failed, skipping', (e as Error).message);
  }
}

const SAMPLE_BOOK = [
  'SAMPLE · New Book post: “Meet at the tea cart at 4 longhours.” · burned 1,000 ZC',
  'SAMPLE · Notable burn: 12,500 ZC burned in one Speak post.',
  'SAMPLE · New Book post: “The library got a new shelf. Still business books.” · burned 1,000 ZC',
  'SAMPLE · Knock: a citizen knocked on the Order’s door (sample event).',
];

const pick = <T,>(xs: T[]) => xs[Math.floor(Math.random() * xs.length)];
const lastBy = (uid: string) => [...db.messages].reverse().find((m) => m.userId === uid);
const jitter = (min: number, max: number) => min + Math.random() * (max - min);

function ambient() {
  if (connectedCount() > 0) {
    const r = Math.random();
    if (r < 0.15) {
      // a seeded citizen wanders in or out of the square
      const u = db.users[pick(['marek', 'pim', 'corvin', 'tobin'])];
      const entering = u.room !== 'square';
      u.room = entering ? 'square' : undefined;
      u.presence = entering ? 'here' : 'off';
      broadcastUser(u);
      postMessage({ channel: 'square', userId: u.id, kind: 'system', sys: entering ? 'enter' : 'leave', text: entering ? 'has entered the square' : 'left the square' });
    } else {
      const a = pick(AMBIENT);
      const u = db.users[a.u];
      if (u && u.presence !== 'off') postMessage({ channel: a.ch, userId: a.u, kind: 'text', text: a.text });
    }
  }
  setTimeout(ambient, jitter(60_000, 150_000));
}

// seeded citizens answer DMs and @mentions (simulated)
const lastReply = new Map<string, number>();
export function onUserMessage(u: User, ch: Channel, m: Message) {
  if (u.kind === 'seed' || u.kind === 'bot') return;
  let target: User | undefined;
  if (ch.layer === 'dm') {
    target = ch.members?.map((id) => db.users[id]).find((x) => x && x.kind === 'seed');
  } else if (ch.id !== 'announcements' && ch.id !== 'feeds') {
    const ic = ch.layer === 'ic';
    target = Object.values(db.users).find((x) => x.kind === 'seed' && m.text.toLowerCase().includes('@' + (ic ? x.citizenName : x.handle).toLowerCase()));
  }
  if (!target) return;
  const key = `${ch.id}:${target.id}`;
  if (Date.now() - (lastReply.get(key) ?? 0) < 15_000) return;
  lastReply.set(key, Date.now());
  const who = ch.layer === 'ic' ? `@${u.citizenName}` : `@${u.handle}`;
  const t = target;
  setTimeout(() => postMessage({ channel: ch.id, userId: t.id, kind: 'text', text: ch.layer === 'dm' ? pick(AUTO_REPLIES) : `${who} ${pick(AUTO_REPLIES)}`, replyTo: ch.layer === 'dm' ? undefined : m.id }), jitter(2500, 5000));
}

export function startBots() {
  const lp = lastBy('pricebot');
  if (!lp || Date.now() - lp.ts > PRICE_EVERY) setTimeout(postPrice, 1500);
  setInterval(postPrice, PRICE_EVERY);
  setInterval(() => { if (connectedCount() > 0) postMessage({ channel: 'feeds', userId: 'bookbot', kind: 'text', text: pick(SAMPLE_BOOK), sample: true }); }, 20 * 60_000);
  setTimeout(ambient, jitter(30_000, 60_000));
}
