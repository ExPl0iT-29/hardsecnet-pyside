#!/usr/bin/env bash
set -euo pipefail

# CIS Benchmark: CIS Ubuntu Linux 24.04 LTS Benchmark
# Control: 5.3.3.2.1 - Ensure password number of changed characters is configured
# Source Page: 626
# Confidence: 0.96
# Status: review_required

# Audit guidance extracted from the benchmark
# Run the following command to verify that the difok option is set to 2 or more and
# follows local site policy:
# # grep -Psi -- '^\h*difok\h*=\h*([2-9]|[1-9][0-9]+)\b'
# /etc/security/pwquality.conf /etc/security/pwquality.conf.d/*.conf
# Example output:
# /etc/security/pwquality.conf.d/50-pwdifok.conf:difok = 2
# Verify returned value(s) are 2 or more and meet local site policy
# Run the following command to verify that difok is not set, is 2 or more, and conforms to
# local site policy:
# # grep -Psi --
# '^\h*password\h+(requisite|required|sufficient)\h+pam_pwquality\.so\h+([^#\n\
# r]+\h+)?difok\h*=\h*([0-1])\b' /etc/pam.d/common-password
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
# Page 627

# Remediation candidate
Create or modify a file ending in .conf in the /etc/security/pwquality.conf.d/
directory or the file /etc/security/pwquality.conf and add or modify the following
sed -ri 's/^\s*difok\s*=/# &/' /etc/security/pwquality.conf
[ ! -d /etc/security/pwquality.conf.d/ ] && mkdir
/etc/security/pwquality.conf.d/
printf '\n%s' "difok = 2" > /etc/security/pwquality.conf.d/50-pwdifok.conf
# grep -Pl -- '\bpam_pwquality\.so\h+([^#\n\r]+\h+)?difok\b' /usr/share/pam-
Edit any returned files and remove the difok argument from the pam_pwquality.so

# TODO: replace the commented/manual steps above with validated bash remediation logic.
