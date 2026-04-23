# CIS Benchmark: CIS Microsoft Windows 11 Stand-alone Benchmark
# Control: 9.2.5 - Ensure 'Windows Firewall: Private: Logging: Size limit (KB)' is set to '16,384 KB or greater'
# Status: reviewed_ready
# Review Notes: Firewall policy remediation implemented from benchmark-provided registry policy path and value.

param([switch]$Apply, [switch]$Rollback, [switch]$Status)
$ErrorActionPreference = "Stop"

$Path = "HKLM:\SOFTWARE\Policies\Microsoft\WindowsFirewall\PrivateProfile\Logging"
$Name = "LogFileSize"
$PropertyType = "DWord"
$DesiredValue = 16384
$ExpectedDescription = "LogFileSize >= 16384"
$SettingTitle = "9.2.5 - Ensure 'Windows Firewall: Private: Logging: Size limit (KB)' is set to '16,384 KB or greater'"
$RollbackDescription = "Rollback removes the policy value so the firewall profile returns to local default or Not Configured behavior."
$ComparisonMode = "min"

function Ensure-RegistryPath {
    if (-not (Test-Path $Path)) {
        New-Item -Path $Path -Force | Out-Null
    }
}

function Get-CurrentValue {
    if (-not (Test-Path $Path)) {
        return $null
    }
    $item = Get-ItemProperty -Path $Path -Name $Name -ErrorAction SilentlyContinue
    if ($null -eq $item) {
        return $null
    }
    return $item.$Name
}

function Set-DesiredValue {
    Ensure-RegistryPath
    $current = Get-CurrentValue
    if ($null -eq $current) {
        New-ItemProperty -Path $Path -Name $Name -PropertyType $PropertyType -Value $DesiredValue -Force | Out-Null
    } else {
        Set-ItemProperty -Path $Path -Name $Name -Value $DesiredValue
    }
}

function Remove-DesiredValue {
    if (Test-Path $Path) {
        Remove-ItemProperty -Path $Path -Name $Name -ErrorAction SilentlyContinue
    }
}

function Test-Compliant([object]$Current) {
    if ($null -eq $Current) { return $false }
    try { return ([int64]$Current -ge [int64]$DesiredValue) } catch { return $false }
}

function Format-Value([object]$Value) {
    if ($null -eq $Value) {
        return "<not configured>"
    }
    if ($Value -is [array]) {
        return ($Value -join ', ')
    }
    return [string]$Value
}

function Write-State {
    $current = Get-CurrentValue
    $on = Test-Compliant $current
    $label = if ($on) { "ON" } else { "OFF" }
    Write-Output "Setting: $SettingTitle"
    Write-Output "Registry: $Path\$Name"
    Write-Output "Expected: $ExpectedDescription"
    Write-Output "Current value: $(Format-Value $current)"
    Write-Output "Status: $label"
    Write-Output "Benefit: aligns local Defender Firewall profile policy with the CIS benchmark for this network profile setting."
}

if ($Status) {
    Write-State
} elseif ($Rollback) {
    Remove-DesiredValue
    Write-Output $RollbackDescription
    Write-State
} elseif ($Apply) {
    Set-DesiredValue
    Write-Output "Applied CIS-aligned firewall policy value."
    Write-State
} else {
    Write-Output "Dry run: would set $Path\$Name to $(Format-Value $DesiredValue)."
    Write-State
}
