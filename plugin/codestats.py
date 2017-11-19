# -*- coding: utf-8 -*-
"""Vim-specific functionality"""

try:
    import vim
except ImportError:
    print("Python package 'vim' not found")
    exit(1)

import sys
import multiprocessing

# make local imports work
codestats_path = vim.eval("s:codestats_path")
if codestats_path not in sys.path:
    sys.path.append(codestats_path)
del codestats_path


class Codestats(object):
    def __init__(self):
        """Start a worker process"""
        from codestats_worker import Worker

        API_KEY = vim.eval("g:codestats_api_key")
        BASE_URL = vim.eval("g:codestats_api_url")
        PULSE_URL = BASE_URL + "/api/my/pulses"

        self.pipe, worker_pipe = multiprocessing.Pipe()
        worker = Worker(worker_pipe, API_KEY, PULSE_URL)
        p = multiprocessing.Process(target=worker.run)
        p.start()

    def log_xp(self):
        """Log XP (send to the worker process)"""
        language = vim.eval("&filetype")
        xp = int(vim.eval("b:codestats_xp"))
        if xp > 0:
            vim.command("let b:codestats_xp = 0")
            self.pipe.send(('xp', (language, xp)))
        # always also check xp
        self.check_xp()

    def check_xp(self):
        """Check if xp has been saved; if so, deduct from global pending xp"""
        while self.pipe.poll():
            sent_xp = self.pipe.recv()
            vim.command("let g:codestats_pending_xp -= %d" % sent_xp)

    def stop_worker(self):
        """Stop the worker process"""
        self.pipe.send(('exit', None))
        # FIXME: this is often too slow


# guard: don't create a new instance on :PlugUpdate
if "codestats" not in globals():
    codestats = Codestats()
# TODO: implement hot reloading or such, ie. updating plugin on the fly
