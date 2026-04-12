#!/usr/bin/env bash
set -euo pipefail

# CIS Benchmark: CIS Ubuntu Linux 24.04 LTS Benchmark
# Control: 1.1.2.6.2 - Ensure nodev option set on /var/log partition
# Source Page: 124
# Confidence: 0.96
# Status: review_required

# Audit guidance extracted from the benchmark
# - IF - a separate partition exists for /var/log, verify that the nodev option is set.
# Run the following command to verify that the nodev mount option is set.
# Example:
# # findmnt -kn /var/log | grep -v nodev
# Nothing should be returned

# Remediation candidate
# IF - a separate partition exists for /var/log.
Edit the /etc/fstab file and add nodev to the fourth field (mounting options) for the

# TODO: replace the commented/manual steps above with validated bash remediation logic.
