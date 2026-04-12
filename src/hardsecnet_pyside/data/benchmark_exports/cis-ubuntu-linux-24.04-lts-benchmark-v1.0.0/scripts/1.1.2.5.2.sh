#!/usr/bin/env bash
set -euo pipefail

# CIS Benchmark: CIS Ubuntu Linux 24.04 LTS Benchmark
# Control: 1.1.2.5.2 - Ensure nodev option set on /var/tmp partition
# Source Page: 115
# Confidence: 0.96
# Status: review_required

# Audit guidance extracted from the benchmark
# - IF - a separate partition exists for /var/tmp, verify that the nodev option is set.
# Run the following command to verify that the nodev mount option is set.
# Example:
# # findmnt -kn /var/tmp | grep -v nodev
# Nothing should be returned

# Remediation candidate
# IF - a separate partition exists for /var/tmp.
Edit the /etc/fstab file and add nodev to the fourth field (mounting options) for the

# TODO: replace the commented/manual steps above with validated bash remediation logic.
