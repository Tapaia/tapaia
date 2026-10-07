import { useEffect, useState } from 'react';
import { I, Px, Av, Figure, Modal, Chk } from '../ui';
import { api, openChannel, refreshConfig, toast, useS, wsSend } from '../store';
import { byteLen } from '../../shared/perms';
import type { PublicUser } from '../../shared/types';

const SIM_STEPS = ['Waiting for your wallet to sign (simulated)', 'Speak transaction pending on Ethereum (simulated)', 'Checking the burn on-chain (simulated)'];

function BurnNotice({ kind }: { kind: 'arrival' | 'speak' }) {
  const cfg = useS((s) => s.config);
  return (
    <div className="callout">
      <div className="t"><Px src="icon-flame" />This would burn real ZC and be permanent</div>
      <ul>
        <li>Posted to the zipcoin Book forever: public, can’t be edited or deleted, reposted to X by @zipcoinbook.</li>
        <li>Links this wallet to Tapaia publicly. Not refundable. We never hold your tokens or keys.</li>
        <li>Only real ZC counts: <b>0x4E67…8722</b></li>
      </ul>
      <div className="costs">
        <div className="cost"><div className="k">BURN</div><div className="v"><Px src="icon-coin" /><span className="ph">{kind === 'arrival' ? 'E' : 'S'}</span> ZC</div></div>
        <div className="cost"><div className="k">≈ VALUE + GAS</div><div className="v">live estimate</div></div>
        <div className="cost"><div className="k">ZIPCOIN MINIMUM</div><div className="v">{(cfg?.speakMinimum ?? 1000).toLocaleString()} ZC</div></div>
      </div>
      <div className="demo-flag" data-testid="demo-flag"><Px src="icon-flame" style={{ width: 16, height: 16 }} />DEMO: nothing is burned. No transaction is sent from this prototype.</div>
    </div>
  );
}

function SimProgress({ step }: { step: number }) {
  return <div className="progress-steps">{SIM_STEPS.map((t, i) => (
    <div key={i} className={`ps ${i < step ? 'done' : i === step ? 'now' : ''}`}><span className="c">{i < step && <I n="check" c="sm" />}</span>{t}</div>
  ))}</div>;
}
const sleep = (ms: number) => new Promise((r) => setTimeout(r, ms));

export function ArrivalModal() {
  const me = useS((s) => s.me)!;
  const cfg = useS((s) => s.config);
  const close = () => useS.setState({ modal: null });
  const [path, setPath] = useState<'founder' | 'burn'>('founder');
  const [text, setText] = useState('');
  const [c1, setC1] = useState(false), [c2, setC2] = useState(false);
  const [stage, setStage] = useState<'write' | 'signing' | 'done'>('write');
  const [simStep, setSimStep] = useState(0);
  const [result, setResult] = useState<PublicUser | null>(null);
  useEffect(() => { refreshConfig().catch(() => {}); }, []);
  const total = cfg?.founderSlots.total ?? 0, used = cfg?.founderSlots.used ?? 0, left = Math.max(0, total - used);
  useEffect(() => { if (cfg && left === 0) setPath('burn'); }, [cfg, left]);
  const bytes = byteLen(text.trim());
  const valid = bytes > 0 && bytes <= 280;
  const canSubmit = valid && (path === 'founder' ? left > 0 : c1 && c2);

  async function submit() {
    if (!canSubmit) return;
    setStage('signing');
    try {
      if (path === 'burn') { for (let i = 0; i < SIM_STEPS.length; i++) { setSimStep(i); await sleep(900); } setSimStep(SIM_STEPS.length); }
      const r = await api<{ me: PublicUser }>('/api/arrival', { path, text: text.trim() });
      useS.setState({ me: r.me });
      setResult(r.me);
      setStage('done');
      refreshConfig().catch(() => {});
    } catch (e) { toast((e as Error).message, true); setStage('write'); }
  }

  const stepIdx = stage === 'write' ? 1 : stage === 'signing' ? 2 : 3;
  const preview = (
    <div className="card-arrival pv"><div className="fig"><Figure cfg={me.avatar} w={48} /></div>
      <div style={{ minWidth: 0 }}><div className="k"><Px src={path === 'founder' ? 'icon-medal' : 'icon-flame'} style={{ width: 14, height: 14 }} />{stage === 'done' ? 'New arrival' : 'Preview'} · {path === 'founder' ? 'Founding Citizen' : 'new citizen'}</div>
        <div className="q"><b>{me.citizenName}</b> “{text.trim() || 'Your arrival message…'}”</div></div></div>
  );

  if (stage === 'done' && result) return (
    <Modal onClose={close} size="sm" label="Welcome">
      <div className="prof-body">
        <div className="welcome">
          <div className="phero"><span className="pill glass tl"><Px src="icon-tree" />Tapaia Square</span><span className="shadow" /><Figure cfg={me.avatar} w={80} className="ava" /></div>
          <h3>Welcome to Tapaia, {result.citizenName}!</h3>
          <p className="small" style={{ margin: 0 }}>{path === 'founder' ? 'You’re a Founding Citizen. Your free arrival post is in the Square.' : 'Your arrival post is in the Square. Demo: nothing was burned.'}</p>
        </div>
        {preview}
        <div className="chips" style={{ display: 'flex', gap: 6, justifyContent: 'center' }}>
          {path === 'founder' ? <span className="pill gold"><Px src="icon-medal" />Founding Citizen</span> : <span className="pill ember"><Px src="icon-flame" />Citizen · arrival post (demo)</span>}
        </div>
      </div>
      <div className="mf"><div className="steps"><span className="s done" /><span className="s done" /><span className="s done" /><span className="s done" />Step 4 of 4 · you’re in</div>
        <div className="r"><button className="btn primary" data-testid="walk-in" onClick={() => { close(); openChannel('square'); }}><Px src="icon-tree" />Walk into Tapaia Square</button></div></div>
    </Modal>
  );

  return (
    <Modal onClose={stage === 'write' ? close : undefined} label="Become a citizen">
      <div className="mh"><span className="medal"><Px src="icon-medal" /></span>
        <div><h2>Become a citizen of Tapaia</h2><p>Your arrival post is how you join. Everyone in Tapaia Square gets to greet you.</p></div>
        <button className="iconbtn x" onClick={close} aria-label="Close" disabled={stage !== 'write'}><I n="x" /></button></div>
      <div className="mb">
        <div className="mcol" style={{ width: 330, flex: 'none' }}>
          <div className="box"><h4>FOUNDING CITIZEN SLOTS</h4>
            <div className="slots-big" data-testid="slots">{left} of {total} left</div>
            <div className="prog"><i style={{ width: `${total ? (left / total) * 100 : 0}%` }} /></div>
            <div className="small" style={{ marginTop: 6 }}>Demo value. The real <span className="ph">X</span> isn’t decided yet.</div>
            <div style={{ marginTop: 12 }}>
              <div className="kv"><span>Founder window</span><b><span className="ph">dates TBD</span></b></div>
              <div className="kv"><span>Limit</span><b>1 per wallet</b></div>
              <div className="kv"><span>Eligibility</span><b><span className="ph">rule TBD</span></b></div></div>
          </div>
          <div className="notice-soft"><I n="info" c="sm" /><div>{left > 0 ? 'In the demo every account is eligible for a free founder slot. Or try the burn path to see how an on-chain arrival post works.' : 'Founder slots are gone, so you’ll join with an arrival post.'}</div></div>
          <div className="box"><h4>AS A CITIZEN YOU CAN</h4>
            <div style={{ fontSize: 14, lineHeight: 1.75 }}>✓ Post in every community channel<br />✓ Chat as your citizen in Tapaia Square<br />✓ Build your pixel avatar<br /><span className="small">One-time entry. Never re-checked.</span></div></div>
        </div>
        <div className="mcol" style={{ flex: 1 }}>
          <span className="seg big" style={{ alignSelf: 'flex-start' }}>
            <button className={path === 'founder' ? 'on' : ''} disabled={left === 0 || stage !== 'write'} onClick={() => setPath('founder')} data-testid="path-founder"><Px src="icon-medal" />Founding Citizen · free</button>
            <button className={`burn ${path === 'burn' ? 'on' : ''}`} disabled={stage !== 'write'} onClick={() => setPath('burn')} data-testid="path-burn"><Px src="icon-flame" />Arrival post · burn</button>
          </span>
          <div className="field"><label htmlFor="arr">Your arrival message</label>
            <textarea id="arr" className="ta" value={text} disabled={stage !== 'write'} placeholder="Hello Tapaia! …" onChange={(e) => setText(e.target.value)} autoFocus data-testid="arrival-text" />
            <div className="fieldrow"><span>Posting as <b style={{ color: 'var(--text-2)' }}>{me.citizenName}</b> · keep it short and kind</span><span className={bytes > 280 ? 'over' : ''}>{bytes} / 280 bytes</span></div></div>
          {preview}
          {path === 'founder' ? (
            <div className="callout green"><div className="t"><Px src="icon-medal" />Free Founding Citizen arrival</div>
              <ul><li>Stored by Tapaia as a free in-game arrival post (not on-chain). It can be moderated like any message.</li>
                <li>You get the <b>Founding Citizen</b> badge. It can’t be transferred and carries no votes or powers.</li>
                <li>One slot per wallet. Uses one of the <span className="ph">X</span> slots.</li></ul></div>
          ) : stage === 'signing' ? (
            <div className="box"><h4>SIGNING · SIMULATED</h4><SimProgress step={simStep} /></div>
          ) : (<>
            <BurnNotice kind="arrival" />
            <Chk on={c1} set={setC1}>I understand this post is permanent and public.</Chk>
            <Chk on={c2} set={setC2}>I understand the burn can’t be refunded.</Chk>
          </>)}
        </div>
      </div>
      <div className="mf"><div className="steps"><span className="s done" /><span className={`s ${stepIdx > 1 ? 'done' : 'on'}`} /><span className={`s ${stepIdx === 2 ? 'on' : ''}`} /><span className="s" />Step {stepIdx + 1} of 4 · {stage === 'write' ? 'write your arrival' : 'signing'}</div>
        <div className="r"><button className="btn ghost" onClick={close} disabled={stage !== 'write'}>Later</button>
          {path === 'founder'
            ? <button className="btn gold" disabled={!canSubmit || stage !== 'write'} onClick={submit} data-testid="claim-founder"><Px src="icon-medal" />Claim founder slot</button>
            : <button className="btn burn" disabled={!canSubmit || stage !== 'write'} onClick={submit} data-testid="sign-burn"><Px src="icon-flame" />Sign &amp; burn (demo)</button>}
        </div></div>
    </Modal>
  );
}

export function SpeakModal({ text, replyTo }: { text: string; replyTo?: number }) {
  const me = useS((s) => s.me)!;
  const close = () => useS.setState({ modal: null });
  const [c1, setC1] = useState(false), [c2, setC2] = useState(false);
  const [step, setStep] = useState(-1);
  const bytes = byteLen(text);
  async function go() {
    for (let i = 0; i < SIM_STEPS.length; i++) { setStep(i); await sleep(700); }
    wsSend({ t: 'send', channel: 'square', text, replyTo, mode: 'speak' });
    useS.setState({ replyTo: null });
    close();
    toast('Spoke to the Square. Demo: nothing burned.');
  }
  return (
    <Modal onClose={step < 0 ? close : undefined} size="md" label="Speak to the Square">
      <div className="mh"><span className="medal ember"><Px src="icon-flame" /></span>
        <div><h2>Speak to the Square</h2><p>A Speak is a real zipcoin Book post. In this demo it’s simulated.</p></div>
        <button className="iconbtn x" onClick={close} aria-label="Close"><I n="x" /></button></div>
      <div className="prof-body">
        <div className="card-speak" style={{ margin: 0 }}><div className="h"><Px src="icon-flame" />Preview · Speak <span className="ph" style={{ textTransform: 'none' }}>S</span> ZC</div>
          <div className="b"><Av u={me} /><div style={{ minWidth: 0 }}><div className="meta"><span className="who">{me.citizenName}</span></div><div className="text">{text}</div></div></div></div>
        <div className="fieldrow" style={{ marginTop: -4 }}><span /><span className={bytes > 280 ? 'over' : ''}>{bytes} / 280 bytes</span></div>
        {step >= 0 ? <div className="box"><h4>SIGNING · SIMULATED</h4><SimProgress step={step} /></div> : <>
          <BurnNotice kind="speak" />
          <Chk on={c1} set={setC1}>I understand this post is permanent and public.</Chk>
          <Chk on={c2} set={setC2}>I understand the burn can’t be refunded.</Chk>
        </>}
      </div>
      <div className="mf"><div className="r"><button className="btn ghost" onClick={close} disabled={step >= 0}>Cancel</button>
        <button className="btn burn" disabled={!c1 || !c2 || bytes > 280 || step >= 0} onClick={go} data-testid="speak-confirm"><Px src="icon-flame" />Sign &amp; speak (demo)</button></div></div>
    </Modal>
  );
}
