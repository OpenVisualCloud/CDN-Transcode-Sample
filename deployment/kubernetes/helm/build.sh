#!/bin/bash -e

DIR=$(dirname $(readlink -f "$0"))
NVODS="${1:-1}"
NLIVES="${2:-1}"
REGISTRY="$3"
HOSTIP=$(ip route get 8.8.8.8 | awk '/ src /{split(substr($0,index($0," src ")),f);print f[2];exit}')

# make sure helm is functional
helm version >/dev/null 2>/dev/null || exit 0

echo "Generating helm chart"
. "${DIR}/../volume-info.sh"
m4 -DREGISTRY_PREFIX=${REGISTRY} -DNVODS=${NVODS} -DNLIVES=${NLIVES} -DUSERID=$(id -u) -DGROUPID=$(id -g) -DHOSTIP=${HOSTIP} $(env | grep _VOLUME_ | sed 's/^/-D/') -I "${DIR}/cdn-transcode" "$DIR/cdn-transcode/values.yaml.m4" > "$DIR/cdn-transcode/values.yaml"

