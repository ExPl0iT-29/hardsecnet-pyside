#!/usr/bin/env bash
set -euo pipefail

# CIS Benchmark: CIS Ubuntu Linux 24.04 LTS Benchmark
# Control: 2.1.3 - Ensure dhcp server services are not in use
# Source Page: 235
# Confidence: 0.96
# Status: review_required

# Audit guidance extracted from the benchmark
# Run the following commands to verify isc-dhcp-server is not installed:
# # dpkg-query -s isc-dhcp-server &>/dev/null && echo "isc-dhcp-server is
# installed"
# Nothing should be returned.
# - OR -
# - IF - the package is required for dependencies:
# Run the following command to verify isc-dhcp-server.service and isc-dhcp-
# server6.service are not enabled:
# # systemctl is-enabled isc-dhcp-server.service isc-dhcp-server6.service
# 2>/dev/null | grep 'enabled'
# Nothing should be returned.
# Run the following command to verify isc-dhcp-server.service and isc-dhcp-
# server6.service are not active:
# # systemctl is-active isc-dhcp-server.service isc-dhcp-server6.service
# 2>/dev/null | grep '^active'
# Nothing should be returned.
# Note: If the package is required for a dependency
# -
# Ensure the dependent package is approved by local site policy
# -
# Ensure stopping and masking the service and/or socket meets local site policy

# Remediation candidate
# systemctl stop isc-dhcp-server.service isc-dhcp-server6.service
# OR -
# IF - the isc-dhcp-server package is required as a dependency:
# systemctl stop isc-dhcp-server.service isc-dhcp-server6.service
# systemctl mask isc-dhcp-server isc-dhcp-server6.service

# TODO: replace the commented/manual steps above with validated bash remediation logic.
