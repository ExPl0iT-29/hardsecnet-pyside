#!/usr/bin/env bash
set -euo pipefail

# CIS Benchmark: CIS Ubuntu Linux 24.04 LTS Benchmark
# Control: 6.2.3.20 - Ensure the audit configuration is immutable
# Source Page: 895
# Confidence: 0.96
# Status: review_required

# Audit guidance extracted from the benchmark
# Run the following command and verify output matches:
# # grep -Ph -- '^\h*-e\h+2\b' /etc/audit/rules.d/*.rules | tail -1
# -e 2

# Remediation candidate
Edit or create the file /etc/audit/rules.d/99-finalize.rules and add the line -e
# printf '\n%s' "-e 2" >> /etc/audit/rules.d/99-finalize.rules
# if [[ $(auditctl -s | grep "enabled") =~ "2" ]]; then printf "Reboot

# TODO: replace the commented/manual steps above with validated bash remediation logic.
