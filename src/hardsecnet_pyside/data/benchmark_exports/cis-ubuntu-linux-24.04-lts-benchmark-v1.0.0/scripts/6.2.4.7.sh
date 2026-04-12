#!/usr/bin/env bash
set -euo pipefail

# CIS Benchmark: CIS Ubuntu Linux 24.04 LTS Benchmark
# Control: 6.2.4.7 - Ensure audit configuration files group owner is configured
# Source Page: 915
# Confidence: 0.96
# Status: review_required

# Audit guidance extracted from the benchmark
# Run the following command to verify that the audit configuration files are owned by the
# group root:
# # find /etc/audit/ -type f \( -name '*.conf' -o -name '*.rules' \) ! -group
# root
# Nothing should be returned

# Remediation candidate
# find /etc/audit/ -type f \( -name '*.conf' -o -name '*.rules' \) ! -group

# TODO: replace the commented/manual steps above with validated bash remediation logic.
