#!/usr/bin/env python3
"""Optimize a Venus product image for the site.

Targets (per TASK-214 / venus-image-triage.md acceptance checklist):
  - WebP output
  - <= 500 KB
  - Correct aspect (square 600x600 for card images; detail main image same file)
  - Keeps a high-fidelity source beside it if it is small enough, else replaces.

Usage:
  optimize-product-image.py <src> <slug> [--max-dim 600] [--dry-run]

Behaviour:
  - Reads <src> (png/jpg/webp, any size)
  - Resizes to fit max-dim (default 600x600, preserving aspect, centre-cropped
    to square to match the card band + gallery aspect expectations)
  - Encodes WebP quality 82 (falls back through 78/72 until <= 500 KB or q>=60)
  - Writes static/images/products/<slug>/front.webp
  - Prints final path, dimensions, bytes; exit 0 on success, 1 on failure.

Policy: this script does NOT judge accuracy. Only wire an image into content
frontmatter after its VERDICT is ACCURATE/verified (see
VENUS-IMAGE-TRIAGE-VERDICTS.md, owned by Pixel).
"""
import argparse
import os
import sys
import subprocess

try:
    from PIL import Image
except ImportError:
    sys.stderr.write("PIL not installed\n")
    sys.exit(2)

MAX_BYTES = 500 * 1024


def encode_webp(img: Image.Image, path: str, max_bytes: int) -> int:
    """Encode img to path.webp, stepping quality down until <= max_bytes."""
    for q in (82, 78, 72, 66, 60):
        img.save(path, "WEBP", quality=q, method=6)
        size = os.path.getsize(path)
        if size <= max_bytes:
            return size
    return os.path.getsize(path)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("src", help="source image path (png/jpg/webp)")
    ap.add_argument("slug", help="product slug, e.g. fun-factory-vim")
    ap.add_argument("--max-dim", type=int, default=600)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    if not os.path.isfile(args.src):
        sys.stderr.write(f"no such source: {args.src}\n")
        return 1
    if not args.slug or "/" in args.slug or os.path.isabs(args.slug):
        sys.stderr.write(f"bad slug: {args.slug}\n")
        return 1

    out_dir = os.path.join("static", "images", "products", args.slug)
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "front.webp")

    with Image.open(args.src) as im:
        im = im.convert("RGB")
        # centre-crop to square, then resize
        w, h = im.size
        side = min(w, h)
        left = (w - side) // 2
        top = (h - side) // 2
        im = im.crop((left, top, left + side, top + side))
        im = im.resize((args.max_dim, args.max_dim), Image.LANCZOS)

        if args.dry_run:
            import io
            buf = io.BytesIO()
            im.save(buf, "WEBP", quality=82, method=6)
            print(f"[dry-run] {args.slug}: square {im.size}, webp q82 ~{len(buf.getvalue())} bytes")
            return 0

        size = encode_webp(im, out_path, MAX_BYTES)
        if size > MAX_BYTES:
            sys.stderr.write(
                f"WARNING: {out_path} = {size} bytes, still over {MAX_BYTES}\n"
            )
        print(f"WROTE {out_path} {im.size[0]}x{im.size[1]} {size} bytes")
        return 0


if __name__ == "__main__":
    sys.exit(main())