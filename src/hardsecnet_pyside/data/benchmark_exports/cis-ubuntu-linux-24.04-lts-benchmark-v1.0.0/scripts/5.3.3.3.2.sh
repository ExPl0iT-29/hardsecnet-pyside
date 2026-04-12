#!/usr/bin/env bash
set -euo pipefail

# CIS Benchmark: CIS Ubuntu Linux 24.04 LTS Benchmark
# Control: 5.3.3.3.2 - Ensure password history is enforced for the root user
# Source Page: 658
# Confidence: 0.96
# Status: review_required

# Audit guidance extracted from the benchmark
# Run the following command to verify that the enforce_for_root argument is exists on
# the pwhistory line in /etc/pam.d/common-password:
# # grep -Psi --
# '^\h*password\h+[^#\n\r]+\h+pam_pwhistory\.so\h+([^#\n\r]+\h+)?enforce_for_ro
# ot\b' /etc/pam.d/common-password
# Output should be similar to:
# password requisite pam_pwhistory.so remember=24 enforce_for_root
# try_first_pass use_authtok
# Page 658

# Remediation candidate
Run the following command to update the files in the /etc/pam.d/ directory:

# TODO: replace the commented/manual steps above with validated bash remediation logic.
