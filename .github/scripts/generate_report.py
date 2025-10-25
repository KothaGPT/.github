#!/usr/bin/env python3
"""
Monitoring Report Generator for KothaGPT

This script generates comprehensive monitoring reports for AI model performance,
health status, GitHub Pages sites, and GitHub API endpoints. The reports are
designed to be human-readable and suitable for GitHub issues and Slack notifications.

Usage:
    python scripts/generate_report.py --output monitoring_report.md [options]

Exit codes:
    0 - Report generated successfully
    1 - Error generating report
"""

import argparse
import json
import os
import sys
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional

import requests


class MonitoringReportGenerator:
    """Generates comprehensive monitoring reports for AI models."""

    def __init__(self):
        self.report_data = {
            'timestamp': datetime.now().isoformat(),
            'period': '6 hours',  # Based on workflow schedule
            'model_performance': {},
            'system_health': {},
            'alerts': [],
            'recommendations': []
        }

    def collect_health_data(self) -> Dict:
        """Collect health check data from previous runs."""
        health_data = {}

        # Check for health check results file
        health_file = os.path.join(os.path.dirname(__file__), 'health_report.json')
        if os.path.exists(health_file):
            try:
                with open(health_file, 'r') as f:
                    health_data = json.load(f)
            except (json.JSONDecodeError, IOError) as e:
                print(f"Warning: Could not read health report: {e}", file=sys.stderr)

        return health_data

    def collect_benchmark_data(self) -> Dict:
        """Collect benchmark data from previous runs."""
        benchmark_data = {}

        # Check for benchmark results file
        benchmark_file = os.path.join(os.path.dirname(__file__), 'benchmark_report.json')
        if os.path.exists(benchmark_file):
            try:
                with open(benchmark_file, 'r') as f:
                    benchmark_data = json.load(f)
            except (json.JSONDecodeError, IOError) as e:
                print(f"Warning: Could not read benchmark report: {e}", file=sys.stderr)

        return benchmark_data

    def collect_drift_data(self) -> Dict:
        """Collect drift detection data from previous runs."""
        drift_data = {}

        # Check for drift detection results file
        drift_file = os.path.join(os.path.dirname(__file__), 'drift_report.json')
        if os.path.exists(drift_file):
            try:
                with open(drift_file, 'r') as f:
                    drift_data = json.load(f)
            except (json.JSONDecodeError, IOError) as e:
                print(f"Warning: Could not read drift report: {e}", file=sys.stderr)

        return drift_data

    def generate_system_status(self) -> str:
        """Generate system status section of the report."""
        status = []

        # Overall system status
        status.append("## 🔍 System Health Overview")
        status.append("")

        # Check if services are running
        try:
            # Basic system resource checks
            import psutil
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')

            status.append(f"**CPU Usage:** {cpu_percent}%")
            status.append(f"**Memory Usage:** {memory.percent}% ({memory.used / 1024**3:.1f}GB / {memory.total / 1024**3:.1f}GB)")
            status.append(f"**Disk Usage:** {disk.percent}% ({disk.used / 1024**3:.1f}GB / {disk.total / 1024**3:.1f}GB)")
            status.append("")

            # System health indicators
            if cpu_percent > 90:
                status.append("⚠️ **High CPU Usage Detected**")
            if memory.percent > 90:
                status.append("⚠️ **High Memory Usage Detected**")
            if disk.percent > 90:
                status.append("⚠️ **High Disk Usage Detected**")

        except ImportError:
            status.append("System resource monitoring requires `psutil` package.")
            status.append("")
        except Exception as e:
            status.append(f"Error collecting system metrics: {e}")
            status.append("")

        return "\n".join(status)

    def generate_model_status(self, health_data: Dict) -> str:
        """Generate model status section of the report."""
        status = []

        status.append("## 🤖 AI Model Status")
        status.append("")

        if not health_data or 'results' not in health_data:
            status.append("No model health data available.")
            status.append("")
            return "\n".join(status)

        results = health_data['results']
        all_healthy = health_data.get('all_healthy', False)
        summary = health_data.get('summary', 'No summary available')

        # Overall status
        if all_healthy:
            status.append("✅ **All models are healthy**")
        else:
            status.append("❌ **Issues detected with one or more models**")

        status.append(f"**Summary:** {summary}")
        status.append("")

        # Detailed results
        status.append("### Endpoint Details")
        status.append("")
        status.append("| Endpoint | Status | Response Time | Error Rate | Details |")
        status.append("|----------|--------|---------------|------------|---------|")

        for result in results:
            endpoint_name = result['endpoint'].replace('http://', '').replace('https://', '').split('/')[0]
            status_icon = "✅" if result['available'] else "❌"
            response_time = f"{result['response_time']".2f"}s" if result['response_time'] > 0 else "N/A"
            error_rate = f"{result['error_rate']".1%"}" if result['error_rate'] > 0 else "0%"

            details = ""
            if result.get('error_message'):
                details = result['error_message'][:100] + "..." if len(result['error_message']) > 100 else result['error_message']

            status.append(f"| {endpoint_name} | {status_icon} | {response_time} | {error_rate} | {details} |")

        status.append("")

        # Model performance metrics
        if 'model_performance' in health_data:
            status.append("### Performance Metrics")
            status.append("")
            for metric, value in health_data['model_performance'].items():
                status.append(f"**{metric.replace('_', ' ').title()}:** {value}")
            status.append("")

        return "\n".join(status)

    def generate_benchmark_section(self, benchmark_data: Dict) -> str:
        """Generate benchmark results section."""
        section = []

        section.append("## 📊 Performance Benchmarks")
        section.append("")

        if not benchmark_data:
            section.append("No benchmark data available.")
            section.append("")
            return "\n".join(section)

        # Benchmark summary
        if 'summary' in benchmark_data:
            section.append(f"**Latest Results:** {benchmark_data['summary']}")
            section.append("")

        # Detailed benchmarks
        if 'benchmarks' in benchmark_data:
            section.append("### Benchmark Details")
            section.append("")
            section.append("| Model | Metric | Value | Baseline | Status |")
            section.append("|-------|--------|-------|----------|--------|")

            for benchmark in benchmark_data['benchmarks']:
                model = benchmark.get('model', 'Unknown')
                metric = benchmark.get('metric', 'Unknown')
                value = benchmark.get('value', 'N/A')
                baseline = benchmark.get('baseline', 'N/A')
                status = benchmark.get('status', 'Unknown')

                section.append(f"| {model} | {metric} | {value} | {baseline} | {status} |")

            section.append("")

        return "\n".join(section)

    def generate_drift_section(self, drift_data: Dict) -> str:
        """Generate drift detection section."""
        section = []

        section.append("## 🔄 Model Drift Detection")
        section.append("")

        if not drift_data:
            section.append("No drift detection data available.")
            section.append("")
            return "\n".join(section)

        # Drift summary
        if 'drift_detected' in drift_data:
            if drift_data['drift_detected']:
                section.append("⚠️ **Model drift detected**")
                section.append("")
                section.append("Model performance has deviated from baseline. Consider retraining or model updates.")
            else:
                section.append("✅ **No significant drift detected**")
            section.append("")

        # Drift details
        if 'drift_metrics' in drift_data:
            section.append("### Drift Metrics")
            section.append("")
            for metric, details in drift_data['drift_metrics'].items():
                threshold = details.get('threshold', 'N/A')
                current = details.get('current_value', 'N/A')
                status = details.get('status', 'Unknown')

                section.append(f"**{metric}:** {current} (threshold: {threshold}) - {status}")
            section.append("")

        return "\n".join(section)

    def generate_recommendations(self, health_data: Dict, benchmark_data: Dict, drift_data: Dict) -> str:
        """Generate recommendations based on collected data."""
        recommendations = []

        recommendations.append("## 💡 Recommendations")
        recommendations.append("")

        # Health-based recommendations
        if health_data and not health_data.get('all_healthy', True):
            recommendations.append("### Immediate Actions Required")
            recommendations.append("- Investigate failed model endpoints")
            recommendations.append("- Check network connectivity and service status")
            recommendations.append("- Review error logs for detailed failure information")
            recommendations.append("")

        # Performance-based recommendations
        if benchmark_data:
            recommendations.append("### Performance Optimization")
            recommendations.append("- Monitor response times for slow endpoints")
            recommendations.append("- Consider scaling resources if consistently high CPU/memory usage")
            recommendations.append("- Review model inference optimization opportunities")
            recommendations.append("")

        # Drift-based recommendations
        if drift_data and drift_data.get('drift_detected', False):
            recommendations.append("### Model Updates")
            recommendations.append("- Schedule model retraining with latest data")
            recommendations.append("- Update model baselines after retraining")
            recommendations.append("- Monitor drift metrics more frequently")
            recommendations.append("")

        # General recommendations
        recommendations.append("### General Maintenance")
        recommendations.append("- Review and update monitoring thresholds as needed")
        recommendations.append("- Ensure backup systems are operational")
        recommendations.append("- Update dependencies and security patches")
        recommendations.append("")

        return "\n".join(recommendations)

    def generate_report(self, output_file: str) -> bool:
        """Generate the complete monitoring report."""
        try:
            # Collect all data
            health_data = self.collect_health_data()
            benchmark_data = self.collect_benchmark_data()
            drift_data = self.collect_drift_data()

            # Generate report sections
            report_sections = []

            # Header
            report_sections.append("# 🚨 AI Model Monitoring Report")
            report_sections.append("")
            report_sections.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}")
            report_sections.append(f"**Monitoring Period:** Last {self.report_data['period']}")
            report_sections.append("")

            # System status
            report_sections.append(self.generate_system_status())

            # Model status
            report_sections.append(self.generate_model_status(health_data))

            # Benchmark results
            report_sections.append(self.generate_benchmark_section(benchmark_data))

            # Drift detection
            report_sections.append(self.generate_drift_section(drift_data))

            # Recommendations
            report_sections.append(self.generate_recommendations(health_data, benchmark_data, drift_data))

            # Footer
            report_sections.append("---")
            report_sections.append("")
            report_sections.append("*This report was generated automatically by the KothaGPT monitoring system.*")
            report_sections.append("*For questions or issues, please contact the ML team.*")

            # Write report
            with open(output_file, 'w') as f:
                f.write('\n'.join(report_sections))

            print(f"✅ Monitoring report generated successfully: {output_file}")
            return True

        except Exception as e:
            print(f"❌ Error generating monitoring report: {e}", file=sys.stderr)
            return False


def main():
    """Main entry point for the report generator."""
    parser = argparse.ArgumentParser(description='Generate AI model monitoring report')
    parser.add_argument('--output', '-o', required=True, help='Output file path for the report')
    parser.add_argument('--format', choices=['markdown', 'json', 'html'], default='markdown',
                       help='Output format (default: markdown)')
    parser.add_argument('--include-system', action='store_true', default=True,
                       help='Include system metrics in report')
    parser.add_argument('--verbose', '-v', action='store_true', help='Enable verbose logging')

    args = parser.parse_args()

    if args.verbose:
        print("Starting monitoring report generation...")

    # Generate report
    generator = MonitoringReportGenerator()

    success = generator.generate_report(args.output)

    if success:
        print(f"Report saved to: {args.output}")
        sys.exit(0)
    else:
        print("Failed to generate report", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
