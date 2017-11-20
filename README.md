[![Build status](https://gitlab.com/code-stats/code-stats-vim/badges/master/build.svg)](https://gitlab.com/code-stats/code-stats-vim/pipelines)
[![Python 3 test coverage](https://gitlab.com/code-stats/code-stats-vim/badges/master/coverage.svg)](https://gitlab.com/code-stats/code-stats-vim/-/jobs/)

# [Code::Stats](https://codestats.net) plugin for Vim

**Warning:** This plugin is still an early beta. Not recommended for use yet.

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

## Tips

Display pending XP in [vim-airline](https://github.com/vim-airline/vim-airline):

```
let g:airline_section_y = airline#section#create_right(['ffenc','%{CodeStatsXp()}'])
```

## Hacking on `code-stats-vim`

Point vim-plug to a local copy: `Plug '~/code-stats-vim'`. Edit. Run lint with `flake8` and tests with `pytest`.
