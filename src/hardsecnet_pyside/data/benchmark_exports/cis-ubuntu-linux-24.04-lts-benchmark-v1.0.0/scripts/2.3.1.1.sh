#!/usr/bin/env bash
set -euo pipefail

# CIS Benchmark: CIS Ubuntu Linux 24.04 LTS Benchmark
# Control: 2.3.1.1 - Ensure a single time synchronization daemon is in use
# Source Page: 307
# Confidence: 0.96
# Status: review_required

# Audit guidance extracted from the benchmark
# On physical systems, and virtual systems where host based time synchronization is not
# available.
# One of the two time synchronization daemons should be available; chrony or systemd-
# timesyncd
# Run the following script to verify that a single time synchronization daemon is available
# on the system:
# Page 307
# #!/usr/bin/env bash
# {
# l_output="" l_output2=""
# service_not_enabled_chk()
# {
# l_out2=""
# if systemctl is-enabled "$l_service_name" 2>/dev/null | grep -q 'enabled'; then
# l_out2="$l_out2\n - Daemon: \"$l_service_name\" is enabled on the system"
# fi
# if systemctl is-active "$l_service_name" 2>/dev/null | grep -q '^active'; then
# l_out2="$l_out2\n - Daemon: \"$l_service_name\" is active on the system"
# fi
# }
# l_service_name="systemd-timesyncd.service" # Check systemd-timesyncd daemon
# service_not_enabled_chk
# if [ -n "$l_out2" ]; then
# l_timesyncd="y"
# l_out_tsd="$l_out2"
# else
# l_timesyncd="n"
# l_out_tsd="\n - Daemon: \"$l_service_name\" is not enabled and not active on the system"
# fi
# l_service_name="chrony.service" # Check chrony
# service_not_enabled_chk
# if [ -n "$l_out2" ]; then
# l_chrony="y"
# l_out_chrony="$l_out2"
# else
# l_chrony="n"
# l_out_chrony="\n - Daemon: \"$l_service_name\" is not enabled and not active on the
# system"
# fi
# l_status="$l_timesyncd$l_chrony"
# case "$l_status" in
# yy)
# l_output2=" - More than one time sync daemon is in use on the
# system$l_out_tsd$l_out_chrony"
# ;;
# nn)
# l_output2=" - No time sync daemon is in use on the system$l_out_tsd$l_out_chrony"
# ;;
# yn|ny)
# l_output=" - Only one time

# Remediation candidate
# systemctl stop systemd-timesyncd.service
# systemctl mask systemd-timesyncd.service

# TODO: replace the commented/manual steps above with validated bash remediation logic.
