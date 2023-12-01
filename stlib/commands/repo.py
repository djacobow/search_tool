from .. import shell
import json
    
class Info:
    def __init__(self, config):
        self.config = config

    def usage(self, adict):
        usage = [
            'prints the current repo information',
        ]
        return usage


    def run(self, adict):
        print(json.dumps(shell.repoinfo(), indent=2, sort_keys=True))
    
    
