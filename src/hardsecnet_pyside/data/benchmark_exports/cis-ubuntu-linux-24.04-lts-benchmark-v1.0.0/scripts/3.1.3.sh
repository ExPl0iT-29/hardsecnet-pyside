#!/usr/bin/env bash
set -euo pipefail

# CIS Benchmark: CIS Ubuntu Linux 24.04 LTS Benchmark
# Control: 3.1.3 - Ensure bluetooth services are not in use
# Source Page: 362
# Confidence: 0.96
# Status: review_required

# Audit guidance extracted from the benchmark
# Run the following command to verify the bluez package is not installed:
# # dpkg-query -s bluez &>/dev/null && echo "bluez is installed"
# Nothing should be returned.
# - OR -
# - IF - the bluez package is required as a dependency:
# Run the following command to verify bluetooth.service is not enabled:
# # systemctl is-enabled bluetooth.service 2>/dev/null | grep 'enabled'
# Nothing should be returned.
# Run the following command to verify bluetooth.service is not active:
# # systemctl is-active bluetooth.service 2>/dev/null | grep '^active'
# Nothing should be returned.
# Note: If the package is required for a dependency
# -
# Ensure the dependent package is approved by local site policy
# -
# Ensure stopping and masking the service and/or socket meets local site policy

# Remediation candidate
# systemctl stop bluetooth.service
# OR -
# IF - the bluez package is required as a dependency:
# systemctl stop bluetooth.service
# systemctl mask bluetooth.service

# TODO: replace the commented/manual steps above with validated bash remediation logic.
