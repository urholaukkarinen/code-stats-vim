try:
    import vim
except ImportError:
    print("Python package 'vim' not found")
    exit(1)

from multiprocessing import Process, Queue

# make local imports work
import sys
sys.path.append(vim.eval("s:codestats_path"))

from codestats_worker import Worker


API_KEY = vim.eval("g:codestats_api_key")
BASE_URL = (vim.eval("g:codestats_api_url") or "https://codestats.net")
PULSE_URL = BASE_URL + "/api/my/pulses"

def log_xp():
    language = vim.eval("&filetype")
    xp = int(vim.eval("b:codestats_xp"))
    vim.command("let b:codestats_xp = 0")
    queue.put(('xp', (language, xp)))

def stop_loop():
    queue.put(('exit', None))

queue = Queue()
worker = Worker(queue, API_KEY, PULSE_URL)
p = Process(target=worker.run)
p.start()
