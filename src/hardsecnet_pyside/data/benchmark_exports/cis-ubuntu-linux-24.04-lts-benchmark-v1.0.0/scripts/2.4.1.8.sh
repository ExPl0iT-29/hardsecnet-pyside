#!/usr/bin/env bash
set -euo pipefail

# CIS Benchmark: CIS Ubuntu Linux 24.04 LTS Benchmark
# Control: 2.4.1.8 - Ensure crontab is restricted to authorized users
# Source Page: 344
# Confidence: 0.96
# Status: review_required

# Audit guidance extracted from the benchmark
# - IF - cron is installed on the system:
# Run the following command to verify /etc/cron.allow:
# -
# Exists
# -
# Is mode 0640 or more restrictive
# -
# Is owned by the user root
# -
# Is group owned by the group root - OR - the group crontab
# # stat -Lc 'Access: (%a/%A) Owner: (%U) Group: (%G)' /etc/cron.allow
# Verify the returned value is:
# Access: (640/-rw-r-----) Owner: (root) Group: (root)
# - OR -
# Access: (640/-rw-r-----) Owner: (root) Group: (crontab)
# Run the following command to verify either cron.deny doesn't exist or is:
# -
# Mode 0640 or more restrictive
# -
# Owned by the user root
# -
# Is group owned by the group root - OR - the group crontab
# # [ -e "/etc/cron.deny" ] && stat -Lc 'Access: (%a/%A) Owner: (%U) Group:
# (%G)' /etc/cron.deny
# Verify either nothing is returned - OR - returned value is one of the following:
# Access: (640/-rw-r-----) Owner: (root) Group: (root)
# - OR -
# Access: (640/-rw-r-----) Owner: (root) Group: (crontab)
# Note: On systems where cron is configured to use the group crontab, if the group
# crontab is not set as the owner of cron.allow, then cron will deny access to all users
# and you will see an error similar to:
# You (<USERNAME>) are not allowed to use this program (crontab)
# See crontab(1) for more information
# Page 345

# Remediation candidate
# IF - cron is installed on the system:
Create /etc/cron.allow if it doesn't exist
[ ! -e "/etc/cron.deny" ] && touch /etc/cron.allow
chmod u-x,g-wx,o-rwx /etc/cron.allow
if grep -Pq -- '^\h*crontab\:' /etc/group; then
chown root:crontab /etc/cron.allow
chown root:root /etc/cron.allow
- IF - /etc/cron.deny exists, run the following script to:
if [ -e "/etc/cron.deny" ]; then
chmod u-x,g-wx,o-rwx /etc/cron.deny
if grep -Pq -- '^\h*crontab\:' /etc/group; then
chown root:crontab /etc/cron.deny
chown root:root /etc/cron.deny

# TODO: replace the commented/manual steps above with validated bash remediation logic.
