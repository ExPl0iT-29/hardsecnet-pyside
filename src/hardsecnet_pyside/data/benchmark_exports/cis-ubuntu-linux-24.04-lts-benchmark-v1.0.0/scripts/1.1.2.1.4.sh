#!/usr/bin/env bash
set -euo pipefail

# CIS Benchmark: CIS Ubuntu Linux 24.04 LTS Benchmark
# Control: 1.1.2.1.4 - Ensure noexec option set on /tmp partition
# Source Page: 85
# Confidence: 0.96
# Status: review_required

# Audit guidance extracted from the benchmark
# - IF - a separate partition exists for /tmp, verify that the noexec option is set.
# Run the following command to verify that the noexec mount option is set.
# Example:
# # findmnt -kn /tmp | grep -v noexec
# Nothing should be returned

# Remediation candidate
# IF - a separate partition exists for /tmp.
Edit the /etc/fstab file and add noexec to the fourth field (mounting options) for the

# TODO: replace the commented/manual steps above with validated bash remediation logic.
