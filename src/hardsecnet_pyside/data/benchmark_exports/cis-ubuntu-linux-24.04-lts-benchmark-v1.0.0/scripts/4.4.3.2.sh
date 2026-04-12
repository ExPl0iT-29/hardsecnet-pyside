#!/usr/bin/env bash
set -euo pipefail

# CIS Benchmark: CIS Ubuntu Linux 24.04 LTS Benchmark
# Control: 4.4.3.2 - Ensure ip6tables loopback traffic is configured
# Source Page: 512
# Confidence: 0.96
# Status: review_required

# Audit guidance extracted from the benchmark
# Run the following commands and verify output includes the listed rules in order (packet
# and byte counts may differ):
# # ip6tables -L INPUT -v -n
# Chain INPUT (policy DROP 0 packets, 0 bytes)
# pkts bytes target prot opt in out source
# destination
# 0 0 ACCEPT all lo * ::/0 ::/0
# 0 0 DROP all * * ::1 ::/0
# # ip6tables -L OUTPUT -v -n
# Chain OUTPUT (policy DROP 0 packets, 0 bytes)
# pkts bytes target prot opt in out source
# destination
# 0 0 ACCEPT all * lo ::/0 ::/0
# - OR -
# Verify IPv6 is disabled:
# Run the following script. Output will confirm if IPv6 is enabled on the system.
# #!/usr/bin/env bash
# {
# l_ipv6_enabled="is"
# ! grep -Pqs -- '^\h*0\b' /sys/module/ipv6/parameters/disable &&
# l_ipv6_enabled="is not"
# if sysctl net.ipv6.conf.all.disable_ipv6 | grep -Pqs --
# "^\h*net\.ipv6\.conf\.all\.disable_ipv6\h*=\h*1\b" && \
# sysctl net.ipv6.conf.default.disable_ipv6 | grep -Pqs --
# "^\h*net\.ipv6\.conf\.default\.disable_ipv6\h*=\h*1\b"; then
# l_ipv6_enabled="is not"
# fi
# echo -e " - IPv6 $l_ipv6_enabled enabled on the system"
# }

# Remediation candidate
# Manual review required
# Convert the remediation guidance below into a validated script action

# TODO: replace the commented/manual steps above with validated bash remediation logic.
