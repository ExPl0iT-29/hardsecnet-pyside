#!/usr/bin/env bash
set -euo pipefail

# CIS Benchmark: CIS Ubuntu Linux 24.04 LTS Benchmark
# Control: 1.5.3 - Ensure core dumps are restricted
# Source Page: 176
# Confidence: 0.96
# Status: review_required

# Audit guidance extracted from the benchmark
# Run the following command and verify output matches:
# # grep -Ps -- '^\h*\*\h+hard\h+core\h+0\b' /etc/security/limits.conf
# /etc/security/limits.d/*
# * hard core 0
# Run the following script to verify fs.suid_dumpable = 0:
# Run the following script to verify the following kernel parameter is set in the running
# configuration and correctly loaded from a kernel parameter configuration file:
# -
# fs.suid_dumpable is set to 0
# Note: kernel parameters are loaded by file and parameter order precedence. The
# following script observes this precedence as part of the auditing procedure. The
# parameters being checked may be set correctly in a file. If that file is superseded, the
# parameter is overridden by an incorrect setting later in that file, or in a canonically later
# file, that "correct" setting will be ignored both by the script and by the system during a
# normal kernel parameter load sequence.
# Page 176
# #!/usr/bin/env bash
# {
# a_output=(); a_output2=(); a_parlist=("fs.suid_dumpable=0")
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
# \"$l_ru

# Remediation candidate
Add the following line to /etc/security/limits.conf or a
/etc/security/limits.d/* file:
Set the following parameter in /etc/sysctl.conf or a file in /etc/sysctl.d/ ending
# printf "\n%s" "fs.suid_dumpable = 0" >> /etc/sysctl.d/60-fs_sysctl.conf
# IF- systemd-coredump is installed:
edit /etc/systemd/coredump.conf and add/modify the following lines:
systemctl daemon-reload

# TODO: replace the commented/manual steps above with validated bash remediation logic.
