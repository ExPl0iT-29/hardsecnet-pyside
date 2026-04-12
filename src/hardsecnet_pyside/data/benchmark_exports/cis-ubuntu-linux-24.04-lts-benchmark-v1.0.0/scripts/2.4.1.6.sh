#!/usr/bin/env bash
set -euo pipefail

# CIS Benchmark: CIS Ubuntu Linux 24.04 LTS Benchmark
# Control: 2.4.1.6 - Ensure permissions on /etc/cron.monthly are configured
# Source Page: 340
# Confidence: 0.96
# Status: review_required

# Audit guidance extracted from the benchmark
# - IF - cron is installed on the system:
# Run the following command and verify Uid and Gid are both 0/root and Access does
# not grant permissions to group or other:
# # stat -Lc 'Access: (%a/%A) Uid: ( %u/ %U) Gid: ( %g/ %G)' /etc/cron.monthly/
# Access: (700/drwx------) Uid: ( 0/ root) Gid: ( 0/ root)

# Remediation candidate
# IF - cron is installed on the system:
/etc/cron.monthly directory:
# chown root:root /etc/cron.monthly/
# chmod og-rwx /etc/cron.monthly/

# TODO: replace the commented/manual steps above with validated bash remediation logic.
