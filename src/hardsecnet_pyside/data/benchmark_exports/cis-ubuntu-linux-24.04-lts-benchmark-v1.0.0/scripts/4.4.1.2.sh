#!/usr/bin/env bash
set -euo pipefail

# CIS Benchmark: CIS Ubuntu Linux 24.04 LTS Benchmark
# Control: 4.4.1.2 - Ensure nftables is not in use with iptables
# Source Page: 494
# Confidence: 0.96
# Status: review_required

# Audit guidance extracted from the benchmark
# Run the following commend to verify that nftables is not installed:
# # dpkg-query -s nftables &>/dev/null && echo "nftables is installed"
# Nothing should be returned
# - OR -
# Run the following command to verify nftables.service is not enabled:
# # systemctl is-enabled nftables.service 2>/dev/null | grep '^enabled'
# Nothing should be returned
# Run the following command to verify nftables.service is not active:
# # systemctl is-active nftables.service 2>/dev/null | grep '^active'
# Nothing should be returned

# Remediation candidate
# OR -
# systemctl stop nftables.service
# systemctl mask nftables.service

# TODO: replace the commented/manual steps above with validated bash remediation logic.
