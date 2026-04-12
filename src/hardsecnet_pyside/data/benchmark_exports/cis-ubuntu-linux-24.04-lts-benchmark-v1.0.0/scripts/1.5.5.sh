#!/usr/bin/env bash
set -euo pipefail

# CIS Benchmark: CIS Ubuntu Linux 24.04 LTS Benchmark
# Control: 1.5.5 - Ensure Automatic Error Reporting is not enabled
# Source Page: 182
# Confidence: 0.96
# Status: review_required

# Audit guidance extracted from the benchmark
# Run the following command to verify that the Apport Error Reporting Service is not
# enabled:
# # dpkg-query -s apport &> /dev/null && grep -Psi --
# '^\h*enabled\h*=\h*[^0]\b' /etc/default/apport
# Nothing should be returned
# Run the following command to verify that the apport service is not active:
# # systemctl is-active apport.service | grep '^active'
# Nothing should be returned

# Remediation candidate
Edit /etc/default/apport and add or edit the enabled parameter to equal 0:
# systemctl stop apport.service
# systemctl mask apport.service
# OR -

# TODO: replace the commented/manual steps above with validated bash remediation logic.
