#!/bin/bash -e

IMAGE="ovc_transcode_sw"
DIR=$(dirname $(readlink -f "$0"))
OPTIONS=("--volume=${DIR}/../../volume/video/archive:/var/www/archive:ro" "--volume=${DIR}/../../volume/video/dash:/var/www/dash:rw" "--volume=${DIR}/../../volume/video/hls:/var/www/hls:rw")

. "${DIR}/../../script/shell.sh"
