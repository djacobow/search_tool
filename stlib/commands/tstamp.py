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

    def _timestamp_within_years(self, t, num_years):
        now_sec = time.time()
        years_in_sec = 60 * 60 * 24 * 365 * num_years
        return abs(t - now_sec) < years_in_sec

    def _try_parse_time_int(self, s):
        try:
            orig_ts = float(s)
        except ValueError:
            return None

        # We want to try to intelligently parse both UNIX and GPS timestamps.
        # GPS and UNIX epochs are about 10 years apart, so there's no easy way
        # to distinguish an old UNIX timestamp from a contemporary GPS
        # timestamp. But, let's assume timestamps are often contemporary. So,
        # first check to see if interpreting the timestamp as GPS time gives us
        # a time within 2 years of today. If so, great. If not, interpret as a
        # UNIX-epoch timestamp.
        #
        # Also, try to parse timestamp as s, ms, us, ns
        powers = {
            0: '',
            3: 'milli',
            6: 'micro',
            9: 'nano',
        }
        for power, prefix in powers.items():
            ts = orig_ts / 10**power

            # Try GPS. WARNING, this offset is only valid in 2024-adjacent years unless
            # we bother to write code that handles leap seconds right
            unix_ts_if_gps = ts + 315964782
            if self._timestamp_within_years(unix_ts_if_gps, num_years=2):
                print(f"Assuming original timestamp is GPS-epoch {prefix}sec")
                return datetime.datetime.fromtimestamp(unix_ts_if_gps, tz=datetime.timezone.utc)

            if self._timestamp_within_years(ts, num_years=50):
                print(f"Assuming original timestamp is UNIX-epoch {prefix}sec")
                return datetime.datetime.fromtimestamp(ts, tz=datetime.timezone.utc)

        return None

    def run(self, adict):
        scname = adict.get('subcommand')
        args = adict.get('args', [])

        prefix = ""
        utc_dt = None

        utcnow_dt = datetime.datetime.now().astimezone(datetime.timezone.utc)
        if len(args) == 0:
            prefix = "CURRENT "
            utc_dt = utcnow_dt
        else:
            ts = None
            if len(args) == 1:
                utc_dt = self._try_parse_time_int(adict['args'][0])

            if not utc_dt and has_dateparser:
                localzone = datetime.datetime.now().astimezone().tzinfo
                utc_dt = dateparser.parse(" ".join(args), settings={
                    'TIMEZONE': str(localzone),
                    'TO_TIMEZONE': 'UTC',
                    'RETURN_AS_TIMEZONE_AWARE': True,
                })

            if not utc_dt:
                util.die('can not parse timestamp')

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
