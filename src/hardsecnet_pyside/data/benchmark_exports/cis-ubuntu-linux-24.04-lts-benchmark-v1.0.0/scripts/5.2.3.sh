#!/usr/bin/env bash
set -euo pipefail

# CIS Benchmark: CIS Ubuntu Linux 24.04 LTS Benchmark
# Control: 5.2.3 - Ensure sudo log file exists
# Source Page: 586
# Confidence: 0.96
# Status: review_required

# Audit guidance extracted from the benchmark
# Run the following command to verify that sudo has a custom log file configured:
# # grep -rPsi
# "^\h*Defaults\h+([^#]+,\h*)?logfile\h*=\h*(\"|\')?\H+(\"|\')?(,\h*\H+\h*)*\h*
# (#.*)?$" /etc/sudoers*
# Verify the output matches:
# Defaults logfile="/var/log/sudo.log"
# Page 586

# Remediation candidate
Edit the file /etc/sudoers or a file in /etc/sudoers.d/ with visudo or visudo -f
sudo will read each file in /etc/sudoers.d, skipping file names that end in ~ or
Files are parsed in sorted lexical order. That is, /etc/sudoers.d/01_first will
be parsed before /etc/sudoers.d/10_second.
/etc/sudoers.d/1_whoops would be loaded after
/etc/sudoers.d/10_second.

# TODO: replace the commented/manual steps above with validated bash remediation logic.
