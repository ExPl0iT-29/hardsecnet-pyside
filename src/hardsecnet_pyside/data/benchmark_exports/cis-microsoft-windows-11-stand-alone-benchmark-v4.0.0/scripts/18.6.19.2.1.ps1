# CIS Benchmark: CIS Microsoft Windows 11 Stand-alone Benchmark
# Control: 18.6.19.2.1 - Disable IPv6 (Ensure TCPIP6 Parameter 'DisabledComponents' is set to '0xff (255)')
# Source Page: 585
# Confidence: 0.96
# Status: review_required

$ErrorActionPreference = 'Stop'

# Audit guidance extracted from the benchmark
# Navigate to the UI Path articulated in the Remediation section and confirm it is set as
# prescribed. This group policy setting is backed by the following registry location with a
# REG_DWORD value of 255.
# HKLM\SYSTEM\CurrentControlSet\Services\TCPIP6\Parameters:DisabledComponents
# Page 585

# Remediation candidate
registry value, custom templates (Configure-IPv6-Components-
setting must be applied to change the registry value to the opposite state.

# TODO: replace the commented/manual steps above with validated PowerShell or registry logic.
