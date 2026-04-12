#!/usr/bin/env bash
set -euo pipefail

# CIS Benchmark: CIS Ubuntu Linux 24.04 LTS Benchmark
# Control: 1.2.1.1 - Ensure GPG keys are configured
# Source Page: 141
# Confidence: 0.9000000000000001
# Status: review_required

# Audit guidance extracted from the benchmark
# Verify GPG keys are configured correctly for your package manager:
# # apt-key list
# Note:
# -
# apt-key list is deprecated. Manage keyring files in trusted.gpg.d instead
# (see apt-key(8)).
# -
# With the deprecation of apt-key it is recommended to use the Signed-By option
# in sources.list to require a repository to pass apt-secure(8) verification with a
# certain set of keys rather than all trusted keys apt has configured.
# - OR -
# 1. Run the following script and verify GPG keys are configured correctly for your
# package manager:
# #! /usr/bin/env bash
# {
# for file in /etc/apt/trusted.gpg.d/*.{gpg,asc}
# /etc/apt/sources.list.d/*.{gpg,asc} ; do
# if [ -f "$file" ]; then
# echo -e "File: $file"
# gpg --list-packets "$file" 2>/dev/null | awk '/keyid/ &&
# !seen[$NF]++ {print "keyid:", $NF}'
# gpg --list-packets "$file" 2>/dev/null | awk '/Signed-By:/ {print
# "signed-by:", $NF}'
# echo -e
# fi
# done
# }
# 2. REVIEW and VERIFY to ensure that GPG keys are configured correctly for your
# package manager IAW site policy.

# Remediation candidate
# Manual review required
# Convert the remediation guidance below into a validated script action

# TODO: replace the commented/manual steps above with validated bash remediation logic.
