#!/usr/bin/env bash
set -euo pipefail

# CIS Benchmark: CIS Ubuntu Linux 24.04 LTS Benchmark
# Control: 4.3.10 - Ensure nftables rules are permanent
# Source Page: 486
# Confidence: 0.96
# Status: review_required

# Audit guidance extracted from the benchmark
# Run the following commands to verify that input, forward, and output base chains are
# configured to be applied to a nftables ruleset on boot:
# Run the following command to verify the input base chain:
# # [ -n "$(grep -E '^\s*include' /etc/nftables.conf)" ] && awk '/hook
# input/,/}/' $(awk '$1 ~ /^\s*include/ { gsub("\"","",$2);print $2 }'
# /etc/nftables.conf)
# Output should be similar to:
# type filter hook input priority 0; policy drop;
# # Ensure loopback traffic is configured
# iif "lo" accept
# ip saddr 127.0.0.0/8 counter packets 0 bytes 0 drop
# ip6 saddr ::1 counter packets 0 bytes 0 drop
# # Ensure established connections are configured
# ip protocol tcp ct state established accept
# ip protocol udp ct state established accept
# # Accept port 22(SSH) traffic from anywhere
# tcp dport ssh accept
# Review the input base chain to ensure that it follows local site policy
# Run the following command to verify the forward base chain:
# # [ -n "$(grep -E '^\s*include' /etc/nftables.conf)" ] && awk '/hook
# forward/,/}/' $(awk '$1 ~ /^\s*include/ { gsub("\"","",$2);print $2 }'
# /etc/nftables.conf)
# Output should be similar to:
# # Base chain for hook forward named forward (Filters forwarded
# network packets)
# chain forward {
# type filter hook forward priority 0; policy drop;
# }
# Review the forward base chain to ensure that it follows local site policy.
# Run the following command to verify the forward base chain:
# # [ -n "$(grep -E '^\s*include' /etc/nftables.conf)" ] && awk '/hook
# output/,/}/' $(awk '$1 ~ /^\s*include/ 

# Remediation candidate
Edit the /etc/nftables.conf file and un-comment or add a line with include
# vi /etc/nftables.conf
include "/etc/nftables.rules"

# TODO: replace the commented/manual steps above with validated bash remediation logic.
