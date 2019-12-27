#!/bin/bash -e

IMAGE="ovc_cdn_service"
DIR=$(dirname $(readlink -f "$0"))

. "${DIR}/../script/build.sh"
