#!/usr/bin/env bash
set -euo pipefail

# CIS Benchmark: CIS Ubuntu Linux 24.04 LTS Benchmark
# Control: 6.2.3.5 - Ensure events that modify the system's network environment are collected
# Source Page: 835
# Confidence: 0.96
# Status: review_required

# Audit guidance extracted from the benchmark
# On disk configuration
# Run the following commands to check the on disk rules:
# # awk '/^ *-a *always,exit/ \
# &&/ -F *arch=b(32|64)/ \
# &&/ -S/ \
# &&(/sethostname/ \
# ||/setdomainname/) \
# &&(/ key= *[!-~]* *$/||/ -k *[!-~]* *$/)' /etc/audit/rules.d/*.rules
# # awk '/^ *-w/ \
# &&(/\/etc\/issue/ \
# ||/\/etc\/issue.net/ \
# ||/\/etc\/hosts/ \
# ||/\/etc\/network/ \
# ||/\/etc\/netplan/) \
# &&/ +-p *wa/ \
# &&(/ key= *[!-~]* *$/||/ -k *[!-~]* *$/)' /etc/audit/rules.d/*.rules
# Verify the output matches:
# -a always,exit -F arch=b64 -S sethostname,setdomainname -k system-locale
# -a always,exit -F arch=b32 -S sethostname,setdomainname -k system-locale
# -w /etc/issue -p wa -k system-locale
# -w /etc/issue.net -p wa -k system-locale
# -w /etc/hosts -p wa -k system-locale
# -w /etc/networks -p wa -k system-locale
# -w /etc/network -p wa -k system-locale
# -w /etc/netplan -p wa -k system-locale
# Running configuration
# Run the following command to check loaded rules:
# # auditctl -l | awk '/^ *-a *always,exit/ \
# &&/ -F *arch=b(32|64)/ \
# &&/ -S/ \
# &&(/sethostname/ \
# ||/setdomainname/) \
# &&(/ key= *[!-~]* *$/||/ -k *[!-~]* *$/)'
# # auditctl -l | awk '/^ *-w/ \
# &&(/\/etc\/issue/ \
# ||/\/etc\/issue.net/ \
# ||/\/etc\/hosts/ \
# ||/\/etc\/network/ \
# ||/\/etc\/netplan/) \
# &&/ +-p *wa/ \
# &&(/ key= *[!-~]* *$/||/ -k *[!-~]* *$/)'
# Verify the output includes:
# Page 836
# -a always,exit -F arch=b64 -S sethostname,setdomainname -F key=system-locale
# -a always,exit -F arch=b32 -S sethostname,setdomainname -F key=system-locale
# -w /etc/issue -p wa -

# Remediation candidate
Edit or create a file in the /etc/audit/rules.d/ directory, ending in .rules extension,
# a always,exit -F arch=b64 -S sethostname,setdomainname -k system-locale
# a always,exit -F arch=b32 -S sethostname,setdomainname -k system-locale
-w /etc/issue -p wa -k system-locale
-w /etc/issue.net -p wa -k system-locale
-w /etc/hosts -p wa -k system-locale
-w /etc/networks -p wa -k system-locale
-w /etc/network/ -p wa -k system-locale
-w /etc/netplan/ -p wa -k system-locale
" >> /etc/audit/rules.d/50-system_locale.rules
# if [[ $(auditctl -s | grep "enabled") =~ "2" ]]; then printf "Reboot

# TODO: replace the commented/manual steps above with validated bash remediation logic.
