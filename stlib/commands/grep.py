import re, os

from .. import util
from ..xterm_colors import colorize
    
class Grep:
    def __init__(self, config):
        self.config = config

    def colorize_regex(self, pattern,line,color):
        try:
            # colorizing and replacing is just complicated enough
            # that we sometimes screw it up. Don't have the script
            # die just because it cannot colorize
            repl = colorize(r'\g<0>',color)
            newline = re.sub(pattern, ''.join(repl), line)
        except:
            newline = line
        return newline
    
    def grepFile(self, fn, pattern, nocolor=False, context=0, replpat=None, ofn_prefix=None):
        matches = {}
        lcount = 0;
        with open(fn,'r') as ifh:
            lines = ifh.readlines()
            for line in lines:
                if re.search(r'' + pattern, line):
                    if replpat is not None:
                        line = re.sub(pattern,replpat,line)
                        lines[lcount] = line 
    
                    if not nocolor:
                        if replpat is None:
                            line = self.colorize_regex(pattern, line, self.config['grep']['match_color'])
                        else:
                            line = self.colorize_regex(replpat, line, self.config['grep']['repl_color'])
                    matches[lcount] = line
                    for offset in range(context):
                        offset += 1
                        if (lcount + offset) < len(lines) and matches.get(lcount+offset) is None:
                            matches[lcount+offset] = lines[lcount+offset]
                        if (lcount - offset) >= 0         and matches.get(lcount-offset) is None:
                            matches[lcount-offset] = lines[lcount-offset]
                lcount += 1
    
        if ofn_prefix is not None:
            (fndir, fnbase) = os.path.split(fn)
            ofn = os.path.join(fndir,ofn_prefix + fnbase)
            try:
                with open(ofn,'w') as ofh:
                   ofh.write(''.join(lines))
            except Exception as e:
                util.die(repr(e))
    
        return [ (x,matches[x]) for x in sorted(matches.keys()) ]
    
    
    def usage(self, adict):
        repo = adict['repoinfo']['name']
        usage = []
        usage += [
            'g <pattern> [replpattern]',
            '            [-type_specifer(s)]',
            '            [-path_specifier(s)]',
            '            [-fpat=file_pattern]',
            '            [-editor_specifier]',
            '            [-context=num]',
            '            [-f] [-really]',
            ''
        ]
        usage += util.getSpecifierList(self.config,repo)
        usage += [
            '',
            ' * if replpattern is present, each occurence of pattern will be REPLACED',
            '   However, this replacement will not happen for real unless the -really',
            '   or -prefix flags are set. With -prefix, the new files have a new name',
            '   with -really, the files are replaced in-place. Without either, you',
            '   just get a "dry run."',
            ' * context is lines above and below match to show',
            ' * -f means don\'t show the matches, just list the files that contained them',
            ' * options with "(*)" are defaults',
        ]
        return usage


    def run(self, adict):
    
        if len(adict['args']) < 1:
            print('no pattern to search')
            return
        
        replpat = None
        if len(adict['args']) > 1:
            replpat= adict['args'][1]
        
        ofn_prefix = None
        if replpat is not None:
            ofn_prefix = adict.get('prefix',None)
            if ofn_prefix is None and adict.get('really',False):
                ofn_prefix = ''
        
        ftypes = util.makeTypeList(self.config, adict)
        spaths = util.makeSearchPathList(self.config, adict)
    
        fpats = None
        if 'fpat' in adict:
            fpats = [adict['fpat']]
        searchFiles = util.fileGlob(spaths, ftypes, fpats)
    
        context = int(adict.get('context','0'))
        matchfiles = []
        for f in searchFiles:
            fmatches = self.grepFile(f, adict['args'][0], 
                                     nocolor=adict.get('nocolor',False),
                                     context=context,
                                     replpat=replpat,
                                     ofn_prefix=ofn_prefix)
            if len(fmatches):
                matchfiles.append(f)
                if not 'f' in adict:
                    print('')
                    ol = os.path.relpath(f)
                    if not 'nocolor' in adict:
                        ol = colorize(ol, self.config['grep']['file_color'])
                    print(ol)
                    print('')
                    for fmatch in fmatches:
                        print('  {:5} : {}'.format(fmatch[0], fmatch[1].rstrip()))
                else:
                    print(os.path.relpath(f))
    
        util.editFiles(self.config, adict, matchfiles)
