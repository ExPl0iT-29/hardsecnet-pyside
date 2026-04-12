#!/usr/bin/env bash
set -euo pipefail

# CIS Benchmark: CIS Ubuntu Linux 24.04 LTS Benchmark
# Control: 4.2.3 - Ensure ufw service is enabled
# Source Page: 452
# Confidence: 0.96
# Status: review_required

# Audit guidance extracted from the benchmark
# Run the following command to verify that the ufw daemon is enabled:
# # systemctl is-enabled ufw.service
# enabled
# Run the following command to verify that the ufw daemon is active:
# # systemctl is-active ufw
# active
# Run the following command to verify ufw is active
# # ufw status
# Status: active

# Remediation candidate
Run the following command to unmask the ufw daemon:
# systemctl unmask ufw.service
Run the following command to enable and start the ufw daemon:
# systemctl --now enable ufw.service
# ufw enable

# TODO: replace the commented/manual steps above with validated bash remediation logic.
