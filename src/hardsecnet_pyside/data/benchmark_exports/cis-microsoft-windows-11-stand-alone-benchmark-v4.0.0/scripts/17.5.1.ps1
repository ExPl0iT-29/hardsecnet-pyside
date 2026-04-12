# CIS Benchmark: CIS Microsoft Windows 11 Stand-alone Benchmark
# Control: 17.5.1 - Ensure 'Audit Account Lockout' is set to include 'Failure'
# Source Page: 420
# Confidence: 0.96
# Status: review_required

$ErrorActionPreference = 'Stop'

# Audit guidance extracted from the benchmark
# Navigate to the UI Path articulated in the Remediation section and confirm it is set as
# prescribed.
# OR
# To audit the system using auditpol.exe, perform the following and confirm it is set as
# prescribed:
# auditpol /get /subcategory:"{0cce9217-69ae-11d9-bed3-505054503030}"
# Page 420

# Remediation candidate
# Manual review required
# Convert the remediation guidance below into a validated script action

# TODO: replace the commented/manual steps above with validated PowerShell or registry logic.
