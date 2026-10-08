// "Get a Zipcoin name" panel. Availability + burn cost come from zipcoin.cash's public API (via our server, cached).
// PROTOTYPE RULE: this never sends a transaction. Real wallets claim on zipcoin.cash's own page (deep link, prefilled);
// demo accounts get a simulated claim, clearly labelled "DEMO: nothing is burned".
import { useEffect, useRef, useState } from 'react';
import { I, ZipBadge, zipDomain } from '../ui';
import { api, toast, useS } from '../store';
import type { PublicUser } from '../../shared/types';

type State = 'idle' | 'checking' | 'available' | 'taken' | 'reserved' | 'invalid' | 'error';
interface Check { name: string; state: Exclude<State, 'idle' | 'checking'>; apiStatus?: string; keptFor?: string | null; holder?: string | null; priceZc?: number; priceUsd?: number; tier?: string; claimUrl?: string | null }

const NAME_RE = /^[a-z0-9](?:[a-z0-9-]{1,22})[a-z0-9]$/;
const fmt = (n: number) => n.toLocaleString('en-US');
const short = (a: string) => `${a.slice(0, 6)}…${a.slice(-4)}`;
export const zipPage = (site: string, name: string) => `${site}/u/${zipDomain(name)}`;

export function ZipNamePanel({ me }: { me: PublicUser }) {
  const site = useS((s) => s.config?.zipcoin.site) ?? 'https://www.zipcoin.cash';
  const [q, setQ] = useState('');
  const [res, setRes] = useState<Check | null>(null);
  const [state, setState] = useState<State>('idle');
  const [busy, setBusy] = useState(false);
  const seq = useRef(0);

  // debounced availability check
  useEffect(() => {
    const name = q.trim().toLowerCase();
    const id = ++seq.current;
    if (!name) { setState('idle'); setRes(null); return; }
    if (!NAME_RE.test(name)) { setState('invalid'); setRes({ name, state: 'invalid' }); return; }
    setState('checking');
    const t = setTimeout(async () => {
      try {
        const r = await api<Check>(`/api/zipcoin/check?name=${encodeURIComponent(name)}`);
        if (id !== seq.current) return;
        setRes(r); setState(r.state);
      } catch { if (id === seq.current) { setRes({ name, state: 'error' }); setState('error'); } }
    }, 400);
    return () => clearTimeout(t);
  }, [q]);

  async function refresh() {
    setBusy(true);
    try {
      const r = await api<{ me: PublicUser; ok: boolean }>('/api/zipcoin/refresh', {});
      useS.setState({ me: r.me });
      if (!r.ok) toast('Couldn’t reach zipcoin.cash. Showing your short address for now.', true);
      else toast(r.me.zip ? `Found it: ${zipDomain(r.me.zip.name)}` : 'No Zipcoin name on this wallet yet. Claims show up a minute or so after the transaction confirms.');
    } catch (e) { toast((e as Error).message, true); } finally { setBusy(false); }
  }
  async function demoClaim() {
    if (!res || res.state !== 'available') return;
    setBusy(true);
    try {
      const r = await api<{ me: PublicUser }>('/api/zipcoin/demo-claim', { name: res.name });
      useS.setState({ me: r.me }); setQ('');
      toast(`DEMO: ${zipDomain(res.name)} is yours in this demo. Nothing was burned.`);
    } catch (e) { toast((e as Error).message, true); } finally { setBusy(false); }
  }

  // ---- already holds a name
  if (me.zip) {
    const d = zipDomain(me.zip.name);
    return <div className="zippanel" data-testid="zip-panel" data-mode={me.zip.demo ? 'demo-held' : 'held'}>
      <div className="zh"><ZipBadge u={me} />{me.zip.demo ? 'Demo Zipcoin name' : 'Your Zipcoin name'}</div>
      <div className="zname" data-testid="zip-held">{me.zip.demo ? d : <a href={zipPage(site, me.zip.name)} target="_blank" rel="noreferrer noopener">{d}</a>}<span className="zipdom"> · {me.zip.name}.zipbook.eth</span></div>
      <div className="zsub">{me.zip.demo
        ? <><b>DEMO: nothing was burned</b> and nothing is registered on zipcoin.cash. It’s your @handle in this demo only.</>
        : <>Verified from your wallet through zipcoin.cash. It’s your @handle here and shows with a green seal. Your citizen name in Tapaia Square is still yours to change.</>}</div>
      {!me.zip.demo && <div className="zfine">Released or transferred it? <button onClick={refresh} disabled={busy} data-testid="zip-refresh">Check again</button></div>}
    </div>;
  }

  const wallet = me.kind === 'wallet';
  const keptForMe = !!(res?.keptFor && me.wallet && short(res.keptFor).toLowerCase() === me.wallet.toLowerCase()); // the short form is only a UI hint; zipcoin.cash enforces the rule
  const cost = res?.priceZc
    ? <>Claiming burns <span className="zcost" data-testid="zip-cost">{fmt(res.priceZc)} ZC</span>{res.priceUsd ? <> (about ${res.priceUsd < 100 ? res.priceUsd.toFixed(2) : fmt(Math.round(res.priceUsd))} today)</> : null}{res.tier && res.tier !== 'row' ? <>. Short names cost more</> : null}.</>
    : <span data-testid="zip-cost">Claiming burns ZC; see zipcoin.cash for the current cost.</span>;
  const msg: Record<State, React.ReactNode> = {
    idle: <>Names are 3 to 24 lowercase letters, digits and hyphens.</>,
    checking: <>Checking zipcoin.cash…</>,
    available: <span><b>{res && zipDomain(res.name)}</b> is available. {cost}</span>,
    taken: <span><b>{res && zipDomain(res.name)}</b> is taken{res?.holder ? <> (held by {short(res.holder)})</> : null}. Try another.</span>,
    reserved: res?.apiStatus === 'reserved-for'
      ? keptForMe ? <span><b>{res && zipDomain(res.name)}</b> is kept for your wallet. {cost}</span>
      : <span><b>{res && zipDomain(res.name)}</b> is reserved: zipcoin.cash keeps it for the owner of the matching well-known .eth name, so only a claim for that address counts.</span>
      : <span><b>{res && zipDomain(res.name)}</b> is reserved by zipcoin.cash (system and house words). Try another.</span>,
    invalid: <>Not a valid name. Use 3 to 24 lowercase letters, digits and hyphens, with no hyphen at either end.</>,
    error: <>Couldn’t reach zipcoin.cash right now. Try again in a moment.</>,
  };
  const canClaim = state === 'available' || (state === 'reserved' && keptForMe);
  return <div className="zippanel" data-testid="zip-panel" data-mode={wallet ? 'wallet' : 'demo'}>
    <div className="zh"><I n="sparkle" c="sm" />Get a Zipcoin name</div>
    <div className="zsub">Claim <b>yourname.zipcoin.cash</b> (and yourname.zipbook.eth) by burning zipcoins. It becomes your verified @handle here, with a green seal.</div>
    <label className="zfield"><input value={q} onChange={(e) => setQ(e.target.value.toLowerCase().replace(/\s/g, ''))} placeholder="yourname" maxLength={24} spellCheck={false} autoCapitalize="none" autoCorrect="off" aria-label="Zipcoin name to check" data-testid="zip-input" /><span className="suf">.zipcoin.cash</span></label>
    <div className="zstate" data-testid="zip-state" data-state={state} aria-live="polite"><span className="dotz" /><span>{msg[state]}</span></div>
    {wallet ? <>
      <div className="zacts">
        <a className={`btn primary sm ${canClaim ? '' : 'disabled'}`} href={canClaim && res ? (res.claimUrl ?? `${site}/names?name=${encodeURIComponent(res.name)}`) : undefined} target="_blank" rel="noreferrer noopener" aria-disabled={!canClaim} onClick={(e) => { if (!canClaim) e.preventDefault(); }} data-testid="zip-claim">Claim on zipcoin.cash<I n="ext" c="sm" /></a>
      </div>
      <div className="zfine">You burn from your own wallet on zipcoin.cash. Tapaia never asks for a transaction. Claimed it already? <button onClick={refresh} disabled={busy} data-testid="zip-refresh">Check my wallet again</button></div>
    </> : <>
      <div className="zacts">
        <button className="btn burn sm" disabled={state !== 'available' || busy} onClick={demoClaim} data-testid="zip-demo-claim">Simulate claim</button>
        <span className="pill demo" data-testid="zip-demo-flag">DEMO: nothing is burned</span>
      </div>
      <div className="zfine">Demo accounts get a simulated name that only exists in this demo. Sign in with a wallet to claim a real one on zipcoin.cash.</div>
    </>}
  </div>;
}
