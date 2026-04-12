#!/usr/bin/env bash
set -euo pipefail

# CIS Benchmark: CIS Ubuntu Linux 24.04 LTS Benchmark
# Control: 4.4.3.3 - Ensure ip6tables outbound and established connections are configured
# Source Page: 515
# Confidence: 0.9000000000000001
# Status: review_required

# Audit guidance extracted from the benchmark
# Run the following command and verify all rules for new outbound, and established
# connections match site policy:
# # ip6tables -L -v -n
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
