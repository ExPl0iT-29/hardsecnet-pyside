#!/usr/bin/env bash
set -euo pipefail

# CIS Benchmark: CIS Ubuntu Linux 24.04 LTS Benchmark
# Control: 7.2.10 - Ensure local interactive user dot files access is configured
# Source Page: 987
# Confidence: 0.96
# Status: review_required

# Audit guidance extracted from the benchmark
# Run the following script to verify local interactive user dot files:
# -
# Don't include .forward, .rhost, or .netrc files
# -
# Are mode 0644 or more restrictive
# -
# Are owned by the local interactive user
# -
# Are group owned by the user's primary group
# -
# .bash_history is mode 0600 or more restrictive
# Note: If a .netrc file is required, and follows local site policy, it should be mode 0600 or
# more restrictive.
# Page 987
# #!/usr/bin/env bash
# {
# a_output2=(); a_output3=()
# l_maxsize="1000" # Maximum number of local interactive users before
# warning (Default 1,000)
# l_valid_shells="^($( awk -F\/ '$NF != "nologin" {print}' /etc/shells | sed
# -rn '/^\//{s,/,\\\\/,g;p}' | paste -s -d '|' - ))$"
# a_user_and_home=() # Create array with local users and their home
# directories
# while read -r l_local_user l_local_user_home; do # Populate array with
# users and user home location
# [[ -n "$l_local_user" && -n "$l_local_user_home" ]] &&
# a_user_and_home+=("$l_local_user:$l_local_user_home")
# done <<< "$(awk -v pat="$l_valid_shells" -F: '$(NF) ~ pat { print $1 " "
# $(NF-1) }' /etc/passwd)"
# l_asize="${#a_user_and_home[@]}" # Here if we want to look at number of
# users before proceeding
# [ "${#a_user_and_home[@]}" -gt "$l_maxsize" ] && printf '%s\n' "" " **
# INFO **" \
# " - \"$l_asize\" Local interactive users found on the system" \
# " - This may be a long running check" ""
# file_access_chk()
# {
# a_access_out=()
# l_max="$( printf '%o' $(( 0777 & ~$l_mask)) )"
# if [ $(( $l_mode & $l_mask )) -gt 0 ]; then
# a_access_out+=(" - File: 

# Remediation candidate
l_valid_shells="^($( awk -F\/ '$NF != "nologin" {print}' /etc/shells | sed
# rn '/^\//{s,/,\\\\/,g;p}' | paste -s -d '|' - ))$"
$(NF-1) }' /etc/passwd)"

# TODO: replace the commented/manual steps above with validated bash remediation logic.
