#!/usr/bin/env bash
set -euo pipefail

# CIS Benchmark: CIS Ubuntu Linux 24.04 LTS Benchmark
# Control: 1.7.6 - Ensure GDM automatic mounting of removable media is disabled
# Source Page: 212
# Confidence: 0.96
# Status: review_required

# Audit guidance extracted from the benchmark
# Run the following commands to verify automatic mounting is disabled:
# # gsettings get org.gnome.desktop.media-handling automount
# false
# # gsettings get org.gnome.desktop.media-handling automount-open
# false
# Page 212

# Remediation candidate
# IF - A user profile exists run the following commands to ensure automatic mounting is
# OR/IF - A user profile does not exist:
1. Create a file /etc/dconf/db/local.d/00-media-automount with following

# TODO: replace the commented/manual steps above with validated bash remediation logic.
