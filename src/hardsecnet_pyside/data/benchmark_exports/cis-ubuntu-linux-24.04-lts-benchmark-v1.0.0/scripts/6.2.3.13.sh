#!/usr/bin/env bash
set -euo pipefail

# CIS Benchmark: CIS Ubuntu Linux 24.04 LTS Benchmark
# Control: 6.2.3.13 - Ensure file deletion events by users are collected
# Source Page: 867
# Confidence: 0.96
# Status: review_required

# Audit guidance extracted from the benchmark
# On disk configuration
# Run the following command to check the on disk rules:
# # {
# UID_MIN=$(awk '/^\s*UID_MIN/{print $2}' /etc/login.defs)
# [ -n "${UID_MIN}" ] && awk "/^ *-a *always,exit/ \
# &&/ -F *arch=b(32|64)/ \
# &&(/ -F *auid!=unset/||/ -F *auid!=-1/||/ -F *auid!=4294967295/) \
# &&/ -F *auid>=${UID_MIN}/ \
# &&/ -S/ \
# &&(/unlink/||/rename/||/unlinkat/||/renameat/) \
# &&(/ key= *[!-~]* *$/||/ -k *[!-~]* *$/)" /etc/audit/rules.d/*.rules \
# || printf "ERROR: Variable 'UID_MIN' is unset.\n"
# }
# Verify the output matches:
# -a always,exit -F arch=b64 -S unlink,unlinkat,rename,renameat -F auid>=1000 -
# F auid!=unset -k delete
# -a always,exit -F arch=b32 -S unlink,unlinkat,rename,renameat -F auid>=1000 -
# F auid!=unset -k delete
# Running configuration
# Run the following command to check loaded rules:
# # {
# UID_MIN=$(awk '/^\s*UID_MIN/{print $2}' /etc/login.defs)
# [ -n "${UID_MIN}" ] && auditctl -l | awk "/^ *-a *always,exit/ \
# &&/ -F *arch=b(32|64)/ \
# &&(/ -F *auid!=unset/||/ -F *auid!=-1/||/ -F *auid!=4294967295/) \
# &&/ -F *auid>=${UID_MIN}/ \
# &&/ -S/ \
# &&(/unlink/||/rename/||/unlinkat/||/renameat/) \
# &&(/ key= *[!-~]* *$/||/ -k *[!-~]* *$/)" \
# || printf "ERROR: Variable 'UID_MIN' is unset.\n"
# }
# Verify the output matches:
# -a always,exit -F arch=b64 -S rename,unlink,unlinkat,renameat -F auid>=1000 -
# F auid!=-1 -F key=delete
# -a always,exit -F arch=b32 -S unlink,rename,unlinkat,renameat -F auid>=1000 -
# F auid!=-1 -F key=delete
# Page 868

# Remediation candidate
Edit or create a file in the /etc/audit/rules.d/ directory, ending in .rules extension,
UID_MIN=$(awk '/^\s*UID_MIN/{print $2}' /etc/login.defs)
# a always,exit -F arch=b64 -S rename,unlink,unlinkat,renameat -F
# a always,exit -F arch=b32 -S rename,unlink,unlinkat,renameat -F
" >> /etc/audit/rules.d/50-delete.rules || printf "ERROR: Variable 'UID_MIN'
# if [[ $(auditctl -s | grep "enabled") =~ "2" ]]; then printf "Reboot

# TODO: replace the commented/manual steps above with validated bash remediation logic.
