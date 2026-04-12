#!/usr/bin/env bash
set -euo pipefail

# CIS Benchmark: CIS Ubuntu Linux 24.04 LTS Benchmark
# Control: 5.1.18 - Ensure sshd MaxStartups is configured
# Source Page: 570
# Confidence: 0.96
# Status: review_required

# Audit guidance extracted from the benchmark
# Run the following command to verify MaxStartups is 10:30:60 or more restrictive:
# # sshd -T | awk '$1 ~ /^\s*maxstartups/{split($2, a, ":");{if(a[1] > 10 ||
# a[2] > 30 || a[3] > 60) print $0}}'
# Nothing should be returned

# Remediation candidate
Edit the /etc/ssh/sshd_config file to set the MaxStartups parameter to 10:30:60 or

# TODO: replace the commented/manual steps above with validated bash remediation logic.
