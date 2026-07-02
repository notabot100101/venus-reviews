# Venus Reviews

**Domain:** ultramarine963.com  
**Subdomain:** reviews.ultramarine963.com
**Public name:** Venus Reviews

## Quick Start

```bash
cd /home/paul/.openclaw/workspaces/assistant/venus-site
./build.sh
```

## Git + Hostinger Deployment

Recommended setup:

1. Keep the Hugo source on the `main` branch.
2. Generate a static deploy branch named `hostinger-deploy`.
3. Connect Hostinger Git deployment to the `hostinger-deploy` branch.

This avoids requiring Hugo on Hostinger. Hostinger only receives plain HTML/CSS files.

```bash
git init
git add .
git commit -m "Initial Venus Reviews site"

# After adding a GitHub/GitLab remote:
git remote add origin <YOUR_REPOSITORY_URL>
git push -u origin main

# Create/update static branch for Hostinger:
scripts/publish-hostinger-branch.sh
git push origin hostinger-deploy
```

### Hostinger Settings

In Hostinger hPanel:

1. Open `reviews.ultramarine963.com`.
2. Go to Git / Git Deployment.
3. Connect the repository.
4. Select branch: `hostinger-deploy`.
5. Set deploy path to the website root, usually `public_html/`.
6. Enable auto-deploy/webhook if Hostinger offers it.

Each update from this workspace is then:

```bash
git add .
git commit -m "Update content"
git push origin main
scripts/publish-hostinger-branch.sh
git push origin hostinger-deploy
```

## DNS Configuration

Since the subdomain was created in Hostinger, keep DNS pointed at Hostinger's nameservers or add the Hostinger-provided A/CNAME record wherever DNS is managed.

## Local Development

```bash
./.bin/hugo server --bind 0.0.0.0 --baseURL http://localhost:1313/
```

## Site Structure

```
venus-site/
├── archetypes/              # Post templates
├── content/                 # Site content
│   ├── en/
│   │   ├── about/          # About page
│   │   ├── affiliate-disclosure/
│   │   └── privacy/        # Privacy policy
├── data/                    # Configuration data
│   ├── products/           # Product data
│   └── comparisons/        # Comparison sets
├── i18n/                    # Translations
├── layouts/                 # Hugo layouts
│   ├── _default/
│   ├── partials/
│   ├── shortcodes/
│   └── pages/
├── static/                  # Static assets
│   ├── css/
│   ├── js/
│   └── images/
└── hugo.toml               # Configuration
```

## Next Steps

1. Add a remote repository URL.
2. Push `main`.
3. Generate and push `hostinger-deploy`.
4. Connect Hostinger to `hostinger-deploy`.
5. Replace placeholder content with verified affiliate links and sourced digital-only comparison articles.
