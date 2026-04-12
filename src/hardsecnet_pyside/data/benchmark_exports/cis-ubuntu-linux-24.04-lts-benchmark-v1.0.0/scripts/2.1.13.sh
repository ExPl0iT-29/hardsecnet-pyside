#!/usr/bin/env bash
set -euo pipefail

# CIS Benchmark: CIS Ubuntu Linux 24.04 LTS Benchmark
# Control: 2.1.13 - Ensure rsync services are not in use
# Source Page: 264
# Confidence: 0.96
# Status: review_required

# Audit guidance extracted from the benchmark
# Run the following command to verify rsync is not installed:
# # dpkg-query -s rsync &>/dev/null && echo "rsync is installed"
# Nothing should be returned.
# - OR -
# - IF - the rsync package is required as a dependency:
# Run the following command to verify rsync.service is not enabled:
# # systemctl is-enabled rsync.service 2>/dev/null | grep 'enabled'
# Nothing should be returned.
# Run the following command to verify rsync.service is not active:
# # systemctl is-active rsync.service 2>/dev/null | grep '^active'
# Nothing should be returned.
# Note: If the package is required for a dependency
# -
# Ensure the dependent package is approved by local site policy
# -
# Ensure stopping and masking the service and/or socket meets local site policy
# Page 264

# Remediation candidate
# systemctl stop rsync.service
# OR -
# IF - the rsync package is required as a dependency:
# systemctl stop rsync.service
# systemctl mask rsync.service

# TODO: replace the commented/manual steps above with validated bash remediation logic.
