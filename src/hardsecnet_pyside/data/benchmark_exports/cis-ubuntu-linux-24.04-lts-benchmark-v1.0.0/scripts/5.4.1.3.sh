#!/usr/bin/env bash
set -euo pipefail

# CIS Benchmark: CIS Ubuntu Linux 24.04 LTS Benchmark
# Control: 5.4.1.3 - Ensure password expiration warning days is configured
# Source Page: 685
# Confidence: 0.96
# Status: review_required

# Audit guidance extracted from the benchmark
# Run the following command and verify PASS_WARN_AGE is 7 or more and follows local
# site policy:
# # grep -Pi -- '^\h*PASS_WARN_AGE\h+\d+\b' /etc/login.defs
# Example output:
# PASS_WARN_AGE 7
# Run the following command to verify all passwords have a PASS_WARN_AGE of 7 or
# more:
# # awk -F: '($2~/^\$.+\$/) {if($6 < 7)print "User: " $1 " PASS_WARN_AGE: "
# $6}' /etc/shadow
# Nothing should be returned
# Page 685

# Remediation candidate
Edit /etc/login.defs and set PASS_WARN_AGE to a value of 7 or more that follows
/etc/shadow

# TODO: replace the commented/manual steps above with validated bash remediation logic.
