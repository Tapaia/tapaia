# Tapaia

*A town square in Veridia.*

**Tapaia** is an open-source town square set in everyday **Veridia**, the country in Vitalik Buterin's novel [*Snowmoon*](https://vitalik.eth.limo/snowmoon/). It's a place for the Zipcoin and *Snowmoon* community to chat, role-play and gather — meant to replace Telegram for day-to-day hangouts — with an optional chat-based role-play RPG layered on top. [Zipcoin](https://www.zipcoin.cash/) (ZC) is the currency that powers the square, the way a game has its in-world money. The name comes from **Tapaia Square**, a town square in Meldan.

Nobody has to role-play to use the community hub. The game never gets in the way of normal conversation.

## Status

**Design phase, with a working Phase 1 prototype** in [`app/`](app/) (demo mode, no wallet needed; it never sends a transaction). This repository holds the design, license, prototype code, and (soon) AI prompts and lore files. Tokenomics for **$TAPAIA** are a working plan decided Oct 7, 2026 (numbers may change before launch); see [docs/tokenomics.md](docs/tokenomics.md).

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/Tapaia/tapaia)

The button deploys the prototype as a free Render web service from [`render.yaml`](render.yaml). See [app/README.md](app/README.md#deploy) for details.

## What we're building

1. **Community hub (out of character)** — announcements, general chat, market talk, support, and bot feeds. The MVP and Telegram replacement.
2. **Veridia RPG (in character)** — original citizens of Meldan, sortition drafts, courts, businesses, and the Order of Steering, built on the novel's institutions (not its war plot).
3. **$TAPAIA on Stockereum** — fair launch paired against Zipcoin (ZC) once the app is live: 1% fee, no presale, no team allocation. See the [tokenomics page](docs/tokenomics.md).

Entry (working plan): the first 100 citizens get in free as Founding Citizens. After that, new citizens make a one-time burn of about $5, half ZC and half $TAPAIA, with a public arrival message. Speaking in Tapaia Square burns about $1 of $TAPAIA.

## Roadmap (summary)

| Phase | Focus |
| --- | --- |
| **0** | Foundations — this repo, code of conduct, legal consult, canon codex |
| **1** | MVP community hub — SIWE login, channels, arrival-post entry, PWA, moderation |
| **2** | Token launch on Stockereum (ZC pair); treasury and policy |
| **3** | Veridia RPG layer — rooms, burns for loud actions, businesses, sortition |
| **4** | Order of Steering, courts, paid extras |
| **5** | Depth — minigames, privacy upgrades, more rubrics |

Phases have exit criteria, not fixed dates. Details: [docs/design-doc.md](docs/design-doc.md).

## Docs in this repo

| Path | What it is |
| --- | --- |
| [docs/tokenomics.md](docs/tokenomics.md) | $TAPAIA tokenomics, the short public version |
| [docs/design-doc.md](docs/design-doc.md) | Full project design (draft v0.4) |
| [docs/phase1-spec.md](docs/phase1-spec.md) | Phase 1 community hub spec (draft) |
| [app/](app/) | Phase 1 hub prototype (web app + Node WebSocket server) |
| [design/](design/) | Visual reference and Phase 1 mockups (current: [mockups-v2](design/mockups-v2/), first take: [mockups](design/mockups/)) |
| [docs/lore/](docs/lore/) | Canon codex and setting files (coming) |
| [prompts/](prompts/) | AI prompts and harness (coming; required by the book's license) |
| [CONTRIBUTING.md](CONTRIBUTING.md) | How to contribute |
| [LICENSE](LICENSE) | GNU GPL v3 |

## Credit

Setting and institutions drawn from ***Snowmoon*** by Vitalik Buterin  
https://vitalik.eth.limo/snowmoon/  
released under the **GNU General Public License v3.0**.

This project publishes its source, AI prompts, lore files, and other non-commodity materials under GPL v3 so others can build on the work, in the spirit of the novel's license note.

## Disclaimer

**Tapaia is not affiliated with, endorsed by, or connected to Vitalik Buterin, the Ethereum Foundation, zipcoin.cash, Stockereum, or any related project.**

Zipcoin (ZC), $TAPAIA, and any other crypto-assets mentioned here are speculative. **Nothing in this repository is financial advice.** Tokenomics are a **working plan** and may change before launch; they are not a commitment or a promise of price or returns. Do your own research. Never share seed phrases or private keys; project staff will never DM you first asking for them.

## License

[GNU General Public License v3.0](LICENSE) — see `LICENSE` for the full text.
