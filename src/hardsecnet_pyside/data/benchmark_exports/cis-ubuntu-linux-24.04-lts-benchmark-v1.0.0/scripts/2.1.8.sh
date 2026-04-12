#!/usr/bin/env bash
set -euo pipefail

# CIS Benchmark: CIS Ubuntu Linux 24.04 LTS Benchmark
# Control: 2.1.8 - Ensure message access server services are not in use
# Source Page: 248
# Confidence: 0.96
# Status: review_required

# Audit guidance extracted from the benchmark
# Run the following command to verify dovecot-imapd and dovecot-pop3d are not
# installed:
# # dpkg-query -s dovecot-imapd &>/dev/null && echo "dovecot-imapd is
# installed"
# Nothing should be returned.
# # dpkg-query -s dovecot-pop3d &>/dev/null && echo "dovecot-pop3d is
# installed"
# Nothing should be returned.
# - OR -
# - IF - a package is installed and is required for dependencies:
# Run the following commands to verify dovecot.socket and dovecot.service are not
# enabled:
# # systemctl is-enabled dovecot.socket dovecot.service 2>/dev/null | grep
# 'enabled'
# Nothing should be returned.
# Run the following command to verify dovecot.socket and dovecot.service are not
# active:
# # systemctl is-active dovecot.socket dovecot.service 2>/dev/null | grep
# '^active'
# Nothing should be returned.
# Note: If the package is required for a dependency
# -
# Ensure the dependent package is approved by local site policy
# -
# Ensure stopping and masking the service and/or socket meets local site policy
# Page 249

# Remediation candidate
# systemctl stop dovecot.socket dovecot.service
# OR -
# IF - a package is installed and is required for dependencies:
# systemctl stop dovecot.socket dovecot.service
# systemctl mask dovecot.socket dovecot.service

# TODO: replace the commented/manual steps above with validated bash remediation logic.
