// End-to-end check with headless Chrome (playwright-core). Usage: node scripts/verify.mjs [baseUrl]
// Saves screenshots to app/screenshots/.
import { chromium } from 'playwright-core';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { generatePrivateKey, privateKeyToAccount } from 'viem/accounts';
import http from 'node:http';
import net from 'node:net';
import os from 'node:os';
import { spawn, spawnSync } from 'node:child_process';

const BASE = process.argv[2] || 'http://localhost:4417';
const OUT = path.join(path.dirname(fileURLToPath(import.meta.url)), '..', 'screenshots');
fs.mkdirSync(OUT, { recursive: true });
const exe = process.env.CHROME || ['/usr/bin/google-chrome', '/usr/bin/chromium', '/usr/bin/chromium-browser'].find((p) => fs.existsSync(p));
const browser = await chromium.launch({ executablePath: exe, headless: true });
const results = [];
const ok = (name, pass, extra = '') => { results.push({ name, pass }); console.log(`${pass ? 'PASS' : 'FAIL'}  ${name}${extra ? '  ' + extra : ''}`); };
const errors = [];
const shot = (page, name) => page.screenshot({ path: path.join(OUT, name) });
const APP = path.join(path.dirname(fileURLToPath(import.meta.url)), '..');
const TX_METHODS = /sendTransaction|signTransaction|eth_sign$|signTypedData|sendCalls|wallet_send/;

// Mock EIP-6963 wallet ("Rabby", throwaway key, no funds). It can only sign the SIWE text; anything else throws and is logged.
async function mockWallet(page, acct, calls) {
  await page.exposeFunction('__mockSign', async (msg) => acct.signMessage({ message: msg }));
  await page.exposeFunction('__mockLog', (m) => { calls.push(m); });
  await page.addInitScript(({ address }) => {
    const listeners = {};
    const provider = {
      isRabby: true,
      request: async ({ method, params }) => {
        window.__mockLog(method);
        if (method === 'eth_requestAccounts' || method === 'eth_accounts') return [address];
        if (method === 'eth_chainId') return '0x1';
        if (method === 'net_version') return '1';
        if (method === 'wallet_switchEthereumChain') return null;
        if (method === 'wallet_requestPermissions' || method === 'wallet_getPermissions') return [{ parentCapability: 'eth_accounts' }];
        if (method === 'personal_sign') { const hex = params[0]; const txt = new TextDecoder().decode(new Uint8Array(hex.slice(2).match(/../g).map((b) => parseInt(b, 16)))); return window.__mockSign(txt); }
        throw Object.assign(new Error('mock wallet: unsupported ' + method), { code: 4200 });
      },
      on: (e, f) => { (listeners[e] ||= []).push(f); }, removeListener: () => {},
    };
    const info = { uuid: '6d2b5c1e-0000-4000-8000-000000000001', name: 'Rabby Wallet', icon: 'data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22/>', rdns: 'io.rabby' };
    const announce = () => window.dispatchEvent(new CustomEvent('eip6963:announceProvider', { detail: Object.freeze({ info, provider }) }));
    window.addEventListener('eip6963:requestProvider', announce);
    announce();
  }, { address: acct.address });
}
async function walletSignIn(page, base) {
  await page.goto(base);
  await page.getByTestId('wallet-rabby').waitFor();
  await page.waitForTimeout(300);
  await page.getByTestId('wallet-rabby').click();
  return page.getByTestId('arrival-text').waitFor({ timeout: 15000 }).then(() => true).catch(() => false);
}
const freePort = () => new Promise((res) => { const s = net.createServer(); s.listen(0, '127.0.0.1', () => { const p = s.address().port; s.close(() => res(p)); }); });

// A second, throwaway instance of this checkout whose zipcoin API is a local mock (same response shapes as
// https://www.zipcoin.cash/api/v1 on Oct 7, 2026). Lets us test "wallet that owns a name" end to end without real names.
async function mockedInstance(names) {
  if (!fs.existsSync(path.join(APP, 'dist', 'index.html'))) return null;
  const mock = http.createServer((req, res) => {
    const u = new URL(req.url, 'http://x');
    const send = (code, body) => { res.writeHead(code, { 'content-type': 'application/json' }); res.end(JSON.stringify(body)); };
    let m;
    if ((m = /^\/identities\/(0x[0-9a-f]{40})$/i.exec(u.pathname))) {
      const a = m[1].toLowerCase();
      return send(200, { address: a, ens: null, zipName: names[a] ? `${names[a]}.zipcoin.cash` : null, avatar: null, team: null, door: null, bell: ['mail'] });
    }
    if (u.pathname === '/names/check') {
      const n = (u.searchParams.get('name') || '').toLowerCase();
      if (n === 'boom') return send(500, { error: 'mock outage' });
      const status = n === 'takenname' ? 'taken' : n === 'admin' ? 'reserved' : n === 'vitalik' ? 'reserved-for' : 'available';
      const tier = n.length === 3 ? 'large' : n.length === 4 ? 'card' : 'row';
      return send(200, { name: n, address: status === 'taken' ? '0x326efe00066fcd8e480d08a7b5fb60952467809d' : null, since: null, tx: null, eth: null, room: 1000, tier, priceZc: tier === 'large' ? 100000 : tier === 'card' ? 10000 : 1000, presetZc: 1000, price: { 3: 100000, 4: 10000, otherwise: 1000 }, status, priceUsd: tier === 'row' ? 18.17 : tier === 'card' ? 181.7 : 1817 });
    }
    return send(404, { error: 'not found' });
  });
  const mport = await freePort();
  await new Promise((r) => mock.listen(mport, '127.0.0.1', r));
  const port = await freePort();
  const dataDir = fs.mkdtempSync(path.join(os.tmpdir(), 'tapaia-verify-'));
  const tsx = path.join(APP, 'node_modules', '.bin', 'tsx');
  const proc = spawn(tsx, ['server/index.ts'], { cwd: APP, stdio: 'ignore', env: { ...process.env, NODE_ENV: 'production', PORT: String(port), LISTEN_HOST: '127.0.0.1', ZIPCOIN_API: `http://127.0.0.1:${mport}`, TAPAIA_DATA_DIR: dataDir } });
  const base = `http://127.0.0.1:${port}`;
  for (let i = 0; i < 60; i++) { if (await fetch(`${base}/api/health`).then((r) => r.ok).catch(() => false)) break; await new Promise((r) => setTimeout(r, 300)); }
  return { base, stop: () => { proc.kill(); mock.close(); fs.rmSync(dataDir, { recursive: true, force: true }); } };
}

async function ctx(opts) {
  const c = await browser.newContext(opts);
  const p = await c.newPage();
  p.on('pageerror', (e) => errors.push(`${opts.label}: ${e.message}`));
  p.on('console', (m) => { if (m.type() === 'error' && !/WebSocket|favicon|Failed to load resource/.test(m.text())) errors.push(`${opts.label}: ${m.text()}`); });
  return p;
}
async function demo(page, { skip }) {
  await page.goto(BASE);
  await page.getByTestId('try-demo').click();
  await page.waitForFunction(() => (document.querySelector('#dn')?.value || '').length > 1);
  const name = await page.locator('#dn').inputValue();
  const handle = await page.locator('#dh').inputValue();
  await page.getByTestId(skip ? 'demo-skip' : 'demo-start').click();
  return { name, handle };
}

try {
  // ---- A: desktop, light
  const A = await ctx({ label: 'A', viewport: { width: 1440, height: 900 }, colorScheme: 'light' });
  await A.goto(BASE);
  await A.getByTestId('try-demo').waitFor();
  await A.waitForTimeout(400);
  await shot(A, '01-sign-in.png');
  {
    const title = await A.title();
    const hero = await A.locator('.hero h1').innerText();
    const desc = await A.locator('meta[name="description"]').getAttribute('content');
    ok('page title and hero lead with the place, name Zipcoin, no "$ZC" ticker',
      title.includes('A town square in Veridia') && /town square\s+in Veridia/.test(hero) && /Zipcoin/.test(desc || '') && !/\$ZC/.test(title + hero + desc + await A.locator('body').innerText()), title);
  }
  await A.getByTestId('try-demo').click();
  await A.waitForFunction(() => (document.querySelector('#dn')?.value || '').length > 1);
  await A.waitForTimeout(300);
  await shot(A, '02-demo-dialog.png');
  const aName = await A.locator('#dn').inputValue();
  const aHandle = await A.locator('#dh').inputValue();
  await A.getByTestId('demo-start').click();
  await A.getByTestId('arrival-text').waitFor();
  ok('demo sign-in (no wallet) opens the arrival flow', true, `${aName} @${aHandle}`);
  await A.getByTestId('path-burn').click();
  await A.getByTestId('arrival-text').fill('Hello Tapaia! Herb grower from Kalimar, here for the tea and the talk.');
  await A.locator('.chk').first().click();
  await A.waitForTimeout(200);
  await shot(A, '03-arrival-burn.png');
  ok('burn path shows the "DEMO: nothing is burned" label', await A.getByTestId('demo-flag').isVisible());
  ok('Sign & burn stays disabled until both boxes are ticked', await A.getByTestId('sign-burn').isDisabled());
  await A.getByTestId('path-founder').click();
  await A.getByTestId('claim-founder').click();
  await A.getByTestId('walk-in').waitFor();
  await A.waitForTimeout(200);
  await shot(A, '04-arrival-welcome.png');
  await A.getByTestId('walk-in').click();
  await A.locator('.card-arrival', { hasText: aName }).first().waitFor();
  ok('founder arrival card appears in Tapaia Square', true);
  ok('Meldan tick clock is shown', /\d{5}/.test(await A.getByTestId('clock').innerText()));

  // ---- B: desktop, dark system preference
  const B = await ctx({ label: 'B', viewport: { width: 1440, height: 900 }, colorScheme: 'dark' });
  const b = await demo(B, { skip: true });
  await B.getByTestId('composer').waitFor();
  ok('theme defaults to system preference (dark)', (await B.evaluate(() => document.documentElement.dataset.theme)) === 'dark');

  const msg = `Hello from A, live test ${Date.now() % 100000}`;
  await A.getByTestId('composer').fill(msg);
  await A.getByTestId('composer').press('Enter');
  const seen = await B.getByText(msg).first().waitFor({ timeout: 8000 }).then(() => true).catch(() => false);
  ok('message sent in context A appears live in context B', seen);
  // mention + reply from B
  await B.getByText(msg).first().hover();
  await B.locator('.msg', { hasText: msg }).locator('.toolbar button[aria-label="Reply"]').click();
  await B.getByTestId('composer').fill(`@${aName.split(' ')[0]}`);
  await B.waitForSelector('.suggest button');
  await B.getByTestId('composer').press('Enter');
  await B.getByTestId('composer').type('welcome to the square!');
  await B.getByTestId('composer').press('Enter');
  const mention = await A.locator('.msg.mention', { hasText: 'welcome to the square!' }).waitFor({ timeout: 8000 }).then(() => true).catch(() => false);
  ok('@mention autocomplete + reply arrive highlighted for the mentioned user', mention);
  ok('reply quote chip shown', await A.locator('.replyline', { hasText: 'Hello from A' }).count() > 0);
  // reaction from A shows in B
  await A.locator('.msg', { hasText: 'welcome to the square!' }).hover();
  await A.locator('.msg', { hasText: 'welcome to the square!' }).locator('.toolbar button[aria-label="React 🍵"]').click();
  ok('reaction syncs live', await B.locator('.msg', { hasText: 'welcome to the square!' }).locator('.react', { hasText: '🍵' }).waitFor({ timeout: 5000 }).then(() => true).catch(() => false));
  ok('enter line for B shown to A', await A.locator('.sysline', { hasText: b.name }).first().waitFor({ timeout: 5000 }).then(() => true).catch(() => false));
  await A.mouse.move(700, 300);
  await A.waitForTimeout(400);
  await shot(A, '05-square-light.png');

  // speak (simulated)
  await A.getByTestId('mode-speak').click();
  await A.getByTestId('composer').fill('Herb swap at the tea cart at 6 longhours. Bring cuttings!');
  await A.getByTestId('send').click();
  await A.getByTestId('speak-confirm').waitFor();
  await A.locator('.modal .chk').nth(0).click();
  await A.locator('.modal .chk').nth(1).click();
  await shot(A, '06-speak-confirm.png');
  await A.getByTestId('speak-confirm').click();
  ok('Speak (simulated) posts a Speak card seen live by B', await B.locator('.card-speak', { hasText: 'Bring cuttings!' }).waitFor({ timeout: 8000 }).then(() => true).catch(() => false));

  // theme toggle + persistence
  const t0 = await A.evaluate(() => document.documentElement.dataset.theme);
  await A.getByTestId('theme-toggle').click();
  const t1 = await A.evaluate(() => document.documentElement.dataset.theme);
  await A.reload();
  await A.getByTestId('composer').waitFor();
  const t2 = await A.evaluate(() => document.documentElement.dataset.theme);
  ok('theme toggle switches and persists across reload', t0 === 'light' && t1 === 'dark' && t2 === 'dark', `${t0}→${t1}→(reload) ${t2}`);
  await A.getByTestId('ch-general').click();
  await A.waitForTimeout(500);
  await shot(A, '07-general-dark.png');
  await A.getByTestId('ch-announcements').click();
  ok('#announcements is read-only for non-team', await A.locator('.blocked', { hasText: 'read-only' }).isVisible());
  await A.getByTestId('ch-feeds').click();
  await A.waitForTimeout(400);
  await shot(A, '08-feeds-dark.png');
  ok('#feeds has a ZC price bot post', await A.locator('.msg', { hasText: 'Source: GeckoTerminal' }).count() > 0);

  // DM with a seeded citizen -> simulated auto-reply
  await A.getByTestId('ch-general').click();
  await A.locator('.mem', { hasText: 'brightmoss' }).first().click();
  await A.getByTestId('dm-btn').click();
  await A.locator('.topbar .title', { hasText: 'brightmoss' }).waitFor();
  await A.getByTestId('composer').fill('Hi! Quick question about founder slots.');
  await A.getByTestId('composer').press('Enter');
  ok('DM opens and a seeded citizen replies (simulated)', await A.locator('.feed .msg .who', { hasText: 'brightmoss' }).nth(0).waitFor({ timeout: 9000 }).then(() => true).catch(() => false));

  // profile + avatar picker
  await A.getByTestId('me-card').click();
  await A.getByTestId('outfit-hood').click();
  await A.waitForTimeout(200);
  await shot(A, '09-profile-dark.png');
  await A.getByTestId('theme-light').click();
  await A.getByTestId('outfit-robe').click();
  await A.waitForTimeout(200);
  await shot(A, '10-profile-light.png');
  await A.getByTestId('save-citizen').click();
  await A.waitForTimeout(300);

  // ---- C: mobile
  const C = await ctx({ label: 'C', viewport: { width: 390, height: 844 }, deviceScaleFactor: 2, isMobile: true, hasTouch: true, colorScheme: 'light' });
  await C.goto(BASE);
  await C.getByTestId('try-demo').waitFor();
  await C.waitForTimeout(300);
  await shot(C, '11-mobile-sign-in.png');
  await demo(C, { skip: true });
  await C.getByTestId('composer').waitFor();
  await C.waitForTimeout(500);
  await shot(C, '12-mobile-square.png');
  const noHScroll = await C.evaluate(() => document.documentElement.scrollWidth <= innerWidth + 1);
  ok('mobile: Tapaia Square fits the screen (no horizontal scroll)', noHScroll);
  ok('mobile: desktop sidebar hidden in chat view', !(await C.locator('.side').isVisible()));
  await C.getByTestId('composer').fill('Saving the bench by the maple');
  await C.getByTestId('send').click();
  ok('mobile: message sent appears live in desktop context A', await A.getByText('Saving the bench by the maple').first().waitFor({ timeout: 8000 }).then(() => true).catch(() => false) || await B.getByText('Saving the bench by the maple').first().waitFor({ timeout: 3000 }).then(() => true).catch(() => false));
  await C.getByTestId('members-m').click();
  await C.waitForTimeout(300);
  await shot(C, '13-mobile-members.png');
  await C.locator('.members .x').click();
  await C.getByTestId('back').click();
  await C.waitForTimeout(300);
  await shot(C, '14-mobile-rooms.png');
  ok('mobile: back shows the room list', await C.locator('.side').isVisible());
  await C.getByTestId('me-card').click();
  await C.waitForTimeout(300);
  await shot(C, '15-mobile-profile.png');
  await C.getByTestId('profile-close').click();
  await C.getByTestId('theme-toggle-side').click();
  await C.getByTestId('ch-general').click();
  await C.waitForTimeout(400);
  await shot(C, '16-mobile-general-dark.png');

  // ---- D: real SIWE flow against a mock EIP-6963 wallet ("Rabby", throwaway key, no funds, signs only the SIWE text)
  const D = await ctx({ label: 'D', viewport: { width: 1280, height: 860 }, colorScheme: 'light' });
  const acct = privateKeyToAccount(generatePrivateKey());
  const calls = [];
  await mockWallet(D, acct, calls);
  await D.goto(BASE);
  await D.getByTestId('wallet-rabby').waitFor();
  await D.waitForTimeout(500);
  ok('EIP-6963 wallet is tagged "Detected"', await D.getByTestId('wallet-rabby').locator('.pill.ok').isVisible());
  await D.getByTestId('wallet-rabby').click();
  const siwe = await D.getByTestId('arrival-text').waitFor({ timeout: 15000 }).then(() => true).catch(() => false);
  ok('wallet sign-in via SIWE (mock EIP-6963 wallet) creates a session', siwe, `wallet ${acct.address.slice(0, 6)}…`);
  ok('no transaction methods were requested from the wallet', !calls.some((m) => TX_METHODS.test(m)), [...new Set(calls)].join(','));
  if (siwe) { await D.locator('.modal .x').click(); await D.waitForTimeout(300); await shot(D, '17-wallet-signed-in.png'); }
  if (siwe) {
    const noName = await D.evaluate(() => fetch('/api/me').then((r) => r.json()));
    ok('zipcoin: wallet without a name falls back to the short address', !noName.me.zip && /^0x[0-9a-fA-F]{4}…[0-9a-fA-F]{4}$/.test(noName.me.wallet) && await D.locator('.me .zipb').count() === 0, noName.me.wallet);
  }

  // ---- Zipcoin names against the target, using the real zipcoin.cash API through our server
  const live = await fetch('https://www.zipcoin.cash/api/v1/names').then((r) => r.json()).catch(() => null);
  const holder = live?.names?.find((n) => /^0x[0-9a-f]{40}$/i.test(n.address || ''));
  if (holder) {
    const [ours, theirs] = await Promise.all([
      fetch(`${BASE}/api/zipcoin/identity/${holder.address}`).then((r) => r.json()).catch(() => ({})),
      fetch(`https://www.zipcoin.cash/api/v1/identities/${holder.address}`).then((r) => r.json()).catch(() => ({})),
    ]);
    ok('zipcoin: server resolver matches zipcoin.cash /identities for a real holder', ours.ok === true && !!ours.domain && ours.domain === theirs.zipName, `${ours.short} → ${ours.domain}`);
  } else ok('zipcoin: server resolver matches zipcoin.cash /identities for a real holder', false, 'zipcoin.cash /names unreachable');
  const chk = await fetch(`${BASE}/api/zipcoin/check?name=admin`).then((r) => r.json()).catch(() => ({}));
  ok('zipcoin: availability proxy reads live zipcoin.cash (admin → reserved, cost from the API)', chk.state === 'reserved' && typeof chk.priceZc === 'number', `${chk.state}, ${chk.priceZc} ZC`);
  await B.getByTestId('ch-square').click().catch(() => {});
  await B.waitForTimeout(400);
  const wrenBadge = B.locator('.zipb.demo[data-name="wrenh"]').first();
  ok('zipcoin: seeded demo names show a DEMO badge, not a verified one', await wrenBadge.count() > 0 && /^Demo Zipcoin name: wrenh\.zipcoin\.cash \(demo data, not a real/.test(await wrenBadge.getAttribute('title') || '') && await B.locator('.zipb:not(.demo)[data-name="wrenh"]').count() === 0);
  await B.getByTestId('me-card').click();
  await B.getByTestId('zip-panel').waitFor();
  await B.getByTestId('zip-input').fill('zz');
  ok('zipcoin: demo profile has the "Get a Zipcoin name" panel labelled DEMO, invalid names flagged', (await B.getByTestId('zip-panel').getAttribute('data-mode')) === 'demo' && /DEMO: nothing is burned/.test(await B.getByTestId('zip-demo-flag').innerText()) && (await B.getByTestId('zip-state').getAttribute('data-state')) === 'invalid');
  await B.getByTestId('profile-close').click();

  // ---- Zipcoin names end to end on a throwaway instance with a mocked zipcoin API (no real names, no network to zipcoin)
  const named = privateKeyToAccount(generatePrivateKey());
  const plain = privateKeyToAccount(generatePrivateKey());
  const inst = await mockedInstance({ [named.address.toLowerCase()]: 'verifyname' });
  if (!inst) ok('zipcoin: mocked-API instance started', false, 'run `npm run build` first');
  else try {
    const E = await ctx({ label: 'E', viewport: { width: 1280, height: 860 }, colorScheme: 'light' });
    const eCalls = [];
    await mockWallet(E, named, eCalls);
    const eIn = await walletSignIn(E, inst.base);
    const eMe = await E.evaluate(() => fetch('/api/me').then((r) => r.json()));
    ok('zipcoin: SIWE wallet that owns a (mocked) name gets it as handle + verified badge data', eIn && eMe.me?.handle === 'verifyname' && eMe.me?.zip?.name === 'verifyname' && !eMe.me?.zip?.demo, `@${eMe.me?.handle}`);
    await E.locator('.modal .x').click();
    await E.getByTestId('composer').fill('Hello from a wallet with a Zipcoin name');
    await E.getByTestId('composer').press('Enter');
    const row = E.locator('.msg', { hasText: 'Hello from a wallet with a Zipcoin name' }).first();
    await row.waitFor({ timeout: 8000 });
    const badge = row.locator('.meta .zipb');
    ok('zipcoin: message row shows the name (not 0x…) and the verified badge with tooltip', (await row.locator('.who').innerText()) === 'verifyname' && (await badge.getAttribute('title')) === 'Verified Zipcoin name: verifyname.zipcoin.cash' && !/0x[0-9a-f]{4}/i.test(await row.innerText()));
    await E.mouse.move(5, 5);
    const bb = await row.boundingBox();
    if (bb) await E.screenshot({ path: path.join(OUT, '18-zipcoin-name-message.png'), clip: { x: Math.max(0, bb.x - 16), y: Math.max(0, bb.y - 14), width: Math.min(760, bb.width + 32), height: bb.height + 28 } });
    ok('zipcoin: member list shows the name with the badge', await E.locator('.members .mem', { hasText: 'verifyname' }).locator('.zipb').count() > 0);
    await E.getByTestId('me-card').click();
    await E.getByTestId('zip-panel').waitFor();
    ok('zipcoin: profile shows the held name and locks the handle to it', (await E.getByTestId('zip-panel').getAttribute('data-mode')) === 'held' && /verifyname\.zipcoin\.cash/.test(await E.getByTestId('zip-held').innerText()) && await E.getByTestId('handle-locked').isVisible());
    await E.getByTestId('profile-close').click();

    // F: a second wallet, no name -> short-address fallback, and the claim panel's states
    const F = await ctx({ label: 'F', viewport: { width: 1280, height: 900 }, colorScheme: 'light' });
    const fCalls = [];
    await mockWallet(F, plain, fCalls);
    await walletSignIn(F, inst.base);
    await F.locator('.modal .x').click();
    await F.getByTestId('composer').fill('@verifyn');
    const sug = F.locator('.suggest button', { hasText: 'verifyname' });
    ok('zipcoin: @mention autocomplete shows the name, badge and domain', await sug.waitFor({ timeout: 5000 }).then(() => true).catch(() => false) && await sug.locator('.zipb').count() > 0 && /verifyname\.zipcoin\.cash/.test(await sug.innerText()));
    await F.getByTestId('composer').fill('');
    await F.locator('.mem', { hasText: 'verifyname' }).first().click();
    ok('zipcoin: profile card shows the verified Zipcoin name', /verifyname\.zipcoin\.cash/.test(await F.getByTestId('pcard-zip').innerText()));
    await F.locator('.pcard-dim').click({ position: { x: 5, y: 5 } });
    await F.getByTestId('me-card').click();
    await F.getByTestId('zip-panel').waitFor();
    const states = {};
    for (const [n, want] of [['zz', 'invalid'], ['-bad-', 'invalid'], ['takenname', 'taken'], ['admin', 'reserved'], ['vitalik', 'reserved'], ['boom', 'error'], ['freshname', 'available']]) {
      await F.getByTestId('zip-input').fill(n);
      await F.waitForFunction((w) => document.querySelector('[data-testid="zip-state"]')?.getAttribute('data-state') === w, want, { timeout: 6000 }).catch(() => {});
      states[n] = await F.getByTestId('zip-state').getAttribute('data-state');
    }
    ok('zipcoin: availability states render (available / taken / reserved / invalid / error)', Object.entries({ zz: 'invalid', '-bad-': 'invalid', takenname: 'taken', admin: 'reserved', vitalik: 'reserved', boom: 'error', freshname: 'available' }).every(([k, v]) => states[k] === v), JSON.stringify(states));
    const cost = await F.getByTestId('zip-cost').innerText();
    const href = await F.getByTestId('zip-claim').getAttribute('href');
    ok('zipcoin: burn cost comes from the API and claim deep-links to zipcoin.cash', /1,000 ZC/.test(cost) && href === 'https://www.zipcoin.cash/names?name=freshname', `${cost} · ${href}`);
    await F.waitForTimeout(200);
    await F.getByTestId('zip-panel').scrollIntoViewIfNeeded();
    await F.getByTestId('zip-panel').screenshot({ path: path.join(OUT, '19-zipcoin-name-panel.png') });
    await shot(F, '20-zipcoin-profile-wallet.png');
    ok('zipcoin: no transaction methods were requested by either wallet', ![...eCalls, ...fCalls].some((m) => TX_METHODS.test(m)), [...new Set([...eCalls, ...fCalls])].join(','));

    // G: demo account -> simulated claim, clearly labelled
    const G = await ctx({ label: 'G', viewport: { width: 1280, height: 900 }, colorScheme: 'light' });
    await G.goto(inst.base);
    await G.getByTestId('try-demo').click();
    await G.waitForFunction(() => (document.querySelector('#dn')?.value || '').length > 1);
    await G.getByTestId('demo-skip').click();
    await G.getByTestId('composer').waitFor();
    await G.getByTestId('me-card').click();
    await G.getByTestId('zip-input').fill('demoname');
    await G.waitForFunction(() => document.querySelector('[data-testid="zip-state"]')?.getAttribute('data-state') === 'available', null, { timeout: 6000 }).catch(() => {});
    await G.getByTestId('zip-demo-claim').click();
    const held = await G.getByTestId('zip-panel').and(G.locator('[data-mode="demo-held"]')).waitFor({ timeout: 5000 }).then(() => true).catch(() => false);
    const gMe = await G.evaluate(() => fetch('/api/me').then((r) => r.json()));
    ok('zipcoin: demo "Simulate claim" gives a DEMO name (labelled, nothing burned)', held && gMe.me?.zip?.name === 'demoname' && gMe.me?.zip?.demo === true && /DEMO: nothing was burned/.test(await G.getByTestId('zip-panel').innerText()));
  } finally { inst.stop(); }

  // resolver unit checks (mocked fetch)
  const unit = spawnSync(path.join(APP, 'node_modules', '.bin', 'tsx'), ['scripts/test-zipcoin.ts'], { cwd: APP, encoding: 'utf8' });
  for (const line of (unit.stdout || '').split('\n')) { const m = /^(PASS|FAIL)  (.*)$/.exec(line); if (m) ok(`zipcoin unit: ${m[2]}`, m[1] === 'PASS'); }
  if (unit.status !== 0 && !/FAIL/.test(unit.stdout || '')) ok('zipcoin unit checks ran', false, unit.stderr?.slice(0, 200));
} catch (e) {
  ok('script ran without exceptions', false, e.message);
}
await browser.close();
if (errors.length) { console.log('\nBrowser errors:'); for (const e of [...new Set(errors)]) console.log('  ' + e); }
const failed = results.filter((r) => !r.pass).length;
console.log(`\n${results.length - failed}/${results.length} checks passed`);
process.exit(failed ? 1 : 0);
