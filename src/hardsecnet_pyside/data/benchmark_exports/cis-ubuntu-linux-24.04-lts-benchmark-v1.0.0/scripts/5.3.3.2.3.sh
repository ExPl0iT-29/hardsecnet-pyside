#!/usr/bin/env bash
set -euo pipefail

# CIS Benchmark: CIS Ubuntu Linux 24.04 LTS Benchmark
# Control: 5.3.3.2.3 - Ensure password complexity is configured
# Source Page: 634
# Confidence: 0.9000000000000001
# Status: review_required

# Audit guidance extracted from the benchmark
# Run the following command to verify:
# -
# dcredit, ucredit, lcredit, and ocredit are not set to a value greater than 0
# -
# Complexity conforms to local site policy:
# # grep -Psi -- '^\h*(minclass|[dulo]credit)\b' /etc/security/pwquality.conf
# /etc/security/pwquality.conf.d/*.conf
# Example output:
# /etc/security/pwquality.conf.d/50-pwcomplexity.conf:minclass = 3
# /etc/security/pwquality.conf.d/50-pwcomplexity.conf:ucredit = -2
# /etc/security/pwquality.conf.d/50-pwcomplexity.conf:lcredit = -2
# /etc/security/pwquality.conf.d/50-pwcomplexity.conf:dcredit = -1
# /etc/security/pwquality.conf.d/50-pwcomplexity.conf:ocredit = 0
# The example represents a requirement of three character classes, with passwords
# requiring two upper case, two lower case, and one numeric character.
# Run the following command to verify that module arguments in the configuration file(s)
# are not being overridden by arguments in /etc/pam.d/common-password:
# # grep -Psi --
# '^\h*password\h+(requisite|required|sufficient)\h+pam_pwquality\.so\h+([^#\n\
# r]+\h+)?(minclass=\d*|[dulo]credit=-?\d*)\b' /etc/pam.d/common-password
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
# o settings in a .conf file in 

# Remediation candidate
'\bpam_pwquality\.so\h+([^#\n\r]+\h+)?(minclass|[dulo]credit)\b'
ocredit arguments from the pam_pwquality.so line(s)
Create or modify a file ending in .conf in the /etc/security/pwquality.conf.d/
directory or the file /etc/security/pwquality.conf and add or modify the following
sed -ri 's/^\s*minclass\s*=/# &/' /etc/security/pwquality.conf
sed -ri 's/^\s*[dulo]credit\s*=/# &/' /etc/security/pwquality.conf
[ ! -d /etc/security/pwquality.conf.d/ ] && mkdir
/etc/security/pwquality.conf.d/
printf '\n%s' "minclass = 3" > /etc/security/pwquality.conf.d/50-
sed -ri 's/^\s*minclass\s*=/# &/' /etc/security/pwquality.conf
sed -ri 's/^\s*[dulo]credit\s*=/# &/' /etc/security/pwquality.conf
[ ! -d /etc/security/pwquality.conf.d/ ] && mkdir
/etc/security/pwquality.conf.d/
/etc/security/pwquality.conf.d/50-pwcomplexity.conf

# TODO: replace the commented/manual steps above with validated bash remediation logic.
