#!/usr/bin/env bash
set -euo pipefail

# CIS Benchmark: CIS Ubuntu Linux 24.04 LTS Benchmark
# Control: 6.2.3.14 - Ensure events that modify the system's Mandatory Access Controls are collected
# Source Page: 871
# Confidence: 0.96
# Status: review_required

# Audit guidance extracted from the benchmark
# On disk configuration
# Run the following command to check the on disk rules:
# # awk '/^ *-w/ \
# &&(/\/etc\/apparmor/ \
# ||/\/etc\/apparmor.d/) \
# &&/ +-p *wa/ \
# &&(/ key= *[!-~]* *$/||/ -k *[!-~]* *$/)' /etc/audit/rules.d/*.rules
# Verify the output matches:
# -w /etc/apparmor/ -p wa -k MAC-policy
# -w /etc/apparmor.d/ -p wa -k MAC-policy
# Running configuration
# Run the following command to check loaded rules:
# # auditctl -l | awk '/^ *-w/ \
# &&(/\/etc\/apparmor/ \
# ||/\/etc\/apparmor.d/) \
# &&/ +-p *wa/ \
# &&(/ key= *[!-~]* *$/||/ -k *[!-~]* *$/)'
# Verify the output matches:
# Page 871
# -w /etc/apparmor/ -p wa -k MAC-policy
# -w /etc/apparmor.d/ -p wa -k MAC-policy

# Remediation candidate
Edit or create a file in the /etc/audit/rules.d/ directory, ending in .rules extension,
-w /etc/apparmor/ -p wa -k MAC-policy
-w /etc/apparmor.d/ -p wa -k MAC-policy
" >> /etc/audit/rules.d/50-MAC-policy.rules
# if [[ $(auditctl -s | grep "enabled") =~ "2" ]]; then printf "Reboot

# TODO: replace the commented/manual steps above with validated bash remediation logic.
