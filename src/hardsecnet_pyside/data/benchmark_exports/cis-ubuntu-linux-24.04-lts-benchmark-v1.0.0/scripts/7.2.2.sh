#!/usr/bin/env bash
set -euo pipefail

# CIS Benchmark: CIS Ubuntu Linux 24.04 LTS Benchmark
# Control: 7.2.2 - Ensure /etc/shadow password fields are not empty
# Source Page: 969
# Confidence: 0.96
# Status: review_required

# Audit guidance extracted from the benchmark
# Run the following command and verify that no output is returned:
# # awk -F: '($2 == "" ) { print $1 " does not have a password "}' /etc/shadow

# Remediation candidate
If any accounts in the /etc/shadow file do not have a password, run the following

# TODO: replace the commented/manual steps above with validated bash remediation logic.
