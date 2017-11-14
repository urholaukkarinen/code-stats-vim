#!/usr/bin/env python

DEFAULT_URL = "https://codestats.net/api/my/pulses"

try:
    import vim
    import datetime
    import json
    import requests

    def get_timestamp():
        return datetime.datetime.now().replace(microsecond=0).isoformat()

    xp = vim.eval("b:codestats_xp")
    if xp != '0':
        language = vim.eval("&filetype")
        payload = {
            'coded_at': get_timestamp(),
            'xps': {'language': language, 'xp': xp}
        }
        print(json.dumps(payload))
        vim.command("let b:codestats_xp = 0")
except ImportError:
    print("Python package 'vim' not found")
