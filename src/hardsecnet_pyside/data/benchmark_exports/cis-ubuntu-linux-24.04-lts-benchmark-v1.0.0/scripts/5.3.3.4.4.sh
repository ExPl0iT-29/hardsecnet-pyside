#!/usr/bin/env bash
set -euo pipefail

# CIS Benchmark: CIS Ubuntu Linux 24.04 LTS Benchmark
# Control: 5.3.3.4.4 - Ensure pam_unix includes use_authtok
# Source Page: 673
# Confidence: 0.96
# Status: review_required

# Audit guidance extracted from the benchmark
# Run the following command to verify that use_authtok is set on the pam_unix.so
# module lines in the password stack:
# # grep -PH --
# '^\h*password\h+([^#\n\r]+)\h+pam_unix\.so\h+([^#\n\r]+\h+)?use_authtok\b'
# /etc/pam.d/common-password
# Output should be similar to:
# /etc/pam.d/common-password:password [success=1 default=ignore]
# pam_unix.so obscure use_authtok try_first_pass yescrypt
# Verify that the line(s) include use_authtok
# Page 673

# Remediation candidate
Run the following command to update the files in the /etc/pam.d/ directory:

# TODO: replace the commented/manual steps above with validated bash remediation logic.
