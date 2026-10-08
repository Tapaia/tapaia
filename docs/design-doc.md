# Veridian Chat: project design doc

*Working title. Draft v0.7, Oct 7, 2026, for Angelo. Not published. **v0.7 adds ten launch-scope features drawn from the novel** (section 5.4): the room "Air" panel, "Fix Tapaia", Hood-up anonymous posts, the Dzego food truck and robot tea server, the trust list, the library shelf and Herald books, pop-up classes, inspector clubs, sortition-rated billboards and a reputation-only forecasting board. Angelo wants a **full product at token launch**, so v0.7 also adds a [launch checklist](launch-checklist.md) with what is built today and a phased build order (roadmap note in section 12). It adds the "no streak mechanics" ground rule and lists six **proposed lore fixes as pending** in section 13; they are not applied. v0.6 adds **Zipcoin names** (6.5): a wallet's `name.zipcoin.cash` becomes its verified handle with a small badge, and claiming happens on zipcoin.cash (built in the prototype). v0.5 adds two features Angelo floated the evening of Oct 7: **Societies** (user-created groups with their own entry rules; lore: Dzego's secret societies [ch9]) and **polls with quadratic voting** that can pay the poster and the voters (lore: Silverchat polling [ch27] and Gladias's QV [ch1]; section 4.1, 5.3). It also parks an **entry-routing** idea as ON HOLD (6.2.7): a one-click 1,000 ZC zipcoin Speak bought with ETH through a non-custodial contract, plus a 2.5% Tapaia fee, with an optional small $TAPAIA buy-and-burn. v0.4's tokenomics stay as the working plan (**working, decided Oct 7, 2026**): $TAPAIA on Stockereum paired against ZC at 1%, 100 free Founding Citizens, then about $5 entry (half ZC, half $TAPAIA), about $1 Speak in $TAPAIA, paid extras about half burned, buyback-and-burn from half of our fee share, and a treasury under Angelo's sole control with public monthly reports (sections 6.2, 6.3 and 7; public summary in [tokenomics.md](tokenomics.md)). Sections 4, 5, 6, 7, 11, 12 and 13 are updated. v0.3 replaced hold-to-enter with the arrival-post entry model (6.2). v0.2 added the community-hub positioning (5.2).*

Sources: `/workspace/snowmoon/briefing.md` (lore, checked against the novel text in `/workspace/snowmoon/text/`) and `/workspace/zipcoin/briefing.md` (ZC and Stockereum). Chapter numbers in brackets, like [ch1], point to the novel. Market and on-chain figures are snapshots from Oct 7, 2026, around 4:45 PM ET, and will change. Anything marked **(design choice)** is ours, not canon.

---

## 1. Pitch

Veridian Chat is two things in one app: a **community chat that can replace Telegram** for the $ZC / Snowmoon community, and a **chat-based role-play game** set in everyday Veridia, the country in Vitalik Buterin's novel *Snowmoon*, layered on top of it. The community side is ordinary out-of-character chat: announcements, general talk, market talk, support and dev updates, with notifications, mobile access and bot feeds (section 5.2). The game side lets players who want it create original citizens of Meldan. They run small businesses, get randomly drafted to rate buildings, sit on five-judge courts, and can join the Order of Steering, whose members audit businesses and vote on tax rubrics under secret assignments, numbered pseudonyms and a standing bounty for anyone who guesses their task. The game is built on the novel's institutions rather than its plot: sortition, quadratic votes, split deliberation rooms, reputation-gated spaces and burning zipcoin as a costly signal. Nobody has to role-play to use the community chat, and the game never gets in the way of normal conversation.

Entry and signaling use real tokens (**working, decided Oct 7, 2026**; sections 6 and 7). The first **100 citizens** get in free as **Founding Citizens**, with a badge and a free in-game arrival post. After that, becoming a citizen takes a one-time burn worth **about $5, half ZC and half $TAPAIA**. The ZC half is a real on-chain "Speak" post on the zipcoin Book that serves as your permanent arrival message (6.2 covers an open issue with the Book's minimum). Holding tokens is not a gate, except possibly for a few special rooms. Speaking in Tapaia Square burns **about $1 of $TAPAIA**, and a few other loud actions (knocks, running for Keeper) cost small burns too. $TAPAIA launches on Stockereum, paired against ZC with a 1% fee, and only after the app is live. The in-game economy itself (taxes, salaries, bounties, court stakes, polls) runs on non-redeemable in-game zipcoin (zc).

## 2. Ground rules from Angelo's decisions

- **Everyday life only.** No war, no pre-war or post-war framing, no battles, no military or Kungaupei plots. The Arctic Empire exists in canon, but it stays offstage and has no playable or NPC role.
- **Original characters only.** No canon characters as players or NPCs: no Gladias, Seila, Mov, Delwart, Zei, Evelor, Verdow and so on. Canon *institutions, places, brands and devices* are fair game: Meldan, Kalimar, Tapaia Square, Silverchat, Hydrafill, GPH, privacy robes, neck bands, Emerald, green circles.
- **Don't invent canon.** Wherever the game needs a rule the book doesn't give, the doc labels it **(design choice)**. The in-game codex should label it the same way.
- **No streaks or engagement traps (v0.7).** No "N days in a row" counters, loss-aversion nags or infinite feeds. People come back for scheduled gatherings and shared goals, not fear of losing something (5.4).
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
- **Polls with quadratic voting (Silverchat-style).** Canon: on Silverchat you pay or burn zipcoins to put a question to a cross-section of users, and more zipcoins reach more people [ch27]. Seila also mixes real questions with decoys so outsiders can't tell what she cares about. Canon QV: Gladias's aesthetics vote is rescaled so each person's average is 0 and mean square is 1, so going extreme on everything doesn't help [ch1].
  - *Game version (draft, ideas Oct 7, 2026):*
    1. **The poster pays to broadcast** in $TAPAIA (or in-game zc if we stay on the safer path; open, 13). Reach scales with payment, as in Silverchat.
    2. **That payment is split**, e.g. **50% shared among the voters, 30% burned, 20% to the treasury** **(design choice; exact split open)**.
    3. **Voters vote with free voice credits** under quadratic voting (same rescale as aesthetics drafts: average 0, mean square 1). They spend nothing to vote and earn a share just for answering.
    4. **Boosts:** other citizens can add funds to a poll they want more people to see; the original poster gets a cut of every boost, so a good question can pay.
    5. **Decoys and common knowledge.** Decoy questions are supported. Results are posted in the square so everyone knows the outcome and knows everyone else saw it (the canon goal [ch27]).
    6. **Societies** can run the same polls internally, scoped to their members (5.3).
  - *Anti-abuse:* only citizens who have entered can vote and earn; one vote per citizen; daily earning caps. Paying people to vote attracts bots and throwaway accounts, so founder-slot and Sybil rules (6.2.3, 11) matter here too.
  - *Payout currency (open, 13):* paying posters and voters in **real $TAPAIA** conflicts with the existing principle that the game never pays real tokens to players (6.1, 11). **Recommended:** start with **in-game zc or badges**, and only later consider real $TAPAIA for big polls, after a legal check. Angelo has not decided.
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
| **Tapaia Square** (town square) | Everyone | In-character broadcast feed: announcements, poll results, season events, and featured posts. Posting to the square is a **Speak** action and burns about $1 of $TAPAIA (burn-to-be-heard, 6.3; working, decided Oct 7, 2026). On-chain zipcoin Book posts can show in a separate, filtered "From the Book" lane. New citizens' arrival posts (on-chain, and founders' in-game ones) show in a filtered **Arrivals** lane, with the same hide-by-default rules **(design choice)**. Note that a square Speak is our own burn, separate from a zipcoin Book post (6.3). |
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
| **Societies** | Members (and public rooms the Society opens) | User-created groups with their own entry rules (5.3). |

### 5.2 Community hub layer (out of character)

The goal is that the community can move its day-to-day chat off Telegram and into this app, whether or not people play the game.

**Channels (OOC).** Plain chat with real handles, no in-world clock and no role-play rules.

| Channel | Who can post | Notes |
|---|---|---|
| **#announcements** | Team only (read for all) | Releases, monthly treasury reports, contract and treasury addresses, security warnings. Pinned "one true address" post for $ZC and $TAPAIA. |
| **#general** | Citizens (see gating below) | Everyday community talk. |
| **#market** | Citizens | Price and trading talk, kept out of #general. Rules: no paid promotion, no "guaranteed" calls, no impersonating the team. The team does not post price predictions or talk up the token here (see regulatory risk). |
| **#support** | Everyone, including people who haven't entered yet | Wallet, onboarding and bug help. Mods and helpers only ever answer in public; pinned warning that staff never DM first and never ask for seed phrases. |
| **#dev-updates** | Team; replies in a thread | Changelogs, links to the GPL repo and the running commit. |
| **#feeds** | Bots only | ZC live feed, Book posts, price alerts (below). |
| **#lobby** | Everyone | An open, read-mostly room so newcomers can see the community before buying ZC or making an arrival post **(design choice; see gating)**. |
| **#off-topic, language rooms** | Citizens | Optional, added as demand appears. |

**Access and gating.**
- **Current direction, for now:** the arrival post (section 6.2) is the gate for posting in the citizen channels. It replaces hold-to-enter as the main gate. It is also the main anti-spam measure: every paid account costs a real, non-refundable burn plus gas, and the arrival post is public and permanent, so spam accounts leave a visible trail.
- Founding Citizens (the first 100) enter free with an in-game arrival post. Founder slots are the weak point for spam and sybil farming, so they need their own limits (6.2.3).
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
- **Treasury:** posts each transaction from the published treasury wallet and each buyback-and-burn, with links, backing up the monthly reports (7.5).
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

### 5.3 Societies (user-created groups)

> **Idea, Oct 7, 2026 evening.** Angelo wants user-made channels or groups with their own entry rules. The lore-accurate name is **Societies**.

**Lore.** Chapter 9: Dzego's secret societies run payments, reputation and governance on cryptographic networks ("the ones that handle payments and reputation and manage governance for Dzego's secret societies") [ch9]. The book has no clans or guilds. **"Circle" is avoided** so it isn't confused with green pay circles. Secret-society flavor fits Dzegojan visitors especially, but any citizen can found a Society **(design choice)**.

**What a Society is.** A user-created group with its own room (or set of rooms), membership list and entry rules. It can be in-character (a Veridia Society) or out-of-character (a community club); the room header says which. Societies sit alongside the fixed rooms in 5.1 and the OOC channels in 5.2; they don't replace #general or Tapaia Square.

**Entry rules the creator sets** (one or a combination) **(design choice):**
- **Hold an amount** of ZC and/or $TAPAIA (same caveats as optional holder rooms, 6.2.6);
- **Burn to enter** (ZC, $TAPAIA, or both);
- **Invite only;**
- **Founders only** (Founding Citizen badge required);
- or a mix (e.g. burn *or* invite).

**Possible extras (open):**
- A **creation cost in $TAPAIA** (about half burned, half to the treasury, matching paid extras in 7.4), so Societies aren't free spam.
- **Society shops:** a Society can run a ground-floor shop / private room under the same rules as "your own shop" (7.4), still audited and taxed in-game.
- Societies can run **internal polls** with the same QV mechanics as square polls (4.1), scoped to members.

**Open:** who can create one (any citizen vs a Rep threshold); max Societies per citizen; whether Society entry burns count toward anything else; moderation (Society mods vs platform mods); and whether OOC Societies share the same creation cost.

### 5.4 Launch-scope features from the novel (v0.7)

> **Decided Oct 7, 2026 (v0.7):** Angelo added all ten features below to the launch plan. He also wants a **full product at token launch**, not a bare prototype. The build order and status are in [launch-checklist.md](launch-checklist.md).
>
> **Principles these features follow** (same as the rest of this doc):
> - **No real-token payouts to players** (6.1). Rewards are badges, cosmetics, communal unlocks or in-game zc.
> - **Nothing that looks like gambling.** No stakes, wagers or prize draws you pay into.
> - **No streak mechanics.** No "N days in a row" counters, no loss-aversion nags, and no infinite feeds. Canon frames attention extraction as the bad guy: Bluewhale wanted "to control people's attention more and extract more money" [ch3:58], and "the internet can be as addictive as drugs" [ch23:170].
>
> **Conventions in this section:**
> - Citations are chapter:line in `/workspace/snowmoon/text/`, and quotes are verbatim.
> - Anything not in the book is marked **(extrapolation)**, which means the same as **(design choice)** elsewhere in this doc.
> - Effort: **S** = days, mostly UI and copy. **M** = one to two weeks with new server logic. **L** = more than that.
> - Ranked by impact vs effort.

#### 5.4.1 Room "Air" panel. Effort S
- **What users see:** every room header has a small watch-style readout, styled after the canon watch screen:
  - **CO2** (a number);
  - **Attested ✓ N**: verified members present (a citizen with a wallet session, or a verified Zipcoin name);
  - **Unknown ? N**: non-citizens, demo accounts and accounts with no verified identity.
  - When unknown accounts cluster, the line turns red: **"Unknown, increased risk!"**
  - Tapping the panel explains what each number means.
- **Rules:**
  - **CO2 tracks activity.** It is a function of messages per minute and the number of people present. It rises when a room is busy and falls back when it calms down **(extrapolation: canon CO2 is real air quality)**.
  - **Ventilation.** Above a threshold, the room shows "ventilating…" and switches to slow mode automatically. In line with the canon rubric, this applies only to rooms with more than 20 people present. Slow mode lifts on its own when CO2 falls.
  - **Risk line.** The "increased risk" line appears when unknown accounts reach a threshold share of a room or show a burst of joins. Its tooltip repeats the standing scam warnings: staff never DM first, never share your seed phrase, and check contract addresses.
  - Thresholds are public and set in config **(extrapolation)**.
- **Canon:**
  - The watch readout: "Air / CO2 906 / PM2.5 4.4 / Devices / Attested ✓ 16 / Unknown ? 0" [ch11:186–199].
  - "Attested ✓ 21 / Unknown, increased risk! 4" [ch19:30–33].
  - The clean indoor air rubric "Applies to spaces that host more than 20 people" [ch6:105].

#### 5.4.2 "Fix Tapaia": a community revival project. Effort M
- **What users see:**
  - A **Coordination Score** meter on the Tapaia Square banner, with the current goal ("A playground kids actually like", "Real books in the library", "Shops people use").
  - Each milestone visibly changes the square's art: a new playground, filled library shelves, lit shopfronts.
  - A **"Tapaia vs Galanar"** card compares us with the livelier square nearby, as a friendly rivalry.
- **Rules:**
  - **What fills the meter** (each with per-person daily caps so no one can farm it): arrivals, hosted events and pop-up classes (5.4.7), library books accepted (5.4.6), assembly turnout, food-truck gatherings (5.4.4), and billboards rated (5.4.9).
  - **Milestones are permanent.** The meter never decays and nothing is taken away (no streaks).
  - **Choosing goals.** Each season, a Herald-run (or, before Heralds exist, team-run) assembly picks the next goal. The assembly uses canon tables of ten taking turns, followed by a multi-item QV ballot.
  - **Rewards are communal and cosmetic only:** square art, a "helped fix Tapaia" badge. No token payouts.
  - The meter, inputs and milestones are **(extrapolation)**. The new Cozy HD art (in progress, see the checklist) supplies the before/after scenes.
- **Canon:**
  - Tapaia "the playground is much more basic, my son says it's not even comfortable. And I always get the feeling that that one is less lively than Galanar" [ch6:221].
  - Its shops are "putting things in that theoretically qualify but that nobody actually wants to use" [ch6:227].
  - Galanar has "a mini library and science museum" [ch6:199].
  - "A Coordination Score is not a property of a person - it's a property of an entire community" [ch18:271].
  - Assembly format: "five tables, each with ten chairs" [ch6:135], with "everyone at each table to take turns" [ch6:183].
  - The canon assembly topic was improving public spaces [ch6:153], and "Keepers check the results when they're debating their tax rubrics" [ch6:205].

#### 5.4.3 "Hood up": anonymous posts with a credential. Effort M
- **What users see:**
  - In rooms that allow it, the composer has a **Hood up** toggle.
  - The post shows as **"Anonymous"** with one credential line the poster chooses, such as "Citizen ✓", "Founding Citizen ✓", "Zipcoin name holder ✓", and later "Rep ≥ 200 Verified ✓" once Rep ships (4.4).
  - The avatar is the uniform dark-purple privacy robe with the hood up. **Hood down** returns to your normal name.
- **Rules:**
  - **Where it's allowed:** opt-in per room, e.g. a feedback room, AMA questions and scam reports. Never in #announcements or #market, and off by default in Societies (the Society chooses).
  - **Limits:**
    - Citizens only.
    - Rate-limited.
    - One credential line per post, and it must be true at posting time.
    - Anonymous posts are not threaded to each other, so they can't be linked by reply chains **(extrapolation)**.
  - **Honesty:**
    - The UI states plainly that **Tapaia's server knows who posted**, as with Order pseudonyms (4.3).
    - Moderators can act on abuse, and abuse removes the poster's Hood-up rights.
    - Never claim canon-level ZK anonymity.
- **Canon:**
  - Delwart's first message arrives as "Anonymous / Rep score ≥ 200 Verified ✓" [ch1:354–356].
  - Robes make people indistinguishable: "Were they male, female, young or old, he could not tell" [ch1:249].
  - The hood as a social signal: "Mov removed the hood on his privacy robe, a gesture to appear less threatening" [ch20:164].

#### 5.4.4 Dzego food truck + robot tea server. Effort S
- **What users see:**
  - **The truck.** A few times each Meldan day, a banner says "Dzego food truck in 7 minutes", followed by a short countdown. The truck then "parks" in Tapaia Square for a few minutes with a numbered menu.
  - **Orders.** People order with in-game zc and a short line appears in the square ("Orla picked up a Number Ten"). The truck then leaves.
  - **The tea house.** A labelled NPC **robot server** slides up with a menu when you enter, takes tea orders and offers refills.
- **Rules:**
  - The schedule is fixed and published in Meldan ticks, so people can plan to gather **(extrapolation: canon trucks deliver to homes)**.
  - Orders cost in-game zc only and include the in-game sales tax (4.2).
  - Menu numbers follow canon (Number Ten is the rice and vegetable dish with mushrooms). Other dishes are **(extrapolation)**.
  - **No streaks:** no "visited N days in a row" and no penalties for missing the truck. The truck is a reason to show up, not an obligation.
  - Bots and NPCs are labelled, as in section 8.
- **Canon:**
  - "Well, the Dzego food truck is coming in seven minutes" / "Sure! I assume the number ten for you again?" [ch1:281, ch1:283].
  - "Dzego food truck in one minute. The usual I assume?" [ch11:310].
  - Number Ten is "a vegetable and rice dish covered with mushrooms" [ch19:143–145].
  - "A robot slid up to him, and showed him a menu" [ch6:235].
  - "the robot had already refilled it four times" [ch15:150].

#### 5.4.5 Trust list (contextual presence). Effort S
- **What users see:**
  - A **Trust list** on your profile.
  - People on it can see which room you're in and your status line ("on my way to the tea house").
  - Everyone else sees only here, idle or offline. A "hide presence" option shows nothing at all.
- **Rules:**
  - **One-way grants.** Adding someone doesn't add you to theirs. You can remove people at any time, and they're not notified.
  - Order pseudonyms and Hood-up posts are **never** revealed through the trust list.
  - Later, Emerald can suggest a temporary unlock for a planned meetup **(extrapolation)**.
- **Canon:** "You put me on your trust list a year ago and never took me off, so our local AIs had permission to enable location sharing" [ch3:46].

#### 5.4.6 Library shelf + Herald books. Effort S
- **What users see:**
  - Tapaia's library becomes a room with **shelves** of long-form "books": guides ("How to claim a Zipcoin name", "Staying safe from scams"), lore notes with citations, translations, and session write-ups.
  - Books by Heralds get a **Herald book** label.
  - A "quiz me" button asks Emerald for a short quiz on a book (needs the AI service, 8).
- **Rules:**
  - Any citizen can submit a book: a title, a shelf and Markdown text up to a length cap.
  - Volunteer librarians (mods at first) accept books. Accepted books count toward Fix Tapaia.
  - **Starting state.** In keeping with canon, the shelves start nearly empty: a few dull "business books" and untranslated Old Belpakian and Haragmir spines. We never write fake Old Belpakian text; those spines simply can't be opened **(extrapolation)**.
  - Lore books must cite chapter:line and keep canon separate from fan additions.
- **Canon:**
  - "All the books are either some boring business books, or things in foreign languages nobody understands, either Old Belpakian or something from Haragmir" [ch6:223].
  - Heralds: "Some give speeches, others write books, others help organize assemblies" [ch6:169].
  - "He asked Emerald to come up with a quiz related to the information he viewed so far" [ch6:107].

#### 5.4.7 Pop-up classes. Effort S
- **What users see:**
  - A **Classes** board.
  - A citizen schedules a short class (topic, host, start tick). At the start tick, the class room "decrypts" and is announced to people who tapped *Remind me*, DU-style.
  - Attendees get an attendance badge for that class, and the host can turn notes into a library book.
- **Rules:**
  - Any citizen can host, with a cap of N classes per week and normal moderation.
  - **Topics:** wallet safety, how Tapaia works, the novel's mechanisms, Dzegoban phrases. Dzegoban classes use **canon-attested words only**, and we don't invent vocabulary.
  - No paid entry at launch (event tickets in 7.4 stay a separate, later paid extra).
  - The last-minute reveal is flavor: rooms are not secret from the server **(extrapolation)**.
- **Canon:**
  - The autobus poster: "Education is every Veridian's responsibility and duty for a lifetime" [ch1:255].
  - DU: "The exact location of the classroom should be getting decrypted and broadcasted any moment now" [ch2:50].

#### 5.4.8 Inspector clubs. Effort S
- **What users see:**
  - An **#inspectors** room and an **Inspector** badge.
  - Volunteers publish reports on what they reviewed: a commit of the GPL repo, bot code, AI prompts, or a range of treasury and buyback transactions. Each report has a summary and findings.
  - The team replies publicly to each finding.
- **Rules:**
  - **Report template:** scope (commit hash or tx range), method, findings, severity.
  - Reports are signed with the author's wallet as a plain message signature (never a transaction).
  - The badge carries **no powers** and no payouts. Open-source contributor bounties from the treasury (7.5) stay a separate, published program.
  - Reports go to the library's "Inspections" shelf.
- **Canon:** Dzego's rule that "anyone can go and unscrew any camera in public and inspect it themselves. There's entire clubs that do it and publish their reports online" [ch5:164].

#### 5.4.9 Billboards on the square, rated by sortition. Effort M
- **What users see:**
  - A billboard strip on Tapaia Square showing rotating in-world posters from businesses, Societies, classes and events.
  - Drafted citizens get "Rate this poster" in their day, using the same −5..+5 slider as aesthetics drafts (4.1).
  - An NPC **Hydrafill** runs parody ads as the house gag, labelled as NPC.
- **Rules:**
  - **Posters:** a fixed-size pixel-art template plus a short caption. Moderation pre-checks each one.
  - **Banned content:** anything promoting "gambling or risky investment" or "excessive display of wealth" (canon Tier 4/5). That means **no token shilling, prices or "pumps" on billboards**.
  - **Rating:** a small random panel rates each poster. Ratings are normalized per rater (mean 0, mean square 1, with the growing-weight edge case in 4.1).
  - **Display time** scales with the score.
  - **The featured slot** uses **randomize-above-cutoff**: every poster in the top 10% has an equal chance.
  - **Paid slots (optional, 7.4).** A poster slot can be a paid extra in $TAPAIA, about half burned. **Payment never changes ratings or the featured draw.**
  - Rating posters is how aesthetics drafts work before players own property **(extrapolation)**.
- **Canon:**
  - Gladias "wished that it had been the Hydrafill advertisement that he had been selected to vote on" / "We need more fun in the world." [ch1:269, ch1:271].
  - At his hearing, the thing he wished he'd voted on was "A Hydrafill billboard" [ch8:180].
  - The Tier 4 criteria include "gambling or risky investment, excessive display of wealth" [ch1:174].
  - Randomize-above-cutoff: "If the committee says you're in the top ten percent, you have the same chance of getting in, no matter if you're at ninety one or ninety nine" [ch17:144].

#### 5.4.10 Forecasting board (reputation only, no money). Effort M
- **What users see:**
  - A **Forecasts** board of questions with a deadline, such as "Will Fix Tapaia reach milestone 2 this season?" or "Will the next Society poll have 50+ voters?".
  - Citizens set a probability (1–99%) and can update it until the deadline.
  - After questions resolve, each person gets a public **Forecaster score** (Brier-based) and a leaderboard.
- **Rules:**
  - **No stakes of any kind.** There is no zc, no tokens, no prizes, and nothing to buy or trade. It is reputation only.
  - **Banned questions:** token or crypto prices, markets, and anything about real people's private lives.
  - **Questions:**
    - Proposed by citizens and approved by mods, later by Heralds.
    - Each has written resolution criteria.
    - Resolved publicly with a link to the evidence.
  - A score shows only after N resolved questions.
  - Forecaster score may later feed Rep (4.4) **(extrapolation)**.
  - This deliberately takes the canon idea **without** Silverchat Predict's betting.
- **Canon:**
  - Verdow on Veridia's missing institution: "There's no position where you have to stand up and say - if we do X, then Y will happen - and you rise up if you're right, and fall if you're wrong" [ch32:102].
  - Silverchat Predict "lets people - or bots - make bets on future events" [ch27:126], with Gladias naming "two weaknesses" [ch27:128].

**Dependencies:**
- Food-truck orders need the in-game zc ledger.
- Billboards need the sortition draft and QV normalizer.
- Hood-up's Rep credential needs Rep v1.
- Library quizzes need the AI service.
- The [launch checklist](launch-checklist.md) orders the build around these.

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

> **Changed in v0.4 (working, decided Oct 7, 2026).** The tokenomics placeholders are replaced with Angelo's decisions: 100 free Founding Citizens, then an entry burn of about $5 split half ZC and half $TAPAIA; a square Speak of about $1 in $TAPAIA only; paid extras about half burned; a 1% fee with half of our share going to buyback-and-burn; and a treasury Angelo controls alone at first, with public monthly reports (6.2, 6.3, 7). Where earlier text conflicts, v0.4 wins.

> **Changed in v0.5 (ideas, Oct 7, 2026 evening).** Adds **Societies** (user-created groups; 5.3) and expands **polls** into a paid quadratic-voting feature that can compensate posters and voters (4.1). Parks an **entry-routing** alternative as ON HOLD (6.2.7): one-click 1,000 ZC Speak via ETH through our non-custodial contract + 2.5% fee, optional small $TAPAIA buy-and-burn; swapping $TAPAIA into ZC was considered and rejected. Open: pay poll earners in real $TAPAIA vs in-game currency first (13). Where v0.5 adds features, it sits on top of v0.4; where it conflicts on entry, the ON HOLD note in 6.2.7 wins only if adopted.

### 6.1 Two kinds of money in the app

| | Real tokens ($ZC + $TAPAIA) | In-game zc (play money) |
|---|---|---|
| **Used for** | The entry burn (about $5: half ZC as an on-chain arrival post, half $TAPAIA, 6.2); small burns for loud actions, e.g. about $1 of $TAPAIA per square Speak (6.3); buying paid extras in $TAPAIA (7.4); optionally, holding for specific gated rooms (6.2.6). | Taxes, salaries, business sales, court stakes, polls, the guess bounty, loans. |
| **Where it lives** | The player's own wallet. We never hold it. | Our database ledger. |
| **Can it pay out to a player?** | **No, under the standing rule.** Burns go to a dead address; about half of each paid-extra payment is burned and the rest goes to the treasury. Nothing in the game sends real tokens to a player (event prizes included, 7.4). **v0.5 exception under discussion:** paid polls that compensate posters and voters in real $TAPAIA would break this (4.1, 13). | It can move between players, but it can't be bought, sold or redeemed. Recommended currency for poll rewards at first. |

Keeping every payout (bounties, court awards, salaries, and for now poll rewards) in play money is what keeps the game away from gambling and wagering rules, so that line stays unless Angelo deliberately accepts the extra risk for real-$TAPAIA poll payouts (13).

### 6.2 Entry: the arrival post (citizenship and chat access)

> **Working, decided Oct 7, 2026.** The first 100 citizens enter free as Founding Citizens. After that, entry is a one-time burn worth about $5, split half ZC and half $TAPAIA. This can still change before launch. It replaced hold-to-enter (v0.2) as the primary gate.

**How it works**
- To become a citizen (post in the citizen channels and get citizen actions: drafts, courts, the Order), a player makes a one-time **entry burn worth about $5** from their own wallet, **split half ZC and half $TAPAIA**.
- The ZC half is a **real on-chain Speak post on the zipcoin Book**. That post is the player's **permanent arrival message**: public, on-chain forever, and tied to their wallet. The $TAPAIA half is a plain transfer to the dead address; both can be batched into one signature (EIP-5792).
- Zipcoin's Speak mechanics (from the briefing, and `/rules` checked at 8:25 PM ET on Oct 7): a post burns **at least 1,000 ZC** (`floorZc`) through ZipBroadcaster and holds up to 280 bytes. Message size and tier are relative to the 7-day median burn, so a larger burn gets a bigger post. The @zipcoinbook bot reposts burns to X, and Ethereum gas is paid on top. Zipcoin sets these rules, not us, and they can change, so the app reads the current rules (`/rules`) rather than hardcoding them. `/rules` now also lists Book boards (e.g. `snowmoon`, `builders`), which may help with tagging (6.2.1).
- **Open issue: the Book minimum is bigger than the ZC half.** At 8:25 PM ET on Oct 7, ZC was about $0.017 (`/stats`), so the 1,000 ZC minimum was about **$17**. That is more than the whole ~$5 entry, let alone its ~$2.50 ZC half. Options: (a) the ZC half is whatever the Book minimum is, so entry really costs about $17 + $2.50 at today's price; (b) the ZC half is a plain burn to the dead address, the arrival message shows in our own Arrivals lane, and a real Book post becomes optional; (c) revisit the $5 target if ZC's price changes a lot. To decide before entry ships.
- Entry is a **one-time** burn per account. Nothing has to stay locked or held afterwards, so a later sale or price drop never removes citizenship.
- Both halves go to burn (dead) addresses. Entry is **not** treasury revenue.
- **Before $TAPAIA exists.** The token launches only after the app is live (7.2), so entry can't include a $TAPAIA half at first. Proposed: the founder window covers the pre-token period; if the 100 slots fill before launch, interim entry is the ZC half only. (Open, 13.)
- Canon fit: loose. Veridian citizenship isn't bought in the book, but burning zipcoin as a costly, public signal is canon [ch19, ch20]. This is a **design choice**.

**6.2.1 The arrival flow**
- The app helps the player write the arrival message and shows a preview, the burn amounts in ZC and $TAPAIA with approximate dollar values, the gas estimate, and a clear warning: "this is permanent and public, can't be deleted, and will be reposted to X." The player signs from their own wallet; we never hold keys or tokens.
- The app verifies both burns on Ethereum RPC (sender = the account's wallet, amounts at least the entry amounts, made after sign-up) before granting citizenship. **To verify before building:** whether a third-party app can tag its Book posts (the `/words` API has a `board` filter and `/rules` lists boards, but whether apps can set one is unconfirmed) so arrival posts can be told apart and filtered.
- Open: whether a Book post made *before* signing up can count as an arrival post (convenient for existing zipcoin posters, but easier to game).

**6.2.2 Founding Citizens (free entry for the first 100)**
- The first **100** citizens get in **free**, with no on-chain burn (**working, decided Oct 7, 2026**).
- They get a **"Founding Citizen" badge**. It carries no votes, Rep or powers, and it can't be transferred.
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

**6.2.4 Turning ~$5 into token amounts (open)**
The dollar targets are decided (entry about $5, square Speak about $1, 6.3; **working, decided Oct 7, 2026**). How the app turns dollars into ZC and $TAPAIA amounts is still open. Entry, Speak and paid extras (7.4) should all use the same method:

| Method | How it works | Pros | Cons |
|---|---|---|---|
| **Fixed token amounts, reviewed on a schedule** | Set ZC and $TAPAIA amounts worth about $5 (or $1) at review time, and re-set them on a published schedule (e.g. per season) by a published rule. | Simple and predictable; needs no oracle; can't be manipulated. | The real dollar cost drifts between reviews (ZC has moved by large percentages within days, per the briefing). Reviews can feel arbitrary unless the rule is published. |
| **USD-equivalent via an on-chain TWAP** | At signing time, compute the amounts worth $5 from a time-weighted average price over a long window on the main pools, with sanity bounds. | The cost stays close to the dollar target. | Spot prices on thin v4 pools are easy to push around, and a new $TAPAIA/ZC pool will be the thinnest of all. More code and more things that can break; the token amounts change every time. |
| **External price oracle** | Read a third-party price feed. | Less pricing code on our side. | There's probably no feed for a new ZC-paired token, and it adds a dependency. |

A middle path is fixed amounts with a published review rule, plus live dollar estimates shown before signing. Never use a single spot read. Because Book post size is relative to the 7-day median burn, the same ZC amount can produce a smaller or bigger post from week to week.

**6.2.5 The entry split: half ZC, half $TAPAIA (decided)**
- **Working, decided Oct 7, 2026:** the entry burn is half ZC (through the Book post, subject to the open issue in 6.2) and half $TAPAIA (a transfer to the dead address).
- This ties entry to both tokens. Newcomers need a little $TAPAIA once, but never have to keep holding it.
- The costs: a second token to buy, and copycat risk. The onboarding flow links straight to the correct Stockereum page (7.7). It still needs the same legal check as the rest of the token design.

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

**6.2.7 Entry routing alternative — ON HOLD (idea, Oct 7, 2026 evening)**

Angelo is sitting on this; it is **not** adopted. If it is, it replaces the ~$5 half-ZC / half-$TAPAIA entry in 6.2.

- **Problem it solves.** Zipcoin Speak needs at least **1,000 ZC** (about **$16** at evening Oct 7 prices), so a ~$5 entry can't also be a real Book post (open issue in 6.2).
- **Proposal:** entry is a **one-click 1,000 ZC zipcoin Speak** bought with **ETH** through **our non-custodial contract**. The contract swaps ETH → ZC, burns the Speak as the player's arrival post on the Book (so every new citizen shows up publicly in the ZC community), and takes a **2.5% Tapaia fee**, shown clearly before the user confirms. The swap and burn happen in **one transaction from the user's wallet**; we never hold funds.
- **Optional add-on:** a small (~**$2–3**) **$TAPAIA buy-and-burn** in the same flow, so every entry also buys on our pool and shrinks supply. Without it, entry only touches ZC.
- **Rejected alternative:** requiring users to swap **$TAPAIA into ZC** for entry. That would make every new citizen a seller of $TAPAIA (sell pressure), add a step before joining, and was dropped.
- **Fee note:** 2.5% is on the high side vs typical wallet-swap fees (often under 1%), but it bundles the swap and the burn; show it before confirm. On a ~$16 Speak, 2.5% is about $0.40 — a small extra income stream, not a main one.
- **If adopted:** update 6.2, 6.2.5, 7.3, the public [tokenomics.md](tokenomics.md), and the open Book-minimum item in 13. Until then, the working plan stays the ~$5 split.

### 6.3 Burn-to-be-heard (game actions)

Canon basis: burning zipcoin is how Veridians show they're serious, e.g. a knock that burned 50 zipcoins [ch20] and the costly-signal posts [ch19]. The game makes a few loud actions cost a **small burn**. The square Speak is decided; the others are still placeholders:

| Action | Burn | Notes |
|---|---|---|
| **Speak** in Tapaia Square (in-character broadcast) | **about $1 of $TAPAIA** (working, decided Oct 7, 2026) | $TAPAIA only, so chatting needs one balance. Ordinary district-room and OOC messages stay free. Paying more could boost visibility, as in the canon costly signal **(design choice)**. |
| **Knock** on a door | c ZC + d $TAPAIA (placeholder) | Lets you reach someone who hasn't opened DMs to you. |
| **Enter the Keeper draw** for a season | e ZC + f $TAPAIA (placeholder) | Canon Keepers are drawn at random with no cost; the burn here is a **design choice** to make entering the pool a signal of intent. It buys a place in the draw, never a seat, a vote or an outcome. |
| **Order advancement** (applying as Acolyte, requesting the hearing) | g ZC + h $TAPAIA (placeholder) | Part of the Order ranks in 7.4. The burn must be the same for both tracks so it doesn't reveal whether you chose Sentinel or Keeper. |

**How burns are made (to decide):**
- **Burn per action, on-chain.** Each action is a wallet-signed transaction sending both tokens to `0x…dEaD` (or a small burn contract that does both in one call and tags the action). Most honest, but every action costs Ethereum gas on top of the burn, and waiting for a transaction is slow for chat. A batched wallet call (EIP-5792) can make it one signature.
- **Burn ahead for action credits (proposed).** The player burns a larger amount once and gets a matching number of non-transferable, non-redeemable action credits in the app. We never hold the tokens (they're destroyed), so there's no custody, and each action is instant. The burn is still real and public; it just happens before the action rather than with it.
- **Fixed amounts vs USD-equivalent** has the same trade-off as the entry burn (6.2.4): fixed amounts are simple but their real cost swings; USD-equivalent needs a price oracle.
- **Not the zipcoin Book.** These are our own burns. Posting to zipcoin's Book (≥1,000 ZC through ZipBroadcaster) is now used once for the entry arrival post (6.2); beyond that, it stays a separate opt-in feature.

Burned tokens reduce supply. They are **not** treasury revenue.

### 6.4 Other ZC features
- **"Post to the Book" (opt-in, after entry):** the same flow as the arrival post (6.2.1), for later posts. Write a message, preview it, confirm a clear warning ("this is permanent, public and costs ≥1,000 ZC plus gas"), then sign a Speak burn from your own wallet. Shown in the "From the Book" lane with a "🔥 real burn" badge.
- **Names:** see 6.5. A wallet's Zipcoin name becomes its verified handle. (Our own paid name claims in 7.4 are in-app character and handle names, a separate namespace.)
- **Never** auto-mirror chat to the chain, and never pay out real tokens from game outcomes.
- **Zip/unzip:** out of scope. The privacy pools are mixer-adjacent with a small anonymity set (82 deposits per the briefing). Linking to zipcoin.cash is enough.
- **To verify before building:** whether a third-party app can tag its Speak posts so they can be filtered (now important, because entry depends on recognizing arrival posts) (the `/words` API has a `board` filter, but whether apps can set one isn't confirmed; check `docs/api-v1.md`), and whether `@zipcoin/agent` can build unsigned transactions for a browser wallet. If not, call the MIT-licensed contracts directly with viem.

### 6.5 Zipcoin names (v0.6, built in the prototype)

Zipcoin names are claimed by burning ZC: a Book word with `/claim alice` on its envelope gives `alice.zipcoin.cash` and `alice.zipbook.eth` (an ENS name that resolves to the holder). The Book is the registry: zipcoin.cash derives it from chain events, and the first valid claim in chain order wins. A 5+ letter name burns one row (1,000 ZC at the Oct 7 room). Four letters cost a card and three letters a large word (10x and 100x the room). Names for well-known people are kept for the owner of the matching `.eth`, and a few house words are reserved outright. All of this is published as data at `/api/v1/rules`.

- **Identity.** At wallet sign-in (SIWE) the server looks up the wallet's name through `GET /api/v1/identities/:address` (field `zipName`). The answer is cached for 10 minutes and refreshed when the user reconnects. If the wallet holds a name, it becomes the account's @handle in community channels, everywhere names appear: messages, @mention autocomplete, member lists, DMs, profile cards, and the arrival and Speak cards. The role-play **citizen name** stays separate and editable, and the verified name stays visible on the profile. If zipcoin.cash is unreachable, we keep the last good answer, or fall back to the short address (`0x1234…abcd`). We never guess.
- **Verified badge.** A small green seal sits next to the name, with the tooltip "Verified Zipcoin name: alice.zipcoin.cash". Demo names use a grey dashed seal ("Demo Zipcoin name … not a real zipcoin.cash registration") so they can never pass as verified. One name maps to one Tapaia account, and a real holder always replaces a demo copy. If a name is released or transferred, the badge goes away on the next lookup.
- **Claim flow.** The profile has a "Get a Zipcoin name" panel. It checks availability (debounced) through `/api/v1/names/check` and shows one of these states: available, taken, reserved (house word or kept name), invalid, or can't reach zipcoin.cash. It shows the burn cost from the API (`priceZc`, plus zipcoin.cash's own USD estimate). **Tapaia never sends the transaction.** Real wallets get a deep link to zipcoin.cash's own claim form, prefilled (`/names?name=alice`), where they burn from their own wallet, then a "Check my wallet again" button. Demo accounts get a simulated claim labelled "DEMO: nothing is burned".
- **Real in-app claim (later, not built).** It would be non-custodial and sent from the user's wallet. Either (a) `ZC.approve(ZipBroadcaster, amount)`, then `ZipBroadcaster.speak(amount, "alice.zipcoin.cash is mine.", "/claim alice")`, where the third argument is the envelope (≤120 bytes) and `amount` is at least the `priceZc` returned by `/names/check`; or (b) an ETH buy-and-burn route like zipcoin.cash's "With ETH only" option; or (c) an anonymous claim from a zipped note with `/claim alice 0x…` on the envelope. Before granting the badge we would still confirm the name through `/identities` (or by replaying the registry rules over chain events).
- **Why it helps Zipcoin.** Every claim is a burn, so each Tapaia citizen who wants a real name reduces the ZC supply and appears on zipcoin's Book and names page. Showing verified names also gives people a reason to claim one, and it makes impersonation harder in a community where scams target newcomers.

## 7. Project token on Stockereum, paired against ZC

> **WORKING, decided Oct 7, 2026.** This section (and the token parts of sections 6, 11, 12 and 13) records the tokenomics Angelo decided on Oct 7, 2026. They are the plan, but the numbers can still change before launch. Nothing here is a commitment to holders or a promise about price or returns, and it all needs a legal check before launch. The public, plain-language summary is [tokenomics.md](tokenomics.md).

### 7.1 How Stockereum works (from the briefing)
- It's a Uniswap v4 hook launchpad on Ethereum with no bonding curve. One transaction mints exactly 1B tokens and puts the whole supply into a single-sided position. The creator deposits no quote asset and pays only a creation fee (amount not found).
- The hook owns the liquidity, so it **can't be pulled**.
- The token template is fixed-supply, with no owner, no mint, no pause and no proxy.
- **ZC is an allowed quote asset.** 167 ZC-paired launches existed on the evening of Oct 7 (only 4 had graduated), e.g. SC/Silverchat, ZB and DZHAMSTER.
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

### 7.2 Chosen direction (working, decided Oct 7, 2026)
1. **Launch on Stockereum, paired against ZC (not ETH), and only after the app is live.** Every buy of $TAPAIA goes through ZC, and creator fees accrue in ZC.
2. **Fair launch.** A fixed supply of 1,000,000,000 $TAPAIA, all of it placed in Stockereum's single-sided Uniswap v4 position. The hook owns that position and has no code path to shrink it, so the liquidity can't be pulled (7.1). **No presale, no team allocation, and no dev buy planned.** If the team ever buys, it discloses the amount and wallet publicly. The team uses the app with tokens bought on the open market like anyone else, and says so.
3. **Fee tier 1%** (matches ZC). Stockereum keeps 0.5% and Tapaia gets 0.5% of volume, in ZC. Our share is split **half to buyback-and-burn of $TAPAIA, half to running costs and prizes**.
4. **Utility in the app:** half of every entry burn (6.2.5), about $1 per square Speak (6.3), and the currency for paid extras, about half of which is burned (7.4). It may also gate specific holder rooms (optional, 6.2.6).
5. **The token's job is to fund the project** (hosting, AI inference, moderation, development, prizes) from fees and activity.
6. **No holder revenue share or yield.** HolderDistributor stays off. See 7.6.

This is close to what v0.1 called a "utility token" and did not recommend, because it ties access to price. Since v0.3, entry is a one-time burn, so holding the token is never required to be a citizen. Angelo has chosen this direction; the trade-offs are tracked as risks in section 11.

### 7.3 Revenue streams

| Stream | What it is | Goes to | Notes |
|---|---|---|---|
| **(a) Stockereum creator fee** | The trade fee on every buy and sell of $TAPAIA. **Decided: 1%** (matches ZC). | Treasury, in ZC | The platform keeps 0.5% and we get 0.5% of volume (per the briefing). Our 0.5% is split half (0.25% of volume) to buyback-and-burn of $TAPAIA and half (0.25%) to running costs and prizes, the same shape as ZC's Veridian sales tax. Income depends entirely on trading volume, which may be thin. Illustration only, not a forecast: $100K of daily volume would bring $500 a day before the split. |
| **(b) Burns** | The entry burn (half ZC, half $TAPAIA, 6.2), square Speak ($TAPAIA, 6.3), and knocks and Order actions. | Nobody (burned) | Reduces the supply of both tokens. **Not treasury revenue.** |
| **(c) Paid extras** | Cosmetics, your own shop, Order ranks and event tickets, priced in $TAPAIA (7.4). | About half burned, about half to the treasury | Cosmetic, social and access items only. They must not buy votes, audit results, court outcomes, Rep or Order seats. |

Fee tier note (decided Oct 7, 2026): 1%, matching ZC. A lower fee keeps traders and volume, which matters more than the rate; ZC holders already accept 1%. 2% would net 1% and 3% would net 2%, but both make a likely thin pool more expensive to trade. The tier can never change after launch.

### 7.4 Paid extras (working, decided Oct 7, 2026)
Everything is priced in $TAPAIA. About **half of each payment is burned** (to `0x…dEaD`) and **half goes to the treasury wallet**, so spending also reduces supply. Payment is a wallet transfer from the player, verified on RPC (9.7). No extra can buy votes, audit results, court outcomes, Rep or Order seats.
- **Cosmetics:** robe colors, avatar items, a tea-table spot in the square, and name colors. Canon robes are uniformly dark purple [ch1], so Order rooms keep the uniform robe and robe colors show everywhere else **(design choice)**.
- **Your own shop:** a ground-floor storefront on Tapaia Square that doubles as a private room you can decorate. It's a nod to the canon rubric for ground-floor active use, which people game with shops nobody uses [ch6]. A paid shop is still audited and taxed in-game like any business, and buying one doesn't change its ratings; citizens still rate it.
- **Order ranks:** Acolyte, Sentinel, Keeper and Herald. Rising takes a burn **plus a track record of activity** (audits done, prediction score, the hearing), so a rank can't be bought outright. The canon rules in 4.3 still apply on top. Sentinel and Keeper are secret tracks, so both cost the same and the public badge shows "full standing" without naming the track. Keeper seats are drawn at random and Heralds are randomly retired members, so the burn buys eligibility, never the seat. The thresholds are open.
- **Event tickets:** tea-house nights, AMAs and Minpentai tournaments. A paid ticket plus a real-value prize can look like a wager, so prizes are cosmetics, badges or in-game zc, or real-value prizes go only to free-entry contests (6.1, 11). This needs the legal check.
- **Still open:** exact prices (using the method chosen in 6.2.4), whether items are one-off or per season, and the rank thresholds. The earlier extras ideas (building-style packs, guild rooms, name claims) are parked. If name claims come back, reserve canon character names and real people's names, as zipcoin does for "kept" names.
- **Societies (v0.5):** a creation cost in $TAPAIA and Society shops are possible paid extras tied to 5.3; same half-burned rule if adopted.

### 7.5 Treasury policy (working, decided Oct 7, 2026)
- **Sole control at first.** Angelo holds the treasury alone in a **dedicated treasury wallet** that is used for nothing else. Its address is published in the repo, the site, #announcements and the app footer. It receives the ZC creator fees and the treasury half of paid extras.
- **Monthly public reports** of fees earned, tokens bought back and burned, and spending, linking every transaction. The #feeds bot posts treasury moves as they happen (5.2).
- **A stated plan to move to a multisig** later, e.g. at 1,000 citizens or once the treasury reaches a set size, with the signers and threshold published then.
- **Buyback and burn:** half of the ZC fee revenue buys $TAPAIA from the pool and burns it. The other half funds running costs and prizes under a published spending policy (hosting, AI inference, moderation, open-source contributor bounties, audits, prizes).
- Treasury buybacks go through our own pool and pay its fee like any other trade. At the 1% tier, half of that fee comes back to us as creator fee and the platform keeps the other half.
- **Dev buy:** none planned. If one is ever made, disclose the amount and wallet publicly.
- **Still to decide:** the treasury address (once the wallet is created); the buyback schedule (a fixed schedule is transparent but easy to front-run, while ad hoc buys are harder to front-run but look discretionary); how and when ZC is converted to pay bills, since fees accrue in ZC and bills are in dollars; a stated rule for the $TAPAIA the treasury receives from extras (hold or burn; selling it would look like the team dumping); and the exact multisig trigger.
- Sole control is a trust risk and a key-loss risk (section 11). Use a hardware wallet with a tested backup.

### 7.6 What we must not promise (keep this)
- Revenue comes from **trading fees and in-app activity**. It belongs to the project and pays for the project. It is **not** a share owed to holders.
- **No holder revenue share, dividends, staking yield or HolderDistributor rewards.** These make the token look like an investment in our work, which is how securities rules are usually triggered.
- Buyback-and-burn is a supply policy, not a price promise. Describe it factually, don't market it as "number go up", and keep it within the published policy. Get a legal view on it specifically, because buybacks funded by revenue can also be read as returning value to holders.
- No price talk from the team in #market or anywhere else. No roadmap promises tied to the token price.

### 7.7 Copycats and name collisions
- "Veridia" and "snowmoon" tokens already exist on-chain (listed at theordereth.xyz). There's an X account @Veridia_zc, and veridia.tv is a separate adaptation. Many fake "ZC"/"zipcoin" tokens exist on Stockereum. One even launched *before* the real ZC.
- **Don't** name the token or ticker "Veridia", "Veridian" or "Snowmoon". Pick a distinctive name and check it against `stockereum.com/api/graduations`, GeckoTerminal and X before launch.
- Publish the one true contract address in the repo, the site, #announcements and the app footer. The app hardcodes both the ZC address and the project-token address, and the entry, burn and any hold-check flows only accept those exact contracts.
- Expect copycats of our token within hours of launch. Because $TAPAIA is burned at entry (6.2.5), and may be used for holder rooms, a copycat could trick newcomers into buying the wrong token: the onboarding flow should link buyers straight to the correct Stockereum page, `https://stockereum.com/t/<address>`, and the #feeds bot flags other addresses.
- The app's own name should also avoid confusion with veridia.tv and @Veridia_zc. "Veridian Chat" is a placeholder; Tapaia / $TAPAIA is the working name.


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
   │        ├── Game engine (sortition, audits, courts, Keeper votes, polls/QV, Societies, bounties, seasons)
   │        ├── Randomness service (public beacon + commit-reveal; all draws auditable)
   │        ├── AI service (GM, NPCs, Emerald, summaries; prompts in repo)
   │        ├── Moderation service (filters, reports, mod queue, scam/wrong-address detection)
   │        └── Chain indexer (zipcoin.cash /api/v1 + /live SSE; burns, extras payments, treasury; verifies on RPC)
   ▼
Ethereum mainnet (ZC token, $TAPAIA + Stockereum pool, ZipBroadcaster, ZipDoorstep, treasury wallet) – read via RPC + zipcoin API
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
- **Arrival-post check:** confirm on RPC that the account's wallet made the entry burns (the ZC Speak post through ZipBroadcaster and the $TAPAIA transfer to the dead address, each at least the entry amount, 6.2.1) before granting citizenship. Founder slots are granted in our database and recorded publicly (count used, rule applied).
- **Hold check (only for optional gated rooms, 6.2.6):** read ZC and project-token balances by RPC for the hardcoded contract addresses only, using the check model chosen there (live, periodic or snapshot, with a grace period).
- **Burns and extras:** verify burns (transfers of both tokens to `0x…dEaD`) and paid-extras payments (about half to the treasury wallet, half to the dead address) on RPC before granting the action, credits or item.
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
| **Regulatory: real-money stakes** | Real-value bounties, wagers on guesses, paid polls with payouts, paid event tickets with real-value prizes, or redeemable credits could count as gambling or money transmission, depending on jurisdiction. Privacy-pool features are mixer-adjacent. **v0.5:** polls that pay posters and voters in real $TAPAIA would deliberately break the "never pays real tokens to players" rule (4.1, 6.1). | All payouts (bounties, court awards, salaries, and poll rewards at first) stay in non-redeemable in-game zc or badges. Real tokens are only held or burned, or paid to the treasury for extras, unless Angelo later accepts real-$TAPAIA poll payouts after a legal check (13). Burn-ahead credits are non-transferable and non-redeemable. Event prizes are cosmetics, badges or in-game zc, or real-value prizes only for free-entry contests (7.4). No custody. |
| **Entry burn excludes newcomers** | To join after the founder slots run out, someone needs a wallet, ETH for gas, and enough ZC and $TAPAIA for the entry burn, which is spent for good. They also have to be willing to post something permanent and public. That's a lot of friction for a Telegram replacement and shuts out curious readers of the novel. | Open #lobby, #support and #announcements; a clear onboarding guide; keep entry at about $5 and resolve the Book-minimum gap (6.2); show current cost in dollars (burn plus gas) before asking anyone to buy; founder slots for the existing community. |
| **Permanent on-chain arrival posts and moderation** | Every paid citizen's arrival post is permanent, public and reposted to X by @zipcoinbook. Someone could pay to make abuse, slurs, scam links or someone else's personal data their arrival post, and we can't delete it. It also permanently links the wallet to joining the community, which some people won't want. | Preview, warning and explicit signature; suggest short, safe arrival messages; hide abusive arrival posts in the app (filtered Arrivals lane, hide-by-default rules) and remove citizenship; say so in the code of conduct; never re-broadcast. Tell people up front that the link between wallet and community is public. |
| **Sybil farming of free founder slots** | Free entry is the cheapest way into the app, so one person could grab many founder slots with many wallets, take badges and stack drafts, juries and the Keeper pool. | One slot per wallet; a founder window; invite list or community allowlist published as a rule; probation before the badge is final; Rep thresholds for civic roles; optional proof-of-personhood (6.2.3). |
| **Poll payout farming** | Paying voters (and posters via boosts) attracts bots and throwaway accounts, especially if rewards are real $TAPAIA. | Only entered citizens vote and earn; one vote per citizen; daily earning caps; prefer in-game rewards first (4.1, 13). |
| **Society spam / paywalled echo chambers** | Free Society creation could flood the sidebar; burn-to-enter Societies could look like selling access. | Creation cost in $TAPAIA if adopted; platform moderation still applies; Society entry never buys civic roles (5.3). |
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
| **Treasury conduct and sole control** | Angelo holds the treasury alone at first, so holders have to trust one person and one key, and a lost or stolen key loses the treasury. Selling $TAPAIA received from paid extras, or unclear spending, would look like the team dumping. Predictable buybacks can be front-run. | A dedicated wallet with a published address; monthly public reports; bot-posted transactions; a stated rule for the $TAPAIA the treasury receives; a public plan to move to a multisig (e.g. at 1,000 citizens); a hardware wallet with a tested backup. |
| **Permanent on-chain messages (beyond arrival posts)** | Book posts can't be deleted and are reposted to X by @zipcoinbook. A player could post abuse or personal data permanently. | Never auto-post. Require preview, warning and explicit signature. Filter on display. Ban the player in-app for abusive burns, and say so in the code of conduct. |
| **Copycats and impersonation** | Fake ZC tokens exist, plus existing "Veridia"/"snowmoon" tokens. Newcomers buying ZC for the entry burn could buy a fake ZC, and because $TAPAIA is also burned at entry, a fake $TAPAIA could fool them too. Fake-support DMs are the most common community scam. | Hardcode and publish addresses; onboarding links straight to the right pool; bot flags other addresses; reserved team handles; "staff never DM first". |
| **Community hub becomes a price room** | If market talk dominates, the community drifts toward speculation, which hurts both the game and the regulatory picture. | Separate #market channel with rules, team stays out of price talk, moderation. |
| **Moving off Telegram fails** | People may not leave Telegram, splitting the community across two places. | Make the hub useful on mobile with notifications first; a migration period with pointers; announcements mirrored during the move. |
| **Sybil accounts** | Wallets are free, so one person can farm drafts, juries and Keeper seats. The entry burn raises the cost per paid account but doesn't stop a well-funded person, and founder slots are free (see the founder-farming row). | Entry burn per paid account, founder-slot limits, Rep thresholds for drafts and Order roles. Optional proof-of-personhood later. Rate limits. Sortition weighted by account age and activity **(design choice)**. |
| **Operator knows the secrets** | The server can see pseudonym mappings, sealed rooms and votes. | Say so clearly. Minimize access. Follow the ZK roadmap in 9.6. |
| **AI drift and cost** | The GM could invent canon or slip into war plots, and inference costs scale with players. | Lore file plus guardrails. Label non-canon content. Cache outputs. Set per-player Emerald quotas. |
| **Endorsement confusion** | Players may assume Vitalik is involved. | Disclaimers everywhere. No use of his name in marketing beyond the credit. |

## 12. Roadmap

There are no dates; each phase ends when its exit criteria are met. **The community hub is the MVP; the RPG layers on top of it.** Token steps follow section 7 (working, decided Oct 7, 2026).

> **v0.7: full product at token launch.** Angelo wants the token to launch on a full product, not a bare prototype. The phases below describe the build sequence. The **token launch (Phase 2 below) now waits until the launch scope is live**: the hub, real entry, Societies, QV polls, the in-game zc ledger, the aesthetics draft, Rep v1, the character upgrade and the ten features in 5.4. The current status and the proposed launch build order (phases A–E) are in [launch-checklist.md](launch-checklist.md). What counts as launch scope vs the first seasons after launch is open decision 28.

**Phase 0: Foundations**
- Pick a name for the app and the token (collision-checked). Create the GPL repo with LICENSE, README credit and disclaimer, and a canon codex with chapter citations.
- Write the code of conduct (OOC and IC sections). Get a legal consult on the token design (entry burn and founder slots, burns, revenue, buybacks, optional holder rooms) and on the in-game zc design, before anything launches.
- *Exit:* repo public, codex reviewed against the novel, legal consult done.

**Phase 1: MVP, community hub (the Telegram replacement)**
- SIWE login, handles (ENS/zipbook display), one account per wallet, optional linked wallets.
- OOC channels: #announcements, #general, #market, #support, #dev-updates, #feeds, #lobby.
- Entry v1: the arrival post. Founder slots for the first 100 citizens, with the "Founding Citizen" badge, free in-game arrival posts and the chosen anti-farming rules. $TAPAIA doesn't exist yet, so if the slots fill before it launches, interim entry is a **ZC-only** Book arrival post (open, 6.2). Filtered Arrivals lane. #lobby, #support and #announcements stay open.
- Before this ships: confirm whether third-party apps can tag Book posts, resolve the Book-minimum gap (6.2) and the USD-to-token pricing method (6.2.4), and test the arrival flow on a mainnet fork.
- Mobile PWA with web push notifications, mentions, DMs, mutes and digests.
- Read-only bots: ZC live feed, Book posts (filtered), price and liquidity.
- Moderation and anti-spam: report queue, rate limits, slow mode, reserved team handles, scam-link and wrong-address filters.
- Telegram/X onboarding guide and migration plan (no outreach until Angelo approves).
- *Exit:* the community's daily chat runs in the app for a full migration period without major moderation or reliability problems.

**Phase 2: Token launch**
- Final legal check. Create the dedicated treasury wallet and publish its address, the spending policy and the buyback rule (half of fee revenue).
- Fee tier: 1% (decided). No dev buy planned; disclose publicly if that ever changes. Prepare copycat warnings.
- Launch on Stockereum paired against ZC, only once the app is live, with holder rewards off. Publish the address everywhere; the app hardcodes it.
- Switch entry for new citizens to the ~$5 burn split half ZC and half $TAPAIA (6.2.5); existing citizens are never asked to re-enter. Optional hold-gated rooms (6.2.6) only if Angelo wants them. Treasury bot live.
- *Exit:* entry flow working for new citizens with no unresolved complaints; first monthly treasury report published.

**Phase 3: Veridia, everyday Meldan (the RPG layer)**
- Character creation (citizen or visitor), and the "Veridia" sidebar group alongside the community.
- Tapaia Square, district rooms, doors with knock-first DMs.
- Burn-to-be-heard for square Speak (about $1 of $TAPAIA) and knocks (chosen burn model; burn-ahead credits if adopted).
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
- Polls with sampling, decoys, quadratic voting, boosts, and the chosen payout currency (in-game first recommended; 4.1, 13). Verifiable sortition published.
- Societies: create, set entry rules, optional creation cost and Society shops; internal polls (5.3).
- Paid extras in $TAPAIA (cosmetics, your own shop, Order ranks, event tickets; Society creation/shops if adopted), about half burned and half to the treasury.
- Opt-in "Post to the Book" with warnings and the "🔥 real burn" badge, and the filtered "From the Book" lane.
- *Exit:* at least one rubric change passed by players. Bounty, court and burn flows tested on a mainnet fork (`anvil --fork-url`, per zipcoin's local dev docs) and then on mainnet with small amounts.

**Phase 5: Depth**
- Minpentai exhibitions (reuse a fan build if the license allows), Helisport scoring and Nim.
- Reputation-backed in-game loans with nullifier-style one-use rules.
- Privacy upgrades (membership proofs, including for any hold-gated rooms).
- Native mobile apps if the PWA isn't enough.
- More rubrics, and Graph Funding committees for in-game public projects.

## 13. Open decisions for Angelo

Decided in v0.4 (**working, decided Oct 7, 2026**; can still change before launch): a 1% fee tier, with our 0.5% split half to buyback-and-burn and half to running costs and prizes; a fair launch (the whole 1B supply in the locked Stockereum pool, no presale, no team allocation, no dev buy planned); 100 free Founding Citizens; entry about $5, half ZC and half $TAPAIA; square Speak about $1 in $TAPAIA only; paid extras (cosmetics, your own shop, Order ranks, event tickets) about half burned; a treasury under Angelo's sole control at first, with a published address, monthly reports and a multisig later; and the token launches only after the app is live.

Added in v0.5 (ideas, not decided): **Societies** as the lore name for user-created groups (5.3); **polls with QV**, boosts, and a draft payment split (4.1). **ON HOLD:** entry as one-click 1,000 ZC Speak via ETH + 2.5% fee, optional small $TAPAIA buy-and-burn (6.2.7).

Decided in v0.3: entry by an arrival post; Founding Citizens with a badge and a free in-game arrival post; hold-to-enter demoted to an optional tool for specific gated rooms.

Decided in v0.2 (public multisig and hold-to-enter since replaced): token on Stockereum paired against ZC; token as a revenue generator; burn-to-be-heard; revenue from the creator fee and paid extras; buyback-and-burn from ZC fees; no holder revenue share; community hub as the MVP with the RPG on top.

**Token and economy**
1. **USD-to-token pricing.** How the ~$5 entry, ~$1 Speak and extras prices become ZC and $TAPAIA amounts: fixed amounts reviewed on a schedule, an on-chain TWAP, or an oracle (6.2.4).
2. **Book minimum vs the ZC half.** The Book's 1,000 ZC floor (about $16–17 on the evening of Oct 7) is above the whole ~$5 entry. Pay the floor, burn the ZC half without a Book post, or revisit the target (6.2). **Related ON HOLD:** the one-click 1,000 ZC Speak routing in 6.2.7 would replace the ~$5 model if adopted.
2a. **Entry routing (ON HOLD).** Adopt 6.2.7 (ETH → 1,000 ZC Speak + 2.5% fee, optional ~$2–3 $TAPAIA buy-and-burn) or keep the ~$5 half-ZC / half-$TAPAIA burn? Swapping $TAPAIA into ZC was rejected.
3. **Founder slots.** The count is decided (100). Still open: the founder window and which anti-farming rules (one per wallet, invite list or allowlist, probation, proof-of-personhood) (6.2.3).
4. **Arrival-post rules.** Whether a pre-existing Book post can count; what happens to citizenship if an arrival post is abusive; suggested guidance for what to write.
5. **Open areas.** Which rooms can be read or used before entering (proposed: #lobby, #support, #announcements).
6. **Hold-gated rooms.** Keep hold-to-enter at all, and if so for which specific rooms, with which thresholds J/K and check model (6.2.6).
7. **Other burn amounts** (knock, Keeper draw, Order advancement: c–h in 6.3). The square Speak is decided at about $1 of $TAPAIA.
8. **Burn mechanism.** Per-action on-chain burns, or burn-ahead non-redeemable action credits (proposed), and whether to write a small burn contract or use plain transfers to the dead address.
9. **Keeper and Order burns.** Keep them, given that canon Keepers are drawn for free and on-chain burns can expose who applied?
10. **Order rank thresholds.** What burn and track record each rank needs (7.4), with the same cost for both secret tracks.
11. **Paid extras.** Exact prices, one-off or per season, and how event prizes avoid looking like wagers (7.4). The split is decided (about half burned).
12. **Treasury.** The treasury address once the wallet is created, the buyback schedule, how ZC is converted for bills, a rule for the $TAPAIA the treasury receives, and the exact multisig trigger (e.g. 1,000 citizens or a set treasury size) (7.5).
13. **Mid-term balance drops.** Mostly resolved by v0.3: entry is one-time, and civic roles are never hold-gated (proposed). Confirm.

**Polls and Societies (v0.5)**
14. **Poll payout currency.** Pay posters and voters in **real $TAPAIA**, or start with **in-game zc / badges** and only later consider real $TAPAIA for big polls? **Recommended: in-game first.** Real $TAPAIA conflicts with "the game never pays real tokens to players" (6.1) and raises regulatory risk (11). Angelo has not decided.
15. **Poll payment split and boosts.** Keep the draft 50% voters / 30% burned / 20% treasury? Poster cut of boosts: what percent? Daily earning caps: what amounts?
16. **Societies.** Creation cost? Who can create (any citizen vs Rep threshold)? Caps per citizen? Society shops? OOC Societies on the same rules? (5.3)

**Community hub**
17. **Gate before the token exists.** Proposed: phase 1 uses the 100 founder slots, then (if they fill before $TAPAIA launches) a ZC-only Book arrival post. Alternatives: fully open at first, or delay the hub until the token launches.
18. **Telegram migration.** Which groups to move, how long the read-only pointer period lasts, and whether to mirror announcements during the move. Who does the outreach (nothing is sent until you decide).
19. **Mobile.** PWA with web push first (proposed), or native apps early? Which extra alert channels (email, XMTP, Farcaster)?
20. **#market rules** and how strictly price talk is moderated; who the first moderators are.
21. **Bots.** Which feeds at launch, alert thresholds, and whether the game digest posts into #general by default or only for people who opt in.

**Game and project**
22. **Name.** Tapaia / $TAPAIA is the working name (this doc's title still says Veridian Chat). Run the collision check (Stockereum graduations API, GeckoTerminal, X) before launch.
23. **Season length** (one in-game year = how many real weeks?). This sets Keeper terms, the quiet period and Herald draws.
24. **License flavor.** GPL-3.0 everywhere, or AGPL-3.0 for the server? Also, which moderation materials, if any, stay private?
25. **AI models.** Open-weight models (cleanest for the open pipeline) or hosted APIs (easier, but less reproducible)?
26. **Visitors at launch.** Ship Dzego and Freetown visitors with the first RPG phase, or later?
27. **Legal review.** Who, which jurisdictions to serve or geo-block. With the new token design this has to happen before the token launch at the latest (phase 0 proposed). Poll payout currency (14) should be in that consult if real $TAPAIA is on the table.

**Launch scope (v0.7)**
28. **What "full product at token launch" includes.** The [launch checklist](launch-checklist.md) proposes two groups:
    - **Before the token:** the hub, real entry, Societies, QV polls, the in-game zc ledger, the aesthetics draft, Rep v1, the character upgrade and the ten features in 5.4.
    - **The first seasons after launch:** the Order, courts, knocks and mini-games.
    - Confirm, or move items across.
29. **Settings for the 5.4 features:**
    - Air thresholds (CO2 formula, ventilation trigger, "increased risk" share);
    - which rooms allow Hood-up;
    - food truck times;
    - billboard panel size and display-time curve;
    - forecast question rules and the minimum resolved count before a score shows.
30. **Hosting budget.** A full launch needs an always-on paid instance and a managed database (the free Render plan sleeps and wipes data on restart). Pick a host and a monthly budget.

**Proposed lore fixes, pending (v0.7; not applied, waiting for Angelo)**
These came out of the novel review on Oct 7, 2026. Nothing in this doc has been changed for them yet.

- **P1. Poll payouts.**
  - 4.1 currently shares 50% of a poll's fee among voters and gives the poster a cut of boosts.
  - In canon the fee goes to the platform: "You can burn zipcoins - well, pay zipcoins to the company" [ch27:36], and when Silverchat ran the poll itself "they get a hundred percent of the fee back" [ch27:48]. Payment buys priority: "you need a high priority level" [ch27:40].
  - Paying people to take part is the book's exploit: Bluewhale's "You donate ten zipcoins and get back twenty" [ch11:244].
  - Proposed: the poster pays for reach and priority; voters get at most a badge or Rep; drop the poster's cut of boosts.
  - Also: QV normalization needs many ratings per person ("All his votes would be automatically shifted, stretched or squeezed…" [ch1:108]), so polls should be multi-item ballots.
- **P2. Robe colors.**
  - 7.4 sells robe colors.
  - In canon the robe is "a loose-fitting dark purple dress… privacy robe wearers all wore shoes of the same dark purple color" [ch1:132], so that "Were they male, female, young or old, he could not tell" [ch1:249].
  - Proposed: robes stay uniform purple everywhere; sell ordinary clothes and accessories instead.
- **P3. Order badges and audits.**
  - 7.4 shows a public "full standing" badge, and 4.3 gives Acolytes a solo audit queue.
  - In canon, membership is secret: "the faux pas of revealing to a stranger his status as an Order member" [ch6:173]; "HEY EVERYONE, IT'S AN ORDER MEMBER!" [ch1:221]. Only Heralds go public, after they have no power [ch6:165]. Acolyte audits are group chats: "nine Acolytes assigned to this audit, split into three groups of three" [ch1:213].
  - Proposed: no visible Order badge except for Heralds; don't market ranks as cosmetics; Acolyte audits in 3×3 rooms.
- **P4. Free square chat.**
  - 5.1 says every square post is a ~$1 Speak, but the prototype already has free "Say" plus optional Speak.
  - Canon Tapaia is where "you can sit down, drink tea, there are shops nearby" [ch6:221]. Burns are rare signals to strangers: "burning a hundred zipcoins at his doorstep" [ch20:164]; the 400 zc broadcast [ch19:188].
  - Proposed: in-character chat is free, and Speak is the optional paid card.
- **P5. Single Veridian names.**
  - The prototype's seed citizens use Anglo first-plus-last names (Nessa Quill, Corvin Ashdale), and one is billed as "Keeper of the tea cart schedule", although Keeper is the secret Order role.
  - Veridians in the book go by single invented names: "Hi, I'm Pelae." [ch6:141]; "I'm Alagael, I've been a Herald for seven years" [ch6:153]; "I'm Lectoby." [ch20:318]. "No surnames" is an observed pattern, not a stated rule **(extrapolation)**.
  - Canon tea is served by robots: "a robot slid up to them, bringing tea" [ch29:96].
- **P6. Emerald honesty label** (smaller, same review).
  - Canon Emerald is "the local AI running from Gladias's hand device" [ch1:24], and ours runs on our server (section 9).
  - Proposed: say so in the UI, and later consider an optional in-browser model.
