try:
    import vim
except ImportError:
    print("Python package 'vim' not found")
    exit(1)

from multiprocessing import Process, Pipe

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
    if xp > 0:
        vim.command("let b:codestats_xp = 0")
        pipe.send(('xp', (language, xp)))

    # check if xp has been saved; if so, deduct from global pending xp
    if pipe.poll():
        sent_xp = pipe.recv()
        vim.command("let g:codestats_pending_xp -= %d" % sent_xp)

def stop_loop():
    pipe.send(('exit', None))

pipe, worker_pipe = Pipe()
worker = Worker(worker_pipe, API_KEY, PULSE_URL)
p = Process(target=worker.run)
p.start()
