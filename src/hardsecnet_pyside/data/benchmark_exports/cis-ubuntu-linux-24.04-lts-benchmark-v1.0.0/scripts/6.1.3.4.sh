#!/usr/bin/env bash
set -euo pipefail

# CIS Benchmark: CIS Ubuntu Linux 24.04 LTS Benchmark
# Control: 6.1.3.4 - Ensure rsyslog log file creation mode is configured
# Source Page: 774
# Confidence: 0.96
# Status: review_required

# Audit guidance extracted from the benchmark
# Run the following command
# Run the following script to verify $FileCreateMode to set to mode 0640 or more
# restrictive:
# Page 774
# #!/usr/bin/env bash
# {
# a_output=() a_output2=() l_analyze_cmd="$(readlink -f /bin/systemd-analyze)"
# l_include='\$IncludeConfig' a_config_files=("rsyslog.conf")
# l_parameter_name='\$FileCreateMode'
# f_parameter_chk()
# {
# l_perm_mask="0137"; l_maxperm="$( printf '%o' $(( 0777 & ~$l_perm_mask )) )"
# l_mode="$(awk '{print $2}' <<< "$l_used_parameter_setting" | xargs)"
# if [ $(( $l_mode & $l_perm_mask )) -gt 0 ]; then
# a_output2+=(" - Parameter: \"${l_parameter_name//\\/}\" is incorrectly set
# to mode: \"$l_file_mode\"" \
# " in the file: \"$l_file\"" " Should be mode: \"$l_maxperm\" or more
# restrictive")
# else
# a_output+=(" - Parameter: \"${l_parameter_name//\\/}\" is correctly set to
# mode: \"$l_file_mode\"" \
# " in the file: \"$l_file\"" " Should be mode: \"$l_maxperm\" or more
# restrictive")
# fi
# }
# while IFS= read -r l_file; do
# l_conf_loc="$(awk '$1~/^\s*'"$l_include"'$/ {print $2}' "$(tr -d '# ' <<<
# "$l_file")" | tail -n 1)"
# [ -n "$l_conf_loc" ] && break
# done < <($l_analyze_cmd cat-config "${a_config_files[*]}" | tac | grep -Pio
# '^\h*#\h*\/[^#\n\r\h]+\.conf\b')
# if [ -d "$l_conf_loc" ]; then
# l_dir="$l_conf_loc" l_ext="*"
# elif grep -Psq '\/\*\.([^#/\n\r]+)?\h*$' <<< "$l_conf_loc" || [ -f "$(readlink -f
# "$l_conf_loc")" ]; then
# l_dir="$(dirname "$l_conf_loc")" l_ext="$(basename "$l_conf_loc")"
# fi
# while read -r -d $'\0' l_file_name; do
# [ -f "$(readlink -f "$l_file_name")" ]

# Remediation candidate
Edit either /etc/rsyslog.conf or a dedicated .conf file in /etc/rsyslog.d/ and set
[ ! -d "/etc/rsyslog.d/" ] && mkdir /etc/rsyslog.d/
printf '%s\n' "" "\$FileCreateMode 0640" >> /etc/rsyslog.d/60-rsyslog.conf
# systemctl reload-or-restart rsyslog

# TODO: replace the commented/manual steps above with validated bash remediation logic.
