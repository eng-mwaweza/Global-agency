#!/usr/bin/env python3
# Script to update the courses section in hero.html

with open('templates/global_agency/includes/hero.html', 'r') as f:
    content = f.read()

# Find the start and end of the courses section
start_marker = "<!-- Top Courses Section -->"
end_marker = "</section>\n\n<style>"

start_idx = content.find(start_marker)
end_idx = content.find(end_marker, start_idx)

if start_idx != -1 and end_idx != -1:
    # Read the new courses section
    with open('templates/global_agency/includes/hero_courses_updated.html', 'r') as f:
        new_courses = f.read()
    
    # Replace the old section with the new one
    new_content = content[:start_idx] + new_courses + "\n\n<style>" + content[end_idx + len(end_marker):]
    
    # Write the updated content
    with open('templates/global_agency/includes/hero.html', 'w') as f:
        f.write(new_content)
    
    print("Successfully updated the courses section!")
else:
    print("Could not find the courses section markers")
    print(f"Start marker found: {start_idx != -1}")
    print(f"End marker found: {end_idx != -1}")
