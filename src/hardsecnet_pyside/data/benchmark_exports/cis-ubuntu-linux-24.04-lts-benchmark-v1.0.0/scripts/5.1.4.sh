#!/usr/bin/env bash
set -euo pipefail

# CIS Benchmark: CIS Ubuntu Linux 24.04 LTS Benchmark
# Control: 5.1.4 - Ensure sshd access is configured
# Source Page: 535
# Confidence: 0.96
# Status: review_required

# Audit guidance extracted from the benchmark
# Run the following command and verify the output:
# # sshd -T | grep -Pi -- '^\h*(allow|deny)(users|groups)\h+\H+'
# Verify that the output matches at least one of the following lines:
# allowusers <userlist>
# -OR-
# allowgroups <grouplist>
# -OR-
# denyusers <userlist>
# -OR-
# denygroups <grouplist>
# Review the list(s) to ensure included users and/or groups follow local site policy
# - IF - Match set statements are used in your environment, specify the connection
# parameters to use for the -T extended test mode and run the audit to verify the setting
# is not incorrectly configured in a match block
# Example additional audit needed for a match block for the user sshuser:
# # sshd -T -C user=sshuser | grep -Pi --
# '^\h*(allow|deny)(users|groups)\h+\H+'
# Note: If provided, any Match directives in the configuration file that would apply are
# applied before the configuration is written to standard output. The connection
# parameters are supplied as keyword=value pairs and may be supplied in any order,
# either with multiple -C options or as a comma-separated list. The keywords are addr
# (source address), user (user), host (resolved source host name), laddr (local
# address), lport (local port number), and rdomain (routing domain).

# Remediation candidate
Edit the /etc/ssh/sshd_config file to set one or more of the parameters above any
# AND/OR -

# TODO: replace the commented/manual steps above with validated bash remediation logic.
