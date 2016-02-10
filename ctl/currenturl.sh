#!/bin/bash

if [[ $# -eq 0 ]]; then
	chromix url
	exit $?
fi

chromix goto $1
exit $?
	
