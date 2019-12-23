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

# This script must be run as root
if [[ $EUID -ne 0 ]]; then
    echo -e $ECHO_PREFIX_ERROR "This script must be run as root!" 1>&2
    exit 1
fi

set +e
try_command hash kubectl > /dev/null

if (kubectl get namespace | awk '{print $1}' | grep -q "pgmon"); then
    kubectl delete -f "$DIR/namespace/namespace.yaml"

    for i in $(find "$DIR" -path "$DIR/namespace" -a -prune -o -name "*.yaml" -print); do
        kubectl delete -f "$i" &> /dev/null
    done
fi
set -e

echo "Prometheus are stopping..."
