#!/usr/bin/env bash
set -euo pipefail

# CIS Benchmark: CIS Ubuntu Linux 24.04 LTS Benchmark
# Control: 5.2.2 - Ensure sudo commands use pty
# Source Page: 583
# Confidence: 0.96
# Status: review_required

# Audit guidance extracted from the benchmark
# Verify that sudo can only run other commands from a pseudo terminal.
# Run the following command to verify Defaults use_pty is set:
# # grep -rPi -- '^\h*Defaults\h+([^#\n\r]+,\h*)?use_pty\b' /etc/sudoers*
# Verify the output matches:
# /etc/sudoers:Defaults use_pty
# Run the follow command to to verify Defaults !use_pty is not set:
# # grep -rPi -- '^\h*Defaults\h+([^#\n\r]+,\h*)?!use_pty\b' /etc/sudoers*
# Nothing should be returned
# Page 583

# Remediation candidate
Edit the file /etc/sudoers with visudo or a file in /etc/sudoers.d/ with visudo -f
Edit the file /etc/sudoers with visudo and any files in /etc/sudoers.d/ with visudo
# f <PATH TO FILE> and remove any occurrence of !use_pty
sudo will read each file in /etc/sudoers.d, skipping file names that end in ~ or
Files are parsed in sorted lexical order. That is, /etc/sudoers.d/01_first will
be parsed before /etc/sudoers.d/10_second.
/etc/sudoers.d/1_whoops would be loaded after
/etc/sudoers.d/10_second.

# TODO: replace the commented/manual steps above with validated bash remediation logic.
