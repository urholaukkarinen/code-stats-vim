[![Build status](https://gitlab.com/code-stats/code-stats-vim/badges/master/build.svg)](https://gitlab.com/code-stats/code-stats-vim/pipelines)
[![Python 3 test coverage](https://gitlab.com/code-stats/code-stats-vim/badges/master/coverage.svg)](https://gitlab.com/code-stats/code-stats-vim/-/jobs/)

# [Code::Stats](https://codestats.net) plugin for Vim

Vim plugin that counts your keypresses and saves statistics to [Code::Stats](https://codestats.net), a free stats tracking service for programmers.

![Screen capture of code-stats-vim logging and sending XP](https://thumbs.gfycat.com/HastyAnxiousBlackfootedferret-size_restricted.gif)

## Requirements

- Vim >= 7.3.1163 or NeoVim
- Python (2.6+ or 3) support

**NOTE:** The version of Vim in **macOS Monterey** (and probably later) is not built with Python support. You will need to install Neovim or Vim yourself to use code-stats-vim.

## Installation

### Easy mode: [vim-plug](https://github.com/junegunn/vim-plug) + [vim-airline](https://github.com/vim-airline/vim-airline)

1) Get a Code::Stats account and copy your API key from the [Code::Stats machine page](https://codestats.net/my/machines).

2) Install [vim-plug](https://github.com/junegunn/vim-plug) if you haven't already.

3) Add the following in your `.vimrc` or `init.vim` (or edit the existing plugin section).

```
call plug#begin('~/.vim/plugged')
" ... your other plugins

Plug 'https://gitlab.com/code-stats/code-stats-vim.git'

" Optional: If you want a nice status line in Vim
Plug 'vim-airline/vim-airline'

call plug#end()
```

4) Run `:PlugUpdate` in Vim to install the new plugins.

5) Add the following settings to the aforementioned file, after `call plug#end()`:

```
" REQUIRED: set your API key
let g:codestats_api_key = 'YOUR_KEY_HERE'

" Optional: configure vim-airline to display status
let g:airline_section_x = airline#section#create_right(['tagbar', 'filetype', '%{CodeStatsXp()}'])
```

7) Start Vim or reload configs and you should be done!

### Advanced

- `g:codestats_api_key` must be set to your API key
- `g:codestats_api_url` may be set to use another Code::Stats server.
- `g:codestats_error` contains an error message when there was an error. When a pulse is successfully sent, the error is cleared.
- `CodeStatsXp()` returns current status as a string, eg. `C::S 57` for 57 unsent XP, or `C::S ERR` if there was an error

## Hacking on `code-stats-vim`

Point vim-plug to a local copy: `Plug '~/code-stats-vim'`. Edit. Run lint with `flake8` and tests with `pytest`.
