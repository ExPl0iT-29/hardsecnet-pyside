#!/usr/bin/env bash
set -euo pipefail

# CIS Benchmark: CIS Ubuntu Linux 24.04 LTS Benchmark
# Control: 6.3.3 - Ensure cryptographic mechanisms are used to protect the integrity of audit tools
# Source Page: 929
# Confidence: 0.96
# Status: review_required

# Audit guidance extracted from the benchmark
# Verify that Advanced Intrusion Detection Environment (AIDE) is properly configured.
# Run the following script to verify:
# -
# AIDE is configured to use cryptographic mechanisms to protect the integrity of
# audit tools:
# -
# The following audit tool files include the options "p, i, n, u, g, s, b, acl, xattrs and
# sha512"
# o auditctl
# o auditd
# o ausearch
# o aureport
# o autrace
# o augenrules
# Page 930
# #!/usr/bin/env bash
# {
# a_output=() a_output2=() l_tool_dir="$(readlink -f /sbin)"
# a_items=("p" "i" "n" "u" "g" "s" "b" "acl" "xattrs" "sha512")
# l_aide_cmd="$(whereis aide | awk '{print $2}')"
# a_audit_files=("auditctl" "auditd" "ausearch" "aureport" "autrace"
# "augenrules")
# if [ -f "$l_aide_cmd" ] && command -v "$l_aide_cmd" &>/dev/null; then
# a_aide_conf_files=("$(find -L /etc -type f -name 'aide.conf')")
# f_file_par_chk()
# {
# a_out2=()
# for l_item in "${a_items[@]}"; do
# ! grep -Psiq -- '(\h+|\+)'"$l_item"'(\h+|\+)' <<< "$l_out" && \
# a_out2+=(" - Missing the \"$l_item\" option")
# done
# if [ "${#a_out2[@]}" -gt "0" ]; then
# a_output2+=(" - Audit tool file: \"$l_file\"" "${a_out2[@]}")
# else
# a_output+=(" - Audit tool file: \"$l_file\" includes:" "
# \"${a_items[*]}\"")
# fi
# }
# for l_file in "${a_audit_files[@]}"; do
# if [ -f "$l_tool_dir/$l_file" ]; then
# l_out="$("$l_aide_cmd" --config "${a_aide_conf_files[@]}" -p
# f:"$l_tool_dir/$l_file")"
# f_file_par_chk
# else
# a_output+=(" - Audit tool file \"$l_file\" doesn't exist")
# fi
# done
# else
# a_output2+=(" - The command \"aide\" was not found" " Please
# install AIDE")
# fi
# if [ "$

# Remediation candidate
Edit /etc/aide/aide.conf and add or update the following selection lines replacing
<PATH>/auditctl p+i+n+u+g+s+b+acl+xattrs+sha512
# printf '%s\n' "" "# Audit Tools" "$(readlink -f /sbin/auditctl)
p+i+n+u+g+s+b+acl+xattrs+sha512" >> /etc/aide/aide.conf
Note: - IF - /etc/aide/aide.conf includes a @@x_include statement:
@@x_include /etc/aide.conf.d ^[a-zA-Z0-9_-]+$

# TODO: replace the commented/manual steps above with validated bash remediation logic.
