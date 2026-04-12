#!/usr/bin/env bash
set -euo pipefail

# CIS Benchmark: CIS Ubuntu Linux 24.04 LTS Benchmark
# Control: 2.3.2.1 - Ensure systemd-timesyncd configured with authorized timeserver
# Source Page: 313
# Confidence: 0.96
# Status: review_required

# Audit guidance extracted from the benchmark
# Run the following command to verify the NTP and/or FallbackNTP option is set to local
# site approved authoritative time server(s):
# Page 313
# #!/usr/bin/env bash
# {
# a_output=(); a_output2=(); a_parlist=("NTP=[^#\n\r]+" "FallbackNTP=[^#\n\r]+")
# l_systemd_config_file="/etc/systemd/timesyncd.conf" # Main systemd configuration file
# f_config_file_parameter_chk()
# {
# unset A_out; declare -A A_out # Check config file(s) setting
# while read -r l_out; do
# if [ -n "$l_out" ]; then
# if [[ $l_out =~ ^\s*# ]]; then
# l_file="${l_out//# /}"
# else
# l_systemd_parameter="$(awk -F= '{print $1}' <<< "$l_out" | xargs)"
# grep -Piq -- "^\h*$l_systemd_parameter_name\b" <<< "$l_systemd_parameter" &&
# A_out+=(["$l_systemd_parameter"]="$l_file")
# fi
# fi
# done < <("$l_systemdanalyze" cat-config "$l_systemd_config_file" | grep -Pio
# '^\h*([^#\n\r]+|#\h*\/[^#\n\r\h]+\.conf\b)')
# if (( ${#A_out[@]} > 0 )); then # Assess output from files and generate output
# while IFS="=" read -r l_systemd_file_parameter_name l_systemd_file_parameter_value; do
# l_systemd_file_parameter_name="${l_systemd_file_parameter_name// /}"
# l_systemd_file_parameter_value="${l_systemd_file_parameter_value// /}"
# if grep -Piq "\b$l_systemd_parameter_value\b" <<< "$l_systemd_file_parameter_value";
# then
# a_output+=(" - \"$l_systemd_parameter_name\" is correctly set to
# \"$l_systemd_file_parameter_value\"" \
# " in \"$(printf '%s' "${A_out[@]}")\"")
# else
# a_output2+=(" - \"$l_systemd_parameter_name\" is incorrectly set to
# \"$l_systemd_file_parameter_value\"" \
# " in 

# Remediation candidate
server(s) in /etc/systemd/timesyncd.conf or a file in
/etc/systemd/timesyncd.conf.d/ ending in .conf in the [Time] section:
[ ! -d /etc/systemd/timesyncd.conf.d/ ] && mkdir
/etc/systemd/timesyncd.conf.d/
if grep -Psq -- '^\h*\[Time\]' /etc/systemd/timesyncd.conf.d/60-
/etc/systemd/timesyncd.conf.d/60-timesyncd.conf
/etc/systemd/timesyncd.conf.d/60-timesyncd.conf
# systemctl reload-or-restart systemd-journald

# TODO: replace the commented/manual steps above with validated bash remediation logic.
