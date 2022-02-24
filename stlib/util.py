import sys, os, glob, re

from . import shell

def die(msg):
    print('-Error- {}'.format(msg))
    sys.exit(-1)

def getSpecifierList(config, repo):
    usage = []

    def makeName(t, config):
        is_default = isinstance(config,dict) and config.get('default',False)
        asterisk = '(*)' if is_default else ''
        return f'-{t}{asterisk}'

    categories = {
        'type': config['code_file_types'],
        'path': config['code_search_paths'][repo],
        'editor':config['editor']['editors']
    }
    for group in categories:
        c = categories[group]
        names = ', '.join(sorted([ makeName(t,c[t]) for t in c ]))
        usage.append(f'{group:6} specifiers: {names}')

    return usage

def fileGlob(paths, types, fpats = None):
    found = []
    for p in paths:
        for t in types:
            if fpats is None:
                globstr = '{}/**/*.{}'.format(p['include'],t['suffix'])
                new = glob.glob(globstr,recursive=True)
                if p.get('exclude') is not None:
                    new = filter(lambda x: not re.search(p['exclude'],x), new)
                found += new

                if len(t['grep_extra_glob']):
                    for extra in t['grep_extra_glob']:
                        globstr = r'{}/**/{}'.format(p['include'],extra)
                        new = glob.glob(globstr, recursive=True)
                        if p.get('exclude') is not None:
                            new = filter(lambda x: not re.search(p['exclude'],x), new)
                        found += new

            else:
                for fpat in fpats:
                    globstr = '{}/**/*{}*.{}'.format(p['include'],fpat,t['suffix'])
                    new = glob.glob(globstr,recursive=True)
                    if p.get('exclude') is not None:
                        new = filter(lambda x: not re.search(p['exclude'],x), new)
                    found += new

    foundhash = { x:1 for x in found }
    return list(foundhash.keys())

             
def makeTypeList(config, adict):
    ftypes = []
    for n in config['code_file_types']:
        if n in adict:
           ftypes.append(n)
    if not len(ftypes):
        ftypes = list(filter(lambda x: config['code_file_types'][x]['default'], config['code_file_types']))

    return [ {'suffix':n, 'grep_extra_glob':config['code_file_types'][n].get('grep_extra_glob',[])} for n in ftypes ]


def makeSearchPathList(config, adict):
    pnames = []
    repo = adict['repoinfo']['name']
    if repo is None:
        die('need to be inside a github repo')
    if repo not in config['code_search_paths']:
        die('Repo {} is not in config file.'.format(repo))

    possibles = list(config['code_search_paths'][repo].keys())
    for n in possibles:
        if n in adict:
            pnames.append(n)

    if not len(pnames):
        pnames = list(filter(lambda x: config['code_search_paths'][repo][x]['default'], possibles));
    
    root = adict['repoinfo']['root']
    paths = []
    for x in pnames:
        for y in config['code_search_paths'][repo][x].get('include'):
            npath = os.path.join(root,y)
            paths.append({ 'include': npath, 'exclude': config['code_search_paths'][repo][x].get('exclude') })
    return paths


def editFiles(config, adict, found):
    count_ok = len(found) and len(found) < config['editor']['max_files']
    edit_req = None 
    for en in config['editor']['editors']:
        if en in adict:
            edit_req = en 
            break

    if edit_req:
        if count_ok:
            shell.shellDetach(config['editor']['editors'][edit_req] + found)
        else:
            print("\n{} is too many files to edit".format(len(found)))
