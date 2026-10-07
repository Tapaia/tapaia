<img src="../design/logo/opt4-refined/D-hybrid/D-hybrid-256.png" alt="Tapaia logo" width="96" height="96">

# Tapaia Phase 1 hub: working prototype

A clickable prototype of the Phase 1 community hub from [`docs/phase1-spec.md`](../docs/phase1-spec.md), built to look like the v2 mockups in [`design/mockups-v2/`](../design/mockups-v2/). Modern chat layout, Inter, the book palette, light and dark themes, and pixel art only as accents. The art and fonts are copied from `design/mockups-v2/` at build time, and the official logo (favicon, app icons, sidebar and sign-in) from `design/logo/opt4-refined/D-hybrid/`. Avatars are drawn live from the same sprite maps as `design/mockups/art/sprites.py` (ported to `shared/avatar.ts`, pixel-identical to the mockup PNGs).

**This is a prototype. It never sends a transaction and nothing touches real ZC.** All burns (arrival post, Speak to the Square) are simulated and labelled as such.

## Run it

Needs Node 20.19+ (or 22+).

```bash
cd app
npm install
npm run build && npm start          # one server: http://localhost:4417
# or for development with hot reload (Vite on :5173, API on :4417):
npm run dev
```

`./scripts/serve.sh` builds and starts the server in the background (logs in `app/server.log`).

Optional environment variables:

| Variable | What it does |
|---|---|
| `PORT` | Server port (default `4417`). Hosts like Render set this for you. |
| `LISTEN_HOST` | Interface to bind (default `0.0.0.0`, all interfaces). |
| `WALLETCONNECT_PROJECT_ID` | Turns on WalletConnect (QR / phone wallets). Without it, browser-extension wallets (EIP-6963) and Coinbase Wallet still work, and the WalletConnect row says it isn't configured. Get an id at cloud.reown.com. |
| `ETH_RPC_URL` | RPC used only to verify smart-contract wallet signatures (EIP-1271 / ERC-6492). Default: a public mainnet RPC. |
| `FOUNDER_SLOTS` | Demo value for X, the number of Founding Citizen slots (default 100; the real X isn't decided). |

Data lives in memory and is snapshotted to `server/data/db.json` (git-ignored). Delete that file to reset to the seed.

### Verify

```bash
npm run verify            # or: node scripts/verify.mjs http://localhost:4417
```

Runs headless Chrome (`playwright-core` + the system Chrome/Chromium) through: demo sign-in, both entry paths, live chat between two browsers, mentions, replies, reactions, Speak, theme toggle and persistence, read-only rooms, #feeds, DMs, the mobile layout, and a real SIWE sign-in against a mock EIP-6963 wallet (throwaway key, no funds). Screenshots go to `screenshots/`.

## Deploy

The prototype is one Node process (Express + `ws`) that serves the built client and the WebSocket chat on the same port, so it needs a host that keeps a server running. Vercel/Netlify serverless functions won't work.

**Render (free, no Docker):** [`render.yaml`](../render.yaml) at the repo root is a Blueprint for a free web service.

1. Open <https://render.com/deploy?repo=https://github.com/Tapaia/tapaia> and sign in with GitHub.
2. Give the Blueprint a name, check that it shows one free web service called `tapaia`, and click **Deploy Blueprint**.
3. When the build finishes, open the `https://tapaia-….onrender.com` URL shown on the service page.

It builds with `cd app && npm ci --include=dev && npm run build` and starts with `cd app && npm start`, on Node 22. The service runs from the repo root, not `app/`, because the build copies art from `design/`. The health check is `/api/health`. No environment variables are required. To turn on WalletConnect, add `WALLETCONNECT_PROJECT_ID` in the service's **Environment** tab, and add the onrender.com domain to the project's allowed domains at cloud.reown.com.

Free-tier caveats: the service sleeps after 15 minutes without traffic, and the first visit after that takes about a minute to wake it. Chat, accounts and sessions live in memory with a snapshot on local disk, which is wiped on every restart, redeploy or spin-down, so the town resets to the seed each time.

Any host that runs a long-lived Node process with WebSockets works the same way (Fly.io, Railway, a VPS): build with `npm ci --include=dev && npm run build` in `app/`, start with `npm start`, and let it read `PORT`.

## What works

- **Sign-in.** A big **Try the demo** button (no wallet: pick or reroll a fictional citizen, then do the arrival flow or skip to the Square). Real **Sign-In with Ethereum** (EIP-4361) with wagmi + viem: EIP-6963 discovery tags installed wallets (Rabby, MetaMask, Coinbase Wallet, Rainbow, Trust and any other) as "Detected", with a legacy `window.ethereum` fallback, the Coinbase Wallet SDK, and WalletConnect when a project id is set. The server checks the single-use nonce, domain, URI, chain, expiry and signature (EOA locally, smart wallets over RPC), then sets an httpOnly SameSite session cookie. Switching accounts in the wallet signs you out. "Browse #lobby" lets you look around without signing in.
- **Entry.** Founder path: a free in-game arrival post with the Founding Citizen badge and a live slot counter. Burn path: the full burn notice, byte counter, preview, two required checkboxes and a step-by-step **simulated** signing ("DEMO: nothing is burned"). Arrivals show up as cards in Tapaia Square, plus a "just became a citizen" line in #general.
- **Rooms.** #announcements (read-only, team only), #general, #market, #support, #dev-updates (team posts), #feeds (bots only), #lobby, and **Tapaia Square** (in character) with the pixel banner and the live Meldan tick clock (100 ticks a minute, 100 minutes a longhour, 10 longhours a day, 00000 at midnight UTC). Access is enforced on the server: non-citizens can read #lobby, #support and #announcements and post in #lobby and #support. Visitors can read #lobby and #announcements.
- **Chat.** Live over WebSockets. Say/Speak toggle in the Square (Speak is simulated, with the burn notice and checkboxes). Arrival and Speak cards, "has entered / left the square" lines, @mention autocomplete with highlights and an @ marker in the room list, replies with quote chips that jump to the original, reactions, edit and delete your own messages, typing indicators, unread markers, pinned notices, and a member list with presence (here, idle, offline) and badges. Basic DMs.
- **Seed and bots.** The fictional citizens from the mockups with their seed messages. The **ZC Price Bot** posts real price, 24h change, liquidity and volume from GeckoTerminal's public API every 30 minutes (it posts nothing if the API fails). The **Book Feed Bot** posts SAMPLE Book posts, clearly labelled. Seeded citizens chat now and then, wander in and out of the Square, and answer DMs and @mentions. All of that is simulated, and their profile cards say so.
- **Profile.** Pixel avatar builder (outfit, hair colour, hair style, skin, shirt colour, silk neck band; randomize and undo), citizen name and handle, a "link names publicly" toggle, and a locked Rep stat. Theme setting: System (default), Light or Dark, saved in the browser. Profile cards include Message, plus Mute, Block and Report (stubbed) and a greyed-out Knock.
- **Mobile.** Below 768px the app becomes a room list and chat screens like the phone mockups, with a slide-over member list and a full-screen arrival flow and profile.

## What's stubbed or left out

- No real burns or transactions of any kind. The Speak/arrival transaction, the on-chain verification and the zipcoin `/rules`, `/words` and `/live` integration are not built yet. The Book feed is sample data.
- The values E, S, X, the founder window and the eligibility rules are placeholders. In the demo every account can claim a founder slot (100 demo slots).
- DMs don't use message requests yet. Mute, block, report, the moderation queue, slow mode, link filters and the address guard are stubs or missing. There's a simple rate limit (8 messages per 10 seconds).
- No push notifications, PWA install, sounds, history paging (each room keeps its last 400 messages), attachments, threads or search beyond filtering the room list.
- ENS / zipbook names aren't looked up.

## Layout

```
app/
  server/       Node + Express + ws: auth (demo + SIWE), rooms, chat, bots, JSON snapshot store
  shared/       types, room access rules, Meldan clock, pixel avatar renderer (shared by client and server)
  src/          React + Vite client (components/, styles/app.css = the v2 design system)
  scripts/      copy-assets, serve.sh, verify.mjs
  screenshots/  output of npm run verify
```

GPL-3.0, like the rest of the repo. Based on *Snowmoon* by Vitalik Buterin. Not affiliated with Vitalik Buterin, zipcoin.cash or Stockereum. Our only X account is [@TapaiaSquare](https://x.com/TapaiaSquare).
