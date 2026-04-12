#!/usr/bin/env bash
set -euo pipefail

# CIS Benchmark: CIS Ubuntu Linux 24.04 LTS Benchmark
# Control: 5.1.15 - Ensure sshd MACs are configured
# Source Page: 563
# Confidence: 0.96
# Status: review_required

# Audit guidance extracted from the benchmark
# Run the following command to verify none of the "weak" MACs are being used:
# # sshd -T | grep -Pi -- 'macs\h+([^#\n\r]+,)?(hmac-md5|hmac-md5-96|hmac-
# ripemd160|hmac-sha1-96|umac-64@openssh\.com|hmac-md5-etm@openssh\.com|hmac-
# md5-96-etm@openssh\.com|hmac-ripemd160-etm@openssh\.com|hmac-sha1-96-
# etm@openssh\.com|umac-64-etm@openssh\.com|umac-128-etm@openssh\.com)\b'
# Nothing should be returned
# Note: Review CVE-2023-48795 and verify the system has been patched. If the system
# has not been patched, review the use of the Encrypt Then Mac (etm) MACs.
# The following are considered "weak" MACs, and should not be used:
# hmac-md5
# hmac-md5-96
# hmac-ripemd160
# hmac-sha1-96
# umac-64@openssh.com
# hmac-md5-etm@openssh.com
# hmac-md5-96-etm@openssh.com
# hmac-ripemd160-etm@openssh.com
# hmac-sha1-96-etm@openssh.com
# umac-64-etm@openssh.com
# umac-128-etm@openssh.com

# Remediation candidate
Edit the /etc/ssh/sshd_config file and add/modify the MACs line to contain a comma
# IF - CVE-2023-48795 has not been reviewed and addressed, the following etm MACs

# TODO: replace the commented/manual steps above with validated bash remediation logic.
