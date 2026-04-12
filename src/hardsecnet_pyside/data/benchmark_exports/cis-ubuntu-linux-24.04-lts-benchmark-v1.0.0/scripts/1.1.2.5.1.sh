#!/usr/bin/env bash
set -euo pipefail

# CIS Benchmark: CIS Ubuntu Linux 24.04 LTS Benchmark
# Control: 1.1.2.5.1 - Ensure separate partition exists for /var/tmp
# Source Page: 113
# Confidence: 0.96
# Status: review_required

# Audit guidance extracted from the benchmark
# Run the following command and verify output shows /var/tmp is mounted.
# Example:
# # findmnt -kn /var/tmp
# /var/tmp /dev/sdb ext4 rw,nosuid,nodev,noexec,relatime,seclabel

# Remediation candidate
/etc/fstab as appropriate.

# TODO: replace the commented/manual steps above with validated bash remediation logic.
