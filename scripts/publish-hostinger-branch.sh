#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

DEPLOY_BRANCH="${DEPLOY_BRANCH:-hostinger-deploy}"
BUILD_DIR="public"
TMP_DIR="$(mktemp -d)"

cleanup() {
  rm -rf "$TMP_DIR"
}
trap cleanup EXIT

./build.sh

git worktree add "$TMP_DIR" "$DEPLOY_BRANCH" 2>/dev/null || git worktree add -B "$DEPLOY_BRANCH" "$TMP_DIR"

find "$TMP_DIR" -mindepth 1 -maxdepth 1 ! -name .git -exec rm -rf {} +
cp -a "$BUILD_DIR"/. "$TMP_DIR"/

(
  cd "$TMP_DIR"
  git add -A
  if git diff --cached --quiet; then
    echo "No deploy changes to commit."
  else
    git commit -m "Deploy site build"
  fi
)

echo "Deploy branch is ready: $DEPLOY_BRANCH"
echo "Push it with: git push origin $DEPLOY_BRANCH"
