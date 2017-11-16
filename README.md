# [Code::Stats](https://codestats.net) plugin for Vim

## Requirements

- Vim >= 7.3.196 or NeoVim
- Compiled with Python (2.6+ or 3) support

Technical reasons: we use the `InsertCharPre` event in Vim and `multiprocessing` module in Python.

## Installation

Using [vim-plug](https://github.com/junegunn/vim-plug), add the following lines to your config:

```
Plug 'https://gitlab.com/code-stats/code-stats-vim.git'
let g:codestats_api_key = 'YOUR_KEY_HERE'
```

Get the API key from your [Code::Stats machine page](https://codestats.net/my/machines).

You may additionally set `g:codestats_api_url` to use another Code::Stats server.
