import { useEffect, useState } from 'react';
import { I, Px, Av, Figure, Modal, BADGE_ICON, BADGE_LABEL, useTicks, avatarUrl, ZipBadge, zipDomain, zipTitle } from '../ui';
import { ZipNamePanel, zipPage } from './ZipName';
import { api, setTheme, signOff, toast, useS, wsSend, type ThemePref } from '../store';
import { ACCENTS, BOTTOMS, SCARVES, TOPS, randomAvatar, type AvatarCfg } from '../../shared/avatar';
import { CLOTH, EXPRS, EYES, HAIRS, HAIRSTYLES, SKINS, type Expr, type HairStyle, type Outfit2 } from '../../shared/avatar2';
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
    {u.zip ? <span className={`pill zip ${u.zip.demo ? 'demo' : ''}`} title={zipTitle(u.zip)} data-testid="zip-pill"><ZipBadge u={u} />{zipDomain(u.zip.name)}{u.zip.demo ? ' · demo' : ''}</span>
      : u.wallet && <span className="pill ok" title="Wallet (no Zipcoin name)"><I n="check" c="sm" />{u.wallet}</span>}
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
  const site = useS.getState().config?.zipcoin.site ?? 'https://www.zipcoin.cash';
  return <>
    <div className="pcard-dim" onClick={close} />
    <div className="pcard" style={{ left: x, top: y }} data-testid="profile-card">
      <div className="scene"><Figure cfg={u.avatar} w={48} /><span className="tr pill dark pixel" style={{ fontSize: 8 }}>{fmtTicks(meldanTicks(since))}</span></div>
      <div className="body">
        <h3 style={{ display: 'flex', alignItems: 'center', gap: 6 }}>{ic || !u.linked ? (ic ? u.citizenName : u.handle) : u.handle}<ZipBadge u={u} /></h3>
        <div className="h">{u.linked || isMe ? (ic ? `@${u.handle} in community channels` : `${u.citizenName} in Tapaia Square`) : ic ? 'Citizen of Meldan' : 'Community member'}</div>
        <div className="chips"><Chips u={u} /></div>
        <div className="row">Citizen since <b>{new Date(since).toLocaleDateString([], { month: 'short', day: 'numeric', year: 'numeric' })}</b></div>
        {u.zip && <div className="row" data-testid="pcard-zip">Zipcoin name <b>{u.zip.demo ? <>{zipDomain(u.zip.name)} <span className="pill sample">DEMO DATA</span></> : <a href={zipPage(site, u.zip.name)} target="_blank" rel="noreferrer noopener">{zipDomain(u.zip.name)}</a>}</b></div>}
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

const OUTFITS: [Outfit2, string][] = [['robe', 'Robe'], ['hood', 'Robe + hood'], ['tee', 'Plain shirt'], ['bandtee', 'Band shirt'],
  ['tunic', 'Tunic'], ['cardigan', 'Cardigan'], ['apron', 'Apron'], ['coat', 'Long coat']];
const STYLE_LABEL: Record<HairStyle, string> = { short: 'Short', swept: 'Swept', crop: 'Crop', curly: 'Curly', long: 'Long', wavy: 'Wavy', bob: 'Bob', braid: 'Braid', ponytail: 'Ponytail', bun: 'Bun', elderbun: 'Low bun' };
const EXPR_LABEL: Record<Expr, string> = { smile: 'Smile', grin: 'Grin', laugh: 'Laugh', content: 'Content', calm: 'Calm', shy: 'Shy', wink: 'Wink', surprised: 'Surprised', thoughtful: 'Thoughtful' };
type BTab = 'outfit' | 'face' | 'extras';

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
  const [tab, setTab] = useState<BTab>('outfit');
  useEffect(() => { avatarUrl(av, 'figure', 80); }, [av]);
  const upd = (p: Partial<AvatarCfg>) => { setHist((h) => [...h.slice(-20), av]); setAv({ ...av, ...p }); };
  const robe = av.outfit === 'robe' || av.outfit === 'hood';
  const hood = av.outfit === 'hood';
  /** switching outfit fills the colour it needs (apron colour, cardigan inner / band-shirt print) */
  const pickOutfit = (k: Outfit2) => upd({ outfit: k, ...(k === 'apron' && !av.over ? { over: 'parchment' } : {}), ...((k === 'cardigan' || k === 'bandtee') && !av.accent ? { accent: 'cream' } : {}) });
  const days = Math.max(1, Math.ceil((Date.now() - (me.arrivalAt ?? me.createdAt)) / 86_400_000));
  async function save() {
    setBusy(true);
    try {
      const { me: m } = await api<{ me: PublicUser }>('/api/profile', { citizenName: name, handle: me.zip && me.handle === me.zip.name ? undefined : handle, avatar: av, linked }, 'PATCH');
      useS.setState({ me: m }); toast('Citizen saved.'); close();
    } catch (e) { toast((e as Error).message, true); } finally { setBusy(false); }
  }
  const sw = (cols: [string, string][], sel: string | undefined | null, on: (k: string) => void, label: string, none?: string) =>
    <span className="sws" role="radiogroup" aria-label={label}>
      {none && <button className={`sw none ${!sel ? 'sel' : ''}`} onClick={() => on('')} aria-label={`${label} ${none}`} aria-checked={!sel} role="radio" title={none} />}
      {cols.map(([k, c]) => <button key={k} className={`sw ${sel === k ? 'sel' : ''}`} style={{ background: c }} onClick={() => on(k)} aria-label={`${label} ${k}`} aria-checked={sel === k} role="radio" title={k} />)}</span>;
  const cl = (keys: string[]): [string, string][] => keys.map((k) => [k, CLOTH[k]]);
  const tog = (on: boolean, set: (v: boolean) => void, label: string, sub: string, disabled = false) =>
    <div className={`swrow ${disabled ? 'off' : ''}`}><div><div style={{ fontSize: 14, fontWeight: 600 }}>{label}</div><div className="sub">{sub}</div></div>
      <button className={`tog ${on ? 'on' : ''}`} onClick={() => !disabled && set(!on)} role="switch" aria-checked={on} aria-label={label} disabled={disabled} data-testid={`tog-${label.toLowerCase().replace(/\W+/g, '-')}`} /></div>;
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
              {me.zip && me.handle === me.zip.name
                ? <div className="h" data-testid="handle-locked">Posts as <b>@{me.handle}</b> <ZipBadge u={me} /> in community channels</div>
                : <div className="h">Posts as <b>@</b><input className="handle-in" style={{ width: `${Math.max(3, handle.length) * 0.6 + 0.9}em` }} value={handle} onChange={(e) => setHandle(e.target.value.toLowerCase().replace(/[^a-z0-9_]/g, ''))} maxLength={20} aria-label="Handle" /> in community channels</div>}
              <div className="chips"><Chips u={me} /></div>
            </div>
            <div className="stats"><div><div className="v">{me.speaks}</div><div className="k">Speaks</div></div>
              <div><div className="v">Day {days}</div><div className="k">{me.isCitizen ? 'Arrived' : 'Joined'}</div></div>
              <div className="locked"><div className="v"><I n="lock" c="sm" />Rep</div><div className="k">Coming later</div></div></div>
            <ZipNamePanel me={me} />
          </div>
          <div>
            <span className="seg btabs" role="tablist" aria-label="Avatar builder">{([['outfit', 'Outfit'], ['face', 'Face & hair'], ['extras', 'Extras']] as [BTab, string][]).map(([k, l]) =>
              <button key={k} role="tab" aria-selected={tab === k} className={tab === k ? 'on' : ''} onClick={() => setTab(k)} data-testid={`btab-${k}`}>{l}</button>)}</span>
            {tab === 'outfit' && <>
              <div className="sect"><div className="sh">Outfit <span>From the Veridia wardrobe</span></div>
                <div className="outfits">{OUTFITS.map(([k, l]) => <button key={k} className={`of ${av.outfit === k ? 'sel' : ''}`} onClick={() => pickOutfit(k)} data-testid={`outfit-${k}`}>
                  <div className="im"><Figure cfg={{ ...av, outfit: k, ...(k === 'apron' && !av.over ? { over: 'parchment' } : {}), ...((k === 'cardigan' || k === 'bandtee') && !av.accent ? { accent: 'cream' } : {}) }} w={32} /></div>{l}</button>)}</div></div>
              <div className="swcard">
                {!robe && <div className="swrow"><span className="lb">{av.outfit === 'apron' ? 'Shirt' : av.outfit === 'cardigan' ? 'Knit' : av.outfit === 'coat' ? 'Coat' : 'Top'}</span>{sw(cl(TOPS), av.top ?? 'leaf', (k) => upd({ top: k }), 'Top colour')}</div>}
                {(av.outfit === 'cardigan' || av.outfit === 'bandtee') && <div className="swrow"><span className="lb">{av.outfit === 'cardigan' ? 'Inner' : 'Print'}</span>{sw(cl(ACCENTS), av.accent, (k) => upd({ accent: k }), av.outfit === 'cardigan' ? 'Inner shirt colour' : 'Print colour')}</div>}
                {av.outfit === 'apron' && <div className="swrow"><span className="lb">Apron</span>{sw(cl(['parchment', 'cream', 'moss', 'wood', 'skyblue', 'rose']), av.over, (k) => upd({ over: k }), 'Apron colour')}</div>}
                {!robe && <div className="swrow"><span className="lb">{av.bottom_kind === 'skirt' ? 'Skirt' : 'Trousers'}</span>{sw(cl(BOTTOMS), av.bottom ?? 'charcoal', (k) => upd({ bottom: k }), 'Bottom colour')}
                  <span className="seg mini">{([['', 'Trousers'], ['skirt', 'Skirt']] as const).map(([k, l]) => <button key={l} className={(av.bottom_kind ?? '') === k ? 'on' : ''} onClick={() => upd({ bottom_kind: k || undefined })}>{l}</button>)}</span></div>}
                {tog(!!av.neckband, (v) => upd({ neckband: v }), 'Silk neck band', hood ? 'Hidden under the hood' : 'A silky cloth band, as in the book', hood)}
              </div>
            </>}
            {tab === 'face' && <>
              <div className="sect"><div className="sh">Hairstyle <span>{hood ? 'Under the hood' : STYLE_LABEL[av.hairstyle ?? 'short']}</span></div>
                <div className="thumbs" role="radiogroup" aria-label="Hairstyle">{HAIRSTYLES.map((h) => <button key={h} role="radio" aria-checked={(av.hairstyle ?? 'short') === h} disabled={hood}
                  className={`th ${(av.hairstyle ?? 'short') === h ? 'sel' : ''}`} onClick={() => upd({ hairstyle: h, ...(h === 'braid' ? { braid_side: av.held && av.hold_side === -1 ? 1 : -1 } : {}) })} title={STYLE_LABEL[h]} data-testid={`hair-${h}`}>
                  <img src={avatarUrl({ ...av, outfit: hood ? 'robe' : av.outfit, hairstyle: h, ...(h === 'braid' && !av.braid_side ? { braid_side: -1 } : {}) }, 'bust', 40)} alt="" draggable={false} /><span>{STYLE_LABEL[h]}</span></button>)}</div></div>
              <div className="swcard">
                <div className="swrow"><span className="lb">Hair</span>{sw(Object.entries(HAIRS), av.hair, (k) => upd({ hair: k as AvatarCfg['hair'] }), 'Hair colour')}</div>
                <div className="swrow"><span className="lb">Skin</span>{sw(Object.entries(SKINS), av.skin, (k) => upd({ skin: k as AvatarCfg['skin'] }), 'Skin tone')}</div>
                <div className="swrow"><span className="lb">Eyes</span>{sw(Object.entries(EYES), av.eyes ?? 'brown', (k) => upd({ eyes: k as AvatarCfg['eyes'] }), 'Eye colour')}</div>
              </div>
              <div className="sect"><div className="sh">Expression <span>{hood ? 'Behind the face cover' : EXPR_LABEL[av.expr ?? 'smile']}</span></div>
                <div className="thumbs faces" role="radiogroup" aria-label="Expression">{EXPRS.map((x) => <button key={x} role="radio" aria-checked={(av.expr ?? 'smile') === x} disabled={hood}
                  className={`th ${(av.expr ?? 'smile') === x ? 'sel' : ''}`} onClick={() => upd({ expr: x })} title={EXPR_LABEL[x]} data-testid={`expr-${x}`}>
                  <img src={avatarUrl({ ...av, outfit: hood ? 'robe' : av.outfit, expr: x }, 'bust', 40)} alt="" draggable={false} /><span>{EXPR_LABEL[x]}</span></button>)}</div></div>
            </>}
            {tab === 'extras' && <>
              <div className="swcard">
                <div className={`swrow ${robe ? 'off' : ''}`}><span className="lb">Holding</span><span className="seg">{([['', 'Nothing'], ['tea', 'Tea cup'], ['book', 'Book']] as const).map(([k, l]) =>
                  <button key={l} disabled={robe} className={(av.held ?? '') === k ? 'on' : ''} onClick={() => upd(k ? { held: k, pose: 'hold', hold_side: av.satchel || (av.hairstyle === 'braid' && (av.braid_side ?? 1) === 1) ? -1 : 1 } : { held: undefined, pose: undefined, hold_side: undefined })} data-testid={`held-${k || 'none'}`}>{l}</button>)}</span>
                  {av.held === 'book' && sw(cl(['maple', 'moss', 'navy', 'plum', 'wood']), av.book_col ?? 'moss', (k) => upd({ book_col: k }), 'Book colour')}</div>
                <div className={`swrow ${robe ? 'off' : ''}`}><span className="lb">Scarf</span>{robe ? <span className="sub">Not with the robe</span> : sw(cl(SCARVES), av.scarf, (k) => upd({ scarf: k || undefined }), 'Scarf', 'No scarf')}</div>
                {tog(!!av.satchel, (v) => upd({ satchel: v || undefined, satchel_side: v ? 1 : undefined, ...(v && av.held ? { hold_side: -1 } : {}) }), 'Satchel', robe ? 'Not with the robe' : 'Leather bag on a shoulder strap', robe)}
                {tog(!!av.glasses, (v) => upd({ glasses: v || undefined }), 'Glasses', hood ? 'Hidden under the hood' : 'Round reading glasses', hood)}
                {tog(!!av.beard, (v) => upd({ beard: v || undefined }), 'Beard', hood ? 'Hidden under the hood' : 'Full, in your hair colour', hood)}
                {tog(!!av.freckles, (v) => upd({ freckles: v || undefined }), 'Freckles', hood ? 'Hidden under the hood' : 'A dusting across the cheeks', hood)}
              </div>
            </>}
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
