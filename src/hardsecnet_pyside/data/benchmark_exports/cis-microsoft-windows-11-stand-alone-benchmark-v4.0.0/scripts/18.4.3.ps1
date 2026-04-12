# CIS Benchmark: CIS Microsoft Windows 11 Stand-alone Benchmark
# Control: 18.4.3 - Ensure 'Enable Certificate Padding' is set to 'Enabled'
# Source Page: 490
# Confidence: 0.96
# Status: review_required

$ErrorActionPreference = 'Stop'

# Audit guidance extracted from the benchmark
# Navigate to the UI Path articulated in the Remediation section and confirm it is set as
# prescribed.
# This group policy setting is backed by the following registry location with a REG_DWORD
# or REG_SZ value of 1.
# HKLM\SOFTWARE\Microsoft\Cryptography\Wintrust\Config:EnableCertPaddingCheck
# 32-bit subsystem on 64-bit OS
# Navigate to the UI Path articulated in the Remediation section and confirm it is set as
# prescribed.
# This group policy setting is backed by the following registry location with a REG_DWORD
# or REG_SZ value of 1.
# HKLM\SOFTWARE\Wow6432Node\Microsoft\Cryptography\Wintrust\Config:EnableCertPa
# ddingCheck

# Remediation candidate
# Manual review required
# Convert the remediation guidance below into a validated script action

# TODO: replace the commented/manual steps above with validated PowerShell or registry logic.
