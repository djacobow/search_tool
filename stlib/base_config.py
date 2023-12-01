#!/usr/bin/env python3

import os
import sys

pathname = os.path.dirname(sys.argv[0])        
sys.path.insert(0, os.path.abspath(pathname))

import stlib.commands.shell
import stlib.commands.grep
import stlib.commands.find
import stlib.commands.baa
import stlib.commands.pb_decode
import stlib.commands.paths
import stlib.commands.tstamp
import stlib.commands.repo
import stlib.shell

repoinfo = stlib.shell.repoinfo()

CONFIG = {
    'grep': {
        'match_color': {
            'fg': 'blue', 'bold': True
        },
        'repl_color': {
            'fg': 'yellow', 'bold': True
        },
        'file_color': {
            'fg': 'green'
        }
    },
    'editor': {
        'max_files': 60,
        'editors': {
            'vi':  ['vim','-o'],
            'vim': ['vim','-o'],
            'gvim': ['gvim','-p'],
            'emacs': ['emacs','-Q'],
        },
    },
    'code_file_types': {
        'c':     { 'default': True, },
        'h':     { 'default': True, },
        'cpp':   { 'default': True, },
        'proto': { 'default': True, },
        'py':    { 'default': False, 'grep_extra_glob': ['SConstruct'], },
        'sh':    { 'default': False, },
        'yaml':  { 'default': False, },
        'txt':   { 'default': False, },
        'mk':    { 'default': False, },
        'json':  { 'default': False, },
        'cmake': { 'default': False, 'grep_extra_glob': ['CMakeLists.txt'], },
    },
    'commands': {
        'f': {
            'description': 'find files in tree',
            'class': stlib.commands.find.Find
        },
        'g': {
            'description': 'find patterns in files in tree',
            'class': stlib.commands.grep.Grep
        },
        'gss': {
            'description': 'git submodule sync',
            'shellcommands': [
                'git submodule sync',
                'git submodule update --init --recursive'
            ],
            'class': stlib.commands.shell.Shell
        },
        'baa': {
            'description': '"bash add alias"; installs an alias to run script with \"st\"',
            'class': stlib.commands.baa.BashAddAlias
        },
        'p': {
            'description': 'Shortcut to get various useful paths.',
            'class': stlib.commands.paths.PathsFn
        },
        't': {
            'description': 'Convert numerical timestamps to human readable',
            'class': stlib.commands.tstamp.TSDecoder
        },
        'ri': {
            'description': 'Convert numerical timestamps to human readable',
            'class': stlib.commands.repo.Info
        }
    }
}

