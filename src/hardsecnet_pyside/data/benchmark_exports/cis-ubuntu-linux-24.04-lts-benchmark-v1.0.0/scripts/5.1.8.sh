#!/usr/bin/env bash
set -euo pipefail

# CIS Benchmark: CIS Ubuntu Linux 24.04 LTS Benchmark
# Control: 5.1.8 - Ensure sshd DisableForwarding is enabled
# Source Page: 547
# Confidence: 0.96
# Status: review_required

# Audit guidance extracted from the benchmark
# Run the following command to verify DisableForwarding is set to yes:
# # sshd -T | grep -i disableforwarding
# disableforwarding yes

# Remediation candidate
Edit the /etc/ssh/sshd_config file to set the DisableForwarding parameter to yes

# TODO: replace the commented/manual steps above with validated bash remediation logic.
