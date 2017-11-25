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
        self.process = multiprocessing.Process(target=worker.run)
        self.process.start()

    def __del__(self):
        """Stop the worker process and clean up"""
        # stop worker loop, wait for the process to stop
        self.pipe.send(('exit', None))
        # worker process sends back xp saved on exit
        self.check_xp()
        self.process.join()

    def log_xp(self, language, xp):
        """Log XP (send to the worker process)"""
        if xp > 0:
            self.pipe.send(('xp', (language, xp)))

    def check_xp(self):
        """Check if xp has been saved; if so, deduct from global pending xp

        If there was an error, save error message in g:codestats_error
        """
        sent_xp = 0
        error = None
        while self.pipe.poll():
            success, data = self.pipe.recv()
            if success:
                sent_xp += data
            else:
                error = data

        if sent_xp > 0:
            vim.command("call s:xp_was_sent(%d)" % sent_xp)
        if error is not None:
            vim.command("let g:codestats_error = '%s'" %
                        error.replace("'", "''"))


# on :PlugUpdate, unload the old instance before setting up a new one
if "codestats" in globals():
    # assumption: refcount is zero after this
    del codestats

codestats = Codestats()
