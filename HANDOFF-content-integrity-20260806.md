# Handoff: content integrity pass, 2026-08-05/06

For any agent picking this up cold. Written by Forge (worker) at the end of a long
Claude Code session. Everything below was verified against the repo, not recalled.

---

## 1. Status right now

`hostinger-deploy` is **18 commits ahead of `origin/hostinger-deploy` and NOT pushed.**
Production still serves the pre-cleanup content.

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

1. **Push to production.** Needs Paul. Everything above is invisible until then.
2. **Hero banner.** `images/hero-banner.jpg` is orphaned — referenced nowhere after
   `36d8492`, still tracked. It is branded "ESSENCE REVIEWS", a different brand, with a
   fake logo and CTA baked into the pixels. Needs a correctly-branded replacement or
   deletion. **Must contain no text** — see §5.
3. **Only 4 ambient placeholders for 13 products**, so unrelated products share an
   image (We-Vibe Chorus and Fun Factory Manta both showed ambient-03). 8 more would
   fix it. Abstract spa still-life, 1024x1024, no text, no people, no products.
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

**Pixel / image-creator — generates fine; its REPLY does not come back.**
Earlier entry said it "produced zero files on two attempts". That was true of those runs
but the wrong diagnosis. On a third attempt it wrote
`venus-images/ambient/ambient-05.png` — a valid 1024x1024 RGB PNG, 1.3 MB, ComfyUI
`prompt` chunk present, and visually on-brief: abstract spa still-life, no text, no
logos, no people, no product. It returned **no text response at all** through
`openclaw agent`. So: give Pixel work, then go look for the file. Never wait for its
report and never conclude from silence that nothing happened.

**Sophia / assistant** — returned an empty response once on 2026-08-06.

**The rule this produces: verify the artifact, never the summary.** That cuts both ways
— a confident report can describe work that does not exist, and silence can hide work
that does.

**And check the right object.** Reviewing Architect I first inspected its worktree's
current HEAD, found an old commit, and nearly recorded it as fabricating. It had simply
switched the worktree back to `agent/planner` after committing. Check the branch it
names, with `git log <branch>` / `git merge-base --is-ancestor`, not whatever the
worktree happens to be pointing at.
