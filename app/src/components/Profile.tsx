import { useEffect, useState } from 'react';
import { I, Px, Av, Figure, Modal, BADGE_ICON, BADGE_LABEL, useTicks, avatarUrl } from '../ui';
import { api, setTheme, signOff, toast, useS, wsSend, type ThemePref } from '../store';
import { HAIRS, SKINS, SHIRTS, randomAvatar, type AvatarCfg, type Outfit } from '../../shared/avatar';
import { fmtTicks, meldanTicks } from '../../shared/clock';
import type { PublicUser } from '../../shared/types';
import { useConfig } from 'wagmi';
import { walletDisconnect } from '../wallet';

function Chips({ u }: { u: PublicUser }) {
  return <>
    {u.entry === 'founder' && <span className="pill gold"><Px src="icon-medal" />Founding Citizen</span>}
    {u.entry === 'burn' && <span className="pill ember"><Px src="icon-flame" />Citizen · arrival post{u.kind === 'demo' || u.kind === 'wallet' ? ' (demo)' : ''}</span>}
    {u.isCitizen && !u.entry && <span className="pill ic">Citizen · demo</span>}
    {!u.isCitizen && u.kind !== 'bot' && <span className="pill neutral">Not a citizen yet</span>}
    {u.badges.filter((b) => b === 'team' || b === 'mod' || b === 'bot').map((b) => <span key={b} className={`pill ${b === 'team' ? 'ok' : 'neutral'}`}><Px src={BADGE_ICON[b]} />{BADGE_LABEL[b]}</span>)}
    {u.wallet && <span className="pill ok"><I n="check" c="sm" />{u.wallet}</span>}
    {u.kind === 'demo' && <span className="pill neutral">demo account</span>}
  </>;
}

export function ProfileCard() {
  const pc = useS((s) => s.pcard);
  const u = useS((s) => (s.pcard ? s.users[s.pcard.userId] : undefined));
  const me = useS((s) => s.me);
  const active = useS((s) => s.active);
  if (!pc || !u) return null;
  const close = () => useS.setState({ pcard: null });
  const ic = active === 'square';
  const x = Math.min(pc.x, innerWidth - 336), y = Math.min(Math.max(8, pc.y - 40), innerHeight - 440);
  const isMe = u.id === me?.id;
  const since = u.arrivalAt ?? u.createdAt;
  return <>
    <div className="pcard-dim" onClick={close} />
    <div className="pcard" style={{ left: x, top: y }} data-testid="profile-card">
      <div className="scene"><Figure cfg={u.avatar} w={48} /><span className="tr pill dark pixel" style={{ fontSize: 8 }}>{fmtTicks(meldanTicks(since))}</span></div>
      <div className="body">
        <h3>{ic || !u.linked ? (ic ? u.citizenName : u.handle) : u.handle}</h3>
        <div className="h">{u.linked || isMe ? (ic ? `@${u.handle} in community channels` : `${u.citizenName} in Tapaia Square`) : ic ? 'Citizen of Meldan' : 'Community member'}</div>
        <div className="chips"><Chips u={u} /></div>
        <div className="row">Citizen since <b>{new Date(since).toLocaleDateString([], { month: 'short', day: 'numeric', year: 'numeric' })}</b></div>
        {u.district && <div className="row">Home district <b>{u.district}</b></div>}
        {u.about && <div className="row">{u.about}</div>}
        {u.arrivalText && <div className="quote"><span className="small">Arrival post</span><br />“{u.arrivalText}”</div>}
        {isMe ? <div className="acts"><button className="btn primary sm" onClick={() => useS.setState({ pcard: null, modal: { kind: 'profile' } })}>Edit your citizen</button></div>
          : <div className="acts">
            <button className="btn primary sm" disabled={!me || u.kind === 'bot'} onClick={() => { if (!me?.isCitizen) return toast('Become a citizen to send direct messages.', true); wsSend({ t: 'dm', userId: u.id }); close(); }} data-testid="dm-btn"><I n="chat" c="sm" />Message</button>
            <button className="btn ghost sm" onClick={() => toast('Mute is stubbed in the prototype.')}>Mute</button>
            <button className="btn ghost sm" onClick={() => toast('Block is stubbed in the prototype.')}>Block</button>
            <button className="btn ghost sm" onClick={() => api('/api/report', { userId: u.id }).then(() => toast('Report sent (stubbed in the prototype).')).catch(() => toast('Sign in to report.', true))}>Report</button>
            <button className="btn ghost sm" disabled title="Knocks arrive with the RPG">Knock</button>
          </div>}
        {u.kind === 'seed' && <div className="note">Fictional demo citizen. Their messages and replies are simulated.</div>}
        {u.kind === 'bot' && <div className="note">Read-only bot. Can’t be messaged and holds no funded wallet.</div>}
      </div>
    </div>
  </>;
}

const OUTFITS: [Outfit, string][] = [['robe', 'Robe'], ['hood', 'Robe + hood'], ['plain', 'Plain shirt'], ['slogan', 'Slogan shirt']];

export function ProfileEditor() {
  const me = useS((s) => s.me)!;
  const theme = useS((s) => s.theme);
  const wagmi = useConfig();
  const close = () => useS.setState({ modal: null });
  const [av, setAv] = useState<AvatarCfg>(me.avatar);
  const [hist, setHist] = useState<AvatarCfg[]>([]);
  const [name, setName] = useState(me.citizenName);
  const [handle, setHandle] = useState(me.handle);
  const [linked, setLinked] = useState(me.linked);
  const [busy, setBusy] = useState(false);
  const ticks = useTicks();
  useEffect(() => { avatarUrl(av); }, [av]);
  const upd = (p: Partial<AvatarCfg>) => { setHist((h) => [...h.slice(-20), av]); setAv({ ...av, ...p }); };
  const shirt = av.outfit === 'plain' || av.outfit === 'slogan';
  const days = Math.max(1, Math.ceil((Date.now() - (me.arrivalAt ?? me.createdAt)) / 86_400_000));
  async function save() {
    setBusy(true);
    try {
      const { me: m } = await api<{ me: PublicUser }>('/api/profile', { citizenName: name, handle, avatar: av, linked }, 'PATCH');
      useS.setState({ me: m }); toast('Citizen saved.'); close();
    } catch (e) { toast((e as Error).message, true); } finally { setBusy(false); }
  }
  const sw = (cols: [string, string][], sel: string, on: (k: string) => void, label: string) =>
    <span className="sws" role="radiogroup" aria-label={label}>{cols.map(([k, c]) => <button key={k} className={`sw ${sel === k ? 'sel' : ''}`} style={{ background: c }} onClick={() => on(k)} aria-label={`${label} ${k}`} aria-checked={sel === k} role="radio" />)}</span>;
  return (
    <Modal onClose={close} size="md" label="Your citizen">
      <div className="mh"><span className="medal" style={{ background: 'var(--robe-100)' }}><Px src="icon-tree" /></span>
        <div><h2>Your citizen</h2><p>Your look in Tapaia Square and how you appear in community channels.</p></div>
        <button className="iconbtn x" onClick={close} aria-label="Close" data-testid="profile-close"><I n="x" /></button></div>
      <div className="prof-body">
        <div className="prof-grid">
          <div>
            <div className="phero"><span className="pill glass tl"><Px src="icon-tree" />Tapaia Square</span><span className="tr pixel">{fmtTicks(ticks)}</span>
              <span className="shadow" /><Figure cfg={av} w={80} className="ava" alt="Avatar preview" /></div>
            <div className="pname">
              <input className="name-in" value={name} onChange={(e) => setName(e.target.value)} maxLength={32} aria-label="Citizen name" />
              <div className="h">Posts as <b>@</b><input className="handle-in" style={{ width: `${Math.max(3, handle.length) * 0.6 + 0.9}em` }} value={handle} onChange={(e) => setHandle(e.target.value.toLowerCase().replace(/[^a-z0-9_]/g, ''))} maxLength={20} aria-label="Handle" /> in community channels</div>
              <div className="chips"><Chips u={me} /></div>
            </div>
            <div className="stats"><div><div className="v">{me.speaks}</div><div className="k">Speaks</div></div>
              <div><div className="v">Day {days}</div><div className="k">{me.isCitizen ? 'Arrived' : 'Joined'}</div></div>
              <div className="locked"><div className="v"><I n="lock" c="sm" />Rep</div><div className="k">Coming later</div></div></div>
          </div>
          <div>
            <div className="sect"><div className="sh">Outfit <span>From the Veridia wardrobe</span></div>
              <div className="outfits">{OUTFITS.map(([k, l]) => <button key={k} className={`of ${av.outfit === k ? 'sel' : ''}`} onClick={() => upd({ outfit: k })} data-testid={`outfit-${k}`}>
                <div className="im"><Figure cfg={{ ...av, outfit: k }} w={32} /></div>{l}</button>)}</div></div>
            <div className="swcard">
              <div className="swrow"><span className="lb">Hair</span>{sw(Object.entries(HAIRS).map(([k, v]) => [k, v[0]]), av.hair, (k) => upd({ hair: k as AvatarCfg['hair'] }), 'Hair colour')}</div>
              <div className="swrow"><span className="lb">Style</span><span className="seg">{(['short', 'long', 'bun'] as const).map((h) => <button key={h} className={av.hairstyle === h ? 'on' : ''} onClick={() => upd({ hairstyle: h })} disabled={av.outfit === 'hood'}>{h[0].toUpperCase() + h.slice(1)}</button>)}</span></div>
              <div className="swrow"><span className="lb">Skin</span>{sw(Object.entries(SKINS).map(([k, v]) => [k, v[0]]), av.skin, (k) => upd({ skin: k as AvatarCfg['skin'] }), 'Skin tone')}</div>
              {shirt && <div className="swrow"><span className="lb">Shirt</span>{sw(SHIRTS.map((c) => [c, c]), av.shirt ?? '#5c9a3e', (k) => upd({ shirt: k }), 'Shirt colour')}</div>}
              <div className="swrow"><div><div style={{ fontSize: 14, fontWeight: 600 }}>Silk neck band</div><div className="sub">A silky cloth band, as in the book</div></div>
                <button className={`tog ${av.band ? 'on' : ''}`} onClick={() => upd({ band: !av.band })} role="switch" aria-checked={av.band} aria-label="Silk neck band" /></div>
            </div>
            <div style={{ display: 'flex', gap: 8 }}>
              <button className="btn ghost sm" onClick={() => upd(randomAvatar())}><I n="shuffle" c="sm" />Randomize</button>
              <button className="btn ghost sm" disabled={!hist.length} onClick={() => { setAv(hist[hist.length - 1]); setHist(hist.slice(0, -1)); }}>Undo</button>
            </div>
            <div className="swcard">
              <div className="swrow"><div><div style={{ fontSize: 14, fontWeight: 600 }}>Link names publicly</div><div className="sub">Show your handle and citizen name together</div></div>
                <button className={`tog ${linked ? 'on' : ''}`} onClick={() => setLinked(!linked)} role="switch" aria-checked={linked} aria-label="Link names publicly" /></div>
              <div className="swrow"><span className="lb">Theme</span><span className="seg right" data-testid="theme-seg">{(['system', 'light', 'dark'] as ThemePref[]).map((t) => <button key={t} className={theme === t ? 'on' : ''} onClick={() => setTheme(t)} data-testid={`theme-${t}`}>{t[0].toUpperCase() + t.slice(1)}</button>)}</span></div>
            </div>
            {!me.isCitizen && <button className="btn gold" onClick={() => useS.setState({ modal: { kind: 'arrival' } })}><Px src="icon-medal" />Become a citizen</button>}
          </div>
        </div>
      </div>
      <div className="mf">
        <button className="btn ghost" onClick={async () => { await walletDisconnect(wagmi); await signOff(); }} data-testid="sign-off"><I n="logout" c="sm" />Sign off</button>
        <div className="r"><button className="btn primary" onClick={save} disabled={busy} data-testid="save-citizen">Save citizen</button></div>
      </div>
    </Modal>
  );
}

export { Av };
