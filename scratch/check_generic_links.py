import os, re, sys

def find_generic_links():
    generic_backup = 'how-to-backup-android-tv-tracker-google-drive.html'
    generic_import = 'how-to-import-tv-time-data-android.html'
    pattern_backup = re.compile(re.escape(generic_backup), re.IGNORECASE)
    pattern_import = re.compile(re.escape(generic_import), re.IGNORECASE)
    found = []
    for fname in os.listdir('.'):
        if not fname.lower().endswith('.html'):
            continue
        path = os.path.join('.', fname)
        with open(path, encoding='utf-8') as f:
            content = f.read()
        for m in pattern_backup.finditer(content):
            found.append((fname, 'backup', m.start()))
        for m in pattern_import.finditer(content):
            found.append((fname, 'import', m.start()))
    return found

found = find_generic_links()
if found:
    for f, typ, pos in found:
        sys.stdout.write(f"Generic {typ} link found in {f}\n")
else:
    sys.stdout.write('No generic English guide links remain.\n')
