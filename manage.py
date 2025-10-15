#!/usr/bin/env python
import os, sys
def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'globalagency_project.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError:
        raise ImportError('Django not installed')
    execute_from_command_line(sys.argv)
if __name__=='__main__':
    main()
