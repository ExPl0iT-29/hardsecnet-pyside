#!/usr/bin/env bash
set -euo pipefail

# CIS Benchmark: CIS Ubuntu Linux 24.04 LTS Benchmark
# Control: 5.4.1.4 - Ensure strong password hashing algorithm is configured
# Source Page: 687
# Confidence: 0.96
# Status: review_required

# Audit guidance extracted from the benchmark
# Run the following command to verify the hashing algorithm is sha512 or yescrypt in
# /etc/login.defs:
# # grep -Pi -- '^\h*ENCRYPT_METHOD\h+(SHA512|yescrypt)\b' /etc/login.defs
# Example output:
# ENCRYPT_METHOD SHA512
# - OR -
# ENCRYPT_METHOD YESCRYPT

# Remediation candidate
Edit /etc/login.defs and set the ENCRYPT_METHOD to SHA512 or YESCRYPT:
/etc/login.defs and the PAM configuration

# TODO: replace the commented/manual steps above with validated bash remediation logic.
