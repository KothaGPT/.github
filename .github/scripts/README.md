# KothaGPT Monitoring Scripts

This directory contains scripts for monitoring AI model performance, health, and drift detection in the KothaGPT project.

## Scripts Overview

### 🔍 `check_model_health.py`
**Purpose**: Comprehensive health monitoring of AI model endpoints, GitHub Pages sites, and GitHub API endpoints

**Usage**:
```bash
# Basic health check using environment variables
python scripts/check_model_health.py

# With custom configuration
python scripts/check_model_health.py --config monitoring_config.json --verbose

# Output results to file
python scripts/check_model_health.py --output health_report.json
```

**Environment Variables**:
- `MODEL_ENDPOINTS`: Comma-separated list of model endpoints to check (default: "http://localhost:8000/predict")

**Features**:
- AI model endpoint availability and prediction validation
- GitHub Pages site accessibility checks
- GitHub API endpoint monitoring with proper authentication
- Response time monitoring
- Error rate tracking
- Configurable thresholds

**Supported Endpoints**:
- **Model endpoints**: AI prediction services (e.g., `http://localhost:8000/predict`)
- **GitHub Pages**: Static websites (e.g., `https://kothagpt.github.io/`)
- **GitHub API**: Repository and organization data (e.g., `https://api.github.com/repos/KothaGPT/.github`)

### 📊 `benchmark_models.py` (Coming Soon)
**Purpose**: Performance benchmarking of AI models

### 🔄 `detect_drift.py` (Coming Soon)
**Purpose**: Detection of model performance drift over time

### 📋 `generate_report.py` (Coming Soon)
**Purpose**: Generate comprehensive monitoring reports

## Configuration

Create a `monitoring_config.json` file to customize monitoring behavior:

```json
{
  "model_endpoints": [
    "http://localhost:8000/predict"
  ],
  "github_pages_endpoints": [
    "https://kothagpt.github.io/",
    "https://kothagpt.github.io/.github/"
  ],
  "github_api_endpoints": [
    "https://api.github.com/repos/KothaGPT/.github",
    "https://api.github.com/repos/KothaGPT/.github/pages"
  ],
  "expected_response_time": 2.0,
  "max_error_rate": 0.05,
  "test_queries": [
    "Hello, how are you?",
    "What is machine learning?"
  ],
  "api_keys": {
    "https://api.github.com/repos/KothaGPT/.github": "${{ secrets.GITHUB_TOKEN }}"
  },
  "timeout": 30
}
```

## GitHub Actions Integration

These scripts are designed to work with the monitoring workflow in `.github/workflows/monitoring.yml`:

```yaml
- name: Check model endpoints
  run: |
    python scripts/check_model_health.py
```

The workflow runs every 6 hours and will:
- Create GitHub issues for failed health checks
- Send Slack notifications on failures
- Generate monitoring reports

## Exit Codes

- `0`: All checks passed
- `1`: One or more health checks failed
- `2`: Configuration or setup error

## GitHub Integration

### GitHub Pages Monitoring
- Checks if GitHub Pages sites are accessible and returning HTTP 200
- Handles rate limiting (403) and too many requests (429) responses appropriately
- Uses GitHub token for higher rate limits when available

### GitHub API Monitoring
- Monitors GitHub API endpoints for repository and organization data
- Uses proper GitHub API authentication with `GITHUB_TOKEN`
- Accepts standard GitHub API responses (200 for success, 404 for not found)
- Includes proper User-Agent headers as required by GitHub API

## Development

When adding new monitoring scripts:

1. Follow the existing code style and structure
2. Include comprehensive error handling
3. Add appropriate logging
4. Update this README
5. Test with the GitHub Actions workflow

## Security Notes

- Store API keys in GitHub repository secrets
- Use HTTPS endpoints in production
- Implement rate limiting for health checks
- Log sensitive information appropriately
- Follow GitHub API best practices and rate limits
