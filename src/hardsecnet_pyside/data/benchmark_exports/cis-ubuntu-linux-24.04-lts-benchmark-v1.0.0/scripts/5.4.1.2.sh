#!/usr/bin/env bash
set -euo pipefail

# CIS Benchmark: CIS Ubuntu Linux 24.04 LTS Benchmark
# Control: 5.4.1.2 - Ensure minimum password days is configured
# Source Page: 682
# Confidence: 0.9000000000000001
# Status: review_required

# Audit guidance extracted from the benchmark
# Run the following command to verify that PASS_MIN_DAYS is set to a value greater than
# 0and follows local site policy:
# # grep -Pi -- '^\h*PASS_MIN_DAYS\h+\d+\b' /etc/login.defs
# Example output:
# PASS_MIN_DAYS 1
# Run the following command to verify all passwords have a PASS_MIN_DAYS greater than
# 0:
# # awk -F: '($2~/^\$.+\$/) {if($4 < 1)print "User: " $1 " PASS_MIN_DAYS: "
# $4}' /etc/shadow
# Nothing should be returned

# Remediation candidate
Edit /etc/login.defs and set PASS_MIN_DAYS to a value greater than 0 that follows
/etc/shadow

# TODO: replace the commented/manual steps above with validated bash remediation logic.
