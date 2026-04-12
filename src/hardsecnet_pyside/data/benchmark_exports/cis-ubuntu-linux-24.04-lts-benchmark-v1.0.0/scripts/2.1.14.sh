#!/usr/bin/env bash
set -euo pipefail

# CIS Benchmark: CIS Ubuntu Linux 24.04 LTS Benchmark
# Control: 2.1.14 - Ensure samba file server services are not in use
# Source Page: 266
# Confidence: 0.96
# Status: review_required

# Audit guidance extracted from the benchmark
# Run the following command to verify samba is not installed:
# # dpkg-query -s samba &>/dev/null && echo "samba is installed"
# Nothing should be returned.
# - OR -
# - IF - the package is required for dependencies:
# Run the following command to verify smbd.service is not enabled:
# # systemctl is-enabled smbd.service 2>/dev/null | grep 'enabled'
# Nothing should be returned.
# Run the following command to verify the smbd.service is not active:
# # systemctl is-active smbd.service 2>/dev/null | grep '^active'
# Nothing should be returned.
# Page 266

# Remediation candidate
# systemctl stop smbd.service
# OR -
# IF - the samba package is required as a dependency:
# systemctl stop smbd.service
# systemctl mask smbd.service

# TODO: replace the commented/manual steps above with validated bash remediation logic.
