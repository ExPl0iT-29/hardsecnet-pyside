#!/usr/bin/env bash
set -euo pipefail

# CIS Benchmark: CIS Ubuntu Linux 24.04 LTS Benchmark
# Control: 2.1.20 - Ensure X window server services are not in use
# Source Page: 284
# Confidence: 0.96
# Status: review_required

# Audit guidance extracted from the benchmark
# - IF - a Graphical Desktop Manager or X-Windows server is not required and approved
# by local site policy:
# Run the following command to Verify X Windows Server is not installed.
# dpkg-query -s xserver-common &>/dev/null && echo "xserver-common is
# installed"
# Nothing should be returned
# Page 284

# Remediation candidate
# IF - a Graphical Desktop Manager or X-Windows server is not required and approved

# TODO: replace the commented/manual steps above with validated bash remediation logic.
