if !exists('g:codestats_api_key')
    echomsg 'code-stats-vim requires g:codestats_api_key to be set!'
    finish
endif

let s:codestats_path = fnamemodify(resolve(expand('<sfile>:p')), ':h')
if has('python')
    execute 'pyfile ' . s:codestats_path . '/codestats.py'
elseif has('python3')
    " TODO: ensure the python code works on python3
    execute 'pyfile3 ' . s:codestats_path . '/codestats.py'
else
    finish
endif

" Two XP counters
let g:codestats_pending_xp = 0  " global total of unsaved XP
let b:codestats_xp = 0          " buffer-local XP

function s:add_xp()
    let g:codestats_pending_xp += 1
    let b:codestats_xp += 1
endfunction

" Handle Vim events
augroup codestats
    au!

    " STARTUP
    au BufEnter * if !exists('b:codestats_xp') | let b:codestats_xp = 0 | endif

    " ADDING XP: Insert mode
    " Does not fire for newlines or backspaces,
    " TextChangedI could be used instead but some
    " plugins are doing something weird with it that
    " messes up the results.
    au InsertCharPre * call s:add_xp()

    " ADDING XP: Normal mode changes
    au TextChanged * call s:add_xp()

    " LOGGING XP
    au InsertEnter,InsertLeave,BufEnter,BufLeave * python log_xp()

    " STOPPING
    au VimLeavePre * python stop_worker()
augroup END

" check xp periodically if possible
if has('timers')
    function CodestatsCheckXp(timer_id)
        python check_xp()
    endfunction

    " run every 500ms, repeat infinitely
    let s:timer = timer_start(500, 'CodestatsCheckXp', {'repeat': -1})
endif

function! CodeStatsXp()
    return 'C::S ' . g:codestats_pending_xp
endfunction
