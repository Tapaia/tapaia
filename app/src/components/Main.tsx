import { useEffect, useLayoutEffect, useMemo, useRef, useState, Fragment } from 'react';
import { I, Px, Av, Figure, BADGE_ICON, BADGE_LABEL, useTicks } from '../ui';
import { backToList, nameIn, mentionsMe, openChannel, toggleTheme, unreadFor, useS, wsSend } from '../store';
import { canPost, canRead, postBlockedReason } from '../../shared/perms';
import { fmtTicks, longhours, meldanTicks } from '../../shared/clock';
import type { Channel, Message, PublicUser } from '../../shared/types';
import { renderText, localTime, dayLabel } from '../format';
import { Composer } from './Composer';
import { dmOther } from './Sidebar';

const QUICK = ['👋', '❤️', '😂', '🍵', '🎉', '👀'];

export function openCard(userId: string, e: React.MouseEvent) {
  e.stopPropagation();
  const r = (e.currentTarget as HTMLElement).getBoundingClientRect();
  useS.setState({ pcard: { userId, x: r.right + 8, y: r.top } });
}

function Badges({ u }: { u?: PublicUser }) {
  if (!u) return null;
  return <>{u.badges.filter((b) => b !== 'mod').map((b) => b === 'team'
    ? <span key={b} className="tagteam">TEAM</span>
    : b === 'bot' ? <span key={b} className="tagteam" style={{ background: 'var(--sidebar-2)', color: 'var(--text-2)' }}>BOT</span>
    : <Px key={b} src={BADGE_ICON[b]} className="badge-ic" alt={BADGE_LABEL[b]} />)}
    {u.badges.includes('mod') && <span className="tagteam" style={{ background: 'var(--robe-100)', color: 'var(--robe-600)' }}>MOD</span>}</>;
}

export function Main({ mobile }: { mobile: boolean }) {
  const me = useS((s) => s.me);
  const active = useS((s) => s.active);
  const ch = useS((s) => s.channels.find((c) => c.id === s.active));
  const showMembers = useS((s) => s.showMembers);
  const dark = useS((s) => s.dark);
  const users = useS((s) => s.users);
  useS((s) => s.lastRead);
  useS((s) => s.messages);
  const pinsHidden = useS((s) => s.pinsHidden);
  const ticks = useTicks();
  if (!ch) return <main className="main" />;
  const readable = canRead(me, ch);
  const ic = ch.layer === 'ic';
  const other = ch.layer === 'dm' ? dmOther(ch, me?.id) : undefined;
  const present = Object.values(users).filter((u) => (ic ? u.isCitizen && u.room === 'square' : u.kind !== 'bot') && u.presence !== 'off');
  const totalUnread = useS.getState().channels.filter((c) => c.id !== ch.id && canRead(me, c)).reduce((a, c) => a + (unreadFor(c).n > 0 ? 1 : 0), 0);
  const stack = present.slice(0, 3);
  const title = ch.layer === 'dm' ? (other?.handle ?? 'Direct message') : ch.name;

  return (
    <main className="main" style={{ position: 'relative' }}>
      <div className="topbar">
        <div className="title">{ic ? <Px src="icon-tree" /> : ch.layer === 'dm' && other ? <Av u={other} size="s28" /> : <span className="hash">#</span>}{title}</div>
        <div className="topic">{ch.layer === 'dm' ? `Direct message with ${other?.handle}. Staff never DM first.` : ch.topic}</div>
        <div className="acts">
          {ch.layer !== 'dm' && <button className="stack" onClick={() => useS.setState({ showMembers: !showMembers })} aria-label="Members"><span className="avs">{stack.map((u) => <Av key={u.id} u={u} />)}</span>{present.length}</button>}
          <button className="iconbtn" onClick={() => useS.setState({ pinsHidden: { ...pinsHidden, [ch.id]: !pinsHidden[ch.id] } })} aria-label="Pinned" title="Pinned"><I n="pin" /></button>
          <button className="iconbtn" onClick={toggleTheme} aria-label="Toggle light or dark theme" title={dark ? 'Light theme' : 'Dark theme'} data-testid="theme-toggle"><I n={dark ? 'sun' : 'moon'} /></button>
          <button className={`iconbtn ${showMembers ? 'on' : ''}`} onClick={() => useS.setState({ showMembers: !showMembers })} aria-label="Toggle member list" data-testid="members-toggle"><I n="users" /></button>
          <button className="iconbtn" onClick={() => document.getElementById('search')?.focus()} aria-label="Search"><I n="search" /></button>
        </div>
      </div>
      <div className="mtop">
        <button className="back" onClick={backToList} aria-label="Back to rooms" data-testid="back"><I n="chev-l" c="lg" />{totalUnread > 0 && <span className="n">{totalUnread}</span>}</button>
        <div className="room">
          <span className={`tile ${ic ? '' : 'ooc'}`}>{ic ? <Px src="icon-tree" /> : ch.layer === 'dm' && other ? <Av u={other} size="s32" /> : '#'}</span>
          <div style={{ minWidth: 0 }}><div className="nm">{title}</div>
            <div className="st">{ic ? <><span className="g" />{present.length} here · in character</> : ch.layer === 'dm' ? 'Direct message' : <><span className="g" />{present.length} online</>}</div></div>
        </div>
        {ch.layer !== 'dm' && <button className="stack" onClick={() => useS.setState({ showMembers: true })} aria-label="Members"><span className="avs">{stack.map((u) => <Av key={u.id} u={u} />)}</span></button>}
        <button className="iconbtn" onClick={() => useS.setState({ showMembers: true })} aria-label="Members" data-testid="members-m"><I n="more" /></button>
      </div>
      {ic && readable && <>
        <div className="banner"><div className="over"><span className="pill glass"><Px src="icon-tree" />In character · Meldan</span>
          <h2>Tapaia Square</h2><p>Sit down, drink tea, the shops are nearby. Speak as your citizen.</p></div>
          <div className="clock" title={`Meldan time: ${fmtTicks(ticks)} ticks (shared clock, 00000 at midnight UTC)`} data-testid="clock"><span className="pixel">{fmtTicks(ticks)}</span><span>ticks · {longhours(ticks)} longhours</span></div></div>
        <div className="mbanner"><div className="over"><span className="pill glass" style={{ height: 20, fontSize: 11, padding: '0 8px' }}><Px src="icon-tree" style={{ width: 12, height: 12 }} />Meldan</span>
          <b>Tea cart’s open</b><span className="s">Speak as your citizen</span></div>
          <div className="clock"><span className="pixel">{fmtTicks(ticks)}</span>ticks</div></div>
      </>}
      {ch.pinned && readable && !pinsHidden[ch.id] && <div className="pinbar"><I n="pin" c="sm" /><span><b>Pinned:</b> <span dangerouslySetInnerHTML={{ __html: ch.pinned }} /></span>
        <button className="r" onClick={() => useS.setState({ pinsHidden: { ...pinsHidden, [ch.id]: true } })} aria-label="Hide pinned"><I n="x" c="sm" /></button></div>}
      {readable ? <Feed ch={ch} mobile={mobile} /> : <LockPanel ch={ch} />}
      {readable && <Typing ch={ch} />}
      {readable && (canPost(me, ch) ? <Composer ch={ch} mobile={mobile} /> : <Blocked ch={ch} />)}
      {!readable && !me && <Blocked ch={ch} />}
    </main>
  );
}

function LockPanel({ ch }: { ch: Channel }) {
  const me = useS((s) => s.me);
  return <div className="feed"><div className="lockpanel"><Px src="icon-lock" />
    <h3>{ch.layer === 'ic' ? 'Tapaia Square is for citizens' : `#${ch.name} is for citizens`}</h3>
    <p>{me ? 'Make your arrival post or claim a free Founding Citizen slot to read and post here.' : 'Sign in and become a citizen to read and post here.'}</p>
    {me ? <button className="btn primary" onClick={() => useS.setState({ modal: { kind: 'arrival' } })} data-testid="become-citizen"><Px src="icon-medal" />Become a citizen</button>
      : <button className="btn primary" onClick={() => useS.setState({ signedIn: false })}>Sign in</button>}
  </div></div>;
}

function Blocked({ ch }: { ch: Channel }) {
  const me = useS((s) => s.me);
  return <div className="blocked"><I n="lock" c="sm" /><span>{postBlockedReason(me, ch)}</span>
    {!me ? <button className="btn primary" onClick={() => useS.setState({ signedIn: false })}>Sign in</button>
      : !me.isCitizen && ch.id !== 'announcements' && ch.id !== 'feeds' && ch.id !== 'dev-updates' ? <button className="btn primary" onClick={() => useS.setState({ modal: { kind: 'arrival' } })}>Become a citizen</button> : null}</div>;
}

function Typing({ ch }: { ch: Channel }) {
  const t = useS((s) => s.typing[ch.id]);
  const users = useS((s) => s.users);
  const now = Date.now();
  const who = Object.entries(t ?? {}).filter(([, until]) => until > now).map(([id]) => nameIn(users[id], ch));
  return <div className="typing" aria-live="polite">{who.length > 0 && <><span className="dots"><i /><i /><i /></span><b style={{ fontWeight: 600, color: 'var(--text-2)' }}>{who.slice(0, 2).join(', ')}</b> {who.length > 1 ? 'are' : 'is'} typing…</>}</div>;
}

function Feed({ ch, mobile }: { ch: Channel; mobile: boolean }) {
  const msgs = useS((s) => s.messages[ch.id]) ?? [];
  const me = useS((s) => s.me);
  const users = useS((s) => s.users);
  const channels = useS((s) => s.channels);
  const ref = useRef<HTMLDivElement>(null);
  const stick = useRef(true);
  const [newBelow, setNewBelow] = useState(false);
  const userList = useMemo(() => Object.values(users), [users]);
  const byId = useMemo(() => new Map(msgs.map((m) => [m.id, m])), [msgs]);

  useLayoutEffect(() => { const el = ref.current; if (el) { el.scrollTop = el.scrollHeight; stick.current = true; } }, [ch.id]);
  useLayoutEffect(() => {
    const el = ref.current; if (!el) return;
    const last = msgs[msgs.length - 1];
    if (stick.current || last?.userId === me?.id) { el.scrollTop = el.scrollHeight; setNewBelow(false); }
    else setNewBelow(true);
  }, [msgs.length]);
  useEffect(() => {
    const el = ref.current; if (!el) return;
    const ro = new ResizeObserver(() => { if (stick.current) el.scrollTop = el.scrollHeight; });
    ro.observe(el); if (el.firstElementChild) ro.observe(el.firstElementChild);
    return () => ro.disconnect();
  }, [ch.id]);
  const onScroll = () => { const el = ref.current!; stick.current = el.scrollHeight - el.scrollTop - el.clientHeight < 60; if (stick.current) setNewBelow(false); };

  const ctx = { users: userList, layer: ch.layer, channels, onUser: openCard, onChannel: (id: string) => channels.some((c) => c.id === id) && openChannel(id) };
  const out: JSX.Element[] = [];
  let prev: Message | undefined;
  for (const m of msgs) {
    if (ch.layer !== 'ic' && (!prev || new Date(prev.ts).toDateString() !== new Date(m.ts).toDateString())) out.push(<div key={`d${m.id}`} className="daysep">{dayLabel(m.ts)}</div>);
    const cont = !!prev && prev.kind === 'text' && m.kind === 'text' && prev.userId === m.userId && !m.replyTo && m.ts - prev.ts < 5 * 60_000 && !prev.deleted;
    out.push(<Item key={m.id} m={m} ch={ch} cont={cont} reply={m.replyTo ? byId.get(m.replyTo) : undefined} ctx={ctx} mobile={mobile} />);
    prev = m;
  }
  return <>
    <div className="feed" ref={ref} onScroll={onScroll} data-testid="feed"><div className="feed-inner">
      {msgs.length === 0 && <div className="sysline">{ch.layer === 'dm' ? 'This is the start of your conversation. Be kind.' : 'No messages yet.'}</div>}
      {out}
    </div></div>
    {newBelow && <button className="newmsgs" onClick={() => { const el = ref.current!; el.scrollTop = el.scrollHeight; }}>New messages ↓</button>}
  </>;
}

type Ctx = Parameters<typeof renderText>[1];

function Toolbar({ m, ch }: { m: Message; ch: Channel }) {
  const me = useS((s) => s.me);
  if (!me || m.deleted) return null;
  const mine = m.userId === me.id;
  const mod = me.badges.includes('mod') || me.badges.includes('team');
  const posting = canPost(me, ch);
  return <div className="toolbar">
    {QUICK.slice(0, 4).map((e) => <button key={e} onClick={() => wsSend({ t: 'react', id: m.id, emoji: e })} aria-label={`React ${e}`}>{e}</button>)}
    {posting && <button onClick={() => { useS.setState({ replyTo: m.id }); document.getElementById('composer-input')?.focus(); }} aria-label="Reply" title="Reply"><I n="reply" c="sm" /></button>}
    {mine && m.kind === 'text' && <button onClick={() => useS.setState({ editing: m.id })} aria-label="Edit" title="Edit"><I n="edit" c="sm" /></button>}
    {(mine || mod) && m.kind !== 'system' && <button onClick={() => { if (confirm('Delete this message?')) wsSend({ t: 'delete', id: m.id }); }} aria-label="Delete" title="Delete"><I n="trash" c="sm" /></button>}
  </div>;
}

function Reactions({ m }: { m: Message }) {
  const me = useS((s) => s.me);
  const entries = Object.entries(m.reactions);
  if (!entries.length) return null;
  return <div className="reactions">{entries.map(([e, ids]) => (
    <button key={e} className={`react ${me && ids.includes(me.id) ? 'mine' : ''}`} onClick={() => me && wsSend({ t: 'react', id: m.id, emoji: e })} title={`${ids.length} reacted`}>{e} {ids.length}</button>
  ))}</div>;
}

function jump(id: number) {
  const el = document.getElementById(`m${id}`);
  if (!el) return;
  el.scrollIntoView({ block: 'center', behavior: 'smooth' });
  el.classList.remove('flash'); void el.offsetWidth; el.classList.add('flash');
}

function Item({ m, ch, cont, reply, ctx, mobile }: { m: Message; ch: Channel; cont: boolean; reply?: Message; ctx: Ctx; mobile: boolean }) {
  const users = useS((s) => s.users);
  const me = useS((s) => s.me);
  const editing = useS((s) => s.editing === m.id);
  const u = users[m.userId ?? ''];
  const ic = ch.layer === 'ic';
  const name = nameIn(u, ch);
  const time = ic ? fmtTicks(meldanTicks(m.ts)) : localTime(m.ts);
  const timeTitle = ic ? `${localTime(m.ts)} your time` : new Date(m.ts).toLocaleString();

  if (m.kind === 'system') {
    if (m.sys === 'citizen') return <div className="sysline" id={`m${m.id}`}>👋 <b role="button" onClick={(e) => u && openCard(u.id, e)}>{name}</b> {m.text}</div>;
    return <div className="sysline" id={`m${m.id}`}><Px src="icon-door" /><b role="button" onClick={(e) => u && openCard(u.id, e)}>{name}</b> {m.text}</div>;
  }
  if (m.kind === 'arrival' && u) {
    const waved = !!me && (m.reactions['👋'] ?? []).includes(me.id);
    const waveCount = (m.reactions['👋'] ?? []).length;
    const founder = u.entry === 'founder';
    return <div className="card-wrap" id={`m${m.id}`}><div className="card-arrival">
      <div className="fig"><Figure cfg={u.avatar} w={mobile ? 32 : 48} /></div>
      <div style={{ minWidth: 0 }}><div className="k"><Px src={founder ? 'icon-medal' : 'icon-flame'} className="badge-ic" />New arrival · {founder ? 'Founding Citizen' : 'Arrival post'}{m.simulated && <span className="pill demo sample">demo · nothing burned</span>}</div>
        <div className="q"><b role="button" onClick={(e) => openCard(u.id, e)} style={{ cursor: 'pointer' }}>{u.citizenName}</b> “{m.text}”</div></div>
      <div className="wave">
        <button className={`btn-soft ${waved ? 'mine' : ''}`} disabled={!me} onClick={() => wsSend({ t: 'react', id: m.id, emoji: '👋' })} data-testid="wave">👋 Wave hello{waveCount > 0 && ` · ${waveCount}`}</button>
        <span className="time" style={{ fontSize: 12, color: 'var(--text-3)' }} title={timeTitle}>{time}</span></div>
    </div><Toolbar m={m} ch={ch} /></div>;
  }
  const replyEl = reply && <div className="replyline" onClick={() => jump(reply.id)}><span className="bar" />{users[reply.userId ?? ''] && <Av u={users[reply.userId!]} />}<b>{nameIn(users[reply.userId ?? ''], ch)}</b><span className="snip">{reply.deleted ? 'deleted message' : reply.text}</span></div>;
  if (m.kind === 'speak' && u) {
    return <>{replyEl}<div className="card-wrap" id={`m${m.id}`}><div className="card-speak">
      <div className="h"><Px src="icon-flame" />Spoke to the Square · burned <span className="ph" style={{ textTransform: 'none' }}>S</span> ZC
        <span className="v demo" title="Prototype: Speak is simulated, nothing was burned">{m.simulated ? <>demo · nothing burned</> : <><I n="check" c="sm" />Verified on-chain</>}</span></div>
      <div className="b"><Av u={u} onClick={(e) => openCard(u.id, e)} /><div style={{ minWidth: 0 }}><div className="meta"><span className="who" role="button" onClick={(e) => openCard(u.id, e)}>{u.citizenName}</span><span className="time" title={timeTitle}>{time}</span></div>
        <div className="text">{m.deleted ? <span className="deleted">message deleted</span> : renderText(m.text, ctx)}</div><Reactions m={m} /></div></div>
    </div><Toolbar m={m} ch={ch} /></div></>;
  }
  const mention = mentionsMe(m, me, ch);
  const body = m.deleted ? <div className="text deleted">message deleted</div>
    : editing ? <EditBox m={m} /> : <div className="text">{renderText(m.text, ctx)}{m.edited && <span className="edited">(edited)</span>}</div>;
  const card = m.card && !m.deleted && <a className="linkcard" href={`https://${m.card.url}`} target="_blank" rel="noreferrer"><span className="thumb"><img src="/brand/logo.svg" alt="" style={{ width: 40, height: 40 }} /></span><div><div className="u">{m.card.url}</div><div className="t">{m.card.title}</div><div className="d">{m.card.desc}</div></div></a>;
  if (cont) return <div className={`msg cont ${mention ? 'mention' : ''}`} id={`m${m.id}`}><span className="time-h">{ic ? '' : localTime(m.ts).replace(/\s?[AP]M/, '')}</span><span className="spacer" /><div className="content">{body}{card}<Reactions m={m} /></div><Toolbar m={m} ch={ch} /></div>;
  return <>{replyEl}<div className={`msg ${mention ? 'mention' : ''}`} id={`m${m.id}`}>
    {u ? <Av u={u} onClick={(e) => openCard(u.id, e)} /> : <span className="av c6" />}
    <div className="content"><div className="meta"><span className="who" role="button" onClick={(e) => u && openCard(u.id, e)}>{name}</span><Badges u={u} />{m.sample && <span className="pill sample">SAMPLE DATA</span>}<span className="time" title={timeTitle}>{time}</span></div>
      {body}{card}<Reactions m={m} /></div>
    <Toolbar m={m} ch={ch} /></div></>;
}

function EditBox({ m }: { m: Message }) {
  const [t, setT] = useState(m.text);
  const done = () => useS.setState({ editing: null });
  return <div><textarea className="ta" style={{ minHeight: 60, fontSize: 15 }} value={t} autoFocus onChange={(e) => setT(e.target.value)}
    onKeyDown={(e) => { if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); if (t.trim()) wsSend({ t: 'edit', id: m.id, text: t }); done(); } if (e.key === 'Escape') done(); }} />
    <div className="small">Enter to save · Esc to cancel</div></div>;
}

export { Fragment };
