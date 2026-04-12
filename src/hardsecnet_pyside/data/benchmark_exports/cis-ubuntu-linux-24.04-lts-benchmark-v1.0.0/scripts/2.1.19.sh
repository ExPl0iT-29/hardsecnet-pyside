#!/usr/bin/env bash
set -euo pipefail

# CIS Benchmark: CIS Ubuntu Linux 24.04 LTS Benchmark
# Control: 2.1.19 - Ensure xinetd services are not in use
# Source Page: 281
# Confidence: 0.96
# Status: review_required

# Audit guidance extracted from the benchmark
# Run the following command to verify the xinetd package is not installed:
# # dpkg-query -s xinetd &>/dev/null && echo "xinetd is installed"
# Nothing should be returned.
# -OR-
# -IF- the xinetd package is required as a dependency:
# Run the following command to verify xinetd.service is not enabled:
# # systemctl is-enabled xinetd.service 2>/dev/null | grep 'enabled'
# Nothing should be returned
# Run the following command to verify xinetd.service is not active:
# # systemctl is-active xinetd.service 2>/dev/null | grep '^active'
# Nothing should be returned
# Note: If the package is required for a dependency
# -
# Ensure the dependent package is approved by local site policy
# -
# Ensure stopping and masking the service and/or socket meets local site policy

# Remediation candidate
# systemctl stop xinetd.service
# OR-
# IF- the xinetd package is required as a dependency:
# systemctl stop xinetd.service
# systemctl mask xinetd.service

# TODO: replace the commented/manual steps above with validated bash remediation logic.
