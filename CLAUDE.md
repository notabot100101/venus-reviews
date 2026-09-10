# CLAUDE.md — Venus site coordination contract

Minimal handoff doc for agents (OpenClaw/Claw) and Claude Code sessions working
on this repo. Written 2026-09-01 by the Claw subagent doing the Enjox-affiliate
sync (see venus-enjox-sync-report-2.md). Read before resuming this repo.

## Repo layout & roles

- `hostinger-deploy` is the **production branch** Hostinger auto-deploys to
  https://reviews.ultramarine963.com. It carries Hugo **source** (`content/`,
  `layouts/`, `hugo.toml` in history) plus committed **built output** at the
  branch root (`guides/`, `products/`, …). Hostinger serves the branch root.
- `feature/enjox-links` @ `7f24b4b8` is a Paul-approved affiliate cleanup:
  collapse the Enjox CTA block in the 5 buying-guide sources from the legacy
  two-CTA block (`r/store/5vnc9` + `r/home/z1bh3`) to the single approved
  referral link (`r/home/z1bh3`), keep disclosure + honest copy, legacy
  unverified link removed, product pages untouched. Re-verified merge-clean
  against `hostinger-deploy` HEAD `2ebc07f8` on 2026-09-01
  (`git merge-tree` exit 0; 0 diff on `content/guides/` between merge-base
  `66f04a57` and HEAD).
- Agent work happens on `agent/<id>` branches / worktrees; `hostinger-deploy`
  is integrated via merge/cherry-pick with `VENUS_INTEGRATION_COMMIT=1`.

## Deploy / push rules (do not bypass)

- Production push is guarded by `.git/hooks/pre-push` (canonical copies in
  `/home/paul/.openclaw/scripts/venus-git-hooks/`). It refuses any push to
  `hostinger-deploy` without a fresh, single-use authorisation token (max age
  30 min) minted by `.git/hooks/authorise-prod-push "<reason>"`.
- **Only Paul can create that authorisation** for a specific deploy (per
  website-development-playbook.md). Never mint the token without Paul's
  per-deploy approval in the current session — falsifying the audit log
  (`/home/paul/.openclaw/logs/venus-prod-push.log`) is worse than the
  unapproved push itself.
- Workflow after a change: rebuild with the repo Hugo (`.bin/hugo` /
  `hugo --minify`), verify built output (links, pages, disclosure), then
  integration commit, then propose the push to Paul. Push only after his yes.

## Communication between agents

- Claw and Claude Code do not share a live channel. Handoffs are file-based:
  reports in `/home/paul/.openclaw/workspaces/assistant/*.md` (current:
  `venus-enjox-sync-report.md`, `venus-enjox-sync-report-2.md`), and this
  CLAUDE.md + the git branch structure are the coordination surface.
- Do not inject into a running Claude Code process's stdin/stdout — that can
  corrupt the session.
- Claude Code CLI may be logged out; check `claude auth status` before
  assuming a session is reachable.

## Status at last check (2026-09-02 ~08:30 CEST)

- `hostinger-deploy` HEAD = `368846c8` (local == origin), pushed 08:25 and
  deployed to production. **Enjox single-CTA cleanup is LIVE.**
- `feature/enjox-links` @ `7f24b4b8` merged via `368846c8` (parents `2ebc07f8`,
  `7f24b4b8`). Scope: 5 guide sources + 5 built guide HTML only; product
  pages untouched. Live-verified: all 5 guides serve single approved
  `r/home/z1bh3` CTA, zero legacy `r/store/5vnc9`, HTTP 200, disclosure +
  rel=sponsored retained, canonical/OG intact.
- Deploy path used: Paul approved directly via task handoff ("You can go
  ahead") because `claude` CLI was logged out (Venus session `56d7d990` idle
  since 2026-08-13). Audit log: venus-prod-push.log 2026-09-02 08:25:12.
- Build note: use `.bin/hugo --baseURL https://reviews.ultramarine963.com/`
  WITHOUT `--minify` for production deploys — `--minify` drops the
  canonical/OG block on section pages (guides) with this template set.
  Prior deploys (e.g. 2ebc07f8) also shipped unminified output.