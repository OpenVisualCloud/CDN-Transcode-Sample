#!/bin/bash -e

DIR=$(dirname $(readlink -f "$0"))
NVODS="${1:-1}"
SCENARIO="${3:-cdn}"
PLATFORM="${4:-Xeon}"
REGISTRY="$5"

rm -rf "$DIR/../../volume/video/cache"
mkdir -p "$DIR/../../volume/video/cache/hls" "$DIR/../../volume/video/cache/dash"

m4 -DNVODS=${NVODS} -DSCENARIO=${SCENARIO} -DPLATFORM=${PLATFORM} -DREGISTRY_PREFIX=${REGISTRY} -I "${DIR}" "${DIR}/docker-compose.yml.m4" > "${DIR}/docker-compose.yml"
