import re, os

class PathsFn:
    def __init__(self, config):
        self.config = config

    def _makeList(self, adict):
        rv = []
        subpaths = self.config.get('subpaths')
        for k in sorted(subpaths):
            elems = [ adict['repoinfo']['root'] ]  + subpaths[k][1]
            name = subpaths[k][0]
            path = os.path.join(*elems)
            err = '' if os.path.isdir(path) else '[ !! NO EXIST !! ]'
            rv.append(f'{k:10}: {name:12} {path} {err}')
        return rv


    def usage(self, adict):
        scname = adict.get('subcommand')
        usage = []
        usage.append(f'{scname} [ sub_path ]')
        usage.append('')
        usage.append('Known subpaths are: ')
        usage += self._makeList(adict)
        return usage


    def run(self, adict):
        req_key = None
        if len(adict['args']):
            req_key = adict['args'][0]

        if req_key is None:
            req_key = 'rr'

        subpaths = self.config.get('subpaths')

        if req_key in subpaths:
            elems = [ adict['repoinfo']['root'] ]  + subpaths[req_key][1]
            print(os.path.join(*elems))
        else:
            print(f'Unknown path key "{req_key}". I know:')
            print('\n'.join(self._makeList(adict)))
 
