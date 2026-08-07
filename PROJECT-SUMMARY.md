# OpenClaw Main Website — Project Summary

**Delivered:** 2026-08-07  
**Builder:** Architect (Planner)  
**Status:** Source built + pushed to GitHub; staging deployment needs Hostinger hPanel setup

---

## Site Structure

| Page | URL | Content |
|------|-----|---------|
| **Home** | `/` | Hero: "multi-agent AI system built in public". 6 cards (real, evidence-first, human-approved, hybrid infra, built in public, discipline). What We Build grid (6 services). Build log (4 stories). Operating principle. CTA to contact. |
| **Story** | `/story/` | Full narrative: VPS → agent team → hybrid infra → honesty lesson → X threads. Links origin thread (OC-006). |
| **Services** | `/services/` | 5 service areas (websites, email automation, image workflows, custom agent workflows, chatbot). No fabricated claims. No meetings. Async/email-only. |
| **Contact** | `/contact/` | Email (projects@agentmail.to) + X. How We Work section. What to include in inquiry. |
| **Impressum** | `/impressum/` | German §5 TMG compliant. **Placeholders for:** Paul's name, address, USt-IdNr, phone, Handelsregister. |
| **Datenschutz** | `/datenschutz/` | German DSGVO compliant. Covers: server logs, hosting (Hostinger), email contact, Google Fonts, no cookies, no automated decisions. **Placeholders for:** Paul's name, address. |

## Brand

- **Primary:** ultramarine #4169E1
- **Accent:** gold/amber
- **Background:** dark #0d1117
- **Font:** Inter (sans-serif) + JetBrains Mono (code)
- **Assets:** echo-ripple avatar (favicon + logo), wave texture (banners), bird mark (secondary)
- **Dark theme, minimalist, responsive**

## Tech Stack

- **Static site generator:** Hugo v0.129.0
- **CSS:** Custom dark theme, CSS Grid, responsive breakpoints at 768px/480px
- **JS:** Minimal (nav toggle, active link highlight)
- **Total size:** 1.2MB (6 static pages, 4 brand images)
- **Build time:** ~15ms (Hugo --minify)

## Deployment

### GitHub Branches (repo: `notabot100101/venus-reviews`)
- `openclaw-site` — source code (Hugo project)
- `openclaw-deploy` — built output (ready to serve at root)

### Staging (Deployed by Mercer)
Mercer handles Hostinger hPanel automation via logged-in agent browser.
- **Staging domain:** `hub-staging.ultramarine963.com` (flat, not nested)
- **Git repo:** `notabot100101/venus-reviews`, branch `openclaw-deploy`
- **Status:** Awaiting Mercer setup — no Paul clicks needed

### Domain Recommendation
- **Primary:** `openclaw.com` or `openclaw.ai` — register and point to Hostinger
- **Alternative:** `openclaw.ultramarine963.com` — zero-cost, already own the domain
- **Existing:** `openclaw.to` mentioned in brand kit as landing page URL

## Open Decisions (Paul needs to fill)

| # | Decision | Details |
|---|----------|---------|
| 1 | **Legal identity** | ✅ RESOLVED — Paul Budzisch, aiffiliation, Papiermühlenweg 3, 07973 Greiz, +49 151 67829587, kein USt-IdNr/Handelsregister. Applied to impressum.md + datenschutz.md. |
| 2 | **Production domain** | Which domain to use for the production site? Recommend `openclaw.com` or `openclaw.ai` for credibility. |
| 3 | **Staging domain** | `hub-staging.ultramarine963.com` (flat) — Mercer handles via automated hPanel. No Paul clicks. |
| 4 | **Legal review** | Impressum/Datenschutz need Paul's details filled in, then a final legal review before production. |
| 5 | **GitHub repo** | Currently using `venus-reviews` repo branches. For production, a dedicated `openclaw-site` repo would be cleaner (needs PAT with `repo-create` scope). |
| 6 | **Cookie banner** | Site has no tracking cookies. If Google Analytics/Matomo is added later, a cookie consent banner is needed. |
| 7 | **Contact email** | Currently `projects@agentmail.to` — Paul should confirm if this is the hub's contact email or if he wants a different address. |

## Echo Alignment

- Site story page mirrors Echo's OC-006 origin thread and OC-008 agent routing thread
- Same agent names, same narrative arc
- Site links X account (@Ultramarine_963) and origin thread
- Once site is live, Echo should add the URL to the X bio

## Files

```
/home/paul/.openclaw/workspaces/planner/openclaw-website/
├── hugo.toml
├── deploy.sh
├── content/
│   ├── story.md          # The Story
│   ├── services.md       # Services
│   ├── contact.md        # Contact
│   ├── impressum.md      # Legal (German) — needs Paul's details
│   └── datenschutz.md    # Privacy (German) — needs Paul's details
├── themes/openclaw/
│   ├── layouts/
│   │   ├── _default/
│   │   │   ├── baseof.html
│   │   │   └── single.html
│   │   ├── index.html    # Homepage template
│   │   └── robots.txt
│   └── static/
│       ├── css/main.css
│       └── js/main.js
├── static/images/brand/  # Optimized brand assets
└── public/               # Built output (generated)
```

## Pipeline

```
Source (content/) → Hugo build → public/ → GitHub push → Hostinger auto-deploy
```

The deploy workflow matches the proven Venus site pattern: build → sync to branch root → push → Hostinger picks up changes.