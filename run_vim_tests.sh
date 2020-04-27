#!/bin/sh
set -e

# note: this variable can't be called VIM (it's used to find runtime path in Neovim)
VIM_CMD=${VIM_CMD:-vim}

rm -f tests/out/*

echo "[TEST] no response"
$VIM_CMD -u tests/vim/no_response.vim --cmd "set rtp+=$(pwd)" tests/out/no_response

echo "\n[TEST] HTTP 201"
python3 tests/vim/server.py 201 &
$VIM_CMD -u tests/vim/http_201.vim --cmd "set rtp+=$(pwd)" tests/out/http_201

echo "\n[TEST] HTTP 403"
python3 tests/vim/server.py 403 &
$VIM_CMD -u tests/vim/http_403.vim --cmd "set rtp+=$(pwd)" tests/out/http_403

diff --recursive tests/expected tests/out --exclude .gitignore

exit 0
