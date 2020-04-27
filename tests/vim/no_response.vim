set nocompatible

" load the plugin manually
let g:codestats_api_key = "MOCK_API_KEY"
let g:codestats_api_url = "http://codestats.invalid"
runtime! plugin/codestats.vim

set filetype=automatedtest
put =CodeStatsXp()
execute "normal! iHelo\<bs>lo world!\<cr>\<esc>"
put =CodeStatsXp()
call codestats#force_send_xp()
sleep 1
put =CodeStatsXp()
put =g:codestats_error

" different libc implementations cause different messages for same error; normalize
%substitute/^\[Errno -2\] Name or service not known$/[Errno 8] nodename nor servname provided, or not known/eg

write
quit
