// Tapaia Phase 1 prototype server: REST for auth/profile, WebSocket for live chat.
import express from 'express';
import http from 'node:http';
import path from 'node:path';
import fs from 'node:fs';
import { execSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import { WebSocketServer, WebSocket } from 'ws';
import * as cookie from 'cookie';
import { createPublicClient, getAddress, http as viemHttp, verifyMessage } from 'viem';
import { mainnet } from 'viem/chains';
import { generateSiweNonce, parseSiweMessage } from 'viem/siwe';
import { db, load, save, addMessage, newId, newToken, publicUser, type User } from './store';
import { canPost, canRead, byteLen } from '../shared/perms';
import { normalizeAvatar, randomAvatar } from '../shared/avatar';
import type { AppConfig, Channel, ClientMsg, Message, PublicUser, ServerMsg, Tile } from '../shared/types';
import { ZC_ADDRESS } from './seed';
import { randomName, RESERVED } from './names';
import { startBots, onUserMessage } from './bots';
import { checkZipName, claimUrl, isZipLabel, resolveZipName, shortAddress, ZIPCOIN_API, ZIPCOIN_SITE } from './zipcoin';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const PORT = Number(process.env.PORT || 4417);
const HOST = process.env.LISTEN_HOST || '0.0.0.0'; // bind all interfaces so hosts like Render can route to us
const PROD = process.env.NODE_ENV === 'production';
const WC_ID = process.env.WALLETCONNECT_PROJECT_ID || process.env.VITE_WALLETCONNECT_PROJECT_ID || null;
const RPC = process.env.ETH_RPC_URL || 'https://ethereum-rpc.publicnode.com';
const FOUNDER_SLOTS = Number(process.env.FOUNDER_SLOTS || 100); // X is undecided; demo value
const SPEAK_MIN = 1000; // zipcoin's live Speak minimum per the spec; S is undecided
const COOKIE = 'tapaia_sid';
const SESSION_MS = 7 * 86_400_000;
let BUILD = (process.env.RENDER_GIT_COMMIT || process.env.SOURCE_COMMIT || '').slice(0, 7) || 'dev';
if (BUILD === 'dev') try { BUILD = execSync('git rev-parse --short HEAD', { cwd: ROOT, stdio: ['ignore', 'pipe', 'ignore'] }).toString().trim(); } catch { /* not a git checkout */ }

load();
const rpcClient = createPublicClient({ chain: mainnet, transport: viemHttp(RPC) });
const nonces = new Map<string, number>(); // nonce -> expiry

// ---------------------------------------------------------------- helpers
const userById = (id?: string) => (id ? db.users[id] : undefined);
const channelById = (id: string) => db.channels.find((c) => c.id === id);
const TILES: Tile[] = ['c1', 'c2', 'c3', 'c4', 'c5', 'c6'];

function sessionUser(req: http.IncomingMessage): User | undefined {
  const sid = cookie.parse(req.headers.cookie || '')[COOKIE];
  const s = sid ? db.sessions[sid] : undefined;
  if (!s || s.expires < Date.now()) return undefined;
  return db.users[s.userId];
}

function setSession(req: express.Request, res: express.Response, userId: string) {
  const token = newToken();
  db.sessions[token] = { userId, expires: Date.now() + SESSION_MS };
  save();
  const secure = req.secure || req.headers['x-forwarded-proto'] === 'https';
  res.setHeader('Set-Cookie', cookie.serialize(COOKIE, token, { httpOnly: true, sameSite: 'lax', secure, path: '/', maxAge: SESSION_MS / 1000 }));
}

function uniqueHandle(base: string) {
  let h = base.replace(/[^a-z0-9_]/g, '').slice(0, 16) || 'citizen';
  const taken = (x: string) => Object.values(db.users).some((u) => u.handle.toLowerCase() === x);
  if (!taken(h)) return h;
  for (let i = 2; ; i++) if (!taken(`${h}${i}`)) return `${h}${i}`;
}
function uniqueCitizenName(base: string) {
  const taken = (x: string) => Object.values(db.users).some((u) => u.citizenName.toLowerCase() === x.toLowerCase());
  if (!taken(base)) return base;
  for (let i = 2; ; i++) if (!taken(`${base} ${'II III IV V VI VII VIII IX X'.split(' ')[i - 2] ?? i}`)) return `${base} ${'II III IV V VI VII VIII IX X'.split(' ')[i - 2] ?? i}`;
}

function newUser(kind: 'demo' | 'wallet', opts: { citizenName?: string; handle?: string; avatar?: unknown; address?: string }): User {
  const r = randomName();
  const id = newId(kind === 'demo' ? 'd' : 'w');
  const u: User = {
    id, kind, handle: uniqueHandle((opts.handle || r.handle).toLowerCase()),
    citizenName: uniqueCitizenName(validCitizenName(opts.citizenName) ? opts.citizenName!.trim() : r.citizenName),
    avatar: normalizeAvatar(opts.avatar) ?? randomAvatar(), tile: TILES[Math.floor(Math.random() * 6)],
    badges: [], isCitizen: false, presence: 'off', linked: false, createdAt: Date.now(), speaks: 0,
    status: kind === 'demo' ? 'trying the demo' : 'new here',
  };
  if (opts.address) { u.address = opts.address; u.wallet = `${opts.address.slice(0, 6)}…${opts.address.slice(-4)}`; }
  db.users[id] = u;
  save();
  return u;
}

function validCitizenName(n?: unknown): n is string {
  if (typeof n !== 'string') return false;
  const t = n.trim();
  return t.length >= 2 && t.length <= 32 && /^[\p{L}][\p{L} '\-.]*$/u.test(t) && !RESERVED.includes(t.toLowerCase());
}

// ---------------------------------------------------------------- Zipcoin names
const STAFF_WORDS = ['tapaia', 'tapaiasquare', 'team', 'admin', 'moderator', 'mod', 'support', 'staff'];
// One Tapaia account per name. A real (wallet-verified) holder always wins over a demo copy.
function clearZip(u: User) {
  if (!u.zip) return false;
  const was = u.zip.name;
  delete u.zip;
  if (u.handle === was) {
    const back = u.preZipHandle && !Object.values(db.users).some((x) => x.id !== u.id && x.handle === u.preZipHandle) ? u.preZipHandle : undefined;
    u.handle = back ?? uniqueHandle(u.address ? `citizen${u.address.slice(2, 6).toLowerCase()}` : 'citizen');
  }
  delete u.preZipHandle;
  return true;
}
/** Give `u` the Zipcoin name `name` (or take it away with null). Returns true if anything visible changed. */
function applyZip(u: User, name: string | null, demo = false): boolean {
  if (!name) return clearZip(u);
  if (u.zip?.name === name && !!u.zip.demo === demo) return false;
  if (u.zip) clearZip(u);
  for (const o of Object.values(db.users)) {
    if (o.id === u.id) continue;
    if (o.zip?.name === name) { clearZip(o); broadcastUser(o); }   // demo copy or a stale holder
  }
  // the name becomes the handle (@alice), unless it's one of our own staff/brand words (a verified holder of a
  // lore or "kept" name like gladias or vitalik does get it: the seal shows it's really theirs)
  if (!STAFF_WORDS.includes(name)) {
    for (const o of Object.values(db.users)) if (o.id !== u.id && o.handle === name) { o.handle = uniqueHandle(name); broadcastUser(o); }
    if (u.handle !== name) { u.preZipHandle = u.handle; u.handle = name; }
  }
  u.zip = demo ? { name, demo: true } : { name };
  return true;
}
/** Look up the wallet's Zipcoin name (cached) and apply it. API down = keep what we have; the UI falls back to the short address. */
async function refreshZip(u: User, force = false) {
  if (u.kind !== 'wallet' || !u.address) return;
  const r = await resolveZipName(u.address, { force });
  if (!r.ok) return;
  if (applyZip(u, r.name)) { save(); broadcastUser(u); rehelloUser(u.id); }
}

const founderUsed = () => Object.values(db.users).filter((u) => u.entry === 'founder').length;

// ---------------------------------------------------------------- websocket hub
interface Client { ws: WebSocket; userId?: string; room: string | null; idle: boolean; recent: number[] }
const clients = new Set<Client>();
const send = (c: Client, m: ServerMsg) => c.ws.readyState === WebSocket.OPEN && c.ws.send(JSON.stringify(m));

export function broadcastMessage(m: Message, update = false) {
  const ch = channelById(m.channel);
  if (!ch) return;
  for (const c of clients) if (canRead(userById(c.userId), ch)) send(c, update ? { t: 'update', m } : { t: 'msg', m });
}
export function broadcastUser(u: User) {
  const pu = publicUser(u);
  for (const c of clients) send(c, { t: 'user', u: pu });
}
export function postMessage(m: Parameters<typeof addMessage>[0]) {
  const msg = addMessage(m);
  broadcastMessage(msg);
  return msg;
}
export const connectedCount = () => clients.size;
export { userById, channelById };

function visibleMessages(u: User | undefined): Message[] {
  const out: Message[] = [];
  for (const ch of db.channels) {
    if (!canRead(u, ch)) continue;
    const ms = db.messages.filter((m) => m.channel === ch.id);
    out.push(...ms.slice(-150));
  }
  return out;
}
function hello(c: Client) {
  const u = userById(c.userId);
  send(c, {
    t: 'hello', me: u ? publicUser(u) : null,
    users: Object.values(db.users).filter((x) => x.kind !== 'demo' || x.presence !== 'off' || x.id === u?.id || Date.now() - x.createdAt < 3_600_000 || db.messages.some((m) => m.userId === x.id)).map(publicUser),
    channels: db.channels.filter((ch) => ch.layer !== 'dm' || canRead(u, ch)),
    messages: visibleMessages(u),
  });
}
function rehelloUser(userId: string) { for (const c of clients) if (c.userId === userId) hello(c); }

// presence + enter/leave lines for Tapaia Square
const leaveTimers = new Map<string, NodeJS.Timeout>();
const inSquare = new Set<string>();
function refreshPresence(userId: string) {
  const u = userById(userId);
  if (!u || u.kind === 'seed' || u.kind === 'bot') return;
  const mine = [...clients].filter((c) => c.userId === userId);
  const presence = mine.length === 0 ? 'off' : mine.every((c) => c.idle) ? 'idle' : 'here';
  const room = mine.find((c) => c.room)?.room ?? undefined;
  const wasSq = inSquare.has(userId);
  const nowSq = u.isCitizen && mine.some((c) => c.room === 'square');
  if (nowSq && !wasSq) {
    inSquare.add(userId);
    const t = leaveTimers.get(userId);
    if (t) { clearTimeout(t); leaveTimers.delete(userId); }
    else postMessage({ channel: 'square', userId, kind: 'system', sys: 'enter', text: 'has entered the square' });
  } else if (!nowSq && wasSq) {
    inSquare.delete(userId);
    leaveTimers.set(userId, setTimeout(() => {
      leaveTimers.delete(userId);
      postMessage({ channel: 'square', userId, kind: 'system', sys: 'leave', text: 'left the square' });
    }, 5000));
  }
  if (u.presence !== presence || u.room !== room) { u.presence = presence; u.room = room; broadcastUser(u); }
}

function handle(c: Client, msg: ClientMsg) {
  const u = userById(c.userId);
  switch (msg.t) {
    case 'room': c.room = typeof msg.channel === 'string' ? msg.channel : null; if (u) refreshPresence(u.id); return;
    case 'presence': c.idle = msg.state === 'idle'; if (u) refreshPresence(u.id); return;
  }
  if (!u) return send(c, { t: 'error', text: 'Sign in first.' });
  switch (msg.t) {
    case 'send': {
      const ch = channelById(msg.channel);
      if (!ch || !canPost(u, ch)) return send(c, { t: 'error', text: 'You can’t post in this room.' });
      const text = String(msg.text ?? '').trim();
      if (!text) return;
      if (text.length > 2000) return send(c, { t: 'error', text: 'Message too long (max 2,000 characters).' });
      const now = Date.now();
      c.recent = c.recent.filter((t) => now - t < 10_000);
      if (c.recent.length >= 8) return send(c, { t: 'error', text: 'Slow down a little: max 8 messages per 10 seconds.' });
      c.recent.push(now);
      const speak = msg.mode === 'speak';
      if (speak && (ch.id !== 'square' || byteLen(text) > 280)) return send(c, { t: 'error', text: 'Speak posts are for Tapaia Square and max 280 bytes.' });
      const replyTo = typeof msg.replyTo === 'number' && db.messages.some((m) => m.id === msg.replyTo && m.channel === ch.id) ? msg.replyTo : undefined;
      const m = postMessage({ channel: ch.id, userId: u.id, kind: speak ? 'speak' : 'text', text, replyTo, simulated: speak || undefined });
      if (speak) { u.speaks++; broadcastUser(u); save(); }
      onUserMessage(u, ch, m);
      return;
    }
    case 'react': {
      const m = db.messages.find((x) => x.id === msg.id);
      const ch = m && channelById(m.channel);
      if (!m || !ch || !canRead(u, ch) || m.deleted) return;
      const e = String(msg.emoji || '').slice(0, 8);
      if (!e) return;
      const list = m.reactions[e] ?? [];
      if (!list.includes(u.id) && Object.keys(m.reactions).length >= 12 && !m.reactions[e]) return;
      m.reactions[e] = list.includes(u.id) ? list.filter((x) => x !== u.id) : [...list, u.id];
      if (!m.reactions[e].length) delete m.reactions[e];
      save(); broadcastMessage(m, true); return;
    }
    case 'delete': {
      const m = db.messages.find((x) => x.id === msg.id);
      if (!m || m.kind === 'system') return;
      const mod = u.badges.includes('mod') || u.badges.includes('team');
      if (m.userId !== u.id && !mod) return;
      m.deleted = true; m.text = ''; m.reactions = {}; delete m.card;
      save(); broadcastMessage(m, true); return;
    }
    case 'edit': {
      const m = db.messages.find((x) => x.id === msg.id);
      const text = String(msg.text ?? '').trim();
      if (!m || m.userId !== u.id || m.kind !== 'text' || m.deleted || !text || text.length > 2000) return;
      m.text = text; m.edited = true; save(); broadcastMessage(m, true); return;
    }
    case 'typing': {
      const ch = channelById(msg.channel);
      if (!ch || !canPost(u, ch)) return;
      for (const o of clients) if (o !== c && o.userId !== u.id && canRead(userById(o.userId), ch)) send(o, { t: 'typing', channel: ch.id, userId: u.id });
      return;
    }
    case 'dm': {
      const other = userById(msg.userId);
      if (!other || other.id === u.id) return;
      if (other.kind === 'bot') return send(c, { t: 'error', text: 'Bots can’t be messaged.' });
      if (!u.isCitizen) return send(c, { t: 'error', text: 'Become a citizen to send direct messages.' });
      const id = `dm:${[u.id, other.id].sort().join(':')}`;
      let ch = channelById(id);
      if (!ch) {
        ch = { id, name: 'dm', layer: 'dm', topic: 'Direct message', members: [u.id, other.id] };
        db.channels.push(ch); save();
      }
      const msgs = db.messages.filter((m) => m.channel === id).slice(-150);
      for (const o of clients) if (o.userId === u.id || o.userId === other.id) send(o, { t: 'channel', c: ch, messages: msgs, open: o === c });
      return;
    }
  }
}

// ---------------------------------------------------------------- http
const app = express();
app.set('trust proxy', true);
app.use(express.json({ limit: '32kb' }));

const me = (req: express.Request) => sessionUser(req);

app.get('/api/health', (_req, res) => res.json({ ok: true, build: BUILD })); // host health check

app.get('/api/config', (_req, res) => {
  const cfg: AppConfig = {
    walletConnectProjectId: WC_ID, build: BUILD,
    founderSlots: { total: FOUNDER_SLOTS, used: founderUsed(), demoValue: true },
    zcAddress: ZC_ADDRESS, speakMinimum: SPEAK_MIN, repoUrl: 'https://github.com/tapaia/tapaia',
    zipcoin: { api: ZIPCOIN_API, site: ZIPCOIN_SITE },
  };
  res.json(cfg);
});
app.get('/api/me', (req, res) => { const u = me(req); res.json({ me: u ? publicUser(u) : null }); });

app.get('/api/demo/suggest', (_req, res) => res.json({ ...randomName(), avatar: randomAvatar() }));

app.post('/api/demo', (req, res) => {
  const { citizenName, handle, avatar, skipArrival } = req.body ?? {};
  const u = newUser('demo', { citizenName, handle: typeof handle === 'string' ? handle : undefined, avatar });
  if (skipArrival) { u.isCitizen = true; u.arrivalAt = Date.now(); u.status = 'demo citizen'; save(); }
  setSession(req, res, u.id);
  broadcastUser(u);
  res.json({ me: publicUser(u) });
});

app.get('/api/siwe/nonce', (_req, res) => {
  const nonce = generateSiweNonce();
  nonces.set(nonce, Date.now() + 10 * 60_000);
  for (const [n, exp] of nonces) if (exp < Date.now()) nonces.delete(n);
  res.json({ nonce });
});

app.post('/api/siwe/verify', async (req, res) => {
  try {
    const { message, signature } = req.body ?? {};
    if (typeof message !== 'string' || typeof signature !== 'string' || !/^0x[0-9a-fA-F]+$/.test(signature)) throw new Error('Bad request');
    const f = parseSiweMessage(message);
    const hosts = [req.headers['x-forwarded-host'], req.headers.host].flat().filter(Boolean).map(String);
    if (!f.domain || !hosts.includes(f.domain)) throw new Error('Domain mismatch');
    if (!f.uri || new URL(f.uri).host !== f.domain) throw new Error('URI mismatch');
    if (f.chainId !== 1) throw new Error('Please sign in on Ethereum mainnet');
    if (!f.nonce || !nonces.has(f.nonce) || nonces.get(f.nonce)! < Date.now()) throw new Error('Nonce expired, try again');
    if (!f.address) throw new Error('No address');
    if (f.expirationTime && f.expirationTime.getTime() < Date.now()) throw new Error('Message expired');
    if (f.issuedAt && Math.abs(Date.now() - f.issuedAt.getTime()) > 10 * 60_000) throw new Error('Message too old');
    nonces.delete(f.nonce); // single use
    const address = getAddress(f.address);
    let ok = await verifyMessage({ address, message, signature: signature as `0x${string}` }).catch(() => false);
    if (!ok) ok = await rpcClient.verifyMessage({ address, message, signature: signature as `0x${string}` }).catch(() => false); // EIP-1271 / ERC-6492
    if (!ok) throw new Error('Signature did not verify');
    let u = Object.values(db.users).find((x) => x.address === address);
    if (!u) {
      const short = address.slice(2, 6).toLowerCase();
      u = newUser('wallet', { handle: `citizen${short}`, address });
    }
    const z = await resolveZipName(address); // cached 10 min, never throws, ~4 s worst case
    if (z.ok) applyZip(u, z.name);
    save();
    setSession(req, res, u.id);
    broadcastUser(u);
    res.json({ me: publicUser(u) });
  } catch (e) {
    res.status(400).json({ error: (e as Error).message || 'Sign-in failed' });
  }
});

app.post('/api/logout', (req, res) => {
  const sid = cookie.parse(req.headers.cookie || '')[COOKIE];
  if (sid) { delete db.sessions[sid]; save(); }
  res.setHeader('Set-Cookie', cookie.serialize(COOKIE, '', { httpOnly: true, sameSite: 'lax', path: '/', maxAge: 0 }));
  res.json({ ok: true });
});

app.post('/api/arrival', (req, res) => {
  const u = me(req);
  if (!u) return res.status(401).json({ error: 'Sign in first' });
  if (u.isCitizen && u.entry) return res.status(400).json({ error: 'You are already a citizen' });
  const { path: p, text } = req.body ?? {};
  const t = String(text ?? '').trim();
  if (!t || byteLen(t) > 280) return res.status(400).json({ error: 'Arrival message must be 1–280 bytes' });
  if (p === 'founder') {
    if (founderUsed() >= FOUNDER_SLOTS) return res.status(400).json({ error: 'No founder slots left' });
    u.entry = 'founder'; u.badges = [...new Set([...u.badges, 'founder' as const])];
  } else if (p === 'burn') {
    // SIMULATED: no transaction is ever built or sent by this prototype.
    u.entry = 'burn'; u.badges = [...new Set([...u.badges, 'onchain' as const])];
  } else return res.status(400).json({ error: 'Unknown entry path' });
  u.isCitizen = true; u.arrivalText = t; u.arrivalAt = Date.now(); u.status = 'just arrived';
  save();
  postMessage({ channel: 'square', userId: u.id, kind: 'arrival', text: t, simulated: p === 'burn' || undefined });
  postMessage({ channel: 'general', userId: u.id, kind: 'system', sys: 'citizen', text: 'just became a citizen. Say hi!' });
  broadcastUser(u);
  rehelloUser(u.id);
  res.json({ me: publicUser(u), founderSlots: { total: FOUNDER_SLOTS, used: founderUsed() } });
});

app.patch('/api/profile', (req, res) => {
  const u = me(req);
  if (!u) return res.status(401).json({ error: 'Sign in first' });
  const b = req.body ?? {};
  if (b.citizenName !== undefined) {
    if (!validCitizenName(b.citizenName)) return res.status(400).json({ error: 'Citizen names are 2–32 letters, and some names are reserved.' });
    const n = b.citizenName.trim();
    if (Object.values(db.users).some((x) => x.id !== u.id && x.citizenName.toLowerCase() === n.toLowerCase())) return res.status(400).json({ error: 'That citizen name is taken.' });
    u.citizenName = n;
  }
  if (b.handle !== undefined) {
    const h = String(b.handle).trim().toLowerCase();
    const locked = !!u.zip && u.handle === u.zip.name; // a Zipcoin name is your handle while you hold it
    if (locked) {
      if (h !== u.handle) return res.status(400).json({ error: 'Your handle is your Zipcoin name. Change your citizen name instead.' });
    } else {
      if (!/^[a-z0-9_]{3,20}$/.test(h) || RESERVED.includes(h)) return res.status(400).json({ error: 'Handles are 3–20 letters, numbers or _.' });
      if (Object.values(db.users).some((x) => x.id !== u.id && x.handle === h)) return res.status(400).json({ error: 'That handle is taken.' });
      u.handle = h;
    }
  }
  if (b.avatar !== undefined) { const a = normalizeAvatar(b.avatar); if (!a) return res.status(400).json({ error: 'Bad avatar' }); u.avatar = a; }   // v1 or v2 in, v2 stored
  if (typeof b.linked === 'boolean') u.linked = b.linked;
  if (typeof b.about === 'string') u.about = b.about.slice(0, 160);
  if (typeof b.status === 'string') u.status = b.status.slice(0, 40);
  save(); broadcastUser(u);
  res.json({ me: publicUser(u) });
});

// ---- Zipcoin names (read-only proxies to zipcoin.cash's public API; nothing here sends a transaction)
app.get('/api/zipcoin/identity/:address', async (req, res) => {
  const a = String(req.params.address || '');
  if (!/^0x[0-9a-fA-F]{40}$/.test(a)) return res.status(400).json({ error: 'Bad address' });
  const r = await resolveZipName(a);
  res.json({ address: a.toLowerCase(), name: r.name, domain: r.name ? `${r.name}.zipcoin.cash` : null, display: r.display, ok: r.ok, short: shortAddress(a) });
});
app.get('/api/zipcoin/check', async (req, res) => {
  const r = await checkZipName(String(req.query.name ?? ''));
  res.json({ ...r, claimUrl: r.state === 'available' || r.state === 'reserved' ? claimUrl(r.name) : null });
});
const lastRefresh = new Map<string, number>();
app.post('/api/zipcoin/refresh', async (req, res) => {
  const u = me(req);
  if (!u) return res.status(401).json({ error: 'Sign in first' });
  if (u.kind !== 'wallet' || !u.address) return res.status(400).json({ error: 'Only wallet accounts have a Zipcoin name to look up.' });
  const force = Date.now() - (lastRefresh.get(u.id) ?? 0) > 15_000;
  if (force) lastRefresh.set(u.id, Date.now());
  const r = await resolveZipName(u.address, { force });
  if (r.ok && applyZip(u, r.name)) { save(); broadcastUser(u); rehelloUser(u.id); }
  res.json({ me: publicUser(u), ok: r.ok });
});
// DEMO accounts only: a simulated claim. Nothing is burned and nothing is registered on zipcoin.cash.
app.post('/api/zipcoin/demo-claim', async (req, res) => {
  const u = me(req);
  if (!u) return res.status(401).json({ error: 'Sign in first' });
  if (u.kind !== 'demo') return res.status(400).json({ error: 'Real wallets claim on zipcoin.cash. Simulated claims are for demo accounts.' });
  const name = String(req.body?.name ?? '').trim().toLowerCase();
  if (!isZipLabel(name)) return res.status(400).json({ error: 'Names are 3 to 24 lowercase letters, digits and hyphens, with no hyphen at either end.' });
  if (Object.values(db.users).some((o) => o.id !== u.id && o.zip?.name === name)) return res.status(400).json({ error: 'Someone in Tapaia already holds that name.' });
  const c = await checkZipName(name);
  if (c.state === 'error') return res.status(503).json({ error: 'Couldn’t reach zipcoin.cash to check that name. Try again in a moment.' });
  if (c.state !== 'available') return res.status(400).json({ error: `That name is ${c.state} on zipcoin.cash.` });
  applyZip(u, name, true);
  save(); broadcastUser(u); rehelloUser(u.id);
  res.json({ me: publicUser(u), simulated: true });
});

app.post('/api/report', (req, res) => { if (!me(req)) return res.status(401).end(); res.json({ ok: true, note: 'Reports are stubbed in the prototype.' }); });

const DIST = path.join(ROOT, 'dist');
if (PROD && fs.existsSync(DIST)) {
  app.use(express.static(DIST, { index: false, maxAge: '1h' }));
  app.get(/^\/(?!api|ws).*/, (_req, res) => res.sendFile(path.join(DIST, 'index.html')));
}

const server = http.createServer(app);
const wss = new WebSocketServer({ noServer: true });
server.on('upgrade', (req, socket, head) => {
  if (!req.url?.startsWith('/ws')) return socket.destroy();
  wss.handleUpgrade(req, socket, head, (ws) => {
    const u = sessionUser(req);
    const c: Client = { ws, userId: u?.id, room: null, idle: false, recent: [] };
    clients.add(c);
    hello(c);
    if (u) { refreshPresence(u.id); if (u.kind === 'wallet') void refreshZip(u); }
    ws.on('message', (raw) => { try { handle(c, JSON.parse(String(raw))); } catch { /* ignore bad frames */ } });
    ws.on('close', () => { clients.delete(c); if (c.userId) refreshPresence(c.userId); });
  });
});
setInterval(() => { for (const c of clients) if (c.ws.readyState === WebSocket.OPEN) c.ws.ping(); }, 25_000);

// demo users who never connected stay "off"; on boot everyone real is offline
for (const u of Object.values(db.users)) if (u.kind === 'demo' || u.kind === 'wallet') { u.presence = 'off'; u.room = undefined; }

server.listen(PORT, HOST, () => {
  console.log(`Tapaia prototype on http://${HOST === '0.0.0.0' ? 'localhost' : HOST}:${PORT} (build ${BUILD}${PROD ? '' : ', API only, use Vite on :5173'})`);
  console.log(WC_ID ? 'WalletConnect enabled' : 'WALLETCONNECT_PROJECT_ID not set: injected wallets and Coinbase Wallet only');
  startBots();
});

export type { Channel, PublicUser };
