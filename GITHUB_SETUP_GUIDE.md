# GitHub Organization Setup Guide for KothaGPT

## 🚀 Step-by-Step Instructions to Enable Security Features and Branch Protection

### 1. Enable Organization-Wide Security Features

#### Dependabot Alerts
1. Go to your organization: `https://github.com/KothaGPT`
2. Click **Settings** in the left sidebar
3. Scroll down to **Security** section
4. Click **Dependabot alerts**
5. Enable **Dependabot alerts** for all repositories
6. Configure notification settings

#### Security Policy
1. In the same Security section, click **Security policy**
2. Create or edit your security policy using the provided SECURITY.md as a template

#### Code Security and Analysis
1. In Security settings, click **Code security and analysis**
2. Enable:
   - GitHub Advanced Security (if you have a license)
   - Secret scanning
   - Code scanning alerts
   - Dependabot alerts (already done)

### 2. Enable Branch Protection Rules

#### For Individual Repositories (e.g., main repo)
1. Go to your repository: `https://github.com/KothaGPT/core`
2. Click **Settings** > **Branches**
3. Click **Add rule** under "Branch protection rules"
4. Set **Branch name pattern** to `main`
5. Configure the following:

**Required status checks:**
- Require branches to be up to date before merging
- Require status checks to pass:
  - `AI Project CI` (from our workflow)
  - `Security Scan` (from our workflow)
  - Any other required checks

**Require pull request reviews:**
- Required approving reviews: 1
- Dismiss stale pull request approvals when new commits are pushed
- Require review from Code Owners

**Additional settings:**
- Require conversation resolution before merging
- Do not allow bypassing required pull request reviews (for admins too)
- Enable **Restrict pushes that create matching branches**

#### Apply to All Repositories
1. Go back to organization settings: `https://github.com/KothaGPT/settings`
2. Click **Repository defaults** in the left sidebar
3. Under **Branch protection**, enable similar rules for all repositories
4. Customize as needed for different repo types

### 3. Enable Required Reviews for Pull Requests

1. In repository settings, go to **Pull Requests**
2. Enable **Require pull request reviews before merging**
3. Set minimum number of approvals (recommend 1-2)
4. Enable **Dismiss stale pull request approvals**
5. Enable **Require review from Code Owners**

### 4. Set Up Organization-Wide Settings

#### Member Privileges
1. In organization settings, click **Member privileges**
2. Configure:
   - Allow members to create public repositories: Disabled
   - Allow members to create private repositories: Based on your needs
   - Default repository permission: Read

#### Team Creation
1. Ensure teams are set up (e.g., maintainers, contributors)
2. Configure team permissions appropriately

### 5. Enable GitHub Apps and Integrations

#### Slack Integration (for notifications)
1. Go to `https://github.com/KothaGPT/settings/installations`
2. Click **Configure** on Slack (or add if not present)
3. Set up notifications for PRs, issues, and deployments

#### Other Integrations
- **Codecov**: For test coverage (if needed)
- **Snyk**: For additional security scanning
- **Read the Docs**: For automatic documentation deployment

### 6. Verify and Test

1. **Create a test PR** in one of your repositories
2. Ensure:
   - CI checks run
   - Security scans pass
   - Branch protection prevents direct pushes
   - Labels are applied correctly

3. **Check notifications** in Slack or email for proper setup

### 7. Additional Recommendations

#### Enable Discussions
1. Go to your repository settings > **General**
2. Scroll to **Features** and enable **Discussions**
3. Create categories like "General", "Ideas", "Q&A", "Show and Tell"

#### Set Up Project Boards
1. Create project boards for tracking issues and PRs
2. Use automation to move issues between columns

#### Enable Wiki (if needed)
1. In repository settings, enable Wiki for documentation

### Troubleshooting

- **Branch protection not working**: Ensure the branch name matches exactly and required checks are passing
- **Dependabot not creating PRs**: Check that the ecosystem is properly configured in dependabot.yml
- **Notifications not working**: Verify webhook URLs and permissions

### Next Steps After Setup

1. **Monitor**: Keep an eye on the Security tab for alerts
2. **Update regularly**: Review and update branch protection rules as your team grows
3. **Train team**: Ensure all members understand the new processes
4. **Automate more**: Consider adding more workflows for releases, deployments, etc.

---

*This guide is based on GitHub's current interface. If you encounter issues, check the [GitHub documentation](https://docs.github.com) for the latest instructions.*
