from datetime import datetime, timedelta
import json
import time
import urllib2

from localtz import LOCAL_TZ

SEND_INTERVAL = timedelta(seconds=10)

def get_timestamp():
    return datetime.now().replace(microsecond=0, tzinfo=LOCAL_TZ).isoformat()

class Worker:
    def __init__(self, pipe, api_key, pulse_url):
        self.pipe = pipe
        self.api_key = api_key
        self.pulse_url = pulse_url

    def send_pulse(self, xps):
        payload = json.dumps({
            'coded_at': get_timestamp(),
            'xps': xps
        })
        headers = {
            "Content-Type": "application/json",
            "User-Agent": "code-stats-vim/poc",
            "X-API-Token": self.api_key
        }

        req = urllib2.Request(url=self.pulse_url, data=payload, headers=headers)

        try:
            urllib2.urlopen(req)
        except urllib2.URLError:
            # TODO: logging? consecutive error counting?
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
