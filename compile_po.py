#!/usr/bin/env python
"""
Compile .po files to .mo files using polib
"""
from pathlib import Path
import polib

if __name__ == '__main__':
    locale_dir = Path(__file__).parent / 'locale'
    
    print('Compiling .po files to .mo files using polib...')
    print('=' * 70)
    
    for po_file in sorted(locale_dir.rglob('django.po')):
        try:
            # Parse and save as .mo
            po = polib.pofile(str(po_file))
            mo_file = po_file.with_suffix('.mo')
            po.save_as_mofile(str(mo_file))
            print(f'✓ {po_file.parent.name:15s} -> {len(po):3d} messages compiled')
        except Exception as e:
            print(f'✗ Error in {po_file.parent.name}: {e}')
    
    print('=' * 70)
    print('Compilation complete!')
