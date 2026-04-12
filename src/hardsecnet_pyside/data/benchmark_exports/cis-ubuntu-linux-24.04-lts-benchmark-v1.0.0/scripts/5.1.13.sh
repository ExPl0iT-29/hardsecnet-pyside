#!/usr/bin/env bash
set -euo pipefail

# CIS Benchmark: CIS Ubuntu Linux 24.04 LTS Benchmark
# Control: 5.1.13 - Ensure sshd LoginGraceTime is configured
# Source Page: 559
# Confidence: 0.96
# Status: review_required

# Audit guidance extracted from the benchmark
# Run the following command and verify that output LoginGraceTime is between 1 and
# 60 seconds:
# # sshd -T | grep logingracetime
# logingracetime 60

# Remediation candidate
Edit the /etc/ssh/sshd_config file to set the LoginGraceTime parameter to 60

# TODO: replace the commented/manual steps above with validated bash remediation logic.
