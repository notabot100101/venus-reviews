# Trade-Site Revival Plan (for the next session or an OpenClaw agent)

Written 2026-08-06 overnight. Prereq reading: README.md in this repo, then
`directives/website-development-playbook.md`.

## Goal (Paul, verbatim intent)
Documents the trading bots, offers them for sale, captures leads. "Brings all
together."

## Assets ready now
- `index.html` — the live page's recovered source (do not deploy over it without Paul)
- `assets-staging/hero-grid.jpg` — 2400x1000 ambient hero (gold lattice on navy),
  generated + reviewed 2026-08-06, no text/logos; seed 201, re-derivable
- Formspree form `mlgwljjn` — LIVE, collecting; do not repoint
- Real bot documentation to draw from: `~/.openclaw/workspaces/trading-bots/`
  (PIPELINE-ROADMAP.md, REAL-MONEY-PILOT-PROPOSAL-20260805.md, daily-reports/)

## Build order
1. **v2 landing** as `v2/index.html` in this repo (never overwrite `index.html`):
   keep the existing copy blocks (hero, problem, how-it-works, backtest, FAQ,
   pricing, CTA), add the hero image, modernize layout. Static HTML, no build step.
2. **"The Bots" documentation page** — one section per bot family (grid A/B
   variants, real-money pilot). EVERY number must cite a file in the
   trading-bots workspace. Backtests labelled as backtests. **Paul approves
   which P&L figures are publishable before anything is written.**
3. **Sales/pricing** — reuse the live page's pricing block as baseline; Paul
   confirms tiers before change.
4. **Leads** — keep Formspree `mlgwljjn`; Hermes already processes AgentMail.
   The 2026-07-21 open question (HubSpot vs plain Formspree) is Paul's call.
5. Only after Paul reviews: deployment discussion (Hostinger, same rules as
   Venus production — explicit authorization, verify live after sync).

## Hard rules (from README, non-negotiable)
No invented stats/testimonials/ratings; no real balances, keys, or wallet
addresses; CREDENTIALS.md in the bots workspace is never referenced; no deploy
and no form changes without Paul's explicit go.
