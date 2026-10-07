import { useEffect, useState, type ReactNode } from 'react';
import { avatarPixels, type AvatarCfg } from '../shared/avatar';
import type { PublicUser } from '../shared/types';
import { meldanTicks } from '../shared/clock';

// SVG line icons, same paths as design/mockups-v2/build.py
const ICONS: Record<string, string> = {
  search: '<circle cx="11" cy="11" r="6.5"/><path d="M16 16l4 4"/>',
  bell: '<path d="M6.5 16.5V11a5.5 5.5 0 0 1 11 0v5.5l1.5 1.5H5z"/><path d="M10 20.5h4"/>',
  users: '<circle cx="9" cy="8.5" r="3.5"/><path d="M2.5 19.5c.8-3.4 3.3-5 6.5-5s5.7 1.6 6.5 5"/><path d="M16 5.5a3.2 3.2 0 0 1 0 6.2M18 14.8c1.9.6 3.1 2.2 3.5 4.7"/>',
  pin: '<path d="M9 3.5h6l-1 5 3 3.5H7l3-3.5z"/><path d="M12 12v8.5"/>',
  plus: '<path d="M12 5v14M5 12h14"/>',
  send: '<path d="M4.5 11.8L19.5 4.5l-4.3 15-3.4-6.3z"/><path d="M11.8 13.2l7.7-8.7"/>',
  smile: '<circle cx="12" cy="12" r="8.5"/><path d="M8.5 14c.9 1.3 2.1 2 3.5 2s2.6-.7 3.5-2"/><path d="M9 9.5h.01M15 9.5h.01"/>',
  'chev-d': '<path d="M7 10l5 5 5-5"/>',
  'chev-l': '<path d="M14.5 6l-6 6 6 6"/>',
  'chev-r': '<path d="M9.5 6l6 6-6 6"/>',
  sliders: '<path d="M4 7h9M17 7h3M4 17h3M11 17h9"/><circle cx="15" cy="7" r="2"/><circle cx="9" cy="17" r="2"/>',
  more: '<circle cx="5.5" cy="12" r="1"/><circle cx="12" cy="12" r="1"/><circle cx="18.5" cy="12" r="1"/>',
  image: '<rect x="3.5" y="5" width="17" height="14" rx="3"/><circle cx="9" cy="10" r="1.6"/><path d="M5 18l5-5 3 3 2.5-2.5L20 18"/>',
  check: '<path d="M5 12.5l4.5 4.5L19 7.5"/>',
  x: '<path d="M6 6l12 12M18 6L6 18"/>',
  ext: '<path d="M13.5 5.5H18.5V10.5"/><path d="M18.5 5.5l-8 8"/><path d="M17 14v4.5a1 1 0 0 1-1 1H6.5a1 1 0 0 1-1-1V8a1 1 0 0 1 1-1H11"/>',
  info: '<circle cx="12" cy="12" r="8.5"/><path d="M12 11v5.5M12 7.8h.01"/>',
  shield: '<path d="M12 3.5l7 3v5c0 4.4-3 7.7-7 9-4-1.3-7-4.6-7-9v-5z"/><path d="M9 12l2.2 2.2L15.5 10"/>',
  lock: '<rect x="5" y="10.5" width="14" height="10" rx="2.5"/><path d="M8.5 10.5V8a3.5 3.5 0 0 1 7 0v2.5"/>',
  chat: '<path d="M4.5 6.5a2 2 0 0 1 2-2h11a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2H10l-4.5 3.5V16.5h1a2 2 0 0 1-2-2z"/>',
  user: '<circle cx="12" cy="8.5" r="3.8"/><path d="M4.5 20c1-3.8 3.9-5.8 7.5-5.8s6.5 2 7.5 5.8"/>',
  thread: '<path d="M6 5v8a3 3 0 0 0 3 3h9"/><path d="M15 13l3 3-3 3"/>',
  shuffle: '<path d="M4 7h3.5c4 0 5 10 9 10H20M17 14l3 3-3 3M4 17h3.5M16.5 7H20M17 4l3 3-3 3"/>',
  sparkle: '<path d="M12 4l1.8 5.2L19 11l-5.2 1.8L12 18l-1.8-5.2L5 11l5.2-1.8z"/>',
  wallet: '<rect x="3.5" y="6" width="17" height="13" rx="3"/><path d="M16 12.5h4.5M3.5 9h13"/>',
  qr: '<rect x="4" y="4" width="6" height="6" rx="1"/><rect x="14" y="4" width="6" height="6" rx="1"/><rect x="4" y="14" width="6" height="6" rx="1"/><path d="M14 14h2v2h-2zM18 18h2v2h-2zM14 18h2M18 14h2"/>',
  edit: '<path d="M5 19l1-4L15.5 5.5l3 3L9 18z"/>',
  moon: '<path d="M19 14.5A7.5 7.5 0 0 1 9.5 5a7.5 7.5 0 1 0 9.5 9.5z"/>',
  sun: '<circle cx="12" cy="12" r="4"/><path d="M12 3v2M12 19v2M3 12h2M19 12h2M5.6 5.6l1.4 1.4M17 17l1.4 1.4M5.6 18.4L7 17M17 7l1.4-1.4"/>',
  reply: '<path d="M10 7L5 12l5 5"/><path d="M5.5 12H14a5 5 0 0 1 5 5v1"/>',
  trash: '<path d="M5 7h14M10 7V5h4v2M7 7l1 12h8l1-12"/>',
  logout: '<path d="M14 5h4a1 1 0 0 1 1 1v12a1 1 0 0 1-1 1h-4"/><path d="M10 8l-4 4 4 4M6 12h9"/>',
};

export function I({ n, c = '' }: { n: string; c?: string }) {
  return <svg className={`i ${c}`} viewBox="0 0 24 24" dangerouslySetInnerHTML={{ __html: ICONS[n] ?? '' }} />;
}

export const Px = ({ src, alt = '', className = '', style }: { src: string; alt?: string; className?: string; style?: React.CSSProperties }) =>
  <img className={`px ${className}`} src={`/assets/${src}.png`} alt={alt} style={style} draggable={false} />;

// ---- pixel avatars, drawn from the sprite maps in shared/avatar.ts
const cache = new Map<string, string>();
export function avatarUrl(cfg: AvatarCfg, bust = false): string {
  const key = JSON.stringify(cfg) + bust;
  const hit = cache.get(key);
  if (hit) return hit;
  const px = avatarPixels(cfg);
  const h = bust ? 16 : px.length;
  const cv = document.createElement('canvas');
  cv.width = 16; cv.height = h;
  const ctx = cv.getContext('2d')!;
  for (let y = 0; y < h; y++) for (let x = 0; x < 16; x++) { const c = px[y][x]; if (c) { ctx.fillStyle = c; ctx.fillRect(x, y, 1, 1); } }
  const url = cv.toDataURL('image/png');
  cache.set(key, url);
  return url;
}

export function Av({ u, size = '', dot, onClick }: { u: Pick<PublicUser, 'avatar' | 'tile'> & Partial<PublicUser>; size?: string; dot?: boolean; onClick?: (e: React.MouseEvent) => void }) {
  const tile = <span className={`av ${size} ${u.tile}`} onClick={onClick}><img src={avatarUrl(u.avatar, true)} alt="" draggable={false} /></span>;
  if (!dot) return tile;
  const p = u.presence === 'idle' ? 'idle' : u.presence === 'off' ? 'off' : '';
  return <span className="av-wrap">{tile}<span className={`dot ${p}`} /></span>;
}

export const Figure = ({ cfg, w, className = '', alt = '' }: { cfg: AvatarCfg; w: number; className?: string; alt?: string }) =>
  <img className={`px ${className}`} src={avatarUrl(cfg)} style={{ width: w, height: 'auto' }} alt={alt} draggable={false} />;

export const BADGE_ICON: Record<string, string> = { founder: 'icon-medal', onchain: 'icon-flame', team: 'icon-shield', bot: 'icon-robot', mod: 'icon-star' };
export const BADGE_LABEL: Record<string, string> = { founder: 'Founding Citizen', onchain: 'Arrival post', team: 'Verified team', bot: 'Bot', mod: 'Moderator' };

export function useTicks() {
  const [t, setT] = useState(meldanTicks());
  useEffect(() => { const id = setInterval(() => setT(meldanTicks()), 432); return () => clearInterval(id); }, []);
  return t;
}

export function useMedia(q: string) {
  const [m, setM] = useState(() => matchMedia(q).matches);
  useEffect(() => { const mq = matchMedia(q); const f = () => setM(mq.matches); mq.addEventListener('change', f); return () => mq.removeEventListener('change', f); }, [q]);
  return m;
}

export function Modal({ children, onClose, size = '', label }: { children: ReactNode; onClose?: () => void; size?: string; label: string }) {
  useEffect(() => {
    const k = (e: KeyboardEvent) => { if (e.key === 'Escape' && onClose) onClose(); };
    addEventListener('keydown', k); return () => removeEventListener('keydown', k);
  }, [onClose]);
  return <>
    <div className="dim" onClick={onClose} />
    <div className={`modal ${size}`} role="dialog" aria-modal="true" aria-label={label}>{children}</div>
  </>;
}

export function Chk({ on, set, children }: { on: boolean; set: (v: boolean) => void; children: ReactNode }) {
  return <label className="chk" onClick={(e) => { e.preventDefault(); set(!on); }} role="checkbox" aria-checked={on} tabIndex={0}
    onKeyDown={(e) => { if (e.key === ' ' || e.key === 'Enter') { e.preventDefault(); set(!on); } }}>
    <span className={`b ${on ? 'on' : ''}`}>{on && <I n="check" c="sm" />}</span>{children}</label>;
}
