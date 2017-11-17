"""Worker that communicates with the Code::Stats API"""

from datetime import datetime, timedelta
import json
import time

# Python 2 and 3 have different modules for urllib2
try:
    from urllib.request import Request, urlopen
    from urllib.error import URLError
except ImportError:
    from urllib2 import Request, urlopen, URLError

from codestats_version import __version__
from codestats_filetypes import get_language_name
from localtz import LOCAL_TZ

SEND_INTERVAL = timedelta(seconds=10)


def get_timestamp():
    return datetime.now().replace(microsecond=0, tzinfo=LOCAL_TZ).isoformat()

def get_xps_list(xps_dict):
    xps_list = []
    for (filetype, xp) in xps_dict.items():
        item = dict(language=get_language_name(filetype), xp=xp)
        xps_list.append(item)
    return xps_list

def get_payload(xps):
    return json.dumps({
        'coded_at': get_timestamp(),
        'xps': get_xps_list(xps)
    }).encode('utf-8')


class Worker:
    def __init__(self, pipe, api_key, pulse_url):
        self.pipe = pipe
        self.api_key = api_key
        self.pulse_url = pulse_url

    def get_headers(self):
        return {
            "Content-Type": "application/json",
            "User-Agent": "code-stats-vim/%s" % __version__,
            "X-API-Token": self.api_key,
            "Accept": "*/*"
        }

    def send_pulse(self, xps):
        req = Request(url=self.pulse_url, data=get_payload(xps), headers=self.get_headers())

        try:
            response = urlopen(req)
            response.read()
            # connection might not be closed without .read()
        except URLError as e:
            # TODO: logging? consecutive error counting?
            # note: response body is in e.read()
            return False
        return True

    def run(self):
        xps = {}
        next_send = datetime.now()

        while True:
            if self.pipe.poll():
                command, args = self.pipe.recv()

                if command == 'xp':
                    language, xp = args
                    if language not in xps:
                        xps[language] = 0
                    xps[language] += xp

                elif command == 'exit':
                    if xps:
                        self.send_pulse(xps)
                    return

            if xps and datetime.now() > next_send:
                next_send = datetime.now() + SEND_INTERVAL

                if self.send_pulse(xps):
                    # clear after successful send; inform the Vim end of pipe
                    total_sent_xp = sum(xps.values())
                    xps = {}
                    self.pipe.send(total_sent_xp)

            time.sleep(0.1) # don't hog CPU idle looping
