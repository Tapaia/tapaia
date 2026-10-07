import { create } from 'zustand';
import type { AppConfig, Channel, ClientMsg, Message, PublicUser, ServerMsg } from '../shared/types';

export type ThemePref = 'system' | 'light' | 'dark';
export type ModalState =
  | null
  | { kind: 'demo' }
  | { kind: 'arrival' }
  | { kind: 'profile' }
  | { kind: 'speak'; text: string; replyTo?: number };

interface Toast { id: number; text: string; err?: boolean }

interface S {
  config: AppConfig | null;
  signedIn: boolean;      // past the sign-in screen (as a user or a guest)
  me: PublicUser | null;
  users: Record<string, PublicUser>;
  channels: Channel[];
  messages: Record<string, Message[]>;
  active: string;
  view: 'list' | 'chat';
  showMembers: boolean;
  lastRead: Record<string, number>;
  typing: Record<string, Record<string, number>>;
  connected: boolean;
  everConnected: boolean;
  toasts: Toast[];
  modal: ModalState;
  pcard: { userId: string; x: number; y: number } | null;
  replyTo: number | null;
  editing: number | null;
  theme: ThemePref;
  dark: boolean;
  pinsHidden: Record<string, boolean>;
}

const sysDark = () => matchMedia('(prefers-color-scheme: dark)').matches;
const savedTheme = (localStorage.getItem('tapaia-theme') as ThemePref) || 'system';

export const useS = create<S>(() => ({
  config: null, signedIn: false, me: null, users: {}, channels: [], messages: {}, active: 'general', view: 'list',
  showMembers: matchMedia('(min-width: 1280px)').matches, lastRead: {}, typing: {}, connected: false, everConnected: false,
  toasts: [], modal: null, pcard: null, replyTo: null, editing: null,
  theme: savedTheme, dark: savedTheme === 'dark' || (savedTheme === 'system' && sysDark()), pinsHidden: {},
}));
const set = useS.setState;
const get = useS.getState;

// ---------------------------------------------------------------- theme
function applyTheme() {
  const { theme } = get();
  const dark = theme === 'dark' || (theme === 'system' && sysDark());
  document.documentElement.dataset.theme = dark ? 'dark' : 'light';
  document.querySelector('meta[name="theme-color"]')?.setAttribute('content', dark ? '#17121d' : '#faf7f2');
  set({ dark });
}
export function setTheme(t: ThemePref) { localStorage.setItem('tapaia-theme', t); set({ theme: t }); applyTheme(); }
export const toggleTheme = () => setTheme(get().dark ? 'light' : 'dark');
matchMedia('(prefers-color-scheme: dark)').addEventListener('change', applyTheme);
applyTheme();

// ---------------------------------------------------------------- toasts
let tid = 1;
export function toast(text: string, err = false) {
  const id = tid++;
  set((s) => ({ toasts: [...s.toasts, { id, text, err }] }));
  setTimeout(() => set((s) => ({ toasts: s.toasts.filter((t) => t.id !== id) })), err ? 6000 : 3500);
}

// ---------------------------------------------------------------- unread tracking
const readKey = () => `tapaia-read-${get().me?.id ?? 'guest'}`;
function saveRead() { localStorage.setItem(readKey(), JSON.stringify(get().lastRead)); }
export function markRead(ch: string) {
  const ms = get().messages[ch];
  const last = ms?.[ms.length - 1]?.id ?? 0;
  if ((get().lastRead[ch] ?? 0) >= last) return;
  set((s) => ({ lastRead: { ...s.lastRead, [ch]: last } }));
  saveRead();
}

export function nameIn(u: PublicUser | undefined, ch: Channel | string | undefined): string {
  if (!u) return 'someone';
  const layer = typeof ch === 'string' ? (ch === 'square' ? 'ic' : 'ooc') : ch?.layer;
  return layer === 'ic' ? u.citizenName : u.handle;
}
export function mentionsMe(m: Message, me: PublicUser | null, ch?: Channel) {
  if (!me || m.userId === me.id || m.kind === 'system' || m.deleted) return false;
  const t = m.text.toLowerCase();
  return t.includes('@' + me.handle.toLowerCase()) || (ch?.layer === 'ic' && t.includes('@' + me.citizenName.toLowerCase()));
}
export function unreadFor(ch: Channel) {
  const s = get();
  const ms = s.messages[ch.id] ?? [];
  const lr = s.lastRead[ch.id] ?? 0;
  let n = 0, at = 0;
  for (let i = ms.length - 1; i >= 0 && ms[i].id > lr; i--) {
    const m = ms[i];
    if (m.userId === s.me?.id || m.kind === 'system') continue;
    n++;
    if (mentionsMe(m, s.me, ch)) at++;
  }
  return { n, at };
}

// ---------------------------------------------------------------- websocket
let ws: WebSocket | null = null;
let retry = 0;
let wantOpen = false;
export function wsSend(m: ClientMsg) { if (ws?.readyState === WebSocket.OPEN) ws.send(JSON.stringify(m)); }

export function connect() {
  wantOpen = true;
  ws?.close();
  const proto = location.protocol === 'https:' ? 'wss' : 'ws';
  const sock = new WebSocket(`${proto}://${location.host}/ws`);
  ws = sock;
  sock.onopen = () => { retry = 0; set({ connected: true, everConnected: true }); wsSend({ t: 'room', channel: get().view === 'chat' || matchMedia('(min-width: 768px)').matches ? get().active : null }); if (document.hidden) wsSend({ t: 'presence', state: 'idle' }); };
  sock.onmessage = (e) => onServer(JSON.parse(e.data));
  sock.onclose = () => {
    if (ws !== sock) return;
    set({ connected: false });
    if (wantOpen) setTimeout(connect, Math.min(8000, 500 * 2 ** retry++));
  };
}
export function disconnectWs() { wantOpen = false; ws?.close(); ws = null; }

document.addEventListener('visibilitychange', () => {
  wsSend({ t: 'presence', state: document.hidden ? 'idle' : 'here' });
  if (!document.hidden && get().view === 'chat') markRead(get().active);
});

function onServer(m: ServerMsg) {
  switch (m.t) {
    case 'hello': {
      const users: Record<string, PublicUser> = {};
      for (const u of m.users) users[u.id] = u;
      if (m.me) users[m.me.id] = m.me;
      const messages: Record<string, Message[]> = {};
      for (const msg of m.messages) (messages[msg.channel] ??= []).push(msg);
      const prevMe = get().me?.id;
      set({ me: m.me, users, channels: m.channels, messages });
      // unread state is per user; first visit starts "caught up" except one announcement
      if (prevMe !== (m.me?.id ?? undefined) || !Object.keys(get().lastRead).length) {
        const raw = localStorage.getItem(readKey());
        let lr: Record<string, number> = raw ? JSON.parse(raw) : {};
        if (!raw) {
          for (const c of m.channels) { const ms = messages[c.id]; if (ms?.length) lr[c.id] = ms[ms.length - 1].id; }
          const ann = messages['announcements'];
          if (ann && ann.length > 1) lr['announcements'] = ann[ann.length - 2].id;
        }
        set({ lastRead: lr }); saveRead();
      }
      const s = get();
      const readable = new Set(Object.keys(messages));
      if (!s.channels.some((c) => c.id === s.active) || (!readable.has(s.active) && s.active !== 'square')) {
        set({ active: m.me?.isCitizen ? 'general' : 'lobby' });
      }
      if (s.view === 'chat' && !document.hidden) markRead(get().active);
      return;
    }
    case 'msg': {
      set((s) => ({ messages: { ...s.messages, [m.m.channel]: [...(s.messages[m.m.channel] ?? []), m.m] } }));
      const s = get();
      if (m.m.userId) { const ty = s.typing[m.m.channel]; if (ty?.[m.m.userId]) { const n = { ...ty }; delete n[m.m.userId]; set({ typing: { ...s.typing, [m.m.channel]: n } }); } }
      const desktop = matchMedia('(min-width: 768px)').matches;
      if (m.m.channel === s.active && (desktop || s.view === 'chat') && !document.hidden) markRead(s.active);
      else if (m.m.userId === s.me?.id) markRead(m.m.channel);
      return;
    }
    case 'update':
      set((s) => ({ messages: { ...s.messages, [m.m.channel]: (s.messages[m.m.channel] ?? []).map((x) => (x.id === m.m.id ? m.m : x)) } }));
      return;
    case 'user':
      set((s) => ({ users: { ...s.users, [m.u.id]: m.u }, me: s.me?.id === m.u.id ? m.u : s.me }));
      return;
    case 'channel':
      set((s) => ({
        channels: s.channels.some((c) => c.id === m.c.id) ? s.channels : [...s.channels, m.c],
        messages: { ...s.messages, [m.c.id]: s.messages[m.c.id] ?? m.messages },
      }));
      if (m.open) openChannel(m.c.id);
      return;
    case 'typing': {
      const until = Date.now() + 4000;
      set((s) => ({ typing: { ...s.typing, [m.channel]: { ...(s.typing[m.channel] ?? {}), [m.userId]: until } } }));
      setTimeout(() => set((s) => ({ typing: { ...s.typing } })), 4100);
      return;
    }
    case 'error':
      toast(m.text, true);
      return;
  }
}

export function openChannel(id: string) {
  set({ active: id, view: 'chat', replyTo: null, editing: null, pcard: null });
  sessionStorage.setItem('tapaia-active', id);
  wsSend({ t: 'room', channel: id });
  markRead(id);
  if (!matchMedia('(min-width: 1280px)').matches) set({ showMembers: false });
}
export function backToList() {
  set({ view: 'list', showMembers: false });
  wsSend({ t: 'room', channel: null });
}

// ---------------------------------------------------------------- http helpers
export async function api<T = any>(path: string, body?: unknown, method = body === undefined ? 'GET' : 'POST'): Promise<T> {
  const r = await fetch(path, { method, headers: body !== undefined ? { 'content-type': 'application/json' } : {}, body: body !== undefined ? JSON.stringify(body) : undefined, credentials: 'same-origin' });
  const j = await r.json().catch(() => ({}));
  if (!r.ok) throw new Error(j.error || `Request failed (${r.status})`);
  return j as T;
}

export async function enterApp(me: PublicUser | null, opts: { arrival?: boolean; channel?: string } = {}) {
  set({ me, signedIn: true, lastRead: {}, active: opts.channel ?? (me?.isCitizen ? 'general' : 'lobby'), view: matchMedia('(min-width: 768px)').matches ? 'chat' : opts.channel ? 'chat' : 'list' });
  sessionStorage.setItem('tapaia-entered', '1');
  connect();
  if (opts.arrival) set({ modal: { kind: 'arrival' } });
}

export async function signOff() {
  await api('/api/logout', {}).catch(() => {});
  disconnectWs();
  sessionStorage.removeItem('tapaia-entered');
  set({ me: null, signedIn: false, modal: null, pcard: null, messages: {}, users: {}, channels: [] });
}

export async function refreshConfig() {
  const config = await api<AppConfig>('/api/config');
  set({ config });
  return config;
}
