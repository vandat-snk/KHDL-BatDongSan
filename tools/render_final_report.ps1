param([string]$Document = 'docs\BAO_CAO_TIEU_LUAN_DA_RA_SOAT.docx')
$ErrorActionPreference = 'Stop'
$taskRoot = Split-Path -Parent $PSScriptRoot
$reportPath = [System.IO.Path]::GetFullPath((Join-Path $taskRoot $Document))
$docsRoot = [System.IO.Path]::GetFullPath((Join-Path $taskRoot 'docs'))
if (-not $reportPath.StartsWith($docsRoot + [System.IO.Path]::DirectorySeparatorChar, [StringComparison]::OrdinalIgnoreCase)) {
    throw 'Report must be inside the project docs folder.'
}
$qaDirectory = Join-Path $taskRoot 'tmp\report_qa'
New-Item -ItemType Directory -Force -Path $qaDirectory | Out-Null
$pdfPath = [System.IO.Path]::ChangeExtension($reportPath, '.pdf')
$word = $null
$report = $null
try {
    $word = New-Object -ComObject Word.Application
    $word.Visible = $false
    $word.DisplayAlerts = 0
    $report = $word.Documents.Open($reportPath, $false, $false, $false)
    for ($pass = 0; $pass -lt 3; $pass++) {
        $report.Repaginate()
        $null = $report.Fields.Update()
    }
    foreach ($section in $report.Sections) {
        foreach ($footer in $section.Footers) { $null = $footer.Range.Fields.Update() }
    }
    $report.Repaginate()
    $report.Save()
    $report.ExportAsFixedFormat($pdfPath, 17)
    $layout = @()
    foreach ($bookmark in $report.Bookmarks) {
        $layout += [ordered]@{ name = $bookmark.Name; page = $bookmark.Range.Information(3); text = $bookmark.Range.Text.Trim() }
    }
    $result = [ordered]@{
        backend = 'Microsoft Word document object model; headless export'
        pages = $report.ComputeStatistics(2)
        native_equations = $report.OMaths.Count
        document = $reportPath
        pdf = $pdfPath
        bookmarks = $layout
    }
    $result | ConvertTo-Json -Depth 6 | Set-Content -LiteralPath (Join-Path $qaDirectory 'word_layout.json') -Encoding utf8
    [pscustomobject]$result | Select-Object backend, pages, native_equations, document, pdf | ConvertTo-Json
}
finally {
    if ($null -ne $report) { $report.Close(0) }
    if ($null -ne $word) { $word.Quit() }
    if ($null -ne $report) { [System.Runtime.InteropServices.Marshal]::FinalReleaseComObject($report) | Out-Null }
    if ($null -ne $word) { [System.Runtime.InteropServices.Marshal]::FinalReleaseComObject($word) | Out-Null }
}
