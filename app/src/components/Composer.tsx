import { useEffect, useRef, useState } from 'react';
import { I, Px, Av } from '../ui';
import { nameIn, toast, useS, wsSend } from '../store';
import { byteLen } from '../../shared/perms';
import type { Channel, PublicUser } from '../../shared/types';

const EMOJI = ['😀', '😂', '🥲', '😍', '🤔', '👋', '🙌', '👍', '🎉', '🔥', '🍵', '☕', '🌿', '🍁', '🃏', '📚', '🙏', '👀'];
const drafts: Record<string, string> = {};

export function Composer({ ch, mobile }: { ch: Channel; mobile: boolean }) {
  const me = useS((s) => s.me)!;
  const users = useS((s) => s.users);
  const replyTo = useS((s) => s.replyTo);
  const reply = useS((s) => (s.replyTo ? s.messages[ch.id]?.find((m) => m.id === s.replyTo) : undefined));
  const [text, setText] = useState(drafts[ch.id] ?? '');
  const [mode, setMode] = useState<'say' | 'speak'>('say');
  const [sug, setSug] = useState<{ q: string; start: number; sel: number } | null>(null);
  const [emo, setEmo] = useState(false);
  const ta = useRef<HTMLTextAreaElement>(null);
  const lastTyping = useRef(0);
  const ic = ch.layer === 'ic';

  useEffect(() => { setText(drafts[ch.id] ?? ''); setMode('say'); setSug(null); }, [ch.id]);
  useEffect(() => { drafts[ch.id] = text; const el = ta.current; if (el) { el.style.height = 'auto'; el.style.height = Math.min(el.scrollHeight, mobile ? 120 : 160) + 'px'; } }, [text, ch.id, mobile]);

  const candidates: PublicUser[] = sug ? Object.values(users)
    .filter((u) => u.id !== me.id && u.kind !== 'bot' && (!ic || u.isCitizen))
    .filter((u) => nameIn(u, ch).toLowerCase().includes(sug.q.toLowerCase()) || u.handle.includes(sug.q.toLowerCase()))
    .sort((a, b) => (a.presence === 'off' ? 1 : 0) - (b.presence === 'off' ? 1 : 0))
    .slice(0, 6) : [];

  function onChange(v: string) {
    setText(v);
    const caret = ta.current?.selectionStart ?? v.length;
    const before = v.slice(0, caret);
    const m = /(^|\s)@([\p{L}0-9_ ]{0,24})$/u.exec(before);
    if (m && !(m[2].includes(' ') && !ic)) setSug({ q: m[2], start: caret - m[2].length - 1, sel: 0 }); else setSug(null);
    if (Date.now() - lastTyping.current > 2500 && v.trim()) { lastTyping.current = Date.now(); wsSend({ t: 'typing', channel: ch.id }); }
  }
  function pick(u: PublicUser) {
    if (!sug) return;
    const caret = ta.current?.selectionStart ?? text.length;
    const ins = `@${nameIn(u, ch)} `;
    const v = text.slice(0, sug.start) + ins + text.slice(caret);
    setText(v); setSug(null);
    requestAnimationFrame(() => { ta.current?.focus(); const p = sug.start + ins.length; ta.current?.setSelectionRange(p, p); });
  }
  function send() {
    const t = text.trim();
    if (!t) return;
    if (mode === 'speak') {
      if (byteLen(t) > 280) return toast('Speak posts are limited to 280 bytes, like the Book.', true);
      useS.setState({ modal: { kind: 'speak', text: t, replyTo: replyTo ?? undefined } });
      setText(''); setMode('say');
      return;
    }
    wsSend({ t: 'send', channel: ch.id, text: t, replyTo: replyTo ?? undefined });
    setText(''); useS.setState({ replyTo: null }); setSug(null);
  }
  function onKey(e: React.KeyboardEvent) {
    if (sug && candidates.length) {
      if (e.key === 'ArrowDown') { e.preventDefault(); setSug({ ...sug, sel: (sug.sel + 1) % candidates.length }); return; }
      if (e.key === 'ArrowUp') { e.preventDefault(); setSug({ ...sug, sel: (sug.sel - 1 + candidates.length) % candidates.length }); return; }
      if (e.key === 'Enter' || e.key === 'Tab') { e.preventDefault(); pick(candidates[sug.sel]); return; }
      if (e.key === 'Escape') { setSug(null); return; }
    }
    if (e.key === 'Enter' && !e.shiftKey && !mobile) { e.preventDefault(); send(); }
    if (e.key === 'Escape' && replyTo) useS.setState({ replyTo: null });
  }
  const placeholder = ch.layer === 'dm' ? `Message ${nameIn(users[ch.members?.find((x) => x !== me.id) ?? ''], ch)}` : ic ? (mode === 'speak' ? 'Speak to the whole square…' : mobile ? 'Say something…' : `Say something as ${me.citizenName}…`) : `Message #${ch.name}`;
  const suggest = sug && candidates.length > 0 && <div className="suggest" role="listbox"><div className="h">{ic ? 'CITIZENS' : 'PEOPLE'}</div>
    {candidates.map((u, i) => <button key={u.id} className={i === sug.sel ? 'sel' : ''} onMouseDown={(e) => { e.preventDefault(); pick(u); }}><Av u={u} size="s28" />{nameIn(u, ch)}<span className="sub">{ic ? `@${u.handle}` : u.citizenName}</span></button>)}</div>;
  const emojis = emo && <div className="emojis">{EMOJI.map((e) => <button key={e} onMouseDown={(ev) => { ev.preventDefault(); setText((t) => t + e); setEmo(false); ta.current?.focus(); }}>{e}</button>)}</div>;
  const replying = reply && <div className="replying"><I n="reply" c="sm" />Replying to <b>{nameIn(users[reply.userId ?? ''], ch)}</b><button className="x" onClick={() => useS.setState({ replyTo: null })} aria-label="Cancel reply"><I n="x" c="sm" /></button></div>;
  const seg = ic && <span className="seg" role="radiogroup" aria-label="Say or Speak">
    <button className={mode === 'say' ? 'on' : ''} onClick={() => setMode('say')} data-testid="mode-say"><I n="chat" c="sm" />Say</button>
    <button className={`burn ${mode === 'speak' ? 'on' : ''}`} onClick={() => setMode('speak')} data-testid="mode-speak"><Px src="icon-flame" />Speak</button></span>;
  const input = <textarea id="composer-input" ref={ta} rows={1} value={text} placeholder={placeholder} onChange={(e) => onChange(e.target.value)} onKeyDown={onKey} onBlur={() => setTimeout(() => setSug(null), 150)} maxLength={2000} data-testid="composer" aria-label={placeholder} enterKeyHint="send" />;
  const sendBtn = <button className={`send ${mode === 'speak' ? 'burn' : ''}`} onClick={send} disabled={!text.trim()} aria-label={mode === 'speak' ? 'Speak' : 'Send'} data-testid="send"><I n="send" /></button>;

  if (mobile) return (
    <div className="mcomp">{suggest}{emojis}{replying}
      {ic && <div className="modes">{seg}<span className="hint">{mode === 'speak' ? 'Speak burns ZC · demo: simulated' : 'Say is free · Speak burns ZC'}</span></div>}
      <div className="row"><button className="plus" onClick={() => toast('Attachments come later. Phase 1 keeps it to text.')} aria-label="Add"><I n="plus" /></button>
        <div className="field">{input}<button className="ic" onClick={() => setEmo(!emo)} aria-label="Emoji"><I n="smile" /></button></div>{sendBtn}</div>
    </div>
  );
  return (
    <div className="composer">{suggest}{emojis}{replying}
      <div className="row"><button className="iconbtn" onClick={() => toast('Attachments come later. Phase 1 keeps it to text.')} aria-label="Add"><I n="plus" /></button>
        {input}
        <button className="iconbtn" onClick={() => setEmo(!emo)} aria-label="Emoji"><I n="smile" /></button>
        {seg}{sendBtn}</div>
      {ic && <div className="foot">Say is free. <b style={{ color: 'var(--ember-600)', fontWeight: 600 }}>Speak</b> posts to the zipcoin Book: burns ≥ <span className="ph">S</span> ZC + gas, permanent and public. <span className="pill demo sample">demo: simulated, nothing burned</span></div>}
    </div>
  );
}
