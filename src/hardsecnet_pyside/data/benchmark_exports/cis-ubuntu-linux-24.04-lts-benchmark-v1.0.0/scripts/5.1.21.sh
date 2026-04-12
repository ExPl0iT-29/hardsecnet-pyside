#!/usr/bin/env bash
set -euo pipefail

# CIS Benchmark: CIS Ubuntu Linux 24.04 LTS Benchmark
# Control: 5.1.21 - Ensure sshd PermitUserEnvironment is disabled
# Source Page: 576
# Confidence: 0.96
# Status: review_required

# Audit guidance extracted from the benchmark
# Run the following command to verify PermitUserEnviroment is set to no:
# # sshd -T | grep permituserenvironment
# permituserenvironment no

# Remediation candidate
Edit the /etc/ssh/sshd_config file to set the PermitUserEnvironment parameter to

# TODO: replace the commented/manual steps above with validated bash remediation logic.
