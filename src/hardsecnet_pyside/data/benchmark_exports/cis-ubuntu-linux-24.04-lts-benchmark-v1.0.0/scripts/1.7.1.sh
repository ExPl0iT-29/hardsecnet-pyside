#!/usr/bin/env bash
set -euo pipefail

# CIS Benchmark: CIS Ubuntu Linux 24.04 LTS Benchmark
# Control: 1.7.1 - Ensure GDM is removed
# Source Page: 198
# Confidence: 0.96
# Status: review_required

# Audit guidance extracted from the benchmark
# Run the following command and verify gdm3 is not installed:
# # dpkg-query -W -f='${binary:Package}\t${Status}\t${db:Status-Status}\n' gdm3
# gdm3 unknown ok not-installed not-installed

# Remediation candidate
# Manual review required
# Convert the remediation guidance below into a validated script action

# TODO: replace the commented/manual steps above with validated bash remediation logic.
