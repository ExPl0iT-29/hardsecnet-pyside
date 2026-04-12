#!/usr/bin/env bash
set -euo pipefail

# CIS Benchmark: CIS Ubuntu Linux 24.04 LTS Benchmark
# Control: 1.1.2.2.3 - Ensure nosuid option set on /dev/shm partition
# Source Page: 92
# Confidence: 0.96
# Status: review_required

# Audit guidance extracted from the benchmark
# - IF - a separate partition exists for /dev/shm, verify that the nosuid option is set.
# # findmnt -kn /dev/shm | grep -v 'nosuid'
# Nothing should be returned

# Remediation candidate
# IF - a separate partition exists for /dev/shm.
Edit the /etc/fstab file and add nosuid to the fourth field (mounting options) for the

# TODO: replace the commented/manual steps above with validated bash remediation logic.
