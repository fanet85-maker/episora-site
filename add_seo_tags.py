from pathlib import Path

base = 'https://www.episora-watchmate.it/'

groups = {
    'main': [
        ('alternativa-tv-time-italiano.html', 'it'),
        ('tv-time-alternative-android-app.html', 'en'),
        ('tv-time-alternative-android-app-es.html', 'es'),
    ],
    'import': [
        ('come-importare-dati-tv-time-italiano.html', 'it'),
        ('how-to-import-tv-time-data-android.html', 'en'),
        ('como-importar-datos-tv-time-android.html', 'es'),
    ],
    'backup': [
        ('how-to-backup-android-tv-tracker-google-drive.html', 'en'),
        ('guia-backup-google-drive-watchmate.html', 'es'),
    ],
    'contact': [
        ('contatti-assistenza-italiano.html', 'it'),
        ('contact-support-english.html', 'en'),
        ('contacto-soporte-espanol.html', 'es'),
    ],
    'privacy': [
        ('privacy-policy-italiano.html', 'it'),
        ('privacy-policy-english.html', 'en'),
        ('politica-de-privacidad-espanol.html', 'es'),
    ],
    'credits': [
        ('credits-italiano.html', 'it'),
        ('credits-english.html', 'en'),
        ('creditos-espanol.html', 'es'),
    ],
}

file_to_group = {fname: entries for entries in groups.values() for fname, _ in entries}


def build_tags(fname, entries):
    tags = [f'<link rel="canonical" href="{base}{fname}" />']
    for other, lang in entries:
        if other != fname:
            tags.append(f'<link rel="alternate" hreflang="{lang}" href="{base}{other}" />')
    if len(entries) >= 3:
        tags.append(f'<link rel="alternate" hreflang="x-default" href="{base}" />')
    return '\n    '.join(tags)


for path in sorted(Path('.').glob('*.html')):
    name = path.name
    text = path.read_text(encoding='utf-8')
    if name == 'index.html':
        if '<link rel="canonical"' not in text:
            marker = '<meta name="viewport" content="width=device-width, initial-scale=1.0">'
            if marker in text:
                text = text.replace(marker, marker + '\n    <link rel="canonical" href="https://www.episora-watchmate.it/" />')
                path.write_text(text, encoding='utf-8')
                print('updated', name)
        continue
    if name in file_to_group:
        tags = build_tags(name, file_to_group[name])
    else:
        tags = f'<link rel="canonical" href="{base}{name}" />'
    if '<link rel="canonical"' in text:
        continue
    if '<meta name="description" content="' in text:
        pos = text.index('<meta name="description" content="')
        end = text.index('>', pos) + 1
        text = text[:end] + '\n    ' + tags + text[end:]
    elif '<meta name="viewport" content="width=device-width, initial-scale=1.0">' in text:
        marker = '<meta name="viewport" content="width=device-width, initial-scale=1.0">'
        text = text.replace(marker, marker + '\n    ' + tags)
    elif '</head>' in text:
        text = text.replace('</head>', '    ' + tags + '\n</head>')
    else:
        continue
    path.write_text(text, encoding='utf-8')
    print('updated', name)
