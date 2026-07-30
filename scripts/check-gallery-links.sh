#!/usr/bin/env bash
# Verify a locally-served preview gallery: every local link and asset on a
# sample of pages per version must return 200.
#
# Exists because an asset-only check gives false confidence. `hugo --minify`
# strips quotes from attributes that do not need them, so stylesheets (quoted,
# because ?v= forces quoting) and navigation links (unquoted) are affected
# differently by URL rewriting. On 2026-07-28 a CSS/JS-only check reported
# "0 failures" while every in-page nav link was still pointing at the domain
# root and would have 404'd on the real subdomain.
#
# Usage: check-gallery-links.sh <base-url> [version ...]
#   e.g. check-gallery-links.sh http://localhost:8899
set -uo pipefail

BASE="${1:?usage: check-gallery-links.sh <base-url> [version ...]}"
shift || true
ROOT_DIR="${GALLERY_DIR:-}"

if [ "$#" -gt 0 ]; then
  VERSIONS=("$@")
elif [ -n "$ROOT_DIR" ] && [ -d "$ROOT_DIR" ]; then
  mapfile -t VERSIONS < <(find "$ROOT_DIR" -mindepth 1 -maxdepth 1 -type d -printf '%f\n' | sort)
else
  echo "ERROR: pass versions explicitly or set GALLERY_DIR." >&2
  exit 2
fi

# Fail loudly if the base URL is unreachable. Without this the loop below simply
# finds no links, reports "checked 0 URLs, 0 broken" and exits 0 - a dead server
# looks identical to a clean run. Hit this for real on 2026-07-29 when the local
# preview server had died between runs.
PROBE=$(curl -s -o /dev/null -w '%{http_code}' -m 8 "$BASE/" || true)
if [ "$PROBE" != "200" ]; then
  echo "ERROR: base URL $BASE/ returned '$PROBE' - server unreachable, nothing was checked." >&2
  exit 2
fi

TOTAL=0; FAIL=0
declare -A SEEN

check(){ # url  context
  local url="$1" ctx="$2"
  [ -n "${SEEN[$url]:-}" ] && return
  SEEN[$url]=1
  local code
  code=$(curl -s -o /dev/null -w '%{http_code}' -m 8 "$url")
  TOTAL=$((TOTAL+1))
  if [ "$code" != "200" ]; then
    FAIL=$((FAIL+1))
    printf '  BROKEN %s  %s\n     (on %s)\n' "$code" "$url" "$ctx"
  fi
}

for v in "${VERSIONS[@]}"; do
  echo "=== $v ==="
  # Sample pages: version root, a nested product page, and any trust pages.
  PAGES=("/$v/" "/$v/products/" "/$v/products/lelo-mona/" "/$v/how-we-test/" "/$v/methodology/")
  for page in "${PAGES[@]}"; do
    body=$(curl -s -m 8 "$BASE$page")
    [ -z "$body" ] && continue
    # Strip inline <script>/<style> bodies first: minified JS contains things
    # like `img.src=x` and `e,thumbnails.forEach((e,t)=`, which the extractor
    # below would otherwise report as broken URLs. A checker that emits false
    # positives gets ignored, which is worse than not having one.
    body=$(printf '%s' "$body" | perl -0777 -pe '
      s{<script\b.*?</script>}{}gis;
      s{<style\b.*?</style>}{}gis;')
    # Extract href/src values in BOTH quoted and unquoted minified forms.
    urls=$(printf '%s' "$body" \
      | grep -oE '(href|src)=("[^"]*"|[^ >]+)' \
      | sed -E 's/^(href|src)=//; s/^"//; s/"$//')
    for u in $urls; do
      case "$u" in
        ""|"#"*|mailto:*|tel:*|javascript:*|data:*) continue ;;
        http*|//*) continue ;;                       # external - not our problem
        /*)  check "$BASE$u" "$page" ;;
        *)   check "$BASE$page$u" "$page" ;;
      esac
    done
  done
done

echo
echo "checked $TOTAL unique local URLs, $FAIL broken"
# A run that found nothing to check is a broken run, not a passing one.
if [ "$TOTAL" -eq 0 ]; then
  echo "ERROR: no URLs were checked - wrong version names, or pages served empty." >&2
  exit 2
fi
[ "$FAIL" -eq 0 ] || exit 1
