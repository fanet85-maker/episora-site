import os, re, sys

def get_lang(content):
    m = re.search(r'<html[^>]*lang=["\']([^"\']+)["\']', content, re.IGNORECASE)
    return m.group(1) if m else 'en'

def get_back_href(content):
    m = re.search(r'<a[^>]*class=["\'][^"\']*back-btn[^"\']*["\'][^>]*href=["\']([^"\']+)["\']', content, re.IGNORECASE)
    return m.group(1) if m else ''

suffix_map = {'es':'-es', 'fr':'-fr', 'de':'-de', 'it':'-it', 'ru':'-ru', 'en':''}

root = '.'
for fname in os.listdir(root):
    if not fname.lower().endswith('.html'):
        continue
    with open(os.path.join(root, fname), encoding='utf-8') as f:
        txt = f.read()
    lang = get_lang(txt)
    href = get_back_href(txt)
    expected_suffix = suffix_map.get(lang, '')
    # expected href should end with expected_suffix + '.html' or for en no suffix
    ok = False
    if expected_suffix == '':
        ok = not re.search(r'-(es|fr|de|it|ru)\.html$', href)
    else:
        ok = href.endswith(expected_suffix + '.html')
    if not ok:
        print(f"{fname}|lang={lang}|href={href}|expected_suffix={expected_suffix}")
