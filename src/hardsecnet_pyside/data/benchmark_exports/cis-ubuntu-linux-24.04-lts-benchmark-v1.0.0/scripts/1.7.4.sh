#!/usr/bin/env bash
set -euo pipefail

# CIS Benchmark: CIS Ubuntu Linux 24.04 LTS Benchmark
# Control: 1.7.4 - Ensure GDM screen locks when the user is idle
# Source Page: 206
# Confidence: 0.96
# Status: review_required

# Audit guidance extracted from the benchmark
# Run the following commands to verify that the screen locks when the user is idle:
# # gsettings get org.gnome.desktop.screensaver lock-delay
# uint32 5
# # gsettings get org.gnome.desktop.session idle-delay
# uint32 900
# Notes:
# -
# lock-delay=uint32 {n} - should be 5 seconds or less and follow local site
# policy
# -
# idle-delay=uint32 {n} - Should be 900 seconds (15 minutes) or less, not 0
# (disabled) and follow local site policy
# Page 206

# Remediation candidate
# IF - A user profile is already created run the following commands to enable screen
# OR/IF- A user profile does not exist:
1. Create or edit the user profile in the /etc/dconf/profile/ and verify it includes
2. Create the directory /etc/dconf/db/local.d/ if it doesn't already exist:
3. Create the key file /etc/dconf/db/local.d/00-screensaver to provide

# TODO: replace the commented/manual steps above with validated bash remediation logic.
