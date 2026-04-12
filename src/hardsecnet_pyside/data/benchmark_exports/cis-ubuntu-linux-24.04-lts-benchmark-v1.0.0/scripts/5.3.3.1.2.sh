#!/usr/bin/env bash
set -euo pipefail

# CIS Benchmark: CIS Ubuntu Linux 24.04 LTS Benchmark
# Control: 5.3.3.1.2 - Ensure password unlock time is configured
# Source Page: 618
# Confidence: 0.96
# Status: review_required

# Audit guidance extracted from the benchmark
# Run the following command to verify that the time in seconds before the account is
# unlocked is either 0 (never) or 900 (15 minutes) or more and meets local site policy:
# # grep -Pi -- '^\h*unlock_time\h*=\h*(0|9[0-9][0-9]|[1-9][0-9]{3,})\b'
# /etc/security/faillock.conf
# unlock_time = 900
# Run the following command to verify that the unlock_time argument has not been set,
# or is either 0 (never) or 900 (15 minutes) or more and meets local site policy:
# # grep -Pi --
# '^\h*auth\h+(requisite|required|sufficient)\h+pam_faillock\.so\h+([^#\n\r]+\h
# +)?unlock_time\h*=\h*([1-9]|[1-9][0-9]|[1-8][0-9][0-9])\b' /etc/pam.d/common-
# auth
# Nothing should be returned

# Remediation candidate
Edit /etc/security/faillock.conf and update or add the following line:

# TODO: replace the commented/manual steps above with validated bash remediation logic.
