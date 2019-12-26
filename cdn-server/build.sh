#!/bin/bash -e

IMAGE="ovc_cdn_service"
DIR=$(dirname $(readlink -f "$0"))

mkdir -p "/var/log/nginx"
. "${DIR}/../script/build.sh"
