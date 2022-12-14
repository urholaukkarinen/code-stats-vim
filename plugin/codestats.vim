"
" Vim side file to integrate support for codestats.net
"

" define external function to do nothign
" in case module doesn't initialize properly
function! CodeStatsXp()
    return 'C::S Not Initialized'
endfunction

" get the module path where the python file is located
let s:codestats_path = fnamemodify(resolve(expand('<sfile>:p')), ':h')

" check if the old <= 0.6.0 codebase is loaded (ie. upgrading to >= 1.0.0)
if exists("g:codestats_pending_xp")
    source s:codestats_path . "/old_version.unload"
endif

function! s:init()
    if !has('python3')
        if !has('python')
            echomsg 'Python2/3 support required for vim-codestats'
            finish
        endif
        let s:python = 'python'

        " load up the python file
        execute 'pyfile ' . s:codestats_path . '/init_codestats.py'
    else
        let s:python = 'python3'
        " load up the python file
        execute 'py3file ' . s:codestats_path . '/init_codestats.py'
    endif

    execute s:python . ' init_codestats("' . g:codestats_api_url . '", "' . g:codestats_api_key . '")'
endfunction

" check for variables that are needed and only
" assign them if they are not already assigned
if !exists("g:codestats_api_url")
    let g:codestats_api_url = 'https://codestats.net/'
endif

if !exists("g:codestats_api_key")
    let g:codestats_api_key = ''
endif

" function to transfer XP over to Python - done on buffer write
function! s:flush_xp()
    call s:init()
    if exists("b:current_xp")
        execute s:python . ' codestats.add_xp("' . &filetype . '", ' . b:current_xp . ')'
    endif
    let b:current_xp = 0
endfunction

" local function to add xp
function! s:add_xp()
    if !exists("b:current_xp")
        let b:current_xp = 0
    endif
    let b:current_xp += 1
endfunction

" local function to exit (which will send any remaining xp)
function! s:exit()
    call s:flush_xp()
    execute s:python . ' codestats.exit()'
endfunction

function! codestats#set_error(error)
    if a:error == ''
        if exists("g:codestats_error")
            unlet g:codestats_error
        endif
    else
        let g:codestats_error = a:error
    endif
endfunction

" Send XP NOW. Used for integation tests.
function! codestats#force_send_xp()
    call s:flush_xp()
    execute s:python . ' codestats.send_xp()'
endfunction

" autocommands to keep track of code stats
augroup codestats
    autocmd!
    autocmd InsertCharPre,TextChanged * call s:add_xp()
    autocmd VimLeavePre * call s:exit()
    autocmd BufWrite,BufLeave * call s:flush_xp()
augroup END

function! CodeStatsXp()
    if exists("g:codestats_error")
        return "C::S ERR"
    endif
    if !exists("b:current_xp")
        let b:current_xp = 0
    endif
    return 'C::S ' . b:current_xp
endfunction
