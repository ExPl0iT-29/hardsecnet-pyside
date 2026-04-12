#!/usr/bin/env bash
set -euo pipefail

# CIS Benchmark: CIS Ubuntu Linux 24.04 LTS Benchmark
# Control: 6.2.4.6 - Ensure audit configuration files owner is configured
# Source Page: 913
# Confidence: 0.96
# Status: review_required

# Audit guidance extracted from the benchmark
# Run the following command to verify that the audit configuration files are owned by the
# root user:
# # find /etc/audit/ -type f \( -name '*.conf' -o -name '*.rules' \) ! -user
# root
# Nothing should be returned

# Remediation candidate
# find /etc/audit/ -type f \( -name '*.conf' -o -name '*.rules' \) ! -user

# TODO: replace the commented/manual steps above with validated bash remediation logic.
