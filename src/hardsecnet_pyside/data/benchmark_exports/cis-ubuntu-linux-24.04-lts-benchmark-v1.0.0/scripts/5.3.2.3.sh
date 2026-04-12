#!/usr/bin/env bash
set -euo pipefail

# CIS Benchmark: CIS Ubuntu Linux 24.04 LTS Benchmark
# Control: 5.3.2.3 - Ensure pam_pwquality module is enabled
# Source Page: 608
# Confidence: 0.96
# Status: review_required

# Audit guidance extracted from the benchmark
# Run the following command to verify that pam_pwhistory is enabled:
# # grep -P -- '\bpam_pwquality\.so\b' /etc/pam.d/common-password
# Output should be similar to:
# password requisite pam_pwquality.so retry=3

# Remediation candidate
Run the following script to verify the pam_pwquality.so line exists in a pam-auth-
# grep -P -- '\bpam_pwquality\.so\b' /usr/share/pam-configs/*
/usr/share/pam-configs/pwquality: requisite
pam_pwquality.so retry=3
/usr/share/pam-configs/pwquality: requisite
pam_pwquality.so retry=3
# IF - similar output is returned:
Run the following command to update /etc/pam.d/common-password with the
# pam-auth-update pwquality
# IF - similar output is NOT returned:
requisite pam_pwquality.so retry=3
requisite pam_pwquality.so retry=3')
printf '%s\n' "${arr[@]}" > /usr/share/pam-configs/pwquality
Run the following command to update /etc/pam.d/common-password with the
pwquality profile:
# pam-auth-update --enable pwquality
/etc/pam.d/ files
PAM that includes the configuration for the pam_pwquality module, enable that

# TODO: replace the commented/manual steps above with validated bash remediation logic.
