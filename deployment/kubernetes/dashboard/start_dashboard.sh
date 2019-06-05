#!/bin/bash -e

DIR=$(dirname $(readlink -f "$0"))

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

# This script must be run as root
if [[ $EUID -ne 0 ]]; then
    echo -e $ECHO_PREFIX_ERROR "This script must be run as root!" 1>&2
    exit 1
fi

try_command hash kubectl > /dev/null

for i in $(find "$DIR" -name "*service.yaml"); do
    len=$(echo $DIR | wc -m)
    i1=$(echo ${i:${len}} | sed 's/-service.yaml//')
    for j in $(kubectl get svc -A | awk '{print $2}' | sed -n '2, $p' | grep -v 'kubernetes$\|kube-dns'); do
        if [ "$i1" == "$j" ]; then
            kubectl delete -f "$i"
        fi
    done
done

"$DIR/update_dashboard.py" "$DIR/../"

for i in $DIR; do
    kubectl apply -f "$i"
done
