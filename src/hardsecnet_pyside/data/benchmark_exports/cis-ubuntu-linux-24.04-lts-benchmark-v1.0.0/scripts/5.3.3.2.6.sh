#!/usr/bin/env bash
set -euo pipefail

# CIS Benchmark: CIS Ubuntu Linux 24.04 LTS Benchmark
# Control: 5.3.3.2.6 - Ensure password dictionary check is enabled
# Source Page: 646
# Confidence: 0.96
# Status: review_required

# Audit guidance extracted from the benchmark
# Run the following command to verify that the dictcheck option is not set to 0 (disabled)
# in a pwquality configuration file:
# # grep -Psi -- '^\h*dictcheck\h*=\h*0\b' /etc/security/pwquality.conf
# /etc/security/pwquality.conf.d/*.conf
# Nothing should be returned
# Run the following command to verify that the dictcheck option is not set to 0 (disabled)
# as a module argument in a PAM file:
# # grep -Psi --
# '^\h*password\h+(requisite|required|sufficient)\h+pam_pwquality\.so\h+([^#\n\
# r]+\h+)?dictcheck\h*=\h*0\b' /etc/pam.d/common-password
# Nothing should be returned
# Note:
# -
# Settings observe an order of precedence:
# o module arguments override the settings in the
# /etc/security/pwquality.conf configuration file
# o settings in the /etc/security/pwquality.conf configuration file
# override settings in a .conf file in the
# /etc/security/pwquality.conf.d/ directory
# o settings in a .conf file in the /etc/security/pwquality.conf.d/
# directory are read in canonical order, with last read file containing the
# setting taking precedence
# -
# It is recommended that settings be configured in a .conf file in the
# /etc/security/pwquality.conf.d/ directory for clarity, convenience, and
# durability.

# Remediation candidate
Edit any file ending in .conf in the /etc/security/pwquality.conf.d/ directory
and/or the file /etc/security/pwquality.conf and comment out or remove any
# sed -ri 's/^\s*dictcheck\s*=/# &/' /etc/security/pwquality.conf
/etc/security/pwquality.conf.d/*.conf
# grep -Pl -- '\bpam_pwquality\.so\h+([^#\n\r]+\h+)?dictcheck\b'
pam_pwquality.so line(s)

# TODO: replace the commented/manual steps above with validated bash remediation logic.
