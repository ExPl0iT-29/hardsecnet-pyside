#!/usr/bin/env bash
set -euo pipefail

# CIS Benchmark: CIS Ubuntu Linux 24.04 LTS Benchmark
# Control: 2.1.1 - Ensure autofs services are not in use
# Source Page: 229
# Confidence: 0.96
# Status: review_required

# Audit guidance extracted from the benchmark
# As a preference autofs should not be installed unless other packages depend on it.
# Run the following command to verify autofs is not installed:
# # dpkg-query -s autofs &>/dev/null && echo "autofs is installed"
# Nothing should be returned.
# - OR -
# - IF - the package is required for dependencies:
# Run the following command to verify autofs.service is not enabled:
# # systemctl is-enabled autofs.service 2>/dev/null | grep 'enabled'
# Nothing should be returned.
# Run the following command to verify the autofs.service is not active:
# # systemctl is-active autofs.service 2>/dev/null | grep '^active'
# Nothing should be returned.
# Note: If the package is required for a dependency
# -
# Ensure the dependent package is approved by local site policy
# -
# Ensure stopping and masking the service and/or socket meets local site policy

# Remediation candidate
# systemctl stop autofs.service
# OR -
# IF - the autofs package is required as a dependency:
# systemctl stop autofs.service
# systemctl mask autofs.service

# TODO: replace the commented/manual steps above with validated bash remediation logic.
