# CIS Benchmark: CIS Microsoft Windows 11 Stand-alone Benchmark
# Control: 2.3.17.8 - Ensure 'User Account Control: Virtualize file and registry write failures to per-user locations' is set to 'Enabled'
# Source Page: 282
# Confidence: 0.96
# Status: review_required

$ErrorActionPreference = 'Stop'

# Audit guidance extracted from the benchmark
# Navigate to the UI Path articulated in the Remediation section and confirm it is set as
# prescribed. This group policy setting is backed by the following registry location with a
# REG_DWORD value of 1.
# HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System:EnableVirtuali
# zation
# Page 282

# Remediation candidate
Policies\Security Options\User Account Control: Virtualize file and registry

# TODO: replace the commented/manual steps above with validated PowerShell or registry logic.
