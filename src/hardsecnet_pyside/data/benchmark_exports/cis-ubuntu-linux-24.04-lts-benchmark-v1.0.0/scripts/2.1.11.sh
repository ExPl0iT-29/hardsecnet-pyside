#!/usr/bin/env bash
set -euo pipefail

# CIS Benchmark: CIS Ubuntu Linux 24.04 LTS Benchmark
# Control: 2.1.11 - Ensure print server services are not in use
# Source Page: 258
# Confidence: 0.96
# Status: review_required

# Audit guidance extracted from the benchmark
# Run the following command to verify cups is not Installed:
# # dpkg-query -s cups &>/dev/null && echo "cups is installed"
# Nothing should be returned.
# - OR -
# - IF - the cups package is required as a dependency:
# Run the following command to verify the cups.socket and cups.service are not
# enabled:
# # systemctl is-enabled cups.socket cups.service 2>/dev/null | grep 'enabled'
# Nothing should be returned.
# Run the following command to verify the cups.socket and cups.service are not
# active:
# # systemctl is-active cups.socket cups.service 2>/dev/null | grep '^active'
# Nothing should be returned.
# Note: If the package is required for a dependency
# -
# Ensure the dependent package is approved by local site policy
# -
# Ensure stopping and masking the service and/or socket meets local site policy

# Remediation candidate
# systemctl stop cups.socket cups.service
# OR -
# IF - the cups package is required as a dependency:
# systemctl stop cups.socket cups.service
# systemctl mask cups.socket cups.service

# TODO: replace the commented/manual steps above with validated bash remediation logic.
