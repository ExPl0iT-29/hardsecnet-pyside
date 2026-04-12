#!/usr/bin/env bash
set -euo pipefail

# CIS Benchmark: CIS Ubuntu Linux 24.04 LTS Benchmark
# Control: 6.2.3.18 - Ensure successful and unsuccessful attempts to use the usermod command are collected
# Source Page: 886
# Confidence: 0.96
# Status: review_required

# Audit guidance extracted from the benchmark
# On disk configuration
# Run the following command to check the on disk rules:
# # {
# UID_MIN=$(awk '/^\s*UID_MIN/{print $2}' /etc/login.defs)
# [ -n "${UID_MIN}" ] && awk "/^ *-a *always,exit/ \
# &&(/ -F *auid!=unset/||/ -F *auid!=-1/||/ -F *auid!=4294967295/) \
# &&/ -F *auid>=${UID_MIN}/ \
# &&/ -F *perm=x/ \
# &&/ -F *path=\/usr\/sbin\/usermod/ \
# &&(/ key= *[!-~]* *$/||/ -k *[!-~]* *$/)" /etc/audit/rules.d/*.rules \
# || printf "ERROR: Variable 'UID_MIN' is unset.\n"
# }
# Verify the output matches:
# -a always,exit -F path=/usr/sbin/usermod -F perm=x -F auid>=1000 -F
# auid!=unset -k usermod
# Running configuration
# Run the following command to check loaded rules:
# # {
# UID_MIN=$(awk '/^\s*UID_MIN/{print $2}' /etc/login.defs)
# [ -n "${UID_MIN}" ] && auditctl -l | awk "/^ *-a *always,exit/ \
# &&(/ -F *auid!=unset/||/ -F *auid!=-1/||/ -F *auid!=4294967295/) \
# &&/ -F *auid>=${UID_MIN}/ \
# &&/ -F *perm=x/ \
# &&/ -F *path=\/usr\/sbin\/usermod/ \
# &&(/ key= *[!-~]* *$/||/ -k *[!-~]* *$/)" \
# || printf "ERROR: Variable 'UID_MIN' is unset.\n"
# }
# Verify the output matches:
# -a always,exit -S all -F path=/usr/sbin/usermod -F perm=x -F auid>=1000 -F
# auid!=-1 -F key=usermod
# Page 887

# Remediation candidate
Edit or create a file in the /etc/audit/rules.d/ directory, ending in .rules extension,
UID_MIN=$(awk '/^\s*UID_MIN/{print $2}' /etc/login.defs)
# a always,exit -F path=/usr/sbin/usermod -F perm=x -F auid>=${UID_MIN} -F
" >> /etc/audit/rules.d/50-usermod.rules || printf "ERROR: Variable 'UID_MIN'
# if [[ $(auditctl -s | grep "enabled") =~ "2" ]]; then printf "Reboot

# TODO: replace the commented/manual steps above with validated bash remediation logic.
