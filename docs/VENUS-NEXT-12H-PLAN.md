# Venus Next 12 Hours Plan

Updated: 2026-07-27

## Current State

- Active repo: `https://github.com/notabot100101/venus-reviews.git`
- Active local checkout: `/home/paul/.openclaw/workspaces/worker/venus-site`
- Active branch: `hostinger-deploy`
- Local deployment workflow commit waiting to push: `d320b48`
- Push blocker: the stored GitHub token can access the repo, but lacks GitHub `workflow` scope for files under `.github/workflows/`.

## What To Do Next

1. Update GitHub credentials.
   - Add `workflow` scope to the GitHub PAT used by local git credentials.
   - Then push `hostinger-deploy`, including commit `d320b48`.

2. Push the prepared website fixes.
   - The rating/star display fix should be pushed after credential scope is corrected.
   - Verify production receives the update through the existing Hostinger deployment path.

3. Create environment branches.
   - Create `dev` from `hostinger-deploy`.
   - Create `staging` from `hostinger-deploy`.
   - Push both branches to GitHub.

4. Configure GitHub Actions secrets.
   - `HOSTINGER_HOST`
   - `HOSTINGER_USERNAME`
   - `HOSTINGER_SSH_KEY`
   - `HOSTINGER_DEV_PATH`
   - `HOSTINGER_STAGING_PATH`
   - `HOSTINGER_PREVIEW_PATH`
   - Optional: `HOSTINGER_PROD_PATH`

5. Test environment deploys.
   - Push a harmless change to `dev` and verify `https://dev.reviews.ultramarine963.com/`.
   - Promote the same state to `staging` and verify `https://staging.reviews.ultramarine963.com/`.
   - Keep production on the current Hostinger Git deployment until the environment workflow is proven.

6. Add visual regression into the workflow.
   - Run the screenshot tests before deployment.
   - Store diffs as GitHub Actions artifacts.
   - Do not block production on the first run until thresholds are tuned.

## Star Rating Fix

Problem found:

- The live product pages still use a single full `★★★★★` string clipped to a percentage, for example `width: 88.0%`.
- At normal size, ratings like `4.4`, `4.7`, and `4.8` look too similar.

Prepared fix:

- Render each star separately.
- Compute each star's fill percentage in Hugo.
- Add a compact gold rating meter beside the numeric rating.

Verification:

- Hugo build passes: `69` pages, `133` static files.
- Local desktop screenshot shows `4.4 / 5` with four full stars, a visibly partial fifth star, and an 88% score meter.
- Local mobile screenshot shows the same rating treatment without text overlap.
