# CIS Benchmark: CIS Microsoft Windows 11 Stand-alone Benchmark
# Control: 18.5.3 - Ensure 'MSS: (DisableIPSourceRouting) IP source routing protection level' is set to 'Enabled: Highest protection, source routing is completely disabled'
# Source Page: 505
# Confidence: 0.96
# Status: review_required

$ErrorActionPreference = 'Stop'

# Audit guidance extracted from the benchmark
# Navigate to the UI Path articulated in the Remediation section and confirm it is set as
# prescribed. This group policy setting is backed by the following registry location with a
# REG_DWORD value of 2.
# HKLM\SYSTEM\CurrentControlSet\Services\Tcpip\Parameters:DisableIPSourceRoutin
# g

# Remediation candidate
# Manual review required
# Convert the remediation guidance below into a validated script action

# TODO: replace the commented/manual steps above with validated PowerShell or registry logic.
