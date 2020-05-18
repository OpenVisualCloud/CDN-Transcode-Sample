#!/bin/bash -e

DIR=$(dirname $(readlink -f "$0"))
NVODS="${1:-1}"
REGISTRY="$3"

m4 -DNVODS=${NVODS} -DREGISTRY_PREFIX=${REGISTRY} -I "${DIR}" "${DIR}/docker-compose.yml.m4" > "${DIR}/docker-compose.yml"
