#!/usr/bin/env python3
"""Classify the provenance of imagery live on the Venus site, and remove what is provably AI.

Authorised by Paul 2026-07-29 ("go ahead, previews first then production").
Rewritten 2026-08-05 after the classifier was found to fail open (see below).

WHY THIS WAS REWRITTEN
The previous version decided provenance by md5-matching Pixel's generation archive
(workspaces/image-creator/venus-images/) and recorded the outcome as:

    .png/.jpg  - 0 of 37 matched an AI generation  -> genuine, KEEP
    .webp      - 36 of 54 matched exactly          -> AI renders, REMOVE

The first line is the bug. "No md5 match" is not evidence of anything except that
the file was absent from the one folder that was searched. Seven ComfyUI-generated
PNGs for womanizer-2-original came from an earlier generation round that was never
copied into that archive, so the lookup returned empty and they were filed as
genuine. They were live on production until 2026-08-05 (removed by hand in 57a984f
and 72226e3).

So: absence of evidence is now UNKNOWN, never GENUINE. Three states, not two.

    MATCHED_AI       positive evidence the file was generated.
    VERIFIED_GENUINE positive evidence the file was photographed / supplied by the
                     brand. Only this state is safe to keep silently.
    UNKNOWN          neither. Reported loudly, never auto-kept, never auto-removed.
                     Any UNKNOWN makes this script exit non-zero, so it cannot
                     report a clean pass while unclassified imagery is live.

EVIDENCE OF GENERATION (any one is sufficient)
  - embedded generator metadata: a ComfyUI/A1111 workflow in a PNG text chunk
  - md5 identical to a file in a generation archive
  - ComfyUI output filename convention (`*_00001_.png`)
  - the product is named in images/products/README.md, which documents which
    products were generated via local ComfyUI. That naming overrides a hash miss -
    the hash miss is exactly the failure mode that let womanizer through.
    NB: the "VERIFIED" labels in that README mean "verified free of people and
    faces". They are not provenance claims. Do not read them as such.

EVIDENCE OF GENUINENESS (a STRONG signal is required)
  strong: camera/EXIF metadata in the file, or a documented source URL recorded in
          ATTESTATIONS below and pinned to the file's md5.
  weak:   the model name embossed on the device in-image, correct product geometry,
          a non-square aspect ratio.

  Weak signals alone leave a file UNKNOWN. They are recorded because they are worth
  something to a human triaging the report, but they cannot promote a file on their
  own - a diffusion model renders embossed lettering and 3:2 crops perfectly well.
  Note in particular that 1536x1024 is both an SDXL bucket and the 35mm frame ratio,
  so "non-square" separates nothing.

  There is no heuristic path to VERIFIED_GENUINE. A file gets there only by someone
  looking at it, finding where it came from, and adding an entry to ATTESTATIONS.
  That is the point: the previous classifier's mistake was letting a computed
  property stand in for a provenance record.

WHY IN-PLACE, NOT A REBUILD
hostinger-deploy holds the Hugo source AND the served output at its branch root, and
the working tree carries unrelated uncommitted work. A rebuild would strip source off
the branch and ship that work unreviewed. Same surgical pattern as commits 9f4c128
(testimonials) and c41ab69 (testing claims).

Usage:  remove-prod-unverified-images.py [--apply] [--all]
        default: dry run over live imagery (referenced from served .html/.css/.js)
        --all:   classify every tracked image, not just what is live
        --apply: delete MATCHED_AI files and scrub their references. Never touches
                 UNKNOWN.
Exit:   0 = every classified file resolved, nothing unknown
        1 = at least one UNKNOWN file (this is not a failure of the script)
Never pushes. Stage explicitly and review `git show --stat` before pushing.
"""
import hashlib
import re
import shutil
import subprocess
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

REPO = Path("/home/paul/.openclaw/workspaces/worker/venus-site")
ARCHIVES = [Path("/home/paul/.openclaw/workspaces/image-creator/venus-images")]
APPLY = "--apply" in sys.argv
SCAN_ALL = "--all" in sys.argv
STAMP = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
BACKUP = Path(f"/home/paul/.openclaw/backups/venus-prod-unverified-images-{STAMP}")

IMG_EXT = {".png", ".jpg", ".jpeg", ".webp", ".gif", ".avif"}
# Directories on the branch that are not the served site: build mirrors, history,
# Hugo source. The branch root itself is what production serves.
NOT_SERVED = {"public", "static", "archive", ".claude", ".backup", "content",
              "layouts", "scripts", "docs", "screenshots", "themes", "config",
              "affiliate-research", "lab", "node_modules"}

MATCHED_AI, VERIFIED_GENUINE, UNKNOWN = "MATCHED_AI", "VERIFIED_GENUINE", "UNKNOWN"

# Generated imagery that is deliberate and disclosed: abstract decorative art that
# depicts no real product, shown where a product has no genuine photography (the
# product-page template says as much in prose). These still classify as MATCHED_AI -
# they are generated and the report must say so - but --apply leaves them alone,
# because deleting them degrades pages instead of correcting a false claim.
# Only ever add paths here that depict no real, trademarked product.
DISCLOSED_DECORATIVE = ("images/placeholders/",)

# Product slugs used in image paths, keyed by the product name as written in
# images/products/README.md. The README names products, not paths.
# Keep these specific. A bare brand alias ("womanizer") would sweep in Womanizer
# Premium 2, a different product the README does not name.
README_NAME_TO_SLUGS = {
    "womanizer 2": ("womanizer-2", "womanizer-2-original"),
    "bvee rabbit": ("bvee-rabbit", "bvee-original-rabbit"),
    "lelo mona": ("lelo-mona",),
}

# md5 -> provenance record. The ONLY route to VERIFIED_GENUINE.
# source_url must be a real, checkable origin for the file. An entry with an empty
# source_url and no EXIF is deliberately not sufficient - it stays UNKNOWN and shows
# up in the report with its evidence, so it is obvious what is still missing.
ATTESTATIONS: dict[str, dict] = {
    # (empty) Nothing in this library has a recorded source URL yet. See the
    # 2026-08-05 report: the ten live lelo-hugo / lelo-sona-2 / lovehoney-desire
    # images carry weak positive evidence only.
}

# PNG text-chunk keys that mean "a generator wrote this".
GENERATOR_KEYS = {"prompt", "workflow", "parameters", "sd-metadata", "Comment"}
GENERATOR_MARKERS = re.compile(
    r"ComfyUI|CheckpointLoaderSimple|KSampler|sd_xl|stable-diffusion|"
    r"CLIPTextEncode|EmptyLatentImage|automatic1111", re.I)
COMFY_FILENAME = re.compile(r"_\d{5}_\.(png|jpg|jpeg|webp)$", re.I)
IMG_REF = re.compile(
    r"""["'(]\s*(/images/[A-Za-z0-9/_.@%-]+?\.(?:png|jpe?g|webp|gif|avif))""", re.I)


def md5(path: Path) -> str:
    h = hashlib.md5()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def archive_index() -> dict[str, list[str]]:
    """md5 -> archive paths, over every archive root, recursively."""
    idx: dict[str, list[str]] = defaultdict(list)
    for root in ARCHIVES:
        if not root.is_dir():
            print(f"WARNING: archive root missing, hash matching is degraded: {root}",
                  file=sys.stderr)
            continue
        for p in root.rglob("*"):
            if p.is_file() and p.suffix.lower() in IMG_EXT:
                idx[md5(p)].append(str(p.relative_to(root)))
    return idx


def readme_ai_slugs() -> tuple[set[str], set[str]]:
    """Products and explicit filenames the products README documents as generated.

    Returns (slugs, filenames). Parsed from the README rather than hardcoded so that
    adding a product to that file automatically closes the loop here.
    """
    readme = REPO / "images/products/README.md"
    slugs: set[str] = set()
    files: set[str] = set()
    if not readme.is_file():
        print(f"WARNING: {readme} missing; README cross-check disabled", file=sys.stderr)
        return slugs, files
    text = readme.read_text("utf8", errors="ignore")
    if not re.search(r"ComfyUI", text, re.I):
        return slugs, files
    low = text.lower()
    for name, mapped in README_NAME_TO_SLUGS.items():
        if name in low:
            slugs.update(mapped)
    files.update(re.findall(r"`([A-Za-z0-9_.-]+\.(?:png|jpe?g|webp))`", text))
    return slugs, files


def generator_metadata(path: Path):
    """Return a description of embedded generator metadata, or None."""
    try:
        from PIL import Image
    except ImportError:
        return None
    try:
        with Image.open(path) as im:
            info = im.info
            for key in GENERATOR_KEYS:
                val = info.get(key)
                if isinstance(val, str) and GENERATOR_MARKERS.search(val):
                    return f"embedded {key!r} chunk names a generator workflow"
            for key, val in info.items():
                if isinstance(val, str) and GENERATOR_MARKERS.search(val):
                    return f"embedded {key!r} metadata names a generator"
    except Exception:
        return None
    return None


def camera_metadata(path: Path):
    """Return a description of camera EXIF, or None. Make/Model only - a bare
    orientation or resolution tag is written by any resizer and proves nothing."""
    try:
        from PIL import Image
    except ImportError:
        return None
    try:
        with Image.open(path) as im:
            exif = im.getexif()
            if not exif:
                return None
            make, model = exif.get(271), exif.get(272)
            if make or model:
                return f"EXIF camera {make or '?'} {model or ''}".strip()
    except Exception:
        return None
    return None


def dimensions(path: Path):
    try:
        from PIL import Image
        with Image.open(path) as im:
            return im.size
    except Exception:
        return None


def slugs_in_path(rel: str, slugs: set[str]) -> list[str]:
    """Which product slugs appear in this path.

    Substring match on a non-alphanumeric boundary, not a path-component split:
    the slug shows up as `images/products/lelo-mona/front.jpg` but equally as
    `images/products/product-lelo-mona.jpg`, and a component split only catches
    the first.
    """
    low = rel.lower()
    return sorted(s for s in slugs
                  if re.search(rf"(?<![a-z0-9]){re.escape(s)}(?![a-z0-9])", low))


def classify(rel: str, arch: dict[str, list[str]], ai_slugs: set[str],
             ai_files: set[str]) -> dict:
    """Three-way classification of one image. Never returns GENUINE by default."""
    path = REPO / rel
    name = Path(rel).name
    digest = md5(path)
    ai_reasons, weak = [], []

    hit = arch.get(digest)
    if hit:
        ai_reasons.append(f"md5 matches generation archive: {hit[0]}")

    gen = generator_metadata(path)
    if gen:
        ai_reasons.append(gen)

    if COMFY_FILENAME.search(name):
        ai_reasons.append("ComfyUI output filename convention")

    if name in ai_files:
        ai_reasons.append("named as ComfyUI output in images/products/README.md")

    named = slugs_in_path(rel, ai_slugs)
    if named:
        ai_reasons.append(
            f"product {named[0]!r} documented as ComfyUI-generated in "
            f"images/products/README.md (overrides hash result)")

    if ai_reasons:
        if rel.startswith(DISCLOSED_DECORATIVE):
            ai_reasons.append("disclosed decorative art, depicts no real product: RETAINED")
        return {"file": rel, "state": MATCHED_AI, "md5": digest,
                "reasons": ai_reasons, "weak": weak, "size": dimensions(path),
                "retain": rel.startswith(DISCLOSED_DECORATIVE)}

    cam = camera_metadata(path)
    att = ATTESTATIONS.get(digest)
    strong = []
    if cam:
        strong.append(cam)
    if att and att.get("source_url"):
        strong.append(f"documented source {att['source_url']} "
                      f"(attested {att.get('reviewed_on', '?')})")

    if att and att.get("evidence"):
        weak.append(att["evidence"])
    size = dimensions(path)
    if size and size[0] != size[1]:
        weak.append(f"non-square {size[0]}x{size[1]}")

    if strong:
        return {"file": rel, "state": VERIFIED_GENUINE, "md5": digest,
                "reasons": strong, "weak": weak, "size": size}

    return {"file": rel, "state": UNKNOWN, "md5": digest,
            "reasons": ["no camera metadata and no documented source"],
            "weak": weak, "size": size}


# Every served file type that can reference an image. CSS matters as much as HTML:
# the site's most prominent image, the homepage hero, is set only as a
# background-image in site-polish.css. Scanning HTML alone reported a clean live
# set while never examining it - a confident pass over an unexamined surface,
# which is the same failure this script exists to prevent.
SERVED_GLOBS = ("*.html", "*.css", "*.js")


def served_files() -> list[Path]:
    out: list[Path] = []
    for pattern in SERVED_GLOBS:
        out += [p for p in REPO.rglob(pattern)
                if not (set(p.relative_to(REPO).parts) & NOT_SERVED)]
    return out


def live_images() -> dict[str, set[str]]:
    """Image path (repo-relative) -> served files that reference it."""
    refs: dict[str, set[str]] = defaultdict(set)
    for page in served_files():
        try:
            text = page.read_text("utf8", errors="ignore")
        except OSError:
            continue
        for url in IMG_REF.findall(text):
            refs[url.lstrip("/")].add(str(page.relative_to(REPO)))
    return refs


def tracked_images() -> list[str]:
    out = subprocess.run(["git", "-C", str(REPO), "ls-files", "images/"],
                         capture_output=True, text=True).stdout
    return [l for l in out.splitlines() if Path(l).suffix.lower() in IMG_EXT]


def product_of(rel: str) -> str:
    m = re.match(r"images/products/([a-z0-9-]+)/", rel)
    if m:
        return m.group(1)
    if rel.startswith("images/placeholders/"):
        return "(placeholder)"
    if rel.startswith("images/products/"):
        return "(loose product image)"
    return "(site chrome)"


def backup(rel: str) -> None:
    dst = BACKUP / rel
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(REPO / rel, dst)


def remove(results: list[dict]) -> tuple[int, int, int]:
    """Delete MATCHED_AI files and scrub references. UNKNOWN is never touched."""
    doomed = [r["file"] for r in results
              if r["state"] == MATCHED_AI and not r.get("retain")]
    if not doomed:
        return 0, 0, 0
    urls = {"/" + f for f in doomed}
    url_re = re.compile("|".join(re.escape(u) for u in sorted(urls)))
    img_tag = re.compile(
        r"\s*<img[^>]*?(?:" + "|".join(re.escape(u) for u in sorted(urls)) + r")[^>]*?>\s*",
        re.I)

    removed = 0
    for rel in doomed:
        p = REPO / rel
        if not p.is_file():
            continue
        if APPLY:
            backup(rel)
            p.unlink()
        removed += 1

    touched = refs = 0
    text_exts = {".html", ".md", ".xml", ".json", ".css", ".js"}
    for p in REPO.rglob("*"):
        if not p.is_file() or p.suffix.lower() not in text_exts:
            continue
        if set(p.relative_to(REPO).parts) & {".git", "node_modules"}:
            continue
        try:
            orig = p.read_text("utf8")
        except (UnicodeDecodeError, OSError):
            continue
        if not url_re.search(orig):
            continue
        text = img_tag.sub("\n", orig)
        text = re.sub(r'^\s*image:\s*"[^"]*"\s*\n',
                      lambda m: "" if url_re.search(m.group(0)) else m.group(0),
                      text, flags=re.M)
        text = re.sub(r'^!\[[^\]]*\]\([^)]*\)\s*\n',
                      lambda m: "" if url_re.search(m.group(0)) else m.group(0),
                      text, flags=re.M)
        text = re.sub(r"\n{3,}", "\n\n", text)
        if text != orig:
            n = len(url_re.findall(orig)) - len(url_re.findall(text))
            if APPLY:
                backup(str(p.relative_to(REPO)))
                p.write_text(text, encoding="utf8")
            touched += 1
            refs += n
    return removed, touched, refs


def report(results: list[dict], refs: dict[str, set[str]]) -> None:
    by_state = defaultdict(list)
    for r in results:
        by_state[r["state"]].append(r)

    for state in (MATCHED_AI, VERIFIED_GENUINE, UNKNOWN):
        rows = sorted(by_state[state], key=lambda r: r["file"])
        print(f"\n{'=' * 78}\n{state}  ({len(rows)} files)\n{'=' * 78}")
        for r in rows:
            size = f"{r['size'][0]}x{r['size'][1]}" if r["size"] else "?"
            pages = len(refs.get(r["file"], ()))
            print(f"  {r['file']}  [{size}, {pages} page(s)]")
            for reason in r["reasons"]:
                print(f"      + {reason}")
            for w in r["weak"]:
                print(f"      ~ weak: {w}")

    print(f"\n{'=' * 78}\nPER-PRODUCT ROLLUP\n{'=' * 78}")
    per = defaultdict(lambda: defaultdict(int))
    for r in results:
        per[product_of(r["file"])][r["state"]] += 1
    for prod in sorted(per):
        counts = per[prod]
        bits = ", ".join(f"{k}={counts[k]}" for k in
                         (MATCHED_AI, VERIFIED_GENUINE, UNKNOWN) if counts[k])
        print(f"  {prod:28s} {bits}")


def main() -> int:
    arch = archive_index()
    ai_slugs, ai_files = readme_ai_slugs()
    refs = live_images()

    if SCAN_ALL:
        targets = sorted(set(tracked_images()) | set(refs))
    else:
        targets = sorted(refs)

    results = [classify(rel, arch, ai_slugs, ai_files)
               for rel in targets if (REPO / rel).is_file()]

    print(f"mode:    {'APPLY' if APPLY else 'dry-run'}")
    print(f"scope:   {'every tracked image' if SCAN_ALL else 'live imagery (html/css/js)'}")
    print(f"archive: {sum(len(v) for v in arch.values())} hashes indexed")
    print(f"README:  products flagged AI -> {sorted(ai_slugs) or 'none'}")
    print(f"files:   {len(results)}")

    report(results, refs)

    removed, touched, ref_count = remove(results)
    unknown = [r for r in results if r["state"] == UNKNOWN]

    print(f"\n{'=' * 78}\nSUMMARY\n{'=' * 78}")
    print(f"  MATCHED_AI       {sum(1 for r in results if r['state'] == MATCHED_AI)}")
    print(f"  VERIFIED_GENUINE {sum(1 for r in results if r['state'] == VERIFIED_GENUINE)}")
    print(f"  UNKNOWN          {len(unknown)}")
    print(f"  files {'removed' if APPLY else 'would remove'}: {removed}")
    print(f"  text files {'touched' if APPLY else 'would touch'}: {touched} "
          f"({ref_count} references)")
    if APPLY and removed:
        print(f"  backup: {BACKUP}")

    if unknown:
        print(f"\n!! {len(unknown)} file(s) of UNKNOWN provenance are in scope.")
        print("!! They were neither kept as verified nor removed as AI. Nothing here")
        print("!! is a clean pass until each one has a source recorded in")
        print("!! ATTESTATIONS or is confirmed generated and removed.")
        for r in unknown:
            print(f"     {r['file']}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
