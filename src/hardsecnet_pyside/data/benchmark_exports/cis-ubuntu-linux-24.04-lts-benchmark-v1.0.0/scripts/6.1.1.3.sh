#!/usr/bin/env bash
set -euo pipefail

# CIS Benchmark: CIS Ubuntu Linux 24.04 LTS Benchmark
# Control: 6.1.1.3 - Ensure journald log file rotation is configured
# Source Page: 735
# Confidence: 0.9000000000000001
# Status: review_required

# Audit guidance extracted from the benchmark
# Review the systemd-journald configuration. Verify logs are rotated according to site
# policy. The specific parameters for log rotation are:
# Run the following script and review the output to ensure logs are rotated according to
# site policy:
# Page 735
# #!/usr/bin/env bash
# {
# a_output=() a_output2=() l_analyze_cmd="$(readlink -f /bin/systemd-analyze)"
# l_systemd_config_file="systemd/journald.conf"
# a_parameters=("SystemMaxUse=^.+$" "SystemKeepFree=^.+$" "RuntimeMaxUse=^.+$"
# "RuntimeKeepFree=^.+$" "MaxFileSec=^.+$")
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
# " set to: \"${l_file_parameter_value// /}\"" \
# " in the file: \"$l_file_name\"")
# fi
# done <<< "$l_file_parameter"
# done <<< "$l_used_parameter_setting"
# else
# a_output2+=(" - Parameter: \"$l_parameter_name\" is not set in an included
# file" \
# " *** Note: ***" " \"$l_parameter_name\" May be set in a file that's
# ig

# Remediation candidate
Edit /etc/systemd/journald.conf or a file ending in .conf the
/etc/systemd/journald.conf.d/ directory. Set the following parameters in the
[ ! -d /etc/systemd/journald.conf.d/ ] && mkdir
/etc/systemd/journald.conf.d/
if grep -Psq -- '^\h*\[Journal\]' /etc/systemd/journald.conf.d/60-
printf '%s\n' "" "${a_settings[@]}" >> /etc/systemd/journald.conf.d/60-
/etc/systemd/journald.conf.d/60-journald.conf
# systemctl reload-or-restart systemd-journald

# TODO: replace the commented/manual steps above with validated bash remediation logic.
