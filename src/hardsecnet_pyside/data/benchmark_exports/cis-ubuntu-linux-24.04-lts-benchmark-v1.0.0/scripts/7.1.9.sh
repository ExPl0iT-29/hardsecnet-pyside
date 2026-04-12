#!/usr/bin/env bash
set -euo pipefail

# CIS Benchmark: CIS Ubuntu Linux 24.04 LTS Benchmark
# Control: 7.1.9 - Ensure permissions on /etc/shells are configured
# Source Page: 951
# Confidence: 0.96
# Status: review_required

# Audit guidance extracted from the benchmark
# Run the following command to verify /etc/shells is mode 644 or more restrictive, Uid
# is 0/root and Gid is 0/root:
# # stat -Lc 'Access: (%#a/%A) Uid: ( %u/ %U) Gid: ( %g/ %G)' /etc/shells
# Access: (0644/-rw-r--r--) Uid: ( 0/ root) Gid: ( 0/ root)

# Remediation candidate
on /etc/shells:
# chmod u-x,go-wx /etc/shells
# chown root:root /etc/shells

# TODO: replace the commented/manual steps above with validated bash remediation logic.
