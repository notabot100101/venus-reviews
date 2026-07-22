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

# Credential preflight - fail EARLY with an actionable message instead of committing
# and then dying on the cryptic "could not read Username for github.com" (which is what
# repeatedly stranded agents mid-deploy). See ~/.openclaw/SECRETS-REGISTRY.md.
if [[ ! -s "$HOME/.git-credentials" ]] && [[ -z "${GITHUB_TOKEN:-}" ]] && [[ -z "${GH_TOKEN:-}" ]]; then
    echo "ERROR: no GitHub credential available - the push would fail." >&2
    echo "  Fix (store the PAT once, then re-run this script):" >&2
    echo '    echo "https://notabot100101:<GITHUB_PAT>@github.com" > ~/.git-credentials && chmod 600 ~/.git-credentials' >&2
    echo "  Full details + token scope: ~/.openclaw/SECRETS-REGISTRY.md" >&2
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

# Reconcile with origin BEFORE pushing, so a concurrent commit from another agent (e.g.
# Sophia pushed a CSS change while this copy was being edited) is integrated instead of
# clobbered. Confirmed real 2026-07-21: local and origin diverged at the last deploy and a
# naive push would have reverted Sophia's live "Center homepage reviews CTA" commit.
echo "==> Reconciling with origin (fetch + rebase)..."
git fetch origin hostinger-deploy
git rebase origin/hostinger-deploy || {
    echo "ERROR: rebase hit a conflict - resolve manually, do NOT force-push (that loses others' commits)." >&2
    git rebase --abort
    exit 1
}
# Rebuild after rebase so public/ reflects any source changes pulled in from origin.
hugo --quiet
rsync -a public/ . --exclude='.git'
git add -A
git diff --cached --quiet || git commit --amend --no-edit

git push origin hostinger-deploy

echo "==> Pushed. Hostinger auto-deploys in ~5-10 minutes."
echo "==> Verify after propagation with:"
echo "    curl -s https://reviews.ultramarine963.com/ | head -20"
