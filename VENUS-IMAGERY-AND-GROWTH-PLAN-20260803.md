# Venus Imagery Remediation & Growth Plan (corrected + executed)
**Date:** 2026-08-03 · **Status:** imagery remediation DEPLOYED (commit `389747e`); affiliate + product-expansion pending Paul's action.

> Note: an earlier draft of this file (Claw/main) was lost — it was never committed and a concurrent agent's git op in this shared working tree wiped the untracked file. This is the corrected, committed version.

---

## 1. Verified live-state (checked against the live site, not memory)
- The **published catalogue lists only the 3 genuine products**: `lelo-hugo`, `lelo-sona-2`, `lovehoney-desire`.
- The other **9 products are all `draft: true`** — excluded from the `hugo --quiet` build. They were never in the catalogue; their pages only lingered as **orphaned stale build output** reachable by direct URL (rsync-no-delete deploy quirk).

### Per-product truth (verified by opening the image files)
| Product | Was | Now |
|---|---|---|
| lelo-hugo, lelo-sona-2, lovehoney-desire | genuine press photos (non-square, correct product) | **KEPT, untouched** |
| bvee-original-rabbit, dame-eva-ii, lelo-enigma, we-vibe-chorus | AI renders (square 1024², purple-gradient) | AI images removed → neutral placeholder |
| womanizer-2-original | square/AI-suspect | images removed → placeholder |
| lelo-mona | wrong product (LELO lay-on massager, not the Mona 2 wand) | images removed → placeholder |
| fun-factory-manta, fun-factory-volta, we-vibe-sync | no images | neutral placeholder |

## 2. EXECUTED 2026-08-03 (commit `389747e`, deployed to hostinger-deploy)
For the 9 draft products: removed AI-render / wrong-product images **and** the orphaned live pages; repointed `image:` to honest-lane placeholders (`/images/placeholders/ambient-0{1..4}.png` — 4 spa still-lifes by Pixel, verified free of products/branding/people); dropped the fake galleries. The 3 genuine products were not touched. **Live effect:** orphaned draft pages now 404; the honest catalogue is unchanged. Drafts are honest-when-published, pending real official assets.

## 3. Affiliate priority — CORRECTED
The authoritative research is `affiliate-research/AFFILIATE-RESEARCH.md` (368 lines, Jul 30). Key correction to earlier advice:
- **Lovehoney is NOT the priority — it DECLINED Venus on 2026-07-29.** Do not lead with it (reapply later once traffic/content grows).
- **#1 = LELO** (web-verified 2026-08-03: 5–20% commission, 30-day cookie, direct match for Venus's LELO products, and **provides affiliate product images** → this unblocks the imagery for lelo-enigma/lelo-mona/hugo/sona-2). Signup: `lip.hasoffers.com/signup` (also on Admitad/FlexOffers/Skimlinks/Awin).
- **#2 = Womanizer + We-Vibe** (Impact network, up to 22%) → unblocks we-vibe-chorus/sync + womanizer imagery.
- **#3 = SheVibe** (Impact, 10%, multi-brand). **#4 = Adam & Eve** (Pepperjam, up to 30%, US). **Last = Amazon** (adult-content policy risk).

The technical framework already exists (Hugo `offers` array + `affiliate-config.json`, disclosure page FTC-compliant). Once approved: drop tracking IDs in `affiliate-config.json`, populate `offers[].url` + `available: true` per product, and pull official product images.

## 4. Product-expansion candidates (research, verify assets/affiliate before adding)
1. **We-Vibe Nova 2** — flexible-arm rabbit; We-Vibe press assets; complements Chorus/Sync.
2. **LELO Dot** — pinpoint elliptical stimulator; LELO press kit; fills "precision external" gap vs Sona 2.
3. **Njoy Pure Wand** — steel G-spot/prostate; cult product; assets easy to source; via Spectrum/Lovehoney.
4. **Hot Octopuss Pulse** — male-focused "guybrator"; direct + Lovehoney programme.
5. **Magic Wand** — category-reference wand; watch for marketplace counterfeits.

## 5. Decisions / actions for Paul
1. **Apply to LELO first** (fastest + unblocks imagery + provides assets). Then Womanizer/We-Vibe (Impact).
2. **Bvee identity:** confirm whether "Bvee" is actually "b-Vibe" (affects whether that slot/affiliate route is valid) — it currently has no genuine imagery or confirmed brand.
3. **Product expansion:** pick which candidate(s) to add first (suggest We-Vibe Nova 2 + Njoy Pure Wand).
4. Once an affiliate approves and sends official images, un-draft the relevant products (they're already honest-placeholder now) and swap in the real assets.
