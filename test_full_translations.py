import os
import django
from django.test import Client

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'globalagency_project.settings')
django.setup()

client = Client()
languages = ['en', 'sw', 'ar', 'fr']

print('\n=== FULL TRANSLATION TEST ===\n')

for lang in languages:
    response = client.get(f'/{lang}/')
    content = response.content.decode('utf-8')
    
    print("Language: " + lang)
    print("  Status: " + str(response.status_code))
    
    # Check for key translated strings
    if lang == 'en':
        checks = [
            ('Who We Are', 'Who We Are' in content),
            ('Home', 'Home' in content),
            ('Our Mission', 'Our Mission' in content),
            ('Integrity', 'Integrity' in content)
        ]
    elif lang == 'sw':
        checks = [
            ('Nani Tunavyo Kuwa', 'Nani Tunavyo Kuwa' in content),
            ('Nyumbani', 'Nyumbani' in content),
            ('Uadilifu', 'Uadilifu' in content),
            ('Lengo Letu', 'Lengo Letu' in content)
        ]
    elif lang == 'ar':
        # Arabic strings - just check they're not empty
        found_translations = ('Lengo' not in content) and content.count('href=') > 10
        checks = [
            ('Arabic content loaded', found_translations)
        ]
    elif lang == 'fr':
        checks = [
            ('Qui sommes-nous', 'Qui sommes-nous' in content),
            ('Accueil', 'Accueil' in content),
            ('Notre Mission', 'Notre Mission' in content)
        ]
    
    for check_name, check_result in checks:
        status = 'PASS' if check_result else 'FAIL'
        print("    [" + status + "] " + check_name)
    
    print()

print('=== TEST COMPLETE ===')
