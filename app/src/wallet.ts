// Real wallet sign-in: wagmi + viem, EIP-6963 discovery, Coinbase Wallet SDK, WalletConnect (optional), SIWE (EIP-4361).
// This prototype never sends a transaction: the only wallet request besides connecting is personal_sign of the SIWE message.
import { createConfig, http, type Config, type Connector } from 'wagmi';
import { mainnet } from 'wagmi/chains';
import { coinbaseWallet, injected, walletConnect } from 'wagmi/connectors';
import { connect, signMessage, switchChain, disconnect } from 'wagmi/actions';
import { createSiweMessage } from 'viem/siwe';
import { getAddress } from 'viem';
import type { PublicUser } from '../shared/types';
import { api } from './store';

export function makeWagmi(projectId: string | null): Config {
  const meta = { name: 'Tapaia', description: 'The town square for the $ZC community', url: location.origin, icons: [`${location.origin}/assets/icon-tea.png`] };
  const connectors = [
    injected({ shimDisconnect: true }), // legacy window.ethereum ("Browser wallet")
    coinbaseWallet({ appName: 'Tapaia', appLogoUrl: meta.icons[0] }),
    ...(projectId ? [walletConnect({ projectId, showQrModal: true, metadata: meta })] : []),
  ];
  return createConfig({ chains: [mainnet], connectors, transports: { [mainnet.id]: http() }, multiInjectedProviderDiscovery: true, ssr: false });
}

export interface KnownWallet { key: string; name: string; rdns: string[]; install: string }
export const KNOWN: KnownWallet[] = [
  { key: 'rabby', name: 'Rabby', rdns: ['io.rabby'], install: 'https://rabby.io' },
  { key: 'metamask', name: 'MetaMask', rdns: ['io.metamask', 'io.metamask.flask', 'io.metamask.mobile'], install: 'https://metamask.io/download/' },
  { key: 'coinbase', name: 'Coinbase Wallet', rdns: ['com.coinbase.wallet'], install: 'https://www.coinbase.com/wallet' },
  { key: 'rainbow', name: 'Rainbow', rdns: ['me.rainbow'], install: 'https://rainbow.me/download' },
  { key: 'trust', name: 'Trust Wallet', rdns: ['com.trustwallet.app'], install: 'https://trustwallet.com/download' },
];

/** EIP-6963 connectors announced by installed extensions (wagmi gives them type "injected" and id = rdns). */
export const isDiscovered = (c: Connector) => c.type === 'injected' && c.id !== 'injected';

export function friendlyError(e: unknown): string {
  const err = e as { name?: string; shortMessage?: string; message?: string; code?: number };
  const msg = `${err?.name ?? ''} ${err?.shortMessage ?? ''} ${err?.message ?? ''}`;
  if (/UserRejected|rejected|denied|cancel/i.test(msg) || err?.code === 4001) return 'You rejected the request in your wallet. Try again when you’re ready.';
  if (/ProviderNotFound|not found|not installed/i.test(msg)) return 'That wallet isn’t installed in this browser.';
  if (/timeout|expired/i.test(msg)) return 'The request timed out. Please try again.';
  return err?.shortMessage || err?.message || 'Wallet sign-in failed.';
}

export async function signInWithWallet(config: Config, connector: Connector): Promise<PublicUser> {
  let address: `0x${string}`;
  try {
    const res = await connect(config, { connector });
    address = getAddress(res.accounts[0]);
    if (res.chainId !== mainnet.id) await switchChain(config, { chainId: mainnet.id }).catch(() => { /* signing works on any chain */ });
  } catch (e) {
    if ((e as Error).name === 'ConnectorAlreadyConnectedError') address = getAddress((await connector.getAccounts())[0]);
    else throw e;
  }
  const { nonce } = await api<{ nonce: string }>('/api/siwe/nonce');
  const message = createSiweMessage({
    domain: location.host, address, uri: location.origin, version: '1', chainId: mainnet.id, nonce,
    statement: 'Sign in to Tapaia. This is free: no transaction, no gas.',
    issuedAt: new Date(), expirationTime: new Date(Date.now() + 10 * 60_000),
  });
  const signature = await signMessage(config, { message, account: address, connector });
  const { me } = await api<{ me: PublicUser }>('/api/siwe/verify', { message, signature });
  return me;
}

export const walletDisconnect = (config: Config) => disconnect(config).catch(() => {});
