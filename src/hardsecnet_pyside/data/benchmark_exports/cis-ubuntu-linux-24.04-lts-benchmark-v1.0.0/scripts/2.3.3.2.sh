#!/usr/bin/env bash
set -euo pipefail

# CIS Benchmark: CIS Ubuntu Linux 24.04 LTS Benchmark
# Control: 2.3.3.2 - Ensure chrony is running as user _chrony
# Source Page: 324
# Confidence: 0.96
# Status: review_required

# Audit guidance extracted from the benchmark
# - IF - chrony is in use on the system, run the following command to verify the chronyd
# service is being run as the _chrony user:
# # ps -ef | awk '(/[c]hronyd/ && $1!="_chrony") { print $1 }'
# Nothing should be returned

# Remediation candidate
Add or edit the user line to /etc/chrony/chrony.conf or a file ending in .conf in
/etc/chrony/conf.d/:
# OR -

# TODO: replace the commented/manual steps above with validated bash remediation logic.
