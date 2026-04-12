# CIS Benchmark: CIS Microsoft Windows 11 Stand-alone Benchmark
# Control: 18.5.1 - Ensure 'MSS: (AutoAdminLogon) Enable Automatic Logon' is set to 'Disabled'
# Source Page: 501
# Confidence: 0.96
# Status: review_required

$ErrorActionPreference = 'Stop'

# Audit guidance extracted from the benchmark
# Navigate to the UI Path articulated in the Remediation section and confirm it is set as
# prescribed. This group policy setting is backed by the following registry location with a
# REG_SZ value of 0.
# HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon:AutoAdminLogon
# Page 501

# Remediation candidate
# Manual review required
# Convert the remediation guidance below into a validated script action

# TODO: replace the commented/manual steps above with validated PowerShell or registry logic.
