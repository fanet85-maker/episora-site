$files = Get-ChildItem -Path . -Filter *.html
foreach ($file in $files) {
    $content = Get-Content $file.FullName -Raw
    $lang = ''
    if ($content -match '<html[^>]*lang=["'']([^"'']+)["'']') {
        $lang = $matches[1]
    }
    $href = ''
    if ($content -match '<a[^>]*class=["''][^"'']*back-btn[^"'']*["''][^>]*href=["'']([^"'']+)["'']') {
        $href = $matches[1]
    }
    Write-Output "$($file.Name)|$lang|$href"
}
