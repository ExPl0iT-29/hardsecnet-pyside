#!/usr/bin/env bash
set -euo pipefail

# CIS Benchmark: CIS Ubuntu Linux 24.04 LTS Benchmark
# Control: 6.2.3.1 - Ensure changes to system administration scope (sudoers) is collected
# Source Page: 820
# Confidence: 0.96
# Status: review_required

# Audit guidance extracted from the benchmark
# On disk configuration
# Run the following command to check the on disk rules:
# # awk '/^ *-w/ \
# &&/\/etc\/sudoers/ \
# &&/ +-p *wa/ \
# &&(/ key= *[!-~]* *$/||/ -k *[!-~]* *$/)' /etc/audit/rules.d/*.rules
# Verify the output matches:
# -w /etc/sudoers -p wa -k scope
# -w /etc/sudoers.d -p wa -k scope
# Running configuration
# Run the following command to check loaded rules:
# # auditctl -l | awk '/^ *-w/ \
# &&/\/etc\/sudoers/ \
# &&/ +-p *wa/ \
# &&(/ key= *[!-~]* *$/||/ -k *[!-~]* *$/)'
# Verify the output matches:
# -w /etc/sudoers -p wa -k scope
# -w /etc/sudoers.d -p wa -k scope

# Remediation candidate
Edit or create a file in the /etc/audit/rules.d/ directory, ending in .rules extension,
-w /etc/sudoers -p wa -k scope
-w /etc/sudoers.d -p wa -k scope
" >> /etc/audit/rules.d/50-scope.rules
# if [[ $(auditctl -s | grep "enabled") =~ "2" ]]; then printf "Reboot

# TODO: replace the commented/manual steps above with validated bash remediation logic.
