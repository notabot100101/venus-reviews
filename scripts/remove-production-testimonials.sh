#!/usr/bin/env bash
# Remove the fabricated testimonial sections from the LIVE Venus site.
#
# WHY (found 2026-07-28, authorised by Paul 2026-07-29)
# ----------------------------------------------------
# The homepage carries four testimonials attributed to named people - "Sarah M.",
# "James K.", "Emily R.", "Marcus T." - with star ratings, generated avatars and
# first-person purchase quotes, under a header reading "Short trust checks from
# real buyers". Two stale product pages go further and label them "Verified
# Tester" under "What Our Testers Say".
#
# None are real. They are hardcoded, carry no provenance, and the site has no
# comment system, no accounts and no purchase path (its buy buttons render a
# disabled "Coming soon" placeholder because every AFFILIATE_ID_* is still a
# placeholder). Fabricated consumer testimonials on a commercial site are an FTC
# matter (16 CFR Part 465, in force since October 2024).
#
# WHY THIS IS SURGICAL, NOT A REBUILD
# -----------------------------------
# The hostinger-deploy branch holds BOTH the Hugo source (layouts/, content/,
# hugo.toml) AND the flattened built output (index.html, products/...) at its
# root - Hostinger serves the branch root. Two consequences:
#   1. A "wipe root, copy build in" publish would delete the source off the
#      branch. Do not do that.
#   2. The working tree carries ~20 unrelated uncommitted changes (Pixel's
#      2026-07-27 product imagery). A rebuild would ship those too, which was
#      not authorised.
# So this edits only the affected files in place and commits only those files.
#
# It does NOT push. Hostinger auto-deploys on push, so that stays a separate
# deliberate step.
set -euo pipefail

REPO=/home/paul/.openclaw/workspaces/worker/venus-site
STRIPPER="$REPO/scripts/strip-testimonials.py"
BACKUP_DIR=/home/paul/.openclaw/backups
NAMES='Sarah M\.|James K\.|Emily R\.|Marcus T\.'

cd "$REPO"

BRANCH=$(git rev-parse --abbrev-ref HEAD)
if [ "$BRANCH" != "hostinger-deploy" ]; then
  echo "ERROR: expected to be on hostinger-deploy, found '$BRANCH'." >&2
  exit 1
fi

mapfile -t TARGETS < <(grep -rlE "$NAMES" \
  index.html layouts/index.html public/index.html products/ 2>/dev/null | sort -u)

if [ ${#TARGETS[@]} -eq 0 ]; then
  echo "Nothing to do - no fabricated testimonials found."
  exit 0
fi

echo "Files to clean:"
printf '  %s\n' "${TARGETS[@]}"
echo

TS=$(date -u +%Y%m%dT%H%M%SZ)
SNAP="$BACKUP_DIR/venus-prod-testimonials-$TS"
mkdir -p "$SNAP"
for f in "${TARGETS[@]}"; do
  mkdir -p "$SNAP/$(dirname "$f")"
  cp "$f" "$SNAP/$f"
done
echo "Backed up originals -> $SNAP"
echo

python3 "$STRIPPER" "${TARGETS[@]}"
find . -name '*.pre-testimonial-strip' -newermt '-5 minutes' -delete 2>/dev/null || true

echo
FAILED=0
for f in "${TARGETS[@]}"; do
  if grep -qE "$NAMES" "$f"; then
    echo "ERROR: names still present in $f"
    FAILED=1
  fi
done
if [ "$FAILED" -ne 0 ]; then
  echo "Restoring from backup and aborting." >&2
  for f in "${TARGETS[@]}"; do cp "$SNAP/$f" "$f"; done
  exit 1
fi
echo "Verified: no fabricated names remain in any target file."

# Sanity-check the homepage still has its other sections and balanced markup.
for f in index.html public/index.html; do
  [ -f "$f" ] || continue
  o=$(grep -o '<section' "$f" | wc -l); c=$(grep -o '</section>' "$f" | wc -l)
  if [ "$o" -ne "$c" ]; then
    echo "ERROR: unbalanced <section> tags in $f ($o open / $c close). Restoring." >&2
    for g in "${TARGETS[@]}"; do cp "$SNAP/$g" "$g"; done
    exit 1
  fi
  echo "  $f: $o sections, markup balanced"
done

# Stage ONLY these files - the tree has unrelated uncommitted work.
git add -- "${TARGETS[@]}"
echo
echo "Staged (nothing else):"
git diff --cached --stat

if git diff --cached --quiet; then
  echo "No staged changes; nothing to commit."
  exit 0
fi

git commit -q -m "fix: remove fabricated testimonials from live site

The homepage presented four invented people as real buyers, with star ratings
and quotes; two stale product pages labelled them Verified Testers. None were
real - they were hardcoded, and the site has no comments, accounts or purchase
path through which a testimonial could have been collected.

Fabricated consumer testimonials are an FTC matter (16 CFR Part 465)."

echo
echo "Committed. Review:   git -C $REPO show --stat HEAD"
echo "Restore if needed:   cp -r $SNAP/. $REPO/"
echo
echo "DEPLOY (irreversible - Hostinger auto-deploys on push):"
echo "    git -C $REPO push origin hostinger-deploy"
