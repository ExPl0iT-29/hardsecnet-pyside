#!/usr/bin/env bash
set -euo pipefail

# CIS Benchmark: CIS Ubuntu Linux 24.04 LTS Benchmark
# Control: 5.4.1.1 - Ensure password expiration is configured
# Source Page: 678
# Confidence: 0.96
# Status: review_required

# Audit guidance extracted from the benchmark
# Run the following command and verify PASS_MAX_DAYS is set to 365 days or less and
# conforms to local site policy:
# # grep -Pi -- '^\h*PASS_MAX_DAYS\h+\d+\b' /etc/login.defs
# Example output:
# PASS_MAX_DAYS 365
# Run the following command to verify all /etc/shadow passwords PASS_MAX_DAYS:
# -
# is greater than 0 days
# -
# is less than or equal to 365 days
# -
# conforms to local site policy
# # awk -F: '($2~/^\$.+\$/) {if($5 > 365 || $5 < 1)print "User: " $1 "
# PASS_MAX_DAYS: " $5}' /etc/shadow
# Nothing should be returned
# Page 679

# Remediation candidate
Set the PASS_MAX_DAYS parameter to conform to site policy in /etc/login.defs :
Edit /etc/login.defs and set PASS_MAX_DAYS to a value greater than 0 that follows
" $1)}' /etc/shadow

# TODO: replace the commented/manual steps above with validated bash remediation logic.
