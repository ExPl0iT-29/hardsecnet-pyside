#!/usr/bin/env bash
set -euo pipefail

# CIS Benchmark: CIS Ubuntu Linux 24.04 LTS Benchmark
# Control: 5.3.2.4 - Ensure pam_pwhistory module is enabled
# Source Page: 611
# Confidence: 0.96
# Status: review_required

# Audit guidance extracted from the benchmark
# Run the following command to verify that pam_pwhistory is enabled:
# # grep -P -- '\bpam_pwhistory\.so\b' /etc/pam.d/common-password
# Output should be similar to:
# password requisite pam_pwhistory.so remember=24 enforce_for_root
# try_first_pass use_authtok

# Remediation candidate
Run the following script to verify the pam_pwquality.so line exists in a pam-auth-
# IF - similar output is returned:
Run the following command to update /etc/pam.d/common-password with the
# IF - similar output is NOT returned:
Run the following command to update /etc/pam.d/common-password with the
/etc/pam.d/ files

# TODO: replace the commented/manual steps above with validated bash remediation logic.
