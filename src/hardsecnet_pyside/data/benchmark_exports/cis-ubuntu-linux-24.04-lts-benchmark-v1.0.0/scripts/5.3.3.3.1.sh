#!/usr/bin/env bash
set -euo pipefail

# CIS Benchmark: CIS Ubuntu Linux 24.04 LTS Benchmark
# Control: 5.3.3.3.1 - Ensure password history remember is configured
# Source Page: 655
# Confidence: 0.96
# Status: review_required

# Audit guidance extracted from the benchmark
# Run the following command and verify:
# -
# The pwhistory line in /etc/pam.d/common-password includes remember=<N>
# -
# The value of <N> is 24 or more
# -
# The value meets local site policy
# # grep -Psi --
# '^\h*password\h+[^#\n\r]+\h+pam_pwhistory\.so\h+([^#\n\r]+\h+)?remember=\d+\b
# ' /etc/pam.d/common-password
# Output should be similar to:
# password requisite pam_pwhistory.so remember=24 enforce_for_root
# try_first_pass use_authtok
# Page 655

# Remediation candidate
Run the following command to update the files in the /etc/pam.d/ directory:

# TODO: replace the commented/manual steps above with validated bash remediation logic.
