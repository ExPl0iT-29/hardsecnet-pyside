#!/usr/bin/env bash
set -euo pipefail

# CIS Benchmark: CIS Ubuntu Linux 24.04 LTS Benchmark
# Control: 2.3.3.3 - Ensure chrony is enabled and running
# Source Page: 326
# Confidence: 0.96
# Status: review_required

# Audit guidance extracted from the benchmark
# - IF - chrony is in use on the system, run the following commands:
# Run the following command to verify that the chrony service is enabled:
# # systemctl is-enabled chrony.service
# enabled
# Run the following command to verify that the chrony service is active:
# # systemctl is-active chrony.service
# active
# Page 326

# Remediation candidate
# IF - chrony is in use on the system, run the following commands:
# systemctl unmask chrony.service
# systemctl --now enable chrony.service
# OR -

# TODO: replace the commented/manual steps above with validated bash remediation logic.
