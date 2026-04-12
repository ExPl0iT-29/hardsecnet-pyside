#!/usr/bin/env bash
set -euo pipefail

# CIS Benchmark: CIS Ubuntu Linux 24.04 LTS Benchmark
# Control: 5.4.2.4 - Ensure root account access is controlled
# Source Page: 701
# Confidence: 0.96
# Status: review_required

# Audit guidance extracted from the benchmark
# Run the following command to verify that either the root user's password is set or the
# root user's account is locked:
# # passwd -S root | awk '$2 ~ /^(P|L)/ {print "User: \"" $1 "\" Password is
# status: " $2}'
# Verify the output is either:
# User: "root" Password is status: P
# - OR -
# User: "root" Password is status: L
# Note:
# -
# P - Password is set
# -
# L - Password is locked
# Page 701

# Remediation candidate
# OR -

# TODO: replace the commented/manual steps above with validated bash remediation logic.
