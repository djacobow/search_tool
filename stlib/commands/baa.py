import re, os, pathlib, sys, datetime

from .. import util


class BashAddAlias:
    def __init__(self, config):
        self.config = config


    def usage(self, adict):
        scname = adict.get('subcommand')
        usage = []
        usage.append(scname)
        return usage


    def run(self, adict):
        scname = adict.get('subcommand')
   
        homedir      =  pathlib.Path.home()
        bashrc       =  os.path.join(homedir, '.bashrc')
        bash_aliases =  os.path.join(homedir, '.bash_aliases')
        use_fn = None
        if os.path.exists(bash_aliases):
            use_fn = bash_aliases
        elif os.path.exists(bashrc):
            use_fn = bashrc
       
        if not use_fn:
            util.die('Could not find .bashrc or .bash_aliases to modify.')

        already_installed = False
        try:
            with open(use_fn,'r') as ifh:
                for line in ifh:
                    if re.match(r'# Inserted by st.py',line):
                        already_installed = True
                        break
        except Exception as e:
            util.die('Could not open {} for read because: {}'.format(use_fn, repr(e)))

        if already_installed:
            util.die('st.py already mentioned in {}'.format(use_fn))

        try:
            with open(use_fn, 'a') as ofh:
                our_path= os.path.abspath(sys.argv[0])
                olines = [
                   '# Inserted by st.py at {}'.format(datetime.datetime.now().isoformat()),
                   f"alias st={our_path}"
                   '',
                ]
                ofh.write('\n'.join(olines))
        except Exception as e:
            util.die('Could not open {} for append because: {}'.format(use_fn, repr(e)))

        print('Success! Modified {}'.format(use_fn))
    
