#!/usr/bin/env python3
"""
Further UI Minimization Script
Reduces all components to create a smoother, more user-friendly interface
"""

import os
import re

def minimize_hero_section():
    """Further minimize hero section components"""
    hero_file = "templates/global_agency/includes/hero.html"

    with open(hero_file, 'r') as f:
        content = f.read()

    # Further reduce padding: py-12 sm:py-16 lg:py-20 → py-8 sm:py-12 lg:py-16
    content = re.sub(r'py-12 sm:py-16 lg:py-20', 'py-8 sm:py-12 lg:py-16', content)

    # Reduce heading sizes: text-3xl sm:text-4xl lg:text-5xl → text-2xl sm:text-3xl lg:text-4xl
    content = re.sub(r'text-3xl font-extrabold text-dark-text sm:text-4xl lg:text-5xl',
                     'text-2xl font-extrabold text-dark-text sm:text-3xl lg:text-4xl', content)

    # Reduce button padding: px-6 py-2.5 → px-5 py-2
    content = re.sub(r'px-6 py-2\.5', 'px-5 py-2', content)

    # Reduce stats padding: p-4 → p-3
    content = re.sub(r'p-4 bg-gray-100 rounded-lg shadow-inner', 'p-3 bg-gray-100 rounded-lg shadow-inner', content)

    # Reduce stats font size: text-3xl → text-2xl
    content = re.sub(r'text-3xl font-bold text-primary-blue', 'text-2xl font-bold text-primary-blue', content)

    with open(hero_file, 'w') as f:
        f.write(content)

    print("✅ Hero section further minimized")

def minimize_destinations_section():
    """Further minimize destinations section components"""
    dest_file = "templates/global_agency/includes/destinations.html"

    with open(dest_file, 'r') as f:
        content = f.read()

    # Further reduce section padding: py-12 sm:py-16 → py-8 sm:py-12
    content = re.sub(r'py-12 sm:py-16', 'py-8 sm:py-12', content)

    # Reduce main heading: text-2xl sm:text-3xl → text-xl sm:text-2xl
    content = re.sub(r'text-2xl font-extrabold text-dark-text sm:text-3xl',
                     'text-xl font-extrabold text-dark-text sm:text-2xl', content)

    # Reduce subheading: text-base → text-sm
    content = re.sub(r'text-base font-semibold text-accent-gold', 'text-sm font-semibold text-accent-gold', content)

    # Reduce description: text-lg → text-base
    content = re.sub(r'text-lg text-gray-600', 'text-base text-gray-600', content)

    # Further reduce card image height: h-40 → h-32
    content = re.sub(r'h-40 w-full object-cover', 'h-32 w-full object-cover', content)

    # Reduce card padding: p-6 → p-4
    content = re.sub(r'<div class="p-6">', '<div class="p-4">', content)

    # Reduce card title: text-2xl → text-xl
    content = re.sub(r'text-2xl font-bold text-primary-blue', 'text-xl font-bold text-primary-blue', content)

    # Reduce list item spacing: space-y-2 → space-y-1
    content = re.sub(r'space-y-2 text-sm text-gray-600', 'space-y-1 text-sm text-gray-600', content)

    # Reduce link margin: mt-4 → mt-3
    content = re.sub(r'mt-4 block text-center', 'mt-3 block text-center', content)

    with open(dest_file, 'w') as f:
        f.write(content)

    print("✅ Destinations section further minimized")

def minimize_footer():
    """Further minimize footer components"""
    footer_file = "templates/global_agency/includes/footer.html"

    with open(footer_file, 'r') as f:
        content = f.read()

    # Further reduce padding: py-8 → py-6
    content = re.sub(r'py-8', 'py-6', content)

    # Reduce heading sizes: text-base → text-sm
    content = re.sub(r'text-base mb-3', 'text-sm mb-3', content)

    # Reduce description text: text-sm → text-xs
    content = re.sub(r'text-sm mb-4 leading-relaxed', 'text-xs mb-4 leading-relaxed', content)

    # Reduce social icon sizes: text-lg → text-base
    content = re.sub(r'text-lg', 'text-base', content)

    # Reduce list spacing: space-y-2 → space-y-1
    content = re.sub(r'space-y-2 text-sm', 'space-y-1 text-sm', content)

    # Reduce check icon size: text-xs → text-xs (already small, but ensure consistency)
    content = re.sub(r'text-xs', 'text-xs', content)

    with open(footer_file, 'w') as f:
        f.write(content)

    print("✅ Footer further minimized")

def minimize_navigation():
    """Further minimize navigation components"""
    base_file = "templates/global_agency/base.html"

    with open(base_file, 'r') as f:
        content = f.read()

    # Further reduce nav height: h-14 → h-12
    content = re.sub(r'h-14', 'h-12', content)

    # Reduce logo size: text-xl → text-lg
    content = re.sub(r'text-xl', 'text-lg', content)

    with open(base_file, 'w') as f:
        f.write(content)

    print("✅ Navigation further minimized")

def minimize_start_application():
    """Further minimize start application form components"""
    app_file = "templates/global_agency/start_application.html"

    with open(app_file, 'r') as f:
        content = f.read()

    # Further reduce container max-width: 800px → 700px
    content = re.sub(r'max-width: 800px', 'max-width: 700px', content)

    # Reduce container margin: 2rem → 1.5rem
    content = re.sub(r'margin: 2rem auto', 'margin: 1.5rem auto', content)

    # Reduce container padding: 2rem → 1.5rem
    content = re.sub(r'padding: 2rem', 'padding: 1.5rem', content)

    # Reduce h2 font size: 1.75rem → 1.5rem
    content = re.sub(r'font-size: 1\.75rem', 'font-size: 1.5rem', content)

    # Reduce form subtitle: 1rem → 0.9rem
    content = re.sub(r'font-size: 1rem', 'font-size: 0.9rem', content)

    # Reduce h3 font size: 1.25rem → 1.1rem
    content = re.sub(r'font-size: 1\.25rem', 'font-size: 1.1rem', content)

    with open(app_file, 'w') as f:
        f.write(content)

    print("✅ Start application form further minimized")

def minimize_payment_page():
    """Further minimize payment page components"""
    payment_file = "student_portal/templates/student_portal/payment.html"

    with open(payment_file, 'r') as f:
        content = f.read()

    # Reduce body padding: padding: 20px → padding: 15px
    content = re.sub(r'padding: 20px', 'padding: 15px', content)

    # Reduce header padding: padding: 1rem 2rem → padding: 0.75rem 1.5rem
    content = re.sub(r'padding: 1rem 2rem', 'padding: 0.75rem 1.5rem', content)

    # Reduce header margin: margin-bottom: 2rem → margin-bottom: 1.5rem
    content = re.sub(r'margin-bottom: 2rem', 'margin-bottom: 1.5rem', content)

    # Reduce h1 font size: font-size: 1.5rem → font-size: 1.25rem
    content = re.sub(r'font-size: 1\.5rem', 'font-size: 1.25rem', content)

    with open(payment_file, 'w') as f:
        f.write(content)

    print("✅ Payment page further minimized")

def minimize_dashboard():
    """Further minimize dashboard components"""
    dashboard_file = "student_portal/templates/student_portal/dashboard.html"

    with open(dashboard_file, 'r') as f:
        content = f.read()

    # Reduce header padding: padding: 1rem 2rem → padding: 0.75rem 1.5rem
    content = re.sub(r'padding: 1rem 2rem', 'padding: 0.75rem 1.5rem', content)

    # Reduce h1 font size: font-size: 1.5rem → font-size: 1.25rem
    content = re.sub(r'font-size: 1\.5rem', 'font-size: 1.25rem', content)

    # Reduce nav menu padding: padding: 0.5rem 1rem → padding: 0.4rem 0.8rem
    content = re.sub(r'padding: 0\.5rem 1rem', 'padding: 0.4rem 0.8rem', content)

    with open(dashboard_file, 'w') as f:
        f.write(content)

    print("✅ Dashboard further minimized")

def main():
    """Main function to run all minimization tasks"""
    print("🚀 Starting further UI minimization...")

    try:
        minimize_hero_section()
        minimize_destinations_section()
        minimize_footer()
        minimize_navigation()
        minimize_start_application()
        minimize_payment_page()
        minimize_dashboard()

        print("\n🎉 All components successfully further minimized!")
        print("📋 Summary of changes:")
        print("   • Hero section: Reduced padding, headings, buttons, and stats")
        print("   • Destinations: Smaller images, padding, and text sizes")
        print("   • Footer: Compact layout with smaller elements")
        print("   • Navigation: Reduced height and logo size")
        print("   • Application form: Smaller container and elements")
        print("   • Payment page: Compact header and spacing")
        print("   • Dashboard: Reduced padding and sizes")
        print("\n✨ UI is now smoother and more user-friendly!")

    except Exception as e:
        print(f"❌ Error during minimization: {e}")

if __name__ == "__main__":
    main()