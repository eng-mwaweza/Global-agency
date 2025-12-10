#!/usr/bin/env python3
"""
Aggressive Homepage UI Minimization Script
Further reduces all homepage components for maximum smoothness and user-friendliness
"""

import os
import re

def aggressively_minimize_hero_section():
    """Aggressively minimize hero section for maximum compactness"""
    hero_file = "templates/global_agency/includes/hero.html"

    with open(hero_file, 'r') as f:
        content = f.read()

    # Further reduce padding: py-4 sm:py-8 lg:py-12 → py-2 sm:py-4 lg:py-6
    content = re.sub(r'py-4 sm:py-8 lg:py-12', 'py-2 sm:py-4 lg:py-6', content)

    # Reduce subheading: text-sm → text-xs
    content = re.sub(r'text-sm font-semibold text-accent-gold', 'text-xs font-semibold text-accent-gold', content)

    # Further reduce heading: text-xl sm:text-2xl lg:text-3xl → text-lg sm:text-xl lg:text-2xl
    content = re.sub(r'text-xl font-extrabold text-dark-text sm:text-2xl lg:text-3xl',
                     'text-lg font-extrabold text-dark-text sm:text-xl lg:text-2xl', content)

    # Reduce description: text-sm → text-xs
    content = re.sub(r'text-sm text-gray-600', 'text-xs text-gray-600', content)

    # Reduce button margin: mt-8 → mt-6
    content = re.sub(r'mt-8 flex flex-col', 'mt-6 flex flex-col', content)

    # Further reduce button padding: px-4 py-1.5 → px-3 py-1
    content = re.sub(r'px-4 py-1\.5', 'px-3 py-1', content)

    # Reduce button text: text-sm → text-xs
    content = re.sub(r'text-sm font-medium', 'text-xs font-medium', content)

    # Reduce hero image margin: mt-12 → mt-8
    content = re.sub(r'mt-12 lg:mt-0', 'mt-8 lg:mt-0', content)

    # Reduce stats section margin: mt-12 → mt-8
    content = re.sub(r'mt-12 border-t', 'mt-8 border-t', content)

    # Reduce stats padding: pt-6 → pt-4
    content = re.sub(r'pt-6 grid grid-cols-2', 'pt-4 grid grid-cols-2', content)

    # Reduce stats gap: gap-4 → gap-3
    content = re.sub(r'gap-4 text-center', 'gap-3 text-center', content)

    # Further reduce stats padding: p-2 → p-1.5
    content = re.sub(r'p-2 bg-gray-100', 'p-1.5 bg-gray-100', content)

    # Reduce stats font: text-xl → text-lg
    content = re.sub(r'text-xl font-bold text-primary-blue', 'text-lg font-bold text-primary-blue', content)

    # Reduce stats text: text-xs → text-xs (keep small)
    content = re.sub(r'text-xs text-gray-600', 'text-xs text-gray-600', content)

    with open(hero_file, 'w') as f:
        f.write(content)

    print("✅ Hero section aggressively minimized")

def aggressively_minimize_destinations_section():
    """Aggressively minimize destinations section for smoother layout"""
    dest_file = "templates/global_agency/includes/destinations.html"

    with open(dest_file, 'r') as f:
        content = f.read()

    # Further reduce section padding: py-8 sm:py-12 → py-4 sm:py-6
    content = re.sub(r'py-8 sm:py-12', 'py-4 sm:py-6', content)

    # Reduce subheading: text-sm → text-xs
    content = re.sub(r'text-sm font-semibold text-accent-gold', 'text-xs font-semibold text-accent-gold', content)

    # Further reduce main heading: text-xl sm:text-2xl → text-lg sm:text-xl
    content = re.sub(r'text-xl font-extrabold text-dark-text sm:text-2xl',
                     'text-lg font-extrabold text-dark-text sm:text-xl', content)

    # Reduce description: text-base → text-sm
    content = re.sub(r'text-base text-gray-600', 'text-sm text-gray-600', content)

    # Reduce description margin: mt-4 → mt-3
    content = re.sub(r'mt-4 text-base text-gray-600', 'mt-3 text-sm text-gray-600', content)

    # Reduce grid margin: mt-16 → mt-12
    content = re.sub(r'mt-16 grid grid-cols-1', 'mt-12 grid grid-cols-1', content)

    # Reduce grid gap: gap-8 → gap-6
    content = re.sub(r'gap-8', 'gap-6', content)

    # Further reduce card image height: h-32 → h-28
    content = re.sub(r'h-32 w-full object-cover', 'h-28 w-full object-cover', content)

    # Further reduce card padding: p-4 → p-3
    content = re.sub(r'<div class="p-4">', '<div class="p-3">', content)

    # Further reduce card title: text-xl → text-lg
    content = re.sub(r'text-xl font-bold text-primary-blue', 'text-lg font-bold text-primary-blue', content)

    # Reduce list margin: mt-3 → mt-2
    content = re.sub(r'mt-3 space-y-1', 'mt-2 space-y-1', content)

    # Further reduce link margin: mt-3 → mt-2
    content = re.sub(r'mt-3 block text-center', 'mt-2 block text-center', content)

    with open(dest_file, 'w') as f:
        f.write(content)

    print("✅ Destinations section aggressively minimized")

def aggressively_minimize_footer():
    """Aggressively minimize footer for minimal footprint"""
    footer_file = "templates/global_agency/includes/footer.html"

    with open(footer_file, 'r') as f:
        content = f.read()

    # Further reduce padding: py-6 → py-4
    content = re.sub(r'py-6', 'py-4', content)

    # Reduce grid margin: mb-8 → mb-6
    content = re.sub(r'mb-8', 'mb-6', content)

    # Reduce grid gap: gap-8 → gap-6
    content = re.sub(r'gap-8 mb-8', 'gap-6 mb-6', content)

    # Further reduce headings: text-sm → text-xs
    content = re.sub(r'text-sm mb-3', 'text-xs mb-3', content)

    # Further reduce description: text-xs → text-xs (keep small)
    content = re.sub(r'text-xs mb-4', 'text-xs mb-3', content)

    # Reduce social icon spacing: space-x-4 → space-x-3
    content = re.sub(r'space-x-4', 'space-x-3', content)

    # Further reduce social icons: text-base → text-sm
    content = re.sub(r'text-base', 'text-sm', content)

    # Further reduce list spacing: space-y-1 → space-y-0.5
    content = re.sub(r'space-y-1 text-sm', 'space-y-0.5 text-xs', content)

    # Reduce check icon size: text-xs → text-xs (keep small)
    content = re.sub(r'text-xs', 'text-xs', content)

    with open(footer_file, 'w') as f:
        f.write(content)

    print("✅ Footer aggressively minimized")

def aggressively_minimize_navigation():
    """Aggressively minimize navigation for sleek appearance"""
    base_file = "templates/global_agency/base.html"

    with open(base_file, 'r') as f:
        content = f.read()

    # Further reduce nav height: h-12 → h-10
    content = re.sub(r'h-12', 'h-10', content)

    # Further reduce logo size: text-lg → text-base
    content = re.sub(r'text-lg', 'text-base', content)

    with open(base_file, 'w') as f:
        f.write(content)

    print("✅ Navigation aggressively minimized")

def aggressively_minimize_start_application():
    """Aggressively minimize start application form"""
    app_file = "templates/global_agency/start_application.html"

    with open(app_file, 'r') as f:
        content = f.read()

    # Further reduce container max-width: 700px → 650px
    content = re.sub(r'max-width: 700px', 'max-width: 650px', content)

    # Further reduce container margin: 1.5rem → 1rem
    content = re.sub(r'margin: 1.5rem auto', 'margin: 1rem auto', content)

    # Further reduce container padding: 1.5rem → 1.25rem
    content = re.sub(r'padding: 1.5rem', 'padding: 1.25rem', content)

    # Further reduce h2 font size: 1.5rem → 1.25rem
    content = re.sub(r'font-size: 1\.5rem', 'font-size: 1.25rem', content)

    # Further reduce form subtitle: 0.9rem → 0.8rem
    content = re.sub(r'font-size: 0\.9rem', 'font-size: 0.8rem', content)

    # Further reduce h3 font size: 1.1rem → 1rem
    content = re.sub(r'font-size: 1\.1rem', 'font-size: 1rem', content)

    with open(app_file, 'w') as f:
        f.write(content)

    print("✅ Start application form aggressively minimized")

def main():
    """Main function to run all aggressive minimization tasks"""
    print("🚀 Starting aggressive homepage UI minimization...")

    try:
        aggressively_minimize_hero_section()
        aggressively_minimize_destinations_section()
        aggressively_minimize_footer()
        aggressively_minimize_navigation()
        aggressively_minimize_start_application()

        print("\n🎉 All homepage components aggressively minimized!")
        print("📋 Summary of aggressive changes:")
        print("   • Hero section: Ultra-compact padding, tiny headings, micro buttons")
        print("   • Destinations: Minimal spacing, small images, tight card layouts")
        print("   • Footer: Micro padding, tiny text, compact social icons")
        print("   • Navigation: Sleek height, small logo")
        print("   • Application form: Tiny container, minimal margins")
        print("\n✨ Homepage is now ultra-smooth and maximally user-friendly!")

    except Exception as e:
        print(f"❌ Error during aggressive minimization: {e}")

if __name__ == "__main__":
    main()