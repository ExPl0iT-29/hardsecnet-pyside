#!/usr/bin/env bash
set -euo pipefail

# CIS Benchmark: CIS Ubuntu Linux 24.04 LTS Benchmark
# Control: 1.5.2 - Ensure ptrace_scope is restricted
# Source Page: 171
# Confidence: 0.96
# Status: review_required

# Audit guidance extracted from the benchmark
# Run the following script to verify the following kernel parameter is set in the running
# configuration and correctly loaded from a kernel parameter configuration file:
# -
# kernel.yama.ptrace_scope is set to a value of: 1, 2, or 3
# Note: kernel parameters are loaded by file and parameter order precedence. The
# following script observes this precedence as part of the auditing procedure. The
# parameters being checked may be set correctly in a file. If that file is superseded, the
# parameter is overridden by an incorrect setting later in that file, or in a canonically later
# file, that "correct" setting will be ignored both by the script and by the system during a
# normal kernel parameter load sequence.
# Page 172
# #!/usr/bin/env bash
# {
# a_output=(); a_output2=(); a_parlist=("kernel.yama.ptrace_scope=(1|2|3)")
# l_ufwscf="$([ -f /etc/default/ufw ] && awk -F= '/^\s*IPT_SYSCTL=/ {print
# $2}' /etc/default/ufw)"
# f_kernel_parameter_chk()
# {
# l_running_parameter_value="$(sysctl "$l_parameter_name" | awk -F=
# '{print $2}' | xargs)" # Check running configuration
# if grep -Pq -- '\b'"$l_parameter_value"'\b' <<<
# "$l_running_parameter_value"; then
# a_output+=(" - \"$l_parameter_name\" is correctly set to
# \"$l_running_parameter_value\""
# " in the running configuration")
# else
# a_output2+=(" - \"$l_parameter_name\" is incorrectly set to
# \"$l_running_parameter_value\"" \
# " in the running configuration" \
# " and should have a value of: \"$l_value_out\"")
# fi
# unset A_out; declare -A A_out # Check durable setting (files)

# Remediation candidate
Set the kernel.yama.ptrace_scope parameter in /etc/sysctl.conf or a file in
/etc/sysctl.d/ ending in .conf to a value of 1, 2, or 3:
# OR -
# OR -
# printf "%s\n" "kernel.yama.ptrace_scope = 1" >> /etc/sysctl.d/60-

# TODO: replace the commented/manual steps above with validated bash remediation logic.
