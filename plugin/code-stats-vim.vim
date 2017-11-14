if !has('python')
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
    au InsertLeave * let b:codestats_xp += 1
    au BufWritePost * pyfile ./plugin/code-stats-vim.py
    au BufEnter * if !exists('b:codestats_xp') | let b:codestats_xp = 0 | endif
augroup END

command! Xp :call s:Xp()
