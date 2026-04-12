#!/usr/bin/env bash
set -euo pipefail

# CIS Benchmark: CIS Ubuntu Linux 24.04 LTS Benchmark
# Control: 6.2.3.8 - Ensure events that modify user/group information are collected
# Source Page: 847
# Confidence: 0.96
# Status: review_required

# Audit guidance extracted from the benchmark
# On disk configuration
# Run the following command to check the on disk rules:
# # awk '/^ *-w/ \
# &&(/\/etc\/group/ \
# ||/\/etc\/passwd/ \
# ||/\/etc\/gshadow/ \
# ||/\/etc\/shadow/ \
# ||/\/etc\/security\/opasswd/ \
# ||/\/etc\/nsswitch.conf/ \
# ||/\/etc\/pam.conf/ \
# ||/\/etc\/pam.d/) \
# &&/ +-p *wa/ \
# &&(/ key= *[!-~]* *$/||/ -k *[!-~]* *$/)' /etc/audit/rules.d/*.rules
# Verify the output matches:
# -w /etc/group -p wa -k identity
# -w /etc/passwd -p wa -k identity
# -w /etc/gshadow -p wa -k identity
# -w /etc/shadow -p wa -k identity
# -w /etc/security/opasswd -p wa -k identity
# -w /etc/nsswitch.conf -p wa -k identity
# -w /etc/pam.conf -p wa -k identity
# -w /etc/pam.d -p wa -k identity
# Running configuration
# Run the following command to check loaded rules:
# # auditctl -l | awk '/^ *-w/ \
# &&(/\/etc\/group/ \
# ||/\/etc\/passwd/ \
# ||/\/etc\/gshadow/ \
# ||/\/etc\/shadow/ \
# ||/\/etc\/security\/opasswd/ \
# ||/\/etc\/nsswitch.conf/ \
# ||/\/etc\/pam.conf/ \
# ||/\/etc\/pam.d/) \
# &&/ +-p *wa/ \
# &&(/ key= *[!-~]* *$/||/ -k *[!-~]* *$/)'
# Verify the output matches:
# Page 848
# -w /etc/group -p wa -k identity
# -w /etc/passwd -p wa -k identity
# -w /etc/gshadow -p wa -k identity
# -w /etc/shadow -p wa -k identity
# -w /etc/security/opasswd -p wa -k identity
# -w /etc/nsswitch.conf -p wa -k identity
# -w /etc/pam.conf -p wa -k identity
# -w /etc/pam.d -p wa -k identity

# Remediation candidate
Edit or create a file in the /etc/audit/rules.d/ directory, ending in .rules extension,
-w /etc/group -p wa -k identity
-w /etc/passwd -p wa -k identity
-w /etc/gshadow -p wa -k identity
-w /etc/shadow -p wa -k identity
-w /etc/security/opasswd -p wa -k identity
-w /etc/nsswitch.conf -p wa -k identity
-w /etc/pam.conf -p wa -k identity
-w /etc/pam.d -p wa -k identity
" >> /etc/audit/rules.d/50-identity.rules
# if [[ $(auditctl -s | grep "enabled") =~ "2" ]]; then printf "Reboot

# TODO: replace the commented/manual steps above with validated bash remediation logic.
