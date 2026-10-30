import os, re, sys

# Mapping language code to expected back button target for backup guide pages
expected = {
    'es': 'tv-time-alternative-android-app-es.html',
    'it': 'alternativa-tv-time-italiano.html',
    'fr': 'tv-time-alternative-android-app-fr.html',
    'de': 'tv-time-alternative-android-app-de.html',
    'ru': 'tv-time-alternative-android-app-ru.html',
    'en': 'tv-time-alternative-android-app.html',
}

# List of backup guide filenames and their language codes
backup_files = {
    'guia-backup-google-drive-watchmate.html': 'es',
    'guida-backup-google-drive-watchmate.html': 'it',
    'comment-sauvegarder-google-drive-watchmate.html': 'fr',
    'wie-man-google-drive-backup-einrichtet.html': 'de',
    'kak-nastroit-rezervnoe-kopirovanie-google-drive.html': 'ru',
    'how-to-backup-android-tv-tracker-google-drive.html': 'en',
}

issues = []
for fname, lang in backup_files.items():
    path = os.path.join('.', fname)
    if not os.path.exists(path):
        issues.append(f"Missing file: {fname}")
        continue
    with open(path, encoding='utf-8') as f:
        txt = f.read()
    # Find back‑button href
    m = re.search(r'<a[^>]*class=["\'][^"\']*back-btn[^"\']*["\'][^>]*href=["\']([^"\']+)["\']', txt, re.IGNORECASE)
    href = m.group(1) if m else ''
    expected_href = expected.get(lang, '')
    if href != expected_href:
        issues.append(f"{fname}: back href '{href}' does not match expected '{expected_href}'")

if issues:
    for line in issues:
        sys.stdout.write(line + "\n")
else:
    sys.stdout.write('All backup guide back‑button links are correct.\n')
