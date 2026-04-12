#!/usr/bin/env bash
set -euo pipefail

# CIS Benchmark: CIS Ubuntu Linux 24.04 LTS Benchmark
# Control: 2.1.18 - Ensure web server services are not in use
# Source Page: 277
# Confidence: 0.96
# Status: review_required

# Audit guidance extracted from the benchmark
# Run the following command to verify apache2 is not installed:
# # dpkg-query -s apache2 &>/dev/null && echo "apache2 is installed"
# Nothing should be returned.
# Run the following command to verify nginx is not installed:
# # dpkg-query -s nginx &>/dev/null && echo "nginx is installed"
# Nothing should be returned.
# - OR -
# - IF - a package is installed and is required for dependencies:
# Run the following command to verify apache2.socket, apache2.service, and
# nginx.service are not enabled:
# # systemctl is-enabled apache2.socket apache2.service nginx.service
# 2>/dev/null | grep 'enabled'
# Nothing should be returned.
# Run the following command to verify apache2.socket, apache2.service, and
# nginx.service are not active:
# # systemctl is-active apache2.socket apache2.service nginx.service
# 2>/dev/null | grep '^active'
# Nothing should be returned.
# Note:
# -
# Other web server packages may exist. They should also be audited, if not
# required and authorized by local site policy
# -
# If the package is required for a dependency:
# o Ensure the dependent package is approved by local site policy
# o Ensure stopping and masking the service and/or socket meets local site
# policy
# Page 278

# Remediation candidate
# systemctl stop apache2.socket apache2.service nginx.service
# OR -
# IF - a package is installed and is required for dependencies:
# systemctl stop apache2.socket apache2.service nginx.service
# systemctl mask apache2.socket apache2.service nginx.service

# TODO: replace the commented/manual steps above with validated bash remediation logic.
