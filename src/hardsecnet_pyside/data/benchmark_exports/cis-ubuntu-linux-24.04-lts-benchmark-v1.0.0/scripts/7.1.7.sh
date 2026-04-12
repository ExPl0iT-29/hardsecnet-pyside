#!/usr/bin/env bash
set -euo pipefail

# CIS Benchmark: CIS Ubuntu Linux 24.04 LTS Benchmark
# Control: 7.1.7 - Ensure permissions on /etc/gshadow are configured
# Source Page: 947
# Confidence: 0.96
# Status: review_required

# Audit guidance extracted from the benchmark
# Run the following command to verify /etc/gshadow is mode 640 or more restrictive,
# Uid is 0/root and Gid is 0/root or `{GID}/shadow:
# # stat -Lc 'Access: (%#a/%A) Uid: ( %u/ %U) Gid: ( %g/ %G)' /etc/gshadow
# Example:
# Access: (0640/-rw-r-----) Uid: ( 0/ root) Gid: ( 42/ shadow)

# Remediation candidate
Run one of the following commands to set ownership of /etc/gshadow to root and
# chown root:shadow /etc/gshadow
# OR-
# chown root:root /etc/gshadow
Run the following command to remove excess permissions form /etc/gshadow:
# chmod u-x,g-wx,o-rwx /etc/gshadow

# TODO: replace the commented/manual steps above with validated bash remediation logic.
