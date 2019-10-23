#!/bin/bash -e

IMAGE="ovc_cdn_service"
DIR=$(dirname $(readlink -f "$0"))

mkdir -p "$DIR/../volume/logs"
. "${DIR}/../script/build.sh"
