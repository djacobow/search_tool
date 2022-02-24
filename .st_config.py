#!/usr/bin/env python3

import os
import sys

pathname = os.path.dirname(sys.argv[0])        
sys.path.insert(0, os.path.abspath(pathname))

import stlib.commands.shell
import stlib.shell

repoinfo = stlib.shell.repoinfo()

CONFIG = {
    'subpaths': {
        'l':   ( 'stlib',          ['stlib']),
        'c':   ( 'commands',       ['stlib','commands']),
    },
    'code_file_types': {
        'py':    { 'default': True,  },
    },
    'code_search_paths': {
        'st': {
            'top': {
                'default': True,
                'include': ['.'],
                'exclude': r'stlib',
            },
            'stlib': {
                'default': True,
                'include': ['stlib'],
            },
        },
    },
}
