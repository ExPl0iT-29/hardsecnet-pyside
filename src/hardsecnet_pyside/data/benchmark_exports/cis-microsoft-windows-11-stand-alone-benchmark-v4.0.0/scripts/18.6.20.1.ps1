# CIS Benchmark: CIS Microsoft Windows 11 Stand-alone Benchmark
# Control: 18.6.20.1 - Ensure 'Configuration of wireless settings using Windows Connect Now' is set to 'Disabled'
# Source Page: 588
# Confidence: 0.96
# Status: review_required

$ErrorActionPreference = 'Stop'

# Audit guidance extracted from the benchmark
# Navigate to the UI Path articulated in the Remediation section and confirm it is set as
# prescribed. This group policy setting is backed by the following registry locations with a
# REG_DWORD value of 0.
# HKLM\SOFTWARE\Policies\Microsoft\Windows\WCN\Registrars:EnableRegistrars
# HKLM\SOFTWARE\Policies\Microsoft\Windows\WCN\Registrars:DisableUPnPRegistrar
# HKLM\SOFTWARE\Policies\Microsoft\Windows\WCN\Registrars:DisableInBand802DOT11
# Registrar
# HKLM\SOFTWARE\Policies\Microsoft\Windows\WCN\Registrars:DisableFlashConfigReg
# istrar
# HKLM\SOFTWARE\Policies\Microsoft\Windows\WCN\Registrars:DisableWPDRegistrar
# Page 588

# Remediation candidate
# Manual review required
# Convert the remediation guidance below into a validated script action

# TODO: replace the commented/manual steps above with validated PowerShell or registry logic.
