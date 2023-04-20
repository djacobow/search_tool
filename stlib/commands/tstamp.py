import sys, datetime, time, re

try:
    import dateparser
    has_dateparser = True
except:
    has_dateparser = False

try:
    import humanize
    has_humanize = True
except:
    has_humanize = False

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
        args = adict.get('args', [])

        prefix = ""
        utc_dt = None

        utcnow_dt = datetime.datetime.now().astimezone(datetime.timezone.utc)
        if len(args) < 1:
            prefix = "CURRENT "
            utc_dt = utcnow_dt
        elif has_dateparser:
            localzone = datetime.datetime.now().astimezone().tzinfo
            utc_dt = dateparser.parse(" ".join(args), settings={
                'TIMEZONE': str(localzone),
                'TO_TIMEZONE': 'UTC',
                'RETURN_AS_TIMEZONE_AWARE': True,
            })

        # parse as float if we don't have dateparser, or if the dateparser fails
        if not utc_dt:
            ts_str = re.search(r'([\.0-9]+)', adict['args'][0].strip())[1]
            ts = float(ts_str)
            utc_dt = datetime.datetime.fromtimestamp(ts, tz=datetime.timezone.utc)


        def _show(prefix, dt):
            print(f'{prefix}{dt.tzinfo.tzname(None)}  Time {dt.isoformat()[:-6]}')

        print(f'{prefix}UNIX Time {utc_dt.timestamp()}')
        _show(prefix, utc_dt)
        _show(prefix, utc_dt.astimezone())

        if len(args) >= 1:
            delta = utcnow_dt - utc_dt
            if has_humanize:
                humdelta = humanize.time.naturaldelta(delta)
            else:
                humdelta = f"{delta.total_seconds()} seconds"

            if delta.total_seconds() > 0:
                print(f'{humdelta} ago')
            else:
                print(f'{humdelta} from now')
