#!/usr/bin/env bash
set -euo pipefail

# CIS Benchmark: CIS Ubuntu Linux 24.04 LTS Benchmark
# Control: 6.2.3.11 - Ensure session initiation information is collected
# Source Page: 860
# Confidence: 0.96
# Status: review_required

# Audit guidance extracted from the benchmark
# On disk configuration
# Run the following command to check the on disk rules:
# # awk '/^ *-w/ \
# &&(/\/var\/run\/utmp/ \
# ||/\/var\/log\/wtmp/ \
# ||/\/var\/log\/btmp/) \
# &&/ +-p *wa/ \
# &&(/ key= *[!-~]* *$/||/ -k *[!-~]* *$/)' /etc/audit/rules.d/*.rules
# Verify the output matches:
# -w /var/run/utmp -p wa -k session
# -w /var/log/wtmp -p wa -k session
# -w /var/log/btmp -p wa -k session
# Running configuration
# Run the following command to check loaded rules:
# # auditctl -l | awk '/^ *-w/ \
# &&(/\/var\/run\/utmp/ \
# ||/\/var\/log\/wtmp/ \
# ||/\/var\/log\/btmp/) \
# &&/ +-p *wa/ \
# &&(/ key= *[!-~]* *$/||/ -k *[!-~]* *$/)'
# Verify the output matches:
# -w /var/run/utmp -p wa -k session
# -w /var/log/wtmp -p wa -k session
# -w /var/log/btmp -p wa -k session
# Page 861

# Remediation candidate
Edit or create a file in the /etc/audit/rules.d/ directory, ending in .rules extension,
# w /var/run/utmp -p wa -k session
# w /var/log/wtmp -p wa -k session
# w /var/log/btmp -p wa -k session
" >> /etc/audit/rules.d/50-session.rules
# if [[ $(auditctl -s | grep "enabled") =~ "2" ]]; then printf "Reboot

# TODO: replace the commented/manual steps above with validated bash remediation logic.
