#!/usr/bin/env bash
set -euo pipefail

# CIS Benchmark: CIS Ubuntu Linux 24.04 LTS Benchmark
# Control: 5.4.1.6 - Ensure all users last password change date is in the past
# Source Page: 693
# Confidence: 0.96
# Status: review_required

# Audit guidance extracted from the benchmark
# Run the following command and verify nothing is returned
# {
# while IFS= read -r l_user; do
# l_change=$(date -d "$(chage --list $l_user | grep '^Last password
# change' | cut -d: -f2 | grep -v 'never$')" +%s)
# if [[ "$l_change" -gt "$(date +%s)" ]]; then
# echo "User: \"$l_user\" last password change was \"$(chage --list
# $l_user | grep '^Last password change' | cut -d: -f2)\""
# fi
# done < <(awk -F: '$2~/^\$.+\$/{print $1}' /etc/shadow)
# }

# Remediation candidate
# Manual review required
# Convert the remediation guidance below into a validated script action

# TODO: replace the commented/manual steps above with validated bash remediation logic.
