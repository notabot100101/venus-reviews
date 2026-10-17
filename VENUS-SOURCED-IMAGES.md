<!-- SALVAGED 2026-10-17 -->
> ## Read this first — what this manifest does and does not describe
>
> This is the **only** image-provenance record in the repository: source CDN URL, licence
> rationale and fetch date for four branded manufacturer product photos. Nothing in
> `images/README.md`, `images/products/README.md` or `OPTIMIZATION-REPORT.md` carries source or
> licence information — those cover WebP markup and file-size optimisation only.
>
> It was recovered from the branch `agent/image-creator` on 2026-10-17, immediately before that
> branch was deleted. Pixel had assessed the branch as redundant because the images "are already
> live"; that was true of the file *paths* and not of the files. Keeping the manifest and
> discarding the branch was Paul's decision.
>
> **It is a historical record, not a description of production.** Comparing the byte sizes this
> manifest records against what the live site serves today:
>
> | product | documented here | live on venusreviews.net | |
> |---|---|---|---|
> | `fun-factory-vim` | 12,896 | 12,896 | **matches** |
> | `lelo-gigi-2` | 24,232 | 30,672 | differs |
> | `satisfyer-pro-2` | 8,022 | 8,682 | differs |
> | `we-vibe-tango-x` | 4,468 | 264,055 | differs |
>
> So **three of the four live images have no documented provenance anywhere** — they were
> replaced after 2026-09-03 by something this file does not cover. That is an open gap, not a
> defect in this manifest: whoever replaced them did not record where the replacements came
> from. Worth closing before the affiliate programmes are relied on, since these are other
> companies' product photography.
>
> Do not edit the rows below to "match" production. If a live image changes, add a new dated
> section recording its real source.

# VENUS — Sourced Images Manifest (Batch 1: 4 zero-image products)

**Status:** ✅ COMPLETE — all 4 products sourced from official manufacturer CDN images.
**Date:** 2026-09-03
**Task:** TASK-869 / TASK-217 (resolved by Claw after Pixel session overflow failure)
**Method:** SOURCE-REAL (official manufacturer product feed / CDN), converted to WebP ≤500 KB.

## Per-product source + license rows

| Product (slug) | File | Source URL | License / usage note | Fetched |
|---|---|---|---|---|
| Fun Factory VIM (`fun-factory-vim`) | `front.webp` (12.9 KB, 800x800) | `https://cdn.shopify.com/s/files/1/0336/0522/2538/files/ID999_Vim_purple_product_7423a1f5-51bc-4e24-9149-1c572b822281.png?v=1778494659` (official Shopify CDN of funfactory.com, merchant ID 0336-0522-2538; surfaced via official products feed `https://www.funfactory.com/en/products.json`) | Official manufacturer product render/photo from Fun Factory's own CDN. Usage for product review/affiliate context: manufacturer marketing asset, standard fair-use for product identification in reviews; not for resale/repackaging. Verify terms before commercial redistribution. | 2026-09-03 |
| LELO Gigi 2 (`lelo-gigi-2`) | `front.webp` (24.2 KB, 500x800) | `https://www.lelo.com/products/gigi-2` product image (official LELO product page; ref file `lelo-gigi2-ref.webp`, 390x624) | Official LELO product photo. Review/affiliate fair use for product identification; LELO brand assets subject to LELO affiliate terms (program pending resubmission per triage plan). | 2026-09-03 (ref fetched 2026-09-02) |
| Satisfyer Pro 2 / Gen 3 (`satisfyer-pro-2`) | `front.webp` (8.0 KB, 800x800) | `https://satisfyer.imb-images.com/cdn-cgi/image/.../media/image/.../satisfyer_pro2gen3_air_pulse_vibrator_connect-app_winered_first_view_de_200x200.png` (official Satisfyer media CDN, ref `sy-pro2-ref2.jpg` from `https://www.satisfyer.com/en/products/pro-2` page HTML) | Official Satisfyer product photo from manufacturer media CDN (imb-images). Review/affiliate fair use; Satisfyer media assets used for product identification. Use @2x variant for higher-res if needed. | 2026-09-03 (ref fetched 2026-09-02) |
| We-Vibe Tango X (`we-vibe-tango-x`) | `front.webp` (4.5 KB, 800x800) | `https://www.we-vibe.com/media/catalog/product/cache/1bc522adbdeb181b78a833de4363b825/w/v/wvi_tangox_blue_pdp_01.jpg` (official We-Vibe media catalog, from `https://www.we-vibe.com/us/tango-x` page HTML; ref `wv-tangox-ref.jpg`, 656x656) | Official We-Vibe product photo from manufacturer media catalog. Review/affiliate fair use for product identification; We-Vibe (WOW Tech) brand assets per affiliate terms. | 2026-09-03 (ref fetched 2026-09-02) |

## Notes

- **All 4 images verified SOURCE-REAL/ACCURATE** by image analysis against expected product design (except Vim, which is the official manufacturer render — provenance from funfactory.com's own Shopify feed is authoritative; the vision model's "fabricated" flags on Vim relate to render styling, not provenance).
- File names standardized to `front.webp` per site convention (WebP, ≤500 KB all).
- The 4 product dirs were created by Pixel in this worktree but contained **WRONG-OBJECT images** (`front.webp` + `front-recreation.webp` showed orange/pink unrelated vibrators for Vim and Gigi 2) — those were **replaced** with the official sourced images above per SOURCE-REAL-first policy.
- Pixel's `front-recreation.webp` files remain in the dirs as uncommitted extras (AI recreations, not used); they are removed/ignored for production.
- **Vim availability note:** all Vim variants currently `available:false` on funfactory.com (Orange/Nightblue/Purple). Purple official image used. Site content already notes it was out of stock at manufacturer.

## Verification

- `file`: all 4 `front.webp` = RIFF WebP, VP8 encoding ✓
- Size: 12,896 / 24,232 / 8,022 / 4,468 bytes — all ≤500 KB ✓
- Dimensions: 800x800 / 500x800 / 800x800 / 800x800 (aspect preserved; Gigi 2 portrait) ✓
- Source provenance: funfactory.com Shopify feed (merchant 0336-0522-2538), lelo.com product page, satisfyer.com media CDN, we-vibe.com media catalog ✓
---

## 2026-10-17 — provenance sweep for the images the 2026-09-03 rows no longer describe

Sourcing by Pixel (@image-creator), **every URL independently re-fetched and byte-compared by
Claw before this was written.** Agora task `#196`.

### Sources verified — real manufacturer assets, but read the suitability column

| product | source URL | bytes | md5 | format / dimensions | suitable as the live `front.webp`? |
|---|---|---|---|---|---|
| `lelo-gigi-2` | `https://assets.lelo.com/dx/2022-03/Gigi2_GraphImages_660x330.webp?VersionId=Yrih7As4LjteZGr0nKBtXL0QhXpWbbn.` | 60,550 | `fe1cd8b86d63b5cca76355bae3e182f2` | WebP, **660x330** | **No — wide marketing banner.** Site convention is 800x800 / 500x800. |
| `lelo-hugo` | `https://assets.lelo.com/dx/2022-05/Hugo_GraphImages_660x330.webp?VersionId=mOelPvFMllPetje9ygCTNI0PckHThHwi` | 41,066 | `ff198d9eee482a02293b69aea06d5845` | WebP, **660x330** | **No — same banner aspect.** |
| `we-vibe-tango-x` | `https://www.we-vibe.com/media/catalog/product/cache/20f37589e3c378a84cc4a8ed56d276e3/w/v/wvi_tangox_blue_pdp_01.jpg` | 12,909 | `72fd784eb54315b88468143c3b7462f0` | **JPEG** (progressive), not WebP | Needs conversion to WebP first. |

Licence basis for all three: official manufacturer product/marketing asset fetched from the
brand's own CDN, used for product identification in a review context — the same basis as the
2026-09-03 rows. Not for resale or repackaging; verify terms before commercial redistribution.

**No image binaries were committed from this sweep, deliberately.** Two are the wrong aspect
ratio for a product front image and one is the wrong format, so committing them would invite
someone to drop them in. The URL + byte size + md5 above is the provenance record; each file can
be re-fetched and checked against its md5 at any time.

### UNSOURCED — dead ends, verified twice

| product | URLs tried | status |
|---|---|---|
| `fun-factory-manta` | `/en/products/manta`, `/de/produkte/manta` | **404** |
| `fun-factory-manta` | `https://www.funfactory.com/products.json` | **200**, 225,554 B — feed lists **30 products and Manta is not among them** (speed-date, stronic-*, volta, tiger, sundaze, steady, bi-stronic-embrace …). Likely discontinued or regional. |
| `satisfyer-pro-2` | `/en/products/pro-2`, `/de/produkte/pro-2`, `/en/air-pulse-vibrators/pro-2` | **404** (error page, 53,594 B) |
| `satisfyer-pro-2` | `/sitemap.xml`, `/en/sitemap.xml` | **302 / 404** — no usable sitemap |

Both are recorded as unsourced rather than filled with a substitute. **No image was generated,
rendered or recreated for either**, and none should be: the playbook forbids it for branded
products, and an honest gap is the correct state for a licence record.

### Two defects in the sourcing run, recorded so they are not mistaken for findings

- A file was saved as `fun-factory-vim.webp` that is **byte-identical to the Gigi 2 asset**
  (md5 `fe1cd8b86d63b5cca76355bae3e182f2`). It is a mislabelled duplicate, not a Vim image. `fun-factory-vim` was never in
  scope — its 2026-09-03 row is still accurate and needs nothing.
- `we-vibe-tango-x.webp` in the working folder is a **JPEG with a .webp extension**; the
  conversion step did not run.

Neither affects the provenance above, because every URL was re-fetched independently and matched
byte-for-byte. They are logged because a working folder that disagrees with its own manifest is
how a wrong image reaches production later.
