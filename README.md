# trade.ultramarine963.com — Trading Bot Landing Site

Recovered and given a repo on 2026-08-06 (overnight session). Before this, the
source existed **only** in recovery archives — the live site had no working copy
anywhere on disk.

## What this is

The half-started project Paul described as *"a website that documents our trading
bots and offers them for sale ... it had to do with Formspree and was probably
started in March this year."* Close: it was **born 2026-02-18** and became the
investor pre-registration flow on **2026-03-13**.

## Established facts (all verified 2026-08-06)

| Fact | Value | Evidence |
|---|---|---|
| URL | https://trade.ultramarine963.com/ | HTTP 200, 13,323 bytes, live now |
| Hosting | Hostinger (same account as Venus) | memory/2026-02-18.md |
| Form backend | Formspree, form ID `mlgwljjn` | `action="https://formspree.io/f/mlgwljjn"` in live HTML |
| Born | 2026-02-18 — pure-HTML landing page, "live and collecting early access signups" | archived memory/2026-02-18.md |
| Purpose shift | 2026-03-13 — pre-registration form as the professional investor contact flow (replaced ad-hoc WhatsApp contact) | archived memory/2026-03-13.md |
| Last known open item | 2026-03-19 — "Website Formspree setup still pending" (the professional contact-capture form beyond the simple email signup) | archived memory/2026-03-19.md |
| Source recovered from | `openclaw-recovery-2026-06-22-174842/.../workspace/_archive_media/landing-page.html` | byte-compared against the live page; identical modulo browser-save artifacts |

`index.html` in this repo is the archived original (the clean pre-deployment
version, not the browser-saved copy).

## Page structure as deployed

Hero → problem ("Crypto Trading Is Hard. Emotions Are Harder.") → How Grid
Trading Works → "Tested on Real Market Data" (backtest proof) → features → FAQ →
pricing → CTA → Formspree email signup.

## What Paul wants it to become (2026-08-06, verbatim intent)

> "a website that documents our trading bots and offers them for sale. This will
> be a project that brings all together."

So: evolve from an early-access landing page into a site that
1. **documents the bots** — the real ones: grid bots (SOL/BNB A/B variants,
   real-money ETH bot) whose state, reports and roadmap live in
   `~/.openclaw/workspaces/trading-bots/` (Quanta's workspace: `PIPELINE-ROADMAP.md`,
   `REAL-MONEY-PILOT-PROPOSAL-20260805.md`, `daily-reports/`)
2. **offers them for sale** — pricing exists on the current page already
3. **captures leads** — Formspree `mlgwljjn` works today; the open question from
   2026-07-21 (`workspaces/assistant/planner-status-formspree-email-system.md`)
   is whether to add HubSpot/CRM. Hermes already processes AgentMail inboxes and
   can process these leads.

## Rules carried over from the Venus project

The full discipline is in
`~/.openclaw/workspace/directives/website-development-playbook.md`. The ones that
already bit us once:

- **No invented products, stats or testimonials.** Every performance number on
  this site must trace to a file in the trading-bots workspace or an exchange
  export. Backtest claims must say they are backtests.
- **No fabricated schema.org ratings/reviews.**
- **Real profit numbers are sensitive** — Paul decides what is published.
  The bots' actual P&L files are not automatically publishable content.
- **Provenance for every image.** Ambient/decorative only unless attested.
- Deploy = serve exactly what is committed; verify live after sync.

## Do not

- Point the Formspree form anywhere else without Paul (live leads flow through it).
- Publish real account balances, API keys, exchange names tied to balances, or
  wallet addresses. `CREDENTIALS.md` in the trading-bots workspace is radioactive —
  never referenced from here.
- Deploy over the live site without Paul's explicit go (same rule as Venus
  production).
