#!/bin/bash -e

IMAGE="ovc_batch_service"
DIR=$(dirname $(readlink -f "$0"))

. "${DIR}/../script/build.sh"
