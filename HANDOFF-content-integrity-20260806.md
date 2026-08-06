# Handoff: content integrity pass, 2026-08-05/06

For any agent picking this up cold. Written by Forge (worker) at the end of a long
Claude Code session. Everything below was verified against the repo, not recalled.

---

## 1. Status right now

**DEPLOYED.** `9382a61..f89ca56` went to production on 2026-08-06 and was verified live:
52 sitemap URLs and 63 internal links resolve, 0 product JSON-LD declaring a placeholder as a
product image. The catalogue below is what production serves.

**One commit is NOT pushed: `20aa043`** (classifier scans css/js, review count derived, /lab/
disallowed in robots.txt). It needs a fresh single-use token - see the authorisation rule in
`website-development-playbook.md`.

**Pushing needs Paul's explicit per-instance authorisation.** He has not given it. Do
not push because this file says the work is finished — it is finished *locally*.

Merged and verified locally:

| Commit | What |
|---|---|
| `62b69dc` | provenance classifier rewritten to fail closed |
| `7e99953` | 12 AI product renders off the Best For pages; `.product-thumbnail` styled |
| `36d8492` | "ESSENCE REVIEWS" hero banner removed |
| `4055e8b` | bvee-original-rabbit + womanizer-2-original unpublished; rating markup dropped for 3 unverified products |
| `e0cc7bf` | misspelled `lovethoney-desire` tree removed |
| `16e30e4` | prices unified on front matter, researched figures |
| `c1dca75` | LELO corrected Swiss→Swedish; Mona 2 no longer described as air-pulse |
| `307e5aa` | `.htaccess` redirects repointed off retired pages |
| `02751a7` | last AI product renders retired (lelo-hugo, lelo-sona-2, lovehoney-desire) |
| `9ff54dd` | 3 sourced reviews merged (Satisfyer Pro 2, LELO GIGI 2, Womanizer Premium 2) |

Catalogue: **13 published products.** Published content, rendered pages and listing
cards all agree at 13 — check all three if you change the catalogue.

Last verified: 52 sitemap URLs and 55 internal links, zero broken.

---

## 2. The principle, because it explains every change

The site published things nobody had checked against a source, and documented them as
verified. Concretely, all of these were live:

- AI-generated renders of real trademarked products, several depicting the **wrong
  product** — `product-lelo-hugo.png` showed an air-pulse clitoral stimulator labelled
  as the Hugo, which is a prostate massager; `product-we-vibe-chorus.jpg` had the
  We-Vibe wordmark rendered **mirrored**
- **Two products that do not exist** — "Bvee Original Rabbit" (no such manufacturer)
  and "Womanizer 2 Original" (no such SKU), one with a photoreal AI render and a
  schema.org 4.6/5 rating emitted to Google
- Every product appearing on two pages had **two different prices**, up to 3.5x apart
- LELO described as **Swiss** (it is Swedish, Stockholm) nine times, including
  "precision manufacturing from Geneva's finest" — Geneva was invented outright
- The Mona 2 called an **air-pulse** device on a page while its own review said it is not

**The rule that follows: absence of evidence is not evidence.** If provenance or a
factual claim cannot be traced to a source, it is UNKNOWN and must not be published as
fact. `scripts/remove-prod-unverified-images.py` enforces this for images and exits
non-zero while any UNKNOWN remains. Nothing enforces it for prose yet — that is the
biggest remaining gap.

---

## 3. Verification method — and the traps

Serve the branch root over a static server and check real URLs. Do not trust greps.

```bash
python3 -m http.server <free-port> --directory /home/paul/.openclaw/workspaces/worker/venus-site
```

Traps that produced wrong answers in this session, all of them mine:

- **`.htaccess` is not honoured by `python -m http.server`.** URLs that 301 in
  production show as 404 locally. I reported "5 broken links" that were never broken.
  Cross-check against the `Redirect 301` lines before calling anything broken.
- **`rglob('*.html')` descends into `.claude/worktrees/`**, which holds full checkouts
  of *other branches*. That inflated a link check from 3 broken to 51. Always exclude
  `.git`, `public`, `archive`, `.claude`, `.backup`.
- **Ports 8899/8901/8902 are used by other agents.** Probe for a free one.
- **Do not hand-edit XML with regex.** I corrupted `sitemap.xml` that way (63 `<url>`
  blocks where 52 were expected) and only caught it on verification. Use
  `xml.etree.ElementTree`.
- **`grep -c "Around $"`** — a trailing `$` is an end-of-line anchor. Use `grep -F`.

---

## 4. Open items

**Highest value first.**

1. **Push `20aa043`.** Needs Paul's per-deploy approval and a fresh token. Everything else is live.
2. **Hero banner — partly resolved, and my earlier claim was wrong.** `images/hero-banner.jpg`
   is NOT orphaned: it is referenced by `.hero-lab-magazine` in `site-polish.css` and renders at
   `/lab/hero-banners/`, which returns 200 on production. That is the "ESSENCE REVIEWS" mock.
   Nothing real links to it and `robots.txt` now disallows `/lab/`, so it is out of the index -
   but the page is still reachable if someone has the URL. The live homepage banner is a
   different, correct file (`hero-banner---a0d189fc-....jpg`, abstract plum satin, no product) and
   Paul has said to keep it. A wide 2400x1000 spare exists at
   `workspaces/image-creator/venus-images/hero/venus-hero-wide.png`, unused.
3. **Placeholders — done.** ambient-01..12 now live; every product has its own except
   womanizer-premium-2, which shares ambient-01. A 13th would make them unique.
4. **`lovehoney-desire` price is UNVERIFIED** and flagged as such in its front matter.
   No reliable retailer figure was found. Do not invent one.
5. **No product photography at all** now, deliberately. The only legitimate routes are
   brand press kits or affiliate-programme asset libraries. **Verified:**
   `we-vibe.com/press` exists and offers a press kit PDF plus `press@we-vibe.com`.
   **`lelo.com/press` is a 404** — Architect asserted it confidently and it does not
   exist; check before relying on any such URL. Press assets normally carry
   editorial-use licence terms; read them before using on an affiliate site.
6. **Unmerged work from other sessions**, all one commit each:
   - `fix/remove-invented-person-avatars` — same theme as this pass
   - `fix/remove-dead-testimonials-css`
   - `retire-orphan-tags` — 28 orphaned tag dirs; **overlaps** the tag deletions in
     `4055e8b`/`c1dca75`, so expect conflicts
   - `venus-workflow-pending` — GitHub environment sync workflow
   - `agent/worker` — 22 commits of review expansions, diverged, needs review
7. **Affiliate applications are live.** Paul applied 2026-08-05; nobody on the team has
   a record of which programmes or dates. Scheduled task
   `venus-affiliate-monday-followup` fires 2026-08-10 09:00 CEST to ask him. All 48
   offer URLs are still `url: ""` — nothing can go live until approvals return
   tracking IDs. Lovehoney declined 2026-07-29; do not reapply yet.

---

## 4b. Tooling added 2026-08-06 — use it, don't rebuild it

- `scripts/remove-prod-unverified-images.py` — provenance classifier. Now scans **.html, .css
  and .js**; it previously read HTML only and so never examined the homepage hero, which is set
  as a CSS background. Exits non-zero while any image is UNKNOWN.
- `~/.openclaw/workspaces/image-creator/comfy-generate.py` — generate at any size. The
  `image_generate` tool can only emit 1024x1024; width/height are hardcoded in the shared
  workflow with no plugin mapping.
- `~/.openclaw/workspaces/image-creator/review-image.py` — mechanical gate over a produced file:
  exists, dimensions vs brief, near-flat detection, byte-identical and perceptual duplicates,
  provenance metadata. Exits non-zero on failure and always prints what it did **not** check
  (text/logos — no OCR on this machine; whether it depicts a real product; quality).
- The shared ComfyUI workflow's negative prompt now permanently carries the safety terms. Caller
  negative prompts were previously discarded entirely — only the positive prompt is substituted.
- `agents.defaults.compaction` is tuned to the GPU (`timeoutSeconds` 600, `keepRecentTokens`
  8000). Rationale and the VRAM measurements are in
  `~/.openclaw/workspace/directives/HARDWARE-SPEC.md`. **Do not revert or swap Pixel's model
  without reproducing those measurements.**

## 5. Rules to keep

- **Never generate an image depicting a real, branded product.** Not a style
  preference — the previous unsupervised batch had a ~3-in-12 factual error rate, and
  Paul is mid-application with the brands depicted. Abstract decorative art depicting
  no real product is fine and is already the site's convention.
- **Never render text in a generated image.** The mirrored We-Vibe wordmark shipped to
  production. Overlay text in HTML instead.
- **The products README's "VERIFIED" labels mean "verified free of people and faces",
  not verified genuine.** Do not read them as provenance.
- **The shared tree refuses ad-hoc commits.** Work on a branch off `hostinger-deploy`
  in your own worktree. A *conflicted* merge finished with a manual `git commit` also
  trips the hook — that is the documented case for
  `VENUS_INTEGRATION_COMMIT=1 VENUS_INTEGRATION_REASON="…"`, which is logged.
- **`public/` is untracked and gitignored** (`c305d17`) so it stops serving a duplicate
  copy of the site. If a merge offers to restore files under `public/`, take the
  deletion.
- **A `Redirect 301` wins over the filesystem.** Adding a redirect for a slug that
  later gets a real page will silently shadow it. Check `.htaccess` after adding pages.

---

## 6. Agent capability, tested 2026-08-06

Superseding an earlier, wrong entry here. Both agents were given real bounded work and
the **artifacts were checked on disk**, not the reports.

**Architect / planner — works. Trust it with repo work.**
Given "cherry-pick `fix/remove-dead-testimonials-css` onto a branch off hostinger-deploy
in your own worktree, verify, do not push", it produced branch
`forge/remove-dead-testimonials-css` (`e278802`, `1d8ea59`) on top of `c986acf`.
Verified independently: 56 references to the dead stylesheet → **0**, CSS file deleted,
60 files changed, not pushed. It also caught something real — the original commit was
based on `4798cdd` and missed 12 pages added in later merges, so it grepped the current
tree and fixed them in a second commit. It reported its own limits honestly (no Hugo in
PATH; could not read the shared tree path directly, worked around it with `git show`).

**Pixel / image-creator — works. It is SLOW and SILENT. Do not call it broken.**
Full note: `~/.openclaw/workspaces/image-creator/PIXEL-IS-SLOW-NOT-BROKEN.md`.
It returns **no text reply at all** — only a plugin banner — and writes its files
**minutes after the dispatch call returns**. Batches work: one request for eight
placeholders produced all eight, correct size, visually distinct, nothing
prohibited in them. Nine good images in total so far.

I called it a failure three separate times, then built a theory that "single-image
briefs succeed, multi-image briefs fail" and dispatched a retry loop around it.
The theory was wrong — every one of those runs had already succeeded and I had
looked at the directory too early.

**Working pattern: dispatch, do not wait for a reply, come back up to an hour
later, judge only by files on disk.** Paul, 2026-08-06: *"it is very okay when
Pixel takes some time, it just has to produce good results."*

**Do not swap its model on the strength of a quiet dispatch.** It runs
`ollama/qwen3.5:9b` with thinking off and that has been sufficient. Changing a
working agent's config because a call was quiet for five minutes is the specific
mistake this paragraph exists to prevent — take artifact-backed evidence to Paul
first.

**Sophia / assistant** — returned an empty response once on 2026-08-06.

**The rule this produces: verify the artifact, never the summary.** That cuts both ways
— a confident report can describe work that does not exist, and silence can hide work
that does.

**And check the right object.** Reviewing Architect I first inspected its worktree's
current HEAD, found an old commit, and nearly recorded it as fabricating. It had simply
switched the worktree back to `agent/planner` after committing. Check the branch it
names, with `git log <branch>` / `git merge-base --is-ancestor`, not whatever the
worktree happens to be pointing at.

---

## Overnight session addendum (2026-08-06 night)

State of `hostinger-deploy` (LOCAL, none of this pushed — Paul decides):

| commit | what |
|---|---|
| `d8d4590` | .htaccess comment corrections (comment-only) |
| `7544292` | /best-for/value/ article body restored (was serving EMPTY live) |
| `c095ded` | 12 products price-verified vs manufacturer pages; 8 render, 4+1 honestly hidden; best-offer requires available:true |
| `d904940` | 3 draft product pages (Tango X, Sila, VIM) — draft:true, not served |

Version branches stored for review (built, committed, NOT merged):
- `venus-imagery-headers` — 12 ambient headers on all best-for/guide pages
- `venus-tags-unretired` — compact/external/g-spot/waterproof live again
- `venus-new-products` — the 3 new product pages published

Other work: trade.ultramarine963.com source recovered to
`~/.openclaw/workspaces/worker/trade-site/` (see its README — this is the
trading-bots sales site, Formspree mlgwljjn, live since Feb). Trade-site hero
image generated. Echo's fact sheet: `directives/VENUS-SITE-FACTS.md`.

Still open, needs Paul: push authorization for the 4 local commits; pick/merge
versions; tag-retirement direction (branch exists for option 2); lelo-hugo page
should mention the original is sold out at LELO (successor Hugo 2, 179 EUR);
`swedish-design` tag title + best-for price-disclaimer hand-fixes need
backporting to source; GitHub workflow branch still needs web-UI landing.
