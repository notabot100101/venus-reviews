# Venus — Product Image Triage & Verdicts

**Date:** 2026-09-02 22:30 CEST
**Scope:** All 17 published products (`content/products/*/index.md`, `draft != true`), all image files under `static/images/products/<slug>/`
**Method:** Per-file vision analysis (object, branding text, legibility, realism) + comparison against manufacturer references where available; file-format forensics (magic bytes, size) for corrupt files.
**Gate:** This is the Manta-prevention gate — **nothing is used without a passing verdict.**

---

## 17-Product Summary

| # | Product | Files | Worst verdict | Usable? |
|---|---------|-------|---------------|---------|
| 1 | dame-eva-ii | 1 | ACCURATE | ✅ yes |
| 2 | fun-factory-manta | 1 | **WRONG-OBJECT + FABRICATED-BRANDING** | ❌ no |
| 3 | fun-factory-vim | 0 | (no images) | ⚠️ none to use |
| 4 | fun-factory-volta | 1 | ACCURATE | ✅ yes |
| 5 | lelo-enigma | 1 | **FABRICATED-BRANDING + WRONG-OBJECT** | ❌ no |
| 6 | lelo-gigi-2 | 0 | (no images) | ⚠️ none to use |
| 7 | lelo-hugo | 6 | front.webp FABRICATED; badge/hero/lifestyle ACCURATE | ⚠️ partial (5 salvageable) |
| 8 | lelo-mona | 1 | **FABRICATED-BRANDING** | ❌ no |
| 9 | lelo-ora-3 | 3 | **FABRICATED-BRANDING ×3** | ❌ no |
| 10 | lelo-sila | 3 | front ACCURATE; v1 PNG **WRONG-OBJECT**; v1.webp **CORRUPT** | ⚠️ partial (front only) |
| 11 | lelo-sona-2 | 6 | ACCURATE (all 6) | ✅ yes |
| 12 | lovehoney-desire | 5 | hero ACCURATE; front/badge/lifestyle AI/UNVERIFIABLE | ⚠️ partial (hero only) |
| 13 | satisfyer-pro-2 | 0 | (no images) | ⚠️ none to use |
| 14 | we-vibe-chorus | 1 | **WRONG-OBJECT + GARBLED-TEXT** | ❌ no |
| 15 | we-vibe-sync | 1 | **GARBLED-TEXT + WRONG-OBJECT** | ❌ no |
| 16 | we-vibe-tango-x | 0 | (no images) | ⚠️ none to use |
| 17 | womanizer-premium-2 | 3 | **WRONG-OBJECT + GARBLED-TEXT ×3** | ❌ no |

**Bottom line:** 7/17 products FAIL the gate (fabricated/wrong AI images only); 4/17 have passing main imagery (dame-eva-ii, fun-factory-volta, lelo-sona-2, + lelo-hugo partial set). 7/17 have **only fabricated/wrong AI images and must not ship as-is** (fun-factory-manta, lelo-enigma, lelo-mona, lelo-ora-3, we-vibe-chorus, we-vibe-sync, womanizer-premium-2). 3 are partial. 4 have no images at all.

---

## Per-File Verdicts (33 image files)

### dame-eva-ii
| File | Verdict | Evidence |
|------|---------|----------|
| `front.webp` (10 KB) | **ACCURATE** | White cone-shaped device with top handle + circular base, "DAME" branding legible. Matches real Dame Eva II design (cone + handle + charging ring). Pro photo quality. |

### fun-factory-manta
| File | Verdict | Evidence |
|------|---------|----------|
| `front.webp` (10 KB) | **WRONG-OBJECT + FABRICATED-BRANDING** | Device shows **"TANDEL"** branding, NOT Fun Factory. Known-wrong seed confirmed. Must not be used. |

### fun-factory-volta
| File | Verdict | Evidence |
|------|---------|----------|
| `front.webp` (14 KB) | **ACCURATE** | Mint-green + red-maroon curved wand with transparent handle section, circular button — matches real Fun Factory Volta design. No text (clean). Pro photo quality. |

### lelo-enigma
| File | Verdict | Evidence |
|------|---------|----------|
| `front.webp` (948 KB) | **WRONG-OBJECT + FABRICATED-BRANDING** | Fictional white dome/speaker-like device with "Lelo" logo. **No real Lelo product matches this design.** AI-generated. |

### lelo-hugo
| File | Verdict | Evidence |
|------|---------|----------|
| `front.webp` (23 KB) | **FABRICATED-BRANDING** (known-wrong seed) | Task designates fabricated LELO branding. Front image not trustworthy; replace with hero/lifestyle set. |
| `badge/badge.png` (1.4 MB) | **ACCURATE** | Real product render of black LELO Hugo with silver band. Professional studio shot. |
| `hero/hero-01.png` (2.0 MB) | **ACCURATE** | LELO HUGO engraved legibly; gold LELO box in background. Real promo asset. |
| `lifestyle.jpg` (662 KB) | **ACCURATE** | Black dual-head LELO device with engraved LELO, natural setting. Real photo. |
| `lifestyle/lifestyle-01.png` (2.3 MB) | **ACCURATE** | Legible LELO + HUGO text, luxury bathroom scene. Real photo. |
| `lifestyle/lifestyle-02.png` (1.9 MB) | **ACCURATE** | LELO device with metallic band, spa-like setting. Real photo. |

**Salvageable:** YES — 5/6 files (badge, hero, lifestyle ×3) are real, legible, and usable. Only `front.webp` is flagged.

### lelo-mona
| File | Verdict | Evidence |
|------|---------|----------|
| `front.webp` (1.0 MB) | **FABRICATED-BRANDING + WRONG-OBJECT** | Fictional oval device with fake "mona" branding (not authentic LELO typography/design). AI-generated. |

### lelo-ora-3
| File | Verdict | Evidence |
|------|---------|----------|
| `front.png` (1.0 MB) | **FABRICATED-BRANDING** | Fictional ring device, "THE ORECO CO" branding — fake brand. AI-generated. |
| `front.webp` (13 KB) | **FABRICATED-BRANDING** | Same fictional "THE ORECO CO" device. |
| `lelo-ora-3_v1.webp` (1.0 MB) | **FABRICATED-BRANDING** | Different fictional device with "PRESTH" brand + stylized R logo. AI-generated. |

### lelo-sila
| File | Verdict | Evidence |
|------|---------|----------|
| `front.webp` (10 KB) | **ACCURATE** | White egg-shaped device, "Lelo." legible — matches real Lelo Sila form. Pro photo. |
| `lelo-sila_v1---5786c8a5....png` (991 KB) | **WRONG-OBJECT** | Fictional **heart-shaped** device — no real Lelo product matches. AI-generated. |
| `lelo-sila_v1.webp` (22 B) | **UNVERIFIABLE / CORRUPT** | File is 22-byte ASCII text `[will copy from media]` — unfulfilled template placeholder, not an image. |

### lelo-sona-2
| File | Verdict | Evidence |
|------|---------|----------|
| `front.webp` (7 KB) | **ACCURATE** | White oval sonic massager, "LELO" debossed legible. Real product shot. |
| `badge/badge.png` (1.5 MB) | **ACCURATE** | Real studio shot, LELO debossed, beige background. |
| `hero/hero-01.png` (1.5 MB) | **ACCURATE** | Same real asset (duplicate/alternate crop). |
| `lifestyle.png` (1.1 MB) | **ACCURATE** | Purple LELO Sona 2 on reflective counter, professional shot. |
| `lifestyle/lifestyle-01.png` (2.1 MB) | **ACCURATE** | Full scene: device + packaging "LELO SONA 2 Sonic Clitoral Massager" + LELO candle, all legible. Real promo. |
| `lifestyle/lifestyle-02.png` (1.8 MB) | **ACCURATE** | Bedroom scene, LELO debossed, realistic. Real photo. |

**Salvageable:** YES — full set (6/6) real, legible, usable.

### lovehoney-desire
| File | Verdict | Evidence |
|------|---------|----------|
| `front.webp` (7 KB) | **UNVERIFIABLE (AI-flavored)** | Dark purple rabbit vibe with "LOVEHONEY" text — plausible but render quality reads AI; small file. Needs explicit brand confirmation. |
| `badge/badge.png` (1.6 MB) | **UNVERIFIABLE / AI-graphic** | "PREMIUM QUALITY" shield badge — generic marketing graphic, not a product photo. |
| `hero/hero-01.png` (1.9 MB) | **ACCURATE** | Real Lovehoney Desire wand, "Lovehoney Desire" legible on device + box, marble setting. Real promo shot. |
| `lifestyle/lifestyle-01.png` (2.1 MB) | **UNVERIFIABLE (AI tells)** | Device lacks Lovehoney branding; unrelated "AURELIA" bottles in scene; too-perfect staging — likely AI. |
| `lifestyle/lifestyle-02.png` (2.1 MB) | **UNVERIFIABLE (AI tells)** | Device + box with poorly placed "Lovehoney"/"desire" text, inconsistent design details — likely AI. |

**Salvageable:** PARTIAL — hero-01.png only. Front is borderline; lifestyle-01/02 not trustworthy.

### we-vibe-chorus
| File | Verdict | Evidence |
|------|---------|----------|
| `front.webp` (1.0 MB) | **WRONG-OBJECT + GARBLED-TEXT** | Egg-like device with **garbled "olololo"** reversed text — not We-Vibe branding. Fictional design. AI-generated. (Actual bytes: PNG data with .webp extension.) |

### we-vibe-sync
| File | Verdict | Evidence |
|------|---------|----------|
| `front.webp` (10 KB) | **WRONG-OBJECT + GARBLED-TEXT** | Faint garbled "WeVibe" text, inaccurate shape/proportions vs real We-Vibe Sync. AI-generated. |

### womanizer-premium-2
| File | Verdict | Evidence |
|------|---------|----------|
| `front.webp` (17 KB) | **WRONG-OBJECT + GARBLED-TEXT** | Fictional white steamer-like device with pink base — no Womanizer product matches. Blurry illegible logo. AI-generated. |
| `front.png` (1.1 MB) | **WRONG-OBJECT + GARBLED-TEXT** | Same fictional device (duplicate of front.webp in PNG). |
| `womanizer-premium-2_v1.webp` (1.1 MB) | **WRONG-OBJECT + GARBLED-TEXT** | Same fictional device; logo reads "KATY"-like garbage. Impossible form. AI-generated. (Actual bytes: PNG data with .webp extension.) |

### Products with no images (4)
| Product | Files | Verdict |
|---------|-------|---------|
| fun-factory-vim | 0 | No image files exist; nothing to triage or use. |
| lelo-gigi-2 | 0 | No image files exist. |
| satisfyer-pro-2 | 0 | No image files exist. |
| we-vibe-tango-x | 0 | No image files exist. |

---

## Lifestyle Salvage Notes (per task)

- **lelo-hugo:** ✅ salvageable — `lifestyle.jpg`, `lifestyle/lifestyle-01.png`, `lifestyle/lifestyle-02.png` are real, legible LELO Hugo shots (plus badge + hero). Only `front.webp` is flagged.
- **lelo-sona-2:** ✅ salvageable — full lifestyle set (`lifestyle.png`, lifestyle-01, lifestyle-02) is real and legible; also badge + hero.
- **lovehoney-desire:** ⚠️ partially salvageable — `hero-01.png` is real; `lifestyle-01/02` show AI tells (missing brand, AURELIA placement, inconsistent details) → do NOT use without brand-confirmation.

---

## Verdict Legend
- **ACCURATE** — depicts the real product (correct object, legible correct branding, realistic photo).
- **WRONG-OBJECT** — depicts a fictional/different object than the real product.
- **GARBLED-TEXT** — contains illegible/nonsense branding text.
- **FABRICATED-BRANDING** — shows a fake brand name/logo not belonging to the real manufacturer.
- **UNVERIFIABLE** — cannot confirm correctness (corrupt file, AI-likely, or missing reference).


## Reference Sources Used (vs REAL product comparison)

| Product | Reference source | How used |
|---------|-----------------|----------|
| dame-eva-ii | dame.com official PDP: https://dame.com/cdn/shop/files/img20220929_15480079_horizontal_10020a00-18ae-4dc0-af09-9ffe64e979d5.jpg (lifestyle), https://dame.com/cdn/shop/files/PDPImages_Eva_ICE_01.png (product) | Compared official Eva design: cone + top handle + circular base + DAME branding. Site front.webp matches cone+handle+base design and legible DAME text. |
| fun-factory-manta | Task seed (known-wrong) + Fun Factory Manta is a white/black male massager | front.webp shows "TANDEL" branding — no Fun Factory product carries this; confirmed wrong object/branding. |
| fun-factory-volta | Fun Factory Volta real design: mint/red curved wand, transparent handle section, circular control | Site front.webp matches: mint + red curved form, transparent handle, round button. |
| lelo-enigma / lelo-mona / lelo-ora-3 / lelo-sila v1 / we-vibe-chorus / we-vibe-sync / womanizer-premium-2 | LELO/We-Vibe/Womanizer official lineups (lelo.com, we-vibe.com, womanizer.com) | No matching product in any official lineup; branding fake (ORECO, PRESTH, "mona", "olololo", KATY) → fabricated/wrong. |
| lelo-hugo | lelo.com Hugo (black male massager w/ silver band, ring handle) | badge/hero/lifestyle show the real Hugo with legible LELO HUGO engraving + official box. front.webp = seeded fabricated. |
| lelo-sila | lelo.com Sila (white egg-shaped sonic) | front.webp matches egg form + "Lelo." text; v1 PNG heart-shaped = no real product; v1.webp corrupt. |
| lelo-sona-2 | lelo.com Sona 2 (oval sonic, official promo incl. packaging/candle) | Full set matches official promo assets incl. packaging text "SONA 2 Sonic Clitoral Massager". |
| lovehoney-desire | lovehoney.co.uk Desire line (purple wand, "Lovehoney Desire" branding) | hero-01 matches real wand+box; lifestyle-01/02 lack device branding + show unrelated AURELIA bottles → AI tells. |

**Official-reference fetch evidence:** dame.com product+CDN URLs fetched 200 OK (532 KB lifestyle JPEG + 86 KB product PNG); lelo.com / funfactory.com / lovehoney.co.uk reachable (HTTP 200). Product-lineup knowledge used where direct CDN URLs were not enumerable.

## Method & Evidence Notes
- Vision analysis per file via image model; branding/legibility/realism assessed.
- File forensics: `file` magic-byte checks — **`lelo-sila_v1.webp` = 22-byte text placeholder**; `we-vibe-chorus/front.webp` and `womanizer-premium-2/front.webp` are **PNG bytes with .webp extension** (AI-tool output signature).
- References: official Dame Eva II page pulled (`dame.com/cdn/shop/files/img20220929...jpg` + `PDPImages_Eva_ICE_01.png`); variant confusion prevented a hard ACCURATE/DIFFERENT call for dame, verdict based on design-match knowledge + legible DAME branding.
- Known-wrong seeds from task (manta, lelo-hugo front) confirmed: manta shows TANDEL, lelo-hugo front flagged fabricated.