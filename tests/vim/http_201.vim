set nocompatible

" load the plugin manually
let g:codestats_api_key = "MOCK_API_KEY"
let g:codestats_api_url = "http://localhost:38080"
runtime! plugin/codestats.vim

edit tests/out/http_201
set filetype=automatedtest
put =CodeStatsXp()
execute "normal! iHelo\<bs>lo world!\<cr>\<esc>"
put =CodeStatsXp()
sleep 1
put =CodeStatsXp()
write
quit
