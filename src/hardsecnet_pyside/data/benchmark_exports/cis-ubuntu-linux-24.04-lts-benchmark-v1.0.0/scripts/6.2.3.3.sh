#!/usr/bin/env bash
set -euo pipefail

# CIS Benchmark: CIS Ubuntu Linux 24.04 LTS Benchmark
# Control: 6.2.3.3 - Ensure events that modify the sudo log file are collected
# Source Page: 827
# Confidence: 0.96
# Status: review_required

# Audit guidance extracted from the benchmark
# Note: This recommendation requires that the sudo logfile is configured. See guidance
# provided in the recommendation "Ensure sudo log file exists"
# On disk configuration
# Run the following command to check the on disk rules:
# # {
# SUDO_LOG_FILE=$(grep -r logfile /etc/sudoers* | sed -e 's/.*logfile=//;s/,?
# .*//' -e 's/"//g' -e 's|/|\\/|g')
# [ -n "${SUDO_LOG_FILE}" ] && awk "/^ *-w/ \
# &&/"${SUDO_LOG_FILE}"/ \
# &&/ +-p *wa/ \
# &&(/ key= *[!-~]* *$/||/ -k *[!-~]* *$/)" /etc/audit/rules.d/*.rules \
# || printf "ERROR: Variable 'SUDO_LOG_FILE' is unset.\n"
# }
# Verify output of matches:
# -w /var/log/sudo.log -p wa -k sudo_log_file
# Running configuration
# Run the following command to check loaded rules:
# # {
# SUDO_LOG_FILE=$(grep -r logfile /etc/sudoers* | sed -e 's/.*logfile=//;s/,?
# .*//' -e 's/"//g' -e 's|/|\\/|g')
# [ -n "${SUDO_LOG_FILE}" ] && auditctl -l | awk "/^ *-w/ \
# &&/"${SUDO_LOG_FILE}"/ \
# &&/ +-p *wa/ \
# &&(/ key= *[!-~]* *$/||/ -k *[!-~]* *$/)" \
# || printf "ERROR: Variable 'SUDO_LOG_FILE' is unset.\n"
# }
# Verify output matches:
# -w /var/log/sudo.log -p wa -k sudo_log_file
# Page 828

# Remediation candidate
Edit or create a file in the /etc/audit/rules.d/ directory, ending in .rules extension,
SUDO_LOG_FILE=$(grep -r logfile /etc/sudoers* | sed -e 's/.*logfile=//;s/,?
# w ${SUDO_LOG_FILE} -p wa -k sudo_log_file
" >> /etc/audit/rules.d/50-sudo.rules || printf "ERROR: Variable
# if [[ $(auditctl -s | grep "enabled") =~ "2" ]]; then printf "Reboot

# TODO: replace the commented/manual steps above with validated bash remediation logic.
