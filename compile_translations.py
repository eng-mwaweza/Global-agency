#!/usr/bin/env python
"""
Script to properly compile .po files to .mo files
Uses the standard Python gettext module to ensure compatibility
"""
import os
import sys
import struct
import array
from pathlib import Path

def generate_mo_from_po(po_file, mo_file):
    """
    Compile a .po file to a .mo file using gettext format
    """
    messages = {}
    metadata = {}
    current_msgid = None
    current_msgstr = None
    
    with open(po_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.rstrip('\n')
            
            # Parse msgid lines
            if line.startswith('msgid "'):
                if current_msgid is not None and current_msgstr is not None:
                    if current_msgid:
                        messages[current_msgid] = current_msgstr
                    else:
                        metadata = parse_metadata(current_msgstr)
                
                current_msgid = line[7:-1]  # Extract string between quotes
                current_msgstr = None
            
            # Parse msgstr lines
            elif line.startswith('msgstr "'):
                current_msgstr = line[8:-1]  # Extract string between quotes
            
            # Handle multi-line strings
            elif line.startswith('"') and line.endswith('"'):
                text = line[1:-1]
                if current_msgstr is not None:
                    current_msgstr += text
                elif current_msgid is not None:
                    current_msgid += text
        
        # Don't forget the last message
        if current_msgid is not None and current_msgstr is not None:
            if current_msgid:
                messages[current_msgid] = current_msgstr
    
    # Write .mo file
    write_mo_file(mo_file, messages)
    print(f'✓ Compiled {po_file} -> {mo_file} ({len(messages)} messages)')

def write_mo_file(mo_file, messages):
    """
    Write messages dict to a .mo file in GNU gettext format
    """
    # Sort messages by key
    sorted_messages = sorted(messages.items())
    
    # Generate offsets
    keys = []
    values = []
    offsets = []
    
    for msgid, msgstr in sorted_messages:
        msgid_bytes = msgid.encode('utf-8')
        msgstr_bytes = msgstr.encode('utf-8')
        
        offsets.append((len(keys), len(msgid_bytes), len(values), len(msgstr_bytes)))
        keys.append(msgid_bytes)
        values.append(msgstr_bytes)
    
    # Write .mo file header
    with open(mo_file, 'wb') as f:
        # Magic number
        f.write(struct.pack('I', 0xde120495))
        # Version
        f.write(struct.pack('I', 0))
        # Number of strings
        f.write(struct.pack('I', len(offsets)))
        # Offset of table with original strings
        f.write(struct.pack('I', 7 * 4))
        # Offset of table with translated strings
        f.write(struct.pack('I', 7 * 4 + len(offsets) * 8))
        # Size of hashing table
        f.write(struct.pack('I', 0))
        # Offset of hashing table
        f.write(struct.pack('I', 0))
        
        # Write original string offsets
        keyoffset = 7 * 4 + len(offsets) * 8 * 2
        for msgid_offset, msgid_len, _, _ in offsets:
            f.write(struct.pack('II', msgid_len, keyoffset))
            keyoffset += msgid_len + 1
        
        # Write translated string offsets
        valueoffset = keyoffset
        for _, _, msgstr_offset, msgstr_len in offsets:
            f.write(struct.pack('II', msgstr_len, valueoffset))
            valueoffset += msgstr_len + 1
        
        # Write original strings
        for key in keys:
            f.write(key)
            f.write(b'\x00')
        
        # Write translated strings
        for value in values:
            f.write(value)
            f.write(b'\x00')

def parse_metadata(metadata_str):
    """Parse metadata from msgstr"""
    metadata = {}
    for line in metadata_str.split('\\n'):
        if ':' in line:
            key, value = line.split(':', 1)
            metadata[key.strip()] = value.strip()
    return metadata

if __name__ == '__main__':
    base_dir = Path(__file__).parent
    locale_dir = base_dir / 'locale'
    
    print('Compiling translation files...')
    print('=' * 70)
    
    # Find all .po files and compile them
    for po_file in locale_dir.rglob('django.po'):
        mo_file = po_file.with_suffix('.mo')
        try:
            generate_mo_from_po(str(po_file), str(mo_file))
        except Exception as e:
            print(f'✗ Error compiling {po_file}: {e}')
    
    print('=' * 70)
    print('Translation compilation complete!')
