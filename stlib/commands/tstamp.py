import sys, datetime, time, re


from .. import util

class TSDecoder:
    def __init__(self, config):
        self.config = config


    def usage(self, adict):
        scname = adict.get('subcommand')
        usage = []
        usage.append(scname)
        return usage


    def run(self, adict):
        scname = adict.get('subcommand')
  
        if len(adict.get('args',[])) < 1:
            now = time.time()
            adict['args'].append(now)
            print(f'Returning the CURRENT time: {now}')

        try:
            ts_str = re.search(r'([\.0-9]+)', adict['args'][0].strip())[1]
            ts = float(ts_str)
        except Exception as e:
            print(f'-Error- {repr(e)}')
            return   

        t = datetime.datetime.fromtimestamp(ts, tz=datetime.timezone.utc)
        ts = re.sub(r'\+[\d:]+$','',t.isoformat())
        print(f'{t.tzinfo.tzname(None)} Time: {ts}')
    
        ltz = datetime.datetime.now(datetime.timezone.utc).astimezone().tzinfo
        lt  = t + ltz.utcoffset(None)
        lts = re.sub(r'\+[\d:]+$','',lt.isoformat())
        print(f'{ltz.tzname(None)} Time: {lts}')
