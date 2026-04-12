#!/usr/bin/env bash
set -euo pipefail

# CIS Benchmark: CIS Ubuntu Linux 24.04 LTS Benchmark
# Control: 2.1.16 - Ensure tftp server services are not in use
# Source Page: 271
# Confidence: 0.96
# Status: review_required

# Audit guidance extracted from the benchmark
# Run the following command to verify tftpd-hpa is not installed:
# # dpkg-query -s tftpd-hpa &>/dev/null && echo "tftpd-hpa is installed"
# Nothing should be returned.
# - OR -
# - IF - the package is required for dependencies:
# Run the following command to verify tftpd-hpa.service is not enabled:
# # systemctl is-enabled tftpd-hpa.service 2>/dev/null | grep 'enabled'
# Nothing should be returned.
# Run the following command to verify the tftpd-hpa.service is not active:
# # systemctl is-active tftpd-hpa.service 2>/dev/null | grep '^active'
# Nothing should be returned.
# Note: If the package is required for a dependency
# -
# Ensure the dependent package is approved by local site policy
# -
# Ensure stopping and masking the service and/or socket meets local site policy

# Remediation candidate
# systemctl stop tftpd-hpa.service
# OR -
# IF - the tftpd-hpa package is required as a dependency:
# systemctl stop tftpd-hpa.service
# systemctl mask tftpd-hpa.service

# TODO: replace the commented/manual steps above with validated bash remediation logic.
