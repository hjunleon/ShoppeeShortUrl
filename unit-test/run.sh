#!/usr/bin/env bash

compatible_realpath () {
	if command -v realpath &> /dev/null
	then
		realpath "$1"
	else
		[[ $1 = /* ]] && echo "$1" || echo "$PWD/${1#./}"
	fi
}

FILE_PATH=$( compatible_realpath "$0" )
DIR_PATH=$( dirname "$FILE_PATH" )
ROOT_PATH=$( dirname "$DIR_PATH" )

docker-compose --project-directory "$ROOT_PATH" run -T short-url sh -c "python3 -m unittest"
