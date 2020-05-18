#!/bin/bash -e

DIR=$(dirname $(readlink -f "$0"))

function create_secret {
    kubectl create secret generic self-signed-certificate "--from-file=${DIR}/../../certificate/self.crt" "--from-file=${DIR}/../../certificate/self.key"
}

# create secrets
REGISTRY="$4"
"$DIR/../../certificate/self-sign.sh" "$REGISTRY"
create_secret 2>/dev/null || (kubectl delete secret self-signed-certificate; create_secret)

for yaml in $(find "$DIR" -maxdepth 1 -name "*-pv.yaml" -print); do
    kubectl apply -f "$yaml"
done
helm install cdn-transcode "$DIR/cdn-transcode"
