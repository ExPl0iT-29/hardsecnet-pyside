#!/usr/bin/env bash
set -euo pipefail

# CIS Benchmark: CIS Ubuntu Linux 24.04 LTS Benchmark
# Control: 5.2.4 - Ensure users must provide password for privilege escalation
# Source Page: 589
# Confidence: 0.96
# Status: review_required

# Audit guidance extracted from the benchmark
# Note: If passwords are not being used for authentication, this is not applicable.
# Verify the operating system requires users to supply a password for privilege escalation.
# Check the configuration of the /etc/sudoers and /etc/sudoers.d/* files with the
# following command:
# # grep -r "^[^#].*NOPASSWD" /etc/sudoers*
# If any line is found refer to the remediation procedure below.

# Remediation candidate
# Manual review required
# Convert the remediation guidance below into a validated script action

# TODO: replace the commented/manual steps above with validated bash remediation logic.
