#!/usr/bin/env bash
set -euo pipefail

# CIS Benchmark: CIS Ubuntu Linux 24.04 LTS Benchmark
# Control: 3.2.2 - Ensure tipc kernel module is not available
# Source Page: 371
# Confidence: 0.96
# Status: review_required

# Audit guidance extracted from the benchmark
# Run the following script to verify:
# - IF - the tipc kernel module is available in ANY installed kernel, verify:
# -
# An entry including /bin/true or /bin/false exists in a file within the
# /etc/modprobe.d/ directory
# -
# The module is deny listed in a file within the /etc/modprobe.d/ directory
# -
# The module is not loaded in the running kernel
# - IF - the tipc kernel module is not available on the system, or pre-compiled into the
# kernel, no additional configuration is necessary
# Page 371
# #!/usr/bin/env bash
# {
# a_output=() a_output2=() a_output3=() l_dl="" l_mod_name="tipc"
# l_mod_type="net"
# l_mod_path="$(readlink -f /lib/modules/**/kernel/$l_mod_type | sort -u)"
# f_module_chk()
# {
# l_dl="y" a_showconfig=()
# while IFS= read -r l_showconfig; do
# a_showconfig+=("$l_showconfig")
# done < <(modprobe --showconfig | grep -P --
# '\b(install|blacklist)\h+'"${l_mod_chk_name//-/_}"'\b')
# if ! lsmod | grep "$l_mod_chk_name" &> /dev/null; then
# a_output+=(" - kernel module: \"$l_mod_name\" is not loaded")
# else
# a_output2+=(" - kernel module: \"$l_mod_name\" is loaded")
# fi
# if grep -Pq -- '\binstall\h+'"${l_mod_chk_name//-
# /_}"'\h+(\/usr)?\/bin\/(true|false)\b' <<< "${a_showconfig[*]}"; then
# a_output+=(" - kernel module: \"$l_mod_name\" is not loadable")
# else
# a_output2+=(" - kernel module: \"$l_mod_name\" is loadable")
# fi
# if grep -Pq -- '\bblacklist\h+'"${l_mod_chk_name//-/_}"'\b' <<<
# "${a_showconfig[*]}"; then
# a_output+=(" - kernel module: \"$l_mod_name\" is deny listed")
# else
# a_output2+=(" - kernel module: \"$l_

# Remediation candidate
# IF - the tipc kernel module is available in ANY installed kernel:
/etc/modprobe.d/ directory
Create a file ending in .conf with blacklist tipc in the /etc/modprobe.d/
Run modprobe -r tipc 2>/dev/null; rmmod tipc 2>/dev/null to remove
# IF - the tipc kernel module is not available on the system, or pre-compiled into the
done < <(modprobe --showconfig | grep -P --
modprobe -r "$l_mod_chk_name" 2>/dev/null; rmmod "$l_mod_name"
/etc/modprobe.d/"$l_mod_name".conf
/etc/modprobe.d/"$l_mod_name".conf

# TODO: replace the commented/manual steps above with validated bash remediation logic.
