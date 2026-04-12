#!/usr/bin/env bash
set -euo pipefail

# CIS Benchmark: CIS Ubuntu Linux 24.04 LTS Benchmark
# Control: 5.1.2 - Ensure permissions on SSH private host key files are configured
# Source Page: 527
# Confidence: 0.96
# Status: review_required

# Audit guidance extracted from the benchmark
# Run the following script to verify SSH private host key files are owned by the root user
# and either:
# -
# owned by the group root and mode 0600 or more restrictive
# - OR -
# -
# owned by the group designated to own openSSH private keys and mode 0640 or
# more restrictive
# #!/usr/bin/env bash
# {
# a_output=(); a_output2=()
# l_ssh_group_name="$(awk -F: '($1 ~ /^(ssh_keys|_?ssh)$/) {print $1}' /etc/group)"
# f_file_chk()
# {
# while IFS=: read -r l_file_mode l_file_owner l_file_group; do
# a_out2=()
# [ "$l_file_group" = "$l_ssh_group_name" ] && l_pmask="0137" || l_pmask="0177"
# l_maxperm="$( printf '%o' $(( 0777 & ~$l_pmask )) )"
# if [ $(( $l_file_mode & $l_pmask )) -gt 0 ]; then
# a_out2+=(" Mode: \"$l_file_mode\" should be mode: \"$l_maxperm\" or
# more restrictive")
# fi
# if [ "$l_file_owner" != "root" ]; then
# a_out2+=(" Owned by: \"$l_file_owner\" should be owned by \"root\"")
# fi
# if [[ ! "$l_file_group" =~ ($l_ssh_group_name|root) ]]; then
# a_out2+=(" Owned by group \"$l_file_group\" should be group owned by:
# \"$l_ssh_group_name\" or \"root\"")
# fi
# if [ "${#a_out2[@]}" -gt "0" ]; then
# a_output2+=(" - File: \"$l_file\"${a_out2[@]}")
# else
# a_output+=(" - File: \"$l_file\"" \
# " Correct: mode: \"$l_file_mode\", owner: \"$l_file_owner\" and group
# owner: \"$l_file_group\" configured")
# fi
# done < <(stat -Lc '%#a:%U:%G' "$l_file")
# }
# while IFS= read -r -d $'\0' l_file; do
# if ssh-keygen -lf &>/dev/null "$l_file"; then
# file "$l_file" | grep -Piq -- '\bopenssh\h+([^#\n\r]+\h+)?private\h+key\b' &&
# f_file_chk
# fi
# done < <(fin

# Remediation candidate
{print $1}' /etc/group)"
done < <(find -L /etc/ssh -xdev -type f -print0 2>/dev/null)

# TODO: replace the commented/manual steps above with validated bash remediation logic.
