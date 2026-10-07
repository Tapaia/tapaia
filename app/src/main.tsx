import { createRoot } from 'react-dom/client';
import { WagmiProvider } from 'wagmi';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import './styles/app.css';
import './styles/screens.css';
import { App } from './App';
import { api, enterApp, refreshConfig } from './store';
import { makeWagmi } from './wallet';
import type { PublicUser } from '../shared/types';

async function boot() {
  const cfg = await refreshConfig().catch(() => null);
  const wagmi = makeWagmi(cfg?.walletConnectProjectId ?? null);
  const qc = new QueryClient();
  const { me } = await api<{ me: PublicUser | null }>('/api/me').catch(() => ({ me: null }));
  if (me) enterApp(me, { channel: sessionStorage.getItem('tapaia-active') ?? undefined });
  else if (sessionStorage.getItem('tapaia-entered')) enterApp(null, { channel: 'lobby' });
  createRoot(document.getElementById('root')!).render(
    <WagmiProvider config={wagmi} reconnectOnMount={false}>
      <QueryClientProvider client={qc}><App /></QueryClientProvider>
    </WagmiProvider>,
  );
}
boot();
