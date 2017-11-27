#!/bin/sh
set -e

VIM=${VIM:-vim}

rm -f tests/out/*

echo "Test: no response"
$VIM -u tests/vim/no_response.vim --cmd "set rtp+=$(pwd)"
echo "\n"

echo "Test: HTTP 201"
python3 tests/vim/server.py 201 &
$VIM -u tests/vim/http_201.vim --cmd "set rtp+=$(pwd)"
echo "\n"

echo "Test: HTTP 403"
python3 tests/vim/server.py 403 &
$VIM -u tests/vim/http_403.vim --cmd "set rtp+=$(pwd)" tests/out/http_403
echo "\n"

diff --recursive tests/expected tests/out --exclude .gitignore
