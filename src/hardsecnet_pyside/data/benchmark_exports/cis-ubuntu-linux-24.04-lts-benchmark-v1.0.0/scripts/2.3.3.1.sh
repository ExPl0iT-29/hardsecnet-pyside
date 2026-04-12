#!/usr/bin/env bash
set -euo pipefail

# CIS Benchmark: CIS Ubuntu Linux 24.04 LTS Benchmark
# Control: 2.3.3.1 - Ensure chrony is configured with authorized timeserver
# Source Page: 320
# Confidence: 0.96
# Status: review_required

# Audit guidance extracted from the benchmark
# - IF - chrony is in use on the system, run the following script to ensure chrony is
# configured with an authorized timeserver:
# #!/usr/bin/env bash
# {
# a_output=() a_output2=() a_config_files=("/etc/chrony/chrony.conf")
# l_include='(confdir|sourcedir)' l_parameter_name='(server|pool)'
# l_parameter_value='.+'
# while IFS= read -r l_conf_loc; do
# l_dir="" l_ext=""
# if [ -d "$l_conf_loc" ]; then
# l_dir="$l_conf_loc" l_ext="*"
# elif grep -Psq '\/\*\.([^#/\n\r]+)?\h*$' <<< "$l_conf_loc" || [ -f
# "$(readlink -f "$l_conf_loc")" ]; then
# l_dir="$(dirname "$l_conf_loc")" l_ext="$(basename "$l_conf_loc")"
# fi
# if [[ -n "$l_dir" && -n "$l_ext" ]]; then
# while IFS= read -r -d $'\0' l_file_name; do
# [ -f "$(readlink -f "$l_file_name")" ] &&
# a_config_files+=("$(readlink -f "$l_file_name")")
# done < <(find -L "$l_dir" -type f -name "$l_ext" -print0
# 2>/dev/null)
# fi
# done < <(awk '$1~/^\s*'"$l_include"'$/{print $2}' "${a_config_files[*]}"
# 2>/dev/null)
# for l_file in "${a_config_files[@]}"; do
# l_parameter_line="$(grep -Psi
# '^\h*'"$l_parameter_name"'(\h+|\h*:\h*)'"$l_parameter_value"'\b' "$l_file")"
# [ -n "$l_parameter_line" ] && a_output+=(" - Parameter: \"$(tr -d '()'
# <<< ${l_parameter_name//|/ or })\"" \
# " Exists in the file: \"$l_file\" as:" "$l_parameter_line")
# done
# [ "${#a_output[@]}" -le "0" ] && a_output2+=(" - Parameter: \"$(tr -d
# '()' <<< ${l_parameter_name//|/ or })\"" \
# " Does not exist in the chrony configuration")
# if [ "${#a_output2[@]}" -le 0 ]; then
# printf '%s\n' "" "- Audit Result:" " ** PASS **" "$

# Remediation candidate
Edit /etc/chrony/chrony.conf or a file ending in .sources in
/etc/chrony/sources.d/ and add or edit server or pool lines as appropriate
[ ! -d "/etc/chrony/sources.d/" ] && mkdir /etc/chrony/sources.d/
"pool time.nist.gov iburst maxsources 4" >> /etc/chrony/sources.d/60-
[ ! -d "/etc/chrony/sources.d/" ] && mkdir /etc/chrony/sources.d/
"server time-d-b.nist.gov iburst" >> /etc/chrony/sources.d/60-
# systemctl reload-or-restart chronyd

# TODO: replace the commented/manual steps above with validated bash remediation logic.
