#!/bin/bash

if ! pgrep 'server.py'; then
	./server.py &> /dev/null &
	echo "Server started."
	exit 0
else
	echo "Server is already running!"
	exit 1
fi
