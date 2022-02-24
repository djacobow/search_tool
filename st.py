#!/usr/bin/env python3

import os, sys, re, pathlib, subprocess

import stlib

def showCommands(config):
   print('{} - command list:'.format(os.path.basename(sys.argv[0])))
   print('')
   print(' Handy-dandy code search tool and swiss army thingy')
   print('')

   cmdsinfo = config.get('commands',None)
   if not cmdsinfo:
       die('no commands info')

   for cmdn in cmdsinfo:
       cmdinfo = cmdsinfo[cmdn]
       f = '{} - {:20}'.format(cmdn,cmdinfo['description'])
       print(stlib.xterm_colors.colorize(f,{'bold':True,'fg':'cyan'}))
       o = config['commands'][cmdn]['class'](config)
       usage = o.usage({'subcommand':cmdn,'repoinfo':stlib.shell.repoinfo()})
       print('')
       for l in usage:
           print('    {}'.format(l))
       print('')


def args2dict(inlist):
    outdict = {
        'args': []
    }
    for arg in inlist:
        dak_match     = re.match(r'-(\w+)',arg)
        assign_match  = re.match(r'-(\w+)=(.*)',arg)
        if assign_match:
            outdict[assign_match[1]] = assign_match[2]
        elif dak_match:
            outdict[dak_match[1]] = True
        else:
            outdict['args'].append(arg)
    return outdict

        
def run(config):
    cmdname = None

    if len(sys.argv) > 1:
        maybename = sys.argv[1]
        if maybename in config['commands']:
            cmdname = maybename

    if cmdname is not None:
        adict = args2dict(sys.argv[2:])
        adict['subcommand'] = cmdname
        adict['repoinfo'] = stlib.shell.repoinfo()
        o = config['commands'][cmdname]['class'](config)
        o.run(adict)
    else:
        showCommands(config)

def buildConfig():
    def shell(cmd):
        return subprocess.run(cmd, stdout=subprocess.PIPE).stdout.decode('utf-8').strip()

    config_files = [
        os.path.join(os.path.abspath(os.path.dirname(sys.argv[0])),'stlib','base_config.py'),
        os.path.join(shell(['git','rev-parse','--show-toplevel']), '.st_config.py'),
        os.path.join(pathlib.Path.home(),'.st_config.py')
    ]

    configfiles_data = []
    for cfgfile in config_files:
        if os.path.exists(cfgfile):
            try:
                with open(cfgfile, 'r') as ifh:
                    data = ifh.read()
                    results = {}
                    exec(data, results) 
                    configfiles_data.append(results.get('CONFIG',{}))
            except Exception as e:
                stlib.util.die(f'Could not read or process config file {cfgfile} because {repr(e)}')

    combined_config = {}
    for file_data in configfiles_data:
        for top_key, top_blob in file_data.items():
            if not top_key in combined_config:
                combined_config[top_key] = top_blob
            else:
                for second_key, second_blob in top_blob.items():
                    if not second_key in combined_config[top_key]:
                        combined_config[top_key][second_key] = second_blob
                    else:
                        for third_key, third_blob in second_blob.items():
                            combined_config[top_key][second_key][third_key] = third_blob 

    return combined_config


if __name__ == '__main__':
    config = buildConfig()
    run(config)
