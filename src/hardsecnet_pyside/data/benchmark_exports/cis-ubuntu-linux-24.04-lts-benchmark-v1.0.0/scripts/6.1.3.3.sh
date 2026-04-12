#!/usr/bin/env bash
set -euo pipefail

# CIS Benchmark: CIS Ubuntu Linux 24.04 LTS Benchmark
# Control: 6.1.3.3 - Ensure journald is configured to send logs to rsyslog
# Source Page: 770
# Confidence: 0.96
# Status: review_required

# Audit guidance extracted from the benchmark
# - IF - rsyslog is the preferred method for capturing logs
# Run the following script to verify that logs are forwarded to rsyslog by setting
# ForwardToSyslog to yes in the systemd-journald configuration:
# Page 770
# #!/usr/bin/env bash
# {
# a_output=() a_output2=() l_analyze_cmd="$(readlink -f /bin/systemd-analyze)"
# l_systemd_config_file="systemd/journald.conf"
# a_parameters=("ForwardToSyslog=yes")
# f_config_file_parameter_chk()
# {
# l_used_parameter_setting=""
# while IFS= read -r l_file; do
# l_file="$(tr -d '# ' <<< "$l_file")"
# l_used_parameter_setting="$(grep -PHs -- '^\h*'"$l_parameter_name"'\b'
# "$l_file" | tail -n 1)"
# [ -n "$l_used_parameter_setting" ] && break
# done < <($l_analyze_cmd cat-config "$l_systemd_config_file" | tac | grep -Pio
# '^\h*#\h*\/[^#\n\r\h]+\.conf\b')
# if [ -n "$l_used_parameter_setting" ]; then
# while IFS=: read -r l_file_name l_file_parameter; do
# while IFS="=" read -r l_file_parameter_name l_file_parameter_value; do
# if grep -Pq -- "$l_parameter_value" <<< "$l_file_parameter_value"; then
# a_output+=(" - Parameter: \"${l_file_parameter_name// /}\"" \
# " correctly set to: \"${l_file_parameter_value// /}\"" \
# " in the file: \"$l_file_name\"")
# else
# a_output2+=(" - Parameter: \"${l_file_parameter_name// /}\"" \
# " incorrectly set to: \"${l_file_parameter_value// /}\"" \
# " in the file: \"$l_file_name\"" \
# " Should be set to: \"$l_value_out\"")
# fi
# done <<< "$l_file_parameter"
# done <<< "$l_used_parameter_setting"
# else
# a_output2+=(" - Parameter: \"$l_parameter_name\" is not set in 

# Remediation candidate
# IF - Journald is the preferred method for capturing logs, this section and
# IF - rsyslog is the preferred method for capturing logs:
/etc/systemd/journald.conf or a file in /etc/systemd/journald.conf.d/ ending
[ ! -d /etc/systemd/journald.conf.d/ ] && mkdir
/etc/systemd/journald.conf.d/
if grep -Psq -- '^\h*\[Journal\]' /etc/systemd/journald.conf.d/60-
printf '%s\n' "" "${a_settings[@]}" >> /etc/systemd/journald.conf.d/60-
/etc/systemd/journald.conf.d/60-journald.conf
# systemctl reload-or-restart systemd-journald.service

# TODO: replace the commented/manual steps above with validated bash remediation logic.
