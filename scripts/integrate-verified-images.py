#!/usr/bin/env python3
"""
Venus product-image integrator (verdict-gated).

TASK-214: Wire accuracy-verified product images into content frontmatter,
one product at a time. This script is the *mechanical* enforcement of the
accuracy gate: it refuses to integrate anything that is not listed as
ACCURATE in the verdicts manifest (VENUS-IMAGE-TRIAGE-VERDICTS.md).

Usage:
  ./scripts/integrate-verified-images.py <verdicts.md> [--products slug1,slug2] [--dry-run]

Design:
  - Parses a markdown table with columns: product/slug, verdict, image path.
  - Only rows with verdict in {ACCURATE, KEEP, VERIFIED, PASS} are integrated.
  - Source image comes from the verdict row's image path (Pixel's staged file)
    OR falls back to <pixel-worktree>/static/images/products/<slug>/front.webp.
  - Copies to static/images/products/<slug>/front.webp, optimizes via
    optimize-product-image.py (WebP 600x600, <=500KB), updates
    content/products/<slug>/index.md `image:` frontmatter.
  - Never touches hostinger-deploy; commits are left to the caller (per-product).
"""
import argparse
import re
import shutil
import subprocess
import sys
from pathlib import Path

WORKTREE = Path(__file__).resolve().parent.parent

# Verdict values that authorize integration (case-insensitive, trimmed)
PASS_VALUES = {"accurate", "keep", "verified", "pass", "ok", "use"}


def parse_verdicts(path: Path):
    """Return dict slug -> {'verdict': str, 'image': str|None}."""
    text = path.read_text(encoding="utf-8", errors="replace")
    rows = {}
    in_table = False
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("|") and stripped.endswith("|"):
            cells = [c.strip() for c in stripped.strip("|").split("|")]
            # normalise: some tables have [slug](link) or `slug`
            slug = re.sub(r"[`\[\]\(\)]", "", cells[0]).strip().lower()
            if not slug or slug == "product" or slug == "slug":
                in_table = True
                continue
            # skip separator rows like |---|---|
            if re.fullmatch(r":?-{2,}:?", cells[1] if len(cells) > 1 else ""):
                continue
            verdict = cells[1].lower().strip() if len(cells) > 1 else "unknown"
            image = None
            if len(cells) > 2 and cells[2] and cells[2] != "-":
                image = re.sub(r"[`\[\]\(\)]", "", cells[2]).strip()
            # keep first occurrence; later rows (re-verdicts) override
            rows[slug] = {"verdict": verdict, "image": image}
            in_table = True
    return rows


def find_source_image(slug: str, verdict_image: str | None, pixel_worktree: Path | None):
    """Resolve the verified source image for a slug."""
    cands = []
    if verdict_image:
        cands.append(Path(verdict_image))
    if pixel_worktree:
        cands.append(pixel_worktree / "static" / "images" / "products" / slug / "front.webp")
        cands.append(pixel_worktree / "static" / "images" / "products" / slug / "front.png")
    cands.append(WORKTREE / "static" / "images" / "products" / slug / "front.webp")
    for c in cands:
        if c.exists() and c.is_file():
            return c
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("verdicts", type=Path, help="Path to VENUS-IMAGE-TRIAGE-VERDICTS.md")
    ap.add_argument("--products", default="", help="Comma-separated slug list (default: all ACCURATE)")
    ap.add_argument("--dry-run", action="store_true", help="Print plan, change nothing")
    ap.add_argument("--pixel-worktree", type=Path, default=None,
                    help="Path to Pixel's worktree for staged front.webp files")
    args = ap.parse_args()

    if not args.verdicts.exists():
        print(f"FATAL: verdicts manifest not found: {args.verdicts}")
        sys.exit(2)

    verdicts = parse_verdicts(args.verdicts)
    print(f"Parsed {len(verdicts)} products from verdicts manifest.")

    requested = [s.strip().lower() for s in args.products.split(",") if s.strip()]
    results = {"integrated": [], "blocked": []}

    for slug, info in sorted(verdicts.items()):
        verdict = info["verdict"]
        if requested and slug not in requested:
            continue
        if verdict not in PASS_VALUES:
            results["blocked"].append((slug, verdict))
            print(f"BLOCKED {slug}: verdict='{verdict}' (not in {sorted(PASS_VALUES)})")
            continue

        src = find_source_image(slug, info["image"], args.pixel_worktree)
        if src is None:
            results["blocked"].append((slug, verdict))
            print(f"BLOCKED {slug}: ACCURATE but no source image found")
            continue

        dest_dir = WORKTREE / "static" / "images" / "products" / slug
        dest_dir.mkdir(parents=True, exist_ok=True)
        dest = dest_dir / "front.webp"
        content = WORKTREE / "content" / "products" / slug / "index.md"
        if not content.exists():
            results["blocked"].append((slug, verdict))
            print(f"BLOCKED {slug}: content file missing {content}")
            continue

        print(f"PLAN {slug}: verdict={verdict} src={src} -> {dest.relative_to(WORKTREE)}")
        if args.dry_run:
            results["integrated"].append(slug)
            continue

        shutil.copy2(src, dest)
        # optimize in place
        opt = subprocess.run(
            [sys.executable, str(WORKTREE / "scripts" / "optimize-product-image.py"),
             str(dest), slug],
            capture_output=True, text=True)
        if opt.returncode != 0:
            results["blocked"].append((slug, verdict))
            print(f"FAIL {slug}: optimizer error: {opt.stderr[-500:]}")
            continue

        # update frontmatter image: line
        text = content.read_text(encoding="utf-8")
        new_text, n = re.subn(r'(?m)^image:\s*".*"', f'image: "/images/products/{slug}/front.webp"', text, count=1)
        if n != 1:
            results["blocked"].append((slug, verdict))
            print(f"FAIL {slug}: image: line not found/updated in frontmatter")
            continue
        content.write_text(new_text, encoding="utf-8")
        results["integrated"].append(slug)
        print(f"DONE  {slug}: frontmatter -> /images/products/{slug}/front.webp")

    print("\n=== SUMMARY ===")
    print(f"integrated ({len(results['integrated'])}): {', '.join(results['integrated']) or '-'}")
    print(f"blocked ({len(results['blocked'])}):")
    for slug, verdict in results["blocked"]:
        print(f"  - {slug}: {verdict}")
    return 0 if not results["blocked"] else 1


if __name__ == "__main__":
    sys.exit(main())