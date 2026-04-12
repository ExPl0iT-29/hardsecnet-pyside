#!/usr/bin/env bash
set -euo pipefail

# CIS Benchmark: CIS Ubuntu Linux 24.04 LTS Benchmark
# Control: 5.1.7 - Ensure sshd ClientAliveInterval and ClientAliveCountMax are configured
# Source Page: 544
# Confidence: 0.96
# Status: review_required

# Audit guidance extracted from the benchmark
# Run the following command and verify ClientAliveInterval and
# ClientAliveCountMax are greater than zero:
# # sshd -T | grep -Pi -- '(clientaliveinterval|clientalivecountmax)'
# Example Output:
# clientaliveinterval 15
# clientalivecountmax 3
# - IF - Match set statements are used in your environment, specify the connection
# parameters to use for the -T extended test mode and run the audit to verify the setting
# is not incorrectly configured in a match block
# Example additional audit needed for a match block for the user sshuser:
# # sshd -T -C user=sshuser | grep -Pi --
# '(clientaliveinterval|clientalivecountmax)'
# Note: If provided, any Match directives in the configuration file that would apply are
# applied before the configuration is written to standard output. The connection
# parameters are supplied as keyword=value pairs and may be supplied in any order,
# either with multiple -C options or as a comma-separated list. The keywords are addr
# (source address), user (user), host (resolved source host name), laddr (local
# address), lport (local port number), and rdomain (routing domain).

# Remediation candidate
Edit the /etc/ssh/sshd_config file to set the ClientAliveInterval and

# TODO: replace the commented/manual steps above with validated bash remediation logic.
