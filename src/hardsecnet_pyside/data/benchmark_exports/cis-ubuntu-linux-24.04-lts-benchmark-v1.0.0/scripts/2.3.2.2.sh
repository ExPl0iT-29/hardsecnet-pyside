#!/usr/bin/env bash
set -euo pipefail

# CIS Benchmark: CIS Ubuntu Linux 24.04 LTS Benchmark
# Control: 2.3.2.2 - Ensure systemd-timesyncd is enabled and running
# Source Page: 317
# Confidence: 0.96
# Status: review_required

# Audit guidance extracted from the benchmark
# - IF - systemd-timesyncd is in use on the system, run the following commands:
# Run the following command to verify that the systemd-timesyncd service is enabled:
# # systemctl is-enabled systemd-timesyncd.service
# enabled
# Run the following command to verify that the systemd-timesyncd service is active:
# # systemctl is-active systemd-timesyncd.service
# active
# Page 317

# Remediation candidate
# IF - systemd-timesyncd is in use on the system, run the following commands:
# systemctl unmask systemd-timesyncd.service
# systemctl --now enable systemd-timesyncd.service
# OR -
# systemctl --now mask systemd-timesyncd.service

# TODO: replace the commented/manual steps above with validated bash remediation logic.
