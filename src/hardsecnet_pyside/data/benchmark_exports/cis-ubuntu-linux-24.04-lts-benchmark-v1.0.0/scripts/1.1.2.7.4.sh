#!/usr/bin/env bash
set -euo pipefail

# CIS Benchmark: CIS Ubuntu Linux 24.04 LTS Benchmark
# Control: 1.1.2.7.4 - Ensure noexec option set on /var/log/audit partition
# Source Page: 137
# Confidence: 0.96
# Status: review_required

# Audit guidance extracted from the benchmark
# - IF - a separate partition exists for /var/log/audit, verify that the noexec option is
# set.
# Run the following command to verify that the noexec mount option is set.
# Example:
# # findmnt -kn /var/log/audit | grep -v noexec
# Nothing should be returned

# Remediation candidate
# IF - a separate partition exists for /var/log/audit.
Edit the /etc/fstab file and add noexec to the fourth field (mounting options) for the

# TODO: replace the commented/manual steps above with validated bash remediation logic.
