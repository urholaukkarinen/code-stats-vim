DEFAULT_URL = "https://codestats.net/api/my/pulses"

try:
    import vim
except ImportError:
    print("Python package 'vim' not found")
    exit(1)

from datetime import datetime
import json
import time
from multiprocessing import Process, Queue

# local imports
import sys
sys.path.append(vim.eval("s:codestats_path"))

from localtz import LOCAL_TZ

def get_timestamp():
    return datetime.now().replace(microsecond=0, tzinfo=LOCAL_TZ).isoformat()

def loop(q):
    while True:
        command, args = q.get()
        if command == 'xp':
            with open('/tmp/vimout', 'a') as f:
                payload = {
                    'coded_at': get_timestamp(),
                    'xps': {'language': args['language'], 'xp': args['xp']}
                }
                f.write(json.dumps(payload) + "\n")
        elif command == 'exit':
            return

def log_xp():
    language = vim.eval("&filetype")
    xp = vim.eval("b:codestats_xp")
    vim.command("let b:codestats_xp = 0")
    q.put(('xp', {'xp': xp, 'language': language}))

def stop_loop():
    q.put(('exit', None))

q = Queue()
p = Process(target=loop, args=(q,))
p.start()
