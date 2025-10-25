#!/usr/bin/env python3
"""
GitHub Pages and API Health Check Script for KothaGPT

This script performs comprehensive health checks on:
- AI model endpoints (prediction services)
- GitHub Pages sites (static websites)
- GitHub API endpoints (repository and organization data)
- Response times and availability monitoring
- Error rate tracking

Usage:
    python scripts/check_model_health.py [--config config.json] [--verbose]

Exit codes:
    0 - All checks passed
    1 - One or more health checks failed
    2 - Configuration or setup error
"""

import argparse
import json
import logging
import os
import sys
import time
from typing import Dict, List, Optional, Tuple

import requests
from dataclasses import dataclass
from pathlib import Path


@dataclass
class HealthCheckConfig:
    """Configuration for model health checks."""
    model_endpoints: List[str]
    github_pages_endpoints: List[str] = None
    github_api_endpoints: List[str] = None
    expected_response_time: float = 2.0  # seconds
    max_error_rate: float = 0.05  # 5%
    test_queries: List[str] = None
    api_keys: Dict[str, str] = None
    timeout: int = 30

    def __post_init__(self):
        if self.github_pages_endpoints is None:
            self.github_pages_endpoints = []
        if self.github_api_endpoints is None:
            self.github_api_endpoints = []
        if self.test_queries is None:
            self.test_queries = [
                "Hello, how are you?",
                "What is the capital of France?",
                "Explain quantum computing in simple terms."
            ]
        if self.api_keys is None:
            self.api_keys = {}


@dataclass
class HealthCheckResult:
    """Result of a single health check."""
    endpoint: str
    available: bool
    response_time: float
    error_rate: float
    status_code: int
    error_message: Optional[str] = None


class ModelHealthChecker:
    """Main class for performing AI model health checks."""

    def __init__(self, config: HealthCheckConfig):
        self.config = config
        self.setup_logging()

    def setup_logging(self):
        """Setup logging configuration."""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)

    def load_config(self, config_path: Optional[str] = None) -> HealthCheckConfig:
        """Load configuration from file or use defaults."""
        if config_path and os.path.exists(config_path):
            with open(config_path, 'r') as f:
                data = json.load(f)
                return HealthCheckConfig(**data)
        else:
            # Default configuration
            endpoints = os.getenv('MODEL_ENDPOINTS', 'http://localhost:8000/predict').split(',')
            return HealthCheckConfig(
                model_endpoints=[e.strip() for e in endpoints if e.strip()]
            )

    def check_endpoint_health(self, endpoint: str) -> HealthCheckResult:
        """
        Check the health of a single model endpoint.

        Returns:
            HealthCheckResult: The result of the health check
        """
        self.logger.info(f"Checking health of endpoint: {endpoint}")

        start_time = time.time()

        try:
            # Prepare test request
            headers = {'Content-Type': 'application/json'}
            if endpoint in self.config.api_keys:
                headers['Authorization'] = f'Bearer {self.config.api_keys[endpoint]}'

            # Try a health check endpoint first
            health_url = f"{endpoint.rstrip('/')}/health"
            response = requests.get(health_url, timeout=self.config.timeout)

            if response.status_code == 200:
                response_time = time.time() - start_time
                return HealthCheckResult(
                    endpoint=endpoint,
                    available=True,
                    response_time=response_time,
                    error_rate=0.0,
                    status_code=response.status_code
                )
            else:
                return HealthCheckResult(
                    endpoint=endpoint,
                    available=False,
                    response_time=time.time() - start_time,
                    error_rate=1.0,
                    status_code=response.status_code,
                    error_message=f"Health check failed with status {response.status_code}"
                )

        except requests.exceptions.Timeout:
            return HealthCheckResult(
                endpoint=endpoint,
                available=False,
                response_time=time.time() - start_time,
                error_rate=1.0,
                status_code=0,
                error_message="Request timeout"
            )
        except requests.exceptions.ConnectionError:
            return HealthCheckResult(
                endpoint=endpoint,
                available=False,
                response_time=time.time() - start_time,
                error_rate=1.0,
                status_code=0,
                error_message="Connection refused"
            )
        except Exception as e:
            return HealthCheckResult(
                endpoint=endpoint,
                available=False,
                response_time=time.time() - start_time,
                error_rate=1.0,
                status_code=0,
                error_message=str(e)
            )

    def check_model_prediction(self, endpoint: str) -> Tuple[bool, str]:
        """
        Test model prediction functionality.

        Returns:
            Tuple of (success: bool, error_message: str)
        """
        try:
            headers = {'Content-Type': 'application/json'}
            if endpoint in self.config.api_keys:
                headers['Authorization'] = f'Bearer {self.config.api_keys[endpoint]}'

            # Test with a simple query
            test_payload = {
                'query': self.config.test_queries[0],
                'max_tokens': 50
            }

            response = requests.post(
                endpoint,
                json=test_payload,
                headers=headers,
                timeout=self.config.timeout
            )

            if response.status_code == 200:
                result = response.json()
                if 'response' in result or 'prediction' in result:
                    return True, ""
                else:
                    return False, "Invalid response format"
            else:
                return False, f"Prediction failed with status {response.status_code}"

        except Exception as e:
            return False, str(e)

    def check_github_pages_health(self, endpoint: str) -> HealthCheckResult:
        """
        Check the health of a GitHub Pages site.

        Returns:
            HealthCheckResult: The result of the health check
        """
        self.logger.info(f"Checking GitHub Pages site: {endpoint}")

        start_time = time.time()

        try:
            # Simple HTTP GET request to check if site is accessible
            headers = {}
            if endpoint in self.config.api_keys:
                # GitHub token can be used for higher rate limits
                headers['Authorization'] = f'token {self.config.api_keys[endpoint]}'

            response = requests.get(endpoint, headers=headers, timeout=self.config.timeout)

            # GitHub Pages typically returns 200 for successful sites
            # or 404 if the page doesn't exist
            # or 403 for rate limiting
            is_available = response.status_code in [200, 403, 429]

            response_time = time.time() - start_time
            error_rate = 0.0 if is_available else 1.0

            error_message = None
            if not is_available:
                error_message = f"GitHub Pages site returned status {response.status_code}"
            elif response.status_code == 403:
                error_message = "Rate limited by GitHub API"
            elif response.status_code == 429:
                error_message = "Too many requests to GitHub"

            return HealthCheckResult(
                endpoint=endpoint,
                available=is_available,
                response_time=response_time,
                error_rate=error_rate,
                status_code=response.status_code,
                error_message=error_message
            )

        except requests.exceptions.Timeout:
            return HealthCheckResult(
                endpoint=endpoint,
                available=False,
                response_time=time.time() - start_time,
                error_rate=1.0,
                status_code=0,
                error_message="Request timeout"
            )
        except requests.exceptions.ConnectionError:
            return HealthCheckResult(
                endpoint=endpoint,
                available=False,
                response_time=time.time() - start_time,
                error_rate=1.0,
                status_code=0,
                error_message="Connection refused"
            )
        except Exception as e:
            return HealthCheckResult(
                endpoint=endpoint,
                available=False,
                response_time=time.time() - start_time,
                error_rate=1.0,
                status_code=0,
                error_message=str(e)
            )

    def check_github_api_health(self, endpoint: str) -> HealthCheckResult:
        """
        Check the health of a GitHub API endpoint.

        Returns:
            HealthCheckResult: The result of the health check
        """
        self.logger.info(f"Checking GitHub API endpoint: {endpoint}")

        start_time = time.time()

        try:
            # Prepare headers for GitHub API
            headers = {
                'Accept': 'application/vnd.github.v3+json',
                'User-Agent': 'KothaGPT-Monitoring/1.0'
            }

            if endpoint in self.config.api_keys:
                headers['Authorization'] = f'token {self.config.api_keys[endpoint]}'

            response = requests.get(endpoint, headers=headers, timeout=self.config.timeout)

            # GitHub API returns 200 for success, 404 for not found, etc.
            is_available = response.status_code in [200, 404]
            response_time = time.time() - start_time
            error_rate = 0.0 if is_available else 1.0

            error_message = None
            if not is_available:
                error_message = f"GitHub API returned status {response.status_code}"
            elif response.status_code == 404:
                error_message = "Repository or API endpoint not found"

            return HealthCheckResult(
                endpoint=endpoint,
                available=is_available,
                response_time=response_time,
                error_rate=error_rate,
                status_code=response.status_code,
                error_message=error_message
            )

        except requests.exceptions.Timeout:
            return HealthCheckResult(
                endpoint=endpoint,
                available=False,
                response_time=time.time() - start_time,
                error_rate=1.0,
                status_code=0,
                error_message="Request timeout"
            )
        except requests.exceptions.ConnectionError:
            return HealthCheckResult(
                endpoint=endpoint,
                available=False,
                response_time=time.time() - start_time,
                error_rate=1.0,
                status_code=0,
                error_message="Connection refused"
            )
        except Exception as e:
            return HealthCheckResult(
                endpoint=endpoint,
                available=False,
                response_time=time.time() - start_time,
                error_rate=1.0,
                status_code=0,
                error_message=str(e)
            )

    def run_comprehensive_check(self) -> List[HealthCheckResult]:
        results = []

        # Check model endpoints
        for endpoint in self.config.model_endpoints:
            # Basic health check
            health_result = self.check_endpoint_health(endpoint)
            results.append(health_result)

            # If endpoint is available, test prediction
            if health_result.available:
                prediction_success, error_msg = self.check_model_prediction(endpoint)
                if not prediction_success:
                    self.logger.warning(f"Prediction test failed for {endpoint}: {error_msg}")
                    health_result.error_rate = 1.0
                    health_result.error_message = error_msg
                    health_result.available = False

        # Check GitHub Pages endpoints
        for endpoint in self.config.github_pages_endpoints:
            pages_result = self.check_github_pages_health(endpoint)
            results.append(pages_result)

        # Check GitHub API endpoints
        for endpoint in self.config.github_api_endpoints:
            api_result = self.check_github_api_health(endpoint)
            results.append(api_result)

        return results

    def evaluate_results(self, results: List[HealthCheckResult]) -> Tuple[bool, str]:
        """
        Evaluate health check results and determine overall status.

        Returns:
            Tuple of (all_healthy: bool, summary: str)
        """
        if not results:
            return False, "No endpoints to check"

        healthy_count = sum(1 for r in results if r.available)
        total_count = len(results)

        # Check response times
        slow_endpoints = [r for r in results if r.response_time > self.config.expected_response_time]
        high_error_endpoints = [r for r in results if r.error_rate > self.config.max_error_rate]

        summary_parts = [f"Checked {total_count} endpoints: {healthy_count} healthy"]

        if slow_endpoints:
            summary_parts.append(f"{len(slow_endpoints)} slow (> {self.config.expected_response_time}s)")

        if high_error_endpoints:
            summary_parts.append(f"{len(high_error_endpoints)} with high error rate")

        summary = ", ".join(summary_parts)

        # Overall health determination
        all_healthy = (
            healthy_count == total_count and
            len(slow_endpoints) == 0 and
            len(high_error_endpoints) == 0
        )

        return all_healthy, summary


def main():
    """Main entry point for the health check script."""
    parser = argparse.ArgumentParser(description='Check AI model health and performance')
    parser.add_argument('--config', type=str, help='Path to configuration file')
    parser.add_argument('--verbose', '-v', action='store_true', help='Enable verbose logging')
    parser.add_argument('--output', type=str, help='Output file for results (JSON)')

    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    # Load configuration
    checker = ModelHealthChecker(HealthCheckConfig([]))
    config = checker.load_config(args.config)

    if not config.model_endpoints and not config.github_pages_endpoints and not config.github_api_endpoints:
        print("ERROR: No endpoints configured", file=sys.stderr)
        print("Configure model_endpoints, github_pages_endpoints, or github_api_endpoints", file=sys.stderr)
        sys.exit(2)

    # Run health checks
    results = checker.run_comprehensive_check()

    # Evaluate results
    all_healthy, summary = checker.evaluate_results(results)

    print(f"Health Check Summary: {summary}")
    print("\nDetailed Results:")

    for result in results:
        status = "✅ HEALTHY" if result.available else "❌ UNHEALTHY"
        print(f"  {result.endpoint}: {status}")
        print(f"    Response time: {result.response_time".2f"}s")
        print(f"    Error rate: {result.error_rate".1%"}")
        if result.error_message:
            print(f"    Error: {result.error_message}")

    # Output results to file if requested
    if args.output:
        output_data = {
            'summary': summary,
            'all_healthy': all_healthy,
            'timestamp': time.time(),
            'results': [
                {
                    'endpoint': r.endpoint,
                    'available': r.available,
                    'response_time': r.response_time,
                    'error_rate': r.error_rate,
                    'status_code': r.status_code,
                    'error_message': r.error_message
                }
                for r in results
            ]
        }

        with open(args.output, 'w') as f:
            json.dump(output_data, f, indent=2)

    # Exit with appropriate code
    if not all_healthy:
        print(f"\n❌ HEALTH CHECK FAILED: {summary}")
        sys.exit(1)
    else:
        print(f"\n✅ ALL HEALTH CHECKS PASSED: {summary}")
        sys.exit(0)


if __name__ == '__main__':
    main()
