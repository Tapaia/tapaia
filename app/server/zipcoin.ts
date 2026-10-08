// Zipcoin names: read-only client for zipcoin.cash's public API (https://www.zipcoin.cash/api/v1, CORS open, no auth).
// Shapes checked against the live API on Oct 7, 2026:
//   GET /identities/:address -> { address, ens, zipName: "alice.zipcoin.cash" | null, avatar, team, door, bell }
//   GET /names/check?name=   -> { name, address, since, tx, eth, room, tier, priceZc, presetZc, price, status, priceUsd }
//        status: "available" | "released" | "taken" | "reserved" (house words) | "reserved-for" (kept for a .eth owner) | "invalid"
// This module never sends a transaction. Claims happen on zipcoin.cash from the user's own wallet.

export const ZIPCOIN_API = (process.env.ZIPCOIN_API || 'https://www.zipcoin.cash/api/v1').replace(/\/$/, '');
export const ZIPCOIN_SITE = 'https://www.zipcoin.cash';
const TTL_MS = 10 * 60_000;      // good answers (including "no name") are cached for 10 minutes
const FAIL_TTL_MS = 60_000;      // after a failure, wait a minute before asking again
const TIMEOUT_MS = 4_000;

/** zipcoin's name grammar (docs: 3 to 24 lowercase letters, digits and hyphens, no hyphen at either end). */
export const NAME_RE = /^[a-z0-9](?:[a-z0-9-]{1,22})[a-z0-9]$/;
export const isZipLabel = (s: unknown): s is string => typeof s === 'string' && NAME_RE.test(s);
export const zipDomain = (label: string) => `${label}.zipcoin.cash`;
export const shortAddress = (a: string) => `${a.slice(0, 6)}…${a.slice(-4)}`;

export interface Resolved {
  name: string | null;           // label, e.g. "alice" (null = this wallet holds no name)
  ok: boolean;                   // false = the API could not be reached / answered badly
  display: string;               // "alice.zipcoin.cash" or the short address
  at: number;
}

let fetcher: typeof fetch = (...a) => fetch(...a);
/** Test hook: swap the fetch implementation (used by scripts/test-zipcoin.ts). */
export function _setFetch(f: typeof fetch) { fetcher = f; cache.clear(); inflight.clear(); }

async function getJson(path: string): Promise<unknown> {
  const ac = new AbortController();
  const t = setTimeout(() => ac.abort(), TIMEOUT_MS);
  try {
    const r = await fetcher(`${ZIPCOIN_API}${path}`, { signal: ac.signal, headers: { accept: 'application/json', 'user-agent': 'tapaia-prototype (+https://github.com/Tapaia/tapaia)' } });
    if (!r.ok) throw new Error(`zipcoin API ${r.status}`);
    return await r.json();
  } finally { clearTimeout(t); }
}

const cache = new Map<string, Resolved>();
const inflight = new Map<string, Promise<Resolved>>();

/** Wallet address -> Zipcoin name, cached. Never throws: on failure it keeps the last good answer, else falls back to the short address. */
export function resolveZipName(address: string, opts: { force?: boolean } = {}): Promise<Resolved> {
  const key = address.toLowerCase();
  const hit = cache.get(key);
  const now = Date.now();
  if (hit && !opts.force && now - hit.at < (hit.ok ? TTL_MS : FAIL_TTL_MS)) return Promise.resolve(hit);
  const pending = inflight.get(key);
  if (pending) return pending;
  const p = (async (): Promise<Resolved> => {
    try {
      const j = await getJson(`/identities/${key}`) as { address?: unknown; zipName?: unknown };
      if (!j || typeof j !== 'object' || (typeof j.address === 'string' && j.address.toLowerCase() !== key)) throw new Error('unexpected identity shape');
      let name: string | null = null;
      if (typeof j.zipName === 'string') {
        const label = j.zipName.toLowerCase().replace(/\.zipcoin\.cash$/, '');
        if (isZipLabel(label)) name = label;
      }
      const r: Resolved = { name, ok: true, display: name ? zipDomain(name) : shortAddress(address), at: Date.now() };
      cache.set(key, r);
      return r;
    } catch {
      // stale-if-error: a name we saw recently is still the best answer we have
      const r: Resolved = hit?.ok ? { ...hit, at: Date.now() - TTL_MS + FAIL_TTL_MS } : { name: null, ok: false, display: shortAddress(address), at: Date.now() };
      cache.set(key, r);
      return r;
    } finally { inflight.delete(key); }
  })();
  inflight.set(key, p);
  return p;
}

export type NameState = 'available' | 'taken' | 'reserved' | 'invalid' | 'error';
export interface NameCheck {
  name: string;
  state: NameState;
  apiStatus?: string;            // raw status from zipcoin ("reserved-for", "released", …)
  keptFor?: string | null;       // for "reserved-for": the address the name is kept for
  holder?: string | null;        // for "taken": the holder's address
  priceZc?: number;              // burn cost today, from the API (number of ZC)
  priceUsd?: number;             // the API's own USD estimate
  tier?: string;                 // "row" | "card" | "large"
}

const checkCache = new Map<string, { at: number; v: NameCheck }>();
/** Availability + burn cost for a name, via /names/check. Cached 30 s. */
export async function checkZipName(raw: string): Promise<NameCheck> {
  const name = String(raw ?? '').trim().toLowerCase().replace(/\.zipcoin\.cash$/, '').slice(0, 40);
  if (!isZipLabel(name)) return { name, state: 'invalid' };
  const hit = checkCache.get(name);
  if (hit && Date.now() - hit.at < 30_000) return hit.v;
  try {
    const j = await getJson(`/names/check?name=${encodeURIComponent(name)}`) as Record<string, unknown>;
    const st = String(j?.status ?? '');
    const state: NameState = st === 'available' || st === 'released' ? 'available' : st === 'taken' ? 'taken'
      : st === 'reserved' || st === 'reserved-for' ? 'reserved' : st === 'invalid' ? 'invalid' : 'error';
    const num = (x: unknown) => (typeof x === 'number' && Number.isFinite(x) && x > 0 ? x : undefined);
    const v: NameCheck = {
      name, state, apiStatus: st || undefined,
      keptFor: st === 'reserved-for' && typeof j.address === 'string' ? j.address : undefined,
      holder: st === 'taken' && typeof j.address === 'string' ? j.address : undefined,
      priceZc: num(j.priceZc), priceUsd: num(j.priceUsd), tier: typeof j.tier === 'string' ? j.tier : undefined,
    };
    if (state !== 'error') checkCache.set(name, { at: Date.now(), v });
    if (checkCache.size > 500) checkCache.clear();
    return v;
  } catch {
    return { name, state: 'error' };
  }
}

/** Deep link into zipcoin.cash's own claim form, prefilled (the /names page reads ?name=). */
export const claimUrl = (label: string) => `${ZIPCOIN_SITE}/names?name=${encodeURIComponent(label)}`;
