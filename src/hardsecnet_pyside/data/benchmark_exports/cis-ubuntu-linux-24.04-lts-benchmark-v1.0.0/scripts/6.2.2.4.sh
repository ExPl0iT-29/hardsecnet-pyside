#!/usr/bin/env bash
set -euo pipefail

# CIS Benchmark: CIS Ubuntu Linux 24.04 LTS Benchmark
# Control: 6.2.2.4 - Ensure system warns when audit logs are low on space
# Source Page: 816
# Confidence: 0.96
# Status: review_required

# Audit guidance extracted from the benchmark
# Run the following command and verify the space_left_action is set to email, exec,
# single, or halt:
# # grep -P -- '^\h*space_left_action\h*=\h*(email|exec|single|halt)\b'
# /etc/audit/auditd.conf
# Verify the output is email, exec, single, or halt
# Example output
# space_left_action = email
# Run the following command and verify the admin_space_left_action is set to single
# - OR - halt:
# # grep -P -- '^\h*admin_space_left_action\h*=\h*(single|halt)\b'
# /etc/audit/auditd.conf
# Verify the output is single or halt
# Example output:
# admin_space_left_action = single
# Note: A Mail Transfer Agent (MTA) must be installed and configured properly to set
# space_left_action = email

# Remediation candidate
Set the space_left_action parameter in /etc/audit/auditd.conf to email, exec,
Set the admin_space_left_action parameter in /etc/audit/auditd.conf to

# TODO: replace the commented/manual steps above with validated bash remediation logic.
