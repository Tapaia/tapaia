# Veridian Chat: project design doc

*Working title. Draft v0.3, Oct 7, 2026, for Angelo. Not published. v0.3 replaces hold-to-enter as the main entry gate with Angelo's new entry model, **current direction, for now**: new citizens burn a real zipcoin Book post ("Speak") as their permanent arrival message, and the first X citizens get in free as Founding Citizens (section 6.2). Hold-to-enter is kept only as an optional, secondary tool for specific gated rooms (6.2.6). Sections 1, 5, 6, 7, 9, 11, 12 and 13 are updated to match; everything else is unchanged from v0.2. v0.2 added the community-hub positioning (section 5.2) and replaces v0.1's token recommendations with Angelo's new direction (sections 6, 7, 11–13). The tokenomics are a **placeholder: best current option, not final**.*

Sources: `/workspace/snowmoon/briefing.md` (lore, checked against the novel text in `/workspace/snowmoon/text/`) and `/workspace/zipcoin/briefing.md` (ZC and Stockereum). Chapter numbers in brackets, like [ch1], point to the novel. Market and on-chain figures are snapshots from Oct 7, 2026, around 4:45 PM ET, and will change. Anything marked **(design choice)** is ours, not canon.

---

## 1. Pitch

Veridian Chat is two things in one app: a **community chat that can replace Telegram** for the $ZC / Snowmoon community, and a **chat-based role-play game** set in everyday Veridia, the country in Vitalik Buterin's novel *Snowmoon*, layered on top of it. The community side is ordinary out-of-character chat: announcements, general talk, market talk, support and dev updates, with notifications, mobile access and bot feeds (section 5.2). The game side lets players who want it create original citizens of Meldan. They run small businesses, get randomly drafted to rate buildings, sit on five-judge courts, and can join the Order of Steering, whose members audit businesses and vote on tax rubrics under secret assignments, numbered pseudonyms and a standing bounty for anyone who guesses their task. The game is built on the novel's institutions rather than its plot: sortition, quadratic votes, split deliberation rooms, reputation-gated spaces and burning zipcoin as a costly signal. Nobody has to role-play to use the community chat, and the game never gets in the way of normal conversation.

Entry and signaling use real tokens. To become a citizen, you **burn a real on-chain "Speak" post** on the zipcoin Book (minimum 1,000 ZC per zipcoin's rules): your permanent, public arrival message. The first X citizens (number not set yet) get in free as **Founding Citizens**, with a badge and a free in-game arrival post, so everyone goes through the same arrival ritual. How much the entry burn should be in dollar terms is still open (section 6.2; **current direction, for now**). Holding tokens is no longer the main gate; it may still be used for a few specific gated rooms. Certain loud actions (town-square broadcasts, knocks, running for Keeper) cost **small burns** of both. The project token launches on Stockereum, paired against ZC (sections 6 and 7; the tokenomics are a placeholder). The in-game economy itself (taxes, salaries, bounties, court stakes, polls) runs on non-redeemable in-game zipcoin (zc).

## 2. Ground rules from Angelo's decisions

- **Everyday life only.** No war, no pre-war or post-war framing, no battles, no military or Kungaupei plots. The Arctic Empire exists in canon, but it stays offstage and has no playable or NPC role.
- **Original characters only.** No canon characters as players or NPCs: no Gladias, Seila, Mov, Delwart, Zei, Evelor, Verdow and so on. Canon *institutions, places, brands and devices* are fair game: Meldan, Kalimar, Tapaia Square, Silverchat, Hydrafill, GPH, privacy robes, neck bands, Emerald, green circles.
- **Don't invent canon.** Wherever the game needs a rule the book doesn't give, the doc labels it **(design choice)**. The in-game codex should label it the same way.
- **In-world clock.** Chat timestamps use the canon decimal time: 100 ticks per minute, 100 minutes per longhour, 10 longhours per day, so a day is 100,000 ticks (e.g. "60259"). Dates use canon months (Snowmoon, Rainmoon, … Frostime). The in-world year is left unspecified so it doesn't tie play to the novel's war timeline **(design choice)**.

## 3. Core loop

A typical session:

1. **Arrive.** Log in with a wallet (SIWE). The first time, you become a citizen by making your arrival post: a real zipcoin Book post, or a free in-game one if you have a founder slot (section 6.2). After that, you land in Tapaia Square, the town-square broadcast channel. Your Emerald assistant (the canon local-AI helper) gives you your day: a sortition draft, an audit to do, a court summons, a knock at your door, or nothing at all.
2. **Do civic duty when drafted.** Rate a building or storefront on −5..+5, judge a dispute, answer a poll. Drafts are random and short, and they are the main way new players meet each other.
3. **Live your life.** Run or visit businesses (a tea shop, a band, a Helisport club, a bookshop), talk in rooms, knock on doors, post to the square.
4. **Get steered, not banned.** Businesses and homes pay in-game taxes set by rubrics, and players change those rubrics through the Order. Players react by changing what they build and do. Canon line: "very few things are strictly banned… But what Veridia does have is intricate systems of taxes and subsidies" [ch1].
5. **Earn reputation.** Good-faith participation (accurate audits, serving as a judge, hosting assemblies, ratings from peers) raises your Rep score. Rep unlocks rooms and roles.
6. **Seasons.** Every few real weeks is one in-game "year" **(design choice; length is an open decision)**. At each season change, Keeper terms roll over (7 new Keepers per rubric), Heralds are drawn, and rubric votes resolve.

What the loop is not: there's no grinding for currency and no pay-to-win. Real tokens (section 6) are for entry and for signaling; they never buy votes, audit outcomes, court rulings, Rep or seats.

## 4. Player roles and progression

Everyone starts as a **citizen**. The other roles layer on top. Everything below follows the book's mechanics, compressed to game time.

### 4.1 Citizens (everyone)
- **Aesthetics draft.** Canon: a citizen "randomly selected by cryptographic sortition" rates a building on a −5..5 slider [ch1]. It is quadratic voting: each person's ratings are rescaled to mean 0 and mean square 1, so the best strategy is to rate honestly.
  - *Game version:* players describe their homes and storefronts in text, optionally with an image. A small random panel of citizens rates each one. For each rater, we take all their ratings, subtract their mean and divide by their RMS, then average across raters. The result sets the aesthetics part of the property's land tax.
  - *Edge case (design choice):* a rater's first few ratings can't be normalized meaningfully, so they get a weight that grows as they rate more.
- **Composite land tax.** Canon: base 1% + aesthetics tax + other rubric taxes. The book's example is Badra St #1103 paying 1.00% + 0.18% + 0.33% = 1.51% [ch1]. The game uses the same structure on in-game property values, charged in in-game zc each season.
- **Courts.** Canon: 5 anonymous, randomly drawn judges, deliberating as two pairs plus a tiebreaker, with the median view deciding. An appeal draws a fresh random panel; there's no court hierarchy. Bad-faith or frivolous suits can earn a penalty judgment [ch6, ch26].
  - *Game version:* players can sue over in-game disputes (an unpaid order, a business accused of misdescribing itself, a contested audit). Five eligible citizens are drawn. Two private pair-rooms and a tiebreaker room each submit a position on a scale (e.g. award 0–100% of the claim), and the median wins. The plaintiff stakes in-game zc, and a 5-0 "frivolous" finding forfeits it.
  - Judges get the canon "no daily news" flavor as an optional honor-code badge.
- **Polls (Silverchat-style).** Canon: on Silverchat you pay or burn zipcoins to put a question to a cross-section of users, and more zipcoins reach more people [ch27]. Seila also mixes real questions with decoys so outsiders can't tell what she cares about.
  - *Game version:* spend in-game zc to send a poll to a random sample of active players; paying more widens the sample. Decoy questions are supported. Results are posted in the square so everyone knows the outcome and knows everyone else saw it (the canon "common knowledge" goal).
- **Assemblies.** Herald-hosted citizens' assemblies on a topic (canon example: improving public spaces [ch6]). The AI writes a "broad listen report", a summary of square sentiment, for Keepers to read.

### 4.2 Businesses
- Any player can register a business: a name, a description, and an "offering" such as menu items, event listings, a band's set list or a shop's goods. Other players buy and use them with in-game zc.
- The canon sales tax is paid automatically at the point of sale (the book's example: a 10.5 zc meal plus 1.1 zc tax = 11.6 zc [ch6]). The game applies a sales tax on every in-game purchase.
- **Audits under rubrics.** Each business is placed in a tier of the relevant rubric, and that tier sets its tax rate. Canon content/performance rubric [ch1]: Tier 1 0%, Tier 2 10%, Tier 3 (neutral) 20%, Tier 4 30%, Tier 5 40%. Tiers 4–5 cover promoting violence, lawlessness, anti-recommended substances, gambling or risky investment, excessive display of wealth, poor conflict resolution, or hatred. Other canon rubrics to start from: aesthetics, accessibility, ground-floor active use, clean indoor air, emergency preparedness, hardware openness.
  - Starting rubrics are seeded from canon text. After that, they change only through Keeper votes.
- The AI game master also runs NPC businesses (section 8), so there's always something to audit even when few players run businesses.

### 4.3 The Order of Steering

Canon structure, which matters for getting this right: an **Acolyte** is in training. With a prediction score of about 90 or more, plus a Parliament committee hearing, they join in full standing on a **track they keep secret, either Sentinel or Keeper** [ch1, ch8]. This is two tracks, not a ladder. **Heralds** are Sentinels or Keepers who are randomly retired each year to become public ambassadors [ch6].

| Role | Canon mechanic | Game version |
|---|---|---|
| **Acolyte** | Audits small businesses. About 10% of their audits are re-done by Sentinels, and the prediction score measures how well they predicted the Sentinels [ch1]. | Any citizen above a Rep threshold can apply. They get a queue of business audits, mostly NPC businesses at first. A random ~10% are re-audited by Sentinel panels, and the score is how often they matched. |
| **Advancement** | Score ≈90+ (top 10%) plus a committee hearing. The hearing doesn't know which track you chose [ch8]. | A hearing in a public room, run by a random panel of citizens standing in for the committee **(design choice: the game has no elected Parliament at MVP)**. The track is chosen privately. |
| **Sentinel** | Audits in 3 groups of 3 [ch6]. | Each audit goes to three 3-person private rooms that can't see each other. The tier is set by majority or median across groups **(the exact aggregation is a design choice)**. |
| **Keeper** | 21 randomly chosen per rubric, 7 new each year, 3-year terms. Three subgroups of 7 discuss each proposal independently and never learn who the others are. Any Keeper can propose. A change needs 13 of 21. The chat cuts off 7 days before a vote. Numbered pseudonyms [ch6, ch17, ch23]. | Exactly that, with terms measured in seasons. Each rubric gets three sealed 7-person rooms where members appear only as "One" … "Twenty" (canon Keepers also go by numbers like Zero). The rooms lock for a quiet period before the vote **(length scaled to the season; design choice)**. Pass at 13/21. |
| **Herald** | Randomly retired each year. Transparent about past work only once they no longer hold power [ch6]. | At each season change, some Sentinels and Keepers are drawn as Heralds. Their pseudonym-to-player link becomes theirs to reveal, and they can publish their old audit and vote reasoning. They host assemblies and mentor applicants. |

**Secret tasks and the guess bounty.** Canon: Order members may not reveal their assigned task. Anyone can send a guess at a member's task with a small deposit; a correct guess docks the member's salary, and the guesser gets half [ch1].
- *Game version:* every Order member has a hidden assignment (e.g. "Keeper, clean indoor air rubric" or "Sentinel, cafés"). Members get an in-game zc salary each season. Anyone can stake an in-game zc deposit to guess a pseudonym's assignment. A correct guess docks the target's salary and pays half of it to the guesser; a wrong guess loses the deposit **(the wrong-guess rule is a design choice; canon only describes the deposit)**.
- This is the main social-deduction layer, so it creates real stakes for talking carelessly in public rooms.
- **It runs on in-game zc only, never real ZC** (see section 11, regulatory risk).

**Privacy flavor.** Canon members wear privacy robes and speak through neck bands with re-randomized AI voices [ch1]. The game version: Order rooms show only pseudonyms, avatars are a uniform purple robe, and an optional "neck band" filter has the AI paraphrase your message so your writing style doesn't give you away **(design choice)**.

**Honesty about privacy.** Canon secrecy rests on zero-knowledge cryptography and coercion-resistant voting keys [ch15]. At MVP, our server knows who is behind each pseudonym. The UI must say so plainly. Later phases could reduce operator knowledge (section 9.6), but we should never claim canon-level privacy we don't provide.

### 4.4 Reputation and gated rooms
- Each player has a **Rep score**. It goes up with Acolyte prediction accuracy, finishing jury duty, rating when drafted, hosting assemblies, and well-reviewed businesses. It goes down with frivolous suits and moderation strikes. **The formula is a design choice and should be published.**
- **Gated rooms.** The canon gate shows "Rep score ≥ 200 Verified ✓" [ch1], and the gate "learned that someone holding a valid and unused credential had arrived - and nothing else." Rooms can have a Rep threshold. At MVP the server checks the threshold. Later, a ZK proof could reveal only that you pass.
- **Later: reputation-backed loans.** Canon has a ZK loan collateralized by reputation, with a nullifier so the same reputation can't back two loans [ch6]. The game version is in-game zc loans to start a business. This is phase 5.

### 4.5 Visitors from Dzego and Freetown
- Canon: Dzegojan tourists visit Freetown [ch5]. Players can make a visitor character from **Dzego** or a **Freetown** visitor instead of a Veridian citizen.
- Visitors are not citizens, so they aren't drafted for sortition, can't join the Order, and can't judge **(design choice, consistent with citizenship-based sortition)**. In exchange, they can run pop-up businesses that are still audited and taxed, and host cultural events.
- Canon flavor to draw on: Dzegoban phrases ("kai ja" = tea), Dzego's decimal-time origin, Freetown's minimal-tax market ethos (its constitution bans taxes beyond a basic land tax). Freetown visitors are a natural voice for "steering vs freedom" debates.
- Keep visitors away from the Kungaupei, sabotage and the war arcs, per the everyday-life rule.

### 4.6 Mini-games (only what the book supports)
- **Minpentai.** Well supported by the text [ch4, ch12, ch14]. It's a Game-of-Life-style strategy game with:
  - fog of war (your "symbol", a dot pattern, lets you see within thirty squares of any copy);
  - an initiation phase where you place squares;
  - gliders, walls, rock formations, glider factories and spaceships that can recreate your symbol elsewhere;
  - periodic "intervention turns";
  - time-reversible rules;
  - a surprise rule change each match set by the priests (e.g. a hex grid in ch12, "rotate one eighty if three" in ch4).

  In canon it's a Dzego sport. In the game it can be an exhibition hosted by Dzegojan visitors. It's a big build, so it comes late (phase 5). A fan project is already building a playable Minpentai; if its license allows, reuse or collaborate rather than rebuild.
- **Helisport scoring.** Canon: redballs are caught, greenballs hit players and blueballs knock down pins, and the score is *multiplicative*, so teams have to balance all three [ch28 and the briefing]. A simple text or dice version suits a club bar, with no copter physics needed.
- **Nim.** Canon: taught with the XOR strategy [ch25]. It's trivial to build, and it works as a tutorial game and a tea-shop pastime.

## 5. Chat structure: community hub and Veridia rooms

The app has two layers that share one login, one sidebar and one moderation system. "Everyone" below means every citizen, i.e. everyone who has made their arrival post (an on-chain Book post, or a free in-game one for Founding Citizens; section 6.2), except where a room is marked open.
- **Community hub (out of character, "OOC").** Normal community chat, the Telegram replacement. Section 5.2.
- **Veridia (in character, "IC").** The role-play rooms. Section 5.1.

### 5.1 Veridia rooms (in character)

| Space | Who sees it | Notes |
|---|---|---|
| **Tapaia Square** (town square) | Everyone | In-character broadcast feed: announcements, poll results, season events, and featured posts. Posting to the square is a **Speak** action and costs a small burn of both $ZC and the project token (burn-to-be-heard, section 6). On-chain zipcoin Book posts can show in a separate, filtered "From the Book" lane. New citizens' arrival posts (on-chain, and founders' in-game ones) show in a filtered **Arrivals** lane, with the same hide-by-default rules **(design choice)**. Note that a square Speak is our own burn, separate from a zipcoin Book post (6.3). |
| **District rooms** | Everyone | Kalimar, the business district, Galanar Square and so on: for local hanging out. Ordinary messages here are free. |
| **Business rooms** | Public or owner-gated | Each business gets a room. Its rubric tier is shown on the door. |
| **Doors and DMs** | The door owner and the knocker | Every player has a door. A **knock** costs a small burn of both tokens as a seriousness signal (canon: "50 zipcoins have just been burned.🔥" [ch20]). The owner chooses whether to open a DM. Unsolicited DMs without a knock are off by default **(design choice; it reduces harassment)**. |
| **Rep-gated rooms** | Rep ≥ threshold | e.g. a "200+ lounge". The gate shows only pass or fail. |
| **Holder rooms (optional)** | Citizens who hold a set amount of tokens | Only if we keep hold-to-enter as a secondary tool (6.2.6), e.g. a holders' lounge. Never needed for citizenship or for the main community channels. |
| **Court rooms** | 5 judges, as 2 pair-rooms + 1 tiebreaker room | Parties file statements into a shared, read-only evidence room. Judges are anonymous to the parties. |
| **Sentinel rooms** | 3 sealed rooms of 3 per audit | Short-lived, one audit each. |
| **Keeper rooms** | 21 per rubric, as 3 sealed rooms of 7 | Members don't know who is in the other two rooms. They see only numbered pseudonyms. Proposals and broad listen reports are shared across all three, but discussion isn't. The rooms lock for the quiet period, then all 21 vote. |
| **Assembly hall** | Open, Herald-run | Structured sessions with a topic. The AI summarizes them. |
| **Visitor hostel** | Everyone | Onboarding for visitor characters. |

### 5.2 Community hub layer (out of character)

The goal is that the community can move its day-to-day chat off Telegram and into this app, whether or not people play the game.

**Channels (OOC).** Plain chat with real handles, no in-world clock and no role-play rules.

| Channel | Who can post | Notes |
|---|---|---|
| **#announcements** | Team only (read for all) | Releases, token and treasury reports, contract addresses, security warnings. Pinned "one true address" post for $ZC and the project token. |
| **#general** | Citizens (see gating below) | Everyday community talk. |
| **#market** | Citizens | Price and trading talk, kept out of #general. Rules: no paid promotion, no "guaranteed" calls, no impersonating the team. The team does not post price predictions or talk up the token here (see regulatory risk). |
| **#support** | Everyone, including people who haven't entered yet | Wallet, onboarding and bug help. Mods and helpers only ever answer in public; pinned warning that staff never DM first and never ask for seed phrases. |
| **#dev-updates** | Team; replies in a thread | Changelogs, links to the GPL repo and the running commit. |
| **#feeds** | Bots only | ZC live feed, Book posts, price alerts (below). |
| **#lobby** | Everyone | An open, read-mostly room so newcomers can see the community before buying ZC or making an arrival post **(design choice; see gating)**. |
| **#off-topic, language rooms** | Citizens | Optional, added as demand appears. |

**Access and gating.**
- **Current direction, for now:** the arrival post (section 6.2) is the gate for posting in the citizen channels. It replaces hold-to-enter as the main gate. It is also the main anti-spam measure: every paid account costs a real, non-refundable burn plus gas, and the arrival post is public and permanent, so spam accounts leave a visible trail.
- Founding Citizens (the first X) enter free with an in-game arrival post. Founder slots are the weak point for spam and sybil farming, so they need their own limits (6.2.3).
- Hold-to-enter is no longer required for the community channels. It is kept only as an optional tool for specific gated rooms (6.2.6).
- Open question: how much is visible before entering. Proposal: #lobby, #support and #announcements are open (read, and post in #lobby/#support with rate limits); everything else needs citizenship. This keeps support reachable for the people who most need it.
- OOC chat has **no burn per message**. Burns apply only to in-character loud actions (square Speak, knocks, Order actions). Charging to talk in #general would kill the community.

**Notifications and mobile.**
- MVP: installable PWA (mobile web), with web push notifications for mentions, replies, DMs, knocks, announcements and draft/summons alerts. Per-channel mute and a quiet-hours setting.
- Optional channels for alerts the user opts into: email, XMTP (zipcoin already uses XMTP for door bells) or a Farcaster mini app later. Native iOS/Android apps are a later decision; the PWA comes first.
- Fallback for people who never open the app: a daily or weekly digest of #announcements.

**Bots and alerts (read-only).**
- **ZC live feed:** subscribe to `https://www.zipcoin.cash/api/v1/live` (SSE); post notable burns and knocks to #feeds, confirmed against Ethereum RPC before posting.
- **Book posts:** new Speak posts from `/words`, shown filtered (same hide-by-default rules as the "From the Book" lane, section 9.8), never re-broadcast elsewhere.
- **Price:** ZC and project-token price and pool liquidity from GeckoTerminal (DexScreener didn't index these Stockereum v4 pools per the briefing). Use calm, rate-limited alerts (e.g. a periodic summary plus threshold moves), not a constant ticker.
- **Treasury:** posts each treasury multisig transaction and each buyback-and-burn with links, which supports the published spending policy.
- **Game bridge (opt-in):** a once-a-day "news from Meldan" digest from the RPG into #general, so non-players see the game without being pulled into it.
- Bots hold no funded wallets and have no write access to chain. Bot code and prompts live in the public repo.

**Moderation and anti-spam.**
- Arrival post (or founder slot) required for posting, per-wallet rate limits, slow mode on busy channels, link and new-account limits in #lobby and #support.
- Filters for the usual Telegram problems: fake-support DMs, impersonation of team handles (reserved handles and a verified-team badge), wallet-drainer links, airdrop scams, and copycat token addresses (the bot flags any contract address that isn't the published one).
- Report button, mod queue, per-channel mods, blocks and mutes. One moderation system covers OOC and IC; the code of conduct has an OOC section (real-world rules) and an IC section (game rules).
- Moderators come from the community at first. Heralds can moderate assemblies on the IC side.

**Onboarding from Telegram and X.**
- A short "Moving to Veridian Chat" guide: connect a wallet, sign in (SIWE), make your arrival post (or claim a founder slot while they last), and where each Telegram topic now lives.
- Migration period: keep the existing Telegram/X presence as read-only pointers to the app for a set period, with the app link and contract addresses pinned. Optionally run a one-way announcement mirror so nobody misses news during the move. *(We found no official ZC Telegram in the briefing; this applies to whatever community groups exist. Any outreach is Angelo's call; nothing is posted or sent from this doc.)*
- Newcomers who haven't entered yet land in #lobby with a plain explanation of the arrival post: what it costs at current prices (burn plus gas), that it is permanent and public and gets reposted to X by @zipcoinbook, and the risks, rather than being bounced at the door.
- Handle carry-over: show ENS or `name.zipbook.eth` via `/identities/:who`; optionally let people link an X handle by a signed post, for recognition.

**How the RPG and community chat coexist.**
- **Separate by default.** The sidebar has two clearly labeled groups: "Community" (OOC) and "Veridia" (IC). New users land in the community side. The game is one click away but never required.
- **No game noise in OOC.** Drafts, summons, knocks and season events go to the Veridia side and to notifications the user has turned on, never into #general. The only crossover is the opt-in daily digest.
- **One account, two faces.** Your OOC handle and your citizen name are separate by default. Linking them publicly is your choice. Order pseudonyms are never shown on the OOC side, and the UI warns that OOC talk about your Order work can expose you to the guess bounty.
- **Different rules, clearly marked.** IC rooms use the decimal clock, in-character speech and burn-to-be-heard; OOC rooms use normal time and free posting. Each room header says which it is.
- **Players and non-players are equal OOC.** Rep and Order roles carry no weight in community channels, and community moderation doesn't depend on game standing.

## 6. Zipcoin integration

Canon zipcoin is just everyday money with burn and ZK features. The novel never says who issues it or what its supply is. Linking the game to real $ZC is our choice, not canon. Real $ZC is an ERC-20 on Ethereum at `0x4E67DB19044549fF420860834c91b45BaD298722`, with a fixed supply of 1B, no owner and no mint. It is not affiliated with Vitalik.

Relevant real features, all on Ethereum mainnet:
- **Speak** (the Book): burn at least 1,000 ZC (about $10 at the Oct 7 snapshot) to post 280 bytes permanently. Size and tier are relative to the 7-day median burn. A bot (@zipcoinbook) reposts burns to X.
- **Knock** (Doorstep): burn at an ENS name or address, optionally with a gift. The burn must be at least 1/10 of the gift. The owner is notified through EtherMail, ENS email and XMTP.
- **Names:** burning `/claim alice` gives `alice.zipcoin.cash` and `alice.zipbook.eth`.
- **Zip/unzip:** private transfers through zipcoin's 0xbow Privacy Pools deployment. Unzips go through a team relayer that charges 1%, and zips pay a 0.5% vetting fee.
- **Builder tools:** `@zipcoin/agent` (SDK/CLI), `@zipcoin/mcp`, and a public read API at `https://www.zipcoin.cash/api/v1` (`/words`, `/doors`, `/identities/:who`, `/names`, `/stats`, `/rules`, `/live` SSE). Writes are on-chain transactions.

> **Changed in v0.2.** Draft v0.1 recommended play money for everything, with real ZC only for optional Book posts and knocks, and a token much later. Angelo has chosen a different direction: real $ZC and the project token are required to enter (held, not spent) and are burned in small amounts for loud in-game actions. The in-game zc economy stays for everything that pays out.

> **Changed in v0.3 (current direction, for now).** Angelo's new entry model replaces hold-to-enter as the primary gate: entry means burning a real zipcoin Book post (Speak) as your permanent arrival message, with the first X citizens entering free as Founding Citizens (6.2). Hold-to-enter is demoted to an optional tool for specific gated rooms (6.2.6). Where v0.2 text conflicts with this, the new model wins.

### 6.1 Two kinds of money in the app

| | Real tokens ($ZC + project token) | In-game zc (play money) |
|---|---|---|
| **Used for** | The entry burn (an on-chain arrival post in ZC; whether the project token is also burned is open, 6.2); small burns for loud actions (6.3); buying paid extras (7.4); optionally, holding for specific gated rooms (6.2.6). | Taxes, salaries, business sales, court stakes, polls, the guess bounty, loans. |
| **Where it lives** | The player's own wallet. We never hold it. | Our database ledger. |
| **Can it pay out to a player?** | No. Burns go to a dead address; paid extras go to the treasury and burn. Nothing in the game sends real tokens to a player. | It can move between players, but it can't be bought, sold or redeemed. |

Keeping every payout (bounties, court awards, salaries) in play money is what keeps the game away from gambling and wagering rules, so that line stays.

### 6.2 Entry: the arrival post (citizenship and chat access)

> **Current direction, for now.** This replaces hold-to-enter (v0.2) as the primary gate. Where the two conflict, this wins. Amounts are placeholders.

**How it works**
- To become a citizen (post in the citizen channels and get citizen actions: drafts, courts, the Order), a player **burns a real on-chain Speak post on the zipcoin Book** from their own wallet. That post is their **permanent arrival message**: public, on-chain forever, and tied to their wallet.
- Zipcoin's Speak mechanics (from the briefing): the post burns **at least 1,000 ZC** (about $10 at the Oct 7 snapshot) through ZipBroadcaster and holds up to 280 bytes. Message size and tier are relative to the 7-day median burn, so a larger burn gets a bigger post. The @zipcoinbook bot reposts burns to X. Ethereum gas is paid on top. Zipcoin sets these rules, not us, and they can change, so the app reads the current rules (`/rules`) rather than hardcoding them.
- Entry is a **one-time** burn per account. Nothing has to stay locked or held afterwards, so a later sale or price drop never removes citizenship (unlike v0.2's hold check).
- The burn goes to zipcoin's burn (dead) address. It is **not** treasury revenue.
- Canon fit: loose. Veridian citizenship isn't bought in the book, but burning zipcoin as a costly, public signal is canon [ch19, ch20]. This is a **design choice**.

**6.2.1 The arrival flow**
- The app helps the player write the arrival message, shows a preview, the burn amount in ZC with an approximate dollar value, the gas estimate, and a clear warning: "this is permanent and public, can't be deleted, and will be reposted to X." The player signs from their own wallet; we never hold keys or tokens.
- The app verifies the post on Ethereum RPC (speaker = the account's wallet, burn at least the entry amount, made after sign-up) before granting citizenship. **To verify before building:** whether a third-party app can tag its Book posts (the `/words` API has a `board` filter, but whether apps can set one is unconfirmed) so arrival posts can be told apart and filtered.
- Open: whether a Book post made *before* signing up can count as an arrival post (convenient for existing zipcoin posters, but easier to game).

**6.2.2 Founding Citizens (free entry for the first X)**
- The first **X** citizens (placeholder; number not decided) get in **free**: no on-chain burn.
- They get a **"Founding Citizen" badge**.
- They still make an arrival post, as a **free in-game (off-chain) post** shown in the same Arrivals lane, so the ritual is the same for everyone. It lives in our database and can be moderated or removed like any in-app message.
- A founder can optionally also burn a real Book post later; it doesn't change their badge **(design choice)**.

**6.2.3 Keeping founder slots from being farmed (to decide)**
Free slots are the easiest thing in the app to farm with many wallets. Options, which can be combined:
- one slot per wallet, and only wallets that sign in during a stated founder window;
- an invite list or invite codes from the existing community (e.g. people active in zipcoin's Book or current community groups), published as a rule up front;
- a short probation before the badge is final (e.g. some real participation, a Rep floor), with obvious farm accounts losing the slot;
- optional proof-of-personhood if a usable one exists;
- founders can't transfer or sell the slot or badge.
None of these fully stops a determined farmer. The honest framing is that founder slots are a launch gift, and Rep and sortition rules (11, Sybil rows) carry the rest.

**6.2.4 How much should the entry burn be? (undecided; placeholder E)**
The dollar amount is not decided. The entry burn is shown as **E** below. Options:

| Option | How it works | Pros | Cons |
|---|---|---|---|
| **Zipcoin's minimum** | E = whatever Speak's minimum is (currently 1,000 ZC). | Simplest; no extra rules; matches the Book exactly. | Zipcoin controls it, not us. Dollar cost moves with ZC price. Might be too cheap to stop spam or too pricey at a price peak. |
| **Fixed ZC amount (our own)** | E = a fixed number of ZC at or above the minimum, reviewed on a published schedule (e.g. per season) by a published rule. | Simple, predictable in ZC, needs no oracle, can't be manipulated. | Real dollar cost swings with ZC (which has moved by large percentages within days per the briefing). Reviews can feel arbitrary unless the rule is published. |
| **USD-equivalent via price oracle** | E = the ZC amount worth a set dollar value at entry time. | Entry cost stays stable in dollars; fairer to newcomers over time. | Needs a price source. Spot prices on thin v4 pools are easy to push around, so it needs a TWAP over a long window with sanity bounds. More code and more things that can break; the amount in ZC changes every time. |

A middle path is a fixed ZC amount with a published review rule, and dollar estimates shown before signing. Note that because Book post size is relative to the 7-day median burn, the same E can produce a smaller or bigger post from week to week.

**6.2.5 Can the project token be burned at entry too? (open question)**
- A Book post burns ZC only, through zipcoin's contract. Burning the project token at entry would be a separate transfer to the dead address (could be batched into one signature, EIP-5792).
- Options: ZC only (simplest, and the only option before the token launches); ZC plus a project-token burn (ties entry to our token, but adds cost, a second token to buy, and copycat risk); or a choice of either.
- Not decided. Needs the same legal check as the rest of the token design.

**6.2.6 What happens to hold-to-enter: kept as an optional, secondary tool**
- **Decision in this draft:** hold-to-enter is **no longer required** for citizenship or for the main community channels. It is kept only as an **optional, secondary idea for specific gated rooms** (e.g. a holders' lounge or a token-holder Q&A room), if Angelo wants them later.
- It is **never** used for civic roles (drafts, courts, the Order), so a balance drop never affects game standing.
- If used, a room requires a connected wallet to hold at least **J $ZC and/or K project tokens** (placeholders; renamed from v0.2's X and Y so they don't clash with the founder count). Nothing is burned or locked. Falling below the threshold removes access to that room only.

**Design questions if hold-gated rooms are kept (open):**
1. **Fixed token amounts vs USD-equivalent.** Fixed amounts (J ZC, K tokens) are simple, need no oracle and can't be manipulated, but the real cost of entry moves with price, possibly by a lot. A USD-equivalent threshold keeps entry cost stable but needs a price source (a TWAP from the pools, since spot prices on thin pools are easy to push around) and can lock people out when prices fall. A middle path: fixed amounts, reviewed on a published schedule (e.g. once per season) by a published rule.
2. **When balances are checked.** Live check on every login and on every gated action is the most accurate but costs RPC calls and can kick people mid-conversation. Periodic checks (e.g. hourly) are cheaper. A snapshot check (at season start) is the most predictable but lets people sell right after.
3. **Gaming the check.** Tokens can be passed from wallet to wallet to pass checks one after another, or borrowed for a moment. Mitigations: require a minimum holding period, or check at a random time within each period, or check balances at a past block.
4. **Grace period.** If a balance dips (a sale, a price-based threshold moving), allow a grace period of N hours or days before access to the gated room is removed, with a warning banner and notification.
5. **Multiple wallets.** Allow linking several wallets (signed with each) and sum the balances? That helps people who keep tokens in a cold wallet. It needs a delegate pattern so no one has to sign in with a cold wallet (e.g. delegate.xyz-style delegation, to be checked).
6. **Which rooms.** Which specific rooms, if any, are hold-gated. The main community channels and citizenship are not.
7. **Order roles and courts.** Proposed: no Order role, court seat or civic draft is ever hold-gated, so a balance drop never affects them.

### 6.3 Burn-to-be-heard (game actions)

Canon basis: burning zipcoin is how Veridians show they're serious, e.g. a knock that burned 50 zipcoins [ch20] and the costly-signal posts [ch19]. The game makes a few loud actions cost a **small burn of both $ZC and the project token**:

| Action | Burn (placeholder) | Notes |
|---|---|---|
| **Speak** in Tapaia Square (in-character broadcast) | a ZC + b tokens | Ordinary district-room and OOC messages stay free. Paying more could boost visibility, as in the canon costly signal **(design choice)**. |
| **Knock** on a door | c ZC + d tokens | Lets you reach someone who hasn't opened DMs to you. |
| **Enter the Keeper draw** for a season | e ZC + f tokens | Canon Keepers are drawn at random with no cost; the burn here is a **design choice** to make entering the pool a signal of intent. It buys a place in the draw, never a seat, a vote or an outcome. |
| **Order advancement** (applying as Acolyte, requesting the hearing) | g ZC + h tokens | The burn must be the same for both tracks so it doesn't reveal whether you chose Sentinel or Keeper. |

**How burns are made (to decide):**
- **Burn per action, on-chain.** Each action is a wallet-signed transaction sending both tokens to `0x…dEaD` (or a small burn contract that does both in one call and tags the action). Most honest, but every action costs Ethereum gas on top of the burn, and waiting for a transaction is slow for chat. A batched wallet call (EIP-5792) can make it one signature.
- **Burn ahead for action credits (proposed).** The player burns a larger amount once and gets a matching number of non-transferable, non-redeemable action credits in the app. We never hold the tokens (they're destroyed), so there's no custody, and each action is instant. The burn is still real and public; it just happens before the action rather than with it.
- **Fixed amounts vs USD-equivalent** has the same trade-off as the entry burn (6.2.4): fixed amounts are simple but their real cost swings; USD-equivalent needs a price oracle.
- **Not the zipcoin Book.** These are our own burns. Posting to zipcoin's Book (≥1,000 ZC through ZipBroadcaster) is now used once for the entry arrival post (6.2); beyond that, it stays a separate opt-in feature.

Burned tokens reduce supply. They are **not** treasury revenue.

### 6.4 Other ZC features
- **"Post to the Book" (opt-in, after entry):** the same flow as the arrival post (6.2.1), for later posts. Write a message, preview it, confirm a clear warning ("this is permanent, public and costs ≥1,000 ZC plus gas"), then sign a Speak burn from your own wallet. Shown in the "From the Book" lane with a "🔥 real burn" badge.
- **Names:** show a player's `name.zipbook.eth` or ENS name (via `/identities/:who`) as a verified handle if they have one. Claiming happens on zipcoin.cash, not in our app. (Our own paid name claims in 7.4 are in-app character and handle names, a separate namespace.)
- **Never** auto-mirror chat to the chain, and never pay out real tokens from game outcomes.
- **Zip/unzip:** out of scope. The privacy pools are mixer-adjacent with a small anonymity set (82 deposits per the briefing). Linking to zipcoin.cash is enough.
- **To verify before building:** whether a third-party app can tag its Speak posts so they can be filtered (now important, because entry depends on recognizing arrival posts) (the `/words` API has a `board` filter, but whether apps can set one isn't confirmed; check `docs/api-v1.md`), and whether `@zipcoin/agent` can build unsigned transactions for a browser wallet. If not, call the MIT-licensed contracts directly with viem.

## 7. Project token on Stockereum, paired against ZC

> **PLACEHOLDER: best current option, not final.** Everything in this section (and the token parts of sections 6, 11, 12 and 13) records Angelo's current direction as of Oct 7, 2026. Amounts are shown as letters (X, Y, a, b…) on purpose. Nothing here is a commitment to holders, and it all needs a legal check before launch.

### 7.1 How Stockereum works (from the briefing)
- It's a Uniswap v4 hook launchpad on Ethereum with no bonding curve. One transaction mints exactly 1B tokens and puts the whole supply into a single-sided position. The creator deposits no quote asset and pays only a creation fee (amount not found).
- The hook owns the liquidity, so it **can't be pulled**.
- The token template is fixed-supply, with no owner, no mint, no pause and no proxy.
- **ZC is an allowed quote asset.** 166 ZC-paired launches exist, e.g. SC/Silverchat, ZB and DZHAMSTER.
- **Fee:** the creator picks 1%, 2% or 3% at launch, and it can never change. The fee is taken on the quote side, so on a ZC pair it accrues in ZC.

  | Fee | Platform keeps | Creator gets |
  |---|---|---|
  | 1% | 0.5% | 0.5% |
  | 2% | 1% | 1% |
  | 3% | 1% | 2% |

  The creator's share can be claimed from an escrow, or routed to holder rewards through a HolderDistributor.
- **Anti-snipe:** for the first 20 seconds, the fee starts at 99% and decays linearly to the launch fee. Everything above the base fee goes to the platform.
- **"Graduation"** is just a tracking metric: 4 ETH of quote in the pool. How it's measured for ZC-quoted pools is unconfirmed.
- The platform's 60% buyback and burn is documented for ETH pairs. Whether it applies to ZC pairs is unconfirmed.
- Swaps are exact-input only.

### 7.2 Chosen direction
1. **Launch on Stockereum, paired against ZC (not ETH).** Every buy of the project token goes through ZC, and creator fees accrue in ZC.
2. **The token's job is to generate revenue for the project** (hosting, AI inference, moderation, development), from fees and activity.
3. **It has real utility in the app:** it's burned for loud actions (6.3), it may also be burned at entry (open question, 6.2.5), it may gate specific holder rooms (optional, 6.2.6), and it's the currency for paid extras (7.4).
4. **No holder revenue share.** HolderDistributor stays off. See 7.6.

This is close to what v0.1 called a "utility token" and did not recommend, because it ties access to price. (v0.3 loosens that link: entry is now a one-time ZC burn, and holding the token is no longer required to be a citizen.) Angelo has chosen it; the trade-offs are now tracked as risks in section 11 instead.

### 7.3 Revenue streams

| Stream | What it is | Goes to | Notes |
|---|---|---|---|
| **(a) Stockereum creator fee** | The trade fee on every buy and sell of the project token. **Leaning 2%.** | Treasury, in ZC | At 2%, the platform keeps 1% and the creator gets 1% of volume (per the briefing). For comparison, 1% nets the creator 0.5% and 3% nets 2%. Income depends entirely on trading volume, which may be thin. |
| **(b) Action burns** | Small burns of both tokens for Speak, knocks and Order actions (6.3). | Nobody (burned) | Reduces supply of both tokens. **Not treasury revenue.** |
| **(c) Paid extras** | Custom building styles and aesthetics, guild rooms, name claims, priced in the project token. | Split: P% treasury, Q% burned | Cosmetic and convenience items only. They must not buy votes, audit results, court outcomes, Rep or Order seats. Paid building styles shouldn't change aesthetics ratings by themselves; citizens still rate them. |

Fee tier note: 2% is the current lean because the creator share doubles from 0.5% to 1% compared with 1%, while traders pay less than at 3%. 3% would net 2% but makes a likely thin pool more expensive to trade. Final tier is an open decision, and it can never change after launch.

### 7.4 Paid extras (details to decide)
- **Building styles / aesthetics packs** for homes and storefronts (text templates, frames, art).
- **Guild rooms:** a private room for a group of players, with a name and door art.
- **Name claims:** reserving an in-app handle or character name. Reserve canon character names and real people's names, as zipcoin does for "kept" names.
- Pricing in fixed token amounts or USD-equivalent (same trade-off as 6.2.4), and whether extras are one-off or per season.
- Payment is a wallet transfer from the player: P% to the treasury multisig, Q% to `0x…dEaD`.

### 7.5 Treasury policy
- **Public multisig** (signers and threshold published) holds all project revenue: ZC from creator fees and project tokens from paid extras.
- **Buyback and burn:** a set share (Z%) of ZC fee revenue is used to buy the project token from the pool and burn it. The rest funds running costs under the spending policy.
- **Published spending policy** covering hosting, AI inference, moderation, open-source contributor bounties and audits, with a regular public report (e.g. quarterly) linking every transaction. The #feeds bot posts treasury moves as they happen (5.2).
- **Things to decide:** the buyback share Z; schedule (fixed schedule is transparent but easy to front-run; ad hoc is harder to front-run but looks discretionary); what happens to project tokens received from paid extras (hold, burn, or a stated rule; selling them would look like the team dumping); how and when ZC is converted to pay bills, since fees accrue in ZC and bills are in dollars.
- Treasury buybacks go through our own pool and pay its fee like any other trade. At a 2% tier, half of that fee comes back to us as creator fee and the platform keeps the other half.
- **Dev buy at launch:** optional, as with ZC's 0.1 WETH. If we do one, disclose the amount and wallet beforehand. The team will need some tokens to use its own app; say where they came from.

### 7.6 What we must not promise (keep this)
- Revenue comes from **trading fees and in-app activity**. It belongs to the project and pays for the project. It is **not** a share owed to holders.
- **No holder revenue share, dividends, staking yield or HolderDistributor rewards.** These make the token look like an investment in our work, which is how securities rules are usually triggered.
- Buyback-and-burn is a supply policy, not a price promise. Describe it factually, don't market it as "number go up", and keep it within the published policy. Get a legal view on it specifically, because buybacks funded by revenue can also be read as returning value to holders.
- No price talk from the team in #market or anywhere else. No roadmap promises tied to the token price.

### 7.7 Copycats and name collisions
- "Veridia" and "snowmoon" tokens already exist on-chain (listed at theordereth.xyz). There's an X account @Veridia_zc, and veridia.tv is a separate adaptation. Many fake "ZC"/"zipcoin" tokens exist on Stockereum. One even launched *before* the real ZC.
- **Don't** name the token or ticker "Veridia", "Veridian" or "Snowmoon". Pick a distinctive name and check it against `stockereum.com/api/graduations`, GeckoTerminal and X before launch.
- Publish the one true contract address in the repo, the site, #announcements and the app footer. The app hardcodes both the ZC address and the project-token address, and the entry, burn and any hold-check flows only accept those exact contracts.
- Expect copycats of our token within hours of launch. If the project token is burned at entry (6.2.5) or used for holder rooms, a copycat could trick newcomers into buying the wrong token: the onboarding flow should link buyers straight to the correct Stockereum page, `https://stockereum.com/t/<address>`, and the #feeds bot flags other addresses.
- The app's own name should also avoid confusion with veridia.tv and @Veridia_zc. "Veridian Chat" is a placeholder.


## 8. AI game master and NPC layer

Guiding canon line: **"AI should be a player, not the game"** [ch32]. The AI narrates, fills in the world and helps players. **It never decides votes, audits, court outcomes, sortition draws or bounty results.** Those are set by players and code.

- **Narrator / GM.** Writes season openers, square announcements, weather, local news, and daily "something happened in Kalimar" prompts. It's seeded from a canon lore file, and anything it invents is marked as non-canon in the codex.
- **NPC businesses and citizens.** Original characters only, e.g. a Hydrafill street promoter (Hydrafill's ad gags are canon: "TEN PERCENT LESS TOXIC"), a tea-shop owner or a bookshop clerk. NPC businesses give Acolytes audits early on. NPCs never pose as players, and every NPC is labeled.
- **Emerald (personal assistant).** Each player's private helper, modeled on the canon local AI that tutors, summarizes, drafts and rates urgency [ch1]. It explains rules, summarizes rooms you missed and drafts messages. It's private to each player and never shares between them.
- **Broad listen reports.** The AI summarizes public square sentiment on a rubric topic for Keepers (canon [ch6, ch23]). The prompt and its inputs are published so the summaries can be checked.
- **Neck-band paraphraser (optional).** Rewrites Order members' messages to hide their writing style.
- **Guardrails:**
  - The AI refuses war plots and canon-character impersonation, per Angelo's rules.
  - Content moderation runs on everything the AI outputs.
  - Model and prompt versions are recorded per message for GPL pipeline disclosure.
  - Prefer models whose use can be fully disclosed. Open-weight models make the "open pipeline" story cleanest, but hosted models are fine if prompts and harness are published.

## 9. Technical architecture sketch

```
Browser / PWA (web app, wallet connect, web push)
   │  SIWE login, WebSocket chat, wallet-signed arrival posts, burns, extras and Speak/Knock txs (direct to Ethereum)
   ▼
API + chat server ──── Postgres (players, rooms, OOC + IC messages, ledger of in-game zc, rep, action credits)
   │        │    └──── Redis (presence, pub/sub, rate limits)
   │        ├── Community hub (OOC channels, notifications/push, digests, bots: ZC feed, Book, price, treasury)
   │        ├── Access service (arrival-post verification, founder slots and badges; optional hold checks for gated rooms)
   │        ├── Game engine (sortition, audits, courts, Keeper votes, bounties, seasons)
   │        ├── Randomness service (public beacon + commit-reveal; all draws auditable)
   │        ├── AI service (GM, NPCs, Emerald, summaries; prompts in repo)
   │        ├── Moderation service (filters, reports, mod queue, scam/wrong-address detection)
   │        └── Chain indexer (zipcoin.cash /api/v1 + /live SSE; burns, extras payments, treasury; verifies on RPC)
   ▼
Ethereum mainnet (ZC token, project token + Stockereum pool, ZipBroadcaster, ZipDoorstep, treasury multisig) – read via RPC + zipcoin API
```

### 9.1 Frontend
A web app (e.g. Next.js or SvelteKit) with wallet connect (e.g. wagmi/viem). It's mobile-friendly and text-first. It shows decimal-time timestamps with a hover to see real time. Doors, rooms and the square are separate views. It ships as an installable PWA with web push so the community hub works on phones (section 5.2). OOC channels show normal time; only IC rooms use the decimal clock.

### 9.2 Chat backend
A WebSocket server with Postgres as the source of truth. Room access is enforced server-side for gates, sealed Keeper rooms and the quiet-period lock. Rate limits are per wallet.

### 9.3 Auth
**Sign-In with Ethereum (EIP-4361)** with a nonce and expiry, then a session cookie.
- One wallet = one account by default. The entry burn raises the cost per paid account, but free founder slots and Sybil resistance in general are still weak; see the risks section.
- Optional: show the ENS or zipbook name from `/identities/:who`.
- Order pseudonyms are a separate identity layer, mapped server-side.

### 9.4 Game engine
Deterministic rules code: the aesthetics normalization, the 13/21 threshold, the 3×3 and 3×7 room assignments, median court rulings, the bounty payout (half the docked salary), prediction scores and season rollover. Every rule is unit-tested and documented in plain language in the codex.

### 9.5 Sortition
Draws must be verifiable, as a nod to the canon "cryptographic sortition".
- Use a public randomness beacon (e.g. drand), or commit-reveal from the server plus a later block hash.
- Publish the seed and the eligible list hash for each draw, so anyone can re-run it.

### 9.6 Privacy roadmap (later)
- Keep the pseudonym-to-player mapping in a separate encrypted store with minimal access.
- Later, explore Semaphore-style group membership proofs for Rep gates and Keeper voting, so the server can check eligibility without linking identities.
- The canon KAG (3-of-5 in-person key ceremony) is out of scope, but it could be a fun optional ritual.

### 9.7 ZC integration
- **Read:** subscribe to `https://www.zipcoin.cash/api/v1/live` (SSE) and query `/words` and `/doors` for burns tied to known player addresses. Then **confirm each event against Ethereum RPC** before showing a "real burn" badge, so we aren't trusting the API blindly.
- **Write:** the user's wallet calls ZipBroadcaster (`0x9925…6928`) or ZipDoorstep (`0x1813…7730`) directly. ABIs come from the MIT-licensed zipcoin repo, or from `@zipcoin/agent` if it supports browser signing. Our server never holds keys.
- **Arrival-post check:** confirm on RPC that the account's wallet made a ZipBroadcaster Speak burn of at least the entry amount E (6.2.1) before granting citizenship. Founder slots are granted in our database and recorded publicly (count used, rule applied).
- **Hold check (only for optional gated rooms, 6.2.6):** read ZC and project-token balances by RPC for the hardcoded contract addresses only, using the check model chosen there (live, periodic or snapshot, with a grace period).
- **Burns and extras:** verify burns (transfers of both tokens to `0x…dEaD`) and paid-extras payments (to the treasury multisig and dead address) on RPC before granting the action, credits or item.
- **MCP:** `@zipcoin/mcp` lets AI agents speak and knock. **Do not give the GM AI a funded wallet.** At most, use read-only tools like price, door and today for flavor.

### 9.8 Moderation
- Standard chat moderation: report button, mod queue, word filters, per-room mods (Heralds can moderate assemblies), and blocks and mutes. Doors default to knock-first.
- On-chain Book posts can't be deleted. The app only displays them: there's a filtered lane, a hide-by-default threshold and a "show anyway" toggle. We never re-broadcast them. This applies to on-chain arrival posts too: we can hide an arrival post in the app and remove the player's citizenship, but the post stays on-chain and on X.
- A clear code of conduct, with a non-canon section for real-world rules (harassment, doxxing, minors).

### 9.9 Hosting and ops
- Containerized services, daily backups, and logs with retention limits.
- In keeping with the canon "data retention" rubric, keep minimal personal data: wallet address, handle, and nothing else by default.

## 10. GPL v3 compliance plan

Vitalik released *Snowmoon* under **GPL v3** and explicitly asks derivative projects to open-source "the pipeline (AI prompts, scripts, task-specific harness, etc) and other non-commodity materials." Plain GPL v3 (unlike AGPL) technically triggers source release only on distribution, so a hosted service might not strictly have to. We meet the spirit anyway. *(Not legal advice.)*

- **Public repo from day one**, licensed GPL-3.0. Consider AGPL-3.0 for the server, which is compatible and makes the hosted-service obligation explicit (open decision). It contains:
  - all app code (frontend, server, game engine, indexer);
  - **`PIPELINE.md` / `PROMPTS.md`**: every system prompt, NPC sheet, GM instruction, summarizer and paraphraser prompt, plus which models and versions are used;
  - **lore files**: the canon codex extracted from the novel (with chapter citations) and our non-canon additions, clearly separated;
  - the AI harness, eval scripts, seeding scripts, randomness code and moderation config. Truly sensitive abuse-detection lists may be kept private if they count as commodity or operational material; decide this deliberately and document it;
  - images, icons and robe art made for the project.
- **Credit**: "Based on *Snowmoon* by Vitalik Buterin (https://vitalik.eth.limo/snowmoon/), used under GPL v3." This goes in the README, the app footer, the codex and the token metadata.
- **Non-affiliation disclaimer**, in the same places: "This project is not affiliated with, endorsed by, or connected to Vitalik Buterin, the Ethereum Foundation, zipcoin.cash, or Stockereum. $ZC and any project token are speculative crypto-assets; nothing here is financial advice."
- **No added restrictions** on GPL'd material (GPL v3 forbids them). zipcoin's contracts are MIT, which is compatible.
- **Player content**: terms of service say players own their messages and grant us a license to display them. Chat logs aren't part of the "pipeline", but publishing anonymized example sessions is a nice touch.
- **Release discipline**: every deployed version is tagged in the repo, and the app footer links to the exact commit running.

## 11. Risks

| Risk | Why it matters | Mitigation |
|---|---|---|
| **Regulatory: securities** | A project token sold to the public, described as a revenue generator, with buybacks funded by revenue, could be read as an investment contract in some jurisdictions. Holder revenue share or dividends would make this much worse. | No holder revenue share, dividends or yield; HolderDistributor off. Describe revenue as paying for the project. Buyback-and-burn framed as supply policy, never as a price promise. No team price talk. Legal advice before launch, including on buybacks; consider geo restrictions. |
| **Regulatory: real-money stakes** | Real-value bounties, wagers on guesses, paid polls with payouts, or redeemable credits could count as gambling or money transmission, depending on jurisdiction. Privacy-pool features are mixer-adjacent. | All payouts (bounties, court awards, salaries, polls) stay in non-redeemable in-game zc. Real tokens are only held or burned, or paid to the treasury for extras; nothing pays out to players. Burn-ahead credits are non-transferable and non-redeemable. No custody. |
| **Entry burn excludes newcomers** | To join after the founder slots run out, someone needs a wallet, ETH for gas, and enough ZC for the entry burn, which is spent for good. They also have to be willing to post something permanent and public. That's a lot of friction for a Telegram replacement and shuts out curious readers of the novel. | Open #lobby, #support and #announcements; a clear onboarding guide; keep E modest; show current cost in dollars (burn plus gas) before asking anyone to buy; founder slots for the existing community. |
| **Permanent on-chain arrival posts and moderation** | Every paid citizen's arrival post is permanent, public and reposted to X by @zipcoinbook. Someone could pay to make abuse, slurs, scam links or someone else's personal data their arrival post, and we can't delete it. It also permanently links the wallet to joining the community, which some people won't want. | Preview, warning and explicit signature; suggest short, safe arrival messages; hide abusive arrival posts in the app (filtered Arrivals lane, hide-by-default rules) and remove citizenship; say so in the code of conduct; never re-broadcast. Tell people up front that the link between wallet and community is public. |
| **Sybil farming of free founder slots** | Free entry is the cheapest way into the app, so one person could grab many founder slots with many wallets, take badges and stack drafts, juries and the Keeper pool. | One slot per wallet; a founder window; invite list or community allowlist published as a rule; probation before the badge is final; Rep thresholds for civic roles; optional proof-of-personhood (6.2.3). |
| **Founders vs paid citizens** | Founders get in free and get a badge; later citizens pay. That can feel unfair, and a "Founding Citizen" badge could become a status item people try to buy or fake. | Same arrival ritual for everyone; the badge carries no votes, Rep or powers; non-transferable; publish how many slots were used and by what rule. |
| **Price swings change entry and action cost** | With a fixed ZC entry burn, a ZC price rise can make entry (or a Speak) expensive overnight, and a fall makes spam cheap. With a USD-equivalent burn, the ZC amount changes all the time and depends on an oracle. Zipcoin's own Speak minimum and median-relative sizing can also change without us. Existing citizens are no longer at risk of being locked out, since entry is one-time. | Pick the model deliberately (6.2.4); review fixed amounts on a published schedule; read zipcoin's current rules rather than hardcoding them; show live dollar estimates (burn plus gas) before signing. |
| **Burn costs need a price source or fixed amounts** | USD-equivalent burns and thresholds need an oracle. Spot prices on thin v4 pools are easy to manipulate, and there's no established oracle for a new ZC-paired token. | Prefer fixed amounts, or a TWAP over a long window from the main pools, with sanity bounds. Never use a single spot read. |
| **Gas and latency of on-chain burns** | Every on-chain burn costs Ethereum mainnet gas on top of the burn, and chat can't wait for confirmations. | Burn-ahead action credits (6.3), batched calls, and keeping burns only on a few loud actions. |
| **Balance-check gaming (optional holder rooms only)** | If hold-gated rooms are kept (6.2.6), tokens can be passed between wallets or borrowed to pass checks. | Minimum holding period, random-time or past-block checks, per-wallet rate limits. |
| **Pay-to-govern perception** | Burning to enter the Keeper draw and to advance in the Order can look like buying influence, which cuts against the book's sortition ideals. | Burns buy a place in a random draw or a hearing, never a seat or a vote. Same small cost for everyone; same cost for both tracks. |
| **On-chain burns can expose Order secrets** | Order actions burned from a wallet linked to your account are public on-chain, so anyone can see that a wallet applied or entered the Keeper draw, and when. | Same burn amount for both tracks; burn-ahead credits so individual Order actions don't appear on-chain; warn players. |
| **Dependency on ZC** | Our token is paired against ZC and entry requires a zipcoin Book post (ZipBroadcaster and zipcoin's rules), so ZC's price, liquidity, reputation and contracts directly affect us. If the Book contract or its rules change, our entry flow has to change too. The ZC team is anonymous. ZC itself has no owner and can't be paused, but the wider zipcoin stack has the risks below. | Keep running costs low; convert some ZC to stable value for bills under the spending policy; don't depend on zipcoin's team-run services for core play. |
| **Unaudited contracts** | zipcoin's own contracts are unaudited by their own statement, and so are the Stockereum launch contracts; only 0xbow components are audited. Our token would live entirely in Stockereum's unaudited contracts. A burn contract of our own would add another. | Never custody. Prefer plain ERC-20 transfers to the dead address over new contracts; if we write a burn contract, keep it tiny and get it reviewed. Warnings in the app. |
| **Upgradeable Entrypoint** | zipcoin's Entrypoint proxy (`0x7a8D…9193`) can be upgraded by the treasury key, with no timelock yet. It sits in the zip/unzip path. | Leave zip/unzip out of the app. Watch for upgrades. Re-evaluate if a timelock or multisig is added. |
| **Centralized zipcoin ops** | The relayer and association-set postman are run by the team, so they can delay or censor. | Don't rely on them for core play. |
| **Thin or fragmented liquidity** | ZC's main pool held about $338K against a $13M+ market cap, with liquidity split across many v4 pools and perps on top. A new ZC-paired token would be thinner still, so fee revenue may be small and buybacks would move the price a lot. Treasury fees are in ZC, so they inherit ZC's volatility (−65% from ATH at snapshot). | Treat token revenue as uncertain. Don't promise anything funded by it. Keep running costs low. Size buybacks to the pool. |
| **ZC price and holder shocks** | ZC moves a lot, and vitalik.eth holds about 4% as an unsolicited gift; a sale would be a major price event. It would change entry and burn costs overnight. | Show the current token amounts and approximate $ values before any signature. Grace periods on hold checks. |
| **Treasury conduct** | Selling project tokens received from paid extras, or unclear spending, would look like the team dumping. Predictable buybacks can be front-run. | Public multisig, published policy, bot-posted transactions, regular reports; a stated rule for project tokens the treasury receives. |
| **Permanent on-chain messages (beyond arrival posts)** | Book posts can't be deleted and are reposted to X by @zipcoinbook. A player could post abuse or personal data permanently. | Never auto-post. Require preview, warning and explicit signature. Filter on display. Ban the player in-app for abusive burns, and say so in the code of conduct. |
| **Copycats and impersonation** | Fake ZC tokens exist, plus existing "Veridia"/"snowmoon" tokens. Newcomers buying ZC for the entry burn could buy a fake ZC, and if the project token is used at entry or for holder rooms, a fake project token could fool them too. Fake-support DMs are the most common community scam. | Hardcode and publish addresses; onboarding links straight to the right pool; bot flags other addresses; reserved team handles; "staff never DM first". |
| **Community hub becomes a price room** | If market talk dominates, the community drifts toward speculation, which hurts both the game and the regulatory picture. | Separate #market channel with rules, team stays out of price talk, moderation. |
| **Moving off Telegram fails** | People may not leave Telegram, splitting the community across two places. | Make the hub useful on mobile with notifications first; a migration period with pointers; announcements mirrored during the move. |
| **Sybil accounts** | Wallets are free, so one person can farm drafts, juries and Keeper seats. The entry burn raises the cost per paid account but doesn't stop a well-funded person, and founder slots are free (see the founder-farming row). | Entry burn per paid account, founder-slot limits, Rep thresholds for drafts and Order roles. Optional proof-of-personhood later. Rate limits. Sortition weighted by account age and activity **(design choice)**. |
| **Operator knows the secrets** | The server can see pseudonym mappings, sealed rooms and votes. | Say so clearly. Minimize access. Follow the ZK roadmap in 9.6. |
| **AI drift and cost** | The GM could invent canon or slip into war plots, and inference costs scale with players. | Lore file plus guardrails. Label non-canon content. Cache outputs. Set per-player Emerald quotas. |
| **Endorsement confusion** | Players may assume Vitalik is involved. | Disclaimers everywhere. No use of his name in marketing beyond the credit. |

## 12. Roadmap

There are no dates; each phase ends when its exit criteria are met. **The community hub is the MVP; the RPG layers on top of it.** Token steps are part of the placeholder in section 7.

**Phase 0: Foundations**
- Pick a name for the app and the token (collision-checked). Create the GPL repo with LICENSE, README credit and disclaimer, and a canon codex with chapter citations.
- Write the code of conduct (OOC and IC sections). Get a legal consult on the token design (entry burn and founder slots, burns, revenue, buybacks, optional holder rooms) and on the in-game zc design, before anything launches.
- *Exit:* repo public, codex reviewed against the novel, legal consult done.

**Phase 1: MVP, community hub (the Telegram replacement)**
- SIWE login, handles (ENS/zipbook display), one account per wallet, optional linked wallets.
- OOC channels: #announcements, #general, #market, #support, #dev-updates, #feeds, #lobby.
- Entry v1 (current direction, for now): the arrival post. Founder slots for the first X citizens with the "Founding Citizen" badge and free in-game arrival posts, with the chosen anti-farming rules. After that, entry needs an on-chain Book arrival post burning E in **ZC only** (the project token doesn't exist yet). Filtered Arrivals lane. #lobby, #support and #announcements stay open.
- Before this ships: confirm whether third-party apps can tag Book posts, decide E (6.2.4) and X, and test the arrival flow on a mainnet fork.
- Mobile PWA with web push notifications, mentions, DMs, mutes and digests.
- Read-only bots: ZC live feed, Book posts (filtered), price and liquidity.
- Moderation and anti-spam: report queue, rate limits, slow mode, reserved team handles, scam-link and wrong-address filters.
- Telegram/X onboarding guide and migration plan (no outreach until Angelo approves).
- *Exit:* the community's daily chat runs in the app for a full migration period without major moderation or reliability problems.

**Phase 2: Token launch**
- Final legal check. Set up the treasury multisig and publish the spending policy and buyback rule.
- Choose the fee tier (leaning 2%). Decide on a dev buy and disclose it. Prepare copycat warnings.
- Launch on Stockereum paired against ZC, with holder rewards off. Publish the address everywhere; the app hardcodes it.
- Decide whether the entry burn also includes the project token (6.2.5); if yes, add it for new citizens only (existing citizens are never asked to re-enter). Optional hold-gated rooms (6.2.6) only if Angelo wants them. Treasury bot live.
- *Exit:* entry flow working for new citizens with no unresolved complaints; first public treasury report.

**Phase 3: Veridia, everyday Meldan (the RPG layer)**
- Character creation (citizen or visitor), and the "Veridia" sidebar group alongside the community.
- Tapaia Square, district rooms, doors with knock-first DMs.
- Burn-to-be-heard for square Speak and knocks (chosen burn model; burn-ahead credits if adopted).
- In-game zc ledger with a season stipend and sales tax.
- Player businesses and AI NPC businesses.
- Aesthetics sortition with normalization, and composite land tax.
- Rep score v1, and one Rep-gated room. AI GM, labeled NPCs and Emerald.
- Opt-in daily "news from Meldan" digest into #general.
- *Exit:* a playtest group can run one full season without admin intervention, and non-players report that the game doesn't get in their way.

**Phase 4: The Order, the courts and paid extras**
- The Acolyte audit queue with the 10% re-audit and prediction score.
- Hearings and the secret track choice, with the same burn for both tracks.
- Sentinel 3×3 rooms, and Keeper 3×7 sealed rooms with pseudonyms, quiet period and the 13/21 vote. Burn to enter the Keeper draw.
- Secret tasks, salaries and the guess bounty (in-game zc only).
- Heralds and assemblies, and broad listen reports.
- Five-judge courts with appeals and frivolous-suit penalties.
- Polls with sampling and decoys. Verifiable sortition published.
- Paid extras in the project token (building styles, guild rooms, name claims) with the treasury/burn split.
- Opt-in "Post to the Book" with warnings and the "🔥 real burn" badge, and the filtered "From the Book" lane.
- *Exit:* at least one rubric change passed by players. Bounty, court and burn flows tested on a mainnet fork (`anvil --fork-url`, per zipcoin's local dev docs) and then on mainnet with small amounts.

**Phase 5: Depth**
- Minpentai exhibitions (reuse a fan build if the license allows), Helisport scoring and Nim.
- Reputation-backed in-game loans with nullifier-style one-use rules.
- Privacy upgrades (membership proofs, including for any hold-gated rooms).
- Native mobile apps if the PWA isn't enough.
- More rubrics, and Graph Funding committees for in-game public projects.

## 13. Open decisions for Angelo

Decided in v0.3 (current direction, for now): entry by burning a real zipcoin Book arrival post; the first X citizens free as Founding Citizens with a badge and a free in-game arrival post; hold-to-enter demoted to an optional tool for specific gated rooms.

Decided in v0.2 (placeholder, not final; hold-to-enter since replaced as the main gate): token on Stockereum paired against ZC; token as a revenue generator; hold-to-enter with both tokens; burn-to-be-heard with both tokens; revenue from the creator fee and paid extras; buyback-and-burn from ZC fees; public multisig; no holder revenue share; community hub as the MVP with the RPG on top.

**Token and economy**
1. **Fee tier.** Leaning 2% (creator nets 1%). Confirm 2%, or choose 1% (nets 0.5%) or 3% (nets 2%). It can never change after launch.
2. **Entry burn amount E.** Zipcoin's minimum, our own fixed ZC amount (with a published review rule), or a USD-equivalent via a price oracle (6.2.4)? The dollar amount is undecided.
3. **Project token at entry.** Burn only ZC (via the Book post), also burn the project token, or let people choose (6.2.5)?
4. **Founder slots.** How many (X), the founder window, and which anti-farming rules (one per wallet, invite list or allowlist, probation, proof-of-personhood) (6.2.3).
5. **Arrival-post rules.** Whether a pre-existing Book post can count; what happens to citizenship if an arrival post is abusive; suggested guidance for what to write.
6. **Open areas.** Which rooms can be read or used before entering (proposed: #lobby, #support, #announcements).
7. **Hold-gated rooms.** Keep hold-to-enter at all, and if so for which specific rooms, with which thresholds J/K and check model (6.2.6).
8. **Burn amounts** (a–h in 6.3) and whether they're fixed or USD-equivalent.
9. **Burn mechanism.** Per-action on-chain burns, or burn-ahead non-redeemable action credits (proposed), and whether to write a small burn contract or use plain transfers to the dead address.
10. **Keeper and Order burns.** Keep them, given that canon Keepers are drawn for free and on-chain burns can expose who applied?
11. **Mid-term balance drops.** Mostly resolved by v0.3: entry is one-time, and civic roles are never hold-gated (proposed). Confirm.
12. **Paid extras.** Which items, prices (fixed or USD-equivalent), one-off or per season, and the treasury/burn split P%/Q%.
13. **Treasury.** Buyback share Z% of ZC fees, buyback schedule, signers and threshold, how ZC is converted for bills, and what is done with project tokens the treasury receives.
14. **Dev buy** at launch: yes or no, and how much, disclosed in advance.
15. **Token launch timing.** Proposed: after the community hub has been running (phase 2), not before a usable product exists.

**Community hub**
16. **Gate before the token exists.** Proposed in v0.3: phase 1 uses founder slots plus a ZC-only Book arrival post. Alternatives: fully open at first, or delay the hub until the token launches.
17. **Telegram migration.** Which groups to move, how long the read-only pointer period lasts, and whether to mirror announcements during the move. Who does the outreach (nothing is sent until you decide).
18. **Mobile.** PWA with web push first (proposed), or native apps early? Which extra alert channels (email, XMTP, Farcaster)?
19. **#market rules** and how strictly price talk is moderated; who the first moderators are.
20. **Bots.** Which feeds at launch, alert thresholds, and whether the game digest posts into #general by default or only for people who opt in.

**Game and project**
21. **Name.** Choose a distinctive name for the app and the token that avoids Veridia, Veridian and Snowmoon in the ticker, plus a collision check.
22. **Season length** (one in-game year = how many real weeks?). This sets Keeper terms, the quiet period and Herald draws.
23. **License flavor.** GPL-3.0 everywhere, or AGPL-3.0 for the server? Also, which moderation materials, if any, stay private?
24. **AI models.** Open-weight models (cleanest for the open pipeline) or hosted APIs (easier, but less reproducible)?
25. **Visitors at launch.** Ship Dzego and Freetown visitors with the first RPG phase, or later?
26. **Legal review.** Who, which jurisdictions to serve or geo-block. With the new token design this has to happen before the token launch at the latest (phase 0 proposed).
