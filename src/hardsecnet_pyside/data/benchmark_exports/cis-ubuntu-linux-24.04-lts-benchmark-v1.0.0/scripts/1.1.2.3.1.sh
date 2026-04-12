#!/usr/bin/env bash
set -euo pipefail

# CIS Benchmark: CIS Ubuntu Linux 24.04 LTS Benchmark
# Control: 1.1.2.3.1 - Ensure separate partition exists for /home
# Source Page: 97
# Confidence: 0.96
# Status: review_required

# Audit guidance extracted from the benchmark
# Run the following command and verify output shows /home is mounted:
# # findmnt -kn /home
# /home /dev/sdb ext4 rw,nosuid,nodev,noexec,relatime,seclabel

# Remediation candidate
/etc/fstab as appropriate.

# TODO: replace the commented/manual steps above with validated bash remediation logic.
