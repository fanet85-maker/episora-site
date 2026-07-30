$base = 'https://www.episora-watchmate.it/'
$groups = @(
    @{ Files = @(
        @{ Name = 'alternativa-tv-time-italiano.html'; Lang = 'it' }
        @{ Name = 'tv-time-alternative-android-app.html'; Lang = 'en' }
        @{ Name = 'tv-time-alternative-android-app-es.html'; Lang = 'es' }
    ) }
    @{ Files = @(
        @{ Name = 'come-importare-dati-tv-time-italiano.html'; Lang = 'it' }
        @{ Name = 'how-to-import-tv-time-data-android.html'; Lang = 'en' }
        @{ Name = 'como-importar-datos-tv-time-android.html'; Lang = 'es' }
    ) }
    @{ Files = @(
        @{ Name = 'how-to-backup-android-tv-tracker-google-drive.html'; Lang = 'en' }
        @{ Name = 'guia-backup-google-drive-watchmate.html'; Lang = 'es' }
    ) }
    @{ Files = @(
        @{ Name = 'contatti-assistenza-italiano.html'; Lang = 'it' }
        @{ Name = 'contact-support-english.html'; Lang = 'en' }
        @{ Name = 'contacto-soporte-espanol.html'; Lang = 'es' }
    ) }
    @{ Files = @(
        @{ Name = 'privacy-policy-italiano.html'; Lang = 'it' }
        @{ Name = 'privacy-policy-english.html'; Lang = 'en' }
        @{ Name = 'politica-de-privacidad-espanol.html'; Lang = 'es' }
    ) }
    @{ Files = @(
        @{ Name = 'credits-italiano.html'; Lang = 'it' }
        @{ Name = 'credits-english.html'; Lang = 'en' }
        @{ Name = 'creditos-espanol.html'; Lang = 'es' }
    ) }
)

$fileToGroup = @{}
foreach ($group in $groups) {
    foreach ($entry in $group.Files) {
        $fileToGroup[$entry.Name] = $group.Files
    }
}

function Build-Tags($currentName, $entries) {
    $tags = @()
    $tags += '<link rel="canonical" href="' + $base + $currentName + '" />'
    foreach ($entry in $entries) {
        if ($entry.Name -ne $currentName) {
            $tags += '<link rel="alternate" hreflang="' + $($entry.Lang) + '" href="' + $base + $($entry.Name) + '" />'
        }
    }
    if ($entries.Count -ge 3) {
        $tags += '<link rel="alternate" hreflang="x-default" href="' + $base + '" />'
    }
    return $tags -join "`n    "
}

Get-ChildItem -Filter *.html | ForEach-Object {
    $path = $_.FullName
    $name = $_.Name
    $text = Get-Content -Raw -Path $path
    if ($name -eq 'index.html') {
        if ($text -notmatch 'rel="canonical"') {
            $marker = '<meta name="viewport" content="width=device-width, initial-scale=1.0">'
            if ($text.Contains($marker)) {
                $text = $text.Replace($marker, $marker + "`n    <link rel='canonical' href='" + $base + "' />")
                Set-Content -Path $path -Value $text -Encoding UTF8
                Write-Output "updated $name"
            }
        }
        return
    }

    if ($fileToGroup.ContainsKey($name)) {
        $tags = Build-Tags -currentName $name -entries $fileToGroup[$name]
    }
    else {
        $tags = "<link rel=\"canonical\" href=\"$base$name\" />"
    }

    if ($text -match 'rel="canonical"') {
        return
    }

    if ($text.Contains('<meta name="description" content="')) {
        $pos = $text.IndexOf('<meta name="description" content="')
        $end = $text.IndexOf('>', $pos) + 1
        $text = $text.Insert($end, "`n    $tags")
    }
    elseif ($text.Contains('<meta name="viewport" content="width=device-width, initial-scale=1.0">')) {
        $marker = '<meta name="viewport" content="width=device-width, initial-scale=1.0">'
        $text = $text.Replace($marker, $marker + "`n    $tags")
    }
    elseif ($text.Contains('</head>')) {
        $text = $text.Replace('</head>', "    $tags`n</head>")
    }

    Set-Content -Path $path -Value $text -Encoding UTF8
    Write-Output "updated $name"
}
