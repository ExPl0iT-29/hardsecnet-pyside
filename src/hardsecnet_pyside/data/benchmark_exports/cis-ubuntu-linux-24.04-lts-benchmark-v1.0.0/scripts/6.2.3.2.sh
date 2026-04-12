#!/usr/bin/env bash
set -euo pipefail

# CIS Benchmark: CIS Ubuntu Linux 24.04 LTS Benchmark
# Control: 6.2.3.2 - Ensure actions as another user are always logged
# Source Page: 823
# Confidence: 0.96
# Status: review_required

# Audit guidance extracted from the benchmark
# On disk configuration
# Run the following command to check the on disk rules:
# # awk '/^ *-a *always,exit/ \
# &&/ -F *arch=b(32|64)/ \
# &&(/ -F *auid!=unset/||/ -F *auid!=-1/||/ -F *auid!=4294967295/) \
# &&(/ -C *euid!=uid/||/ -C *uid!=euid/) \
# &&/ -S *execve/ \
# &&(/ key= *[!-~]* *$/||/ -k *[!-~]* *$/)' /etc/audit/rules.d/*.rules
# Verify the output matches:
# -a always,exit -F arch=b64 -C euid!=uid -F auid!=unset -S execve -k
# user_emulation
# -a always,exit -F arch=b32 -C euid!=uid -F auid!=unset -S execve -k
# user_emulation
# Running configuration
# Run the following command to check loaded rules:
# # auditctl -l | awk '/^ *-a *always,exit/ \
# &&/ -F *arch=b(32|64)/ \
# &&(/ -F *auid!=unset/||/ -F *auid!=-1/||/ -F *auid!=4294967295/) \
# &&(/ -C *euid!=uid/||/ -C *uid!=euid/) \
# &&/ -S *execve/ \
# &&(/ key= *[!-~]* *$/||/ -k *[!-~]* *$/)'
# Verify the output matches:
# -a always,exit -F arch=b64 -S execve -C uid!=euid -F auid!=-1 -F
# key=user_emulation
# -a always,exit -F arch=b32 -S execve -C uid!=euid -F auid!=-1 -F
# key=user_emulation
# Page 824

# Remediation candidate
Edit or create a file in the /etc/audit/rules.d/ directory, ending in .rules extension,
# a always,exit -F arch=b64 -C euid!=uid -F auid!=unset -S execve -k
# a always,exit -F arch=b32 -C euid!=uid -F auid!=unset -S execve -k
" >> /etc/audit/rules.d/50-user_emulation.rules
# if [[ $(auditctl -s | grep "enabled") =~ "2" ]]; then printf "Reboot

# TODO: replace the commented/manual steps above with validated bash remediation logic.
