#!/usr/bin/env bash
set -euo pipefail

# CIS Benchmark: CIS Ubuntu Linux 24.04 LTS Benchmark
# Control: 1.3.1.3 - Ensure all AppArmor Profiles are in enforce or complain mode
# Source Page: 156
# Confidence: 0.96
# Status: review_required

# Audit guidance extracted from the benchmark
# Run the following command and verify that profiles are loaded, and are in either enforce
# or complain mode:
# # apparmor_status | grep profiles
# Review output and ensure that profiles are loaded, and in either enforce or complain
# mode:
# 37 profiles are loaded.
# 35 profiles are in enforce mode.
# 2 profiles are in complain mode.
# 4 processes have profiles defined.
# Run the following command and verify no processes are unconfined
# # apparmor_status | grep processes
# Review the output and ensure no processes are unconfined:
# 4 processes have profiles defined.
# 4 processes are in enforce mode.
# 0 processes are in complain mode.
# 0 processes are unconfined but have a profile defined.
# Page 156

# Remediation candidate
# aa-enforce /etc/apparmor.d/*
# OR -
# aa-complain /etc/apparmor.d/*

# TODO: replace the commented/manual steps above with validated bash remediation logic.
