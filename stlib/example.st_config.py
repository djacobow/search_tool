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
    'code_search_paths': {
        'iot-firmware': {
            'common': {
                'default': True,
                'include': ['mcufw/common'],
            },
            'gemini': {
                'default': True,
                'include': ['mcufw/gemini'],
            },
            'tag': {
                'default': True,
                'include': ['mcufw/tag'],
            },
            'ltetag': {
                'default': True,
                'include': ['mcufw/ltetag'],
            },
            'test': {
                'default': True,
                'include': ['mcufw/test',],
                'exclude': r'build/',
            },
            'iotp': {
                'default': True,
                'include': ['shared/protocols','ext/nanopb','shared/protocols'],
                'exclude': r'(?:conan-wrapper|examples|tests|tools)/',
            },
            'tools': {
                'default': True,
                'include': ['mcufw/tools', 'linuxfw/bluebell/tools','shared/tools'],
            },
            'projects': {
                'default': True,
                'include': ['mcufw/projects'],
                'exclude': r'Generated_Source/',
            },
            'generated': {
                'default': False,
                'include': ['mcufw/projects/creator/*/Generated_Source'],
            },
            'bl': {
                'default': True,
                'include': ['mcufw/bootloader/'],
            },
            'app': {
                'default': True,
                'include': ['linuxfw/bluebell/app'],
            },
            'lib': {
                'default': True,
                'include': ['linuxfw/bluebell/lib', 'linuxfw/bluebell/shared'],
            },
            'mod': {
                'default': False,
                'include': ['linuxfw/bluebell/mod'],
            },
            'ext': {
                'default': False,
                'include': ['ext', 'linuxfw/bluebell/ext'],
            },
            'scripts': {
                'default': True,
                'include': ['linuxfw/bluebell/scripts'],
            },
        },
    },
    'code_file_types': {
        'c':     { 'default': True, },
        'h':     { 'default': True, },
        'cpp':   { 'default': True, },
        'proto': { 'default': True, },
        'py':    { 'default': False, 'grep_extra_glob': ['SConstruct'], },
        'sh':    { 'default': False, },
        'txt':   { 'default': False, },
        'sh':    { 'default': False, },
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
        'pf': {
            'description': 'preflight commit: build all targets and run base tests',
            'shellcommands': [
                ''.join([
                    os.path.relpath(os.path.join(repoinfo['root'],'mcufw/tools/piperunner.py'),os.getcwd()),
                    ' -c ',
                    os.path.relpath(os.path.join(repoinfo['root'],'mcufw/pipework.json')),
                    ' -r preflight'
                ]),
            ],
            'class': stlib.commands.shell.Shell
        },
        'baa': {
            'description': '"bash add alias"; installs an alias to run script with \"st\"',
            'class': stlib.commands.baa.BashAddAlias
        },
        'pb': {
            'description': 'decode a protobuf',
            'searchpaths': [
                os.path.join(repoinfo['root'],'shared/protocols/protobuf'),
                os.path.join(repoinfo['root'],'shared/protocols/psoc-camera/pb'),
                os.path.join(repoinfo['root'],'mcufw/ltetag/protos'),
                os.path.join(repoinfo['root'],'ext/nanopb-release/nanopb-0.4.2-linux-x86/generator/proto'),
            ],
            'protofiles': [
                os.path.join(repoinfo['root'],'shared/protocols/psoc-camera/pb/cmt_messages.proto'),
                os.path.join(repoinfo['root'],'mcufw/ltetag/protos/ltetag.proto'),
             ],
            'class': stlib.commands.pb_decode.ProtobufDecode
        },
        'p': {
            'description': 'Shortcut to get various useful paths.',
            'class': stlib.commands.paths.PathsFn
        },
        'hs': {
            'description': 'Show the HIL status',
            'shellcommands': [
                os.path.join(repoinfo['root'],'mcufw/tools/hil-status.py'),
            ],
            'class': stlib.commands.shell.Shell
        },
    }
}

