#!/usr/bin/env bash
set -euo pipefail

# CIS Benchmark: CIS Ubuntu Linux 24.04 LTS Benchmark
# Control: 1.7.5 - Ensure GDM screen locks cannot be overridden
# Source Page: 209
# Confidence: 0.96
# Status: review_required

# Audit guidance extracted from the benchmark
# Run the following script to verify that the screen lock cannot be overridden:
# #!/usr/bin/env bash
# {
# a_output=() a_output2=()
# f_check_setting()
# {
# grep -Psrilq -- "^\h*$2\b" /etc/dconf/db/local.d/locks/* && \
# echo "- \"$3\" is locked" || echo "- \"$3\" is not locked or not set"
# }
# declare -A settings=(
# ["idle-delay"]="/org/gnome/desktop/session/idle-delay"
# ["lock-delay"]="/org/gnome/desktop/screensaver/lock-delay"
# )
# for setting in "${!settings[@]}"; do
# result=$(f_check_setting "$setting" "${settings[$setting]}" "$setting")
# if [[ $result == *"is not locked"* || $result == *"not set to false"*
# ]]; then
# a_output2+=("$result")
# else
# a_output+=("$result")
# fi
# done
# printf '%s\n' "" "- Audit Result:"
# if [ "${#a_output2[@]}" -gt 0 ]; then
# printf '%s\n' " ** FAIL **" " - Reason(s) for audit failure:"
# "${a_output2[@]}"
# [ "${#a_output[@]}" -gt 0 ] && printf '%s\n' "" "- Correctly set:"
# "${a_output[@]}"
# else
# printf '%s\n' " ** PASS **" "${a_output[@]}"
# fi
# }

# Remediation candidate
/etc/dconf/db/local.d/locks/00-screensaver with the following content:

# TODO: replace the commented/manual steps above with validated bash remediation logic.
