# search_tool

Command-line code search and manipulation tools for git projects

## motivation

For those of that prefer not to use IDEs, or at least want to be able
to quickly navigate a large codebase, it's nice to have some command-
line tools that make it easy to find files around your repo.

This tool, which I call `st` for "search tool" is sort of a Swiss
army knife for navigating your repo. It makes it easy to find files
by name and to search within your repo by string.

Of coure, this can be done with existing unix tools like find
and grep and `st` is really nothing more than sugar around those,
cutting down the keystrokes required, because you can configure it
to understand the layout of your repo.

## configuration

`st` builds up its configurations from three places, in order:

    1. it has some pre-baked config settings in this repo itself
    2. it will load an `.st_config.py` from the root of your repo
    3. it will load an `.st_config.py` from your home directory.

Each of these files are `exec`d, so you should only put safe things
in them. The loaders works with the top two levels of keys in
the contained dicts, so that each file can add to what was left
from the previous, or override it, up to the second level key.
This lets you add paths and commands without removing existing
ones.

### config examples

For a simple repo, you pretty much just want to specify folder
you want to be searchable with simple `-` flags, and which
of those you want to be searched by default.

For example:

This file, taken from a DS1000z controller project, incldues
four code search paths. They are all enabled by default, and
so could really have been specified as just one, since searches
are always recursive. However, the exclude sections provide
patterns to exclude certain files.

Using this scheme you can easily set up your paths to exclude
searches of directories of machine generated code, or various
other areas that you generally do not want to see, but can
still turn them on when need be.


```python3
CONFIG = {
    'subpaths': {
        'l':   ( 'dslib',          ['dslib']),
        'ps':  ( 'personaliities', ['dslib','personalities']),
        'd1':  ( 'ds1k',           ['dslib','personalities','ds1k']),
        'd2':  ( 'ds2k',           ['dslib','personalities','ds2k']),
    },  
    'code_file_types': {
        'py':    { 'default': True,  },
    },  
    'code_search_paths': {
        'ds1000_ds2000_cmdline': {
            'top': {
                'default': True,
                'include': ['.'],
                'exclude': r'dslib',
            },
            'dslib': {
                'default': True,
                'include': ['dslib'],
                'exclude': r'personalities',
            },  
            'ds1k': {
                'default': True,
                'include': ['dslib/personalities/ds1k'],
            },  
            'ds2k': {
                'default': True,
                'include': ['dslib/personalities/ds2k'],
            },  
        },  
    },  
    'commands': {
    }
}   
```

The file `stlib/base_config.py` in this repo provides a much more
complex example showing how commands are added and called.

## use

### finding files

Find all files that have "uart" in their name:

```bash
st f uart
```

Find only python files matching "uart":

```bash
st f uart -py
```

Find only python files matching UART in the "dslib" directory group:

```bash
st f uart -dslib -py
```

If you know you want to edit the file, you can add `-vi` or `-emacs` to you command
and all matching files will be opened in those programs.


### finding text


`st g` works similarly, but on the contents of the files. The search
paths will follow the same fules.

```bash
st g color
```

will find and show all the spots where the text color appears in your files.
There are a lot of other options, to show context, to limit searches, etc.

You can even use `st g` to find and replace text strings in your entire repo.

