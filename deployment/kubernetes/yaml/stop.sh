#!/bin/bash

DIR=$(dirname $(readlink -f "$0"))
EXT=*.yaml

# Set Bash color
ECHO_PREFIX_INFO="\033[1;32;40mINFO...\033[0;0m"
ECHO_PREFIX_ERROR="\033[1;31;40mError...\033[0;0m"

# Try command  for test command result.
function try_command {
    "$@"
    status=$?
    if [ $status -ne 0 ]; then
        echo -e $ECHO_PREFIX_ERROR "ERROR with \"$@\", Return status $status."
        exit $status
    fi
    return $status
}

try_command hash kubectl > /dev/null

for i in $(find "$DIR" "$DIR/.." -maxdepth 1 -name "*.yaml"); do
    kubectl delete --wait=false -f "$i" 2> /dev/null
done

kubectl delete secret self-signed-certificate 2> /dev/null || echo -n ""
