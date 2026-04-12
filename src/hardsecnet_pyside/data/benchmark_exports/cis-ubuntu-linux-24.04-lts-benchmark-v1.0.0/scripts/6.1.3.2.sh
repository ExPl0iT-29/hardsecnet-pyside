#!/usr/bin/env bash
set -euo pipefail

# CIS Benchmark: CIS Ubuntu Linux 24.04 LTS Benchmark
# Control: 6.1.3.2 - Ensure rsyslog service is enabled and active
# Source Page: 768
# Confidence: 0.96
# Status: review_required

# Audit guidance extracted from the benchmark
# - IF - rsyslog is being used for logging on the system:
# Run the following command to verify rsyslog.service is enabled:
# # systemctl is-enabled rsyslog
# enabled
# Run the following command to verify rsyslog.service is active:
# # systemctl is-active rsyslog.service
# active

# Remediation candidate
# IF - rsyslog is being used for logging on the system:
# systemctl unmask rsyslog.service
# systemctl enable rsyslog.service
# systemctl start rsyslog.service

# TODO: replace the commented/manual steps above with validated bash remediation logic.
