import os, re
from .. import util
    
class Find():
    def __init__(self, config):
        self.config = config
    
    def usage(self, adict):
        usage = [
            'f <pattern1> [pattern2] [-type_specifer(s)] [-path_specifier(s)] [-editor]',
            '',
        ]
        usage += util.getSpecifierList(self.config, adict['repoinfo']['name'])
        usage += [
            '',
            ' * options with "(*)" are defaults',
            ' * pattern1 only is matched on file basename, not the complete path',
            ' * pattern2 is matched anything in the path',
        ]
        return usage

    def run(self, adict):
    
        ftypes = util.makeTypeList(self.config, adict)
        spaths = util.makeSearchPathList(self.config, adict)
        
        fpats = adict['args']
        if not len(fpats):
            print('no patterns to search')
            return
    
        # glob is on the basename only
        found = util.fileGlob(spaths, ftypes, [fpats[0]])

        # you can enforce a subset based on other parts of the path here
        if len(fpats) > 1:
            for pat2 in fpats[1:]:
                found = list(filter(lambda l: re.search(pat2, l), found))
                
        if len(found):
            print('\n'.join(map(os.path.relpath,found)))
    
        util.editFiles(self.config, adict, found)
