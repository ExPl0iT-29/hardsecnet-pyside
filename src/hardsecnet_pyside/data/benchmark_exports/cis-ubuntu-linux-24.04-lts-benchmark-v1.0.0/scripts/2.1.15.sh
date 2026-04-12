#!/usr/bin/env bash
set -euo pipefail

# CIS Benchmark: CIS Ubuntu Linux 24.04 LTS Benchmark
# Control: 2.1.15 - Ensure snmp services are not in use
# Source Page: 268
# Confidence: 0.96
# Status: review_required

# Audit guidance extracted from the benchmark
# Run the following command to verify snmpd is not installed:
# # dpkg-query -s snmpd &>/dev/null && echo "snmpd is installed"
# Nothing should be returned.
# - OR -
# - IF - the package is required for dependencies:
# Run the following command to verify the snmpd.service is not enabled:
# # systemctl is-enabled snmpd.service 2>/dev/null | grep 'enabled'
# Nothing should be returned.
# Run the following command to verify the snmpd.service is not active:
# # systemctl is-active snmpd.service 2>/dev/null | grep '^active'
# Nothing should be returned.
# Note: If the package is required for a dependency
# -
# Ensure the dependent package is approved by local site policy
# -
# Ensure stopping and masking the service and/or socket meets local site policy

# Remediation candidate
# systemctl stop snmpd.service
# OR - If the package is required for dependencies:
# systemctl stop snmpd.service
# systemctl mask snmpd.service

# TODO: replace the commented/manual steps above with validated bash remediation logic.
