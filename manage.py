#!/usr/bin/env python
import os
import sys
from path import path

if __name__ == "__main__":
    sys.path.append(path(__file__).dirname() / 'src')
    sys.path.append(path(__file__).dirname() / 'lib')

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
