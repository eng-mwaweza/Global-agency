"""
Test script to verify improved translations are working
"""
import os
import django
import sys

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'globalagency_project.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
django.setup()

from django.test import Client
from django.conf import settings

def test_translation(lang_code, test_strings):
    """Test if specific strings appear in the translated page"""
    client = Client()
    url = f'/{lang_code}/'
    
    print(f"\n{'='*60}")
    print(f"Testing {lang_code.upper()} - URL: {url}")
    print('='*60)
    
    response = client.get(url)
    content = response.content.decode('utf-8')
    
    print(f"Status Code: {response.status_code}")
    
    found_count = 0
    not_found = []
    
    for test_string in test_strings:
        if test_string in content:
            print(f"  ✓ FOUND: {test_string[:50]}...")
            found_count += 1
        else:
            print(f"  ✗ NOT FOUND: {test_string[:50]}...")
            not_found.append(test_string)
    
    print(f"\nResult: {found_count}/{len(test_strings)} strings found")
    
    if not_found:
        print("\nMissing strings:")
        for s in not_found:
            print(f"  - {s}")
    
    return found_count == len(test_strings)

def main():
    print("\n" + "="*60)
    print("TESTING IMPROVED TRANSLATIONS")
    print("="*60)
    
    # Test English (base language)
    english_strings = [
        "Who We Are",
        "Our Mission",
        "Our Vision",
        "Integrity",
        "Innovation",
        "Excellence",
        "Customer Focus",
        "Accountability",
        "Teamwork"
    ]
    
    # Test Swahili - IMPROVED translations
    swahili_strings = [
        "Kuhusu Sisi",  # Changed from "Nani Tunavyo Kuwa"
        "Dhamira Yetu",  # Changed from "Lengo Letu"
        "Dira Yetu",  # Changed from "Macho Yetu"
        "Uadilifu",
        "Ubunifu",
        "Ubora",
        "Kuzingatia Wateja",  # Changed from "Mkazo wa Mteja"
        "Uwajibikaji",  # Changed from "Wajibu"
        "Ushirikiano"  # Changed from "Kazi ya Timu"
    ]
    
    # Test Arabic
    arabic_strings = [
        "من نحن",
        "مهمتنا",
        "رؤيتنا",
        "النزاهة",
        "الابتكار",
        "التميز"
    ]
    
    # Test French
    french_strings = [
        "Qui nous sommes",
        "Notre Mission",
        "Notre Vision",
        "Intégrité",
        "Innovation",
        "Excellence",
        "Orientation client",
        "Responsabilité",
        "Travail d'équipe"
    ]
    
    results = {}
    
    results['en'] = test_translation('en', english_strings)
    results['sw'] = test_translation('sw', swahili_strings)
    results['ar'] = test_translation('ar', arabic_strings)
    results['fr'] = test_translation('fr', french_strings)
    
    # Summary
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    
    for lang, success in results.items():
        status = "✓ PASS" if success else "✗ FAIL"
        print(f"{lang.upper()}: {status}")
    
    all_passed = all(results.values())
    
    if all_passed:
        print("\n🎉 All translations are working correctly with improved accuracy!")
    else:
        print("\n⚠ Some translations need attention")
    
    print("\n" + "="*60)
    
    # Show key improvements
    print("\nKEY IMPROVEMENTS IN SWAHILI:")
    print("  • 'Who We Are': 'Nani Tunavyo Kuwa' → 'Kuhusu Sisi' (more natural)")
    print("  • 'Our Mission': 'Lengo Letu' → 'Dhamira Yetu' (more accurate)")
    print("  • 'Our Vision': 'Macho Yetu' → 'Dira Yetu' (proper translation)")
    print("  • 'Customer Focus': 'Mkazo wa Mteja' → 'Kuzingatia Wateja' (better phrasing)")
    print("  • 'Accountability': 'Wajibu' → 'Uwajibikaji' (more precise)")
    print("  • 'Teamwork': 'Kazi ya Timu' → 'Ushirikiano' (proper term)")
    print("="*60)

if __name__ == "__main__":
    main()
