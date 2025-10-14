# KothaGPT — Organization-level GitHub configuration

This repository contains recommended org-level GitHub configuration for KothaGPT. Drop these files into https://github.com/KothaGPT/.github (or upload via the web UI / gh CLI) to centralize templates and workflows across the organization.

## What's included (quick index)

- `.github/ISSUE_TEMPLATE/` — bug and feature templates
- `.github/PULL_REQUEST_TEMPLATE.md` — PR template
- `.github/CONTRIBUTING.md` — contributor guide + code of conduct hooks
- `.github/WORKFLOWS/` — GitHub Actions workflows:
  - `ci.yml` — CI (matrix tests + lint)
  - `release.yml` — releases and semantic tagging
  - `dependabot-updater.yml` — keep actions & infra up-to-date
  - `fork-sync.yml` — sync forks/branches from upstream (for community forks)
  - `automerge.yml` — auto-merge PRs when checks pass
  - `repo-maintenance.yml` — scheduled housekeeping (stale, labeler)
- `.github/dependabot.yml` — Dependabot config for deps & github actions
- `.github/CODEOWNERS` — default ownership rules
- `.github/SECURITY.md` — security policy / disclosure procedure
- `terraform/` — starter terraform examples to manage org settings

## File tree

```
.github/
├─ ISSUE_TEMPLATE/
│  ├─ bug_report.md
│  └─ feature_request.md
├─ workflows/
│  ├─ ci.yml
│  ├─ release.yml
│  ├─ dependabot-updater.yml
│  ├─ fork-sync.yml
│  ├─ automerge.yml
│  └─ repo-maintenance.yml
├─ PULL_REQUEST_TEMPLATE.md
├─ CONTRIBUTING.md
├─ CODEOWNERS
├─ dependabot.yml
├─ SECURITY.md
└─ terraform/
   └─ org-settings.tf
```

## Usage

1. **Copy files to your organization**: Upload these files to `https://github.com/KothaGPT/.github`
2. **Customize per repository**: Individual repositories can override these defaults by creating their own `.github/` directory
3. **Team setup**: Ensure the teams referenced in `CODEOWNERS` exist in your GitHub organization
4. **Terraform setup**: Configure GitHub token and backend for Terraform state management

## Security & policy recommendations

- Enable SAML/SCIM or enforced 2FA for org members
- Protect main branches with branch protection rules (require PR reviews, required checks, disallow force pushes)
- Use CODEOWNERS to request reviews automatically
- Enable Dependabot + automatic action updates
- Use org teams (not individual accounts) in CODEOWNERS so access rotates cleanly
- Use OIDC for Actions when deploying to cloud (avoid long-lived secrets)
- Use Terraform to manage org state and store Terraform state in a secure backend (S3/GCS + locking)

## Customization

Each repository can override these organization defaults by:
- Creating their own `.github/` directory
- Adding repository-specific workflow files
- Customizing issue/PR templates
- Overriding CODEOWNERS rules

## Notes

- All workflows use latest action versions (checkout@v4, etc.)
- Team names in CODEOWNERS assume GitHub teams are already created
- Terraform example requires GITHUB_TOKEN variable setup
- Repository-level overrides can customize these org defaults