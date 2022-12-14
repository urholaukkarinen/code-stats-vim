set nocompatible

" load the plugin manually
let g:codestats_api_key = "MOCK_API_KEY"
let g:codestats_api_url = "http://localhost:38080/403/"
runtime! plugin/codestats.vim

set filetype=automatedtest
put =CodeStatsXp()
execute "normal! iHelo\<bs>lo world!\<cr>\<esc>"
put =CodeStatsXp()
call codestats#force_send_xp()
sleep 1
put =CodeStatsXp()
put =g:codestats_error

write tests/out/http_403
quit
