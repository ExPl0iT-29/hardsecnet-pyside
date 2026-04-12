#!/usr/bin/env bash
set -euo pipefail

# CIS Benchmark: CIS Ubuntu Linux 24.04 LTS Benchmark
# Control: 6.2.3.12 - Ensure login and logout events are collected
# Source Page: 864
# Confidence: 0.96
# Status: review_required

# Audit guidance extracted from the benchmark
# On disk configuration
# Run the following command to check the on disk rules:
# # awk '/^ *-w/ \
# &&(/\/var\/log\/lastlog/ \
# ||/\/var\/run\/faillock/) \
# &&/ +-p *wa/ \
# &&(/ key= *[!-~]* *$/||/ -k *[!-~]* *$/)' /etc/audit/rules.d/*.rules
# Verify the output matches:
# -w /var/log/lastlog -p wa -k logins
# -w /var/run/faillock -p wa -k logins
# Running configuration
# Run the following command to check loaded rules:
# # auditctl -l | awk '/^ *-w/ \
# &&(/\/var\/log\/lastlog/ \
# ||/\/var\/run\/faillock/) \
# &&/ +-p *wa/ \
# &&(/ key= *[!-~]* *$/||/ -k *[!-~]* *$/)'
# Verify the output matches:
# Page 864
# -w /var/log/lastlog -p wa -k logins
# -w /var/run/faillock -p wa -k logins

# Remediation candidate
Edit or create a file in the /etc/audit/rules.d/ directory, ending in .rules extension,
# w /var/log/lastlog -p wa -k logins
# w /var/run/faillock -p wa -k logins
" >> /etc/audit/rules.d/50-login.rules
# if [[ $(auditctl -s | grep "enabled") =~ "2" ]]; then printf "Reboot

# TODO: replace the commented/manual steps above with validated bash remediation logic.
