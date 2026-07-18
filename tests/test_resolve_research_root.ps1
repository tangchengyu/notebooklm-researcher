$ErrorActionPreference = 'Stop'
$resolver = Join-Path (Split-Path $PSScriptRoot -Parent) 'scripts\resolve_research_root.ps1'
$originalProcessRoot = $env:NOTEBOOKLM_RESEARCH_ROOT

try {
  $env:NOTEBOOKLM_RESEARCH_ROOT = 'C:\Process Research Root'
  $actual = & $resolver
  $expected = [IO.Path]::GetFullPath('C:\Process Research Root')
  if ($actual -ne $expected) {
    throw "Process environment root was not selected. Expected '$expected', got '$actual'."
  }

  $actual = & $resolver -ExplicitRoot 'D:\Explicit Research Root'
  $expected = [IO.Path]::GetFullPath('D:\Explicit Research Root')
  if ($actual -ne $expected) {
    throw "Explicit root did not take precedence. Expected '$expected', got '$actual'."
  }

  Write-Output 'resolve_research_root: tests passed'
}
finally {
  $env:NOTEBOOKLM_RESEARCH_ROOT = $originalProcessRoot
}
