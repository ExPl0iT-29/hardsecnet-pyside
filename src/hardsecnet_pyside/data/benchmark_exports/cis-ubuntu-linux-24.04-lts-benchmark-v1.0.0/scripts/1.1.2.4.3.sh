#!/usr/bin/env bash
set -euo pipefail

# CIS Benchmark: CIS Ubuntu Linux 24.04 LTS Benchmark
# Control: 1.1.2.4.3 - Ensure nosuid option set on /var partition
# Source Page: 110
# Confidence: 0.96
# Status: review_required

# Audit guidance extracted from the benchmark
# - IF - a separate partition exists for /var, verify that the nosuid option is set.
# Run the following command to verify that the nosuid mount option is set.
# Example:
# # findmnt -kn /var | grep -v nosuid
# Nothing should be returned

# Remediation candidate
# IF - a separate partition exists for /var.
Edit the /etc/fstab file and add nosuid to the fourth field (mounting options) for the

# TODO: replace the commented/manual steps above with validated bash remediation logic.
