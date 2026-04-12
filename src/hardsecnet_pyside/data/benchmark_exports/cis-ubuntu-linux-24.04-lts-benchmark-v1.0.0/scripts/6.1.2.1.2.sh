#!/usr/bin/env bash
set -euo pipefail

# CIS Benchmark: CIS Ubuntu Linux 24.04 LTS Benchmark
# Control: 6.1.2.1.2 - Ensure systemd-journal-upload authentication is configured
# Source Page: 745
# Confidence: 0.9000000000000001
# Status: review_required

# Audit guidance extracted from the benchmark
# Run the following script to verify systemd-journal-upload authentication is
# configured:
# Page 745
# #!/usr/bin/env bash
# {
# a_output=() a_output2=() l_analyze_cmd="$(readlink -f /bin/systemd-analyze)"
# l_systemd_config_file="systemd/journal-upload.conf"
# a_parameters=("URL=^.+$" "ServerKeyFile=^.+$" "ServerCertificateFile=^.+$"
# "TrustedCertificateFile=^.+$")
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
# ignored by load procedure")
# fi
# }
# for l_input_parameter in "${a_parameters[@]}"; do
# while IFS="=" read -r l_parameter_name l_parameter_value; do # Assess and che

# Remediation candidate
Edit the /etc/systemd/journal-upload.conf file or a file in
/etc/systemd/journal-upload.conf.d ending in .conf and ensure the following
ServerKeyFile=/etc/ssl/private/journal-upload.pem
ServerCertificateFile=/etc/ssl/certs/journal-upload.pem
TrustedCertificateFile=/etc/ssl/ca/trusted.pem
a_settings=("URL=192.168.50.42" "ServerKeyFile=/etc/ssl/private/journal-
"ServerCertificateFile=/etc/ssl/certs/journal-upload.pem"
"TrustedCertificateFile=/etc/ssl/ca/trusted.pem")
[ ! -d /etc/systemd/journal-upload.conf.d/ ] && mkdir
/etc/systemd/journal-upload.conf.d/
if grep -Psq -- '^\h*\[Upload\]' /etc/systemd/journal-upload.conf.d/60-
printf '%s\n' "" "${a_settings[@]}" >> /etc/systemd/journal-
/etc/systemd/journal-upload.conf.d/60-journald_upload.conf
# systemctl reload-or-restart systemd-journal-upload

# TODO: replace the commented/manual steps above with validated bash remediation logic.
