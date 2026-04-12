# CIS Benchmark: CIS Microsoft Windows 11 Stand-alone Benchmark
# Control: 19.7.8.1 - Ensure 'Configure Windows spotlight on lock screen' is set to 'Disabled'
# Source Page: 1263
# Confidence: 0.96
# Status: review_required

$ErrorActionPreference = 'Stop'

# Audit guidance extracted from the benchmark
# Navigate to the UI Path articulated in the Remediation section and confirm it is set as
# prescribed. This group policy setting is backed by the following registry location with a
# REG_DWORD value of 2.
# HKU\[USER
# SID]\Software\Policies\Microsoft\Windows\CloudContent:ConfigureWindowsSpotlig
# ht

# Remediation candidate
# Manual review required
# Convert the remediation guidance below into a validated script action

# TODO: replace the commented/manual steps above with validated PowerShell or registry logic.
