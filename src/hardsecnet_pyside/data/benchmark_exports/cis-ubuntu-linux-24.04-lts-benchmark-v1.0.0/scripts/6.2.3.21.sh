#!/usr/bin/env bash
set -euo pipefail

# CIS Benchmark: CIS Ubuntu Linux 24.04 LTS Benchmark
# Control: 6.2.3.21 - Ensure the running and on disk configuration is the same
# Source Page: 897
# Confidence: 0.9000000000000001
# Status: review_required

# Audit guidance extracted from the benchmark
# Merged rule sets
# Ensure that all rules in /etc/audit/rules.d have been merged into
# /etc/audit/audit.rules:
# # augenrules --check
# /usr/sbin/augenrules: No change
# Should there be any drift, run augenrules --load to merge and load all rules.

# Remediation candidate
if [[ $(auditctl -s | grep "enabled") =~ "2" ]]; then echo "Reboot required

# TODO: replace the commented/manual steps above with validated bash remediation logic.
