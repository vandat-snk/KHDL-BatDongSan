$ErrorActionPreference = 'Stop'
$taskRoot = Split-Path -Parent $PSScriptRoot
$reportPath = Join-Path $taskRoot 'docs\BAO_CAO_DO_AN.docx'
$qaDirectory = Join-Path $taskRoot 'tmp\qa_report'
New-Item -ItemType Directory -Force -Path $qaDirectory | Out-Null
$pdfPath = Join-Path $qaDirectory 'BAO_CAO_DO_AN.pdf'
$word = $null
$report = $null
try {
    $word = New-Object -ComObject Word.Application
    $word.Visible = $false
    $word.DisplayAlerts = 0
    $report = $word.Documents.Open($reportPath, $false, $true, $false)
    $report.Repaginate()
    $report.ExportAsFixedFormat($pdfPath, 17)
    Write-Output ('Rendered report pages: ' + $report.ComputeStatistics(2))
    Write-Output $pdfPath
}
finally {
    if ($null -ne $report) { $report.Close(0) }
    if ($null -ne $word) { $word.Quit() }
    if ($null -ne $report) { [System.Runtime.InteropServices.Marshal]::FinalReleaseComObject($report) | Out-Null }
    if ($null -ne $word) { [System.Runtime.InteropServices.Marshal]::FinalReleaseComObject($word) | Out-Null }
}
