#!/usr/bin/env bash
set -euo pipefail

# CIS Benchmark: CIS Ubuntu Linux 24.04 LTS Benchmark
# Control: 6.1.1.4 - Ensure only one logging system is in use
# Source Page: 739
# Confidence: 0.96
# Status: review_required

# Audit guidance extracted from the benchmark
# Run the following script to ensure only one logging system is in use:
# #!/usr/bin/env bash
# {
# l_output="" l_output2="" # Check the status of rsyslog and journald
# if systemctl is-active --quiet rsyslog; then
# l_output="$l_output\n - rsyslog is in use\n- follow the
# recommendations in Configure rsyslog subsection only"
# elif systemctl is-active --quiet systemd-journald; then
# l_output="$l_output\n - journald is in use\n- follow the
# recommendations in Configure journald subsection only"
# else
# echo -e “unable to determine system logging”
# l_output2="$l_output2\n - unable to determine system logging\n-
# Configure only ONE system logging: rsyslog OR journald"
# fi
# if [ -z "$l_output2" ]; then # Provide audit results
# echo -e "\n- Audit Result:\n ** PASS **\n$l_output\n"
# else
# echo -e "\n- Audit Result:\n ** FAIL **\n - Reason(s) for audit
# failure:\n$l_output2"
# fi
# }

# Remediation candidate
# Manual review required
# Convert the remediation guidance below into a validated script action

# TODO: replace the commented/manual steps above with validated bash remediation logic.
