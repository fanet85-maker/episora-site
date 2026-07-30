$files = Get-ChildItem -Filter *.html
foreach ($file in $files) {
    $text = Get-Content -Raw -Path $file.FullName -Encoding UTF8
    if ($text -match 'Ã|Â') {
        $bytes = [System.Text.Encoding]::GetEncoding(1252).GetBytes($text)
        $fixed = [System.Text.Encoding]::UTF8.GetString($bytes)
        if ($fixed -ne $text) {
            [System.IO.File]::WriteAllText($file.FullName, $fixed, [System.Text.Encoding]::UTF8)
            Write-Output "fixed $($file.Name)"
        }
    }
}
