import os
from .. import util
    
class Find():
    def __init__(self, config):
        self.config = config
    
    def usage(self, adict):
        usage = [
            'f <pattern> [-type_specifer(s)] [-path_specifier(s)] [-editor]',
            '',
        ]
        usage += util.getSpecifierList(self.config, adict['repoinfo']['name'])
        usage += [
            '',
            ' * options with "(*)" are defaults',
            ' * pattern only is matched on file basename, not the complete path',
        ]
        return usage

    def run(self, adict):
    
        ftypes = util.makeTypeList(self.config, adict)
        spaths = util.makeSearchPathList(self.config, adict)
        
        fpats = adict['args']
        if not len(fpats):
            print('no patterns to search')
            return
    
        found = util.fileGlob(spaths, ftypes, fpats)
                
        if len(found):
            print('\n'.join(map(os.path.relpath,found)))
    
        util.editFiles(self.config, adict, found)
