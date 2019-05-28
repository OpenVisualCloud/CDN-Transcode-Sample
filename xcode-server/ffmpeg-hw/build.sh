#!/bin/bash -e

IMAGE="ovc_transcode_hw"
DIR=$(dirname $(readlink -f "$0"))

. "${DIR}/../../script/build.sh"
