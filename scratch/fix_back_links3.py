import os, re, sys

# Expected back‑button target per language (home page)
home_map = {
    'es': 'tv-time-alternative-android-app-es.html',
    'it': 'alternativa-tv-time-italiano.html',
    'fr': 'tv-time-alternative-android-app-fr.html',
    'de': 'tv-time-alternative-android-app-de.html',
    'ru': 'tv-time-alternative-android-app-ru.html',
    'en': 'tv-time-alternative-android-app.html',
}

def replace_back_href(content, target):
    # Find each <a ...> tag
    def repl(match):
        attrs = match.group('attrs')
        # check class attribute contains back-btn
        if re.search(r'class=["\'][^"\']*back-btn[^"\']*["\']', attrs, re.IGNORECASE):
            # replace or add href attribute
            if re.search(r'href=["\']', attrs, re.IGNORECASE):
                new_attrs = re.sub(r'href=["\'][^"\']*["\']', f'href="{target}"', attrs, flags=re.IGNORECASE)
            else:
                new_attrs = attrs + f' href="{target}"'
            return f'<a{new_attrs}>'
        return match.group(0)
    return re.sub(r'<a(?P<attrs>[^>]*?)>', repl, content, flags=re.IGNORECASE)

changed = []
for fname in os.listdir('.'):
    if not fname.lower().endswith('.html'):
        continue
    path = os.path.join('.', fname)
    with open(path, encoding='utf-8') as f:
        txt = f.read()
    # detect language
    m_lang = re.search(r'<html[^>]*lang=["\']([^"\']+)["\']', txt, re.IGNORECASE)
    lang = m_lang.group(1) if m_lang else 'en'
    target = home_map.get(lang, home_map['en'])
    new_txt = replace_back_href(txt, target)
    if new_txt != txt:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(new_txt)
        changed.append((fname, lang, target))

if changed:
    for f, l, t in changed:
        sys.stdout.write(f"Updated {f}: lang={l}, href set to {t}\n")
else:
    sys.stdout.write('No back‑button links needed updating.\n')
