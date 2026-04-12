#!/usr/bin/env bash
set -euo pipefail

# CIS Benchmark: CIS Ubuntu Linux 24.04 LTS Benchmark
# Control: 6.2.3.6 - Ensure use of privileged commands are collected
# Source Page: 839
# Confidence: 0.96
# Status: review_required

# Audit guidance extracted from the benchmark
# On disk configuration
# Run the following script to check on disk rules:
# #!/usr/bin/env bash
# {
# for PARTITION in $(findmnt -n -l -k -it $(awk '/nodev/ { print $2 }'
# /proc/filesystems | paste -sd,) | grep -Pv "noexec|nosuid" | awk '{print
# $1}'); do
# for PRIVILEGED in $(find "${PARTITION}" -xdev -perm /6000 -type f); do
# grep -qr "${PRIVILEGED}" /etc/audit/rules.d && printf "OK:
# '${PRIVILEGED}' found in auditing rules.\n" || printf "Warning:
# '${PRIVILEGED}' not found in on disk configuration.\n"
# done
# done
# }
# Verify that all output is OK.
# Running configuration
# Run the following script to check loaded rules:
# #!/usr/bin/env bash
# {
# RUNNING=$(auditctl -l)
# [ -n "${RUNNING}" ] && for PARTITION in $(findmnt -n -l -k -it $(awk
# '/nodev/ { print $2 }' /proc/filesystems | paste -sd,) | grep -Pv
# "noexec|nosuid" | awk '{print $1}'); do
# for PRIVILEGED in $(find "${PARTITION}" -xdev -perm /6000 -type f); do
# printf -- "${RUNNING}" | grep -q "${PRIVILEGED}" && printf "OK:
# '${PRIVILEGED}' found in auditing rules.\n" || printf "Warning:
# '${PRIVILEGED}' not found in running configuration.\n"
# done
# done \
# || printf "ERROR: Variable 'RUNNING' is unset.\n"
# }
# Verify that all output is OK.
# Special mount points
# If there are any special mount points that are not visible by default from findmnt as per
# the above audit, said file systems would have to be manually audited.
# Page 840

# Remediation candidate
Edit or create a file in the /etc/audit/rules.d/ directory, ending in .rules extension,
UID_MIN=$(awk '/^\s*UID_MIN/{print $2}' /etc/login.defs)
AUDIT_RULE_FILE="/etc/audit/rules.d/50-privileged.rules"
# v UID_MIN=${UID_MIN} '{print "-a always,exit -F path=" $1 " -F perm=x -F
# if [[ $(auditctl -s | grep "enabled") =~ "2" ]]; then printf "Reboot

# TODO: replace the commented/manual steps above with validated bash remediation logic.
