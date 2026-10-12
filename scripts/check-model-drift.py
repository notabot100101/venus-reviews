#!/usr/bin/env python3
"""Catch REVIEW-vs-REALITY drift: a review that names one model while its manufacturer
offer row points at another, or at a page that has died or become a search result.

WHY THIS EXISTS (2026-10-12). Four cases accumulated before anyone noticed, all the same
shape and all found by hand, one at a time:
  - lelo-mona          titled "LELO Mona", offer URL lands on MONA 2
  - womanizer-liberty  /de/liberty redirects to /de/liberty-2 (Liberty 2 is the current model)
  - we-vibe-sync       DELISTED: /de/sync and /eu/sync both land on a catalog-search page
  - satisfyer-pro-2    body describes Generation 3, offer URL points at Generation 2
                       (and Satisfyer sells FOUR live Pro 2 generations at 48.97-89.95)
A written rule was not enough: the model a page sells changes without anything in our repo
changing, so only a check that actually FETCHES can notice. Read-only - it never edits.

Usage:  scripts/check-model-drift.py [--no-net] [--delay 1.0] [--only <slug>]
Exit:   0 clean, 1 findings. Safe to cron.
"""
import re, sys, json, glob, time, html, urllib.request, urllib.error, argparse

UA = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
      "Chrome/120 Safari/537.36")

# Prose that is true on the day it is written and rots silently afterwards.
TIMEBOMB = re.compile(
    r"the current version is|currently the (?:newest|latest|only)|"
    r"the latest (?:\w+ )?(?:model|version|generation)|the newest \w+|as of (?:now|today)", re.I)

# Words that carry no model identity, so they must not create a false "match".
NOISE = set("""the a an and or for with of in on to from by at is are was
coloring book kids review vibrator vibe massager stimulator toy toys plus set
satisfyer lelo we-vibe wevibe womanizer dame fun factory lovehoney b-vibe bvibe
black red violet rosa blau schwarz rot amethyst purple pink blue""".split())


QUALIFIER = re.compile(r"^(?:\d+\+?|ii|iii|iv|vi|generation|gen|mk\d*)$")

def qualifiers(words):
    return {w for w in words if QUALIFIER.match(w)}

UMLAUT = {"\u00e4": "ae", "\u00f6": "oe", "\u00fc": "ue", "\u00df": "ss",
          "\u00e9": "e", "\u00e8": "e", "\u00e1": "a", "\u00f3": "o"}

def norm(s):
    s = html.unescape(s or "").lower()
    s = re.sub(r"[\u2122\u00ae\u00a9]", " ", s)
    for k, v in UMLAUT.items():          # transliterate, never delete
        s = s.replace(k, v)
    s = re.sub(r"[^a-z0-9+]+", " ", s)
    return [w for w in s.split() if w and w not in NOISE]


# The list price is often ONLY in the rendered price block, as a struck-through sibling
# of the selling price. A page's JSON-LD / structured price is the SELLING price.
# Confirmed on three unrelated brands in one evening: lelo-mona (JSON-LD 108.42 was a
# 22% promo of 139.00), we-vibe-chorus (JSON-LD 159 against "Regulaerer Preis 209"),
# satisfyer-pro-2-generation-3 (JSON-LD 55.97 against a struck 79,95, 30% off). Pricing a
# review from JSON-LD alone silently publishes a promotion as the list price.
PRICE_BLOCK = re.compile(r'class="(?:price--content|product--price|product-info-price)[^"]*".{0,900}', re.S)

def price_block_figures(body):
    """(figures found in the product's own price block, struck-price marker present)."""
    m = PRICE_BLOCK.search(body)
    if not m:
        return [], False
    blk = m.group(0)
    figs = []
    for raw in re.findall(r'\d{1,4}[.,]\d{2}', blk):
        try: figs.append(float(raw.replace(",", ".")))
        except ValueError: pass
    struck = bool(re.search(r'line-through|old-price|special-price|price--discount-percentage|'
                            r'Regul\u00e4rer Preis|UVP|statt\b', blk, re.I))
    return sorted(set(figs)), struck

def fetch(url, timeout=40):
    req = urllib.request.Request(url, headers={"User-Agent": UA,
                                               "Accept-Language": "de,en;q=0.8"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.status, r.geturl(), r.read(600_000).decode("utf-8", "replace")

def landed_name(body):
    """The product name the PAGE claims, from the most authoritative source available."""
    for blob in re.findall(r'<script[^>]*application/ld\+json[^>]*>(.*?)</script>', body, re.S):
        try:
            data = json.loads(blob.strip())
        except Exception:
            continue
        for o in (data if isinstance(data, list) else [data]):
            if isinstance(o, dict) and o.get("@type") == "Product" and o.get("name"):
                return o["name"], "json-ld"
    m = re.search(r'dtgsGtmArticleName"\s+value="([^"]+)"', body)      # Satisfyer/Shopware
    if m: return m.group(1), "gtm"
    m = re.search(r'<meta[^>]+property="og:title"[^>]+content="([^"]+)"', body)
    if m: return m.group(1), "og:title"
    m = re.search(r'<title>([^<]+)', body)
    if m: return m.group(1), "title"
    return "", "none"

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--no-net", action="store_true", help="prose checks only")
    ap.add_argument("--delay", type=float, default=1.0)
    ap.add_argument("--only")
    a = ap.parse_args()

    findings = []
    for path in sorted(glob.glob("content/products/*/index.md")):
        slug = path.split("/")[2]
        if a.only and a.only != slug:
            continue
        src = open(path, encoding="utf-8").read()
        tm = re.search(r'^title:\s*"([^"]+)"', src, re.M)
        title = tm.group(1) if tm else slug
        pm = re.search(r'^price:\s*"?([\d.]+)"?', src, re.M)
        review_price = float(pm.group(1)) if pm else None

        for m in TIMEBOMB.finditer(src):
            line = src[:m.start()].count("\n") + 1
            findings.append((slug, "TIMEBOMB_PROSE", f'line {line}: "…{src[m.start():m.start()+60].strip()}…"',
                             "States what is current TODAY. Name the generation reviewed + the "
                             "verification date instead - that stays true."))

        um = re.search(r'retailer:\s*"[^"]*\(manufacturer\)"\s*\n\s*url:\s*"([^"]*)"', src)
        url = um.group(1) if um else ""
        # the review's own claim about stock on the manufacturer row
        am = re.search(r'retailer:\s*"[^"]*\(manufacturer\)".*?available:\s*(true|false)', src, re.S)
        claims_available = (am.group(1) == "true") if am else None
        if not url:
            findings.append((slug, "NO_MANUFACTURER_URL", "-", "No manufacturer offer row to verify against."))
            continue
        if a.no_net:
            continue

        try:
            status, final, body = fetch(url)
        except urllib.error.HTTPError as e:
            findings.append((slug, "DEAD_URL", f"{url} -> HTTP {e.code}",
                             "Offer row points at a page that errors. Retire, re-point, or mark unavailable."))
            time.sleep(a.delay); continue
        except Exception as e:
            findings.append((slug, "FETCH_FAILED", f"{url} -> {type(e).__name__}",
                             "Could not verify - NOT evidence the link is fine."))
            time.sleep(a.delay); continue

        if re.search(r"catalogsearch|/search|suchergebnis|search\?q=", final, re.I):
            findings.append((slug, "LANDS_ON_SEARCH", f"{url} -> {final}",
                             "DELISTED: the product page is gone and the slug now resolves to a "
                             "search listing. Same shape as we-vibe-sync."))
            time.sleep(a.delay); continue

        # STOCK: a review that says available: true while the manufacturer has stopped
        # stocking it sends buyers to a dead end. fun-factory-manta, lelo-hugo and
        # satisfyer-pro-3-plus were all found by hand; this catches the next one.
        avail = None
        m = re.search(r'schema\.org/(InStock|OutOfStock|LimitedAvailability|SoldOut|Discontinued|PreOrder|BackOrder)', body)
        if m:
            avail = m.group(1)
        elif re.search(r'nicht zur Verf\u00fcgung|ausverkauft|nicht verf\u00fcgbar|out of stock|sold out', body, re.I):
            avail = "OutOfStock(text)"
        if avail and avail != "InStock" and claims_available is True:
            findings.append((slug, "STOCK_DRIFT", f'review says available: true, page says {avail}',
                             "Manufacturer is no longer stocking it. Set available: false with a "
                             "one-line note; JSON-LD follows automatically."))
        elif avail == "InStock" and claims_available is False:
            findings.append((slug, "STOCK_DRIFT", 'review says available: false, page says InStock',
                             "Back in stock - the offer row understates it."))

        figs, struck = price_block_figures(body)
        if review_price is not None and len(figs) >= 2 and struck:
            hi, lo = max(figs), min(figs)
            if abs(review_price - lo) < 0.02:
                findings.append((slug, "PRICE_IS_PROMO_NOT_LIST",
                                 f"review price {review_price} equals the SELLING price; the block "
                                 f"also shows a struck {hi} ({round((1-lo/hi)*100)}% off)",
                                 "House convention is the manufacturer LIST price with the discount "
                                 "noted in prose. Use the struck figure."))
            elif abs(review_price - hi) > 0.02:
                findings.append((slug, "PRICE_MATCHES_NEITHER",
                                 f"review price {review_price}; page block shows {lo} selling / {hi} list",
                                 "Neither figure matches - re-verify before changing anything."))

        name, src_kind = landed_name(body)
        tw, nw = set(norm(title)), set(norm(name))
        if tw and nw and not (tw & nw):
            findings.append((slug, "NAME_MISMATCH", f'review "{title}" vs page "{name}" [{src_kind}]',
                             "The page sells a different product than the review names."))
        elif qualifiers(tw - nw):
            missing = " ".join(sorted(qualifiers(tw - nw)))
            findings.append((slug, "MODEL_QUALIFIER_DRIFT",
                             f'review "{title}" vs page "{name}" (review-only: {missing}) [{src_kind}]',
                             "Partial match - usually a generation/version qualifier differing. "
                             "Check which model is actually reviewed."))
        elif qualifiers(nw - tw):
            extra = " ".join(sorted(qualifiers(nw - tw)))
            findings.append((slug, "PAGE_IS_NEWER_MODEL",
                             f'review "{title}" vs page "{name}" (page-only qualifier: {extra}) [{src_kind}]',
                             "The page names a model qualifier the review does not - the "
                             "manufacturer has probably moved on. Same shape as lelo-mona/MONA 2."))
        # Only a SLUG change matters. lelo.com/hugo -> lelo.com/de/hugo is a locale
        # prefix every LELO link gets (sourcing map), and reporting it on all 19 of them
        # drowns the real finding. A different last path segment means a different product.
        def slug_of(u):
            return [x for x in u.split("?")[0].rstrip("/").split("/") if x][-1:] or [""]
        if slug_of(final) != slug_of(url):
            findings.append((slug, "REDIRECTED_TO_OTHER_SLUG", f"{url} -> {final}",
                             "The recorded url is not where buyers land, and the final segment "
                             "differs - so it may be a different product. Record the LANDED url."))
        time.sleep(a.delay)

    if not findings:
        print("clean: no model drift found"); return 0
    order = {"LANDS_ON_SEARCH":0,"DEAD_URL":1,"NAME_MISMATCH":2,"MODEL_QUALIFIER_DRIFT":3,
             "PAGE_IS_NEWER_MODEL":4,"PRICE_IS_PROMO_NOT_LIST":5,"PRICE_MATCHES_NEITHER":6,"STOCK_DRIFT":7,"TIMEBOMB_PROSE":6,"REDIRECTED_TO_OTHER_SLUG":7,"FETCH_FAILED":7,
             "NO_MANUFACTURER_URL":8}
    findings.sort(key=lambda f: (order.get(f[1], 9), f[0]))
    print(f"{len(findings)} finding(s):\n")
    for slug, kind, detail, why in findings:
        print(f"  [{kind}] {slug}\n      {detail}\n      -> {why}\n")
    return 1

if __name__ == "__main__":
    sys.exit(main())
