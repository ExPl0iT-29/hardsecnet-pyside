#!/usr/bin/env bash
set -euo pipefail

# CIS Benchmark: CIS Ubuntu Linux 24.04 LTS Benchmark
# Control: 4.3.6 - Ensure nftables loopback traffic is configured
# Source Page: 477
# Confidence: 0.96
# Status: review_required

# Audit guidance extracted from the benchmark
# Run the following commands to verify that the loopback interface is configured:
# Run the following command to verify the loopback interface is configured to accept
# network traffic:
# # nft list ruleset | awk '/hook input/,/}/' | grep 'iif "lo" accept'
# Example output:
# iif "lo" accept
# Run the following command to verify network traffic from an iPv4 loopback interface is
# configured to drop:
# # nft list ruleset | awk '/hook input/,/}/' | grep 'ip saddr'
# Example output:
# ip saddr 127.0.0.0/8 counter packets 0 bytes 0 drop
# - IF - IPv6 is enabled on the system:
# Run the following command to verify network traffic from an iPv6 loopback interface is
# configured to drop:
# # nft list ruleset | awk '/hook input/,/}/' | grep 'ip6 saddr'
# Example output:
# ip6 saddr ::1 counter packets 0 bytes 0 drop
# Page 477

# Remediation candidate
# IF - IPv6 is enabled on the system:

# TODO: replace the commented/manual steps above with validated bash remediation logic.
