#!/bin/bash

includefile=$(dirname "$0")'/include.js'

l(){

	{	
		echo -e "javascript:"
		if [[ $incl -eq 1 ]]; then
			cat "$includefile"
		fi
		cat
	}  | xargs -0 chromix goto
}

if [[ "$1" = '-i' ]]; then
	incl=1
	shift
fi

if [[ $# -eq 0 ]]; then
	cat | l
else
	cat "$1" | l
fi

exit $?