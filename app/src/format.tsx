import type { ReactNode } from 'react';
import type { Channel, PublicUser } from '../shared/types';

const esc = (s: string) => s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');

/** Renders message text: links, @mentions, #channels, **bold**, *italic*, __underline__. No raw HTML. */
export function renderText(text: string, opts: { users: PublicUser[]; layer: Channel['layer']; channels: Channel[]; onUser: (id: string, e: React.MouseEvent) => void; onChannel: (id: string) => void }): ReactNode[] {
  const nameOf = (u: PublicUser) => (opts.layer === 'ic' ? [u.citizenName, u.handle] : [u.handle, u.citizenName]);
  const map = new Map<string, PublicUser>();
  for (const u of opts.users) for (const n of nameOf(u)) if (!map.has(n.toLowerCase())) map.set(n.toLowerCase(), u);
  const names = [...map.keys()].sort((a, b) => b.length - a.length).map(esc).join('|') || '(?!x)x';
  const chans = opts.channels.filter((c) => c.layer === 'ooc').map((c) => esc(c.id)).join('|') || '(?!x)x';
  const re = new RegExp(`(https?:\\/\\/[^\\s<]+[^\\s<.,:;"')\\]!?])|(@(?:${names}))(?![\\w])|(#(?:${chans}))(?![\\w-])|\\*\\*([^*\\n]+)\\*\\*|__([^_\\n]+)__|\\*([^*\\n]+)\\*`, 'gi');
  const out: ReactNode[] = [];
  let last = 0, k = 0;
  for (const m of text.matchAll(re)) {
    const i = m.index ?? 0;
    if (i > last) out.push(text.slice(last, i));
    if (m[1]) out.push(<a key={k++} href={m[1]} target="_blank" rel="noreferrer noopener">{m[1]}</a>);
    else if (m[2]) {
      const u = map.get(m[2].slice(1).toLowerCase());
      out.push(<span key={k++} className="at" role="button" onClick={(e) => u && opts.onUser(u.id, e)}>@{u ? (opts.layer === 'ic' ? u.citizenName : u.handle) : m[2].slice(1)}</span>);
    } else if (m[3]) out.push(<span key={k++} className="at" role="button" onClick={() => opts.onChannel(m[3].slice(1).toLowerCase())}>{m[3]}</span>);
    else if (m[4]) out.push(<b key={k++}>{m[4]}</b>);
    else if (m[5]) out.push(<u key={k++}>{m[5]}</u>);
    else if (m[6]) out.push(<i key={k++}>{m[6]}</i>);
    last = i + m[0].length;
  }
  if (last < text.length) out.push(text.slice(last));
  return out;
}

export const localTime = (ts: number) => new Date(ts).toLocaleTimeString([], { hour: 'numeric', minute: '2-digit' });
export function dayLabel(ts: number) {
  const d = new Date(ts), now = new Date();
  const y = new Date(now); y.setDate(now.getDate() - 1);
  if (d.toDateString() === now.toDateString()) return 'Today';
  if (d.toDateString() === y.toDateString()) return 'Yesterday';
  return d.toLocaleDateString([], { weekday: 'long', month: 'short', day: 'numeric' });
}
