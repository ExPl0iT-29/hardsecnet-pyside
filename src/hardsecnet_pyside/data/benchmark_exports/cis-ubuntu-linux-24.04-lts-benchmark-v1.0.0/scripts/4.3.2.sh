#!/usr/bin/env bash
set -euo pipefail

# CIS Benchmark: CIS Ubuntu Linux 24.04 LTS Benchmark
# Control: 4.3.2 - Ensure ufw is uninstalled or disabled with nftables
# Source Page: 469
# Confidence: 0.96
# Status: review_required

# Audit guidance extracted from the benchmark
# Run the following commands to verify that ufw is either not installed or inactive. Only
# one of the following needs to pass.
# Run the following command to verify that ufw is not installed:
# # dpkg-query -s ufw &>/dev/null && echo "ufw is installed"
# Nothing should be returned
# -OR-
# Run the following commands to verify ufw is disabled and ufw.service is not enabled:
# # ufw status
# Status: inactive
# # systemctl is-enabled ufw.service
# masked
# Page 469

# Remediation candidate
Run one of the following to either remove ufw or disable ufw and mask ufw.service:
# OR-
Run the following commands to disable ufw and mask ufw.service:
# ufw disable
# systemctl stop ufw.service
# systemctl mask ufw.service
Note: ufw disable needs to be run before systemctl mask ufw.service in order to

# TODO: replace the commented/manual steps above with validated bash remediation logic.
