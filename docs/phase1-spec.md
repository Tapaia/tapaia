# Tapaia Phase 1 spec: the community hub MVP

*Draft v0.1, Oct 7, 2026, for Angelo. Builds on `docs/design-doc.md` v0.3 (section 5.2 and the Phase 1 roadmap). Mockups: `design/mockups/` (PNGs in `design/mockups/png/`). Visual sources: `design/visual-reference.md`.*

**Placeholders are letters on purpose.** No amounts, counts or dates are decided yet. Anything this spec adds that the design doc doesn't already say is marked **(decision to confirm)** and collected in section 9.

---

## 1. What Phase 1 is

Tapaia Phase 1 is the place the $ZC community actually hangs out: a chat app that can replace Telegram, styled like a cozy 8-bit take on a late-90s AOL chat room. It has the normal out-of-character (OOC) community channels, plus **one in-character (IC) room, Tapaia Square**, where people can chat as their Veridian citizen. Everything else from the RPG (game systems, the Order, courts, the project token) comes in later phases.

People sign in with any major Ethereum wallet, then become a **citizen** by making an **arrival post**: free for the first X Founding Citizens, and otherwise a real zipcoin Book post that burns E ZC.

**Exit criteria (from the design doc):** the community's daily chat runs in Tapaia for a full migration period without major moderation or reliability problems.

**Ground rules carried over:**
- Nobody has to role-play. New users land on the community side.
- Original characters only; no canon characters as players or NPCs.
- We never hold anyone's keys or tokens. Every on-chain action is signed by the user's own wallet.
- Nothing in the app pays real tokens out to anyone.
- Credit and non-affiliation notice on every screen footer; the app links the exact commit it runs.

## 2. Who uses it

| Role | What they can do |
|---|---|
| **Visitor** (not signed in) | See the sign-in screen. Read #lobby and #announcements (proposed, open question Q6). |
| **Signed-in, not a citizen yet** | Read #lobby, #support, #announcements; post in #lobby and #support with tight rate limits; start the arrival flow. |
| **Citizen** | Post in all community channels and Tapaia Square; profile and avatar; DMs; notifications. |
| **Founding Citizen** | A citizen who entered through a free founder slot. Same powers, plus the badge. |
| **Moderator** | Community members with mod tools in the channels they're assigned to. |
| **Team** | Verified team handles. Post in #announcements and #dev-updates. Same moderation rules as everyone. |
| **Bot** | Read-only feeds in #feeds (and pinned items). Labeled, can't be DM'd, hold no funded wallets. |

## 3. Features, user stories and acceptance criteria

### F1. Wallet sign-in (Sign-In with Ethereum)
Mockup: `01-sign-in.png`.

**User stories**
- As a newcomer, I want to sign in with the wallet I already use (Rabby, MetaMask, Coinbase Wallet, Rainbow, Trust Wallet, or any wallet over WalletConnect) so I don't need a new account or password.
- As a phone user, I want to sign in from my mobile wallet by scanning a QR code or tapping a deep link.
- As a cautious user, I want to see exactly what I'm signing and know it costs nothing.
- As a curious reader, I want to look around (#lobby) before connecting anything.

**Acceptance criteria**
1. The wallet picker lists **Rabby, MetaMask, Coinbase Wallet, Rainbow, Trust Wallet and WalletConnect**, in a retro list box with original pixel icons (not official logos).
2. Browser-extension wallets are found with **EIP-6963** multi-wallet discovery, and the ones actually installed are tagged "Detected". Several installed wallets don't fight over `window.ethereum`. A legacy `window.ethereum` provider is still offered as "Browser wallet" if it doesn't announce itself through EIP-6963.
3. **WalletConnect v2** works for mobile and any other wallet: QR code on desktop, deep link on mobile, and session restore on reload.
4. Sign-in uses **SIWE (EIP-4361)** on Ethereum mainnet. The message shows our domain, the wallet address, a statement ("Sign in to Tapaia"), the chain, a fresh server nonce, and issued-at and expiry times. The screen says plainly: "free, no transaction, no gas."
5. The server verifies the signature, nonce (single use), domain, URI, chain and expiry before creating a session. It accepts both normal wallets and **smart-contract wallets** (EIP-1271, plus ERC-6492 for not-yet-deployed smart wallets such as Coinbase Smart Wallet).
6. The session is an httpOnly, secure, same-site cookie with an expiry; "Sign Off" ends it on the server.
7. One wallet = one account. Switching accounts in the wallet signs you out of the old one, with a clear message.
8. Errors are friendly and specific: wallet not installed (link to install), wrong network (offer to switch), signature rejected (try again), WalletConnect timeout (new QR).
9. "Just looking? #lobby" and "Help · #support" are reachable without connecting a wallet (subject to Q6).
10. The footer shows the *Snowmoon* GPL v3 credit, the non-affiliation notice, "staff never DM first and never ask for your seed phrase", and the running build commit.

*Implementation note:* wagmi + viem with RainbowKit or Reown AppKit both cover EIP-6963 and WalletConnect v2; either is fine. Server-side SIWE verification with viem's `verifySiweMessage` or the `siwe` package, using an RPC that supports EIP-1271/6492 checks.

### F2. Entry: the arrival post (becoming a citizen)
Mockup: `02-arrival.png`.

**User stories**
- As an early community member, I want to claim a free Founding Citizen slot so I can join right away and get the badge.
- As a later newcomer, I want to burn a real zipcoin Book post as my arrival message so I become a citizen, knowing exactly what it costs and that it's permanent.
- As a citizen, I want to see new arrivals greeted in Tapaia Square.
- As the team, we want a public record of how many founder slots were used and by what rule.

**Acceptance criteria: founder path**
1. While founder slots remain and the founder window (placeholder dates) is open, an eligible wallet sees the "Founding Citizen · free" tab with the slots left: **"X−n of X left"** (live count, X is a placeholder).
2. Eligibility follows the chosen anti-farming rule set (Q4): at least one slot per wallet, plus whichever of the founder window, invite codes or community allowlist, probation, or proof-of-personhood is chosen. Ineligible wallets see why, in plain words.
3. The founder writes an arrival message (same 280-byte limit as the Book, for a consistent ritual). It's stored off-chain in our database as a **free in-game arrival post**, and can be moderated like any message.
4. On submit the account becomes a citizen with the **Founding Citizen** badge. The badge can't be transferred, carries no votes, Rep or powers, and is shown on the profile and buddy list.
5. A public counter (in #announcements and the repo) shows slots used and the rule applied.

**Acceptance criteria: burn path**
6. The composer shows the message, a live byte counter (max 280 bytes), and a preview of how it will look in the Arrivals lane.
7. A burn notice is always shown before signing, and can't be dismissed: the burn amount **E ZC** with an approximate dollar value and a gas estimate (both live); "permanent and public, can't be edited or deleted"; "reposted to X by @zipcoinbook"; "publicly links this wallet to Tapaia"; "Tapaia never holds your tokens or keys"; the one real ZC address (`0x4E67DB19044549fF420860834c91b45BaD298722`).
8. Two checkboxes must be ticked (permanent and public; not refundable) before "Sign & Burn" is enabled.
9. The app reads zipcoin's current rules from `https://www.zipcoin.cash/api/v1/rules` and never lets E drop below zipcoin's live Speak minimum (currently 1,000 ZC per zipcoin's rules). If the wallet holds less than E ZC, the button is disabled and links to the correct ZC pool, never a search.
10. The user's wallet sends the Speak transaction to ZipBroadcaster directly. We never relay or custody it.
11. **Verification:** citizenship is granted only after we confirm on Ethereum RPC that the post's speaker is the account's wallet, the burn is at least E, and it was made after sign-up. The zipcoin API (`/words`, `/live`) is used to find it, never trusted alone. Pending, confirmed and failed states are shown; a dropped or replaced transaction can be retried.
12. The confirmed post appears in Tapaia Square's **Arrivals lane** with a "🔥 on-chain" marker, using the same hide-by-default rules as other Book content.
13. Entry is one-time. Nothing is re-checked later; selling ZC never removes citizenship.
14. If a pre-existing Book post can count (Q5), the flow offers "use an earlier post" with the same checks; otherwise only new posts count.

**Blocked on:** whether third-party apps can tag their Book posts (the `/words` `board` filter) so arrival posts can be told apart (V1); E (Q2); X and founder rules (Q4).

### F3. Rooms and channels
Mockup: `03-tapaia-square.png` (room list on the left).

**User stories**
- As anyone, I want a clear list of rooms, grouped into "Community" (out of character) and "Veridia" (in character), with unread counts.
- As a non-player, I want to ignore the game entirely.
- As a player, I want one room where I can talk as my citizen.

**Rooms at launch**

| Room | Layer | Who can read | Who can post | Notes |
|---|---|---|---|---|
| #announcements | OOC | Everyone (proposed) | Team only | Pinned "one true address" post for ZC. Read-only for others. |
| #general | OOC | Citizens | Citizens | Everyday talk. |
| #market | OOC | Citizens | Citizens | Price talk kept out of #general. No paid promotion, no "guaranteed" calls, no team price talk. |
| #support | OOC | Everyone signed in | Everyone signed in (rate-limited) | Pinned: staff never DM first, never ask for seed phrases. Helpers answer in public. |
| #dev-updates | OOC | Citizens | Team; replies in threads | Changelogs, repo and running-commit links. |
| #feeds | OOC | Citizens | Bots only | See F6. |
| #lobby | OOC | Everyone (proposed) | Signed-in users (rate-limited) | Read-mostly room for newcomers. Explains the arrival post. |
| **Tapaia Square** | IC | Citizens | Citizens | The town square of Meldan. In character, decimal clock. Has the Arrivals lane. |

**Acceptance criteria**
1. The sidebar has two labeled groups, "COMMUNITY · OOC" and "VERIDIA · IN CHARACTER". New citizens land in #general (non-citizens in #lobby).
2. Each room shows its unread count; @mentions show a separate marker.
3. Each room header says whether it's OOC or IC, shows the topic and a pinned item, and (IC only) shows the decimal clock.
4. Room access is enforced on the server, not just hidden in the UI.
5. A greyed "Districts, doors… later" row hints at future Veridia rooms without being clickable (decision to confirm).
6. Off-topic and language rooms can be added by admins later without a code change.

### F4. Chat
Mockup: `03-tapaia-square.png`.

**User stories**
- As a citizen, I want to send messages, @mention people, and reply to a specific message, and get them in real time.
- As a citizen, I want to see who's in the room right now, like a buddy list, and hear the classic door sounds when people come and go.
- As a player in Tapaia Square, I want it to feel in-world: citizen names, `Name → message` lines and decimal timestamps like the book's devices.
- As a citizen with something important to say, I want to "Speak to the Square" with a real burn so my message stands out.

**Acceptance criteria: messages**
1. Messages arrive in real time over WebSocket and are stored as the source of truth on the server. History loads as you scroll up.
2. Text up to a set length (placeholder L), with basic formatting (bold, italic, underline), links and emoji. Links from new accounts are limited (F7).
3. **Mentions:** typing `@` suggests people in the room; a mention highlights the line for the person mentioned and notifies them (F8).
4. **Replies:** a reply shows a small quote chip of the original ("↪ Ilse") that jumps to it when tapped.
5. Edit and delete your own messages (edits marked "edited"). Moderators can remove any message.
6. OOC rooms show handles and normal local times. IC rooms show citizen names, the book's `Name → message` format, and a 5-digit **tick timestamp** (hover or long-press shows your local time).
7. **Decimal clock:** 100 ticks per minute, 100 minutes per longhour, 10 longhours per day. Proposed: one shared "Meldan time" for everyone, with tick 00000 at midnight UTC, so "meet at 6 longhours" means the same moment for everyone (decision to confirm). How real dates map to canon months is open (Q13).

**Acceptance criteria: system lines, sounds, presence**
8. Entering or leaving a room posts a system line in AOL style ("SQUARE HOST: Juniper Vale has entered the square."). In busy rooms (over placeholder N people) these lines collapse into a periodic summary so they don't flood the chat.
9. **Sounds** (decision to confirm): a wooden door creak when someone enters, a latch click when they leave, a tea-cup clink for a mention, a low crackle for a real burn. Door sounds play only for people on your buddy list or in rooms under N people. All sounds are off by default on mobile and can be muted globally or per room.
10. **Buddy list** (right panel): people in the current room, grouped as Founding Citizens, Citizens, Team, Away, each with pixel avatar, name, badges and a presence dot (here / idle / away). Users can appear invisible.
11. Clicking a person opens their profile card (F5) with Message, Mute, Block, Report.

**Acceptance criteria: Tapaia Square specifics**
12. The room header shows the pixel Tapaia Square scene, an "IN CHARACTER" tag, and the topic.
13. The composer has two modes: **Say** (free, the default) and **Speak to the Square (burn)**.
14. Proposed for Phase 1 (decision to confirm): *Speak to the Square* is a **real zipcoin Book post** burning at least **S** ZC (placeholder, never below zipcoin's live minimum), made with the same composer, warnings, checkboxes and RPC verification as the arrival post. It shows in the room as a highlighted "SPOKE TO THE SQUARE · REAL BOOK POST" card with "verified on-chain". (The design doc's later version burns both ZC and the project token, which doesn't exist yet in Phase 1.)
15. The **Arrivals lane** shows founders' free posts and confirmed on-chain arrival posts, styled differently from normal chat.
16. Ordinary "Say" messages in the square are free. No Rep, drafts, businesses, doors or other game systems in Phase 1.

**DMs**
17. Proposed (decision to confirm): DMs use **message requests**. The recipient sees the first message as a request and accepts or declines; anyone can turn requests off. Knock-to-DM comes with the RPG. Staff and bots never DM first.

### F5. Profiles and the avatar builder
Mockup: `04-profile-builder.png`.

**User stories**
- As a citizen, I want a pixel avatar dressed the way Veridians are described in the book, and a citizen name for Tapaia Square.
- As a privacy-minded user, I want my OOC handle and citizen name kept apart unless I choose to link them.
- As anyone, I want to see someone's badges and arrival post before I DM them.

**Acceptance criteria**
1. **Avatar builder** with a live preview on a small Tapaia Square backdrop. Options from the book: outfit (privacy robe with hood down; robe with hood up and face cover with the nose strap; plain shirt; band shirt), hair style and color, skin tone, optional silk neck band. Robes come with dark purple shoes with high heels and uneven soles. Randomize, Undo, Save.
2. Avatars are original pixel art generated from layered sprite parts in the repo (`design/mockups/art/`); no uploaded images in Phase 1 (decision to confirm, it removes a big moderation load).
3. **Citizen name**: unique, checked live, with canon character names and real people's names reserved (as in the design doc's name-claims section). It's separate from the OOC handle. The OOC handle can show an ENS or `name.zipbook.eth` name via `/identities/:who` if the user has one.
4. A "link publicly" toggle controls whether the profile shows both names together. Default: not linked.
5. **Profile card** shows: avatar, citizen name, OOC handle (if linked), badges, wallet (shortened), ENS/zipbook name, citizen-since date (decimal and normal), optional home district (IC flavor text) and "about" text, the arrival post, and actions (Message, Mute, Block, Report; Knock greyed until the RPG).
6. **Badges in Phase 1:** Founding Citizen; on-chain arrival (🔥) or free founder arrival; Verified Team; Moderator; Bot.
7. **Rep** is shown as a locked stat bar ("arrives with the RPG"), not computed in Phase 1 (decision to confirm). A "profile complete" bar is the only active stat.
8. Profiles store only what's listed above. Nothing else is collected by default.

### F6. Bots (read-only)
**User stories**
- As a community member, I want ZC burns, Book posts and price updates in one place without leaving the app.
- As a skeptic, I want proof that what bots post really happened on-chain.

**Acceptance criteria**
1. **ZC live feed bot:** subscribes to `https://www.zipcoin.cash/api/v1/live` (SSE), confirms each event on Ethereum RPC, then posts notable burns and knocks to #feeds. "Notable" uses a published threshold (placeholder).
2. **Book posts bot:** new Speak posts from `/words`, posted filtered with the hide-by-default rules (placeholder thresholds), with "show anyway". Never re-broadcast outside the app.
3. **Price bot:** ZC price and pool liquidity from GeckoTerminal (DexScreener didn't index these pools per the briefing). A periodic summary (placeholder interval) plus threshold moves (placeholder %), not a constant ticker. No price commentary.
4. **Treasury bot:** built in Phase 1 but switched off until the treasury multisig exists (Phase 2), when it posts each multisig transaction and buyback with links (decision to confirm).
5. **Address guard:** any ZC-like contract address posted anywhere that isn't the published one gets flagged automatically (see F7).
6. Bots have no funded wallets and no write access to chain; their code and prompts live in the public repo.

### F7. Moderation and anti-spam
**User stories**
- As a member, I want scams, fake support and impersonators gone fast.
- As a moderator, I want a queue of reports and simple tools.

**Acceptance criteria**
1. Citizenship (arrival post or founder slot) is required to post outside #lobby and #support.
2. Per-wallet rate limits (placeholder R messages per minute), slow mode per channel, and link and mention limits for new accounts in #lobby and #support.
3. Filters for the usual Telegram problems: fake-support messages, impersonation (reserved team handles, verified-team badge, look-alike name check), wallet-drainer and phishing links (blocklist), airdrop scams, and copycat token addresses.
4. Report button on every message and profile; mod queue with context; actions: remove, warn, mute for a time, remove from a room, ban; every action logged with a reason.
5. Users can block and mute others.
6. **On-chain content:** Book posts can't be deleted, so the app can only hide them. An abusive arrival post is hidden in the app and the account's citizenship can be removed; the code of conduct says so up front.
7. One code of conduct with an OOC section (real-world rules) and an IC section (role-play rules), linked from every room header.
8. First moderators come from the community (Q11).

### F8. Notifications and mobile web
**User stories**
- As a phone user, I want Tapaia on my home screen with push notifications, like Telegram.
- As a busy person, I want quiet hours and per-room mute.

**Acceptance criteria**
1. Installable **PWA** that works on iOS and Android browsers, with a mobile layout: room list, chat and buddy list become swipeable panels; the composer stays usable with the on-screen keyboard.
2. **Web push** for mentions, replies, DMs (message requests), #announcements, and arrival confirmation. Each type can be turned off.
3. Per-room mute and a quiet-hours setting.
4. Optional email or XMTP alerts for people who opt in (which channels: Q9). Optional daily or weekly #announcements digest.
5. Pixel fonts are hard for some people: a **"readable font"** setting swaps in a plain font everywhere; text sizes have minimums; animations respect "reduce motion"; everything is keyboard-usable with visible focus.

### F9. Open source, credit and transparency
1. Public GPL v3 repo with every bit of app code, bot code, prompts, art generators and lore files.
2. Footer on every screen: *Snowmoon* credit, non-affiliation notice, "staff never DM first", and a link to the exact running commit.
3. Published: founder-slot rule and count used, E and S and how they're reviewed, bot thresholds, moderation policy.

### F10. Moving over from Telegram and X
1. A short "Moving to Tapaia" guide: connect a wallet, sign in, make your arrival post or claim a founder slot, and where each old topic now lives.
2. A migration plan for whichever community groups exist (no official ZC Telegram was found). **No outreach or posts are made until Angelo approves them.**

## 4. Look and sound
Late-90s AOL chat room, redrawn as cozy pixel art: wooden window frames with brass rivets, robe-purple title bars, parchment panels with beveled AOL edges, a toolbar on a wooden plank, room list on the left, buddy list on the right, "has entered the room" lines and door sounds. Colors and decor come from how the book describes Meldan: dark purple robes, tree-shaded stone and wood buildings, beige / light-blue / grey houses, glowing green circles (our "verify / sign" color), red for errors, and the book's navy-and-blue device panels for clocks and system info. Fonts: Press Start 2P for labels and buttons, VT323 for text (both SIL OFL, bundled locally). Full sources and palette: `design/visual-reference.md`.

## 5. Explicitly out of scope until later phases
- **Phase 2:** the project token ($TAPAIA) and its launch; treasury, buybacks and the live treasury bot; any project-token burn at entry; optional holder-gated rooms.
- **Phase 3 (the RPG):** character systems beyond name and avatar; district rooms, business rooms, doors and knocks; burn-to-be-heard with both tokens and burn-ahead credits; the in-game zc ledger, taxes and businesses; aesthetics sortition; Rep scores and Rep-gated rooms; the AI game master, NPCs and Emerald; the daily "news from Meldan" digest.
- **Phase 4:** the Order of Steering (Acolytes, Sentinels, Keepers, Heralds), secret tasks and the guess bounty; courts; polls; paid extras; the general opt-in "Post to the Book" feature outside Tapaia Square.
- **Phase 5:** mini-games (Minpentai, Helisport scoring, Nim), reputation loans, privacy upgrades, native apps.
- **Never:** paying real tokens out to players, holding user funds or keys, zip/unzip privacy pools inside the app.

## 6. Placeholders

| Letter | What it is | Decided by |
|---|---|---|
| **X** | Number of free Founding Citizen slots | Q4 |
| **E** | Entry burn in ZC (never below zipcoin's live minimum) | Q2 |
| **S** | Minimum burn for Speak to the Square in Phase 1 | Q14 |
| Founder window | Start and end dates for founder slots | Q4 |
| Eligibility rule | Which anti-farming rules apply to founder slots | Q4 |
| **L** | Max message length | build |
| **R** | Messages per minute per wallet; slow-mode seconds | build, tuned in beta |
| **N** | Room size above which enter/leave lines collapse and door sounds stop | build |
| Bot thresholds | Notable burn size, price-alert % and summary interval, Book hide-by-default rules | Q10 |

## 7. Open questions that block Phase 1
Carried over from the design doc (numbers in brackets are its section 13):
- **Q2. Entry burn E [2].** Zipcoin's minimum, our own fixed ZC amount with a published review rule, or a dollar value via a price oracle? Dollar amount undecided.
- **Q4. Founder slots [4].** How many (X), the founder window, and which anti-farming rules.
- **Q5. Arrival-post rules [5].** Can a pre-existing Book post count? What happens to citizenship if an arrival post is abusive? What guidance do we give for what to write?
- **Q6. Open areas [6].** Which rooms can be read or used before entering (proposed: #lobby, #support, #announcements).
- **Q7. Gate before the token exists [16].** Proposed: founder slots plus a ZC-only arrival post. Alternatives: fully open at first, or delay the hub.
- **Q8. Telegram migration [17].** Which groups, how long the pointer period lasts, whether to mirror announcements, and who does outreach.
- **Q9. Mobile [18].** PWA first (proposed) or native early; which extra alert channels.
- **Q10. Bots [20].** Which feeds at launch and the alert thresholds.
- **Q11. #market rules and first moderators [19].**
- **Q12. License flavor [23].** GPL-3.0 everywhere or AGPL-3.0 for the server; which moderation lists, if any, stay private.

Things to verify before building:
- **V1.** Can a third-party app tag its Book posts (the `/words` `board` filter) so arrival posts can be told apart? If not, a fallback is to require a short marker in the post text (e.g. a "#tapaia" tag), which costs bytes and can be copied (decision to confirm if needed).
- **V2.** Can `@zipcoin/agent` build unsigned Speak transactions for a browser wallet? If not, call the MIT-licensed ZipBroadcaster contract directly with viem.
- **V3.** Test the arrival flow end to end on a mainnet fork before launch.

New questions from this spec:
- **Q13.** How do real dates map to the book's months? The book lists 11 month names and doesn't give the full calendar.
- **Q14.** Speak to the Square in Phase 1: keep it as a real Book post burning at least S ZC (proposed), or hide it until the RPG phase?

## 8. Suggested build order
1. Sign-in (F1) and the room/chat core (F3, F4 without Speak) behind an invite, for the team.
2. Founder path (F2 founder), profiles and avatar builder (F5), moderation basics (F7).
3. Burn path and verification (F2 burn) on a mainnet fork, then mainnet with small amounts.
4. Bots (F6), PWA and push (F8), then Speak to the Square if kept (Q14).
5. Migration guide and a public beta (F10), once Angelo approves outreach.

## 9. Design decisions in this spec (please confirm)
1. **Tapaia Square ships in Phase 1** as a free in-character chat room with the Arrivals lane. No other game systems until Phase 3.
2. **Speak to the Square in Phase 1 = a real zipcoin Book post** (ZC only, at least S), reusing the arrival-post flow (Q14).
3. **One shared Meldan clock** with tick 00000 at midnight UTC, so everyone sees the same tick time.
4. **Founders write their free arrival post with the same 280-byte limit** as Book posts.
5. **DMs use message requests** (accept or decline) until knocks arrive with the RPG.
6. **Rep is shown as locked**, not computed, in Phase 1.
7. **Avatars are built only from our pixel parts**; no image uploads in Phase 1.
8. **Treasury bot is built but stays off** until the multisig exists in Phase 2.
9. **AOL sounds:** door creak on enter, latch click on leave, cup clink on mention, crackle on burn; off by default on mobile.
10. **A "readable font" setting** alongside the pixel fonts, for accessibility.
11. **A greyed "Districts, doors… later" row** in the room list to hint at the RPG.
