#!/usr/bin/env bash
set -euo pipefail

# CIS Benchmark: CIS Ubuntu Linux 24.04 LTS Benchmark
# Control: 1.7.8 - Ensure GDM autorun-never is enabled
# Source Page: 218
# Confidence: 0.96
# Status: review_required

# Audit guidance extracted from the benchmark
# Run the following command to verify that autorun-never is set to true for GDM:
# # gsettings get org.gnome.desktop.media-handling autorun-never
# true
# Page 218

# Remediation candidate
# IF - A user profile exists run the following command to set autorun-never to true for
# OR/IF - A user profile does not exist:
1. create the file /etc/dconf/db/local.d/locks/00-media-autorun with the

# TODO: replace the commented/manual steps above with validated bash remediation logic.
