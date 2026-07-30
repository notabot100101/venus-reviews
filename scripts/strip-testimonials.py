#!/usr/bin/env python3
"""Remove the fabricated-testimonial section from a Hugo layout.

The section presents four invented people ("Sarah M.", "James K.", "Emily R.",
"Marcus T.") with star ratings, avatars and first-person purchase quotes, under
a header explicitly claiming they are "from real buyers". The site has no
comment system, no accounts, and no purchase path, so no real testimonial could
have been collected. Fabricated consumer testimonials on a commercial site are
an FTC problem (16 CFR Part 465), so they get removed rather than reworded.

Removes the whole <section ...testimonials-section...> ... </section> block by
matching nested section tags, so no orphan markup is left behind.
"""
import re
import sys
from pathlib import Path

FABRICATED = ["Sarah M.", "James K.", "Emily R.", "Marcus T."]


def strip_section(html: str) -> tuple[str, bool]:
    start = None
    for m in re.finditer(r'<section\b[^>]*>', html):
        if 'testimonials-section' in m.group(0):
            start = m.start()
            break
    if start is None:
        return html, False

    # Walk forward balancing <section>/</section> so nesting can't truncate us.
    depth = 0
    pos = start
    for m in re.finditer(r'</?section\b[^>]*>', html[start:]):
        tag = m.group(0)
        pos = start + m.end()
        depth += -1 if tag.startswith('</') else 1
        if depth == 0:
            break
    else:
        return html, False

    return html[:start] + html[pos:], True


def main() -> int:
    changed = 0
    for path_str in sys.argv[1:]:
        path = Path(path_str)
        if not path.is_file():
            continue
        original = path.read_text(encoding='utf8')
        if not any(name in original for name in FABRICATED):
            continue

        path.with_suffix(path.suffix + '.pre-testimonial-strip').write_text(
            original, encoding='utf8')
        new, ok = strip_section(original)
        if not ok:
            print(f"  !! {path}: names present but no testimonials-section found "
                  f"- left untouched, needs manual review")
            continue

        leftover = [n for n in FABRICATED if n in new]
        if leftover:
            print(f"  !! {path}: names still present after strip {leftover} "
                  f"- left untouched")
            continue

        path.write_text(new, encoding='utf8')
        print(f"  stripped {path}  ({len(original) - len(new)} bytes removed)")
        changed += 1
    print(f"files changed: {changed}")
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
