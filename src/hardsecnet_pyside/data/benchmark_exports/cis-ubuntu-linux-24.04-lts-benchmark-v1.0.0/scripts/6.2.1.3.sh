#!/usr/bin/env bash
set -euo pipefail

# CIS Benchmark: CIS Ubuntu Linux 24.04 LTS Benchmark
# Control: 6.2.1.3 - Ensure auditing for processes that start prior to auditd is enabled
# Source Page: 804
# Confidence: 0.96
# Status: review_required

# Audit guidance extracted from the benchmark
# Run the following command:
# # find /boot -type f -name 'grub.cfg' -exec grep -Ph -- '^\h*linux' {} + |
# grep -v 'audit=1'
# Nothing should be returned.

# Remediation candidate
Edit /etc/default/grub and add audit=1 to GRUB_CMDLINE_LINUX:

# TODO: replace the commented/manual steps above with validated bash remediation logic.
