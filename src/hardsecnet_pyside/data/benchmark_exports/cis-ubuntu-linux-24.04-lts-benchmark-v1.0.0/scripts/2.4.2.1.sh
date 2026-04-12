#!/usr/bin/env bash
set -euo pipefail

# CIS Benchmark: CIS Ubuntu Linux 24.04 LTS Benchmark
# Control: 2.4.2.1 - Ensure at is restricted to authorized users
# Source Page: 349
# Confidence: 0.96
# Status: review_required

# Audit guidance extracted from the benchmark
# - IF - at is installed on the system:
# Run the following command to verify /etc/at.allow:
# -
# Exists
# -
# Is mode 0640 or more restrictive
# -
# Is owned by the user root
# -
# Is group owned by the group daemon or group root
# # stat -Lc 'Access: (%a/%A) Owner: (%U) Group: (%G)' /etc/at.allow
# Access: (640/-rw-r-----) Owner: (root) Group: (daemon)
# -OR-
# Access: (640/-rw-r-----) Owner: (root) Group: (root)
# Verify mode is 640 or more restrictive, owner is root, and group is daemon or root
# Run the following command to verify at.deny doesn't exist, -OR- is:
# -
# Mode 0640 or more restrictive
# -
# Owned by the user root
# -
# Group owned by the group daemon or group root
# # [ -e "/etc/at.deny" ] && stat -Lc 'Access: (%a/%A) Owner: (%U) Group: (%G)'
# /etc/at.deny
# Access: (640/-rw-r-----) Owner: (root) Group: (daemon)
# -OR-
# Access: (640/-rw-r-----) Owner: (root) Group: (root)
# -OR-
# Nothing is returned
# If a value is returned, verify mode is 640 or more restrictive, owner is root, and group is
# daemon or root
# Page 350

# Remediation candidate
# IF - at is installed on the system:
/etc/at.allow:
- IF - /etc/at.deny exists:
grep -Pq -- '^daemon\b' /etc/group && l_group="daemon" || l_group="root"
[ ! -e "/etc/at.allow" ] && touch /etc/at.allow
chown root:"$l_group" /etc/at.allow
chmod u-x,g-wx,o-rwx /etc/at.allow
[ -e "/etc/at.deny" ] && chown root:"$l_group" /etc/at.deny
[ -e "/etc/at.deny" ] && chmod u-x,g-wx,o-rwx /etc/at.deny

# TODO: replace the commented/manual steps above with validated bash remediation logic.
