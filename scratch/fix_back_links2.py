import os, re, sys

# Mapping language code to appropriate back‑button target page
home_map = {
    'es': 'tv-time-alternative-android-app-es.html',
    'it': 'alternativa-tv-time-italiano.html',
    'fr': 'tv-time-alternative-android-app-fr.html',
    'de': 'tv-time-alternative-android-app-de.html',
    'ru': 'tv-time-alternative-android-app-ru.html',
    'en': 'tv-time-alternative-android-app.html',
}

root = '.'
changed = []
for fname in os.listdir(root):
    if not fname.lower().endswith('.html'):
        continue
    path = os.path.join(root, fname)
    with open(path, encoding='utf-8') as f:
        content = f.read()
    # Detect language from <html lang="..">
    m_lang = re.search(r'<html[^>]*lang=["\']([^"\']+)["\']', content, re.IGNORECASE)
    lang = m_lang.group(1) if m_lang else 'en'
    target = home_map.get(lang)
    if not target:
        continue
    # Replace href of the back‑button anchor (class contains back-btn)
    pattern = r'(<a[^>]*class=["\'][^"\']*\bback-btn\b[^"\']*["\'][^>]*href=)["\'][^"\']*["\']'
    new_content, count = re.subn(pattern, r"\1\"{}\"".format(target), content, flags=re.IGNORECASE)
    if count > 0 and new_content != content:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        changed.append((fname, lang, target, count))

# Output summary using only ASCII characters
if changed:
    for fname, lang, target, cnt in changed:
        sys.stdout.write(f"Updated {fname}: lang={lang}, href set to {target} (replacements={cnt})\n")
else:
    sys.stdout.write('No back‑button links required updating.\n')
