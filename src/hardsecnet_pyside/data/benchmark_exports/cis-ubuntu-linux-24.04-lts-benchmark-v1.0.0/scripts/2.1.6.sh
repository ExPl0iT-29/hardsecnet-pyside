#!/usr/bin/env bash
set -euo pipefail

# CIS Benchmark: CIS Ubuntu Linux 24.04 LTS Benchmark
# Control: 2.1.6 - Ensure ftp server services are not in use
# Source Page: 243
# Confidence: 0.96
# Status: review_required

# Audit guidance extracted from the benchmark
# Run the following command to verify vsftpd is not installed:
# # dpkg-query -s vsftpd &>/dev/null && echo "vsftpd is installed"
# Nothing should be returned.
# - OR -
# - IF - the package is required for dependencies:
# Run the following command to verify vsftpd service is not enabled:
# # systemctl is-enabled vsftpd.service 2>/dev/null | grep 'enabled'
# Nothing should be returned.
# Run the following command to verify the vsftpd service is not active:
# # systemctl is-active vsftpd.service 2>/dev/null | grep '^active'
# Nothing should be returned.
# Note:
# -
# Other ftp server packages may exist. They should also be audited, if not required
# and authorized by local site policy
# -
# If the package is required for a dependency:
# o Ensure the dependent package is approved by local site policy
# o Ensure stopping and masking the service and/or socket meets local site
# policy

# Remediation candidate
# systemctl stop vsftpd.service
# OR -
# IF - the vsftpd package is required as a dependency:
# systemctl stop vsftpd.service
# systemctl mask vsftpd.service

# TODO: replace the commented/manual steps above with validated bash remediation logic.
