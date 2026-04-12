#!/usr/bin/env bash
set -euo pipefail

# CIS Benchmark: CIS Ubuntu Linux 24.04 LTS Benchmark
# Control: 1.6.1 - Ensure message of the day is configured properly
# Source Page: 185
# Confidence: 0.96
# Status: review_required

# Audit guidance extracted from the benchmark
# Run the following command and verify that the contents match site policy:
# # cat /etc/motd
# Run the following command and verify no results are returned:
# # grep -E -i "(\\\v|\\\r|\\\m|\\\s|$(grep '^ID=' /etc/os-release | cut -d= -
# f2 | sed -e 's/"//g'))" /etc/motd
# Page 185

# Remediation candidate
Edit the /etc/motd file with the appropriate contents according to your site policy,
# OR -
# IF - the motd is not used, this file can be removed.
# rm /etc/motd

# TODO: replace the commented/manual steps above with validated bash remediation logic.
