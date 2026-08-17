#!/usr/bin/env bash
# =============================================================================
# Venus Affiliate Link Setup Script
# =============================================================================
# Drop in your approved affiliate tracking IDs and this script updates
# everything needed: affiliate-config.json + product front matter offers.
#
# Usage:
#   Single program:
#     ./affiliate-link-setup.sh --lelo=YOUR_LELO_ID
#
#   Multiple programs:
#     ./affiliate-link-setup.sh \
#       --lelo=YOUR_LELO_ID \
#       --womanizer=YOUR_IMPACT_ID \
#       --wevibe=YOUR_IMPACT_ID \
#       --shevibe=YOUR_IMPACT_ID \
#       --adameve=YOUR_PEPPERJAM_ID
#
#   From env file (keep OUT of git):
#     ./affiliate-link-setup.sh --env-file=.env.affiliate
#
#   After running, verify with `git diff` then deploy:
#     ./deploy.sh "activate LELO affiliate links"
# =============================================================================
set -euo pipefail
cd "$(dirname "$0")"
exec python3 "$(dirname "$0")/affiliate-link-setup.py" "$@"