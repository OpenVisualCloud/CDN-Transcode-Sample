#!/bin/bash -e

DIR=$(dirname $(readlink -f "$0"))

function create_secret {
    kubectl create secret generic self-signed-certificate "--from-file=${DIR}/../../certificate/self.crt" "--from-file=${DIR}/../../certificate/self.key"
}

# create secrets
"$DIR/../../certificate/self-sign.sh"
create_secret 2>/dev/null || (kubectl delete secret self-signed-certificate; create_secret)

kubectl apply -f "$DIR"/*-pv.yaml
helm install smtc "$DIR/cdn-transcode"
