#!/bin/bash -e

IMAGE="ovc_transcode_sw"
DIR=$(dirname $(readlink -f "$0"))

. "${DIR}/../../script/build.sh"
