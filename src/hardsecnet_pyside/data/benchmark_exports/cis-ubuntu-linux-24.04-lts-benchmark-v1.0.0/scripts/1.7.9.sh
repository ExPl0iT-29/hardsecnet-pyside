#!/usr/bin/env bash
set -euo pipefail

# CIS Benchmark: CIS Ubuntu Linux 24.04 LTS Benchmark
# Control: 1.7.9 - Ensure GDM autorun-never is not overridden
# Source Page: 221
# Confidence: 0.96
# Status: review_required

# Audit guidance extracted from the benchmark
# Run the following script to verify that autorun-never=true cannot be overridden:
# #!/usr/bin/env bash
# {
# # Function to check and report if a specific setting is locked and set to
# true
# check_setting() {
# grep -Psrilq "^\h*$1\h*=\h*true\b" /etc/dconf/db/local.d/locks/* 2>
# /dev/null && echo "- \"$3\" is locked and set to false" || echo "- \"$3\" is
# not locked or not set to false"
# }
# # Array of settings to check
# declare -A settings=(["autorun-never"]="org/gnome/desktop/media-
# handling")
# # Check GNOME Desktop Manager configurations
# l_output=() l_output2=()
# for setting in "${!settings[@]}"; do
# result=$(check_setting "$setting")
# l_output+=("$result")
# if [[ $result == *"is not locked"* || $result == *"not set to true"*
# ]]; then
# l_output2+=("$result")
# fi
# done
# # Report results
# if [ ${#l_output2[@]} -ne 0 ]; then
# printf '%s\n' "- Audit Result:" " ** FAIL **"
# printf '%s\n' "- Reason(s) for audit failure:"
# for msg in "${l_output2[@]}"; do
# printf '%s\n' "$msg"
# done
# else
# printf '%s\n' "- Audit Result:" " ** PASS **"
# fi
# }
# Page 222

# Remediation candidate
/etc/dconf/db/local.d/locks/00-media-autorun with the following content:

# TODO: replace the commented/manual steps above with validated bash remediation logic.
