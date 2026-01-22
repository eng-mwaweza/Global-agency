#!/usr/bin/env python
# Script to compile .po files to .mo files manually
import os
import struct
import array

def generate_mo_file(po_file, mo_file):
    """
    Generate .mo file from .po file content
    This is a simple implementation for development purposes
    """
    messages = {}
    current_msgid = None
    
    with open(po_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line.startswith('msgid "'):
                current_msgid = line[7:-1]  # Remove 'msgid "' and '"'
            elif line.startswith('msgstr "') and current_msgid:
                msgstr = line[8:-1]  # Remove 'msgstr "' and '"'
                if current_msgid and current_msgid != '':
                    messages[current_msgid] = msgstr
                current_msgid = None
    
    # Write a simple .mo file format
    # This is a minimal implementation - for production, use GNU gettext tools
    write_mo_file(mo_file, messages)

def write_mo_file(mo_file, messages):
    """Write messages to .mo file in binary format"""
    # Simplified .mo file format
    offsets = []
    ids = b''
    strs = b''
    
    for msgid in sorted(messages.keys()):
        msgstr = messages[msgid]
        
        msgid_bytes = msgid.encode('utf-8')
        msgstr_bytes = msgstr.encode('utf-8')
        
        offsets.append((len(ids), len(msgid_bytes), len(strs), len(msgstr_bytes)))
        ids += msgid_bytes + b'\x00'
        strs += msgstr_bytes + b'\x00'
    
    # Write MO file
    with open(mo_file, 'wb') as f:
        # MO file magic number and version
        f.write(struct.pack('Iiiiiii',
                           0x950412de,  # Magic
                           0,           # Version
                           len(offsets),  # Number of messages
                           7 * 4 + 16,  # Offset of table with original strings
                           7 * 4 + 16 + len(offsets) * 8,  # Offset of table with translated strings
                           0,           # Hash table size
                           0))          # Offset of hash table
        
        for off in offsets:
            f.write(struct.pack('ii', off[1], off[0]))
        
        for off in offsets:
            f.write(struct.pack('ii', off[3], off[2]))
        
        f.write(ids)
        f.write(strs)

if __name__ == '__main__':
    base_path = 'c:\\Users\\WINDOWS 11\\Documents\\Projects\\Global-agency\\locale'
    languages = ['en', 'sw', 'ar', 'fr']
    
    for lang in languages:
        po_file = os.path.join(base_path, lang, 'LC_MESSAGES', 'django.po')
        mo_file = os.path.join(base_path, lang, 'LC_MESSAGES', 'django.mo')
        
        if os.path.exists(po_file):
            print(f"Compiling {lang}...")
            generate_mo_file(po_file, mo_file)
            print(f"Created {mo_file}")
        else:
            print(f"Warning: {po_file} not found")
