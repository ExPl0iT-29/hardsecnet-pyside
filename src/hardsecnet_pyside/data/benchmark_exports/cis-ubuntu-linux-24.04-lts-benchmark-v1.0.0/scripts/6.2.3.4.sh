#!/usr/bin/env bash
set -euo pipefail

# CIS Benchmark: CIS Ubuntu Linux 24.04 LTS Benchmark
# Control: 6.2.3.4 - Ensure events that modify date and time information are collected
# Source Page: 831
# Confidence: 0.96
# Status: review_required

# Audit guidance extracted from the benchmark
# On disk configuration
# Run the following command to check the on disk rules:
# # {
# awk '/^ *-a *always,exit/ \
# &&/ -F *arch=b(32|64)/ \
# &&/ -S/ \
# &&(/adjtimex/ \
# ||/settimeofday/ \
# ||/clock_settime/ ) \
# &&(/ key= *[!-~]* *$/||/ -k *[!-~]* *$/)' /etc/audit/rules.d/*.rules
# awk '/^ *-w/ \
# &&/\/etc\/localtime/ \
# &&/ +-p *wa/ \
# &&(/ key= *[!-~]* *$/||/ -k *[!-~]* *$/)' /etc/audit/rules.d/*.rules
# }
# Verify output of matches:
# -a always,exit -F arch=b64 -S adjtimex,settimeofday -k time-change
# -a always,exit -F arch=b32 -S adjtimex,settimeofday -k time-change
# -a always,exit -F arch=b64 -S clock_settime -F a0=0x0 -k time-change
# -a always,exit -F arch=b32 -S clock_settime -F a0=0x0 -k time-change
# -w /etc/localtime -p wa -k time-change
# Running configuration
# Run the following command to check loaded rules:
# # {
# auditctl -l | awk '/^ *-a *always,exit/ \
# &&/ -F *arch=b(32|64)/ \
# &&/ -S/ \
# &&(/adjtimex/ \
# ||/settimeofday/ \
# ||/clock_settime/ ) \
# &&(/ key= *[!-~]* *$/||/ -k *[!-~]* *$/)'
# auditctl -l | awk '/^ *-w/ \
# &&/\/etc\/localtime/ \
# &&/ +-p *wa/ \
# &&(/ key= *[!-~]* *$/||/ -k *[!-~]* *$/)'
# }
# Verify the output includes:
# Page 832
# -a always,exit -F arch=b64 -S adjtimex,settimeofday -F key=time-change
# -a always,exit -F arch=b32 -S settimeofday,adjtimex -F key=time-change
# -a always,exit -F arch=b64 -S clock_settime -F a0=0x0 -F key=time-change
# -a always,exit -F arch=b32 -S clock_settime -F a0=0x0 -F key=time-change
# -w /etc/localtime -p wa -k time-change

# Remediation candidate
Edit or create a file in the /etc/audit/rules.d/ directory, ending in .rules extension,
# a always,exit -F arch=b64 -S adjtimex,settimeofday -k time-change
# a always,exit -F arch=b32 -S adjtimex,settimeofday -k time-change
# a always,exit -F arch=b64 -S clock_settime -F a0=0x0 -k time-change
# a always,exit -F arch=b32 -S clock_settime -F a0=0x0 -k time-change
-w /etc/localtime -p wa -k time-change
" >> /etc/audit/rules.d/50-time-change.rules
# if [[ $(auditctl -s | grep "enabled") =~ "2" ]]; then printf "Reboot

# TODO: replace the commented/manual steps above with validated bash remediation logic.
