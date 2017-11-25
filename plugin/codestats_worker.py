# -*- coding: utf-8 -*-

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
    """Get current time in ISO 8601 format with local timezone"""
    return datetime.now().replace(microsecond=0, tzinfo=LOCAL_TZ).isoformat()


def get_xps_list(xps_dict):
    """Convert XPs from internal format to API format"""
    xps_list = []
    for (filetype, xp) in xps_dict.items():
        item = dict(language=get_language_name(filetype), xp=xp)
        xps_list.append(item)
    return xps_list


def get_payload(xps):
    """Create Pulse data given XPs"""
    return json.dumps({
        'coded_at': get_timestamp(),
        'xps': get_xps_list(xps)
    }).encode('utf-8')


class Worker(object):
    """Worker that communicates with the Code::Stats API"""

    def __init__(self, pipe, api_key, pulse_url):
        self.pipe = pipe
        self.api_key = api_key
        self.pulse_url = pulse_url
        self.xps = {}

    def get_headers(self):
        """Get HTTP headers used for the API"""
        return {
            "Content-Type": "application/json",
            "User-Agent": "code-stats-vim/%s" % __version__,
            "X-API-Token": self.api_key,
            "Accept": "*/*"
        }

    def _send_pulse(self, xps):
        """Send XP to the Pulses API"""
        req = Request(url=self.pulse_url,
                      data=get_payload(xps),
                      headers=self.get_headers())

        try:
            response = urlopen(req)
            response.read()
            # connection might not be closed without .read()
        except URLError as e:
            try:
                # HTTP error
                return (False, "%d %s" % (e.code, e.read().decode("utf-8")))
            except AttributeError:
                # non-HTTP error, eg. no network
                return (False, e.reason)
        return (True, None)

    def send_xp(self):
        """Send XP to API, communicate sent XP to parent process"""
        if self.xps:
            success, error = self._send_pulse(self.xps)
            if success:
                # clear after successful send
                total_sent_xp = sum(self.xps.values())
                self.xps = {}
                self.pipe.send((True, total_sent_xp))
            else:
                self.pipe.send((False, str(error)))

    def run(self):
        """Main loop: listen to events, send pulses"""
        next_send = datetime.now()

        while True:
            # handle all events in pipe (usually there's at most one)
            while self.pipe.poll():
                command, args = self.pipe.recv()

                if command == 'xp':
                    language, xp = args
                    if language not in self.xps:
                        self.xps[language] = 0
                    self.xps[language] += xp

                elif command == 'exit':
                    self.send_xp()
                    return

            # check if it's time to send and there's pending XP
            if self.xps and datetime.now() > next_send:
                next_send = datetime.now() + SEND_INTERVAL
                self.send_xp()

            time.sleep(0.1)  # don't hog CPU idle looping
