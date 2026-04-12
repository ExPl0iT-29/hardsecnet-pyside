#!/usr/bin/env bash
set -euo pipefail

# CIS Benchmark: CIS Ubuntu Linux 24.04 LTS Benchmark
# Control: 5.3.3.2.7 - Ensure password quality checking is enforced
# Source Page: 649
# Confidence: 0.96
# Status: review_required

# Audit guidance extracted from the benchmark
# Run the following command to verify that enforcing=0 has not been set in a
# pwquality configuration file:
# # grep -PHsi -- '^\h*enforcing\h*=\h*0\b' /etc/security/pwquality.conf
# /etc/security/pwquality.conf.d/*.conf
# Nothing should be returned
# Run the following command to verify that the enforcing=0 argument has not been set
# on the pam_pwquality module:
# # grep -PHsi --
# '^\h*password\h+[^#\n\r]+\h+pam_pwquality\.so\h+([^#\n\r]+\h+)?enforcing=0\b'
# /etc/pam.d/common-password
# Nothing should be returned
# Page 649

# Remediation candidate
# grep -Pl -- '\bpam_pwquality\.so\h+([^#\n\r]+\h+)?enforcing=0\b'
pam_pwquality.so line(s)
Edit /etc/security/pwquality.conf and all files ending in .conf in the
/etc/security/pwquality.conf.d/ directory and remove or comment out any line
# sed -ri 's/^\s*enforcing\s*=\s*0/# &/' /etc/security/pwquality.conf
/etc/security/pwquality.conf.d/*.conf

# TODO: replace the commented/manual steps above with validated bash remediation logic.
