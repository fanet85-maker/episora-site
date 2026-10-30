import os, re, sys

# Mapping language code to filenames for backup guide and import guide
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
    'ru': 'kak-importirovat-dannye-tv-time-android.html',  # placeholder if exists
}

# Helper to get language from HTML content
lang_regex = re.compile(r'<html[^>]*lang=["\']([^"\']+)["\']', re.IGNORECASE)

# Patterns to replace generic English guide links with language‑specific ones
patterns = {
    r'how-to-backup-android-tv-tracker-google-drive\.html': lambda lang: backup_map.get(lang, backup_map['en']),
    r'how-to-import-tv-time-data-android\.html': lambda lang: import_map.get(lang, import_map['en']),
}

root = '.'
changed_files = []
for fname in os.listdir(root):
    if not fname.lower().endswith('.html'):
        continue
    path = os.path.join(root, fname)
    with open(path, encoding='utf-8') as f:
        content = f.read()
    m_lang = lang_regex.search(content)
    lang = m_lang.group(1) if m_lang else 'en'
    new_content = content
    for pat, repl_func in patterns.items():
        # Find all occurrences of the English filename
        regex = re.compile(pat, re.IGNORECASE)
        for match in regex.finditer(new_content):
            target = repl_func(lang)
            if target:
                new_content = new_content.replace(match.group(0), target)
    if new_content != content:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        changed_files.append((fname, lang))

if changed_files:
    for f, l in changed_files:
        sys.stdout.write(f"Updated links in {f} for language {l}\n")
else:
    sys.stdout.write('No link updates were necessary.\n')
