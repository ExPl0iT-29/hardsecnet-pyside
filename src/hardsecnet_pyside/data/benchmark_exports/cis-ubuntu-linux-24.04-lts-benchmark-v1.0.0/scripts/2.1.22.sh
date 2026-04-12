#!/usr/bin/env bash
set -euo pipefail

# CIS Benchmark: CIS Ubuntu Linux 24.04 LTS Benchmark
# Control: 2.1.22 - Ensure only approved services are listening on a network interface
# Source Page: 289
# Confidence: 0.9000000000000001
# Status: review_required

# Audit guidance extracted from the benchmark
# Run the following command:
# # ss -plntu
# Review the output to ensure:
# -
# All services listed are required on the system and approved by local site policy.
# -
# Both the port and interface the service is listening on are approved by local site
# policy.
# -
# If a listed service is not required:
# o Remove the package containing the service
# o - IF - the service's package is required for a dependency, stop and mask
# the service and/or socket

# Remediation candidate
# systemctl stop <service_name>.socket <service_name>.service
# OR - If required packages have a dependency:
# systemctl stop <service_name>.socket <service_name>.service
# systemctl mask <service_name>.socket <service_name>.service

# TODO: replace the commented/manual steps above with validated bash remediation logic.
