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

TESTS=(create resolve)

RANDOM_PORTION=$1

for TEST in "${TESTS[@]}"; do
    echo
    echo "=================================== $TEST ==================================="
    echo
    docker-compose --project-directory "$ROOT_PATH" run -T stress-test run -q -e RANDOM_PORTION="$RANDOM_PORTION" - < "$DIR_PATH/${TEST}.js"
done
