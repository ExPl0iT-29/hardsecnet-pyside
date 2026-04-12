#!/usr/bin/env bash
set -euo pipefail

# CIS Benchmark: CIS Ubuntu Linux 24.04 LTS Benchmark
# Control: 6.1.1.2 - Ensure journald log file access is configured
# Source Page: 732
# Confidence: 0.9000000000000001
# Status: review_required

# Audit guidance extracted from the benchmark
# Run the following script to verify:
# -
# systemd-journald logfiles are mode 0640 or more restrictive
# -
# Directories /run/ and /var/lib/systemd/ are mode 0755 or more restrictive
# -
# All other configured directories are mode 2755, 0750, or more restrictive
# Page 732
# #!/usr/bin/env bash
# {
# a_output=() a_output2=()
# l_systemd_config_file="/etc/tmpfiles.d/systemd.conf"
# l_analyze_cmd="$(readlink -f /bin/systemd-analyze)"
# f_file_chk()
# {
# l_maxperm="$( printf '%o' $(( 0777 & ~$l_perm_mask )) )"
# if [ $(( $l_mode & $l_perm_mask )) -le 0 ] || [[ "$l_type" =
# "Directory" && "$l_mode" =~ 275(0|5) ]]; then
# a_out+=(" - $l_type \"$l_logfile\" access is:" \
# " mode: \"$l_mode\", owned by: \"$l_user\", and group owned by:
# \"$l_group\"")
# else
# a_out2+=(" - $l_type \"$l_logfile\" access is:" \
# " mode: \"$l_mode\", owned by: \"$l_user\", and group owned by:
# \"$l_group\"" \
# " should be mode: \"$l_maxperm\" or more restrictive")
# fi
# }
# while IFS= read -r l_file; do
# l_file="$(tr -d '# ' <<< "$l_file")" a_out=() a_out2=()
# l_logfile_perms_line="$(awk '($1~/^(f|d)$/ && $2~/\/\S+/ && $3~/[0-
# 9]{3,}/){print $2 ":" $3 ":" $4 ":" $5}' "$l_file")"
# while IFS=: read -r l_logfile l_mode l_user l_group; do
# if [ -d "$l_logfile" ]; then
# l_perm_mask="0027" l_type="Directory"
# grep -Psq '^(\/run|\/var\/lib\/systemd)\b' <<< "$l_logfile" &&
# l_perm_mask="0022"
# else
# l_perm_mask="0137" l_type="File"
# fi
# grep -Psq '^(\/run|\/var\/lib\/systemd)\b' <<< "$l_logfile" &&
# l_perm_mask="0022"
# f_file_chk
# done <<< "$l_logfile_perms_line"
# [ "${#a_

# Remediation candidate
/usr/lib/tmpfiles.d/systemd.conf to /etc/tmpfiles.d/systemd.conf and

# TODO: replace the commented/manual steps above with validated bash remediation logic.
