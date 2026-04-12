#!/usr/bin/env bash
set -euo pipefail

# CIS Benchmark: CIS Ubuntu Linux 24.04 LTS Benchmark
# Control: 1.7.7 - Ensure GDM disabling automatic mounting of removable media is not overridden
# Source Page: 215
# Confidence: 0.96
# Status: review_required

# Audit guidance extracted from the benchmark
# Run the following script to verify automatic mounting of removable media is not
# overridden and correctly configured in a configuration file:
# -
# automount=false
# -
# automount-open=false
# #!/usr/bin/env bash
# {
# a_output=() a_output2=()
# check_setting()
# {
# grep -Psrilq "^\h*$1\h*=\h*false\b" /etc/dconf/db/local.d/locks/* 2>
# /dev/null && \
# echo "- \"$3\" is locked and set to false" || echo "- \"$3\" is not
# locked or not set to false"
# }
# declare -A settings=(
# ["automount"]="org/gnome/desktop/media-handling"
# ["automount-open"]="org/gnome/desktop/media-handling"
# )
# for setting in "${!settings[@]}"; do
# result=$(check_setting "$setting" "${settings[$setting]}" "$setting")
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
# Page 216

# Remediation candidate
/etc/dconf/db/local.d/locks/00-media-automount with the following

# TODO: replace the commented/manual steps above with validated bash remediation logic.
