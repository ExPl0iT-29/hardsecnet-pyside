#!/usr/bin/env bash
set -euo pipefail

# CIS Benchmark: CIS Ubuntu Linux 24.04 LTS Benchmark
# Control: 7.1.1 - Ensure permissions on /etc/passwd are configured
# Source Page: 935
# Confidence: 0.96
# Status: review_required

# Audit guidance extracted from the benchmark
# Run the following command to verify /etc/passwd is mode 644 or more restrictive, Uid
# is 0/root and Gid is 0/root:
# # stat -Lc 'Access: (%#a/%A) Uid: ( %u/ %U) Gid: ( %g/ %G)' /etc/passwd
# Access: (0644/-rw-r--r--) Uid: ( 0/ root) Gid: ( 0/ root)

# Remediation candidate
on /etc/passwd:
# chmod u-x,go-wx /etc/passwd
# chown root:root /etc/passwd

# TODO: replace the commented/manual steps above with validated bash remediation logic.
