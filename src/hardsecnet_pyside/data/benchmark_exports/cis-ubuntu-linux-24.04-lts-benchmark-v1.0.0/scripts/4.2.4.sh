#!/usr/bin/env bash
set -euo pipefail

# CIS Benchmark: CIS Ubuntu Linux 24.04 LTS Benchmark
# Control: 4.2.4 - Ensure ufw loopback traffic is configured
# Source Page: 455
# Confidence: 0.96
# Status: review_required

# Audit guidance extracted from the benchmark
# Run the following command and verify loopback interface to accept traffic:
# # grep -P -- 'lo|127.0.0.0' /etc/ufw/before.rules
# Output includes:
# # allow all on loopback
# -A ufw-before-input -i lo -j ACCEPT
# -A ufw-before-output -o lo -j ACCEPT
# Run the following command and verify all other interfaces deny traffic to the loopback
# network (127.0.0.0/8 for IPv4 and ::1/128 for IPv6)
# # ufw status verbose
# To Action From
# -- ------ ----
# Anywhere DENY IN 127.0.0.0/8
# Anywhere (v6) DENY IN ::1
# Note: ufw status only shows rules added with ufw and not the rules found in the
# /etc/ufw rules files where allow all on loopback is configured by default.
# Page 455

# Remediation candidate
# ufw allow in on lo
# ufw allow out on lo
# ufw deny in from 127.0.0.0/8
# ufw deny in from ::1

# TODO: replace the commented/manual steps above with validated bash remediation logic.
