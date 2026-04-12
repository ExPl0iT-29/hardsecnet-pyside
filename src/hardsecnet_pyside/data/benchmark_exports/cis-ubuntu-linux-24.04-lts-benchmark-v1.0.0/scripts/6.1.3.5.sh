#!/usr/bin/env bash
set -euo pipefail

# CIS Benchmark: CIS Ubuntu Linux 24.04 LTS Benchmark
# Control: 6.1.3.5 - Ensure rsyslog logging is configured
# Source Page: 778
# Confidence: 0.9000000000000001
# Status: review_required

# Audit guidance extracted from the benchmark
# Review the contents of /etc/rsyslog.conf and /etc/rsyslog.d/*.conf files to
# ensure appropriate logging is set. In addition, run the following command and verify that
# the log files are logging information as expected:
# Run the following script and review the output from the rsyslog configuration to ensure
# appropriate logging is set an in accordance with local site policy.
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
# grep -PHs -- '^\h*[^#\n\r\/:]+\/var\/log\/.*$' "$l_logfile"
# done
# }
# Example output:
# Page 778
# /etc/rsyslog.d/60-rsyslog.conf:auth,authpriv.* /var/log/secure
# /etc/rsyslog.d/60-rsyslog.conf:mail.* -/var/log/mail
# /etc/rsyslog.d/60-rsyslog.conf:mai

# Remediation candidate
# systemctl reload-or-restart rsyslog

# TODO: replace the commented/manual steps above with validated bash remediation logic.
