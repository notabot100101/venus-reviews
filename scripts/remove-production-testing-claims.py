#!/usr/bin/env python3
"""Rewrite fabricated hands-on-testing claims on the LIVE Venus site to honest
curation language. Paul's decision 2026-07-29: "go with honest curation, no
testing claims."

Same category as the fabricated "Verified Tester" testimonials removed on
2026-07-29: concrete claims about work nobody did ("We tested the Womanizer 2
extensively over several weeks", "Hands-on product testing", "We test sound
levels in quiet environments"). No products were hands-on tested; the site has
no testing operation.

Surgical string replacement per file (the hostinger-deploy branch holds source
AND served output at its root — a rebuild would strip source off the branch and
ship ~20 unrelated uncommitted changes; see
directives/site-project-repo-policy.md and the testimonial-removal precedent).
"""
import re
import sys
from pathlib import Path

REPO = Path("/home/paul/.openclaw/workspaces/worker/venus-site")

# (pattern, replacement) — applied in order, case-sensitive, exact.
REPLACEMENTS = [
    # about page: expertise bullet
    ("Hands-on product testing, real-world usage context",
     "In-depth product research and real-world usage context"),
    # about page: numbered methodology item heading
    ("Hands-On Testing",
     "Product Research"),
    # about page: noise item
    ("We test sound levels in quiet environments for accurate comparisons",
     "We compare manufacturer-stated and user-reported sound levels for accurate comparisons"),
    # products list tagline (source layout + built pages)
    ("We test everything so you don't have to",
     "We research everything so you don't have to"),
    # stale womanizer-2 page: fabricated multi-week test narrative
    ("We tested the Womanizer 2 extensively over several weeks, evaluating its "
     "performance, comfort, suction power, app integration, and overall value proposition.",
     "We researched the Womanizer 2 in depth, comparing its documented performance, "
     "comfort, suction power, app integration, and overall value proposition."),
]

# Every file that carries at least one of the above (source + served output +
# the publicly reachable build-local artifacts). public/about has uncommitted
# drift, so it is restored from HEAD by the caller before this runs.
FILES = [
    "content/about.md",
    "about/index.html",
    "public/about/index.html",
    "products/index.html",
    "layouts/products/list.html",
    "products/womanizer-2/index.html",
    "build-local/about/index.html",
    "build-local/products/index.html",
]

CLAIM_RE = re.compile(
    r"hands.on (product )?testing|we test\b|we tested\b|our testing", re.I)
# Allowed survivors: product copy that isn't a testing claim.
ALLOWED_RE = re.compile(r"hands.on intimacy", re.I)


def main() -> int:
    changed, failures = [], []
    for rel in FILES:
        p = REPO / rel
        if not p.is_file():
            print(f"  skip {rel}: not present")
            continue
        text = p.read_text(encoding="utf8")
        orig = text
        for old, new in REPLACEMENTS:
            text = text.replace(old, new)
        if text != orig:
            p.write_text(text, encoding="utf8")
            changed.append(rel)
            print(f"  fixed {rel}")
        # verify nothing claim-like survives (minus allowed product copy)
        residue = [m.group(0) for m in CLAIM_RE.finditer(text)
                   if not ALLOWED_RE.search(text[max(0, m.start()-20):m.end()+20])]
        if residue:
            failures.append((rel, residue[:3]))
    print(f"\nfiles changed: {len(changed)}")
    if failures:
        print("RESIDUAL CLAIMS (fix manually):")
        for rel, r in failures:
            print(f"  {rel}: {r}")
        return 1
    print("verified: no testing-claim language remains in the target files")
    return 0


if __name__ == "__main__":
    sys.exit(main())
