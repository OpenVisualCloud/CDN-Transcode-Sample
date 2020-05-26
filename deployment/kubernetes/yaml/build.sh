#!/bin/bash -e

DIR=$(dirname $(readlink -f "$0"))
NVODS="${1:-1}"
NLIVES="${2:-1}"
REGISTRY="$3"
HOSTIP=$(ip route get 8.8.8.8 | awk '/ src /{split(substr($0,index($0," src ")),f);print f[2];exit}')

. "${DIR}/../volume-info.sh"
for template in $(find "${DIR}" -maxdepth 1 -name "*.yaml.m4" -print); do
    m4 -DNVODS=${NVODS} -DNLIVES=${NLIVES} -DHOSTIP=${HOSTIP} -DREGISTRY_PREFIX=${REGISTRY} $(env | grep _VOLUME_ | sed 's/^/-D/') -I "${DIR}" "${template}" > "${template/.m4/}"
done
