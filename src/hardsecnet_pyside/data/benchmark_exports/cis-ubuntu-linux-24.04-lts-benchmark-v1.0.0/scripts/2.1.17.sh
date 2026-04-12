#!/usr/bin/env bash
set -euo pipefail

# CIS Benchmark: CIS Ubuntu Linux 24.04 LTS Benchmark
# Control: 2.1.17 - Ensure web proxy server services are not in use
# Source Page: 274
# Confidence: 0.96
# Status: review_required

# Audit guidance extracted from the benchmark
# Run the following command to verify squid is not installed:
# # dpkg-query -s squid &>/dev/null && echo "squid is installed"
# Nothing should be returned.
# - OR -
# - IF - the package is required for dependencies:
# Run the following command to verify squid.service is not enabled:
# # systemctl is-enabled squid.service 2>/dev/null | grep 'enabled'
# Nothing should be returned.
# Run the following command to verify the squid.service is not active:
# # systemctl is-active squid.service 2>/dev/null | grep '^active'
# Nothing should be returned.
# Note: If the package is required for a dependency
# -
# Ensure the dependent package is approved by local site policy
# -
# Ensure stopping and masking the service and/or socket meets local site policy

# Remediation candidate
# systemctl stop squid.service
# OR - If the squid package is required as a dependency:
# systemctl stop squid.service
# systemctl mask squid.service

# TODO: replace the commented/manual steps above with validated bash remediation logic.
