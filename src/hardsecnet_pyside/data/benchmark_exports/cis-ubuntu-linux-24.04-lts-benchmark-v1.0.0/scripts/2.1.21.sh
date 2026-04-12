#!/usr/bin/env bash
set -euo pipefail

# CIS Benchmark: CIS Ubuntu Linux 24.04 LTS Benchmark
# Control: 2.1.21 - Ensure mail transfer agent is configured for local-only mode
# Source Page: 286
# Confidence: 0.96
# Status: review_required

# Audit guidance extracted from the benchmark
# Run the following script to verify that the MTA is not listening on any non-loopback
# address ( 127.0.0.1 or ::1
# #!/usr/bin/env bash
# {
# a_output=(); a_output2=(); a_port_list=("25" "465" "587")
# for l_port_number in "${a_port_list[@]}"; do
# if ss -plntu | grep -P -- ':'"$l_port_number"'\b' | grep -Pvq --
# '\h+(127\.0\.0\.1|\[?::1\]?):'"$l_port_number"'\b'; then
# a_output2+=(" - Port \"$l_port_number\" is listening on a non-
# loopback network interface")
# else
# a_output+=(" - Port \"$l_port_number\" is not listening on a non-
# loopback network interface")
# fi
# done
# if command -v postconf &> /dev/null; then
# l_interfaces="$(postconf -n inet_interfaces)"
# elif command -v exim &> /dev/null; then
# l_interfaces="$(exim -bP local_interfaces)"
# elif command -v sendmail &> /dev/null; then
# l_interfaces="$(grep -i "0 DaemonPortOptions=" /etc/mail/sendmail.cr |
# grep -oP '?<=Addr=)[^,+]+')"
# fi
# if [ -n "$l_interfaces" ]; then
# if grep -Pqi '\ball\b' <<< "$l_interfaces"; then
# a_output2+=(" - MTA is bound to all network interfaces")
# elif ! grep -Pqi '(inet_interfaces\h*=\h*)?(0\.0\.0\.0|::1|loopback-
# only)' <<< "$l_interfaces"; then
# a_output2+=(" - MTA is bound to a network interface" "
# \"$l_interfaces\"")
# else
# a_output+=(" - MTA is not bound to a non loopback network interface"
# " \"$l_interfaces\"")
# fi
# else
# a_output+=(" - MTA not detected or in use")
# fi
# if [ "${#a_output2[@]}" -le 0 ]; then
# printf '%s\n' "" "- Audit Result:" " ** PASS **" "${a_output[@]}"
# else
# printf '%s\n' "" "- Audit Result:" " ** FAIL **

# Remediation candidate
Edit /etc/postfix/main.cf and add the following line to the RECEIVING MAIL
# systemctl restart postfix

# TODO: replace the commented/manual steps above with validated bash remediation logic.
