#!/usr/bin/env bash
set -euo pipefail

# CIS Benchmark: CIS Ubuntu Linux 24.04 LTS Benchmark
# Control: 5.3.3.2.2 - Ensure minimum password length is configured
# Source Page: 630
# Confidence: 0.96
# Status: review_required

# Audit guidance extracted from the benchmark
# Run the following command to verify that password length is 14 or more characters, and
# conforms to local site policy:
# # grep -Psi -- '^\h*minlen\h*=\h*(1[4-9]|[2-9][0-9]|[1-9][0-9]{2,})\b'
# /etc/security/pwquality.conf /etc/security/pwquality.conf.d/*.conf
# Example output:
# /etc/security/pwquality.conf.d/50-pwlength.conf:minlen = 14
# Verify returned value(s) are no less than 14 characters and meet local site policy
# Run the following command to verify that minlen is not set, or is 14 or more characters,
# and conforms to local site policy:
# # grep -Psi --
# '^\h*password\h+(requisite|required|sufficient)\h+pam_pwquality\.so\h+([^#\n\
# r]+\h+)?minlen\h*=\h*([0-9]|1[0-3])\b' /etc/pam.d/system-auth
# /etc/pam.d/common-password
# Nothing should be returned
# Note:
# -
# settings should be configured in only one location for clarity
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
# Page 631

# Remediation candidate
Create or modify a file ending in .conf in the /etc/security/pwquality.conf.d/
directory or the file /etc/security/pwquality.conf and add or modify the following
sed -ri 's/^\s*minlen\s*=/# &/' /etc/security/pwquality.conf
[ ! -d /etc/security/pwquality.conf.d/ ] && mkdir
/etc/security/pwquality.conf.d/
printf '\n%s' "minlen = 14" > /etc/security/pwquality.conf.d/50-
# grep -Pl -- '\bpam_pwquality\.so\h+([^#\n\r]+\h+)?minlen\b' /usr/share/pam-
Edit any returned files and remove the minlen argument from the pam_pwquality.so

# TODO: replace the commented/manual steps above with validated bash remediation logic.
