#!/bin/sh

if [ -r server.pid ]; then
    kill $(cat server.pid)
    rm server.pid
fi
