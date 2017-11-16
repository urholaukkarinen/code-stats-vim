try:
    import vim
except ImportError:
    print("Python package 'vim' not found")
    exit(1)

from datetime import datetime, timedelta
import json
import time
from multiprocessing import Process, Queue
import urllib2

# local imports
import sys
sys.path.append(vim.eval("s:codestats_path"))

from localtz import LOCAL_TZ


API_KEY = vim.eval("g:codestats_api_key")
BASE_URL = (vim.eval("g:codestats_api_url") or "https://codestats.net")
PULSE_URL = BASE_URL + "/api/my/pulses"
SEND_INTERVAL = timedelta(seconds=10)

def get_timestamp():
    return datetime.now().replace(microsecond=0, tzinfo=LOCAL_TZ).isoformat()

def loop(q):
    xps = {}
    next_send = datetime.now()

    while True:
        command, args = q.get()
        if command == 'xp':
            language, xp = args
            if language not in xps:
                xps[language] = 0
            xps[language] += xp
        elif command == 'exit':
            return

        if datetime.now() > next_send:
            next_send = datetime.now() + SEND_INTERVAL

            payload = json.dumps({
                'coded_at': get_timestamp(),
                'xps': xps
            })
            headers = {
                "Content-Type": "application/json",
                "User-Agent": "code-stats-vim/poc",
                "X-API-Token": API_KEY
            }
            req = urllib2.Request(url=PULSE_URL, data=payload, headers=headers)
            response = urllib2.urlopen(req)
            # TODO: handle response

            xps = {}

        time.sleep(0.1) # don't hog CPU idle looping


def log_xp():
    language = vim.eval("&filetype")
    xp = int(vim.eval("b:codestats_xp"))
    vim.command("let b:codestats_xp = 0")
    q.put(('xp', (language, xp)))

def stop_loop():
    q.put(('exit', None))

q = Queue()
p = Process(target=loop, args=(q,))
p.start()
