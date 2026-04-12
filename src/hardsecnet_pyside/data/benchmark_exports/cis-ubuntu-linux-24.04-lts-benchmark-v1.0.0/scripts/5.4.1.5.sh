#!/usr/bin/env bash
set -euo pipefail

# CIS Benchmark: CIS Ubuntu Linux 24.04 LTS Benchmark
# Control: 5.4.1.5 - Ensure inactive password lock is configured
# Source Page: 690
# Confidence: 0.96
# Status: review_required

# Audit guidance extracted from the benchmark
# Run the following command and verify INACTIVE conforms to site policy (no more than
# 45 days):
# # useradd -D | grep INACTIVE
# INACTIVE=45
# Verify all users with a password have Password inactive no more than 45 days after
# password expires
# Verify all users with a password have Password inactive no more than 45 days after
# password expires: Run the following command and Review list of users and INACTIVE
# to verify that all users INACTIVE conforms to site policy (no more than 45 days):
# # awk -F: '($2~/^\$.+\$/) {if($7 > 45 || $7 < 0)print "User: " $1 " INACTIVE:
# " $7}' /etc/shadow
# Nothing should be returned
# Page 690

# Remediation candidate
" $1)}' /etc/shadow

# TODO: replace the commented/manual steps above with validated bash remediation logic.
