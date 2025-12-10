#!/usr/bin/env python3
# Script to remove emojis from templates and replace with FontAwesome icons

import os
import re

# Define emoji to icon replacements
replacements = {
    '📧': '<i class="fas fa-envelope"></i>',
    '🎓': '<i class="fas fa-graduation-cap"></i>',
    '🛂': '<i class="fas fa-passport"></i>',
    '📍': '<i class="fas fa-map-marker-alt"></i>',
}

# Files to update
files = [
    'employee/templates/employee/contact_messages.html',
    'student_portal/templates/student_portal/service_form.html',
    'student_portal/templates/student_portal/document_services.html',
    'templates/global_agency/university_detail.html',
]

for file_path in files:
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Replace emojis with icons
        for emoji, icon in replacements.items():
            content = content.replace(emoji, icon)
        
        # Only write if changes were made
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✓ Updated {file_path}")
        else:
            print(f"- No changes needed in {file_path}")
    else:
        print(f"✗ File not found: {file_path}")

print("\nAll emojis have been replaced with professional icons!")
