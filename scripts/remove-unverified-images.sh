#!/usr/bin/env bash
# Remove unverified Venus product imagery — AI renders, web-page screenshots, and
# the two genuine-but-wrong-product photos. PREPARED, NOT RUN: needs Paul's approval.
#
# Provenance was settled by md5-matching Pixel's own generation archive
# (workspaces/image-creator/venus-images/, 77 files) against the live library:
#   .png/.jpg  37 files —  0 byte-identical to AI generations  -> genuine, KEEP
#   .webp      54 files — 36 byte-identical to AI generations  -> REMOVE
#                          18 others are 1024x1024 web-page screenshots -> REMOVE
# Plus lelo-mona/front.jpg and top.png: genuine photos, but of the WRONG products
# (dual-arm rabbit and flat pebble massager; the Mona 2 is a single-arm wand).
# Full detail: workspaces/image-creator/venus-image-parity/CLAW-ANSWER-KEY.md
#
# Net effect: 91 -> 35 verified-genuine images. Three products lose all imagery
# (fun-factory-manta, fun-factory-volta, we-vibe-sync) — they have no legitimate
# images to begin with. Real product photos arrive with affiliate approval.
#
# Usage:
#   ./remove-unverified-images.sh --dry-run     # default; prints, changes nothing
#   ./remove-unverified-images.sh --apply       # versions only, never production
#
# Production is deliberately OUT OF SCOPE here: hostinger-deploy holds source and
# served output at its root and carries unrelated uncommitted work, so it needs a
# separate surgical pass (same pattern as the testimonial/testing-claim removals).
set -euo pipefail

MODE="${1:---dry-run}"
VERSIONS_ROOT=/home/paul/.openclaw/workspaces/venus-versions
BACKUP_DIR="/home/paul/.openclaw/backups/venus-unverified-images-$(date -u +%Y%m%dT%H%M%SZ)"
WRONG_PRODUCT=(lelo-mona/front.jpg lelo-mona/top.png)

removed=0; kept=0
for vdir in "$VERSIONS_ROOT"/*/; do
  [ -d "$vdir/static/images/products" ] || continue
  version=$(basename "$vdir")
  base="$vdir/static/images/products"

  while IFS= read -r f; do
    rel="${f#"$base"/}"
    if [ "$MODE" = "--apply" ]; then
      mkdir -p "$BACKUP_DIR/$version/$(dirname "$rel")"
      mv "$f" "$BACKUP_DIR/$version/$rel"
    fi
    removed=$((removed+1))
  done < <(find "$base" -name '*.webp')

  for w in "${WRONG_PRODUCT[@]}"; do
    f="$base/$w"
    [ -f "$f" ] || continue
    if [ "$MODE" = "--apply" ]; then
      mkdir -p "$BACKUP_DIR/$version/$(dirname "$w")"
      mv "$f" "$BACKUP_DIR/$version/$w"
    fi
    removed=$((removed+1))
  done

  kept=$((kept + $(find "$base" -type f ! -name '*.webp' | wc -l)))
done

echo "mode: $MODE"
echo "images removed: $removed"
echo "images kept:    $kept"
[ "$MODE" = "--apply" ] && echo "backup: $BACKUP_DIR"

cat <<'NEXT'

Content references still need updating — product front matter and markdown bodies point at
removed files. After --apply, run a reference sweep before promoting:

  grep -rn '\.webp' <version>/content/products/*/index.md
  grep -rln 'lelo-mona/\(front\.jpg\|top\.png\)' <version>/content/

Then rebuild + link-check (check-gallery-links.sh will catch any missed reference as a 404)
before pushing. Production requires its own separate surgical pass.
NEXT
