#!/usr/bin/env bash
set -euo pipefail

# CIS Benchmark: CIS Ubuntu Linux 24.04 LTS Benchmark
# Control: 5.4.2.7 - Ensure system accounts do not have a valid login shell
# Source Page: 709
# Confidence: 0.96
# Status: review_required

# Audit guidance extracted from the benchmark
# Run the following command to verify system accounts, except for root, halt, sync,
# shutdown or nfsnobody, do not have a valid login shell:
# #!/usr/bin/env bash
# {
# l_valid_shells="^($(awk -F\/ '$NF != "nologin" {print}' /etc/shells | sed
# -rn '/^\//{s,/,\\\\/,g;p}' | paste -s -d '|' - ))$"
# awk -v pat="$l_valid_shells" -F:
# '($1!~/^(root|halt|sync|shutdown|nfsnobody)$/ && ($3<'"$(awk
# '/^\s*UID_MIN/{print $2}' /etc/login.defs)"' || $3 == 65534) && $(NF) ~ pat)
# {print "Service account: \"" $1 "\" has a valid shell: " $7}' /etc/passwd
# }
# Nothing should be returned
# Page 709

# Remediation candidate
l_valid_shells="^($( awk -F\/ '$NF != "nologin" {print}' /etc/shells | sed
# rn '/^\//{s,/,\\\\/,g;p}' | paste -s -d '|' - ))$"
'/^\s*UID_MIN/{print $2}' /etc/login.defs)"' || $3 == 65534) && $(NF) ~ pat)
{system ("usermod -s '"$(command -v nologin)"' " $1)}' /etc/passwd

# TODO: replace the commented/manual steps above with validated bash remediation logic.
