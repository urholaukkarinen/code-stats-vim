[![Build status](https://gitlab.com/code-stats/code-stats-vim/badges/master/build.svg)](https://gitlab.com/code-stats/code-stats-vim/pipelines)
[![Python 3 test coverage](https://gitlab.com/code-stats/code-stats-vim/badges/master/coverage.svg)](https://gitlab.com/code-stats/code-stats-vim/-/jobs/)

# [Code::Stats](https://codestats.net) plugin for Vim

Vim plugin that counts your keypresses and saves statistics to [Code::Stats](https://codestats.net), a free stats tracking service for programmers.

![Screen capture of code-stats-vim logging and sending XP](https://thumbs.gfycat.com/HastyAnxiousBlackfootedferret-size_restricted.gif)

## Installation

Using [vim-plug](https://github.com/junegunn/vim-plug), add the following lines to your config:

```
Plug 'https://gitlab.com/code-stats/code-stats-vim.git'
let g:codestats_api_key = 'YOUR_KEY_HERE'
```

Get the API key from your [Code::Stats machine page](https://codestats.net/my/machines).

You may additionally set `g:codestats_api_url` to use another Code::Stats server.

## Requirements

- Vim >= 7.3.196 or NeoVim
- Compiled with Python (2.6+ or 3) support

Technical reasons: we use the `InsertCharPre` event in Vim and `multiprocessing` module in Python.

## Tips

Display pending XP in [vim-airline](https://github.com/vim-airline/vim-airline):

```
let g:airline_section_x = airline#section#create_right(['tagbar', 'filetype', '%{CodeStatsXp()}'])
```

If there was an error (eg. no network connection, invalid API key), `CodeStatsXp()` returns `C::S ERR`. An error message can be seen in `g:codestats_error`. When a pulse is successfully sent, the error is cleared.

## Hacking on `code-stats-vim`

Point vim-plug to a local copy: `Plug '~/code-stats-vim'`. Edit. Run lint with `flake8` and tests with `pytest`.
