#!/usr/bin/env bash
set -euo pipefail

# CIS Benchmark: CIS Ubuntu Linux 24.04 LTS Benchmark
# Control: 4.4.3.1 - Ensure ip6tables default deny firewall policy
# Source Page: 509
# Confidence: 0.96
# Status: review_required

# Audit guidance extracted from the benchmark
# Run the following command and verify that the policy for the INPUT, OUTPUT, and
# FORWARD chains is DROP or REJECT:
# # ip6tables -L
# Chain INPUT (policy DROP)
# Chain FORWARD (policy DROP)
# Chain OUTPUT (policy DROP)
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
# IF - IPv6 is enabled on your system:

# TODO: replace the commented/manual steps above with validated bash remediation logic.
