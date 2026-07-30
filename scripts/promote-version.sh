#!/usr/bin/env bash
# Promote a Venus design version from an agent's sandboxed workspace into the
# canonical shared location, then build and publish it to its deploy branch.
#
# Agents cannot write to /home/paul/.openclaw/workspaces/venus-versions/ (it is
# outside their sandbox), so their real work lands in
# workspaces/<agent-ws>/venus-versions/<version>/ instead. This script is the
# bridge - see directives/site-project-repo-policy.md, "Known gap".
#
# Usage: promote-version.sh <version-name> <agent-workspace> <deploy-target>
#   <deploy-target> is either a branch name (whole-subdomain deploy) or
#   "preview:<subpath>" to publish into a subfolder of the preview gallery.
#
# Examples:
#   promote-version.sh data-driven planner preview:data-driven
#   promote-version.sh keep-current-polish worker dev
set -euo pipefail

VERSION="${1:?usage: promote-version.sh <version> <agent-workspace> <deploy-target>}"
AGENT_WS="${2:?missing agent workspace (e.g. planner, worker)}"
TARGET="${3:?missing deploy target (branch name, or preview:<subpath>)}"

WS_ROOT=/home/paul/.openclaw/workspaces
CANON="$WS_ROOT/venus-versions/$VERSION"
AGENT_COPY="$WS_ROOT/$AGENT_WS/venus-versions/$VERSION"
REPO="$WS_ROOT/worker/venus-site"
BACKUP_DIR=/home/paul/.openclaw/backups

# "canonical" means the shared copy is already the source of truth (nothing to
# reconcile) - used when rebuilding/redeploying a version no agent has touched.
if [ "$AGENT_WS" = "canonical" ]; then
  AGENT_COPY="$CANON"
fi

if [ ! -d "$AGENT_COPY" ]; then
  echo "ERROR: no source at $AGENT_COPY - nothing to promote." >&2
  exit 1
fi
if [ ! -f "$AGENT_COPY/hugo.toml" ]; then
  echo "ERROR: $AGENT_COPY has no hugo.toml - not a usable Hugo site." >&2
  exit 1
fi

# --- 1. Reconcile agent copy -> canonical (backup canonical first) ----------
if [ "$AGENT_WS" = "canonical" ]; then
  echo "Source is already canonical - skipping reconcile."
elif [ -d "$CANON" ]; then
  TS=$(date -u +%Y%m%dT%H%M%SZ)
  mkdir -p "$BACKUP_DIR"
  echo "Backing up existing canonical $VERSION ..."
  tar czf "$BACKUP_DIR/venus-version-$VERSION-pre-promote-$TS.tar.gz" \
      -C "$WS_ROOT/venus-versions" \
      --exclude='screenshots' --exclude='public' --exclude='node_modules' \
      "$VERSION" 2>/dev/null || true
fi
if [ "$AGENT_WS" != "canonical" ]; then
  mkdir -p "$CANON"
  rsync -a --delete \
    --exclude='.git' --exclude='screenshots' --exclude='.hugo_build.lock' \
    --exclude='node_modules' --exclude='build-local' --exclude='public' \
    "$AGENT_COPY"/ "$CANON"/
  echo "Reconciled $AGENT_COPY -> $CANON"
fi

# --- 2. Work out the baseURL for this target -------------------------------
case "$TARGET" in
  preview:*)
    SUBPATH="${TARGET#preview:}"
    BASE_URL="https://preview.reviews.ultramarine963.com/$SUBPATH/"
    BRANCH="preview"
    ;;
  dev)     BASE_URL="https://dev.reviews.ultramarine963.com/";     BRANCH="dev" ;;
  staging) BASE_URL="https://staging.reviews.ultramarine963.com/"; BRANCH="staging" ;;
  *)
    echo "ERROR: unrecognised deploy target '$TARGET'." >&2
    exit 1
    ;;
esac

# --- 3. Build ---------------------------------------------------------------
BUILD=$(mktemp -d)
echo "Building $VERSION with baseURL=$BASE_URL"
( cd "$CANON" && hugo --minify --baseURL "$BASE_URL" --destination "$BUILD" ) \
  | grep -E "Pages|Static|Total|ERROR" || true

# Gallery deploys serve a version from /<subpath>/, and the versions disagree about
# how they emit asset URLs: the older ones hardcode root-absolute "/css/..." strings
# (which resolve against the DOMAIN root and 404 under a subpath), while newer ones
# use Hugo's URL functions and already include the subpath. Confirmed both cases on
# 2026-07-28 - and either way the page still returns HTTP 200 while rendering
# completely unstyled, so a status check alone will not catch it.
#
# Rather than guess a build flag, normalise afterwards: prefix any root-absolute
# local URL that is not already under /<subpath>/. Idempotent, and correct for both
# template styles.
if [ -n "${SUBPATH:-}" ]; then
  # Two forms must be handled. `hugo --minify` strips quotes from attribute
  # values that do not need them, so a page emits BOTH:
  #     href="/css/x.css?v=1"   (quoted - the ? forces quoting)
  #     href=/methodology/      (unquoted)
  # Matching only the quoted form silently fixes every stylesheet while leaving
  # every navigation link pointing at the domain root - which then 404s under a
  # subpath. Confirmed the hard way on 2026-07-28: an asset-only check reported
  # "0 failures" while all in-page navigation was broken.
  # Skips "//" (protocol-relative) and anything already under /<subpath>/.
  find "$BUILD" -type f \( -name '*.html' -o -name '*.xml' -o -name '*.css' \) -print0 \
    | SUBPATH="$SUBPATH" xargs -0 -r perl -pi -e '
        s{(href|src)="/(?!/|\Q$ENV{SUBPATH}\E/)}{$1="/$ENV{SUBPATH}/}g;
        s{(href|src)=/(?!/|\Q$ENV{SUBPATH}\E/)}{$1=/$ENV{SUBPATH}/}g;
      '
  echo "Normalised root-absolute URLs (quoted + unquoted) under /$SUBPATH/"
fi
if [ ! -f "$BUILD/index.html" ]; then
  echo "ERROR: build produced no index.html - aborting, no branch touched." >&2
  rm -rf "$BUILD"; exit 1
fi

# Non-production environments must never be indexed - they are full duplicates
# of the live affiliate site and would compete with it for the same keywords.
cat > "$BUILD/robots.txt" <<'ROBOTS'
# Non-production environment. Never index.
User-agent: *
Disallow: /
ROBOTS
rm -f "$BUILD/sitemap.xml"

# --- 4. Publish to the deploy branch ---------------------------------------
cd "$REPO"
WT=$(mktemp -d)
if git show-ref --verify --quiet "refs/heads/$BRANCH"; then
  git worktree add "$WT" "$BRANCH" >/dev/null
else
  git worktree add -B "$BRANCH" "$WT" main >/dev/null
  git -C "$WT" rm -rf . >/dev/null 2>&1 || true
fi

if [ -n "${SUBPATH:-}" ]; then
  # Gallery deploy: replace only this version's subfolder, leave siblings alone.
  rm -rf "${WT:?}/${SUBPATH:?}"
  mkdir -p "$WT/$SUBPATH"
  cp -r "$BUILD"/. "$WT/$SUBPATH"/
  rm -f "$WT/$SUBPATH/robots.txt"   # one robots.txt at the gallery root is enough
else
  find "$WT" -mindepth 1 -maxdepth 1 -not -name '.git' -exec rm -rf {} +
  cp -r "$BUILD"/. "$WT"/
fi
rm -rf "$BUILD"

cd "$WT"
git add -A
if git diff --cached --quiet; then
  echo "No changes - '$BRANCH' already matches this build."
else
  git commit -q -m "deploy($BRANCH): $VERSION rebuild ($(date -u +%Y-%m-%dT%H:%M:%SZ))"
  echo "Committed $VERSION to '$BRANCH'."
fi
cd "$REPO"
git worktree remove "$WT" --force

echo
echo "Done. Push when ready:  git -C $REPO push origin $BRANCH"
