#!/usr/bin/env python
"""Debug script to check language detection"""
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'globalagency_project.settings')
django.setup()

from django.test import RequestFactory
from django.utils.translation import get_language, activate
from django.conf import settings

# Test language activation
for lang_code in ['en', 'sw', 'ar', 'fr']:
    activate(lang_code)
    print(f'Activated {lang_code}: get_language() = {get_language()}')

print()
print('Django Settings:')
print(f'  LANGUAGE_CODE: {settings.LANGUAGE_CODE}')
print(f'  LANGUAGES: {settings.LANGUAGES}')
print(f'  USE_I18N: {settings.USE_I18N}')
print(f'  MIDDLEWARE: {settings.MIDDLEWARE}')
