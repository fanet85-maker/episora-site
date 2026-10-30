import os, re, sys

# Mapping language code to correct back‑button target page (ASCII only strings)
home_map = {
    'es': 'tv-time-alternative-android-app-es.html',
    'it': 'alternativa-tv-time-italiano.html',
    'fr': 'tv-time-alternative-android-app-fr.html',
    'de': 'tv-time-alternative-android-app-de.html',
    'ru': 'tv-time-alternative-android-app-ru.html',
    'en': 'tv-time-alternative-android-app.html',
}

changed = []
for fname in os.listdir('.'):
    if not fname.lower().endswith('.html'):
        continue
    path = os.path.join('.', fname)
    with open(path, encoding='utf-8') as f:
        content = f.read()
    m_lang = re.search(r'<html[^>]*lang=["\']([^"\']+)["\']', content, re.IGNORECASE)
    lang = m_lang.group(1) if m_lang else 'en'
    target = home_map.get(lang)
    if not target:
        continue
    # Replace href of <a class="... back-btn ..." href="...">
    pattern = r'(<a[^>]*class=["\'][^"\']*\bback-btn\b[^"\']*["\'][^>]*href=)["\'][^"\']*["\']'
    new_content, count = re.subn(pattern, r"\1\"{}\"".format(target), content, flags=re.IGNORECASE)
    if count > 0:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        changed.append((fname, lang, target, count))

if changed:
    for fname, lang, target, cnt in changed:
        sys.stdout.write(f"Updated {fname}: lang={lang}, href={target} (replacements={cnt})\n")
else:
    sys.stdout.write('No back-button links needed updating.\n')
