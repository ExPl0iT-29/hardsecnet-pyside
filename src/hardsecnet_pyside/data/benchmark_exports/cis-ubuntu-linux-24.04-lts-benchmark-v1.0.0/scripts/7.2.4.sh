#!/usr/bin/env bash
set -euo pipefail

# CIS Benchmark: CIS Ubuntu Linux 24.04 LTS Benchmark
# Control: 7.2.4 - Ensure shadow group is empty
# Source Page: 973
# Confidence: 0.96
# Status: review_required

# Audit guidance extracted from the benchmark
# Run the following commands and verify no results are returned:
# # awk -F: '($1=="shadow") {print $NF}' /etc/group
# # awk -F: '($4 == '"$(getent group shadow | awk -F: '{print $3}' | xargs)"')
# {print " - user: \"" $1 "\" primary group is the shadow group"}' /etc/passwd

# Remediation candidate
# sed -ri 's/(^shadow:[^:]*:[^:]*:)([^:]+$)/\1/' /etc/group

# TODO: replace the commented/manual steps above with validated bash remediation logic.
