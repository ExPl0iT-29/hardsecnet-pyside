#!/usr/bin/env bash
set -euo pipefail

# CIS Benchmark: CIS Ubuntu Linux 24.04 LTS Benchmark
# Control: 1.1.2.1.1 - Ensure /tmp is a separate partition
# Source Page: 77
# Confidence: 0.96
# Status: review_required

# Audit guidance extracted from the benchmark
# Run the following command and verify the output shows that /tmp is mounted.
# Particular requirements pertaining to mount options are covered in ensuing sections.
# # findmnt -kn /tmp
# Example output:
# /tmp tmpfs tmpfs rw,nosuid,nodev,noexec
# Ensure that systemd will mount the /tmp partition at boot time.
# # systemctl is-enabled tmp.mount
# Example output:
# generated
# Verify output is not masked or disabled.
# Note: By default, systemd will output generated if there is an entry in /etc/fstab for
# /tmp. This just means systemd will use the entry in /etc/fstab instead of its default
# unit file configuration for /tmp.

# Remediation candidate
# systemctl unmask tmp.mount
/etc/fstab.

# TODO: replace the commented/manual steps above with validated bash remediation logic.
