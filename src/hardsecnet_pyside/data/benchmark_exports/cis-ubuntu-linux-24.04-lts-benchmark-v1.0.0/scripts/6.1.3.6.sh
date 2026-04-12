#!/usr/bin/env bash
set -euo pipefail

# CIS Benchmark: CIS Ubuntu Linux 24.04 LTS Benchmark
# Control: 6.1.3.6 - Ensure rsyslog is configured to send logs to a remote log host
# Source Page: 781
# Confidence: 0.9000000000000001
# Status: review_required

# Audit guidance extracted from the benchmark
# Run the following script and review the output of rsyslog configuration. Verify that logs
# are sent to a central host used by your organization:
# basic format
# #!/usr/bin/env bash
# {
# l_analyze_cmd="$(readlink -f /bin/systemd-analyze)"
# l_include='\$IncludeConfig' a_config_files=("rsyslog.conf")
# while IFS= read -r l_file; do
# l_conf_loc="$(awk '$1~/^\s*'"$l_include"'$/ {print $2}' "$(tr -d '# '
# <<< "$l_file")" | tail -n 1)"
# [ -n "$l_conf_loc" ] && break
# done < <($l_analyze_cmd cat-config "${a_config_files[@]}" | tac | grep -
# Pio '^\h*#\h*\/[^#\n\r\h]+\.conf\b')
# if [ -d "$l_conf_loc" ]; then
# l_dir="$l_conf_loc" l_ext="*"
# elif grep -Psq '\/\*\.([^#/\n\r]+)?\h*$' <<< "$l_conf_loc" || [ -f
# "$(readlink -f "$l_conf_loc")" ]; then
# l_dir="$(dirname "$l_conf_loc")" l_ext="$(basename "$l_conf_loc")"
# fi
# while read -r -d $'\0' l_file_name; do
# [ -f "$(readlink -f "$l_file_name")" ] && a_config_files+=("$(readlink
# -f "$l_file_name")")
# done < <(find -L "$l_dir" -type f -name "$l_ext" -print0 2>/dev/null)
# for l_logfile in "${a_config_files[@]}"; do
# grep -Hs -- "^*.*[^I][^I]*@" "$l_logfile"
# done
# }
# Output should include @@<FQDN or IP of remote loghost>:
# Example output:
# /etc/rsyslog.d/60-rsyslog.conf:*.* @@loghost.example.com
# - OR -
# Run the following script and review the output of rsyslog configuration. Verify that logs
# are sent to a central host used by your organization:
# advanced format
# Page 782
# #!/usr/bin/env bash
# {
# l_analyze_cmd="$(readlink -f /bin/systemd-analyze)"
# l_include='\$IncludeConfig' a_

# Remediation candidate
[ ! -d "/etc/rsyslog.d/" ] && mkdir /etc/rsyslod.d/
printf '%s\n' "" "${a_parameters[@]}" >> /etc/rsyslog.d/60-rsyslog.conf
# systemctl reload-or-restart rsyslog.service

# TODO: replace the commented/manual steps above with validated bash remediation logic.
