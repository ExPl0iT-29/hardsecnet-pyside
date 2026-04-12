#!/usr/bin/env bash
set -euo pipefail

# CIS Benchmark: CIS Ubuntu Linux 24.04 LTS Benchmark
# Control: 5.1.5 - Ensure sshd Banner is configured
# Source Page: 538
# Confidence: 0.96
# Status: review_required

# Audit guidance extracted from the benchmark
# Run the following command to verify Banner is set:
# # sshd -T | grep -Pi -- '^banner\h+\/\H+'
# Example:
# banner /etc/issue.net
# - IF - Match set statements are used in your environment, specify the connection
# parameters to use for the -T extended test mode and run the audit to verify the setting
# is not incorrectly configured in a match block
# Example additional audit needed for a match block for the user sshuser:
# # sshd -T -C user=sshuser | grep -Pi -- '^banner\h+\/\H+'
# Note: If provided, any Match directives in the configuration file that would apply are
# applied before the configuration is written to standard output. The connection
# parameters are supplied as keyword=value pairs and may be supplied in any order,
# either with multiple -C options or as a comma-separated list. The keywords are addr
# (source address), user (user), host (resolved source host name), laddr (local
# address), lport (local port number), and rdomain (routing domain).
# Run the following command and verify that the contents or the file being called by the
# Banner argument match site policy:
# # [ -e "$(sshd -T | awk '$1 == "banner" {print $2}')" ] && cat "$(sshd -T |
# awk '$1 == "banner" {print $2}')"
# Run the following command and verify no results are returned:
# # grep -Psi -- "(\\\v|\\\r|\\\m|\\\s|\b$(grep '^ID=' /etc/os-release | cut -
# d= -f2 | sed -e 's/"//g')\b)" "$(sshd -T | awk '$1 == "banner" {print $2}')"
# Page 539

# Remediation candidate
Edit the /etc/ssh/sshd_config file to set the Banner parameter above any Include
Banner /etc/issue.net
reported." > "$(sshd -T | awk '$1 == "banner" {print $2}')"

# TODO: replace the commented/manual steps above with validated bash remediation logic.
