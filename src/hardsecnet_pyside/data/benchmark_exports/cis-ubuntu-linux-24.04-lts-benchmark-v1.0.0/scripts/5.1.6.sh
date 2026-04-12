#!/usr/bin/env bash
set -euo pipefail

# CIS Benchmark: CIS Ubuntu Linux 24.04 LTS Benchmark
# Control: 5.1.6 - Ensure sshd Ciphers are configured
# Source Page: 541
# Confidence: 0.96
# Status: review_required

# Audit guidance extracted from the benchmark
# Run the following command to verify none of the "weak" ciphers are being used:
# # sshd -T | grep -Pi --
# '^ciphers\h+\"?([^#\n\r]+,)?((3des|blowfish|cast128|aes(128|192|256))-
# cbc|arcfour(128|256)?|rijndael-cbc@lysator\.liu\.se|chacha20-
# poly1305@openssh\.com)\b'
# - IF - a line is returned, review the list of ciphers. If the line includes chacha20-
# poly1305@openssh.com, review CVE-2023-48795 and verify the system has been
# patched. No ciphers in the list below should be returned as they're considered "weak":
# 3des-cbc
# aes128-cbc
# aes192-cbc
# aes256-cbc

# Remediation candidate
Edit the /etc/ssh/sshd_config file and add/modify the Ciphers line to contain a comma
# IF - CVE-2023-48795 has been addressed, and it meets local site policy, chacha20-

# TODO: replace the commented/manual steps above with validated bash remediation logic.
