import { useState } from 'react';
import { I, Px, Av } from '../ui';
import { openChannel, toggleTheme, unreadFor, useS } from '../store';
import { canRead } from '../../shared/perms';
import type { Channel } from '../../shared/types';
import { Legal } from './Legal';

export const COMMUNITY = ['announcements', 'general', 'market', 'support', 'dev-updates', 'feeds', 'lobby'];

export function dmOther(ch: Channel, meId?: string) {
  const s = useS.getState();
  return s.users[ch.members?.find((id) => id !== meId) ?? ''];
}

export function Sidebar() {
  const me = useS((s) => s.me);
  const channels = useS((s) => s.channels);
  const active = useS((s) => s.active);
  const users = useS((s) => s.users);
  const dark = useS((s) => s.dark);
  useS((s) => s.messages); useS((s) => s.lastRead); // re-render on unread changes
  const [q, setQ] = useState('');
  const match = (name: string) => !q || name.toLowerCase().includes(q.toLowerCase());
  const inSquare = Object.values(users).filter((u) => u.isCitizen && u.presence !== 'off' && u.room === 'square').length;

  const row = (ch: Channel) => {
    const readable = canRead(me, ch);
    const { n, at } = readable ? unreadFor(ch) : { n: 0, at: 0 };
    const cls = ch.id === active ? 'on' : !readable ? 'locked' : n ? 'unread' : '';
    return (
      <button key={ch.id} className={`ch ${cls}`} onClick={() => openChannel(ch.id)} data-testid={`ch-${ch.id}`} aria-current={ch.id === active}>
        <span className="hash">#</span><span className="nmx">{ch.name}</span>
        {!readable ? <span className="lock"><I n="lock" c="sm" /></span> : ch.id !== active && (at > 0 ? <span className="mention" title="You were mentioned">@</span> : n > 0 && (ch.id === 'announcements' || ch.id === 'dev-updates') ? <span className="badge">{n > 99 ? '99+' : n}</span> : null)}
      </button>
    );
  };
  const sq = channels.find((c) => c.id === 'square');
  const dms = channels.filter((c) => c.layer === 'dm');
  return (
    <aside className="side">
      <div className="ws"><img className="logo" src="/brand/logo.svg" alt="Tapaia" />
        <div><div className="name">Tapaia</div><div className="sub">$ZC community</div></div>
        <button className="chev iconbtn" onClick={toggleTheme} aria-label="Toggle light or dark theme" title="Light / dark" data-testid="theme-toggle-side"><I n={dark ? 'sun' : 'moon'} c="sm" /></button></div>
      <label className="search"><I n="search" c="sm" /><input id="search" placeholder="Search Tapaia" value={q} onChange={(e) => setQ(e.target.value)} /><kbd>⌘K</kbd></label>
      <nav className="nav">
        <div className="sec-h">COMMUNITY</div>
        {COMMUNITY.map((id) => channels.find((c) => c.id === id)).filter((c): c is Channel => !!c && match(c.name)).map(row)}
        <div className="sec-h">VERIDIA <span className="tag ic">in character</span></div>
        {sq && match(sq.name) && (() => {
          const readable = canRead(me, sq); const { n, at } = readable ? unreadFor(sq) : { n: 0, at: 0 };
          return <button className={`ch ${active === 'square' ? 'on' : !readable ? 'locked' : n ? 'unread' : ''}`} onClick={() => openChannel('square')} data-testid="ch-square">
            <Px src="icon-tree" />Tapaia Square
            {!readable ? <span className="lock"><I n="lock" c="sm" /></span> : at > 0 && active !== 'square' ? <span className="mention">@</span> : <span className="count">{inSquare} here</span>}
          </button>;
        })()}
        <div className="ch muted" aria-disabled><Px src="icon-lock" style={{ opacity: 0.55 }} />More of Meldan<span className="lock">soon</span></div>
        {me && <div className="sec-h">DIRECT MESSAGES</div>}
        {dms.map((ch) => {
          const o = dmOther(ch, me?.id); if (!o || !match(o.handle)) return null;
          const { n } = unreadFor(ch);
          return <button key={ch.id} className={`ch ${ch.id === active ? 'on' : n ? 'unread' : ''}`} onClick={() => openChannel(ch.id)}><Av u={o} size="s28" /><span className="nmx">{o.handle}</span>{n > 0 && ch.id !== active && <span className="badge">{n}</span>}</button>;
        })}
        {me && !dms.length && <div className="small" style={{ padding: '2px 10px 8px' }}>Click someone’s name to message them.</div>}
      </nav>
      {me ? (
        <div className="me" onClick={() => useS.setState({ modal: { kind: 'profile' } })} data-testid="me-card" role="button" tabIndex={0}>
          <Av u={me} dot />
          <div style={{ minWidth: 0 }}><div className="nm">{active === 'square' ? me.citizenName : me.handle}</div><div className="st">{!me.isCitizen ? 'Not a citizen yet' : active === 'square' ? 'In Tapaia Square' : 'Online'}</div></div>
          <div className="icons">
            <button onClick={(e) => { e.stopPropagation(); toggleTheme(); }} aria-label="Toggle theme" data-testid="theme-toggle-me"><I n={dark ? 'sun' : 'moon'} c="sm" /></button>
            <button aria-label="Profile and settings"><I n="sliders" c="sm" /></button>
          </div>
        </div>
      ) : (
        <div className="me" onClick={() => useS.setState({ signedIn: false })} role="button"><span className="av c6"><Px src="icon-door" style={{ width: 24, height: 24, marginBottom: 8 }} /></span><div><div className="nm">Just looking</div><div className="st">Sign in to chat</div></div><div className="icons"><button aria-label="Sign in"><I n="chev-r" c="sm" /></button></div></div>
      )}
      <Legal short />
    </aside>
  );
}
