import os, re, sys

# Mapping from language code to the appropriate home page (back button target)
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
    # Find back‑button anchor
    pattern = r'(<a[^>]*class=["\']([^"\']*\bback-btn\b[^"\']*)["\'][^>]*href=)["\'][^"\']*["\']'
    def repl(match):
        return f"{match.group(1)}\"{target}\""
    new_content, count = re.subn(pattern, repl, content, flags=re.IGNORECASE)
    if count > 0 and new_content != content:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        changed.append((fname, lang, target, count))

# Print summary
if changed:
    for fname, lang, target, cnt in changed:
        print(f"Updated {fname}: lang={lang}, set href to {target} (replacements={cnt})")
else:
    print('No back‑button links needed updating.')
