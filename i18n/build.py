#!/usr/bin/env python3
"""GoIPPro i18n Build System v2 — All pages, all languages"""

import json, os, re
from pathlib import Path

ROOT = Path(__file__).parent.parent
LANGS_DIR = ROOT / 'i18n' / 'langs'

PAGES = [
    'index.html',
    'for-pros/index.html',
    'for-pros/termination/index.html',
    'for-pros/sms-operators/index.html',
    'for-buyers/index.html',
    'how-to-start/index.html',
    'goip-devices/index.html',
    'rules/index.html',
    'verify/index.html',
]

LANGUAGES = {
    'en': {'dir': 'ltr'}, 'ru': {'dir': 'ltr'}, 'tr': {'dir': 'ltr'},
    'ar': {'dir': 'rtl'}, 'fa': {'dir': 'rtl'}, 'fr': {'dir': 'ltr'},
    'zh': {'dir': 'ltr'}, 'ur': {'dir': 'rtl'}, 'ko': {'dir': 'ltr'},
}

LANG_CODES = [l for l in LANGUAGES if l != 'en']

def make_hreflang(page_path):
    base = 'https://goippro.com'
    suffix = '' if page_path == 'index.html' else page_path.replace('index.html','')
    tags = [
        f'  <link rel="alternate" hreflang="en" href="{base}/{suffix}">',
        f'  <link rel="alternate" hreflang="x-default" href="{base}/{suffix}">',
    ]
    for lang in LANG_CODES:
        if (LANGS_DIR / f'{lang}.json').exists():
            tags.append(f'  <link rel="alternate" hreflang="{lang}" href="{base}/{lang}/{suffix}">')
    return '\n'.join(tags)

def build_page(en_html, lang, translations, page_path):
    html = en_html
    
    # html lang + dir
    html = re.sub(r'<html lang="[^"]*"(\s*dir="[^"]*")?', f'<html lang="{lang}"', html)
    if LANGUAGES[lang]['dir'] == 'rtl':
        html = html.replace(f'<html lang="{lang}"', f'<html lang="{lang}" dir="rtl"')
    
    # canonical
    suffix = '' if page_path == 'index.html' else page_path.replace('index.html','')
    html = re.sub(r'<link rel="canonical" href="https://goippro\.com/[^"]*"',
                  f'<link rel="canonical" href="https://goippro.com/{lang}/{suffix}"', html)
    
    # og:url
    html = re.sub(r'<meta property="og:url" content="https://goippro\.com/[^"]*"',
                  f'<meta property="og:url" content="https://goippro.com/{lang}/{suffix}"', html)
    
    # hreflang: remove old, add new
    html = re.sub(r'  <link rel="alternate" hreflang="[^"]*" href="[^"]*">\n?', '', html)
    hreflang = make_hreflang(page_path)
    html = re.sub(r'(<link rel="canonical"[^>]*>)', r'\1\n' + hreflang, html)
    
    # Apply translations (longest first to avoid partial matches)
    sorted_trans = sorted(translations.items(), key=lambda x: -len(x[0]))
    for en_text, tr_text in sorted_trans:
        html = html.replace(en_text, tr_text)
    
    # Language switcher: make links
    for l in LANG_CODES:
        html = html.replace(f'<a href="/{l}/" class="lang" data-lang="{l}">', 
                           f'<a href="/{l}/{suffix}" class="lang" data-lang="{l}">')
        html = html.replace(f'<a href="/{l}/" class="lang active" data-lang="{l}">',
                           f'<a href="/{l}/{suffix}" class="lang active" data-lang="{l}">')
    
    # Highlight current language
    html = html.replace(f'class="lang active" data-lang="en"', f'class="lang" data-lang="en"')
    html = html.replace(f'class="lang" data-lang="{lang}"', f'class="lang active" data-lang="{lang}"')
    
    # RTL CSS
    if LANGUAGES[lang]['dir'] == 'rtl' and '/* RTL Support */' not in html:
        rtl = '\n    /* RTL Support */\n    body{direction:rtl;text-align:right;}\n'
        html = html.replace('</style>', rtl + '  </style>', 1)
    
    return html

def build_all():
    total = 0
    for page in PAGES:
        en_path = ROOT / page
        if not en_path.exists():
            continue
        with open(en_path) as f:
            en_html = f.read()
        
        for lang in LANG_CODES:
            tr_file = LANGS_DIR / f'{lang}.json'
            if not tr_file.exists():
                continue
            with open(tr_file) as f:
                translations = json.load(f)
            
            translated = build_page(en_html, lang, translations, page)
            
            out_dir = ROOT / lang / os.path.dirname(page)
            out_dir.mkdir(parents=True, exist_ok=True)
            out_path = ROOT / lang / page
            with open(out_path, 'w') as f:
                f.write(translated)
            total += 1
    
    print(f"Generated {total} pages ({len(PAGES)} pages × {len(LANG_CODES)} languages)")

if __name__ == '__main__':
    build_all()
