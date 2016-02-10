#!/bin/bash

if [[ $# -eq 0 ]]; then
	chromix list | cut -d " " -f 3-
	exit $?
fi

exit 1
	
