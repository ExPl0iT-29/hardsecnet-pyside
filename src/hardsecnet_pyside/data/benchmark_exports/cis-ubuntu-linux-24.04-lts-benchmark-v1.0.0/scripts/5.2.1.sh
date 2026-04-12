#!/usr/bin/env bash
set -euo pipefail

# CIS Benchmark: CIS Ubuntu Linux 24.04 LTS Benchmark
# Control: 5.2.1 - Ensure sudo is installed
# Source Page: 581
# Confidence: 0.96
# Status: review_required

# Audit guidance extracted from the benchmark
# Run the following command to verify that either sudo is installed:
# # dpkg-query -s sudo &>/dev/null && echo "sudo is installed"
# sudo is installed
# - OR -
# Run the following command to verify that either sudo-ldap is installed:
# # dpkg-query -s sudo-ldap &>/dev/null && echo "sudo-ldap is installed"
# sudo-ldap is installed

# Remediation candidate
# Manual review required
# Convert the remediation guidance below into a validated script action

# TODO: replace the commented/manual steps above with validated bash remediation logic.
