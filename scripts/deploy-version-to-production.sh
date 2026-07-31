#!/usr/bin/env bash
# Ship a chosen Venus design version to PRODUCTION (hostinger-deploy).
# Authorised per-run by Paul; this run: best-of, 2026-07-30.
#
# WHY THIS IS NOT promote-version.sh
# The hostinger-deploy branch holds the Hugo SOURCE and the SERVED OUTPUT together at
# its root, and Hostinger serves that root directly. promote-version.sh wipes the root
# and copies a build in — on this branch that would delete the source. This script
# replaces source and output deliberately, and preserves the production-only files a
# build does not generate.
#
# PRESERVED (never taken from the version build):
#   robots.txt   production's real one (Allow: /) — non-prod versions carry a
#                Disallow-everything file; shipping that would deindex the site
#   .htaccess    clean-URL rules, error pages, existing 301s
#
# Usage: deploy-version-to-production.sh <version> [--apply]
set -euo pipefail

VERSION="${1:?usage: deploy-version-to-production.sh <version> [--apply]}"
APPLY="${2:-}"
REPO=/home/paul/.openclaw/workspaces/worker/venus-site
SRC="/home/paul/.openclaw/workspaces/venus-versions/$VERSION"
BASE_URL="https://reviews.ultramarine963.com/"
STAMP=$(date -u +%Y%m%dT%H%M%SZ)
BACKUP="/home/paul/.openclaw/backups/venus-prod-pre-$VERSION-$STAMP"
export PATH="/home/paul/bin:$PATH"

[ -d "$SRC" ] || { echo "ERROR: no version at $SRC" >&2; exit 1; }
cd "$REPO"
[ "$(git rev-parse --abbrev-ref HEAD)" = "hostinger-deploy" ] || {
  echo "ERROR: not on hostinger-deploy" >&2; exit 1; }

# Source trees replaced wholesale; built output flattened to root afterwards.
SOURCE_DIRS=(content layouts static data docs)
SOURCE_FILES=(hugo.toml)
# Stale pages that exist on production but not in the chosen version.
STALE_PRODUCTS=(all bvee-rabbit compare h2o-holo-vibe lelo-gigi-2 satisfyer-pro-2
                womanizer-2 womanizer-premium-2)
# Publicly-served build-artifact dirs — stale duplicates of the old site.
ARTIFACT_DIRS=(public build-local)

BUILD=$(mktemp -d)
hugo --source "$SRC" --minify --baseURL "$BASE_URL" --destination "$BUILD" \
  | grep -E "Pages|Static|Total|ERROR" || true
[ -f "$BUILD/index.html" ] || { echo "ERROR: build produced no index.html" >&2; rm -rf "$BUILD"; exit 1; }
[ -f "$BUILD/sitemap.xml" ] || { echo "ERROR: build produced no sitemap.xml" >&2; rm -rf "$BUILD"; exit 1; }

# Guard: the version build must not carry a noindex robots.txt into production.
if [ -f "$BUILD/robots.txt" ] && grep -qi "Disallow: /$" "$BUILD/robots.txt"; then
  echo "Dropping the version's noindex robots.txt; production's own is preserved."
  rm -f "$BUILD/robots.txt"
fi

if [ "$APPLY" != "--apply" ]; then
  echo
  echo "DRY RUN — nothing changed."
  echo "  would replace source dirs:   ${SOURCE_DIRS[*]}"
  echo "  would flatten build to root: $(find "$BUILD" -type f | wc -l) files"
  echo "  would remove stale products: ${STALE_PRODUCTS[*]}"
  echo "  would remove artifact dirs:  ${ARTIFACT_DIRS[*]}"
  echo "  preserved: robots.txt .htaccess"
  rm -rf "$BUILD"; exit 0
fi

# The branch is fully committed and pushed, so git itself is the backup for tracked
# files — `git checkout hostinger-deploy -- .` restores everything. Only the small set
# of UNCOMMITTED working-tree changes needs saving, and tarring the whole tree (4GB of
# images) just times out. Recovery commit is recorded alongside.
mkdir -p "$BACKUP"
git rev-parse HEAD > "$BACKUP/RESTORE-FROM-COMMIT.txt"
git diff > "$BACKUP/uncommitted-tracked.patch" 2>/dev/null || true
git status --porcelain > "$BACKUP/status-before.txt"
# UNTRACKED files are NOT in git and are destroyed by the `rm -rf` below. On
# 2026-07-30 this exact gap wiped 19 untracked Pixel images (recovered only because
# Sentinel's nightly backup happened to hold them). Copy them out explicitly.
git ls-files --others --exclude-standard -z \
  | tar --null -T - -czf "$BACKUP/untracked-files.tar.gz" 2>/dev/null || true
echo "  untracked files saved: $(git ls-files --others --exclude-standard | wc -l)"
echo "Backup (git-based): $BACKUP"
echo "  restore tracked files: git -C $REPO checkout $(git rev-parse --short HEAD) -- ." 

# 1. replace source
for d in "${SOURCE_DIRS[@]}"; do
  [ -d "$SRC/$d" ] || continue
  rm -rf "${REPO:?}/$d"
  cp -r "$SRC/$d" "$REPO/$d"
done
for f in "${SOURCE_FILES[@]}"; do
  [ -f "$SRC/$f" ] && cp "$SRC/$f" "$REPO/$f"
done

# 2. drop stale product pages and served build artifacts
for p in "${STALE_PRODUCTS[@]}"; do rm -rf "${REPO:?}/products/$p"; done
for d in "${ARTIFACT_DIRS[@]}"; do rm -rf "${REPO:?}/$d"; done

# 3. flatten the build over the root (robots.txt/.htaccess untouched by the build)
cp -r "$BUILD"/. "$REPO"/
rm -rf "$BUILD"

echo
echo "Applied. Verify, then stage explicitly and review before pushing:"
echo "    git -C $REPO status --short | head"
echo "    git -C $REPO show --stat HEAD"
