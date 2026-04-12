#!/usr/bin/env bash
set -euo pipefail

# CIS Benchmark: CIS Ubuntu Linux 24.04 LTS Benchmark
# Control: 5.3.3.4.2 - Ensure pam_unix does not include remember
# Source Page: 668
# Confidence: 0.96
# Status: review_required

# Audit guidance extracted from the benchmark
# Run the following command to verify that the remember argument is not set on the
# pam_unix.so module:
# # grep -PH -- '^\h*^\h*[^#\n\r]+\h+pam_unix\.so\b' /etc/pam.d/common-
# {password,auth,account,session,session-noninteractive} | grep -Pv --
# '\bremember=\d+\b'
# Output should be similar to:
# /etc/pam.d/common-password:password [success=1 default=ignore]
# pam_unix.so obscure yescrypt
# /etc/pam.d/common-auth:auth [success=1 default=ignore] pam_unix.so
# /etc/pam.d/common-account:account [success=1 new_authtok_reqd=done
# default=ignore] pam_unix.so
# /etc/pam.d/common-session:session required pam_unix.so
# /etc/pam.d/common-session-noninteractive:session required pam_unix.so
# Page 668

# Remediation candidate
Run the following command to update the files in the /etc/pam.d/ directory:
Note: If custom files are being used, the corresponding files in /etc/pam.d/ would

# TODO: replace the commented/manual steps above with validated bash remediation logic.
