#!/usr/bin/env bash
set -euo pipefail

# CIS Benchmark: CIS Ubuntu Linux 24.04 LTS Benchmark
# Control: 5.1.12 - Ensure sshd KexAlgorithms is configured
# Source Page: 556
# Confidence: 0.96
# Status: review_required

# Audit guidance extracted from the benchmark
# Run the following command to verify none of the "weak" Key Exchange algorithms are
# being used:
# # sshd -T | grep -Pi -- 'kexalgorithms\h+([^#\n\r]+,)?(diffie-hellman-group1-
# sha1|diffie-hellman-group14-sha1|diffie-hellman-group-exchange-sha1)\b'
# Nothing should be returned
# The following are considered "weak" Key Exchange Algorithms, and should not be
# used:
# diffie-hellman-group1-sha1
# diffie-hellman-group14-sha1
# diffie-hellman-group-exchange-sha1

# Remediation candidate
Edit the /etc/ssh/sshd_config file and add/modify the KexAlgorithms line to contain

# TODO: replace the commented/manual steps above with validated bash remediation logic.
