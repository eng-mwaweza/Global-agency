#!/usr/bin/env python
"""
Proper .mo file compiler from .po files using msgfmt-like approach
"""
import os
import struct
from pathlib import Path

def parse_po_file(po_file):
    """Parse a .po file and return messages dict"""
    messages = {}
    current_msgid = ""
    current_msgstr = ""
    in_msgid = False
    in_msgstr = False
    
    with open(po_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.rstrip('\n')
            
            if line.startswith('msgid "'):
                if current_msgid and current_msgstr:
                    if current_msgid:  # Don't include empty msgid
                        messages[current_msgid] = current_msgstr
                current_msgid = line[7:-1]  # Remove msgid " and trailing "
                current_msgstr = ""
                in_msgid = True
                in_msgstr = False
                
            elif line.startswith('msgstr "'):
                current_msgstr = line[8:-1]  # Remove msgstr " and trailing "
                in_msgid = False
                in_msgstr = True
                
            elif line.startswith('"') and (in_msgid or in_msgstr):
                # Continuation line
                text = line[1:-1]  # Remove quotes
                if in_msgstr:
                    current_msgstr += text
                else:
                    current_msgid += text
        
        # Add last message
        if current_msgid and current_msgstr:
            messages[current_msgid] = current_msgstr
    
    return messages

def write_mo_file(mo_file, messages):
    """Write .mo file in proper GNU gettext format"""
    if not messages:
        messages = {}
    
    # Build the message catalog
    keys = []
    values = []
    
    for msgid, msgstr in sorted(messages.items()):
        if msgid:  # Skip empty msgid
            keys.append(msgid.encode('utf-8'))
            values.append(msgstr.encode('utf-8'))
    
    if not keys:
        # Create empty .mo file
        with open(mo_file, 'wb') as f:
            f.write(b'')
        return
    
    # Write proper MO file format
    keyoffset = 7 * 4 + 16 * len(keys)
    valueoffset = keyoffset + sum(len(k) + 1 for k in keys)
    
    with open(mo_file, 'wb') as f:
        # Magic number (big-endian)
        f.write(struct.pack('>I', 0xde120495))
        # Version
        f.write(struct.pack('>I', 0))
        # Number of message pairs
        f.write(struct.pack('>I', len(keys)))
        # Offset of table with original strings
        f.write(struct.pack('>I', 7 * 4))
        # Offset of table with translated strings
        f.write(struct.pack('>I', 7 * 4 + 8 * len(keys)))
        # Size of hashing table
        f.write(struct.pack('>I', 0))
        # Offset of hashing table
        f.write(struct.pack('>I', 0))
        
        # Original strings table
        for key in keys:
            f.write(struct.pack('>I', len(key)))
            f.write(struct.pack('>I', keyoffset))
            keyoffset += len(key) + 1
        
        # Translated strings table
        for value in values:
            f.write(struct.pack('>I', len(value)))
            f.write(struct.pack('>I', valueoffset))
            valueoffset += len(value) + 1
        
        # Original strings
        for key in keys:
            f.write(key)
            f.write(b'\x00')
        
        # Translated strings
        for value in values:
            f.write(value)
            f.write(b'\x00')

if __name__ == '__main__':
    locale_dir = Path(__file__).parent / 'locale'
    
    print('Compiling .po files to .mo files...')
    print('=' * 70)
    
    compiled_count = 0
    for po_file in sorted(locale_dir.rglob('django.po')):
        try:
            messages = parse_po_file(po_file)
            mo_file = po_file.with_suffix('.mo')
            write_mo_file(mo_file, messages)
            print(f'✓ {po_file.parent.name:5s} -> {len(messages):3d} messages')
            compiled_count += 1
        except Exception as e:
            print(f'✗ Error: {po_file}: {e}')
    
    print('=' * 70)
    print(f'Successfully compiled {compiled_count} language files')
