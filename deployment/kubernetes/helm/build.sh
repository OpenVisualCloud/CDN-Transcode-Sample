#!/bin/bash -e

DIR=$(dirname $(readlink -f "$0"))
NVODS="${1:-1}"
NLIVES="${2:-1}"
REGISTRY="$3"
HOSTIP=$(ip route get 8.8.8.8 | awk '/ src /{split(substr($0,index($0," src ")),f);print f[2];exit}')

if [ ! -x /usr/bin/helm ] && [ ! -x /usr/local/bin/helm ]; then
    exit 0
fi 

echo "Generating helm chart"
. "${DIR}/../volume-info.sh"
m4 -DREGISTRY_PREFIX=${REGISTRY} -DNVODS=${NVODS} -DNLIVES=${NLIVES} -DUSERID=$(id -u) -DGROUPID=$(id -g) -DHOSTIP=${HOSTIP} $(env | grep _VOLUME_ | sed 's/^/-D/') -I "${DIR}/cdn-transcode" "$DIR/cdn-transcode/values.yaml.m4" > "$DIR/cdn-transcode/values.yaml"

