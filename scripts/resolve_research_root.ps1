[CmdletBinding()]
param(
  [Parameter()]
  [string]$ExplicitRoot
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

function ConvertTo-FullPath {
  param([Parameter(Mandatory)][string]$Path)

  $expanded = [Environment]::ExpandEnvironmentVariables($Path.Trim())
  return [IO.Path]::GetFullPath($expanded)
}

$configuredRoots = @(
  $ExplicitRoot,
  $env:NOTEBOOKLM_RESEARCH_ROOT,
  [Environment]::GetEnvironmentVariable('NOTEBOOKLM_RESEARCH_ROOT', 'User'),
  [Environment]::GetEnvironmentVariable('NOTEBOOKLM_RESEARCH_ROOT', 'Machine')
)

foreach ($configuredRoot in $configuredRoots) {
  if (-not [string]::IsNullOrWhiteSpace($configuredRoot)) {
    ConvertTo-FullPath -Path $configuredRoot
    exit 0
  }
}

$localObsidianVault = 'G:\obsidian_vault\Obsidian Vault'
if (Test-Path -LiteralPath $localObsidianVault -PathType Container) {
  ConvertTo-FullPath -Path $localObsidianVault
  exit 0
}

$documents = [Environment]::GetFolderPath('MyDocuments')
ConvertTo-FullPath -Path (Join-Path $documents 'NotebookLM Research')
