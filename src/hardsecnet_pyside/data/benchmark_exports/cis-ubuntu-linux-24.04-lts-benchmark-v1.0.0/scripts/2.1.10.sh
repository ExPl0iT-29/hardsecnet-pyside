#!/usr/bin/env bash
set -euo pipefail

# CIS Benchmark: CIS Ubuntu Linux 24.04 LTS Benchmark
# Control: 2.1.10 - Ensure nis server services are not in use
# Source Page: 255
# Confidence: 0.96
# Status: review_required

# Audit guidance extracted from the benchmark
# Run the following command to verify ypserv is not installed:
# # dpkg-query -s ypserv &>/dev/null && echo "ypserv is installed"
# Nothing should be returned.
# - OR -
# - IF - the package is required for dependencies:
# Run the following command to verify ypserv.service is not enabled:
# # systemctl is-enabled ypserv.service 2>/dev/null | grep 'enabled'
# Nothing should be returned.
# Run the following command to verify ypserv.service is not active:
# # systemctl is-active ypserv.service 2>/dev/null | grep '^active'
# Nothing should be returned.
# Note: If the package is required for a dependency
# -
# Ensure the dependent package is approved by local site policy
# -
# Ensure stopping and masking the service and/or socket meets local site policy

# Remediation candidate
# systemctl stop ypserv.service
# OR -
# IF - the ypserv package is required as a dependency:
# systemctl stop ypserv.service
# systemctl mask ypserv.service

# TODO: replace the commented/manual steps above with validated bash remediation logic.
