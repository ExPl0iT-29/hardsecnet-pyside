#!/usr/bin/env bash
set -euo pipefail

# CIS Benchmark: CIS Ubuntu Linux 24.04 LTS Benchmark
# Control: 3.3.5 - Ensure icmp redirects are not accepted
# Source Page: 407
# Confidence: 0.96
# Status: review_required

# Audit guidance extracted from the benchmark
# Run the following script to verify the following kernel parameters are set in the running
# configuration and correctly loaded from a kernel parameter configuration file:
# -
# net.ipv4.conf.all.accept_redirects is set to 0
# -
# net.ipv4.conf.default.accept_redirects is set to 0
# -
# net.ipv6.conf.all.accept_redirects is set to 0
# -
# net.ipv6.conf.default.accept_redirects is set to 0
# Note:
# -
# kernel parameters are loaded by file and parameter order precedence. The
# following script observes this precedence as part of the auditing procedure. The
# parameters being checked may be set correctly in a file. If that file is superseded,
# the parameter is overridden by an incorrect setting later in that file, or in a
# canonically later file, that "correct" setting will be ignored both by the script and
# by the system during a normal kernel parameter load sequence.
# -
# IPv6 kernel parameters only apply to systems where IPv6 is enabled
# Page 407
# #!/usr/bin/env bash
# {
# a_output=(); a_output2=(); l_ipv6_disabled=""
# a_parlist=("net.ipv4.conf.all.accept_redirects=0"
# "net.ipv4.conf.default.accept_redirects=0"
# "net.ipv6.conf.all.accept_redirects=0"
# "net.ipv6.conf.default.accept_redirects=0")
# l_ufwscf="$([ -f /etc/default/ufw ] && awk -F= '/^\s*IPT_SYSCTL=/ {print
# $2}' /etc/default/ufw)"
# f_ipv6_chk()
# {
# l_ipv6_disabled="no"
# ! grep -Pqs -- '^\h*0\b' /sys/module/ipv6/parameters/disable &&
# l_ipv6_disabled="yes"
# if sysctl net.ipv6.conf.all.disable_ipv6 | grep -Pqs --
# "^\h*net\.ipv6\.conf\.all\.disable_ipv6\h*=\h*1\b" && \

# Remediation candidate
Set the following parameters in /etc/sysctl.conf or a file in /etc/sysctl.d/ ending
"net.ipv4.conf.default.accept_redirects = 0" >> /etc/sysctl.d/60-
# IF - IPv6 is enabled on the system:
Set the following parameters in /etc/sysctl.conf or a file in /etc/sysctl.d/ ending
"net.ipv6.conf.default.accept_redirects = 0" >> /etc/sysctl.d/60-

# TODO: replace the commented/manual steps above with validated bash remediation logic.
