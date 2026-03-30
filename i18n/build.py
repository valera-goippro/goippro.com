#!/usr/bin/env python3
"""GoIPPro i18n Build System v2 — All pages, all languages"""

import json, os, re
from pathlib import Path

ROOT = Path(__file__).parent.parent
LANGS_DIR = ROOT / 'i18n' / 'langs'

# All pages to translate
PAGES = [
    'index.html',
    'for-pros/index.html',
    'for-pros/termination/index.html',
    'for-pros/sms-operators/index.html',
    'how-to-start/index.html',
    'goip-devices/index.html',
    'rules/index.html',
    'for-buyers/index.html',
    'verify/index.html',
]

LANGUAGES = {
    'en': {'dir': 'ltr'},
    'ru': {'dir': 'ltr'},
    'tr': {'dir': 'ltr'},
    'ar': {'dir': 'rtl'},
    'fa': {'dir': 'rtl'},
    'fr': {'dir': 'ltr'},
    'zh': {'dir': 'ltr'},
    'ur': {'dir': 'rtl'},
    'ko': {'dir': 'ltr'},
    'pt': {'dir': 'ltr'},
    'es': {'dir': 'ltr'},
}

LANGS_WITH_FILES = []

def init():
    global LANGS_WITH_FILES
    for lang in LANGUAGES:
        if lang == 'en': continue
        if (LANGS_DIR / f'{lang}.json').exists():
            LANGS_WITH_FILES.append(lang)

def load_translations(lang):
    fpath = LANGS_DIR / f'{lang}.json'
    if fpath.exists():
        with open(fpath) as f:
            return json.load(f)
    return {}

def make_hreflang(page_path):
    base = 'https://goippro.com'
    tags = []
    
    if page_path == 'index.html':
        en_url = f'{base}/'
    else:
        p = page_path.replace('/index.html', '/').replace('index.html', '')
        en_url = f'{base}/{p}'
    
    tags.append(f'  <link rel="alternate" hreflang="en" href="{en_url}">')
    tags.append(f'  <link rel="alternate" hreflang="x-default" href="{en_url}">')
    
    for lang in LANGS_WITH_FILES:
        if page_path == 'index.html':
            url = f'{base}/{lang}/'
        else:
            p = page_path.replace('/index.html', '/').replace('index.html', '')
            url = f'{base}/{lang}/{p}'
        tags.append(f'  <link rel="alternate" hreflang="{lang}" href="{url}">')
    
    return '\n'.join(tags)

def get_page_url(page_path, lang=None):
    base = 'https://goippro.com'
    if page_path == 'index.html':
        path = ''
    else:
        path = page_path.replace('/index.html', '/').replace('index.html', '')
    
    if lang:
        return f'{base}/{lang}/{path}'
    return f'{base}/{path}'

def build_page(en_html, lang, translations, page_path):
    html = en_html
    
    # 1. html lang + dir
    html = re.sub(r'<html lang="[^"]*"', f'<html lang="{lang}"', html)
    if LANGUAGES[lang]['dir'] == 'rtl':
        html = html.replace(f'<html lang="{lang}"', f'<html lang="{lang}" dir="rtl"')
    
    # 2. Replace hreflang
    html = re.sub(r'  <link rel="alternate" hreflang="[^"]*" href="[^"]*">\n?', '', html)
    new_hreflang = make_hreflang(page_path)
    
    en_canonical = get_page_url(page_path)
    lang_canonical = get_page_url(page_path, lang)
    
    # Update canonical
    html = html.replace(f'href="{en_canonical}"', f'href="{lang_canonical}"')
    
    # Insert hreflang after canonical
    canon_tag = f'<link rel="canonical" href="{lang_canonical}">'
    if canon_tag in html:
        html = html.replace(canon_tag, canon_tag + '\n' + new_hreflang)
    
    # 3. Update OG URL
    html = html.replace(
        f'<meta property="og:url" content="{en_canonical}">',
        f'<meta property="og:url" content="{lang_canonical}">'
    )
    
    # 4. Apply translations (longest first to avoid partial matches)
    sorted_trans = sorted(translations.items(), key=lambda x: len(x[0]), reverse=True)
    for en_text, translated in sorted_trans:
        html = html.replace(en_text, translated)
    
    # 5. Language switcher — make current lang active
    html = html.replace('class="lang active"', 'class="lang"')
    # Find the button/link for this language and make it active
    for pattern in [
        f'class="lang" data-lang="{lang}"',
        f"class=\"lang\" data-lang=\"{lang}\""
    ]:
        html = html.replace(pattern, f'class="lang active" data-lang="{lang}"')
    
    # 7a. Swap video sources for translated versions
    video_map = {
        'ru': 'goippro_tutorial_ru.mp4',
    }
    if lang in video_map:
        html = html.replace('goippro_tutorial_en.mp4', video_map[lang])
    
    # 7. Rewrite internal links to include language prefix
    # e.g., href="/for-pros/" → href="/ru/for-pros/" on Russian pages
    internal_paths = [
        '/for-pros/', '/for-pros/termination/', '/for-pros/sms-operators/',
        '/for-buyers/', '/verify/', '/how-to-start/', '/goip-devices/', '/rules/',
    ]
    for path in internal_paths:
        # href="/path/" → href="/lang/path/"
        html = html.replace(f'href="{path}"', f'href="/{lang}{path}"')
    
    # Also fix homepage link: href="/" should go to /lang/
    # But only for nav links, not for logo (which should stay /)
    # Replace in nav context: links with just "/" that are language switcher
    # Keep href="/" for logo, replace others
    # Actually, the language switcher links should stay as-is (they point to specific langs)
    # Just the "Login" link should stay at /dashboard/ (no lang prefix for dashboard)
    
    # 6. RTL CSS
    if LANGUAGES[lang]['dir'] == 'rtl' and '/* RTL Support */' not in html:
        rtl_css = """
    /* RTL Support */
    body { direction: rtl; text-align: right; }
    .nav, .nav-links { flex-direction: row-reverse; }
    .hero-btns, .hero-buttons { flex-direction: row-reverse; }
    .footer-links { direction: rtl; }
"""
        html = html.replace('</style>', rtl_css + '  </style>')
    
    return html

def build_all():
    init()
    total = 0
    
    for page in PAGES:
        en_path = ROOT / page
        if not en_path.exists():
            continue
        
        with open(en_path) as f:
            en_html = f.read()
        
        for lang in LANGS_WITH_FILES:
            translations = load_translations(lang)
            if not translations:
                continue
            
            translated = build_page(en_html, lang, translations, page)
            
            # Output path: /lang/page
            if page == 'index.html':
                out_dir = ROOT / lang
            else:
                page_dir = os.path.dirname(page)
                out_dir = ROOT / lang / page_dir
            
            out_dir.mkdir(parents=True, exist_ok=True)
            out_path = out_dir / 'index.html'
            
            with open(out_path, 'w') as f:
                f.write(translated)
            
            total += 1
        
        print(f"  ✓ {page} → {len(LANGS_WITH_FILES)} languages")
    
    print(f"\nTotal: {total} pages generated")

if __name__ == '__main__':
    build_all()
