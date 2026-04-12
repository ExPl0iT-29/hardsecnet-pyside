# CIS Benchmark: CIS Microsoft Windows 11 Stand-alone Benchmark
# Control: 18.9.26.2 - Ensure 'Configures LSASS to run as a protected process' is set to 'Enabled: Enabled with UEFI Lock'
# Source Page: 717
# Confidence: 0.96
# Status: review_required

$ErrorActionPreference = 'Stop'

# Audit guidance extracted from the benchmark
# Navigate to the UI Path articulated in the Remediation section and confirm it is set as
# prescribed. This group policy setting is backed by the following registry location with a
# REG_DWORD value of 1.
# HKLM\SYSTEM\CurrentControlSet\Control\Lsa:RunAsPPL
# Page 717

# Remediation candidate
registry location of HKLM\SYSTEM\CurrentControlSet\Control\Lsa:RunAsPPL was set
for Configures LSASS to run as a protected process. This same registry location and
setting Configures LSASS to run as a protected process has a new registry location of
version of the ADML/ADML templates, the new registry location will not auto-apply to

# TODO: replace the commented/manual steps above with validated PowerShell or registry logic.
