#!/usr/bin/env python
"""Test translation content in different languages"""
import requests
import re

languages = {
    'en': 'Home',
    'sw': 'Nyumbani',
    'ar': 'الرئيسية',
    'fr': 'Accueil',
}

print('Testing Translations Across All Languages')
print('=' * 70)

for lang, expected_word in languages.items():
    try:
        r = requests.get(f'http://localhost:8000/{lang}/', timeout=5)
        
        # Check for expected translation
        if expected_word in r.text:
            print(f'✓ {lang}: Found "{expected_word}" - TRANSLATED')
        elif lang == 'en':
            # English might have lowercase
            if 'home' in r.text.lower():
                print(f'✓ {lang}: Found translation (case variant)')
        else:
            print(f'✗ {lang}: Translation NOT found')
            # Try to find what navigation text is present
            nav_matches = re.findall(r'class="[^"]*lang-option[^"]*"[^>]*>.*?<span[^>]*>([^<]+)</span>', r.text)
            if nav_matches:
                print(f'  Available langs in navbar: {nav_matches[:4]}')
    
    except Exception as e:
        print(f'✗ {lang}: Connection error')

print('=' * 70)
