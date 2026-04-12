#!/usr/bin/env bash
set -euo pipefail

# CIS Benchmark: CIS Ubuntu Linux 24.04 LTS Benchmark
# Control: 6.2.4.9 - Ensure audit tools owner is configured
# Source Page: 920
# Confidence: 0.96
# Status: review_required

# Audit guidance extracted from the benchmark
# Run the following command to verify the audit tools are owned by the root user:
# # stat -Lc "%n %U" /sbin/auditctl /sbin/aureport /sbin/ausearch /sbin/autrace
# /sbin/auditd /sbin/augenrules | awk '$2 != "root" {print}'
# Nothing should be returned

# Remediation candidate
# chown root /sbin/auditctl /sbin/aureport /sbin/ausearch /sbin/autrace

# TODO: replace the commented/manual steps above with validated bash remediation logic.
