#!/usr/bin/env bash
set -euo pipefail

# CIS Benchmark: CIS Ubuntu Linux 24.04 LTS Benchmark
# Control: 1.6.6 - Ensure access to /etc/issue.net is configured
# Source Page: 195
# Confidence: 0.96
# Status: review_required

# Audit guidance extracted from the benchmark
# Run the following command and verify Access is 644 or more restrictive and Uid and
# Gid are both 0/root:
# # stat -Lc 'Access: (%#a/%A) Uid: ( %u/ %U) Gid: { %g/ %G)' /etc/issue.net
# Access: (0644/-rw-r--r--) Uid: ( 0/ root) Gid: ( 0/ root)

# Remediation candidate
Run the following commands to set mode, owner, and group on /etc/issue.net:
# chown root:root $(readlink -e /etc/issue.net)
# chmod u-x,go-wx $(readlink -e /etc/issue.net)

# TODO: replace the commented/manual steps above with validated bash remediation logic.
