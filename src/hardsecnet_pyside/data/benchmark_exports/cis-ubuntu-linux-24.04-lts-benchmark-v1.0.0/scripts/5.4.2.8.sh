#!/usr/bin/env bash
set -euo pipefail

# CIS Benchmark: CIS Ubuntu Linux 24.04 LTS Benchmark
# Control: 5.4.2.8 - Ensure accounts without a valid login shell are locked
# Source Page: 712
# Confidence: 0.96
# Status: review_required

# Audit guidance extracted from the benchmark
# Run the following script to verify all non-root accounts without a valid login shell are
# locked.
# #!/usr/bin/env bash
# {
# l_valid_shells="^($(awk -F\/ '$NF != "nologin" {print}' /etc/shells | sed
# -rn '/^\//{s,/,\\\\/,g;p}' | paste -s -d '|' - ))$"
# while IFS= read -r l_user; do
# passwd -S "$l_user" | awk '$2 !~ /^L/ {print "Account: \"" $1 "\" does
# not have a valid login shell and is not locked"}'
# done < <(awk -v pat="$l_valid_shells" -F: '($1 != "root" && $(NF) !~ pat)
# {print $1}' /etc/passwd)
# }
# Nothing should be returned
# Page 712

# Remediation candidate
l_valid_shells="^($(awk -F\/ '$NF != "nologin" {print}' /etc/shells | sed
# rn '/^\//{s,/,\\\\/,g;p}' | paste -s -d '|' - ))$"
{print $1}' /etc/passwd)

# TODO: replace the commented/manual steps above with validated bash remediation logic.
