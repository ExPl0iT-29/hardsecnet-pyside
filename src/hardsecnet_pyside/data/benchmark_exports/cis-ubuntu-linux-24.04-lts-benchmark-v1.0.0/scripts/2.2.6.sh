#!/usr/bin/env bash
set -euo pipefail

# CIS Benchmark: CIS Ubuntu Linux 24.04 LTS Benchmark
# Control: 2.2.6 - Ensure ftp client is not installed
# Source Page: 303
# Confidence: 0.96
# Status: review_required

# Audit guidance extracted from the benchmark
# Verify tnftp & ftp is not installed. Use the following command to provide the needed
# information:
# # dpkg-query -l | grep -E 'ftp|tnftp' &>/dev/null && echo "ftp is installed"
# Nothing should be returned.

# Remediation candidate
# Manual review required
# Convert the remediation guidance below into a validated script action

# TODO: replace the commented/manual steps above with validated bash remediation logic.
