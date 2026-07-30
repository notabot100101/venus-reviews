#!/usr/bin/env python3
"""Remove unverified imagery from the LIVE Venus site (hostinger-deploy working tree).

Authorised by Paul 2026-07-29 ("go ahead, previews first then production").

WHAT IS UNVERIFIED, AND HOW WE KNOW
Provenance was settled by md5-matching Pixel's own generated-image archive
(workspaces/image-creator/venus-images/, 77 files) against the library:
  .png/.jpg  — 0 of 37 matched an AI generation  -> genuine, KEEP
  .webp      — 36 of 54 matched exactly          -> AI renders, REMOVE
               the other 18 are 1024x1024 web-page screenshots -> REMOVE
Plus lelo-mona/front.jpg and top.png: genuine photos of the WRONG products
(dual-arm rabbit / flat pebble massager; the Mona 2 is a single-arm wand).
Detail: workspaces/image-creator/venus-image-parity/CLAW-ANSWER-KEY.md

WHY IN-PLACE, NOT A REBUILD
hostinger-deploy holds the Hugo source AND the served output at its branch root, and
the working tree carries unrelated uncommitted work. A rebuild would strip source off
the branch and ship that work unreviewed. Same surgical pattern as commits 9f4c128
(testimonials) and c41ab69 (testing claims).

Usage:  remove-prod-unverified-images.py [--apply]     (default: dry run)
Never pushes. Stage explicitly and review `git show --stat` before pushing.
"""
import re
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO = Path("/home/paul/.openclaw/workspaces/worker/venus-site")
APPLY = "--apply" in sys.argv
STAMP = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
BACKUP = Path(f"/home/paul/.openclaw/backups/venus-prod-unverified-images-{STAMP}")

WRONG = ("images/products/lelo-mona/front.jpg", "images/products/lelo-mona/top.png")
DEAD_URL = re.compile(
    r'/images/products/[^"\'\s>)]*\.webp'
    r'|/images/products/lelo-mona/front\.jpg'
    r'|/images/products/lelo-mona/top\.png')
# <img ...dead...> including any wrapping <picture>/<source> siblings is overkill here;
# the live markup is plain <img> tags, verified before writing this.
IMG_TAG = re.compile(r'\s*<img[^>]*?(?:\.webp|lelo-mona/(?:front\.jpg|top\.png))[^>]*?>\s*',
                     re.I)


def tracked(pattern: str) -> list[str]:
    out = subprocess.run(["git", "-C", str(REPO), "ls-files", pattern],
                         capture_output=True, text=True).stdout
    return [l for l in out.splitlines() if l]


def backup(rel: str) -> None:
    src = REPO / rel
    dst = BACKUP / rel
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)


def main() -> int:
    # 1. image files themselves
    files = sorted(set(tracked("*.webp")) |
                   {p for w in WRONG for p in tracked(f"*{Path(w).name}")
                    if "lelo-mona" in p})
    removed_files = 0
    for rel in files:
        if not (REPO / rel).is_file():
            continue
        if APPLY:
            backup(rel)
            (REPO / rel).unlink()
        removed_files += 1

    # 2. references inside text files
    text_exts = {".html", ".md", ".xml", ".json", ".css", ".js"}
    touched, refs = 0, 0
    for rel in subprocess.run(["git", "-C", str(REPO), "grep", "-l", "-I", r"\.webp\|lelo-mona/front\.jpg\|lelo-mona/top\.png"],
                              capture_output=True, text=True).stdout.splitlines():
        p = REPO / rel
        if not p.is_file() or p.suffix.lower() not in text_exts:
            continue
        try:
            orig = p.read_text(encoding="utf8")
        except UnicodeDecodeError:
            continue
        text = IMG_TAG.sub("\n", orig)                      # served HTML
        text = re.sub(r'^\s*image:\s*"[^"]*(?:\.webp|lelo-mona/(?:front\.jpg|top\.png))"\s*\n',
                      "", text, flags=re.M)                  # front matter key
        text = re.sub(r'^\s*-\s*(?:src:\s*)?"[^"]*(?:\.webp|lelo-mona/(?:front\.jpg|top\.png))"\s*\n'
                      r'(?:\s+(?:alt|caption):.*\n)*', "", text, flags=re.M)  # list items
        text = re.sub(r'^!\[[^\]]*\]\([^)]*(?:\.webp|lelo-mona/(?:front\.jpg|top\.png))\)\s*\n',
                      "", text, flags=re.M)                  # markdown images
        text = re.sub(r'\n{3,}', '\n\n', text)
        if text != orig:
            n = len(DEAD_URL.findall(orig)) - len(DEAD_URL.findall(text))
            if APPLY:
                backup(rel)
                p.write_text(text, encoding="utf8")
            touched += 1
            refs += n

    print(f"mode: {'APPLY' if APPLY else 'dry-run'}")
    print(f"image files removed: {removed_files}")
    print(f"text files touched:  {touched}")
    print(f"references removed:  {refs}")
    if APPLY:
        print(f"backup: {BACKUP}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
