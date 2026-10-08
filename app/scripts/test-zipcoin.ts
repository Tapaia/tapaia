// Unit checks for the Zipcoin name resolver (server/zipcoin.ts) with a mocked fetch: no network, no transactions.
// Run: npx tsx scripts/test-zipcoin.ts   (verify.mjs runs it too). Prints PASS/FAIL lines.
import { _setFetch, resolveZipName, checkZipName, isZipLabel } from '../server/zipcoin';

let fails = 0;
const ok = (name: string, pass: boolean, extra = '') => { if (!pass) fails++; console.log(`${pass ? 'PASS' : 'FAIL'}  ${name}${extra ? '  ' + extra : ''}`); };
const A = '0x1111111111111111111111111111111111111111';
const B = '0x2222222222222222222222222222222222222222';
let calls = 0;
let down = false;
const json = (body: unknown, status = 200) => new Response(JSON.stringify(body), { status, headers: { 'content-type': 'application/json' } });
_setFetch((async (input: RequestInfo | URL) => {
  calls++;
  if (down) throw new Error('ECONNREFUSED');
  const url = String(input);
  // shapes copied from the live API (Oct 7, 2026)
  if (url.endsWith(`/identities/${A}`)) return json({ address: A, ens: null, zipName: 'alice.zipcoin.cash', avatar: null, team: null, door: null, bell: ['mail'] });
  if (url.endsWith(`/identities/${B}`)) return json({ address: B, ens: null, zipName: null, avatar: null, team: null, door: null, bell: ['mail'] });
  const m = /names\/check\?name=([^&]+)/.exec(url);
  if (m) {
    const n = decodeURIComponent(m[1]);
    const status = n === 'alice' ? 'taken' : n === 'admin' ? 'reserved' : n === 'vitalik' ? 'reserved-for' : 'available';
    return json({ name: n, address: status === 'taken' ? A : null, since: null, tx: null, eth: null, room: 1000, tier: n.length === 4 ? 'card' : 'row', priceZc: n.length === 4 ? 10000 : 1000, presetZc: 1000, price: {}, status, priceUsd: 18.17 });
  }
  return json({ error: 'not found' }, 404);
}) as typeof fetch);

const a1 = await resolveZipName(A);
ok('resolver: wallet with a mocked name resolves to it', a1.ok && a1.name === 'alice' && a1.display === 'alice.zipcoin.cash');
const before = calls;
await resolveZipName(A.toUpperCase().replace('0X', '0x'));
ok('resolver: answers are cached (10 min, case-insensitive)', calls === before);
const b1 = await resolveZipName(B);
ok('resolver: wallet without a name falls back to the short address', b1.ok && b1.name === null && b1.display === '0x2222…2222');
down = true;
const a2 = await resolveZipName(A, { force: true });
ok('resolver: API down keeps the last good name (stale-if-error)', a2.name === 'alice' && a2.ok);
const C = '0x3333333333333333333333333333333333333333';
const c1 = await resolveZipName(C);
ok('resolver: API down with no history -> short address, ok=false, no throw', !c1.ok && c1.name === null && c1.display === '0x3333…3333');
down = false;
ok('name grammar: 3–24 lowercase letters/digits/hyphens, no edge hyphens', isZipLabel('abc') && isZipLabel('a-b') && !isZipLabel('zz') && !isZipLabel('-ab') && !isZipLabel('ab-') && !isZipLabel('x_y') && !isZipLabel('Alice') && !isZipLabel('a'.repeat(25)));
const st = await Promise.all(['alice', 'admin', 'vitalik', 'newname', 'zz'].map((n) => checkZipName(n)));
ok('check: taken / reserved / reserved-for / available / invalid map to UI states', st.map((x) => x.state).join(',') === 'taken,reserved,reserved,available,invalid', st.map((x) => x.state).join(','));
ok('check: burn cost comes from the API (priceZc), not invented', st[3].priceZc === 1000 && (await checkZipName('abcd')).priceZc === 10000);
down = true;
ok('check: API down -> "error" state, no throw', (await checkZipName('another')).state === 'error');
process.exit(fails ? 1 : 0);
