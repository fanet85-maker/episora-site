import os, re, sys

# Mapping from language code to appropriate guide filenames
backup_map = {
    'en': 'how-to-backup-android-tv-tracker-google-drive.html',
    'es': 'guia-backup-google-drive-watchmate.html',
    'it': 'guida-backup-google-drive-watchmate.html',
    'fr': 'comment-sauvegarder-google-drive-watchmate.html',
    'de': 'wie-man-google-drive-backup-einrichtet.html',
    'ru': 'kak-nastroit-rezervnoe-kopirovanie-google-drive.html',
}
import_map = {
    'en': 'how-to-import-tv-time-data-android.html',
    'es': 'como-importar-datos-tv-time-android.html',
    'it': 'come-importare-dati-tv-time-android.html',
    'fr': 'comment-importer-donnees-tv-time-android.html',
    'de': 'wie-man-tv-time-daten-importiert.html',
    'ru': 'kak-importirovat-dannye-tv-time-android.html',
}

# Patterns to detect the generic English guide links
english_backup = re.compile(r'how-to-backup-android-tv-tracker-google-drive\.html', re.IGNORECASE)
english_import = re.compile(r'how-to-import-tv-time-data-android\.html', re.IGNORECASE)

lang_regex = re.compile(r'<html[^>]*lang=["\']([^"\']+)["\']', re.IGNORECASE)

changed = []
for fname in os.listdir('.'):
    if not fname.lower().endswith('.html'):
        continue
    path = os.path.join('.', fname)
    with open(path, encoding='utf-8') as f:
        content = f.read()
    m_lang = lang_regex.search(content)
    lang = m_lang.group(1) if m_lang else 'en'
    new_content = content
    # Replace backup guide links
    if english_backup.search(new_content):
        target = backup_map.get(lang, backup_map['en'])
        new_content = english_backup.sub(target, new_content)
    # Replace import guide links
    if english_import.search(new_content):
        target = import_map.get(lang, import_map['en'])
        new_content = english_import.sub(target, new_content)
    if new_content != content:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        changed.append((fname, lang))

if changed:
    for f, l in changed:
        sys.stdout.write(f'Updated links in {f} for language {l}\n')
else:
    sys.stdout.write('No guide link updates necessary.\n')
