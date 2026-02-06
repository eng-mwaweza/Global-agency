#!/usr/bin/env python3
"""
Comprehensive system improvements script
- Remove emojis from payment page
- Improve UI components (make them smaller and more elegant)
- Optimize styling across the system
"""

import os
import re

def remove_emoji_from_payment():
    """Remove emoji from payment page"""
    file_path = 'student_portal/templates/student_portal/payment.html'
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace the emoji with an icon
    content = content.replace(
        '<span style="font-size: 1.5rem;">⏳</span>',
        '<i class="fas fa-clock" style="color: #f59e0b;"></i>'
    )
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✓ Removed emoji from payment page")

def optimize_payment_page_ui():
    """Make payment page components smaller and more elegant"""
    file_path = 'student_portal/templates/student_portal/payment.html'
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Optimize container max-width
    content = content.replace(
        'max-width: 800px;',
        'max-width: 700px;'
    )
    
    # Reduce header padding
    content = content.replace(
        '.payment-header {\n            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);\n            color: white;\n            padding: 2rem;',
        '.payment-header {\n            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);\n            color: white;\n            padding: 1.5rem;'
    )
    
    # Reduce amount font size
    content = content.replace(
        '.payment-header .amount {\n            font-size: 3rem;',
        '.payment-header .amount {\n            font-size: 2.5rem;'
    )
    
    # Reduce body padding
    content = content.replace(
        '.payment-body {\n            padding: 2rem;',
        '.payment-body {\n            padding: 1.5rem;'
    )
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✓ Optimized payment page UI")

def optimize_form_styling():
    """Optimize application form styling"""
    file_path = 'templates/global_agency/start_application.html'
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Reduce container max-width
    content = content.replace(
        '.container { \n      max-width: 900px;',
        '.container { \n      max-width: 800px;'
    )
    
    # Reduce padding
    content = content.replace(
        'padding: 2.5rem;',
        'padding: 2rem;',
        1  # Only first occurrence
    )
    
    # Reduce h2 font size
    content = content.replace(
        'font-size: 2rem;',
        'font-size: 1.75rem;',
        1  # Only first occurrence in h2
    )
    
    # Reduce h3 font size
    content = content.replace(
        'font-size: 1.5rem;',
        'font-size: 1.25rem;'
    )
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✓ Optimized application form UI")

def add_fontawesome_to_payment():
    """Ensure FontAwesome is loaded in payment page"""
    file_path = 'student_portal/templates/student_portal/payment.html'
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if FontAwesome is already included
    if 'font-awesome' not in content.lower():
        # Add FontAwesome before </head>
        content = content.replace(
            '</head>',
            '    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">\n</head>'
        )
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✓ Added FontAwesome to payment page")
    else:
        print("- FontAwesome already included in payment page")

def main():
    print("Starting comprehensive system improvements...\n")
    
    try:
        add_fontawesome_to_payment()
        remove_emoji_from_payment()
        optimize_payment_page_ui()
        optimize_form_styling()
        
        print("\n✅ All improvements completed successfully!")
        print("\nChanges made:")
        print("1. Removed emoji from payment page")
        print("2. Optimized payment page layout (smaller, more elegant)")
        print("3. Optimized application form layout")
        print("4. Added FontAwesome icons")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        raise

if __name__ == "__main__":
    main()
