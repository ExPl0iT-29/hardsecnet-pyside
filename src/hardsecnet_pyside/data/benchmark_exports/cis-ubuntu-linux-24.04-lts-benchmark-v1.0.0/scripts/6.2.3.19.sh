#!/usr/bin/env bash
set -euo pipefail

# CIS Benchmark: CIS Ubuntu Linux 24.04 LTS Benchmark
# Control: 6.2.3.19 - Ensure kernel module loading unloading and modification is collected
# Source Page: 890
# Confidence: 0.96
# Status: review_required

# Audit guidance extracted from the benchmark
# On disk configuration
# Run the following script to check the on disk rules:
# #!/usr/bin/env bash
# {
# awk '/^ *-a *always,exit/ \
# &&/ -F *arch=b(32|64)/ \
# &&(/ -F auid!=unset/||/ -F auid!=-1/||/ -F auid!=4294967295/) \
# &&/ -S/ \
# &&(/init_module/ \
# ||/finit_module/ \
# ||/delete_module/ \
# ||/create_module/ \
# ||/query_module/) \
# &&(/ key= *[!-~]* *$/||/ -k *[!-~]* *$/)' /etc/audit/rules.d/*.rules
# UID_MIN=$(awk '/^\s*UID_MIN/{print $2}' /etc/login.defs)
# [ -n "${UID_MIN}" ] && awk "/^ *-a *always,exit/ \
# &&(/ -F *auid!=unset/||/ -F *auid!=-1/||/ -F *auid!=4294967295/) \
# &&/ -F *auid>=${UID_MIN}/ \
# &&/ -F *perm=x/ \
# &&/ -F *path=\/usr\/bin\/kmod/ \
# &&(/ key= *[!-~]* *$/||/ -k *[!-~]* *$/)" /etc/audit/rules.d/*.rules \
# || printf "ERROR: Variable 'UID_MIN' is unset.\n"
# }
# Verify the output matches:
# -a always,exit -F arch=b64 -S
# init_module,finit_module,delete_module,create_module,query_module -F
# auid>=1000 -F auid!=unset -k kernel_modules
# -a always,exit -F path=/usr/bin/kmod -F perm=x -F auid>=1000 -F auid!=unset -
# k kernel_modules
# Running configuration
# Run the following script to check loaded rules:
# Page 891
# #!/usr/bin/env bash
# {
# auditctl -l | awk '/^ *-a *always,exit/ \
# &&/ -F *arch=b(32|64)/ \
# &&(/ -F auid!=unset/||/ -F auid!=-1/||/ -F auid!=4294967295/) \
# &&/ -S/ \
# &&(/init_module/ \
# ||/finit_module/ \
# ||/delete_module/ \
# ||/create_module/ \
# ||/query_module/) \
# &&(/ key= *[!-~]* *$/||/ -k *[!-~]* *$/)'
# UID_MIN=$(awk '/^\s*UID_MIN/{print $2}' /etc/login.defs)
# [ -n "${UID_MIN}" ] && audit

# Remediation candidate
Edit or create a file in the /etc/audit/rules.d/ directory, ending in .rules extension,
UID_MIN=$(awk '/^\s*UID_MIN/{print $2}' /etc/login.defs)
# a always,exit -F arch=b64 -S
# a always,exit -F path=/usr/bin/kmod -F perm=x -F auid>=${UID_MIN} -F
" >> /etc/audit/rules.d/50-kernel_modules.rules || printf "ERROR: Variable
# if [[ $(auditctl -s | grep "enabled") =~ "2" ]]; then printf "Reboot

# TODO: replace the commented/manual steps above with validated bash remediation logic.
