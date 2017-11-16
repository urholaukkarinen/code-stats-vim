let s:codestats_path = fnamemodify(resolve(expand('<sfile>:p')), ':h')

if has('python')
    execute 'pyfile ' . s:codestats_path . '/code-stats-vim.py'
elseif has('python3')
    " TODO: ensure the python code works on python3
    execute 'pyfile3 ' . s:codestats_path . '/code-stats-vim.py'
else
    finish
endif


let b:codestats_xp = 0

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
    au InsertCharPre * let b:codestats_xp += 1

    " ADDING XP: Normal mode changes
    au TextChanged * let b:codestats_xp += 1

    " LOGGING XP
    au InsertLeave * python log_xp()
    au BufLeave * python log_xp()

    " STOPPING
    au VimLeavePre * python stop_loop()
augroup END

function! CodeStatsXp()
    return 'C::S ' . b:codestats_xp
endfunction
