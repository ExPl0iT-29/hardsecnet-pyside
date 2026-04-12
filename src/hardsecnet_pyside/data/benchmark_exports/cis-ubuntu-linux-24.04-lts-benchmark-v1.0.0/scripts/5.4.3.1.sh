#!/usr/bin/env bash
set -euo pipefail

# CIS Benchmark: CIS Ubuntu Linux 24.04 LTS Benchmark
# Control: 5.4.3.1 - Ensure nologin is not listed in /etc/shells
# Source Page: 715
# Confidence: 0.96
# Status: review_required

# Audit guidance extracted from the benchmark
# Run the following command to verify that nologin is not listed in the /etc/shells file:
# # grep -Ps '^\h*([^#\n\r]+)?\/nologin\b' /etc/shells
# Nothing should be returned

# Remediation candidate
Edit /etc/shells and remove any lines that include nologin

# TODO: replace the commented/manual steps above with validated bash remediation logic.
