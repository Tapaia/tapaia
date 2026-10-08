// In-memory store with a JSON snapshot on disk (server/data/db.json, git-ignored).
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import { fileURLToPath } from 'node:url';
import type { Channel, Message, PublicUser } from '../shared/types';
import { CHANNELS, SEED_MESSAGES, SEED_USERS } from './seed';
import { normalizeAvatar, randomAvatar } from '../shared/avatar';

const DIR = process.env.TAPAIA_DATA_DIR || path.join(path.dirname(fileURLToPath(import.meta.url)), 'data'); // override used by verify's mocked-zipcoin instance
const FILE = path.join(DIR, 'db.json');
const MAX_PER_CHANNEL = 400;

export interface User extends PublicUser { address?: string; preZipHandle?: string }
export interface Session { userId: string; expires: number }

interface DB {
  version: number;
  users: Record<string, User>;
  channels: Channel[];
  messages: Message[];
  sessions: Record<string, Session>;
  nextId: number;
}

const DB_VERSION = 3; // v2: Zipcoin names (demo names on two seed citizens) · v3: Cozy HD avatars (v2 avatar configs)
export let db: DB;

function seed(): DB {
  const now = Date.now();
  const users: Record<string, User> = {};
  for (const s of SEED_USERS) {
    users[s.id] = {
      id: s.id, handle: s.handle, citizenName: s.citizenName, avatar: s.avatar, tile: s.tile, badges: s.badges,
      isCitizen: s.kind !== 'bot', entry: s.entry, arrivalText: s.arrivalText, arrivalAt: now - 86_400_000 * (2 + Math.floor(Math.random() * 5)),
      wallet: s.wallet, kind: s.kind ?? 'seed', status: s.status, presence: s.presence, room: s.room,
      linked: s.linked ?? false, about: s.about, district: s.district, createdAt: now - 86_400_000 * 6, speaks: s.id === 'wren' ? 1 : 0,
      ...(s.zipDemo ? { zip: { name: s.zipDemo, demo: true } } : {}),
    };
  }
  const messages: Message[] = [];
  let id = 1;
  const ids: number[] = [];
  for (const m of SEED_MESSAGES) {
    const msg: Message = {
      id: id++, channel: m.ch, userId: m.u, kind: m.kind ?? 'text', text: m.text, ts: now - m.ago * 60_000,
      reactions: m.react ?? {}, sys: m.sys, card: m.card, sample: m.sample, simulated: m.simulated,
    };
    if (m.replyTo !== undefined) msg.replyTo = ids[m.replyTo];
    ids.push(msg.id);
    messages.push(msg);
  }
  return { version: DB_VERSION, users, channels: CHANNELS.map((c) => ({ ...c })), messages, sessions: {}, nextId: id };
}

export function load() {
  try {
    const raw = JSON.parse(fs.readFileSync(FILE, 'utf8')) as DB;
    if (raw.version === 2) { migrateV3(raw); db = raw; save(true); return; }
    if (raw.version === DB_VERSION) { db = raw; return; }
  } catch { /* fresh start */ }
  db = seed();
  save(true);
}

/** v2 -> v3: keep everyone, move avatars to v2 configs (lossless for v1), and dress the seed citizens in the new cast. */
function migrateV3(raw: DB) {
  const seeds = new Map(SEED_USERS.map((s) => [s.id, s]));
  for (const u of Object.values(raw.users)) {
    const s = seeds.get(u.id);
    u.avatar = s && (u.kind === 'seed' || u.kind === 'bot') ? s.avatar : normalizeAvatar(u.avatar) ?? randomAvatar();
  }
  raw.version = 3;
}

let timer: NodeJS.Timeout | null = null;
export function save(now = false) {
  const write = () => { fs.mkdirSync(DIR, { recursive: true }); fs.writeFileSync(FILE + '.tmp', JSON.stringify(db)); fs.renameSync(FILE + '.tmp', FILE); timer = null; };
  if (now) return write();
  if (!timer) timer = setTimeout(write, 1500);
}

export function addMessage(m: Omit<Message, 'id' | 'ts' | 'reactions'> & Partial<Pick<Message, 'ts' | 'reactions'>>): Message {
  const msg: Message = { reactions: {}, ts: Date.now(), ...m, id: db.nextId++ };
  db.messages.push(msg);
  const inCh = db.messages.filter((x) => x.channel === msg.channel);
  if (inCh.length > MAX_PER_CHANNEL) {
    const drop = new Set(inCh.slice(0, inCh.length - MAX_PER_CHANNEL).map((x) => x.id));
    db.messages = db.messages.filter((x) => !drop.has(x.id));
  }
  save();
  return msg;
}

export const newId = (p: string) => `${p}_${crypto.randomBytes(6).toString('hex')}`;
export const newToken = () => crypto.randomBytes(24).toString('base64url');

export function publicUser(u: User): PublicUser {
  const { address: _a, preZipHandle: _p, ...rest } = u;
  return rest;
}
