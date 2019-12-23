#!/bin/bash -e

DIR=$(dirname $(readlink -f "$0"))

# Set Bash color
ECHO_PREFIX_INFO="\033[1;32;40mINFO...\033[0;0m"
ECHO_PREFIX_ERROR="\033[1;31;40mError...\033[0;0m"

# Try command for test command result
function try_command {
    "$@" 2> /dev/null
    status=$?
    if [ $status -ne 0 ]; then
        echo -e $ECHO_PREFIX_ERROR "ERROR with \"$@\", Return status $status."
        exit $status
    fi
    return $status
}

"$DIR/stop_alerting.sh"

set +e
try_command hash kubectl > /dev/null
set -e

kubectl create -f "$DIR/namespace/namespace.yaml"

for i in $(find "$DIR" -path "$DIR/namespace" -a -prune -o -name "*.yaml" -print); do
    kubectl create -f "$i"
done

echo "Prometheus are running..."
