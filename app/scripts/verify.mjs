// End-to-end check with headless Chrome (playwright-core). Usage: node scripts/verify.mjs [baseUrl]
// Saves screenshots to app/screenshots/.
import { chromium } from 'playwright-core';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { generatePrivateKey, privateKeyToAccount } from 'viem/accounts';

const BASE = process.argv[2] || 'http://localhost:4417';
const OUT = path.join(path.dirname(fileURLToPath(import.meta.url)), '..', 'screenshots');
fs.mkdirSync(OUT, { recursive: true });
const exe = process.env.CHROME || ['/usr/bin/google-chrome', '/usr/bin/chromium', '/usr/bin/chromium-browser'].find((p) => fs.existsSync(p));
const browser = await chromium.launch({ executablePath: exe, headless: true });
const results = [];
const ok = (name, pass, extra = '') => { results.push({ name, pass }); console.log(`${pass ? 'PASS' : 'FAIL'}  ${name}${extra ? '  ' + extra : ''}`); };
const errors = [];
const shot = (page, name) => page.screenshot({ path: path.join(OUT, name) });

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
  await D.exposeFunction('__mockSign', async (msg) => acct.signMessage({ message: msg }));
  await D.exposeFunction('__mockLog', (m) => { calls.push(m); });
  await D.addInitScript(({ address }) => {
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
  await D.goto(BASE);
  await D.getByTestId('wallet-rabby').waitFor();
  await D.waitForTimeout(500);
  ok('EIP-6963 wallet is tagged "Detected"', await D.getByTestId('wallet-rabby').locator('.pill.ok').isVisible());
  await D.getByTestId('wallet-rabby').click();
  const siwe = await D.getByTestId('arrival-text').waitFor({ timeout: 15000 }).then(() => true).catch(() => false);
  ok('wallet sign-in via SIWE (mock EIP-6963 wallet) creates a session', siwe, `wallet ${acct.address.slice(0, 6)}…`);
  ok('no transaction methods were requested from the wallet', !calls.some((m) => /sendTransaction|signTransaction|eth_sign$|signTypedData/.test(m)), [...new Set(calls)].join(','));
  if (siwe) { await D.locator('.modal .x').click(); await D.waitForTimeout(300); await shot(D, '17-wallet-signed-in.png'); }
} catch (e) {
  ok('script ran without exceptions', false, e.message);
}
await browser.close();
if (errors.length) { console.log('\nBrowser errors:'); for (const e of [...new Set(errors)]) console.log('  ' + e); }
const failed = results.filter((r) => !r.pass).length;
console.log(`\n${results.length - failed}/${results.length} checks passed`);
process.exit(failed ? 1 : 0);
