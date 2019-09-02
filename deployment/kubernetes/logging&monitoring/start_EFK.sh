#!/bin/bash -e

DIR=$(dirname $(readlink -f "$0"))

# Try command  for test command result.

# Set Bash color
ECHO_PREFIX_INFO="\033[1;32;40mINFO...\033[0;0m"
ECHO_PREFIX_ERROR="\033[1;31;40mError...\033[0;0m"

function try_command {
    "$@" 2> /dev/null
    status=$?
    if [ $status -ne 0 ]; then
        echo -e $ECHO_PREFIX_ERROR "ERROR with \"$@\", Return status $status."
        exit $status
    fi
    return $status
}

"$DIR/stop_EFK.sh" "$DIR"

set +e
kubectl proxy --address='0.0.0.0' --port=8081 --accept-hosts='^*$' &
try_command hash kubectl > /dev/null

"$DIR/update_EFK.py" "$DIR/"
set -e

for i in $(ls $DIR/*.yaml); do
    kubectl create -f "$i"
done

echo "EFK are running..."
