#!/usr/bin/env bash
set -euo pipefail

# CIS Benchmark: CIS Ubuntu Linux 24.04 LTS Benchmark
# Control: 5.1.3 - Ensure permissions on SSH public host key files are configured
# Source Page: 531
# Confidence: 0.96
# Status: review_required

# Audit guidance extracted from the benchmark
# Run the following command and verify Access does not grant write or execute
# permissions to group or other for all returned files:
# Run the following script to verify SSH public host key files are mode 0644 or more
# restrictive, owned by the root user, and owned by the root group:
# Page 531
# #!/usr/bin/env bash
# {
# a_output=(); a_output2=()
# l_pmask="0133"; l_maxperm="$( printf '%o' $(( 0777 & ~$l_pmask )) )"
# f_file_chk()
# {
# while IFS=: read -r l_file_mode l_file_owner l_file_group; do
# a_out2=()
# if [ $(( $l_file_mode & $l_pmask )) -gt 0 ]; then
# a_out2+=(" Mode: \"$l_file_mode\" should be mode:
# \"$l_maxperm\" or more restrictive")
# fi
# if [ "$l_file_owner" != "root" ]; then
# a_out2+=(" Owned by: \"$l_file_owner\" should be owned by:
# \"root\"")
# fi
# if [ "$l_file_group" != "root" ]; then
# a_out2+=(" Owned by group \"$l_file_group\" should be group
# owned by group: \"root\"")
# fi
# if [ "${#a_out2[@]}" -gt "0" ]; then
# a_output2+=(" - File: \"$l_file\"" "${a_out2[@]}")
# else
# a_output+=(" - File: \"$l_file\"" \
# " Correct: mode: \"$l_file_mode\", owner: \"$l_file_owner\"
# and group owner: \"$l_file_group\" configured")
# fi
# done < <(stat -Lc '%#a:%U:%G' "$l_file")
# }
# while IFS= read -r -d $'\0' l_file; do
# if ssh-keygen -lf &>/dev/null "$l_file"; then
# file "$l_file" | grep -Piq --
# '\bopenssh\h+([^#\n\r]+\h+)?public\h+key\b' && f_file_chk
# fi
# done < <(find -L /etc/ssh -xdev -type f -print0 2>/dev/null)
# if [ "${#a_output2[@]}" -le 0 ]; then
# [ "${#a_output[@]}" -le 0 ] && a_output+=(" - No openSSH public keys

# Remediation candidate
done < <(find -L /etc/ssh -xdev -type f -print0 2>/dev/null)

# TODO: replace the commented/manual steps above with validated bash remediation logic.
