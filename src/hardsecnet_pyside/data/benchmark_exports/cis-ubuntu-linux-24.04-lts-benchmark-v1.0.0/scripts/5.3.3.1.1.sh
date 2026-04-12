#!/usr/bin/env bash
set -euo pipefail

# CIS Benchmark: CIS Ubuntu Linux 24.04 LTS Benchmark
# Control: 5.3.3.1.1 - Ensure password failed attempts lockout is configured
# Source Page: 616
# Confidence: 0.96
# Status: review_required

# Audit guidance extracted from the benchmark
# Run the following command to verify that Number of failed logon attempts before the
# account is locked is no greater than 5 and meets local site policy:
# # grep -Pi -- '^\h*deny\h*=\h*[1-5]\b' /etc/security/faillock.conf
# deny = 5
# Run the following command to verify that the deny argument has not been set, or 5 or
# less and meets local site policy:
# # grep -Pi --
# '^\h*auth\h+(requisite|required|sufficient)\h+pam_faillock\.so\h+([^#\n\r]+\h
# +)?deny\h*=\h*(0|[6-9]|[1-9][0-9]+)\b' /etc/pam.d/common-auth
# Nothing should be returned

# Remediation candidate
Create or edit the following line in /etc/security/faillock.conf setting the deny

# TODO: replace the commented/manual steps above with validated bash remediation logic.
