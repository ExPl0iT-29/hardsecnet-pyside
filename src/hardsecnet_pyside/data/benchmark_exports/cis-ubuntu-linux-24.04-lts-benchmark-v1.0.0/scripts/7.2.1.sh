#!/usr/bin/env bash
set -euo pipefail

# CIS Benchmark: CIS Ubuntu Linux 24.04 LTS Benchmark
# Control: 7.2.1 - Ensure accounts in /etc/passwd use shadowed passwords
# Source Page: 966
# Confidence: 0.96
# Status: review_required

# Audit guidance extracted from the benchmark
# Run the following command and verify that no output is returned:
# # awk -F: '($2 != "x" ) { print "User: \"" $1 "\" is not set to shadowed
# passwords "}' /etc/passwd

# Remediation candidate
passwords in /etc/passwd to /etc/shadow:

# TODO: replace the commented/manual steps above with validated bash remediation logic.
