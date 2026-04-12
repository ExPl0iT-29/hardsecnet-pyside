#!/usr/bin/env bash
set -euo pipefail

# CIS Benchmark: CIS Ubuntu Linux 24.04 LTS Benchmark
# Control: 7.1.3 - Ensure permissions on /etc/group are configured
# Source Page: 939
# Confidence: 0.96
# Status: review_required

# Audit guidance extracted from the benchmark
# Run the following command to verify /etc/group is mode 644 or more restrictive, Uid
# is 0/root and Gid is 0/root:
# # stat -Lc 'Access: (%#a/%A) Uid: ( %u/ %U) Gid: ( %g/ %G)' /etc/group
# Access: (0644/-rw-r--r--) Uid: ( 0/ root) Gid: ( 0/ root)

# Remediation candidate
on /etc/group:
# chmod u-x,go-wx /etc/group
# chown root:root /etc/group

# TODO: replace the commented/manual steps above with validated bash remediation logic.
