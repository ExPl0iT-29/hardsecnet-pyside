#!/usr/bin/env bash
set -euo pipefail

# CIS Benchmark: CIS Ubuntu Linux 24.04 LTS Benchmark
# Control: 4.4.1.3 - Ensure ufw is not in use with iptables
# Source Page: 496
# Confidence: 0.96
# Status: review_required

# Audit guidance extracted from the benchmark
# Run the following commands to verify that ufw is either not installed or disabled. Only
# one of the following needs to pass.
# Run the following command to verify that ufw is not installed:
# # dpkg-query -s ufw &>/dev/null && echo "ufw is installed"
# Nothing should be returned.
# - OR -
# Run the following command to verify ufw is disabled:
# # ufw status
# Status: inactive
# Run the following commands to verify that the ufw.service is not enabled:
# # systemctl is-enabled ufw 2>dev/null | grep '^enabled'
# Nothing should be returned
# Run the following command to verify ufw.service is not active:
# # systemctl is-active ufw.service 2>/dev/null | grep '^active'
# Nothing should be returned
# Page 496

# Remediation candidate
# OR -
# ufw disable
# systemctl stop ufw.service
# systemctl mask ufw.service
Note: ufw disable needs to be run before systemctl mask ufw.service in order to

# TODO: replace the commented/manual steps above with validated bash remediation logic.
