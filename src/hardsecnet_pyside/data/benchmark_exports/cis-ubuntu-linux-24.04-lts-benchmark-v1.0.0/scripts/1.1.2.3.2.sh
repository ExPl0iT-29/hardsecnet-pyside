#!/usr/bin/env bash
set -euo pipefail

# CIS Benchmark: CIS Ubuntu Linux 24.04 LTS Benchmark
# Control: 1.1.2.3.2 - Ensure nodev option set on /home partition
# Source Page: 100
# Confidence: 0.96
# Status: review_required

# Audit guidance extracted from the benchmark
# - IF - a separate partition exists for /home, verify that the nodev option is set.
# Run the following command to verify that the nodev mount option is set.
# Example:
# # findmnt -kn /home | grep -v nodev
# Nothing should be returned

# Remediation candidate
# IF - a separate partition exists for /home.
Edit the /etc/fstab file and add nodev to the fourth field (mounting options) for the

# TODO: replace the commented/manual steps above with validated bash remediation logic.
