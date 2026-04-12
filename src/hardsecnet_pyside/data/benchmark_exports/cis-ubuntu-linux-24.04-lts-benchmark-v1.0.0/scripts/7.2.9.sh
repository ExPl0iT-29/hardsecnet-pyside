#!/usr/bin/env bash
set -euo pipefail

# CIS Benchmark: CIS Ubuntu Linux 24.04 LTS Benchmark
# Control: 7.2.9 - Ensure local interactive user home directories are configured
# Source Page: 982
# Confidence: 0.96
# Status: review_required

# Audit guidance extracted from the benchmark
# Run the following script to Ensure:
# -
# local interactive user home directories exist
# -
# Ensure local interactive users own their home directories
# -
# Ensure local interactive user home directories are mode 750 or more restrictive
# Page 982
# #!/usr/bin/env bash
# {
# l_output="" l_output2="" l_heout2="" l_hoout2="" l_haout2=""
# l_valid_shells="^($( awk -F\/ '$NF != "nologin" {print}' /etc/shells | sed
# -rn '/^\//{s,/,\\\\/,g;p}' | paste -s -d '|' - ))$"
# unset a_uarr && a_uarr=() # Clear and initialize array
# while read -r l_epu l_eph; do # Populate array with users and user home
# location
# a_uarr+=("$l_epu $l_eph")
# done <<< "$(awk -v pat="$l_valid_shells" -F: '$(NF) ~ pat { print $1 " "
# $(NF-1) }' /etc/passwd)"
# l_asize="${#a_uarr[@]}" # Here if we want to look at number of users
# before proceeding
# [ "$l_asize " -gt "10000" ] && echo -e "\n ** INFO **\n - \"$l_asize\"
# Local interactive users found on the system\n - This may be a long running
# check\n"
# while read -r l_user l_home; do
# if [ -d "$l_home" ]; then
# l_mask='0027'
# l_max="$( printf '%o' $(( 0777 & ~$l_mask)) )"
# while read -r l_own l_mode; do
# [ "$l_user" != "$l_own" ] && l_hoout2="$l_hoout2\n - User:
# \"$l_user\" Home \"$l_home\" is owned by: \"$l_own\""
# if [ $(( $l_mode & $l_mask )) -gt 0 ]; then
# l_haout2="$l_haout2\n - User: \"$l_user\" Home \"$l_home\" is
# mode: \"$l_mode\" should be mode: \"$l_max\" or more restrictive"
# fi
# done <<< "$(stat -Lc '%U %#a' "$l_home")"
# else
# l_heout2="$l_heout2\n - User: \"$l_user\" Home \"$l_home\" Doesn't
# e

# Remediation candidate
create a directory for the user. If undefined, edit /etc/passwd and add the
l_valid_shells="^($( awk -F\/ '$NF != "nologin" {print}' /etc/shells | sed
# rn '/^\//{s,/,\\\\/,g;p}' | paste -s -d '|' - ))$"
$(NF-1) }' /etc/passwd)"

# TODO: replace the commented/manual steps above with validated bash remediation logic.
