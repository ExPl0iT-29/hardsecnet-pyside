#!/usr/bin/env bash
set -euo pipefail

# CIS Benchmark: CIS Ubuntu Linux 24.04 LTS Benchmark
# Control: 2.1.7 - Ensure ldap server services are not in use
# Source Page: 246
# Confidence: 0.96
# Status: review_required

# Audit guidance extracted from the benchmark
# Run the following command to verify slapd is not installed:
# # dpkg-query -s slapd &>/dev/null && echo "slapd is installed"
# Nothing should be returned.
# - OR -
# - IF - the package is required for dependencies:
# Run the following command to verify slapd.service is not enabled:
# # systemctl is-enabled slapd.service 2>/dev/null | grep 'enabled'
# Nothing should be returned.
# Run the following command to verify slapd.service is not active:
# # systemctl is-active slapd.service 2>/dev/null | grep '^active'
# Nothing should be returned.
# Note: If the package is required for a dependency
# -
# Ensure the dependent package is approved by local site policy
# -
# Ensure stopping and masking the service and/or socket meets local site policy
# Page 246

# Remediation candidate
# systemctl stop slapd.service
# OR -
# IF - the slapd package is required as a dependency:
# systemctl stop slapd.service
# systemctl mask slapd.service

# TODO: replace the commented/manual steps above with validated bash remediation logic.
