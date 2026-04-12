#!/usr/bin/env bash
set -euo pipefail

# CIS Benchmark: CIS Ubuntu Linux 24.04 LTS Benchmark
# Control: 1.3.1.4 - Ensure all AppArmor Profiles are enforcing
# Source Page: 158
# Confidence: 0.96
# Status: review_required

# Audit guidance extracted from the benchmark
# Run the following commands and verify that profiles are loaded and are not in complain
# mode:
# # apparmor_status | grep profiles
# Review output and ensure that profiles are loaded, and in enforce mode:
# 34 profiles are loaded.
# 34 profiles are in enforce mode.
# 0 profiles are in complain mode.
# 2 processes have profiles defined.
# Run the following command and verify that no processes are unconfined:
# apparmor_status | grep processes
# Review the output and ensure no processes are unconfined:
# 2 processes have profiles defined.
# 2 processes are in enforce mode.
# 0 processes are in complain mode.
# 0 processes are unconfined but have a profile defined.

# Remediation candidate
# aa-enforce /etc/apparmor.d/*

# TODO: replace the commented/manual steps above with validated bash remediation logic.
