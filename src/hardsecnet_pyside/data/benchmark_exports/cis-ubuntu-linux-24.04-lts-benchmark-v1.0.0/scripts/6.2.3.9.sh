#!/usr/bin/env bash
set -euo pipefail

# CIS Benchmark: CIS Ubuntu Linux 24.04 LTS Benchmark
# Control: 6.2.3.9 - Ensure discretionary access control permission modification events are collected
# Source Page: 851
# Confidence: 0.96
# Status: review_required

# Audit guidance extracted from the benchmark
# Note: Output showing all audited syscalls, e.g. (-a always,exit -F arch=b64 -S
# chmod,fchmod,fchmodat,chmod,fchmod,fchmodat,setxattr,lsetxattr,fsetxattr,removexattr
# ,lremovexattr,fremovexattr -F auid>=1000 -F auid!=unset -F key=perm_mod) is also
# acceptable. These have been separated by function on the displayed output for clarity.
# On disk configuration
# Run the following command to check the on disk rules:
# # {
# UID_MIN=$(awk '/^\s*UID_MIN/{print $2}' /etc/login.defs)
# [ -n "${UID_MIN}" ] && awk "/^ *-a *always,exit/ \
# &&/ -F *arch=b(32|64)/ \
# &&(/ -F *auid!=unset/||/ -F *auid!=-1/||/ -F *auid!=4294967295/) \
# &&/ -S/ \
# &&/ -F *auid>=${UID_MIN}/ \
# &&(/chmod/||/fchmod/||/fchmodat/ \
# ||/chown/||/fchown/||/fchownat/||/lchown/ \
# ||/setxattr/||/lsetxattr/||/fsetxattr/ \
# ||/removexattr/||/lremovexattr/||/fremovexattr/) \
# &&(/ key= *[!-~]* *$/||/ -k *[!-~]* *$/)" /etc/audit/rules.d/*.rules \
# || printf "ERROR: Variable 'UID_MIN' is unset.\n"
# }
# Verify the output matches:
# -a always,exit -F arch=b64 -S chmod,fchmod,fchmodat -F auid>=1000 -F
# auid!=unset -F key=perm_mod
# -a always,exit -F arch=b64 -S chown,fchown,lchown,fchownat -F auid>=1000 -F
# auid!=unset -F key=perm_mod
# -a always,exit -F arch=b32 -S chmod,fchmod,fchmodat -F auid>=1000 -F
# auid!=unset -F key=perm_mod
# -a always,exit -F arch=b32 -S lchown,fchown,chown,fchownat -F auid>=1000 -F
# auid!=unset -F key=perm_mod
# -a always,exit -F arch=b64 -S
# setxattr,lsetxattr,fsetxattr,removexattr,lremovexattr,fremovexattr -F
# auid>=1000 -F auid!=unset -

# Remediation candidate
Edit or create a file in the /etc/audit/rules.d/ directory, ending in .rules extension,
UID_MIN=$(awk '/^\s*UID_MIN/{print $2}' /etc/login.defs)
# a always,exit -F arch=b64 -S chmod,fchmod,fchmodat -F auid>=${UID_MIN} -F
# a always,exit -F arch=b64 -S chown,fchown,lchown,fchownat -F
# a always,exit -F arch=b32 -S chmod,fchmod,fchmodat -F auid>=${UID_MIN} -F
# a always,exit -F arch=b32 -S lchown,fchown,chown,fchownat -F
# a always,exit -F arch=b64 -S
# a always,exit -F arch=b32 -S
" >> /etc/audit/rules.d/50-perm_mod.rules || printf "ERROR: Variable
# if [[ $(auditctl -s | grep "enabled") =~ "2" ]]; then printf "Reboot

# TODO: replace the commented/manual steps above with validated bash remediation logic.
