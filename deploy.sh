#!/usr/bin/env bash
# Venus site deploy - the ONE command to publish changes.
#
# Hostinger auto-deploys the ROOT of the hostinger-deploy branch (configured
# in hPanel -> Git: repo notabot100101/venus-reviews, branch hostinger-deploy,
# root public_html). It does NOT serve the public/ subfolder. Editing source
# and rebuilding into public/ is NOT enough - the build output must be synced
# to the branch root or the live site silently keeps serving stale pages
# (this exact miss caused task 616's "pushed but site unchanged" failure,
# root-caused 2026-07-16).
#
# Usage: ./deploy.sh "commit message"

set -euo pipefail
cd "$(dirname "$0")"

MSG="${1:-site update}"

BRANCH="$(git branch --show-current)"
if [[ "$BRANCH" != "hostinger-deploy" ]]; then
    echo "ERROR: on branch '$BRANCH', deploys must happen from hostinger-deploy" >&2
    exit 1
fi

echo "==> Building site with Hugo..."
hugo --quiet

echo "==> Syncing build output (public/) to branch root (what Hostinger serves)..."
rsync -a public/ . --exclude='.git'

echo "==> Committing and pushing..."
git add -A
if git diff --cached --quiet; then
    echo "Nothing to deploy - build output identical to branch root."
    exit 0
fi
git commit -m "deploy: ${MSG}"
git push origin hostinger-deploy

echo "==> Pushed. Hostinger auto-deploys in ~5-10 minutes."
echo "==> Verify after propagation with:"
echo "    curl -s https://reviews.ultramarine963.com/ | head -20"
