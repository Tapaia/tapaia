import { useEffect, useState } from 'react';
import { useConfig, useConnectors, type Connector } from 'wagmi';
import { I, Px, Av, Figure, Modal } from '../ui';
import { api, enterApp, toast, useS } from '../store';
import { KNOWN, isDiscovered, signInWithWallet, friendlyError } from '../wallet';
import { randomAvatar, type AvatarCfg } from '../../shared/avatar';
import type { PublicUser } from '../../shared/types';
import { Legal } from './Legal';

const HERO_PEOPLE: Pick<PublicUser, 'avatar' | 'tile'>[] = [
  { tile: 'c5', avatar: { outfit: 'robe', skin: 'fair', hair: 'ginger', hairstyle: 'long', band: true } },
  { tile: 'c2', avatar: { outfit: 'robe', skin: 'deep', hair: 'black', hairstyle: 'bun', band: true } },
  { tile: 'c1', avatar: { outfit: 'hood', skin: 'warm', hair: 'black', hairstyle: 'short', band: true } },
  { tile: 'c3', avatar: { outfit: 'plain', skin: 'tan', hair: 'black', hairstyle: 'short', band: false, shirt: '#f2c84b' } },
];

export function SignIn() {
  const config = useConfig();
  const connectors = useConnectors();
  const wcEnabled = !!useS((s) => s.config?.walletConnectProjectId);
  const [busy, setBusy] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [demo, setDemo] = useState(false);

  const discovered = connectors.filter(isDiscovered);
  const byRdns = (rdns: string[]) => discovered.find((c) => rdns.includes(c.id) || (c.rdns && [c.rdns].flat().some((r) => rdns.includes(r))));
  const legacy = connectors.find((c) => c.id === 'injected');
  const cbSdk = connectors.find((c) => c.id === 'coinbaseWalletSDK');
  const wc = connectors.find((c) => c.id === 'walletConnect');
  const knownRdns = KNOWN.flatMap((k) => k.rdns);
  const others = discovered.filter((c) => !knownRdns.includes(c.id));
  const hasLegacy = typeof window !== 'undefined' && !!(window as any).ethereum && discovered.length === 0;

  async function go(key: string, c: Connector | undefined, install?: string) {
    setError(null);
    if (!c) {
      setError(wcEnabled ? 'Not detected in this browser.' : `${KNOWN.find((k) => k.key === key)?.name ?? 'That wallet'} isn’t installed in this browser. Install it, or use “Try the demo”. Phone wallets over WalletConnect need a WalletConnect project id on the server.`);
      if (install) window.open(install, '_blank', 'noopener');
      return;
    }
    setBusy(key);
    try {
      const me = await signInWithWallet(config, c);
      await enterApp(me, { arrival: !me.isCitizen });
    } catch (e) {
      setError(friendlyError(e));
    } finally { setBusy(null); }
  }

  const row = (key: string, name: string, c: Connector | undefined, opts: { detected?: boolean; sub?: string; install?: string; icon?: string; right?: React.ReactNode } = {}) => (
    <button key={key} className="wrow" disabled={!!busy} onClick={() => go(key, c, opts.install)} data-testid={`wallet-${key}`}>
      <span className="ico">{opts.icon ? <img src={opts.icon} alt="" /> : <Px src={`wallet-${key}`} />}</span>
      <span className="lbl">{name}{opts.sub && <span className="sub">{opts.sub}</span>}</span>
      <span className="r">{busy === key ? <span className="small">Check your wallet…</span> : opts.right ?? (opts.detected && <span className="pill ok">Detected</span>)}<I n="chev-r" c="sm" /></span>
    </button>
  );

  return (
    <div className="split">
      <section className="hero" aria-hidden>
        <div className="brand"><span className="logo-tile"><Px src="icon-tea" /></span><b>Tapaia</b></div>
        <div className="copy"><h1>The town square for<br />the $ZC community.</h1>
          <p>Chat like you would on Telegram. Step into Veridia and speak as your citizen whenever you feel like it.</p>
          <div className="proof"><span className="avs">{HERO_PEOPLE.map((p, i) => <Av key={i} u={p} />)}</span>Open source · based on <i>Snowmoon</i></div></div>
      </section>
      <section className="form"><div className="inner">
        <div className="mobile-hero"><div className="brand"><span className="logo-tile"><Px src="icon-tea" /></span><b>Tapaia</b></div><div className="t">The town square for the $ZC community.</div></div>
        <h2>Welcome to Tapaia</h2>
        <p className="lede">Try it instantly, or sign in with the wallet you already use.</p>
        <button className="demo-cta" onClick={() => setDemo(true)} data-testid="try-demo">
          <span className="ico"><Px src="icon-tea" /></span>
          <span><b>Try the demo</b><span className="s">No wallet needed. Nothing touches real ZC.</span></span>
          <span className="r"><I n="chev-r" /></span>
        </button>
        <div className="orline">or sign in with your wallet</div>
        <div className="wallets">
          {KNOWN.map((k) => {
            const d = byRdns(k.rdns);
            if (k.key === 'coinbase') return row(k.key, k.name, d ?? cbSdk, { detected: !!d, sub: d ? undefined : 'Extension, app or smart wallet' });
            return row(k.key, k.name, d ?? (wcEnabled ? wc : undefined), { detected: !!d, install: k.install, sub: !d && wcEnabled ? 'Scan with your phone' : undefined });
          })}
          {others.map((c) => row(c.id, c.name, c, { detected: true, icon: c.icon }))}
          {hasLegacy && row('injected', 'Browser wallet', legacy, { detected: true, icon: '/assets/icon-wallet.png' })}
          {row('walletconnect', 'WalletConnect', wc, { sub: wcEnabled ? 'Phone wallets and many more' : 'Not configured on this server', right: <span className="pill neutral"><I n="qr" c="sm" />QR</span> })}
        </div>
        {error && <div className="err-box" role="alert">{error}</div>}
        <div className="siwe"><I n="shield" c="sm" /><div><b>Free, no transaction, no gas.</b> You’ll sign a one-time message (Sign-In with Ethereum) to prove the wallet is yours. We never touch your funds.</div></div>
        <div className="alt"><span>Just looking? <button onClick={() => enterApp(null, { channel: 'lobby' })} data-testid="browse-lobby">Browse #lobby →</button></span><button onClick={() => enterApp(null, { channel: 'lobby' })}>Get help</button></div>
        <Legal className="legal" />
      </div></section>
      {demo && <DemoDialog onClose={() => setDemo(false)} />}
    </div>
  );
}

export function DemoDialog({ onClose }: { onClose: () => void }) {
  const [s, setS] = useState<{ citizenName: string; handle: string; avatar: AvatarCfg } | null>(null);
  const [busy, setBusy] = useState(false);
  const reroll = () => api<{ citizenName: string; handle: string; avatar: AvatarCfg }>('/api/demo/suggest').then(setS).catch(() => setS({ citizenName: 'Fennel Ashby', handle: 'fennela', avatar: randomAvatar() }));
  useEffect(() => { reroll(); }, []);
  async function start(skipArrival: boolean) {
    if (!s) return;
    setBusy(true);
    try {
      const { me } = await api<{ me: PublicUser }>('/api/demo', { ...s, skipArrival });
      await enterApp(me, { arrival: !skipArrival, channel: skipArrival ? 'square' : 'lobby' });
    } catch (e) { toast((e as Error).message, true); setBusy(false); }
  }
  return (
    <Modal onClose={onClose} size="sm" label="Try the demo">
      <div className="mh"><span className="medal"><Px src="icon-tea" /></span>
        <div><h2>Try Tapaia as a demo citizen</h2><p>No wallet, no sign-up. Pick a name or roll a new one.</p></div>
        <button className="iconbtn x" onClick={onClose} aria-label="Close"><I n="x" /></button></div>
      <div className="prof-body">
        <div className="phero"><span className="pill glass tl"><Px src="icon-tree" />Tapaia Square</span>
          <span className="shadow" />{s && <Figure cfg={s.avatar} w={80} className="ava" alt="Your demo avatar" />}
          <button className="btn ghost sm reroll" onClick={reroll} data-testid="reroll"><I n="shuffle" c="sm" />Roll again</button></div>
        <div className="field"><label htmlFor="dn">Citizen name (used in Tapaia Square)</label>
          <input id="dn" className="input" value={s?.citizenName ?? ''} maxLength={32} onChange={(e) => s && setS({ ...s, citizenName: e.target.value })} /></div>
        <div className="field"><label htmlFor="dh">Handle (used in community channels)</label>
          <input id="dh" className="input" value={s?.handle ?? ''} maxLength={20} onChange={(e) => s && setS({ ...s, handle: e.target.value.toLowerCase().replace(/[^a-z0-9_]/g, '') })} /></div>
        <div className="notice-soft"><I n="info" c="sm" /><div>Demo mode: other people trying the demo can see your messages live. Nothing is burned and no wallet is involved. You can change your avatar later.</div></div>
      </div>
      <div className="mf"><div className="steps"><span className="s on" /><span className="s" /><span className="s" /><span className="s" />Step 1 of 4 · pick a citizen</div>
        <div className="r">
          <button className="btn ghost" disabled={busy || !s} onClick={() => start(true)} data-testid="demo-skip">Skip to the Square</button>
          <button className="btn primary" disabled={busy || !s} onClick={() => start(false)} data-testid="demo-start">Start with arrival</button>
        </div></div>
    </Modal>
  );
}
