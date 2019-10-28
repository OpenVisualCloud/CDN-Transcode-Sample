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

"$DIR/stop_EFK.sh"

set +e
try_command hash kubectl > /dev/null

try_command kubectl create secret generic kibana-ssl-certificates --namespace=kube-system --from-file=self.key="$DIR/../../../self-certificates/self.key" --from-file=self.crt="$DIR/../../../self-certificates/self.crt" --from-file=dhparam.pem="$DIR/../../../self-certificates/dhparam.pem" --dry-run -o yaml > "$DIR/kibana-ssl-certificates.yaml"
set -e

"$DIR/update_EFK.py" "$DIR/"

for i in $(ls $DIR/*.yaml); do
    kubectl create -f "$i"
done

echo "EFK are running..."
