from .. import util
from .. import shell
    
class Exec:
    def __init__(self, config):
        self.config = config

    def usage(self, adict):
        scname = adict.get('subcommand')
        usage = []
        usage.append(scname)
        usage += [
            '',
            'execs :'
        ]
        usage += [ ' '*4 + self.config['commands'][scname].get('exec_command')]
        return usage


    def run(self, adict):
        scname = adict.get('subcommand')

        if scname is None:
            stlib.util.die('unknown subcommand')
    
        if ((scname is not None) and 
            (self.config['commands'].get(scname) is not None) and
            (self.config['commands'][scname].get('command') is not None)):

            # if number of provided arguments is less than the number
            # in the defaults, substitute the defaults
            default_args = self.config['commands'][scname].get('default_args',[])
            for i in range(len(default_args)):
                if len(adict['args']) -1 < i:
                    adict['args'].append(default_args[i])

            args = { f'a{idx}': adict['args'][idx] for idx in range(len(adict['args'])) }

            a = [ x.format(**args) for x in self.config['commands'][scname].get('args',[]) ]
            cmd = self.config['commands'][scname].get('command').format(**args)
            shell.shellDetach([cmd] + a)
    
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
                shell.shellShowOutput(scname,args,show_name=show_name)
    
