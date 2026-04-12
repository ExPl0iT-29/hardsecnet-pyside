#!/usr/bin/env bash
set -euo pipefail

# CIS Benchmark: CIS Ubuntu Linux 24.04 LTS Benchmark
# Control: 1.1.2.2.1 - Ensure /dev/shm is a separate partition
# Source Page: 88
# Confidence: 0.96
# Status: review_required

# Audit guidance extracted from the benchmark
# -IF- /dev/shm is to be used on the system, run the following command and verify the
# output shows that /dev/shm is mounted. Particular requirements pertaining to mount
# options are covered in ensuing sections.
# # findmnt -kn /dev/shm
# Example output:
# /dev/shm tmpfs tmpfs rw,nosuid,nodev,noexec,relatime,seclabel
# Page 88

# Remediation candidate
modify /etc/fstab.

# TODO: replace the commented/manual steps above with validated bash remediation logic.
