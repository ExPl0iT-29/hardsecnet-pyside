#!/usr/bin/env bash
set -euo pipefail

# CIS Benchmark: CIS Ubuntu Linux 24.04 LTS Benchmark
# Control: 2.1.12 - Ensure rpcbind services are not in use
# Source Page: 261
# Confidence: 0.96
# Status: review_required

# Audit guidance extracted from the benchmark
# Run the following command to verify rpcbind package is not installed:
# # dpkg-query -s rpcbind &>/dev/null && echo "rpcbind is installed"
# Nothing should be returned.
# - OR -
# - IF - the rpcbind package is required as a dependency:
# Run the following command to verify rpcbind.socket and rpcbind.service are not
# enabled:
# # systemctl is-enabled rpcbind.socket rpcbind.service 2>/dev/null | grep
# 'enabled'
# Nothing should be returned.
# Run the following command to verify rpcbind.socket and rpcbind.service are not
# active:
# # systemctl is-active rpcbind.socket rpcbind.service 2>/dev/null | grep
# '^active'
# Nothing should be returned.
# Note: If the package is required for a dependency
# -
# Ensure the dependent package is approved by local site policy
# -
# Ensure stopping and masking the service and/or socket meets local site policy

# Remediation candidate
# systemctl stop rpcbind.socket rpcbind.service
# OR -
# IF - the rpcbind package is required as a dependency:
# systemctl stop rpcbind.socket rpcbind.service
# systemctl mask rpcbind.socket rpcbind.service

# TODO: replace the commented/manual steps above with validated bash remediation logic.
