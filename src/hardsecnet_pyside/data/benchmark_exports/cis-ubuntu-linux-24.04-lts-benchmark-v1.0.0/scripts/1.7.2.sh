#!/usr/bin/env bash
set -euo pipefail

# CIS Benchmark: CIS Ubuntu Linux 24.04 LTS Benchmark
# Control: 1.7.2 - Ensure GDM login banner is configured
# Source Page: 200
# Confidence: 0.96
# Status: review_required

# Audit guidance extracted from the benchmark
# Run the following commands to verify that the text banner on the login screen is
# enabled and set:
# # gsettings get org.gnome.login-screen banner-message-enable
# true
# # gsettings get org.gnome.login-screen banner-message-text
# 'Authorized uses only. All activity may be monitored and reported'
# Page 200

# Remediation candidate
# IF - A user profile is already created run the following commands to set and enable the
# OR/IF - A user profile does not exist:
1. Create or edit the gdm profile in the /etc/dconf/profile/gdm with the following
2. Create a gdm keyfile for machine-wide settings in /etc/dconf/db/gdm.d/01-

# TODO: replace the commented/manual steps above with validated bash remediation logic.
