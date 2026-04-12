#!/usr/bin/env bash
set -euo pipefail

# CIS Benchmark: CIS Ubuntu Linux 24.04 LTS Benchmark
# Control: 6.2.4.3 - Ensure audit log files group owner is configured
# Source Page: 906
# Confidence: 0.96
# Status: review_required

# Audit guidance extracted from the benchmark
# Run the following command to verify log_group parameter is set to either adm or root
# in /etc/audit/auditd.conf:
# # grep -Piws -- '^\h*log_group\h*=\h*\H+\b' /etc/audit/auditd.conf | grep -
# Pvi -- '(adm)'
# Nothing should be returned
# Using the path of the directory containing the audit logs, verify audit log files are owned
# by the "root" or "adm" group by running the following script:
# #!/usr/bin/env bash
# {
# if [ -e /etc/audit/auditd.conf ]; then
# l_fpath="$(dirname "$(awk -F "=" '/^\s*log_file/ {print $2}'
# /etc/audit/auditd.conf | xargs)")"
# find -L "$l_fpath" -not -path "$l_fpath"/lost+found -type f \( ! -group
# root -a ! -group adm \) -exec ls -l {} +
# fi
# }
# Nothing should be returned
# Page 906

# Remediation candidate
/etc/audit/auditd.conf | xargs)) -type f \( ! -group adm -a ! -group root \)
# exec chgrp adm {} +
/etc/audit/auditd.conf
# systemctl restart auditd

# TODO: replace the commented/manual steps above with validated bash remediation logic.
