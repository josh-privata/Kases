#!/usr/bin/env python
"""
Command-line utility for administrative tasks.
"""

import os
import sys

if __name__ == "__main__":
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Kases.settings')
    os.environ.setdefault('DJANGO_CONFIGURATION', 'Dev')

    from configurations.management import execute_from_command_line
    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
