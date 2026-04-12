#!/usr/bin/env bash
set -euo pipefail

# CIS Benchmark: CIS Ubuntu Linux 24.04 LTS Benchmark
# Control: 4.4.3.4 - Ensure ip6tables firewall rules exist for all open ports
# Source Page: 518
# Confidence: 0.96
# Status: review_required

# Audit guidance extracted from the benchmark
# Run the following command to determine open ports:
# # ss -6tuln
# Netid State Recv-Q Send-Q Local Address:Port Peer
# Address:Port
# udp UNCONN 0 0 ::1:123
# :::*
# udp UNCONN 0 0 :::123
# :::*
# tcp LISTEN 0 128 :::22
# :::*
# tcp LISTEN 0 20 ::1:25
# :::*
# Run the following command to determine firewall rules:
# # ip6tables -L INPUT -v -n
# Chain INPUT (policy DROP 0 packets, 0 bytes)
# pkts bytes target prot opt in out source
# destination
# 0 0 ACCEPT all lo * ::/0 ::/0
# 0 0 DROP all * * ::1 ::/0
# 0 0 ACCEPT tcp * * ::/0 ::/0
# tcp dpt:22 state NEW
# Verify all open ports listening on non-localhost addresses have at least one firewall rule.
# The last line identified by the "tcp dpt:22 state NEW" identifies it as a firewall rule for
# new connections on tcp port 22.
# - OR - verify IPv6 is not enabled:
# Run the following script. Output will confirm if IPv6 is enabled on the system:
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
# Page 519

# Remediation candidate
# Manual review required
# Convert the remediation guidance below into a validated script action

# TODO: replace the commented/manual steps above with validated bash remediation logic.
