#!/usr/bin/env python3
"""
Venus Affiliate Link Setup Script

Drop in tracking IDs and this updates affiliate-config.json + product front matter.
Usage: python3 affiliate-link-setup.py --lelo=ID --womanizer=ID ... [--env-file=.env]
"""
import json
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CONFIG_FILE = ROOT / "affiliate-config.json"

# Product -> which retailers sell it (program key)
PRODUCT_RETAILER_MAP = {
    "bvee-original-rabbit": ["shevibe"],
    "dame-eva-ii": ["shevibe"],
    "fun-factory-manta": ["shevibe"],
    "fun-factory-volta": ["shevibe"],
    "lelo-enigma": ["lelo", "shevibe"],
    "lelo-hugo": ["lelo", "shevibe"],
    "lelo-mona": ["lelo", "shevibe"],
    "lelo-sona-2": ["lelo", "shevibe"],
    "we-vibe-chorus": ["wevibe", "shevibe"],
    "we-vibe-sync": ["wevibe", "shevibe"],
    "womanizer-2-original": ["womanizer", "shevibe"],
}

# Retailer base URLs and product slugs
RETAILER_INFO = {
    "lelo": {"base": "https://www.lelo.com", "track": "?aff=", "display": "LELO"},
    "womanizer": {"base": "https://www.womanizer.com/us", "track": "?sid=", "display": "Womanizer"},
    "wevibe": {"base": "https://www.we-vibe.com/us", "track": "?sid=", "display": "We-Vibe"},
    "shevibe": {"base": "https://shevibe.com", "track": "?utm_source=venus&utm_medium=affiliate&utm_campaign=", "display": "SheVibe"},
    "adameve": {"base": "https://www.adameve.com", "track": "?aff=", "display": "Adam & Eve"},
    "bellesa": {"base": "https://www.bboutique.co", "track": "?utm_source=venus&utm_medium=affiliate&utm_campaign=", "display": "Bellesa"},
    "amazon": {"base": "https://www.amazon.com", "track": "?tag=", "display": "Amazon"},
}

# Product slugs on retailer websites
PRODUCT_SLUGS = {
    "bvee-original-rabbit": "b-vibe-original-rabbit",
    "dame-eva-ii": "dame-eva-ii",
    "fun-factory-manta": "fun-factory-manta",
    "fun-factory-volta": "fun-factory-volta",
    "lelo-enigma": "enigma",
    "lelo-hugo": "hugo",
    "lelo-mona": "mona-2",
    "lelo-sona-2": "sona-2",
    "we-vibe-chorus": "chorus",
    "we-vibe-sync": "sync",
    "womanizer-2-original": "womanizer-premium-2",
}

ALL_PROGRAMS = ["lelo", "womanizer", "wevibe", "shevibe", "adameve", "bellesa", "amazon"]


def parse_args():
    ids = {}
    env_file = None
    for arg in sys.argv[1:]:
        if arg.startswith("--env-file="):
            env_file = arg.split("=", 1)[1]
        elif arg.startswith("--"):
            parts = arg[2:].split("=", 1)
            if len(parts) == 2 and parts[0] in ALL_PROGRAMS:
                ids[parts[0]] = parts[1]
            elif arg in ("--help", "-h"):
                print(__doc__)
                sys.exit(0)
    if env_file:
        with open(env_file) as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if "=" not in line:
                    continue
                key, val = line.split("=", 1)
                key_clean = key.strip().lower().replace("venus_affiliate_", "")
                if key_clean in ALL_PROGRAMS:
                    ids[key_clean] = val.strip().strip('"').strip("'")
    return ids


def update_config(ids):
    """Update trackingPrefixes in affiliate-config.json."""
    with open(CONFIG_FILE) as f:
        config = json.load(f)

    updated = []
    for program, tid in ids.items():
        old = config.get("trackingPrefixes", {}).get(program, "")
        if old and old != f"AFFILIATE_ID_{program.upper()}":
            print(f"  Overwriting existing {program}: '{old}' -> '{tid}'")
        config["trackingPrefixes"][program] = tid
        updated.append(program)

    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=2)
        f.write("\n")

    print(f"  Updated trackingPrefixes for: {', '.join(updated)}")
    return updated


def update_product_front_matter(ids):
    """Update product index.md files with real affiliate URLs."""
    products_dir = ROOT / "content" / "products"
    updated_products = []
    skipped_programs = []

    for product_dir in sorted(products_dir.iterdir()):
        if not product_dir.is_dir():
            continue
        product_name = product_dir.name
        index_file = product_dir / "index.md"
        if not index_file.exists():
            continue

        retailers = PRODUCT_RETAILER_MAP.get(product_name, [])
        if not retailers:
            continue

        content = index_file.read_text()
        modified = False

        for program in retailers:
            if program not in ids:
                continue
            tid = ids[program]
            ri = RETAILER_INFO[program]
            base = ri["base"]
            track = ri["track"]
            display = ri["display"]
            slug = PRODUCT_SLUGS.get(product_name, product_name)
            url = f"{base}/{slug}{track}{tid}"

            # Find the offers section and update matching retailer entry
            # Use a simple regex/line approach
            lines = content.split("\n")
            in_offers = False
            in_target_retailer = False
            new_lines = []

            for line in lines:
                stripped = line.strip()

                # Detect offers block
                if stripped == "offers:":
                    in_offers = True
                    new_lines.append(line)
                    continue

                # Detect end of offers block
                if in_offers and stripped and not stripped.startswith("-") and not stripped.startswith(" ") and ":" in line and not line.startswith("  "):
                    in_offers = False

                # Detect retailer entry
                if in_offers and stripped.startswith("- retailer:"):
                    rname = stripped.split(":", 1)[1].strip().strip('"').strip("'").strip()
                    in_target_retailer = rname.lower() == display.lower()

                # Update url and available for the target retailer
                if in_target_retailer and in_offers:
                    if stripped.startswith("url:") and ('""' in stripped or "''" in stripped):
                        line = re.sub(r'url:\s*["\']{2}', f'url: "{url}"', line)
                        modified = True
                    if stripped.startswith("available:") and "false" in stripped:
                        line = line.replace("available: false", "available: true")
                        modified = True

                new_lines.append(line)

            if modified:
                index_file.write_text("\n".join(new_lines))
                updated_products.append(product_name)
                print(f"    -> {product_name}: set {display} URL")

    return updated_products


def create_env_template():
    """Create .env.example if it doesn't exist."""
    env_path = ROOT / ".env.affiliate.example"
    if not env_path.exists():
        content = """# Venus Affiliate Tracking IDs
# Copy this file to .env.affiliate and fill in real IDs
# Then run: ./affiliate-link-setup.sh --env-file=.env.affiliate
#
# Get these IDs from your affiliate dashboard after approval.

VENUS_AFFILIATE_LELO=""
VENUS_AFFILIATE_WOMANIZER=""
VENUS_AFFILIATE_WEVIBE=""
VENUS_AFFILIATE_SHEVIBE=""
VENUS_AFFILIATE_ADAMEVE=""
VENUS_AFFILIATE_BELLESA=""
VENUS_AFFILIATE_AMAZON=""
"""
        env_path.write_text(content)
        print(f"\n  Created {env_path} - fill with real IDs and use --env-file=.env.affiliate")
        print("  (Add .env.affiliate to .gitignore to keep IDs secret)")


def main():
    ids = parse_args()
    if not ids:
        print("ERROR: No tracking IDs provided.")
        print("Usage: python3 affiliate-link-setup.py --lelo=ID --womanizer=ID ...")
        print("  Or:  python3 affiliate-link-setup.py --env-file=.env.affiliate")
        sys.exit(1)

    print("=" * 60)
    print("Venus Affiliate Link Setup")
    print("=" * 60)
    print(f"\nPrograms to configure: {', '.join(sorted(ids.keys()))}")

    # Update config
    print("\n--- Step 1: Updating affiliate-config.json ---")
    update_config(ids)

    # Update product pages
    print("\n--- Step 2: Updating product page offers ---")
    updated = update_product_front_matter(ids)

    # Create env template
    create_env_template()

    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"\nTracking IDs configured: {len(ids)}")
    print(f"Product pages updated: {len(updated)}")

    if updated:
        print("\nUpdated products:")
        for p in updated:
            print(f"  - content/products/{p}/index.md")

    print("\n--- Next Steps ---")
    print("1. Verify:  git diff")
    print("2. Deploy:  ./deploy.sh \"activate affiliate links\"")
    print("3. Check:   curl -s https://reviews.ultramarine963.com/products/lelo-sona-2/")
    print("=" * 60)


if __name__ == "__main__":
    main()