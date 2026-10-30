import os, re, sys

# Mapping from language code to the expected back‑button target page
expected_target = {
    'es': 'tv-time-alternative-android-app-es.html',
    'it': 'alternativa-tv-time-italiano.html',
    'fr': 'tv-time-alternative-android-app-fr.html',
    'de': 'tv-time-alternative-android-app-de.html',
    'ru': 'tv-time-alternative-android-app-ru.html',
    'en': 'tv-time-alternative-android-app.html',
}

root = '.'
issues = []
for fname in os.listdir(root):
    if not fname.lower().endswith('.html'):
        continue
    path = os.path.join(root, fname)
    with open(path, encoding='utf-8') as f:
        txt = f.read()
    # Get language
    m_lang = re.search(r'<html[^>]*lang=["\']([^"\']+)["\']', txt, re.IGNORECASE)
    lang = m_lang.group(1) if m_lang else 'en'
    expected = expected_target.get(lang, expected_target['en'])
    # Find back‑button href
    m_href = re.search(r'<a[^>]*class=["\'][^"\']*back-btn[^"\']*["\'][^>]*href=["\']([^"\']+)["\']', txt, re.IGNORECASE)
    href = m_href.group(1) if m_href else ''
    if href != expected:
        issues.append(f"{fname}: lang={lang}, href='{href}', expected='{expected}'")

if issues:
    for line in issues:
        sys.stdout.write(line + "\n")
else:
    sys.stdout.write('All back‑button links are correct.\n')
