#!/usr/bin/env bash
set -euo pipefail

# CIS Benchmark: CIS Ubuntu Linux 24.04 LTS Benchmark
# Control: 1.3.1.1 - Ensure AppArmor is installed
# Source Page: 152
# Confidence: 0.96
# Status: review_required

# Audit guidance extracted from the benchmark
# Run the following command to verify that apparmor is installed:
# # dpkg-query -s apparmor &>/dev/null && echo "apparmor is installed"
# apparmor is installed
# Run the following command to verify that apparmor-utils is installed:
# # dpkg-query -s apparmor-utils &>/dev/null && echo "apparmor-utils is
# installed"
# apparmor-utils is installed

# Remediation candidate
# Manual review required
# Convert the remediation guidance below into a validated script action

# TODO: replace the commented/manual steps above with validated bash remediation logic.
