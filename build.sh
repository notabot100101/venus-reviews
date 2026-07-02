#!/bin/bash
# Venus Site Build Script

set -e

cd "$(dirname "$0")"

# Build command. Use the checked-in local binary when available.
HUGO_BIN="${HUGO_BIN:-hugo}"
if [ -x ".bin/hugo" ]; then
  HUGO_BIN=".bin/hugo"
fi

"$HUGO_BIN" --destination=public --minify

# Optional: Add analytics
if [ ! -z "$GA_ID" ]; then
  cat > public/analytics.js << EOF
(function() {
  var analytics = document.createElement('script');
  analytics.async = true;
  analytics.src = 'https://www.googletagmanager.com/gtag/js?id=${GA_ID}';
  var s = document.getElementsByTagName('script')[0];
  s.parentNode.insertBefore(analytics, s);
  window.dataLayer = window.dataLayer || [];
  window.gtag = function() { window.dataLayer.push(arguments); };
  gtag('js', new Date());
  gtag('config', '${GA_ID}');
})();
EOF
fi

echo "Build complete! Files in: public/"
ls -la public/
