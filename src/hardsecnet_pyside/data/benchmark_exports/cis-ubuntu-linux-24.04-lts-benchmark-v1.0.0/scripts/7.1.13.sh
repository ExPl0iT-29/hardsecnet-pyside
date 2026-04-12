#!/usr/bin/env bash
set -euo pipefail

# CIS Benchmark: CIS Ubuntu Linux 24.04 LTS Benchmark
# Control: 7.1.13 - Ensure SUID and SGID files are reviewed
# Source Page: 962
# Confidence: 0.9000000000000001
# Status: review_required

# Audit guidance extracted from the benchmark
# Run the following script to generate a list of SUID and SGID files:
# #!/usr/bin/env bash
# {
# l_output="" l_output2=""
# a_suid=(); a_sgid=() # initialize arrays
# while IFS= read -r l_mount; do
# while IFS= read -r -d $'\0' l_file; do
# if [ -e "$l_file" ]; then
# l_mode="$(stat -Lc '%#a' "$l_file")"
# [ $(( $l_mode & 04000 )) -gt 0 ] && a_suid+=("$l_file")
# [ $(( $l_mode & 02000 )) -gt 0 ] && a_sgid+=("$l_file")
# fi
# done < <(find "$l_mount" -xdev -type f \( -perm -2000 -o -perm -4000 \)
# -print0 2>/dev/null)
# done < <(findmnt -Dkerno fstype,target,options | awk '($1 !~
# /^\s*(nfs|proc|smb|vfat|iso9660|efivarfs|selinuxfs)/ && $2 !~
# /^\/run\/user\// && $3 !~/noexec/ && $3 !~/nosuid/) {print $2}')
# if ! (( ${#a_suid[@]} > 0 )); then
# l_output="$l_output\n - No executable SUID files exist on the system"
# else
# l_output2="$l_output2\n - List of \"$(printf '%s' "${#a_suid[@]}")\"
# SUID executable files:\n$(printf '%s\n' "${a_suid[@]}")\n - end of list -\n"
# fi
# if ! (( ${#a_sgid[@]} > 0 )); then
# l_output="$l_output\n - No SGID files exist on the system"
# else
# l_output2="$l_output2\n - List of \"$(printf '%s' "${#a_sgid[@]}")\"
# SGID executable files:\n$(printf '%s\n' "${a_sgid[@]}")\n - end of list -\n"
# fi
# [ -n "$l_output2" ] && l_output2="$l_output2\n- Review the preceding
# list(s) of SUID and/or SGID files to\n- ensure that no rogue programs have
# been introduced onto the system.\n"
# unset a_arr; unset a_suid; unset a_sgid # Remove arrays
# # If l_output2 is empty, Nothing to report
# if [ -z "$l_output2" ]; then

# Remediation candidate
# Manual review required
# Convert the remediation guidance below into a validated script action

# TODO: replace the commented/manual steps above with validated bash remediation logic.
