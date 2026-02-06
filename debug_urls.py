#!/usr/bin/env python
"""Debug script to inspect URL patterns"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'globalagency_project.settings')
sys.path.insert(0, '.')
django.setup()

from django.urls import get_resolver
from django.conf import settings

resolver = get_resolver()

def show_patterns(patterns, indent=0):
    """Recursively show URL patterns"""
    for idx, pattern in enumerate(patterns):
        prefix = '  ' * indent
        try:
            pattern_str = str(pattern.pattern)
            if hasattr(pattern, 'url_patterns'):
                # It's a nested URLconf
                print(f'{prefix}{idx}. [INCLUDE] {pattern_str}/')
                show_patterns(pattern.url_patterns, indent+1)
            else:
                name = getattr(pattern, 'name', '?')
                print(f'{prefix}{idx}. {pattern_str:40s} -> {name}')
        except Exception as e:
            print(f'{prefix}{idx}. Error: {e}')

print('URL Patterns Generated:')
print('=' * 80)
show_patterns(resolver.url_patterns)

print('\n' + '=' * 80)
print('LANGUAGES Configured:', settings.LANGUAGES)
print('LANGUAGE_CODE:', settings.LANGUAGE_CODE)
print('USE_I18N:', settings.USE_I18N)
