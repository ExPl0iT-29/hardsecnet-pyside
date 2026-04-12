#!/usr/bin/env bash
set -euo pipefail

# CIS Benchmark: CIS Ubuntu Linux 24.04 LTS Benchmark
# Control: 2.1.9 - Ensure network file system services are not in use
# Source Page: 252
# Confidence: 0.96
# Status: review_required

# Audit guidance extracted from the benchmark
# Run the following command to verify nfs-kernel-server is not installed:
# # dpkg-query -s nfs-kernel-server &>/dev/null && echo "nfs-kernel-server is
# installed"
# Nothing should be returned.
# - OR -
# - IF - package is required for dependencies:
# Run the following command to verify that the nfs-server.service is not enabled:
# # systemctl is-enabled nfs-server.service 2>/dev/null | grep 'enabled'
# Nothing should be returned.
# Run the following command to verify the nfs-server.service is not active:
# # systemctl is-active nfs-server.service 2>/dev/null | grep '^active'
# Nothing should be returned.
# Note: If the package is required for a dependency
# -
# Ensure the dependent package is approved by local site policy
# -
# Ensure stopping and masking the service and/or socket meets local site policy

# Remediation candidate
# systemctl stop nfs-server.service
# OR -
# IF - the nfs-kernel-server package is required as a dependency:
# systemctl stop nfs-server.service
# systemctl mask nfs-server.service

# TODO: replace the commented/manual steps above with validated bash remediation logic.
