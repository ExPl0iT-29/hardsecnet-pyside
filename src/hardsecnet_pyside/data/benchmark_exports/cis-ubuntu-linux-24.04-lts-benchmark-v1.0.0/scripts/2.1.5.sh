#!/usr/bin/env bash
set -euo pipefail

# CIS Benchmark: CIS Ubuntu Linux 24.04 LTS Benchmark
# Control: 2.1.5 - Ensure dnsmasq services are not in use
# Source Page: 241
# Confidence: 0.96
# Status: review_required

# Audit guidance extracted from the benchmark
# Run one of the following commands to verify dnsmasq is not installed:
# # dpkg-query -s dnsmasq &>/dev/null && echo "dnsmasq is installed"
# Nothing should be returned.
# - OR -
# - IF - the package is required for dependencies:
# Run the following command to verify dnsmasq.service is not enabled:
# # systemctl is-enabled dnsmasq.service 2>/dev/null | grep 'enabled'
# Nothing should be returned.
# Run the following command to verify the dnsmasq.service is not active:
# # systemctl is-active dnsmasq.service 2>/dev/null | grep '^active'
# Nothing should be returned.
# Note: If the package is required for a dependency
# -
# Ensure the dependent package is approved by local site policy
# -
# Ensure stopping and masking the service and/or socket meets local site policy
# Page 241

# Remediation candidate
# systemctl stop dnsmasq.service
# OR -
# IF - the dnsmasq package is required as a dependency:
# systemctl stop dnsmasq.service
# systemctl mask dnsmasq.service

# TODO: replace the commented/manual steps above with validated bash remediation logic.
