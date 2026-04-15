# Pandoc writes diagnostics to stderr; do not treat that as a terminating error.
$ErrorActionPreference = "Continue"
$here = $PSScriptRoot
$md = Join-Path $here "Vision_Series_Production_Test_Plan.md"
$ref = Join-Path $here "templates\word_document_template.docx"
$out = Join-Path $here "Vision_Series_Production_Test_Plan.docx"
$alt = Join-Path $here "Vision_Series_Production_Test_Plan_from_template.docx"
$pandoc = if (Test-Path "$env:LOCALAPPDATA\Pandoc\pandoc.exe") {
    "$env:LOCALAPPDATA\Pandoc\pandoc.exe"
} else {
    "${env:ProgramFiles}\Pandoc\pandoc.exe"
}

if (-not (Test-Path $pandoc)) {
    Write-Error "Pandoc not found. Install with: winget install JohnMacFarlane.Pandoc"
}
if (-not (Test-Path $ref)) {
    Write-Error "Reference document not found: $ref"
}

Set-Location $here
& $pandoc $md -o $out --reference-doc="$ref" *>$null

if ($LASTEXITCODE -ne 0) {
    & $pandoc $md -o $alt --reference-doc="$ref"
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
    Write-Warning "Could not write '$out' (file in use?). Wrote '$alt' instead. Close Word and run this script again to update '$out'."
    exit 0
}

Write-Host "Wrote: $out"
