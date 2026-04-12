#!/usr/bin/env bash
set -euo pipefail

# CIS Benchmark: CIS Ubuntu Linux 24.04 LTS Benchmark
# Control: 3.3.9 - Ensure suspicious packets are logged
# Source Page: 427
# Confidence: 0.96
# Status: review_required

# Audit guidance extracted from the benchmark
# Run the following script to verify the following kernel parameters are set in the running
# configuration and correctly loaded from a kernel parameter configuration file:
# -
# net.ipv4.conf.all.log_martians is set to 1
# -
# net.ipv4.conf.default.log_martians is set to 1
# Note: kernel parameters are loaded by file and parameter order precedence. The
# following script observes this precedence as part of the auditing procedure. The
# parameters being checked may be set correctly in a file. If that file is superseded, the
# parameter is overridden by an incorrect setting later in that file, or in a canonically later
# file, that "correct" setting will be ignored both by the script and by the system during a
# normal kernel parameter load sequence.
# Page 427
# #!/usr/bin/env bash
# {
# a_output=(); a_output2=(); l_ipv6_disabled=""
# a_parlist=("net.ipv4.conf.all.log_martians=1"
# "net.ipv4.conf.default.log_martians=1")
# l_ufwscf="$([ -f /etc/default/ufw ] && awk -F= '/^\s*IPT_SYSCTL=/ {print
# $2}' /etc/default/ufw)"
# f_ipv6_chk()
# {
# l_ipv6_disabled="no"
# ! grep -Pqs -- '^\h*0\b' /sys/module/ipv6/parameters/disable &&
# l_ipv6_disabled="yes"
# if sysctl net.ipv6.conf.all.disable_ipv6 | grep -Pqs --
# "^\h*net\.ipv6\.conf\.all\.disable_ipv6\h*=\h*1\b" && \
# sysctl net.ipv6.conf.default.disable_ipv6 | grep -Pqs --
# "^\h*net\.ipv6\.conf\.default\.disable_ipv6\h*=\h*1\b"; then
# l_ipv6_disabled="yes"
# fi
# }
# f_kernel_parameter_chk()
# {
# l_running_parameter_value="$(sysctl "$l_parameter_name" | awk -F=
# '{print $2}' | xargs)" # Check r

# Remediation candidate
Set the following parameters in /etc/sysctl.conf or a file in /etc/sysctl.d/ ending
"net.ipv4.conf.default.log_martians = 1" >> /etc/sysctl.d/60-

# TODO: replace the commented/manual steps above with validated bash remediation logic.
