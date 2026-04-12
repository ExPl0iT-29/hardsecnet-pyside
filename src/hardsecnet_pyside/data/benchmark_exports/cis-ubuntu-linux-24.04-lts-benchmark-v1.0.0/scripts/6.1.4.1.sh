#!/usr/bin/env bash
set -euo pipefail

# CIS Benchmark: CIS Ubuntu Linux 24.04 LTS Benchmark
# Control: 6.1.4.1 - Ensure access to all logfiles has been configured
# Source Page: 791
# Confidence: 0.96
# Status: review_required

# Audit guidance extracted from the benchmark
# Run the following script to verify that files in /var/log/ have appropriate permissions
# and ownership:
# #!/usr/bin/env bash
# {
# a_output=(); a_output2=()
# f_file_test_chk()
# {
# a_out2=()
# maxperm="$( printf '%o' $(( 0777 & ~$perm_mask)) )"
# [ $(( $l_mode & $perm_mask )) -gt 0 ] && \
# a_out2+=(" o Mode: \"$l_mode\" should be \"$maxperm\" or more restrictive")
# [[ ! "$l_user" =~ $l_auser ]] && \
# a_out2+=(" o Owned by: \"$l_user\" and should be owned by \"${l_auser//|/ or }\"")
# [[ ! "$l_group" =~ $l_agroup ]] && \
# a_out2+=(" o Group owned by: \"$l_group\" and should be group owned by
# \"${l_agroup//|/ or }\"")
# [ "${#a_out2[@]}" -gt 0 ] && a_output2+=(" - File: \"$l_fname\" is:" "${a_out2[@]}")
# }
# while IFS= read -r -d $'\0' l_file; do
# while IFS=: read -r l_fname l_mode l_user l_group; do
# if grep -Pq -- '\/(apt)\h*$' <<< "$(dirname "$l_fname")"; then
# perm_mask='0133' l_auser="root" l_agroup="(root|adm)"; f_file_test_chk
# else
# case "$(basename "$l_fname")" in
# lastlog | lastlog.* | wtmp | wtmp.* | wtmp-* | btmp | btmp.* | btmp-* | README)
# perm_mask='0113' l_auser="root" l_agroup="(root|utmp)"
# f_file_test_chk ;;
# cloud-init.log* | localmessages* | waagent.log*)
# perm_mask='0133' l_auser="(root|syslog)" l_agroup="(root|adm)"
# file_test_chk ;;
# secure{,*.*,.*,-*} | auth.log | syslog | messages)
# perm_mask='0137' l_auser="(root|syslog)" l_agroup="(root|adm)"
# f_file_test_chk ;;
# SSSD | sssd)
# perm_mask='0117' l_auser="(root|SSSD)" l_agroup="(root|SSSD)"
# f_file_test_chk ;;
# gdm | gdm3)
# perm_mask='0117' l_aus

# Remediation candidate
'$1=="'"$l_user"'" {print $7}' /etc/passwd)\b" /etc/shells; then

# TODO: replace the commented/manual steps above with validated bash remediation logic.
