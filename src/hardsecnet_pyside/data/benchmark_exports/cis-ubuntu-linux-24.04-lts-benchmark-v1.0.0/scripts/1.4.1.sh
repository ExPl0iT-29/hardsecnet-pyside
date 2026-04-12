#!/usr/bin/env bash
set -euo pipefail

# CIS Benchmark: CIS Ubuntu Linux 24.04 LTS Benchmark
# Control: 1.4.1 - Ensure bootloader password is set
# Source Page: 161
# Confidence: 0.96
# Status: review_required

# Audit guidance extracted from the benchmark
# Run the following commands and verify output matches:
# # grep "^set superusers" /boot/grub/grub.cfg
# set superusers="<username>"
# # awk -F. '/^\s*password/ {print $1"."$2"."$3}' /boot/grub/grub.cfg
# password_pbkdf2 <username> grub.pbkdf2.sha512
# Page 161

# Remediation candidate
Add the following into a custom /etc/grub.d configuration file:
/etc/grub.d/00_header file as this file could be overwritten in a package update.
/etc/grub.d/10_linux and add --unrestricted to the line CLASS=

# TODO: replace the commented/manual steps above with validated bash remediation logic.
