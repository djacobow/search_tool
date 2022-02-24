from .. import util
    
class Shell:
    def __init__(self, config):
        self.config = config


    def usage(self, adict):
        scname = adict.get('subcommand')
        usage = []
        usage.append(scname)
        usage += [
            '',
            'alias for:'
        ]
        usage += [ ' '*4 + x for x in self.config['commands'][scname].get('shellcommands',[])]
        return usage


    def run(self, adict):
        scname = adict.get('subcommand')
    
        if scname is None:
            stlib.util.die('unknown subcommand')
    
        if ((scname is not None) and 
            (self.config['commands'].get(scname) is not None) and
            (self.config['commands'][scname].get('shellcommands') is not None) and
            len(self.config['commands'][scname]['shellcommands'])):
            show_name = self.config['commands'][scname].get('show_name',True)
            for args in self.config['commands'][scname]['shellcommands']:
                stlib.shell.shellShowOutput(scname,args,show_name=show_name)
    
