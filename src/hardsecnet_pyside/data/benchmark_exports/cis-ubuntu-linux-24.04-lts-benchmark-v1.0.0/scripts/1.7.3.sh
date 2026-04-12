#!/usr/bin/env bash
set -euo pipefail

# CIS Benchmark: CIS Ubuntu Linux 24.04 LTS Benchmark
# Control: 1.7.3 - Ensure GDM disable-user-list option is enabled
# Source Page: 203
# Confidence: 0.96
# Status: review_required

# Audit guidance extracted from the benchmark
# Run the following command and to verify that the disable-user-list option is
# enabled:
# # gsettings get org.gnome.login-screen disable-user-list
# true
# Page 203

# Remediation candidate
# IF - A user profile exists run the following command to enable the disable-user-
# OR/IF - A user profile does not exist:
1. Create or edit the gdm profile in /etc/dconf/profile/gdm with the following
2. Create a gdm keyfile for machine-wide settings in /etc/dconf/db/gdm.d/00-

# TODO: replace the commented/manual steps above with validated bash remediation logic.
