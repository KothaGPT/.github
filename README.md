# KothaGPT — Organization-level GitHub configuration

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![CI Status](https://github.com/KothaGPT/.github/workflows/ci.yml/badge.svg)](https://github.com/KothaGPT/.github/actions)

This repository contains recommended org-level GitHub configuration for KothaGPT. Drop these files into https://github.com/KothaGPT/.github (or upload via the web UI / gh CLI) to centralize templates and workflows across the organization.

## 🌟 About KothaGPT

KothaGPT is an open-source organization dedicated to advancing conversational AI through collaborative development. We build tools, models, and APIs that make AI more accessible and powerful for everyone.

[View our Organization Profile README →](profile/README.md)

## What's included (quick index)

- `.github/ISSUE_TEMPLATE/` — bug and feature templates
- `.github/PULL_REQUEST_TEMPLATE.md` — PR template
- `.github/CONTRIBUTING.md` — contributor guide + code of conduct hooks
- `.github/WORKFLOWS/` — GitHub Actions workflows:
  - `ci.yml` — AI-optimized CI (matrix tests + lint + model validation)
  - `release.yml` — releases and semantic tagging
  - `dependabot-updater.yml` — keep actions & infra up-to-date
  - `fork-sync.yml` — sync forks/branches from upstream
  - `automerge.yml` — auto-merge PRs when checks pass
  - `repo-maintenance.yml` — scheduled housekeeping (stale, labeler)
  - `security.yml` — vulnerability scanning and CodeQL analysis
  - `deploy.yml` — automated deployment to cloud
  - `model-training.yml` — AI model training and validation
  - `ai-review.yml` — automated AI-powered code review
  - `monitoring.yml` — AI model performance monitoring and alerting
- `.github/requirements.txt` — Core dependencies (monitoring only)
- `.github/requirements-monitoring.txt` — Monitoring-specific dependencies
- `requirements.txt` — Core dependencies for monitoring workflows
- `requirements-monitoring.txt` — Lightweight monitoring dependencies only
- `requirements-training.txt` — Heavy ML training dependencies (optional)

## Python Dependencies

The repository includes multiple requirements files for different use cases:

### Monitoring Dependencies
Install monitoring dependencies for health checks and reporting:
```bash
pip install -r requirements-monitoring.txt
```

**Includes:** requests, prometheus_client

### Full Dependencies
Install all dependencies including ML training packages:
```bash
pip install -r requirements.txt
```

**Includes:** All monitoring dependencies plus torch, transformers, datasets, etc.

### Development Setup
For local development with all features:
```bash
# Install all dependencies
pip install -r requirements.txt

# Or install only what you need
pip install -r requirements-monitoring.txt  # for monitoring only
pip install -r requirements-training.txt     # for ML training only
```

```
.github/
├─ ISSUE_TEMPLATE/
│  ├─ bug_report.md
│  ├─ feature_request.md
│  ├─ documentation.md
│  ├─ performance.md
│  └─ ai_model.md
├─ workflows/
│  ├─ ci.yml
│  ├─ release.yml
│  ├─ dependabot-updater.yml
│  ├─ fork-sync.yml
│  ├─ automerge.yml
│  ├─ repo-maintenance.yml
│  ├─ security.yml
│  ├─ deploy.yml
│  ├─ model-training.yml
│  ├─ ai-review.yml
│  └─ monitoring.yml
├─ scripts/
│  ├─ README.md
│  ├─ check_model_health.py
│  ├─ generate_report.py
│  ├─ monitoring_config.json
│  ├─ benchmark_models.py (coming soon)
│  ├─ detect_drift.py (coming soon)
│  └─ create_model_card.py (coming soon)
├─ PULL_REQUEST_TEMPLATE.md
├─ CONTRIBUTING.md
├─ CODEOWNERS
├─ dependabot.yml
├─ SECURITY.md
├─ requirements.txt
├─ requirements-monitoring.txt
├─ requirements-training.txt
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

---

*This configuration is maintained by the KothaGPT core team. For questions or suggestions, please [open an issue](https://github.com/KothaGPT/.github/issues) or [start a discussion](https://github.com/KothaGPT/.github/discussions).*"