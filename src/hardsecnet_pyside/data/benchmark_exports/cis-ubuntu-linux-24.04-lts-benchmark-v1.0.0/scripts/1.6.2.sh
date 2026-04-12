#!/usr/bin/env bash
set -euo pipefail

# CIS Benchmark: CIS Ubuntu Linux 24.04 LTS Benchmark
# Control: 1.6.2 - Ensure local login warning banner is configured properly
# Source Page: 187
# Confidence: 0.96
# Status: review_required

# Audit guidance extracted from the benchmark
# Run the following command and verify that the contents match site policy:
# # cat /etc/issue
# Run the following command and verify no results are returned:
# # grep -E -i "(\\\v|\\\r|\\\m|\\\s|$(grep '^ID=' /etc/os-release | cut -d= -
# f2 | sed -e 's/"//g'))" /etc/issue
# Page 187

# Remediation candidate
Edit the /etc/issue file with the appropriate contents according to your site policy,
/etc/issue

# TODO: replace the commented/manual steps above with validated bash remediation logic.
