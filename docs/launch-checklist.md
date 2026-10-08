# Tapaia launch checklist

*Oct 7, 2026, for Angelo. It goes with [design-doc.md](design-doc.md) v0.7.*

**The goal:** a **full product at token launch**, not a bare prototype. $TAPAIA launches on Stockereum only once the launch scope below is live (design doc section 12, v0.7 note).

**Effort scale:**
- **S** = a few days;
- **M** = one to two weeks;
- **L** = three weeks or more.

These estimates assume one developer working with agents, and they are rough.

**How the "built" list was checked.** It comes from the committed code on `main` at `6603b80` (`app/server`, `app/src`, `app/shared`), the checks in `app/scripts/verify.mjs`, and `app/README.md`. It is not from memory. The last full local verify run, at `85b201c` (the Zipcoin names commit), passed 48/48.

**Live site status.** `https://tapaia.onrender.com/api/health` reported build **`60c2782`** at 9:51 PM ET on Oct 7. The live site is therefore behind `main`: Zipcoin names and the new wording are not deployed until a Render deploy of the latest commit.

---

## 1. Built today (in the prototype)

Each item below is exercised by `verify.mjs` unless it is marked otherwise.

| Area | What works | Notes |
|---|---|---|
| **Sign-in** | Demo sign-in with no wallet, plus real Sign-In with Ethereum (EIP-4361). <br>• Wallets: EIP-6963 wallet discovery ("Detected"), Coinbase Wallet SDK, and WalletConnect when `WALLETCONNECT_PROJECT_ID` is set. <br>• Server checks: single-use nonce, domain, URI, chain, expiry and signature (EOAs locally; EIP-1271 / ERC-6492 smart wallets over RPC). <br>• Session: httpOnly cookie. | verify uses a mock wallet with a throwaway key and checks that **no transaction methods** are ever requested. |
| **Entry** | Founder path: free in-game arrival post, Founding Citizen badge, slot counter. <br>Burn path: the full burn notice, preview and two checkboxes, with a **simulated** signing labelled "DEMO: nothing is burned". | No real burn yet, and the founder anti-farming rules aren't built. |
| **Rooms and access** | #announcements, #general, #market, #support, #dev-updates, #feeds, #lobby and Tapaia Square (in character, with the live Meldan tick clock). Access rules are enforced on the server (`shared/perms.ts`). | |
| **Chat** | Live WebSocket chat: mentions with autocomplete, replies with quote chips, reactions, edit and delete, typing indicators, unread markers, pins, a member list with presence, and basic DMs. <br>The Square has a Say/Speak toggle; Speak is **simulated**. | There's a simple rate limit (8 messages per 10 s). Each room keeps its last 400 messages. |
| **Bots** | ZC Price Bot with real GeckoTerminal data every 30 min. Book Feed Bot with **sample** data, labelled. Simulated chatter from the seed citizens. | No live zipcoin `/live` or `/words` feed yet. |
| **Profile** | Pixel avatar builder (16×24 sprites), citizen name and handle, "link names" toggle, locked Rep stat, and a theme setting (system, light or dark). | Mute, Block and Report are stubs; Knock is greyed out. |
| **Zipcoin names** | Name lookup at sign-in (`/identities`, cached 10 min, falls back to the short address). The verified name and seal show everywhere names appear. "Get a Zipcoin name" panel: availability states and burn cost from the API, and a deep link to zipcoin.cash's claim page. Demo accounts get a labelled simulated claim. | Tapaia never sends the claim transaction (by design for now). |
| **Mobile** | Below 768 px: a room list and chat screens, a slide-over member list, and full-screen arrival and profile screens. | Not an installable PWA yet, and no push notifications. |
| **Open source** | GPL v3 repo, credit and non-affiliation footer, a link to the running commit, and Render Blueprint (`render.yaml`). | `PIPELINE.md` / `PROMPTS.md` aren't needed until the AI features ship. |
| **Characters (study, not yet in the app)** | Cozy HD pixel citizens: 32×48 sprites, native busts, a 12-citizen sheet, builder parts, the HD Square scene and a before/after comparison (`design/characters/`, commits `236ac29` and `6603b80`). | **App integration is in progress** in a separate task. Uncommitted `app/` changes exist; see section 2. |

**Not built at all yet:**
- Societies, QV polls, knocks and doors;
- the in-game zc ledger, businesses, the aesthetics draft and Rep;
- AI (the game master, NPCs, Emerald);
- the Order and courts;
- the moderation queue, slow mode, link filters and the wrong-address guard;
- push notifications, PWA install, search, attachments, threads and history paging;
- persistent storage;
- all ten v0.7 features (design doc 5.4).

---

## 2. Still needed for a full launch

### 2.1 Platform and operations
- [ ] **Persistent storage (L, critical).** On Render's free plan, chat, accounts and sessions live in memory with a snapshot on local disk, which is wiped on every restart, redeploy or spin-down. The free service also sleeps after 15 minutes. Needed:
  - Postgres (managed) as the source of truth (design doc 9.2);
  - a migration from the JSON store;
  - daily backups.
- [ ] **Always-on paid hosting (S).** A paid Render instance or equivalent, with WebSockets, a custom domain if wanted, and health checks.
- [ ] **Auto-deploy from GitHub (S).** Link Render to the repo so `main` deploys on push. Today it's manual.
- [ ] **Chat completeness (M):**
  - history paging beyond 400 messages per room;
  - search;
  - image attachments, if wanted;
  - DM message requests (knock-first, design doc 5.1).
- [ ] **Notifications (M).** An installable PWA, web push for mentions, replies, DMs, class reminders and the food truck, per-channel mute and quiet hours.
- [ ] **Monitoring (S).** Error logging, uptime alerts and basic metrics.
- [ ] **Load and security review (M).** WebSocket load test, rate limits per wallet and IP, auth and session review, dependency audit.

### 2.2 Moderation and safety (M, launch-critical)
- [ ] A real report queue and mod tools: delete, mute, timeout, ban, and remove citizenship.
- [ ] Working mute and block for users.
- [ ] Slow mode. The 5.4.1 Air panel's "ventilation" builds on this.
- [ ] Filters:
  - link and new-account limits in #lobby and #support;
  - scam-link and drainer filters;
  - a **wrong-address guard** that flags any contract address other than the published ones;
  - impersonation checks on team handles (reserved words exist today).
- [ ] A code of conduct (OOC and IC sections), terms and a privacy note.
- [ ] Hood-up abuse handling (5.4.3) and moderation of the arrival lane.

### 2.3 Real on-chain flows (no simulation at launch)
- [ ] **Real arrival burn (M).** A ZipBroadcaster Speak from the user's wallet, verified on RPC before citizenship is granted. Three open items block it:
  - the **Book minimum vs ~$5 entry** decision;
  - whether third-party apps can **tag Book posts**;
  - the entry-routing ON HOLD option (design doc 6.2, 6.2.7, open decisions 2 and 2a).
- [ ] **Real Speak to the Square (S–M)**, using the chosen burn model: per action, or burn-ahead credits (open decision 8).
- [ ] **$TAPAIA half of entry and Speak (S, after the token exists).** The address is hardcoded and links to the correct Stockereum page.
- [ ] **Founder slot rules (S).** One per wallet, the founder window, and the allowlist or probation rules (open decision 3).
- [ ] **Live zipcoin feed (S).** `/live` SSE and `/words` into #feeds, confirmed on RPC, replacing the sample Book bot.
- [ ] **Zipcoin names claim flow.**
  - **Today:** a deep link to zipcoin.cash, which is enough for launch.
  - **Optional (M):** an in-app non-custodial claim (approve, then `speak(..., "/claim name")`), then a re-check through `/identities`.
  - Add ENS display alongside.
- [ ] **Mainnet-fork testing (S)** of every burn flow (`anvil --fork-url`), then small mainnet tests.
- [ ] **Treasury (S).** A dedicated wallet, a published address and a treasury feed bot (design doc 7.5).

### 2.4 Community features
- [ ] **Societies (M).** Create a Society, set entry rules (hold, burn, invite, founders), add Society rooms and mods, plus an optional creation cost and shops (design doc 5.3). Several rules are still open (open decision 16).
- [ ] **QV polls (M).** Multi-item ballots, reach, decoys, results posted to the square, and Society-internal polls (design doc 4.1).
  - Payout currency is undecided (open decision 14; in-game first is recommended).
  - Proposed lore fix P1 (don't pay voters) is pending.

### 2.5 Veridia layer needed by the launch features
- [ ] **In-game zc ledger + season stipend + sales tax (M).** Needed for food-truck and tea orders and for businesses.
- [ ] **Character creation, citizen vs visitor (S–M).**
- [ ] **Aesthetics draft + QV normalizer + verifiable sortition (M).** Needed for billboards, later for buildings and shops (design doc 4.1, 9.5).
- [ ] **Rep v1 with a published formula (M).** Needed for Rep-gated rooms and Hood-up's Rep credential.
- [ ] **AI service (M).** Labelled NPCs (robot server, Hydrafill), Emerald basics, library quizzes, and a published `PROMPTS.md` per GPL (design doc 8, 10).

### 2.6 The ten v0.7 features (design doc 5.4)
- [ ] 5.4.1 Room "Air" panel: **S**
- [ ] 5.4.2 Fix Tapaia (Coordination Score, milestones, assembly): **M**
- [ ] 5.4.3 Hood-up anonymous posts: **M**
- [ ] 5.4.4 Dzego food truck + robot tea server: **S** (needs the ledger)
- [ ] 5.4.5 Trust list: **S**
- [ ] 5.4.6 Library shelf + Herald books: **S** (quizzes need AI)
- [ ] 5.4.7 Pop-up classes: **S** (reminders need push)
- [ ] 5.4.8 Inspector clubs: **S**
- [ ] 5.4.9 Sortition-rated billboards: **M** (needs the aesthetics draft)
- [ ] 5.4.10 Reputation-only forecasting board: **M**

### 2.7 Characters
- [ ] **Integrate the Cozy HD pixel characters (M, in progress).** This covers:
  - 32×48 sprites and native busts in chat, the member list, profiles and the arrival card;
  - the new avatar builder parts;
  - the HD Square banner with live citizens;
  - Fix Tapaia's before/after scenes (design/characters/README.md, integration plan).

### 2.8 Legal, docs and launch prep
- [ ] **Legal consult (M, calendar time)** on entry burns, founder slots, paid extras, buyback-and-burn, poll payouts and geo restrictions (design doc 11, open decision 27).
- [ ] **Clean up old placeholders.** `docs/phase1-spec.md` and `app/README.md` still use old placeholders, and `$ZC` remains in old mockups.
- [ ] **Name collision check** before the token launches (Stockereum graduations API, GeckoTerminal, X).
- [ ] **Copycat plan.** One true address everywhere, plus the bot guard.
- [ ] **Telegram/X migration guide** and pinned pointers (any outreach needs Angelo's approval).
- [ ] **Decide the pending items:**
  - proposed lore fixes P1–P6 (design doc 13);
  - USD-to-token pricing (6.2.4);
  - launch scope (open decision 28);
  - hosting budget (open decision 30).

---

## 3. Suggested build order

Phases run in order, though work inside a phase can run in parallel. Totals are rough calendar estimates for one developer working with agents.

| Phase | What | Rough effort |
|---|---|---|
| **A. Foundations** | • Postgres persistence + backups <br>• Paid always-on hosting + auto-deploy <br>• Moderation core (report queue, mute/block, slow mode, filters, wrong-address guard) <br>• Finish the character integration <br>• Air panel (5.4.1), since it rides on slow mode | **3–4 weeks** |
| **B. Real entry and identity** | • Settle the Book-minimum and tagging questions <br>• Real arrival burn + RPC verification on a mainnet fork, then mainnet <br>• Founder slot rules <br>• Real Speak (chosen burn model) <br>• Live zipcoin feed <br>• ENS display <br>• Trust list (5.4.5) | **2–3 weeks** |
| **C. Community core** | • Societies <br>• QV polls (in-game rewards unless decided otherwise) <br>• PWA + push <br>• Library (5.4.6) <br>• Pop-up classes (5.4.7) <br>• Inspector clubs (5.4.8) <br>• Hood-up (5.4.3) <br>• History paging and search | **3–4 weeks** |
| **D. Veridia layer + novel features** | • In-game zc ledger <br>• Character creation <br>• Food truck + robot tea (5.4.4) <br>• Aesthetics draft + verifiable sortition <br>• Billboards (5.4.9) <br>• Rep v1 <br>• Forecasting board (5.4.10) <br>• Fix Tapaia (5.4.2) with the HD scenes <br>• AI service for NPCs and quizzes, plus `PROMPTS.md` | **4–6 weeks** |
| **E. Launch hardening → token** | • Legal consult sign-off <br>• Security and load review <br>• Treasury wallet + bot <br>• Placeholder cleanup <br>• Name collision check <br>• Final verify on production <br>• Then the Stockereum launch (paired against ZC, 1%) and switching entry to the ZC + $TAPAIA split | **1–2 weeks** (the legal review runs in parallel from Phase A) |
| **After launch (seasons 1–2)** | • The Order (Acolytes 3×3, Sentinels, Keepers, Heralds, guess bounty) <br>• Courts <br>• Knocks and doors <br>• Businesses with audits <br>• Minpentai, Helisport, Nim <br>• Reputation loans <br>• Optional in-app Zipcoin name claim | ongoing |

**Total to token launch:** roughly **13–19 weeks**. That shrinks if Phase D is trimmed, or if some 5.4 features move to "after launch" (open decision 28).

## 4. Biggest blockers

1. **Persistent storage and paid hosting.** Nothing survives a restart today, so no real community can live on the current deployment.
2. **Real entry is blocked on undecided rules.** These are the Book minimum vs ~$5 entry, whether apps can tag Book posts, burn-per-action vs credits, USD-to-token pricing, and the founder anti-farming rules.
3. **Legal consult.** The token design, burns and any poll payouts need it before launch, and it takes calendar time.
4. **Moderation tooling** has to exist before opening to the public. This matters most for anonymous Hood-up posts, permanent on-chain arrival posts, and a scam-heavy crypto audience.
5. **Prerequisite systems.** The in-game zc ledger, the aesthetics draft, Rep v1 and the AI service each unlock several launch features, so they sit on the critical path.
6. **Scope vs time.** A full product is about 3–5 months of work. Decide early what is "launch" and what is "season 1" (open decision 28).
