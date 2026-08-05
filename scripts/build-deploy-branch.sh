#!/usr/bin/env bash
# Build a Hugo site with the correct baseURL for a target environment and
# publish the flattened output to a deploy branch - the same pattern already
# proven for production (hostinger-deploy), extended to be reusable for any
# environment/project. Hostinger's native Git integration deploys whatever is
# at the ROOT of the connected branch (confirmed 2026-07-28: its "root
# directory" setting is the DESTINATION folder on the host, not a source path
# inside the branch) - so each deploy branch must hold ready-to-serve flat
# output, not a Hugo source tree.
#
# Usage: build-deploy-branch.sh <source-dir> <base-url> <deploy-branch>
# Example:
#   ./build-deploy-branch.sh /home/paul/.openclaw/workspaces/worker/venus-site \
#       https://dev.reviews.ultramarine963.com/ dev
set -euo pipefail

SOURCE_DIR="${1:?usage: build-deploy-branch.sh <source-dir> <base-url> <deploy-branch>}"
BASE_URL="${2:?missing base-url}"
DEPLOY_BRANCH="${3:?missing deploy-branch}"

if [ ! -d "$SOURCE_DIR/.git" ]; then
  echo "ERROR: $SOURCE_DIR is not a git repo (expected the Hugo source with a real git history)." >&2
  exit 1
fi

cd "$SOURCE_DIR"
SOURCE_BRANCH=$(git rev-parse --abbrev-ref HEAD)
echo "Building '$SOURCE_BRANCH' with baseURL=$BASE_URL -> deploy branch '$DEPLOY_BRANCH'"

if [ -n "$(git status --porcelain)" ]; then
  echo "NOTE: working tree has uncommitted changes - building from the working tree as-is (not just HEAD)."
fi

BUILD_DIR=$(mktemp -d)
hugo --minify --baseURL "$BASE_URL" --destination "$BUILD_DIR"

if [ ! -f "$BUILD_DIR/index.html" ]; then
  echo "ERROR: Hugo build did not produce an index.html - aborting, not touching any branch." >&2
  rm -rf "$BUILD_DIR"
  exit 1
fi

# Stage the flattened output onto the deploy branch without disturbing the
# current working tree/branch (uses a separate worktree, not `git checkout`).
WORKTREE_DIR=$(mktemp -d)
if git show-ref --verify --quiet "refs/heads/$DEPLOY_BRANCH"; then
  git worktree add "$WORKTREE_DIR" "$DEPLOY_BRANCH" >/dev/null
else
  git worktree add -B "$DEPLOY_BRANCH" "$WORKTREE_DIR" "$SOURCE_BRANCH" >/dev/null
  # Fresh branch: clear inherited source-tree content, we only want built output.
  git -C "$WORKTREE_DIR" rm -rf . >/dev/null 2>&1 || true
fi

find "$WORKTREE_DIR" -mindepth 1 -maxdepth 1 -not -name '.git' -exec rm -rf {} +
cp -r "$BUILD_DIR"/. "$WORKTREE_DIR"/
rm -rf "$BUILD_DIR"

cd "$WORKTREE_DIR"
git add -A
if git diff --cached --quiet; then
  echo "No changes to deploy (built output identical to current '$DEPLOY_BRANCH')."
else
  # Explicit author - see the same note in promote-version.sh. Without it this temporary
  # worktree inherits the repo's shared fallback identity.
  git -c user.name="Venus Deploy Automation" \
      -c user.email="deploy-automation@openclaw.local" \
      commit -q -m "deploy($DEPLOY_BRANCH): rebuild from $SOURCE_BRANCH ($(date -u +%Y-%m-%dT%H:%M:%SZ))"
  echo "Committed to '$DEPLOY_BRANCH'. Review with: git -C $SOURCE_DIR log -1 $DEPLOY_BRANCH"
  echo "Push when ready: git -C $SOURCE_DIR push origin $DEPLOY_BRANCH"
fi

cd "$SOURCE_DIR"
git worktree remove "$WORKTREE_DIR" --force
