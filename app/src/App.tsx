import { useEffect } from 'react';
import { useConnection, useConfig } from 'wagmi';
import { useMedia } from './ui';
import { signOff, toast, useS } from './store';
import { SignIn } from './components/SignIn';
import { Sidebar } from './components/Sidebar';
import { Main } from './components/Main';
import { Members } from './components/Members';
import { ArrivalModal, SpeakModal } from './components/Arrival';
import { ProfileCard, ProfileEditor } from './components/Profile';
import { walletDisconnect } from './wallet';

function Toasts() {
  const toasts = useS((s) => s.toasts);
  return <div className="toasts" aria-live="polite">{toasts.map((t) => <div key={t.id} className={`toast ${t.err ? 'err' : ''}`}>{t.text}</div>)}</div>;
}

// Spec F1.7: switching accounts in the wallet signs you out of the old one.
function WalletWatch() {
  const me = useS((s) => s.me);
  const conn = useConnection();
  const config = useConfig();
  useEffect(() => {
    if (me?.kind !== 'wallet' || !me.wallet || conn.status !== 'connected' || !conn.address) return;
    const short = `${conn.address.slice(0, 6)}…${conn.address.slice(-4)}`;
    if (short.toLowerCase() !== me.wallet.toLowerCase()) {
      toast('You switched accounts in your wallet, so we signed you out. Sign in again with the new account.', true);
      walletDisconnect(config).then(signOff);
    }
  }, [conn.address, conn.status, me?.wallet]);
  return null;
}

export function App() {
  const signedIn = useS((s) => s.signedIn);
  const view = useS((s) => s.view);
  const showMembers = useS((s) => s.showMembers);
  const modal = useS((s) => s.modal);
  const me = useS((s) => s.me);
  const connected = useS((s) => s.connected);
  const ever = useS((s) => s.everConnected);
  const mobile = useMedia('(max-width: 767px)');

  useEffect(() => {
    const k = (e: KeyboardEvent) => { if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === 'k') { e.preventDefault(); document.getElementById('search')?.focus(); } };
    addEventListener('keydown', k); return () => removeEventListener('keydown', k);
  }, []);

  if (!signedIn) return <><SignIn /><Toasts /></>;
  return (
    <>
      <div className="app" data-view={view}>
        <Sidebar />
        <Main mobile={mobile} />
        {showMembers && (!mobile || view === 'chat') && <Members />}
      </div>
      {ever && !connected && <div className="conn">Reconnecting…</div>}
      <ProfileCard />
      {modal?.kind === 'arrival' && me && <ArrivalModal />}
      {modal?.kind === 'speak' && me && <SpeakModal text={modal.text} replyTo={modal.replyTo} />}
      {modal?.kind === 'profile' && me && <ProfileEditor />}
      <WalletWatch />
      <Toasts />
    </>
  );
}
