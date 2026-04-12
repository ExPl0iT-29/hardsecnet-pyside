# CIS Benchmark: CIS Microsoft Windows 11 Stand-alone Benchmark
# Control: 19.7.8.5 - Ensure 'Turn off Spotlight collection on Desktop' is set to 'Enabled'
# Source Page: 1271
# Confidence: 0.96
# Status: review_required

$ErrorActionPreference = 'Stop'

# Audit guidance extracted from the benchmark
# Navigate to the UI Path articulated in the Remediation section and confirm it is set as
# prescribed. This group policy setting is backed by the following registry location with a
# REG_DWORD value of 1.
# HKU\[USER
# SID]\SOFTWARE\Policies\Microsoft\Windows\CloudContent:DisableSpotlightCollect
# ionOnDesktop

# Remediation candidate
# Manual review required
# Convert the remediation guidance below into a validated script action

# TODO: replace the commented/manual steps above with validated PowerShell or registry logic.
