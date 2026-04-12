#!/usr/bin/env bash
set -euo pipefail

# CIS Benchmark: CIS Ubuntu Linux 24.04 LTS Benchmark
# Control: 1.3.1.2 - Ensure AppArmor is enabled in the bootloader configuration
# Source Page: 154
# Confidence: 0.96
# Status: review_required

# Audit guidance extracted from the benchmark
# Run the following command to verify that all linux lines have the apparmor=1
# parameter set:
# # grep "^\s*linux" /boot/grub/grub.cfg | grep -v "apparmor=1"
# Nothing should be returned.
# Run the following command to verify that all linux lines have the security=apparmor
# parameter set:
# # grep "^\s*linux" /boot/grub/grub.cfg | grep -v "security=apparmor"
# Nothing should be returned.

# Remediation candidate
Edit /etc/default/grub and add the apparmor=1 and security=apparmor

# TODO: replace the commented/manual steps above with validated bash remediation logic.
