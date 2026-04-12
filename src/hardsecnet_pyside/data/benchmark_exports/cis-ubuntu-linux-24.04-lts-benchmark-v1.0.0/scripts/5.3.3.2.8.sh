#!/usr/bin/env bash
set -euo pipefail

# CIS Benchmark: CIS Ubuntu Linux 24.04 LTS Benchmark
# Control: 5.3.3.2.8 - Ensure password quality is enforced for the root user
# Source Page: 651
# Confidence: 0.96
# Status: review_required

# Audit guidance extracted from the benchmark
# Run the following command to verify that the enforce_for_root option is enabled in a
# pwquality configuration file:
# # grep -Psi -- '^\h*enforce_for_root\b' /etc/security/pwquality.conf
# /etc/security/pwquality.conf.d/*.conf
# Example output:
# /etc/security/pwquality.conf.d/50-pwroot.conf:enforce_for_root
# Note:
# -
# Settings observe an order of precedence:
# o module arguments override the settings in the
# /etc/security/pwquality.conf configuration file
# o settings in the /etc/security/pwquality.conf configuration file
# override settings in a .conf file in the
# /etc/security/pwquality.conf.d/ directory
# o settings in a .conf file in the /etc/security/pwquality.conf.d/
# directory are read in canonical order, with last read file containing the
# setting taking precedence
# -
# It is recommended that settings be configured in a .conf file in the
# /etc/security/pwquality.conf.d/ directory for clarity, convenience, and
# durability.

# Remediation candidate
Edit or add the following line in a *.conf file in /etc/security/pwquality.conf.d or
in /etc/security/pwquality.conf:
[ ! -d /etc/security/pwquality.conf.d/ ] && mkdir
/etc/security/pwquality.conf.d/
printf '\n%s\n' "enforce_for_root" > /etc/security/pwquality.conf.d/50-

# TODO: replace the commented/manual steps above with validated bash remediation logic.
