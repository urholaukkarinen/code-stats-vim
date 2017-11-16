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

function! s:Xp()
    echom 'Code::Stats XP:' b:codestats_xp
endfunction

augroup codestats
    au!
    au TextChanged * let b:codestats_xp += 1

    " Does not fire for newlines or backspaces,
    " TextChangedI could be used instead but some
    " plugins are doing something weird with it that
    " messes up the results.
    au InsertCharPre * let b:codestats_xp += 1

    " Compensate the lack of xp from newlines and
    " backspaces by gaining xp when entering/leaving
    " insert mode.
    au InsertEnter * let b:codestats_xp += 1
    au InsertLeave * python log_xp()
    au BufWritePost * python stop_loop()
    au BufEnter * if !exists('b:codestats_xp') | let b:codestats_xp = 0 | endif
augroup END

command! Xp :call s:Xp()
