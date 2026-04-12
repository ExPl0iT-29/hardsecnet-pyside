#!/usr/bin/env bash
set -euo pipefail

# CIS Benchmark: CIS Ubuntu Linux 24.04 LTS Benchmark
# Control: 5.3.3.1.3 - Ensure password failed attempts lockout includes root account
# Source Page: 621
# Confidence: 0.96
# Status: review_required

# Audit guidance extracted from the benchmark
# Run the following command to verify that even_deny_root and/or root_unlock_time
# is enabled:
# # grep -Pi -- '^\h*(even_deny_root|root_unlock_time\h*=\h*\d+)\b'
# /etc/security/faillock.conf
# Example output:
# even_deny_root
# --AND/OR--
# root_unlock_time = 60
# Run the following command to verify that - IF - root_unlock_time is set, it is set to 60
# (One minute) or more:
# # grep -Pi -- '^\h*root_unlock_time\h*=\h*([1-9]|[1-5][0-9])\b'
# /etc/security/faillock.conf
# Nothing should be returned
# Run the following command to check the pam_faillock.so module for the
# root_unlock_time argument. Verify -IF- root_unlock_time is set, it is set to 60 (One
# minute) or more:
# # grep -Pi --
# '^\h*auth\h+([^#\n\r]+\h+)pam_faillock\.so\h+([^#\n\r]+\h+)?root_unlock_time\
# h*=\h*([1-9]|[1-5][0-9])\b' /etc/pam.d/common-auth
# Nothing should be returned

# Remediation candidate
Edit /etc/security/faillock.conf:

# TODO: replace the commented/manual steps above with validated bash remediation logic.
