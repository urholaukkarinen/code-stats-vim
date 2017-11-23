" Check InsertCharPre support (Vim >= 7.3.186 in practice)
if !exists('##InsertCharPre')
    echomsg 'code-stats-vim requires InsertCharPre support (Vim >= 7.3.186)!'
    finish
endif

" API key: required
if !exists('g:codestats_api_key')
    echomsg 'code-stats-vim requires g:codestats_api_key to be set!'
    finish
endif

" API endpoint
if !exists('g:codestats_api_url')
    let g:codestats_api_url = 'https://codestats.net'
endif

" this script may be run many times; stop timer before reloading Python code
if exists('s:timer')
    call timer_stop(s:timer)
endif

" check Python 2 or 3 support
let s:codestats_path = fnamemodify(resolve(expand('<sfile>:p')), ':h')
if has('python3')
    execute 'py3file ' . s:codestats_path . '/codestats.py'
    let s:python = 'python3'
elseif has('python')
    execute 'pyfile ' . s:codestats_path . '/codestats.py'
    let s:python = 'python'
else
    echomsg 'code-stats-vim requires Python support!'
    finish
endif


" Two XP counters.
" On :PlugUpdate, we intentionally clear pending XP because the worker
" process that was supposed to send it is already gone.
" Buffer-local XP is kept and sent in the future.
let g:codestats_pending_xp = 0      " global total of unsaved XP
if !exists('b:codestats_xp')
    let b:codestats_xp = 0          " buffer-local XP
endif


function! s:add_xp()
    let g:codestats_pending_xp += 1
    let b:codestats_xp += 1
endfunction

function! s:log_xp()
    execute s:python . ' codestats.log_xp()'
endfunction

function! s:exit()
    if exists('s:timer')
        call timer_stop(s:timer)
    endif
    execute s:python . ' del codestats'
endfunction


" Handle Vim events
augroup codestats
    autocmd!

    " STARTUP
    autocmd BufEnter * if !exists('b:codestats_xp') | let b:codestats_xp = 0 | endif

    " ADDING XP: Insert mode
    " Does not fire for newlines or backspaces,
    " TextChangedI could be used instead but some
    " plugins are doing something weird with it that
    " messes up the results.
    autocmd InsertCharPre * call s:add_xp()

    " ADDING XP: Normal mode changes
    autocmd TextChanged * call s:add_xp()

    " LOGGING XP
    autocmd InsertEnter,InsertLeave,BufEnter,BufLeave * call s:log_xp()

    " STOPPING
    autocmd VimLeavePre * call s:exit()
augroup END


" check xp periodically if possible
if has('timers')
    " NOTE: the script cannot be script-local (s:check_xp or such) because
    " the timer could not access it
    function! codestats#check_xp(timer_id)
        execute s:python . ' codestats.check_xp()'
    endfunction

    " run every 500ms, repeat infinitely
    let s:timer = timer_start(500, 'codestats#check_xp', {'repeat': -1})
endif


" export function that returns pending xp like "C::S 13"
function! CodeStatsXp()
    return 'C::S ' . g:codestats_pending_xp
endfunction
