#!/usr/bin/env bash
set -euo pipefail

# CIS Benchmark: CIS Ubuntu Linux 24.04 LTS Benchmark
# Control: 7.1.10 - Ensure permissions on /etc/security/opasswd are configured
# Source Page: 953
# Confidence: 0.96
# Status: review_required

# Audit guidance extracted from the benchmark
# Run the following commands to verify /etc/security/opasswd and
# /etc/security/opasswd.old are mode 600 or more restrictive, Uid is 0/root and
# Gid is 0/root if they exist:
# # [ -e "/etc/security/opasswd" ] && stat -Lc '%n Access: (%#a/%A) Uid: (
# %u/ %U) Gid: ( %g/ %G)' /etc/security/opasswd
# /etc/security/opasswd Access: (0600/-rw-------) Uid: ( 0/ root) Gid: ( 0/
# root)
# -OR-
# Nothing is returned
# # [ -e "/etc/security/opasswd.old" ] && stat -Lc '%n Access: (%#a/%A) Uid:
# ( %u/ %U) Gid: ( %g/ %G)' /etc/security/opasswd.old
# /etc/security/opasswd.old Access: (0600/-rw-------) Uid: ( 0/ root) Gid: (
# 0/ root)
# -OR-
# Nothing is returned
# Page 953

# Remediation candidate
on /etc/security/opasswd and /etc/security/opasswd.old is they exist:
# [ -e "/etc/security/opasswd" ] && chmod u-x,go-rwx /etc/security/opasswd
# [ -e "/etc/security/opasswd" ] && chown root:root /etc/security/opasswd
# [ -e "/etc/security/opasswd.old" ] && chmod u-x,go-rwx
/etc/security/opasswd.old
# [ -e "/etc/security/opasswd.old" ] && chown root:root
/etc/security/opasswd.old

# TODO: replace the commented/manual steps above with validated bash remediation logic.
