#!/bin/sh
set -e

if [ ! -f server.pid ]; then
    python3 tests/vim/server.py &
    echo $! > server.pid
fi

# note: this variable can't be called VIM (it's used to find runtime path in Neovim)
VIM_CMD=${VIM_CMD:-vim}

rm -f tests/out/*

echo "[TEST] no response"
$VIM_CMD -u tests/vim/no_response.vim --cmd "set rtp+=$(pwd)"

echo "\n[TEST] HTTP 201"
$VIM_CMD -u tests/vim/http_201.vim --cmd "set rtp+=$(pwd)"

echo "\n[TEST] HTTP 403"
$VIM_CMD -u tests/vim/http_403.vim --cmd "set rtp+=$(pwd)"

diff --recursive tests/expected tests/out --exclude .gitignore

exit 0
