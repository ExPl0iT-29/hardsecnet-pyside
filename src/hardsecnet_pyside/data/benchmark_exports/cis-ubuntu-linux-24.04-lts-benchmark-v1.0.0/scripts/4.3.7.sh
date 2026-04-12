#!/usr/bin/env bash
set -euo pipefail

# CIS Benchmark: CIS Ubuntu Linux 24.04 LTS Benchmark
# Control: 4.3.7 - Ensure nftables outbound and established connections are configured
# Source Page: 479
# Confidence: 0.9000000000000001
# Status: review_required

# Audit guidance extracted from the benchmark
# Run the following commands and verify all rules for established incoming connections
# match site policy: site policy:
# # nft list ruleset | awk '/hook input/,/}/' | grep -E 'ip protocol (tcp|udp)
# ct state'
# Output should be similar to:
# ip protocol tcp ct state established accept
# ip protocol udp ct state established accept
# Run the folllowing command and verify all rules for new and established outbound
# connections match site policy
# # nft list ruleset | awk '/hook output/,/}/' | grep -E 'ip protocol (tcp|udp)
# ct state'
# Output should be similar to:
# ip protocol tcp ct state established,related,new accept
# ip protocol udp ct state established,related,new accept
# Page 479

# Remediation candidate
# Manual review required
# Convert the remediation guidance below into a validated script action

# TODO: replace the commented/manual steps above with validated bash remediation logic.
