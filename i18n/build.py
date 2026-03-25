#!/usr/bin/env python3
"""
GoIPPro i18n Build System
Generates translated pages in subdirectories with proper hreflang + SEO
"""

import json, os, re, copy, sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
LANGS_DIR = ROOT / 'i18n' / 'langs'
OUTPUT_PAGES = ['index.html']  # Start with homepage, expand later

# Language configs
LANGUAGES = {
    'en': {'name': 'English', 'dir': 'ltr', 'native': 'English'},
    'ru': {'name': 'Russian', 'dir': 'ltr', 'native': 'Русский'},
    'tr': {'name': 'Turkish', 'dir': 'ltr', 'native': 'Türkçe'},
    'ar': {'name': 'Arabic', 'dir': 'rtl', 'native': 'العربية'},
    'fa': {'name': 'Persian', 'dir': 'rtl', 'native': 'فارسی'},
    'fr': {'name': 'French', 'dir': 'ltr', 'native': 'Français'},
    'zh': {'name': 'Chinese', 'dir': 'ltr', 'native': '中文'},
    'ur': {'name': 'Urdu', 'dir': 'rtl', 'native': 'اردو'},
    'ko': {'name': 'Korean', 'dir': 'ltr', 'native': '한국어'},
}

def load_translations(lang):
    fpath = LANGS_DIR / f'{lang}.json'
    if fpath.exists():
        with open(fpath) as f:
            return json.load(f)
    return {}

def generate_hreflang_tags(page_path):
    """Generate hreflang tags for all language versions"""
    tags = []
    base_url = 'https://goippro.com'
    
    # EN is at root
    en_url = f'{base_url}/{page_path}' if page_path != 'index.html' else f'{base_url}/'
    tags.append(f'  <link rel="alternate" hreflang="en" href="{en_url}">')
    tags.append(f'  <link rel="alternate" hreflang="x-default" href="{en_url}">')
    
    # Other languages in subdirectories
    for lang in LANGUAGES:
        if lang == 'en':
            continue
        lang_file = LANGS_DIR / f'{lang}.json'
        if lang_file.exists():
            if page_path == 'index.html':
                url = f'{base_url}/{lang}/'
            else:
                url = f'{base_url}/{lang}/{page_path}'
            tags.append(f'  <link rel="alternate" hreflang="{lang}" href="{url}">')
    
    return '\n'.join(tags)

def build_translated_page(html, lang, translations, page_path):
    """Build a translated version of the page"""
    
    # 1. Replace html lang attribute
    html = re.sub(r'<html lang="[^"]*"', f'<html lang="{lang}"', html)
    
    # 2. Add dir="rtl" for RTL languages
    if LANGUAGES[lang]['dir'] == 'rtl':
        html = html.replace(f'<html lang="{lang}"', f'<html lang="{lang}" dir="rtl"')
    
    # 3. Replace hreflang tags
    old_hreflang = re.findall(r'  <link rel="alternate" hreflang="[^"]*" href="[^"]*">', html)
    if old_hreflang:
        first = old_hreflang[0]
        last = old_hreflang[-1]
        new_tags = generate_hreflang_tags(page_path)
        html = html.replace(first, new_tags, 1)
        for tag in old_hreflang[1:]:
            html = html.replace(tag + '\n', '')
    
    # 4. Update canonical URL
    if page_path == 'index.html':
        html = html.replace(
            'href="https://goippro.com/"',
            f'href="https://goippro.com/{lang}/"'
        )
    
    # 5. Update OG URL
    if page_path == 'index.html':
        html = re.sub(
            r'<meta property="og:url" content="https://goippro.com/"',
            f'<meta property="og:url" content="https://goippro.com/{lang}/"',
            html
        )
    
    # 6. Apply text translations
    for en_text, translated_text in translations.items():
        html = html.replace(en_text, translated_text)
    
    # 7. Update language switcher: highlight current language
    html = html.replace(f'class="lang active" data-lang="en"', f'class="lang" data-lang="en"')
    html = html.replace(f'class="lang" data-lang="{lang}"', f'class="lang active" data-lang="{lang}"')
    
    # 8. Make language switcher links point to real URLs
    for l in LANGUAGES:
        if l == 'en':
            html = html.replace(f'data-lang="en">EN</button>', f'data-lang="en"><a href="/" style="color:inherit;text-decoration:none">EN</a></button>')
        else:
            html = html.replace(f'data-lang="{l}">{l.upper()}</button>', 
                               f'data-lang="{l}"><a href="/{l}/" style="color:inherit;text-decoration:none">{l.upper()}</a></button>')
    
    # 9. Add RTL CSS if needed
    if LANGUAGES[lang]['dir'] == 'rtl':
        rtl_css = '''
    /* RTL Support */
    body { direction: rtl; text-align: right; }
    .nav { flex-direction: row-reverse; }
    .hero-btns { flex-direction: row-reverse; }
    .seg-grid { direction: rtl; }
    .step-grid { direction: rtl; }
    .footer-links { direction: rtl; }
    .calc-results { direction: rtl; }
'''
        html = html.replace('</style>', rtl_css + '  </style>')
    
    return html

def build_all():
    """Build all translated pages"""
    for page in OUTPUT_PAGES:
        en_path = ROOT / page
        if not en_path.exists():
            print(f"  ✗ {page} not found")
            continue
        
        with open(en_path) as f:
            en_html = f.read()
        
        for lang, config in LANGUAGES.items():
            if lang == 'en':
                continue
            
            translations = load_translations(lang)
            if not translations:
                print(f"  ⊘ {lang}: no translations file, skipping")
                continue
            
            translated = build_translated_page(en_html, lang, translations, page)
            
            # Create output directory
            out_dir = ROOT / lang
            out_dir.mkdir(parents=True, exist_ok=True)
            
            out_path = out_dir / page
            with open(out_path, 'w') as f:
                f.write(translated)
            
            print(f"  ✓ {lang}/{page} ({len(translations)} translations applied)")

if __name__ == '__main__':
    build_all()
    print("\nDone!")

