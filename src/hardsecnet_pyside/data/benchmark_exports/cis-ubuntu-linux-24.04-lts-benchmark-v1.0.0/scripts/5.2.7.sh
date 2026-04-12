#!/usr/bin/env bash
set -euo pipefail

# CIS Benchmark: CIS Ubuntu Linux 24.04 LTS Benchmark
# Control: 5.2.7 - Ensure access to the su command is restricted
# Source Page: 595
# Confidence: 0.96
# Status: review_required

# Audit guidance extracted from the benchmark
# Run the following command:
# # grep -Pi
# '^\h*auth\h+(?:required|requisite)\h+pam_wheel\.so\h+(?:[^#\n\r]+\h+)?((?!\2)
# (use_uid\b|group=\H+\b))\h+(?:[^#\n\r]+\h+)?((?!\1)(use_uid\b|group=\H+\b))(\
# h+.*)?$' /etc/pam.d/su
# Verify the output matches:
# auth required pam_wheel.so use_uid group=<group_name>
# Run the following command and verify that the group specified in <group_name>
# contains no users:
# # grep <group_name> /etc/group
# Verify the output does not contain any users in the relevant group:
# <group_name>:x:<GID>:
# Page 595

# Remediation candidate
Add the following line to the /etc/pam.d/su file, specifying the empty group:

# TODO: replace the commented/manual steps above with validated bash remediation logic.
