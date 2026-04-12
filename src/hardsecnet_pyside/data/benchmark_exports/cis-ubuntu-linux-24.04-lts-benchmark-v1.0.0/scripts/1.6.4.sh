#!/usr/bin/env bash
set -euo pipefail

# CIS Benchmark: CIS Ubuntu Linux 24.04 LTS Benchmark
# Control: 1.6.4 - Ensure access to /etc/motd is configured
# Source Page: 191
# Confidence: 0.96
# Status: review_required

# Audit guidance extracted from the benchmark
# Run the following command and verify that if /etc/motd exists, Access is 644 or more
# restrictive, Uid and Gid are both 0/root:
# # [ -e /etc/motd ] && stat -Lc 'Access: (%#a/%A) Uid: ( %u/ %U) Gid: { %g/
# %G)' /etc/motd
# Access: (0644/-rw-r--r--) Uid: ( 0/ root) Gid: ( 0/ root)
# -- OR --
# Nothing is returned

# Remediation candidate
Run the following commands to set mode, owner, and group on /etc/motd:
# chown root:root $(readlink -e /etc/motd)
# chmod u-x,go-wx $(readlink -e /etc/motd)
# OR -
Run the following command to remove the /etc/motd file:
# rm /etc/motd

# TODO: replace the commented/manual steps above with validated bash remediation logic.
