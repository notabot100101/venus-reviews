#!/usr/bin/env bash
# Venus visual monitor.
# Detects the "HTTP 200 but visually unstyled" failure mode by opening the live
# site in Chromium, checking computed styles, and saving screenshots.

set -euo pipefail

SITE_BASE="https://reviews.ultramarine963.com"
SITE_DIR="/home/paul/.openclaw/workspaces/worker/venus-site"
SCREENSHOT_DIR="$SITE_DIR/screenshots/visual-monitor"
STATE_FILE="$SITE_DIR/screenshots/visual-monitor-state.json"
LOG_FILE="$SITE_DIR/visual-monitor-cronjob.log"
OPENCLAW_BIN="/home/paul/.npm-global/bin/openclaw"
DISCORD_CHANNEL="1521616964039086378"
CHROME_PATH="${CHROME_PATH:-/home/paul/.agent-browser/browsers/chrome-149.0.7827.54/chrome}"

mkdir -p "$SCREENSHOT_DIR"

timestamp() {
  TZ=Europe/Berlin date '+%Y-%m-%d %H:%M:%S Berlin'
}

log() {
  printf '[%s] %s\n' "$(timestamp)" "$*" >> "$LOG_FILE"
}

send_alert() {
  local message="$1"
  if [[ -x "$OPENCLAW_BIN" ]]; then
    "$OPENCLAW_BIN" message send --channel discord --target "channel:$DISCORD_CHANNEL" --message "$message" >> "$LOG_FILE" 2>&1 || true
  else
    log "WARN: openclaw CLI unavailable, could not send alert"
  fi
}

result_json="$(
  NODE_PATH=/home/paul/.openclaw/node_modules SITE_BASE="$SITE_BASE" SCREENSHOT_DIR="$SCREENSHOT_DIR" CHROME_PATH="$CHROME_PATH" node <<'NODE'
const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright');

const siteBase = process.env.SITE_BASE;
const screenshotDir = process.env.SCREENSHOT_DIR;
const chromePath = process.env.CHROME_PATH;

const checks = [
  {
    label: 'homepage',
    url: `${siteBase}/`,
    requiredText: ['Venus Reviews', 'Featured Reviews', 'Reader Confidence Notes'],
  },
  {
    label: 'products',
    url: `${siteBase}/products/`,
    requiredText: ['Product Reviews'],
  },
  {
    label: 'about',
    url: `${siteBase}/about/`,
    requiredText: ['About', 'Venus Reviews'],
  },
];

function isTransparent(color) {
  return color === 'rgba(0, 0, 0, 0)' || color === 'transparent';
}

function looksLikeBrowserDefault(fontFamily) {
  return /Times New Roman|serif/i.test(fontFamily || '');
}

(async () => {
  const browser = await chromium.launch({ executablePath: chromePath, headless: true });
  const failures = [];
  const pages = [];

  for (const check of checks) {
    const page = await browser.newPage({ viewport: { width: 1366, height: 900 } });
    const response = await page.goto(check.url, { waitUntil: 'networkidle', timeout: 45000 });
    const screenshot = path.join(screenshotDir, `${check.label}-${new Date().toISOString().replace(/[:.]/g, '-')}.png`);
    await page.screenshot({ path: screenshot, fullPage: true });

    const data = await page.evaluate((requiredText) => {
      const bodyStyle = getComputedStyle(document.body);
      const card = document.querySelector('.product-card');
      const cardStyle = card ? getComputedStyle(card) : null;
      const nav = document.querySelector('.nav');
      const hero = document.querySelector('.hero');
      const text = document.body.innerText || '';
      return {
        title: document.title,
        hasHtmlShell: document.documentElement.tagName.toLowerCase() === 'html' && !!document.head && !!document.body,
        stylesheetLinks: document.querySelectorAll('link[rel="stylesheet"]').length,
        loadedStyleSheets: document.styleSheets.length,
        bodyFont: bodyStyle.fontFamily,
        bodyBackground: bodyStyle.backgroundColor,
        navCount: nav ? 1 : 0,
        heroCount: hero ? 1 : 0,
        productCardCount: document.querySelectorAll('.product-card').length,
        reviewsHeaderCount: document.querySelectorAll('.reviews-header').length,
        oldSectionActionsCount: document.querySelectorAll('.section-actions').length,
        cardBackground: cardStyle ? cardStyle.backgroundColor : '',
        cardRadius: cardStyle ? cardStyle.borderRadius : '',
        cardPadding: cardStyle ? cardStyle.padding : '',
        requiredTextPresent: requiredText.map((needle) => ({ needle, present: text.includes(needle) })),
      };
    }, check.requiredText);

    const pageFailures = [];
    if (!response || response.status() >= 400) pageFailures.push(`HTTP status ${response ? response.status() : 'missing'}`);
    if (!data.hasHtmlShell) pageFailures.push('missing HTML document shell');
    if (data.stylesheetLinks < 4) pageFailures.push(`too few stylesheet links (${data.stylesheetLinks})`);
    if (data.loadedStyleSheets < 4) pageFailures.push(`too few loaded stylesheets (${data.loadedStyleSheets})`);
    if (looksLikeBrowserDefault(data.bodyFont)) pageFailures.push(`browser-default font detected (${data.bodyFont})`);
    if (isTransparent(data.bodyBackground)) pageFailures.push(`transparent/default body background (${data.bodyBackground})`);
    if (data.navCount < 1) pageFailures.push('missing nav');
    if (check.label === 'homepage' && data.heroCount < 1) pageFailures.push('missing homepage hero');
    if (check.label === 'homepage' && data.productCardCount < 6) pageFailures.push(`too few homepage product cards (${data.productCardCount})`);
    if (check.label === 'homepage' && data.reviewsHeaderCount < 1) pageFailures.push('missing reviews header');
    if (data.oldSectionActionsCount > 0) pageFailures.push('old section-actions CTA is back');
    if (check.label === 'homepage' && (!data.cardPadding || data.cardPadding === '0px')) pageFailures.push('product cards have no CSS padding');
    for (const item of data.requiredTextPresent) {
      if (!item.present) pageFailures.push(`missing text: ${item.needle}`);
    }

    pages.push({ label: check.label, url: check.url, screenshot, data, failures: pageFailures });
    for (const failure of pageFailures) failures.push(`${check.label}: ${failure}`);
    await page.close();
  }

  await browser.close();
  console.log(JSON.stringify({ ok: failures.length === 0, failures, pages }, null, 2));
})().catch((error) => {
  console.log(JSON.stringify({ ok: false, failures: [`monitor crashed: ${error.message}`], pages: [] }, null, 2));
  process.exitCode = 0;
});
NODE
)"

printf '%s\n' "$result_json" > "$SCREENSHOT_DIR/latest-result.json"

ok="$(printf '%s\n' "$result_json" | NODE_PATH=/home/paul/.openclaw/node_modules node -e 'let s="";process.stdin.on("data",d=>s+=d);process.stdin.on("end",()=>console.log(JSON.parse(s).ok ? "true" : "false"))')"
summary="$(printf '%s\n' "$result_json" | NODE_PATH=/home/paul/.openclaw/node_modules node -e 'let s="";process.stdin.on("data",d=>s+=d);process.stdin.on("end",()=>{const r=JSON.parse(s); console.log(r.failures.join("\\n"));})')"

previous="unknown"
if [[ -f "$STATE_FILE" ]]; then
  previous="$(NODE_PATH=/home/paul/.openclaw/node_modules node -e 'const fs=require("fs"); try { console.log(JSON.parse(fs.readFileSync(process.argv[1],"utf8")).ok ? "true" : "false") } catch { console.log("unknown") }' "$STATE_FILE")"
fi

printf '{"ok":%s,"checked_at":"%s"}\n' "$ok" "$(timestamp)" > "$STATE_FILE"

if [[ "$ok" == "true" ]]; then
  log "OK: visual checks passed"
  if [[ "$previous" == "false" ]]; then
    send_alert "**Venus visual monitor recovered** ($(timestamp))"$'\n\n'"Homepage, products, and about pages now pass style, DOM, and screenshot checks."
  fi
else
  log "FAIL: $summary"
  if [[ "$previous" != "false" ]]; then
    send_alert "**Venus visual regression detected** ($(timestamp))"$'\n\n'"$summary"$'\n\n'"Latest screenshots and JSON result are in: $SCREENSHOT_DIR"
  fi
  exit 1
fi
